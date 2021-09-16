import numpy as np
import cv2 as cv
import sys
import os

from Robot.lib.object_detection.detect_expressions import capture_and_detect_face
from Robot.lib.object_detection.detect_objects import capture_and_detect_objects

WIDTH = 300
HEIGHT = 300
WH_RATIO = WIDTH /float(HEIGHT)
SCALE_FACTOR = 0.007843
MEAN_VAL = 127.5
VIDEO_SIZE = (1920,1080)
OBJECT_BOUNDING_COLOURS = np.random.uniform(255, 0, size=1001)

ds_factor = 0.6
grand_parent = os.path.abspath(__file__ + "/../../../")
cascPath = grand_parent + '/tf_models/haarcascade_frontalface_default.xml'

np.set_printoptions(threshold=sys.maxsize)

faceCascade = cv.CascadeClassifier(cascPath)

class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)
        

    def __del__(self):
        self.video.release()

    
    def crop_objects(_, frame):
        try:
            img = cv.resize(frame, (244, 244), fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)
            normalise_frame = (2 * ((img - 0 )/(255 - 0))) - 1
            frame = capture_and_detect_objects(normalise_frame)
            frame = ((frame + 1) * 127.5)
            print("RETURNING FRAME FROM DETECT_OBJECTS !!!!...... {}".format(frame))
        except Exception as e:
            print(e)
        return frame


    def crop_face(_, frame):
        crop_img = None
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

        # Detect facial expression....
        expression_result = capture_and_detect_face(crop_img)
        # Add expression as text above face bounding box
        try:
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(frame, expression_result, (x, y - 10), font, 0.8, (0, 0, 255), 1, cv.LINE_AA)
        except:
            pass

        return frame


    def get_frame(self):
        ret, frame = self.video.read()

        # Detect face add bounding box and create crop image for detect_expressions.py
        frame  = self.crop_face(frame)
        frame = self.crop_objects(frame)

        frame = cv.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv.INTER_AREA)
        ret, jpeg = cv.imencode('.jpg', frame)
        
        return jpeg.tobytes()