from flask import Blueprint, render_template, request, redirect
#from keras.models import load_model
#from keras.utils import load_img, img_to_array
import random
import cv2
import numpy as np
import os


pest = Blueprint('pest', __name__, template_folder='dist', static_folder='static')

dic = {
    0 : 'ants',
    1 : 'bees',
    2 : 'beetles',
    3 : 'catterpillars',
    4 : 'earthworms',
    5 : 'earwigs',
    6 : 'grasshopper',
    7 : 'moth',
    8 : 'slugs',
    9 : 'snails',
    10: 'wasps',
    11: 'weevils',
}
#script_dir = os.path.dirname(os.path.abspath(__file__))
#xmodel_path = os.path.join(script_dir, 'models', 'PestDetection.h5')
    
#model = load_model(model_path)
#model.make_predict_function()
def load_and_preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_label(img_path):
    #result = model.predict(np.array(load_and_preprocess_image(img_path)))
    #predicted_class = np.argmax(result[0], axis=-1)
    #predicted_class_name = dic[predicted_class]
    predicted_class_name = random.choice(list(dic.values()))
    return predicted_class_name

# routes
@pest.route("/models/pestDetect", methods=['GET', 'POST'])
def kuch_bhi():
    return render_template("/models/pest.html")

@pest.route("/pest/submit", methods = ['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
		# empty the static folder
        import os
        import shutil
        folder = 'static/upload/pest/'
        # check if the folder exists if not create it
        if not os.path.exists(folder):
            os.makedirs(folder)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
		
        img = request.files['my_image']

        img_path = "static/upload/pest/" + img.filename	
        img.save(img_path)

        p = predict_label(img_path)
        
        return render_template("models/pest.html", prediction = p, img_path = img_path)

    return render_template("models/pest.html")

@pest.route("/pest/models")
def chicken_model():
    return redirect("/models")
@pest.route("/pest/blog")
def chicken_blog():
    return redirect("/blog")
@pest.route("/pest/chat")
def chicken_chat():
    return redirect("/chat")