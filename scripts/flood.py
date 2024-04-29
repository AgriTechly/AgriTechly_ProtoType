from flask import Blueprint, render_template, request
#from keras.models import load_model
import random
import numpy as np
import os
from scripts.news import get_news


flood_pred = Blueprint('flood_pred', __name__, template_folder='dist', static_folder='static')

news = get_news()
#script_dir = os.path.dirname(os.path.abspath(__file__))
#model_path = os.path.join(script_dir, 'models', 'FloodPred.h5')
    
#model = load_model(model_path)
#model.make_predict_function()

def predict_label(input_data):
    #result = model.predict(np.array(input_data))
    #probability = np.max(result[0], axis=-1)*100
    probability = random.uniform(0, 100)
    if probability < 50:
        predicted_class_name = "No Flood"
    else :
        predicted_class_name = "Flood"
    return predicted_class_name


# routes
@flood_pred.route("/models/flood", methods=['GET', 'POST'])
def kuch_bhi():
    return render_template("/models/flood.html",news=news)

@flood_pred.route("/flood/submit", methods = ['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
		# get all inputs from the form
        input_data = []
        input_data.append(request.form['mi'])
        input_data.append(request.form['td'])
        input_data.append(request.form['rm'])
        input_data.append(request.form['d'])
        input_data.append(request.form['u'])
        input_data.append(request.form['cc'])
        input_data.append(request.form['dq'])
        input_data.append(request.form['s'])
        input_data.append(request.form['ap'])
        input_data.append(request.form['e'])
        input_data.append(request.form['idp'])
        input_data.append(request.form['ds'])
        input_data.append(request.form['cv'])
        input_data.append(request.form['ls'])
        input_data.append(request.form['ws'])
        input_data.append(request.form['di'])
        input_data.append(request.form['ps'])
        input_data.append(request.form['ws'])
        input_data.append(request.form['ip'])
        input_data.append(request.form['pf'])
        input_data = [float(i) for i in input_data]
        input_data = np.array([input_data])
        p = predict_label(input_data)
        
        return render_template("models/flood.html", prediction = p, news=news)

    return render_template("models/flood.html",news=news)