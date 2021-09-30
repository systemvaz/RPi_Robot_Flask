import numpy as np
import cv2 as cv
import sys
import os

from Robot.lib.object_detection.detect_expressions import capture_and_detect_face

WIDTH = 300
HEIGHT = 300
WH_RATIO = WIDTH /float(HEIGHT)
SCALE_FACTOR = 0.007843
MEAN_VAL = 127.5
VIDEO_SIZE = (1920,1080)
OBJECT_BOUNDING_COLOURS = np.random.uniform(255, 0, size=1001)

classNames = ('background',
'aeroplane', 'bicycle', 'bird', 'boat',
'bottle', 'bus', 'car', 'cat', 'chair',
'cow', 'diningtable', 'dog', 'horse',
'motorbike', 'person', 'pottedplant',
'sheep', 'sofa', 'train', 'tvmonitor')


ds_factor = 0.6
grand_parent = os.path.abspath(__file__ + "/../../../")
# For face detection and expression recognition....
cascPath = grand_parent + '/tf_models/haarcascade_frontalface_default.xml'
# For object detection and recognition....
SSDprotoPath = grand_parent + "/tf_models/MobileNetSSD_deploy.prototxt.txt"
SSDcafePath = grand_parent + "/tf_models/MobileNetSSD_deploy.caffemodel"


np.set_printoptions(threshold=sys.maxsize)

class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)
        

    def __del__(self):
        self.video.release()

    
    # ---------------------------------------------------------------------------------------
    # Crop, detect and predict objects
    # ---------------------------------------------------------------------------------------
    def crop_objects(_, frame):
        ssd_net = cv.dnn.readNetFromCaffe(SSDprotoPath, SSDcafePath)
        bounding_box_colours = np.random.uniform(255, 0, size=(len(classNames), 3))

        (h, w) = frame.shape[:2]

        blob = cv.dnn.blobFromImage(cv.resize(frame, (WIDTH, HEIGHT)),
                                                        SCALE_FACTOR, (WIDTH, HEIGHT),
                                                        MEAN_VAL)
        ssd_net.setInput(blob)

        # Predict/detect objects
        ssd_net_results = ssd_net.forward()
        for i in np.arange(0, ssd_net_results.shape[2]):
            confidence = ssd_net_results[0, 0, i, 2]
            if confidence > 0.20:
                idx = int(ssd_net_results[0, 0, i, 1])
                
                crop = ssd_net_results[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = crop.astype("int")
                label = classNames[idx]

                cv.putText(frame, label, (x1, y1-5), cv.FONT_HERSHEY_TRIPLEX, 1.0, (204, 102, 0))
                cv.rectangle(frame, (x1, y1), (x2, y2), bounding_box_colours[idx], 2)

        return frame


    # ---------------------------------------------------------------------------------------
    # Detect and crop face. Pass to capture_and_detect_face library for
    # facial expression detection. Return expression and add to frame as text.
    # ---------------------------------------------------------------------------------------
    def crop_face(_, frame):
        crop_img = None
        faceCascade = cv.CascadeClassifier(cascPath)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(48, 48),
                                            flags=cv.CASCADE_SCALE_IMAGE)
        # Draw bounding boxes
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            crop_img = frame[y:y+h, x:x+w]

        # Detect facial expression and add expression as text above face bounding box
        expression_result = capture_and_detect_face(crop_img)
        try:
            font = cv.FONT_HERSHEY_TRIPLEX
            cv.putText(frame, expression_result, (x, y - 30), font, 0.8, (204, 0, 204), 1, cv.LINE_AA)
        except:
            pass
        return frame


    # ---------------------------------------------------------------------------------------
    # Main function
    # ---------------------------------------------------------------------------------------
    def get_frame(self):
        try:
            ret, frame = self.video.read()

            # Detect face add bounding box and create crop image for detect_expressions.py
            frame  = self.crop_face(frame)
            frame = self.crop_objects(frame)

            frame = cv.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv.INTER_AREA)
            ret, jpeg = cv.imencode('.jpg', frame)
        except:
            pass
        
        return jpeg.tobytes()