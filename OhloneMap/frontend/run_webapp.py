import flask
from flask import Flask

from backend.find_path import find_path
from backend.segment_path import segment_path
from backend.build_image import build_image

app = Flask(__name__)
segments = []

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/map")
def map():
    #global segments
    start = flask.request.args.get('From')
    end = flask.request.args.get('To')
    
    # index of current floor_map within stops
    i = flask.request.args.get('i')
    if i is None:
        i = 0
    
    #if segments == []:
    if True:
        path = find_path(start, end)
        if path is None:
            return flask.render_template("index.html")

        segments = segment_path(path)
    
    if i > len(segments):
        return flask.render_template("index.html")

    img = build_image(segments[i])
    return flask.render_template(f"map.html", From=start, To=end, i=i, img=img)

def run_webapp():
    app.run()