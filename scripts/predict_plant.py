"""
this file is used to predict and return the result in results/result[i].json file the i is the number of the result to save history of the results
it will be executed by the server
"""

# import the necessary packages
import sys
sys.path.append('/venv/Lib/site-packages')
import os
import json
import cv2
import tensorflow as tf
import numpy as np
from keras.models import load_model

# loading and preprocessing the image
def load_and_preprocess_image(image_path):
    """
    this function is used to load and preprocess the image
    """
    # load the image
    img = cv2.imread(image_path)
    # Resize the image to match the model's input shape
    img = cv2.resize(img, (224, 224))
    # Preprocess the image (you may need to adjust preprocessing based on your model)
    img = img / 255.0  # Normalize pixel values to be between 0 and 1
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Class mapping of the 58 classes in the dataset
class_mapping = {
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

def main():
    """
    this is the main function
    """
    # print the curent dir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'models', 'PlantDisease.h5')
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
 
    image_path = sys.argv[1]
    print("Image path:", image_path)
    print("Model path:", model_path)
    model = load_model(model_path)
    print("Model loaded successfully")

    # Process input data (e.g., image) and make predictions
    result = model.predict(np.array(load_and_preprocess_image(image_path)))
    
    # Get the predicted class with the highest probability
    predicted_class = np.argmax(result[0], axis=-1)
    # Get the class name of the predicted class
    predicted_class_name = class_mapping[predicted_class]
    # save the result in the results folder
    # check if the class name contains healthy
    if "healthy" in predicted_class_name:
        # create the result dict
        result_dict = {
            "class": predicted_class_name,
            "probability": str(np.max(result[0], axis=-1) * 100)
        }
    else:
        # load the cure.json file
        with open(os.path.join(script_dir, 'cure.json'), encoding="utf8") as json_file:
            cure_dict = json.load(json_file)
        # get the cure for the disease
        cure = cure_dict.get(predicted_class_name.lower(), "No prevention information available.")
        # create the result dict
        result_dict = {
            "class": predicted_class_name,
            "probability": str(np.max(result[0], axis=-1)),
            "cure": cure
        }
    # save the result in the results folder
    with open(os.path.join(script_dir, 'results', 'result_plants.json'), 'w') as outfile:
        json.dump(result_dict, outfile)
    

if __name__ == "__main__":
    main()