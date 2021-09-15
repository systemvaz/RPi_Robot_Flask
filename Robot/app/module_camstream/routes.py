from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from werkzeug.wrappers import Response

from Robot.lib.object_detection.camera import VideoCamera


mod_camStream = Blueprint("module_camstream", __name__, url_prefix="/camstream")

@mod_camStream.route("/")
def home():
    return render_template("module_camstream/index.html")

def generate(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@mod_camStream.route('/video_feed')
def video_feed():
    return Response(generate(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')