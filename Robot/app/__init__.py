from flask import Flask, render_template

app = Flask(__name__)
print("{}".format(app))
app.config.from_object('config')

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from Robot.app.module_camstream.routes import mod_camStream
app.register_blueprint(mod_camStream)