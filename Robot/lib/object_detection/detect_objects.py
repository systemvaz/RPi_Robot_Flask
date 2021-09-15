import numpy as np
import cv2 as cv
import os

grand_parent = os.path.abspath(__file__ + "/../../../")
labelsPath = grand_parent + '/tf_models/mobilenet_v2_1.0_224_quant_labels.txt'

with open(labelsPath, 'r') as f:
    object_labels = [line.strip() for line in f]

def capture_and_detect_objects(frame):
    # frame = cv.resize(frame, file_size, interpolation=cv.INTER_NEAREST)
    # cv.imshow("Object Detection Test", frame)
    return frame