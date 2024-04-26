"""
this file is the server of the project
"""

# import the necessary packages
from flask import Flask, render_template, redirect
import os
import sys
import locale
import tensorflow as tf

# import DL classifiers
from scripts.plant import plant_disease
from scripts.weed import weed_detect
from scripts.flood import flood_pred
from scripts.lemon import lemon_detect
from scripts.irrigation import irrigation
from scripts.cropP import cropP
from scripts.cropR import cropR
"""
#from scripts.pest import pest
#from scripts.chicken import chicken
"""

# add news script
import scripts.news
from scripts.news import news

# add articles script
from scripts.articles import articles

# Set the locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Set environment variables
os.environ['LC_ALL'] = 'en_US.UTF-8'
os.environ['LANG'] = 'en_US.UTF-8'

sys.path.append('/venv/Lib/site-packages')

app = Flask(__name__, template_folder='dist', static_folder='static')
app.register_blueprint(news)
app.register_blueprint(plant_disease)
app.register_blueprint(weed_detect)
app.register_blueprint(flood_pred)
app.register_blueprint(lemon_detect)
app.register_blueprint(irrigation)
app.register_blueprint(cropP)
app.register_blueprint(cropR)
app.register_blueprint(articles)
"""
#app.register_blueprint(pest)
#app.register_blueprint(chicken)
"""

# setup wsgi object
wsgi_app = app.wsgi_app

news_data = scripts.news.get_news()

@app.route('/')
def index():
    # print current directory
    return render_template('index.html')
@app.route('/index')
def index2():
    # print current directory
    return render_template('index.html',news=news_data)
@app.route('/blog')
def blog():
    # print current directory
    return render_template('blog.html',news=news_data)
@app.route('/chat')
def chat():
    # print current directory
    return redirect("http://chat.agritechly.tech")
@app.route('/models')
def models():
    # print current directory
    return render_template('models.html',news=news_data)
@app.route('/models/plantDisease')
def plantDisease():
    # print current directory
    return render_template('models/plant.html')    
@app.route('/models/weedDetector')
def weedDetector():
    # print current directory
    return render_template('models/weed.html')
@app.route('/models/lemonChecker')
def lemonChecker():
    # print current directory
    return render_template('models/lemon.html')
@app.route('/models/irrigation')
def irrigation():
    # print current directory
    return render_template('models/irrigation.html')
"""
@app.route('/models/pestDetect')
def pestDetection():
    # print current directory
    return render_template('models/pest.html')
@app.route('/models/chickenFecal')
def chickenFecal():
    # print current directory
    return render_template('models/chicken.html')
@app.route('/models/cropP')
def cropPred():
    # print current directory
    return render_template('models/cropP.html')
"""
@app.route('/models/cropR')
def cropRec():
    # print current directory
    return render_template('models/cropR.html')
@app.route('/models/floodPred')
def floodPred():
    # print current directory
    return render_template('models/flood.html')

if __name__ == '__main__':
    app.run(debug=True,port=5500)
