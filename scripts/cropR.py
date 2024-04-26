from flask import Blueprint, render_template, request
import joblib
from joblib import load, dump
import numpy as np
import os
from scripts.news import get_news


cropR = Blueprint('crop_rec', __name__, template_folder='dist', static_folder='static')

news = get_news()
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'models', 'CropRec.joblib')
    
model = load(model_path)
dict = {
    0 : 'rice',
    1 : 'maize',
    2 : 'chickpea',
    3 : 'kidneybeans',
    4 : 'pigeonpeas',
    5 : 'mothbeans',
    6 : 'mungbean',
    7 : 'blackgram',
    8 : 'lentil',
    9 : 'pomegranate',
    10: 'banana',
    11: 'mango',
    12: 'grapes',
    13: 'watermelon',
    14: 'muskmelon',
    15: 'apple',
    16: 'orange',
    17: 'papaya',
    18: 'coconut',
    19: 'cotton',
    20: 'jute',
    21: 'coffee'
}
def predict_label(input_data):
    result = model.predict(np.array(input_data))
    # get the predicted class name
    predicted_class_name = dict[result[0]]
    return predicted_class_name

# routes
@cropR.route("/models/cropR", methods=['GET', 'POST'])
def kuch_bhi():
    return render_template("/models/cropR.html", news=news)

@cropR.route("/cropR/submit", methods = ['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
		# get the data from inputs
        input_data = []
        input_data.append(request.form['n'])
        input_data.append(request.form['p'])
        input_data.append(request.form['k'])
        input_data.append(request.form['t'])
        input_data.append(request.form['h'])
        input_data.append(request.form['ph'])
        input_data.append(request.form['rain'])
        input_data = [float(i) for i in input_data]
        input_data = np.array([input_data])
        p = predict_label(input_data)
        
        return render_template("models/cropR.html", prediction = p, news=news)

    return render_template("models/cropR.html", news=news)