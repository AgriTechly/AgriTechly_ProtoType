from flask import Blueprint, render_template, request
from keras.models import load_model
from keras.utils import load_img, img_to_array
import cv2
import numpy as np
import os


weed_detect = Blueprint('weed_detect', __name__, template_folder='dist', static_folder='static')

dic = {
    0 : 'broadleaf',
    1 : 'grass',
    2 : 'soil',
    3 : 'soybean'
 }
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'models', 'WeedDetector.h5')
    
model = load_model(model_path)
model.make_predict_function()
def load_and_preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (227, 227))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_label(img_path):
    result = model.predict(np.array(load_and_preprocess_image(img_path)))
    predicted_class = np.argmax(result[0], axis=-1)
    predicted_class_name = dic[predicted_class]
    # check if prediction is less than 50% probability
    probability = np.max(result[0], axis=-1)*100
    if probability < 50:
        predicted_class_name = "No Weed in " + predicted_class_name
    else :
        predicted_class_name = "Weed in " + predicted_class_name
    return predicted_class_name


# routes
@weed_detect.route("/models/weedDetector", methods=['GET', 'POST'])
def kuch_bhi():
    return render_template("/models/weed.html")

@weed_detect.route("/weed/submit", methods = ['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
		# empty the static folder
        import os
        import shutil
        folder = 'static/upload/weed/'
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

        img_path = "static/upload/weed/" + img.filename	
        img.save(img_path)

        p = predict_label(img_path)
        
        return render_template("models/weed.html", prediction = p, img_path = img_path)

    return render_template("models/weed.html")