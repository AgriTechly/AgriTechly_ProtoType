from flask import Blueprint, render_template, request
from keras.models import load_model
import numpy as np
import os
from scripts.news import get_news


water = Blueprint('water', __name__, template_folder='dist', static_folder='static')

news = get_news()
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'models', 'water.h5')
    
model = load_model(model_path)
model.make_predict_function()

def predict_label(input_data):
    result = model.predict(np.array(input_data))
    probability = np.max(result[0], axis=-1)*100
    if probability < 33:
        predicted_class_name = "Not For drinking or Irrigation"
    elif probability < 67:
        predicted_class_name = "For Irrigation but not for drinking"
    else :
        predicted_class_name = "For Drinking and Irrigation"
    return predicted_class_name


# routes
@water.route("/models/water", methods=['GET', 'POST'])
def kuch_bhi():
    return render_template("/models/water.html")

@water.route("/water/submit", methods = ['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
		# get the data from inputs
        input_data = request.form['inputs']
        input_data = input_data.split(',')
        input_data = [float(i) for i in input_data]
        input_data = np.array([input_data])
        p = predict_label(input_data)
        
        return render_template("models/water.html", prediction = p, news=news)

    return render_template("models/water.html", news=news)