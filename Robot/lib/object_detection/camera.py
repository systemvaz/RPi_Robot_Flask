import numpy as np
import cv2 as cv
import os

from Robot.lib.object_detection.detect_expressions import capture_and_detect_face
# from Robot.lib.object_detection.detect_objects import capture_and_detect_objects

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
SSDprotoPath = grand_parent + "/tf_models/MobileNetSSD_deploy.prototxt.txt"
SSDcafePath = grand_parent + "/tf_models/MobileNetSSD_deploy.caffemodel"

faceCascade = cv.CascadeClassifier(cascPath)
ssd_net = cv.dnn.readNetFromCaffe(SSDprotoPath, SSDcafePath)

class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)
        

    def __del__(self):
        self.video.release()

    
    def crop_objects(_, frame):
        (h, w) = frame.shape[:2]
        blob = cv.dnn.blobFromImage(cv.resize(frame, (WIDTH, HEIGHT), SCALE_FACTOR, MEAN_VAL))
        ssd_net.setInput(blob)
        ssd_net_results = ssd_net.forward()

        # Draw bounding boxes
        for i in np.arange(0, ssd_net_results.shape[2]):
            confidence = ssd_net_results[0, 0, i, 2]
            if confidence > 0.30:
                idx = int(ssd_net_results[0, 0, i, 1])
                crop = ssd_net_results[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = crop.astype("int")
                cv.rectangle(frame, (x1, y1), (x2, y2), OBJECT_BOUNDING_COLOURS[idx], 2)
                # print("detected object: x1:{} y1:{} x2:{} y2:{}".format(x1,y2,x2,y2))

        return frame


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
        frame = self.crop_objects(frame)

        frame = cv.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv.INTER_AREA)
        ret, jpeg = cv.imencode('.jpg', frame)
        
        return jpeg.tobytes()