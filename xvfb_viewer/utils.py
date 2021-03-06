from os.path import join
import struct
from StringIO import StringIO
from flask import current_app, send_file

import numpy as np
from PIL import Image

_XWD_HEADER = struct.Struct('>lllllllhhhhhh')


def filename_to_im(filename):
    with open(filename, 'rb') as xf:
        fb = np.fromfile(xf, np.uint8)
    w, h = _read_w_h_from_header(fb)
    np_image = fb[3232:].reshape((h, w, 4))[:, :, (2, 1, 0)]

    im = Image.fromarray(np_image)
    return im


def im_to_file(im, filename):
    if not im:
        return None
    if not filename.endswith(".png"):
        filename += ".png"
    dir = current_app.config['IMAGE_DIR']
    filepath = join(dir, filename)
    im.save(filepath, format="png")
    return filepath


def image(fb_filename, filename):
    return im_to_file(filename_to_im(fb_filename), filename)


def _read_w_h_from_header(fb):
    return _XWD_HEADER.unpack_from(fb)[4:6]


def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
