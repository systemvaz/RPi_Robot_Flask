import numpy as np
import cv2 as cv
import os

WIDTH = 300
HEIGHT = 300
WH_RATIO = WIDTH /float(HEIGHT)
SCALE_FACTOR = 0.007843
MEAN_VAL = 127.5
file_size = (1920,1080)

grand_parent = os.path.abspath(__file__ + "/../../../")
labelsPath = grand_parent + "/tf_models/mobilenet_v2_1.0_224_quant_labels.txt"
SSDprotoPath = grand_parent + "/tf_models/MobileNetSSD_deploy.prototxt.txt"
SSDcafePath = grand_parent + "/tf_models/MobileNetSSD_deploy.caffemodel"

with open(labelsPath, 'r') as f:
    object_labels = [line.strip() for line in f]

ssd_net = cv.dnn.readNetFromCaffe(SSDprotoPath, SSDcafePath)

bounding_box_colours = np.random.uniform(255, 0, size=(len(object_labels), 3))

# For testing here....
video = cv.VideoCapture(0)

while video.isOpened():
    _, frame = video.read()
    (h, w) = frame.shape[:2]

    blob = cv.dnn.blobFromImage(cv.resize(frame, (WIDTH, HEIGHT), SCALE_FACTOR, MEAN_VAL))

    ssd_net.setInput(blob)
    # Predict/detect objects
    ssd_net_results = ssd_net.forward()

    # Draw bounding boxes
    for i in np.arange(0, ssd_net_results.shape[2]):
        confidence = ssd_net_results[0, 0, i, 2]
        if confidence > 0.30:
            idx = int(ssd_net_results[0, 0, i, 1])
            crop = ssd_net_results[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = crop.astype("int")
            print("detected object: x1:{} y1:{} x2:{} y2:{}".format(x1,y2,x2,y2))
            cv.rectangle(frame, (x1, y1), (x2, y2), bounding_box_colours[idx], 2)

    # frame = cv.resize(frame, file_size, interpolation=cv.INTER_NEAREST)
    # cv.imshow("Object Detection Test", frame)


video.release()


def capture_and_detect_objects(frame):
    return None