from flask import Blueprint, render_template, request
from keras.models import load_model
from keras.utils import load_img, img_to_array
import cv2
import numpy as np
import os
from scripts.news import get_news


plant_disease = Blueprint('plant_disease', __name__, template_folder='dist', static_folder='static')

dic = {
    0: 'Apple Apple scab',
    1: 'Apple Black rot',
    2: 'Apple Cedar apple rust',
    3: 'Apple healthy',
    4: 'Bacterial leaf blight in rice leaf',
    5: 'Blight in corn Leaf',
    6: 'Blueberry healthy',
    7: 'Brown spot in rice leaf',
    8: 'Cercospora leaf spot',
    9: 'Cherry (including sour) Powdery mildew',
    10: 'Cherry (including_sour) healthy',
    11: 'Common Rust in corn Leaf',
    12: 'Corn (maize) healthy',
    13: 'Garlic',
    14: 'Grape Black rot',
    15: 'Grape Esca Black Measles',
    16: 'Grape Leaf blight Isariopsis Leaf Spot',
    17: 'Grape healthy',
    18: 'Gray Leaf Spot in corn Leaf',
    19: 'Leaf smut in rice leaf',
    20: 'Nitrogen deficiency in plant',
    21: 'Orange Haunglongbing Citrus greening',
    22: 'Peach healthy',
    23: 'Pepper bell Bacterial spot',
    24: 'Pepper bell healthy',
    25: 'Potato Early blight',
    26: 'Potato Late blight',
    27: 'Potato healthy',
    28: 'Raspberry healthy',
    29: 'Sogatella rice',
    30: 'Soybean healthy',
    31: 'Strawberry Leaf scorch',
    32: 'Strawberry healthy',
    33: 'Tomato Bacterial spot',
    34: 'Tomato Early blight',
    35: 'Tomato Late blight',
    36: 'Tomato Leaf Mold',
    37: 'Tomato Septoria leaf spot',
    38: 'Tomato Spider mites Two spotted spider mite',
    39: 'Tomato Target Spot',
    40: 'Tomato Tomato mosaic virus',
    41: 'Tomato healthy',
    42: 'Waterlogging in plant',
    43: 'algal leaf in tea',
    44: 'anthracnose in tea',
    45: 'bird eye spot in tea',
    46: 'brown blight in tea',
    47: 'cabbage looper',
    48: 'corn',
    49: 'ginger',
    50: 'healthy tea leaf',
    51: 'lemon canker',
    52: 'onion',
    53: 'potassium deficiency in plant',
    54: 'potato crop',
    55: 'potato hollow heart',
    56: 'red leaf spot in tea',
    57: 'tomato canker'
}

news = get_news()
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'models', 'PlantDisease.h5')
    
model = load_model(model_path)
model.make_predict_function()
def load_and_preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_label(img_path):
    result = model.predict(np.array(load_and_preprocess_image(img_path)))
    predicted_class = np.argmax(result[0], axis=-1)
    predicted_class_name = dic[predicted_class]
    return predicted_class_name


# routes
@plant_disease.route("/models/plantDisease", methods=['GET', 'POST'])
def kuch_bhi():
    return render_template("/models/plant.html", news=news)

@plant_disease.route("/plant/submit", methods = ['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
		# empty the static folder
        import os
        import shutil
        folder = 'static/upload/plants/'
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

        img_path = "static/upload/plants/" + img.filename	
        img.save(img_path)

        p = predict_label(img_path)

        # check if the prediction does not contain healthy
        if 'healthy' not in p:
            # get the cure for the disease
            # read the cure for the disease
            import json
            with open('dist/cure.json', encoding="utf8") as f:
                data = json.load(f)
            # get the cure for the disease
            cure = data[p.lower()]
            return render_template("models/plant.html", prediction = p, cure=cure, img_path = img_path, news=news)
        else:
            return render_template("models/plant.html", prediction = p, img_path = img_path, news=news)




    return render_template("models/plant.html", news=news)