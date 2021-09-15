import cv2 as cv
import os

from Robot.lib.object_detection.detect_expressions import capture_and_detect_face
from Robot.lib.object_detection.detect_objects import capture_and_detect_objects

ds_factor = 0.6
grand_parent = os.path.abspath(__file__ + "/../../../")
cascPath = grand_parent + '/tf_models/haarcascade_frontalface_default.xml'

faceCascade = cv.CascadeClassifier(cascPath)

class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)
        

    def __del__(self):
        self.video.release()


    def crop_face(_, frame):
        crop_img = None
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(48, 48),
                                            flags=cv.CASCADE_SCALE_IMAGE)

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

        frame = cv.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv.INTER_AREA)
        ret, jpeg = cv.imencode('.jpg', frame)
        
        return jpeg.tobytes()