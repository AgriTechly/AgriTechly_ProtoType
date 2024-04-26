from flask import Blueprint, render_template, request
from joblib import load, dump
import numpy as np
import os


cropP = Blueprint('crop_pred', __name__, template_folder='dist', static_folder='static')

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'models', 'CropPred.joblib')
    
model = load(model_path)

def predict_label(input_data):
    result = model.predict(np.array(input_data))
    # get the predicted value of regression
    predicted_class = result[0]
    return predicted_class


# routes
@cropP.route("/models/cropP", methods=['GET', 'POST'])
def kuch_bhi():
    return render_template("/models/cropP.html")

@cropP.route("/cropP/submit", methods = ['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
		# get the data from inputs
        input_data = []
        #input_data = ["Algeria"]
        # add current year to the input data
        input_data.append(float("2024"))
        input_data.append(float(request.form['t']))
        input_data.append(float(request.form['p']))
        input_data.append(request.form['i'])
        input_data.append(float(request.form['rain']))
        input_data = np.array([input_data])
        p = predict_label(input_data)
        
        return render_template("models/cropP.html", prediction = p)

    return render_template("models/cropP.html")