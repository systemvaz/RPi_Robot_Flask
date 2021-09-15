# ----------------------------------------------
# Author: Alex Varano
# Main video capture and expression detection code.
# Expression is mimicked by robot via 8x8 LED matrix.
# Utilises model saved by train.py
# ----------------------------------------------

import cv2
import sys
import os
import numpy as np
import tflite_runtime.interpreter as tflite

import Robot.lib.led_matrix.led_expressions as led_expressions


# Get filepath declarations and classes dictionary
grand_parent = os.path.abspath(__file__ + "/../../../")
cascPath = grand_parent + '/tf_models/haarcascade_frontalface_default.xml'
modelPath = grand_parent + '/tf_models/expression_detect.tflite'

classes_dict = {0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy',
                4:'Sad', 5:'Surprised', 6:'Neutral'}

# Load model and input parameters
model = tflite.Interpreter(model_path=modelPath)
model.allocate_tensors()
input_index = model.get_input_details()[0]["index"]
faceCascade = cv2.CascadeClassifier(cascPath)


def expressions(result):
    if result == 'Angry':
        led_expressions.angry_face()
    elif result == 'Disgust':
        led_expressions.angry_face()
    elif result == 'Fear':
        led_expressions.scared_face()
    elif result == 'Happy':
        led_expressions.happy_face()
    elif result == 'Sad':
        led_expressions.sad_face()
    elif result == 'Surprised':
        led_expressions.surprised_face()
    elif result == 'Neutral':
        led_expressions.neutral_face()


# Main video capture/expression detection loop, press q to quit
def capture_and_detect_face(crop_img):
    # Resize and predict expression
    try:
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        crop_img = crop_img.astype('float32') / 255
        crop_img = cv2.resize(crop_img, (48, 48))
        crop_img = crop_img.reshape(1,48,48,1)

        # TFLite prediction
        model.set_tensor(input_index, crop_img)
        model.invoke()
        output_details = model.get_output_details()
        expression = model.get_tensor(output_details[0]['index'])
        expression = int(np.argmax(expression, axis = 1))
        result = classes_dict.get(expression, "Don't know")
        # Send expression to LED matrix
        expressions(result)
    except Exception as e:
        result = None
        led_expressions.neutral_face()
    
    return result