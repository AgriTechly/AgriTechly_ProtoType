from flask import Blueprint, render_template, request, redirect
#from keras.models import load_model
import random
import numpy as np
import os
from scripts.news import get_news


water = Blueprint('water', __name__, template_folder='dist', static_folder='static')

news = get_news()
#script_dir = os.path.dirname(os.path.abspath(__file__))
#model_path = os.path.join(script_dir, 'models', 'water.h5')
    
#model = load_model(model_path)
#model.make_predict_function()

def predict_label(input_data):
    #result = model.predict(np.array(input_data))
    #probability = np.max(result[0], axis=-1)*100
    probability = random.uniform(0, 100)
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
        input_data = []
        input_data.append(request.form['ph'])
        input_data.append(request.form['h'])
        input_data.append(request.form['s'])
        input_data.append(request.form['c'])
        input_data.append(request.form['su'])
        input_data.append(request.form['cd'])
        input_data.append(request.form['oc'])
        input_data.append(request.form['thm'])
        input_data.append(request.form['trb'])
        input_data = [float(i) for i in input_data]
        input_data = np.array([input_data])
        p = predict_label(input_data)
        
        return render_template("models/water.html", prediction = p, news=news)

    return render_template("models/water.html", news=news)

@water.route("/water/models")
def chicken_model():
    return redirect("/models")
@water.route("/water/blog")
def chicken_blog():
    return redirect("/blog")
@water.route("/water/chat")
def chicken_chat():
    return redirect("/chat")