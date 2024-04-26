from flask import Blueprint, render_template, request
from keras.models import load_model
import numpy as np
import os
from scripts.news import get_news


irrigation = Blueprint('irrigation', __name__, template_folder='dist', static_folder='static')

news = get_news()
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'models', 'AutoIrrigation.h5')
    
model = load_model(model_path)
model.make_predict_function()

def predict_label(input_data):
    result = model.predict(np.array(input_data))
    probability = np.max(result[0], axis=-1)*100
    if probability < 50:
        predicted_class_name = "Don't need Water"
    else :
        predicted_class_name = "Need Water"
    return predicted_class_name


# routes
@irrigation.route("/models/irrigation", methods=['GET', 'POST'])
def kuch_bhi():
    return render_template("/models/irrigation.html", news=news)

@irrigation.route("/irrigation/submit", methods = ['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
		# get the data from inputs
        input_data = []
        input_data.append(request.form['m'])
        input_data.append(request.form['t'])
        input_data = [float(i) for i in input_data]
        input_data = np.array([input_data])
        p = predict_label(input_data)
        
        return render_template("models/irrigation.html", prediction = p, news=news)

    return render_template("models/irrigation.html", news=news)