import enum
import numpy as np
import cv2 as cv
import os

import tflite_runtime.interpreter as tflite

OBJECT_CONFIDENCE = 0.50
FONT = cv.FONT_HERSHEY_SIMPLEX
COLORS = np.random.uniform(0, 255, size=(1000, 3))

grand_parent = os.path.abspath(__file__ + "/../../../")
labelsPath = grand_parent + '/tf_models/mobilenet_v2_1.0_224_quant_labels.txt'
modelPath = grand_parent + '/tf_models/mobilenet_v2_1.0_224_quant.tflite'

model = tflite.Interpreter(model_path=modelPath)
model.allocate_tensors()

with open(labelsPath, 'r') as f:
    object_labels = {i: line.strip() for i, line in enumerate(f.readlines())}

def create_input_tensor(img):
    print(img[:10])
    tensor_index = model.get_input_details()[0]['index']
    input_tensor = model.tensor(tensor_index)()[0]
    img = np.expand_dims(img, axis=0)
    print("tensor setup, trying to add image data....")
    print(img.dtype)
    input_tensor[:, :] = img


def get_output_tensor(index):
    output_details = model.get_output_details()[index]
    tensor = np.squeeze(model.get_tensor(output_details['index']))

    return tensor

def detect_objects(frame):
    create_input_tensor(frame)
    model.invoke()
    # Get MobileNetv2 output
    boxes = get_output_tensor(0)
    classes = get_output_tensor(1)
    scores = get_output_tensor(2)
    count = int(get_output_tensor(3))
    results = []

    for i in range(count):
        if scores[i] >= OBJECT_CONFIDENCE:
            result = {'bounding box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i]}
    
            results.append(result)

    return results

def capture_and_detect_objects(frame):
    og_height, og_width = frame.shape[:2]
    results = detect_objects(frame)

    for i in range(len(results)):
        id = int(results[i]['class_id'])
        probability = int(round(results[i]['score'], 2) * 100)
        ymin, xmin, ymax, xmax = results[i]['bounding_box']

        xmin = int(xmin * og_width)
        xmax = int(xmax * og_width)
        ymin = int(ymin * og_height)
        ymax = int(ymax * og_height)

        text = "{}: {}%".format(object_labels[id], probability)

        if ymin > 10:
            ytxt = ymin - 10
        else:
            ytxt = ymin + 15

        frame = cv.rectangle(frame, (xmin, ymin), (xmax, ymax), COLORS[id], thickness=2)
        frame = cv.putText(frame, text, (xmin + 3, ytxt), FONT, 0.5, COLORS[id])

    return frame