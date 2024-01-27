# import the necessary packages
import sys
sys.path.append('/venv/Lib/site-packages')
import os
import json
import tensorflow as tf
import numpy as np


# get the inputs from input_flood.json
with open('inputs\input_flood.json') as json_file:
    input_dict = json.load(json_file)


def main():
    """
    this is the main function
    """
    # print the curent dir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'models', 'FloodPred.h5')
    
    model = tf.keras.models.load_model(model_path)

    # Process input data (e.g., image) and make predictions
    result = model.predict(np.array(input_dict['inputs']))
    # save the result in the results folder
    # create the result dict
    result_dict = {
        "probability": str(np.max(result[0], axis=-1))
    }
    # save the result in the results folder
    with open(os.path.join(script_dir, 'results', 'result_flood.json'), 'w') as outfile:
        json.dump(result_dict, outfile)
    

if __name__ == "__main__":
    main()