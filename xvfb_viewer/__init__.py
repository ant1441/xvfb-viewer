import logging
from os.path import join, split
from flask import Flask

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

log.addHandler(ch)

__version__ = '0.0.2'

log.info("Initialising application")
app = Flask(__name__)

app.config['IMAGE_DIR'] = join(split(__file__)[0], 'static')
app.config['REFRESH'] = 0.5
app.config['XVFB_FILE'] = "/var/tmp/Xvfb_display2/Xvfb_screen0"
app.config['DEBUG'] = False
log.info("Initilisation complete")

from .views import views


def run():
    app.run('0.0.0.0', debug=True)
    #RestrictNumberFiles(app.config['XVFB_FILE'], 2).run()
