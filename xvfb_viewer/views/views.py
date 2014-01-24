from datetime import datetime
from os.path import split, exists
from flask import render_template, url_for, Response, redirect, request, abort
from werkzeug.datastructures import Headers
from .. import app
from ..utils import image
from . import log


@app.route('/')
def index():
    return render_template("index.html",
            interval=app.config['REFRESH'] * 1000,
            max=10)


@app.route('/exists')
def xvfb_exists():
    if exists(app.config['XVFB_FILE']):
        return "true"
    return "false"


@app.route('/current')
def xvfb_image():
    filename = datetime.now().isoformat().replace(':', '-')
    image_path = image(app.config['XVFB_FILE'], filename)
    if image_path is None:
        return no_xvfb()
    filename = split(image_path)[1]
    log.info("File %s created", filename)
    url = url_for('static', filename=filename)

    for type in request.accept_mimetypes:
        if "text" in type[0]:
            return image_txt(url)
        if "image" in type[0] or "png" in type[0]:
            return image_png(url)
    return image_txt(url)


def image_txt(url):
    headers = Headers({'Cache-Control': 'no-cache',
                       'Location': url,
                       'Refresh': app.config['REFRESH']})
    return Response(url, mimetype='text/plain', headers=headers, status=201)


def image_png(url):
    return redirect(url), 307

def no_xvfb():
    return abort(404)
