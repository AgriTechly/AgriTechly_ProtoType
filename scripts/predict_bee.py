"""
this file is used to predict and return the result in results/result[i].json file the i is the number of the result to save history of the results
it will be executed by the server
"""

# import the necessary packages
import sys
import os
import json
import cv2
import tensorflow as tf
import numpy as np

# loading and preprocessing the image
def load_and_preprocess_image(image_path):
    """
    this function is used to load and preprocess the image
    """
    # load the image
    img = cv2.imread(image_path)
    # Resize the image to match the model's input shape
    img = cv2.resize(img, (100, 100))
    # Preprocess the image (you may need to adjust preprocessing based on your model)
    img = img / 255.0  # Normalize pixel values to be between 0 and 1
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Class mapping of the 58 classes in the dataset
class_mapping = {
    0 :'-1',
    1 : '1 Mixed local stock 2',
    2 : 'Carniolan honey bee',
    3 : 'Italian honey bee',
    4 : 'Russian honey bee',
    5 : 'VSH Italian honey bee',
    6 : 'Western honey bee'
 }

def main():
    """
    this is the main function
    """
  # print the curent dir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'models', 'HoneyBee.h5')
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
 
    image_path = sys.argv[1]
    model = tf.keras.models.load_model(model_path)

    # Process input data (e.g., image) and make predictions
    result = model.predict(np.array(load_and_preprocess_image(image_path)))
    
    # Get the predicted class with the highest probability
    predicted_class = np.argmax(result[0], axis=-1)
    # Get the class name of the predicted class
    predicted_class_name = class_mapping[predicted_class]
    # Get the probability of the predicted class
    probability = result[0][predicted_class]
    probability *= 100
    # take only 2 digits after the decimal point
    probability = "{:.2f}".format(probability)
    # save the result in the results folder
    # create the result dict
    
    result_dict = {
        "class": predicted_class_name,
        "probability": str(probability)
    }
    # save the result in the results folder
    with open(os.path.join(script_dir, 'results', 'result_bee.json'), 'w') as outfile:
        json.dump(result_dict, outfile)

if __name__ == "__main__":
    main()