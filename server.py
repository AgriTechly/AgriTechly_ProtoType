"""
this file is the server of the project
"""

# import the necessary packages
from flask import Flask, request, jsonify, render_template, redirect
import subprocess
import json
import os
import sys
import locale

# Set the locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Set environment variables
os.environ['LC_ALL'] = 'en_US.UTF-8'
os.environ['LANG'] = 'en_US.UTF-8'

sys.path.append('/venv/Lib/site-packages')

app = Flask(__name__, template_folder='dist', static_folder='static')

# setup wsgi object
wsgi_app = app.wsgi_app

@app.route('/')
def index():
    # print current directory
    return render_template('index.html')
@app.route('/index')
def index2():
    # print current directory
    return render_template('index.html')
@app.route('/chat')
def chat():
    # print current directory
    return redirect("http://127.0.0.1:3000")
@app.route('/models')
def models():
    # print current directory
    return render_template('models.html')
@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'pimage' in request.files:
            uploaded_file = request.files['pimage']
            print(uploaded_file)
            if uploaded_file:
                # Save the uploaded file
                uploaded_file.save('uploaded_image.jpg')

                current_dir = os.getcwd()
                # change \ to / in current dir
                current_dir = current_dir.replace("\\", "/")
                # Run plant prediction script
                subprocess.run(['python', current_dir+'/scripts/predict_plant.py', 'uploaded_image.jpg'])

                # Read the result from the JSON file
                with open(current_dir+'/scripts/results/result_plants.json') as json_file:
                    result_dict = json.load(json_file)

                # Return the result as JSON
                return jsonify({'success': True, 'message': 'File uploaded and processed successfully', 'result': result_dict})
            else:
                return jsonify({'success': False, 'message': 'No file uploaded'})
        if 'bimage' in request.files:
            uploaded_file = request.files['bimage']
            print(uploaded_file)
            if uploaded_file:
                # Save the uploaded file
                uploaded_file.save('uploaded_image.jpg')

                current_dir = os.getcwd()
                # change \ to / in current dir
                current_dir = current_dir.replace("\\", "/")
                # Run plant prediction script
                subprocess.run(['python', current_dir+'/scripts/predict_bee.py', 'uploaded_image.jpg'])

                # Read the result from the JSON file
                with open(current_dir+'/scripts/results/result_bee.json') as json_file:
                    result_dict = json.load(json_file)

                # Return the result as JSON
                return jsonify({'success': True, 'message': 'File uploaded and processed successfully', 'result': result_dict})
            else:
                return jsonify({'success': False, 'message': 'No file uploaded'})
        if 'wimage' in request.files:
            uploaded_file = request.files['wimage']
            print(uploaded_file)
            if uploaded_file:
                # Save the uploaded file
                uploaded_file.save('uploaded_image.jpg')

                current_dir = os.getcwd()
                # change \ to / in current dir
                current_dir = current_dir.replace("\\", "/")
                # Run plant prediction script
                subprocess.run(['python', current_dir+'/scripts/predict_weed.py', 'uploaded_image.jpg'])

                # Read the result from the JSON file
                with open(current_dir+'/scripts/results/result_weed.json') as json_file:
                    result_dict = json.load(json_file)

                # Return the result as JSON
                return jsonify({'success': True, 'message': 'File uploaded and processed successfully', 'result': result_dict})
            else:
                return jsonify({'success': False, 'message': 'No file uploaded'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e), 'trace': 'exception'})
    
if __name__ == '__main__':
    app.run(debug=True,port=5500)
