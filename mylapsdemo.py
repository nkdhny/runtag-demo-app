import json
import logging
from flask import Flask, request, jsonify, Response
from werkzeug.utils import secure_filename
from crossdomain import crossdomain
import os.path
import cv2
import runtag.secded
from flask import send_file
import base64
import numpy as np

app = Flask(__name__)


def format_marker(img, m):
    height, width = img.shape[:2]

    mx1, my1 = m[1][0]
    mx3, my3 = m[1][2]

    mw = abs(mx3 - mx1)
    mh = abs(my3 - my1)

    mx = min(mx1, mx3)
    my = min(my1, my3)

    return {
        'id': m[0],
        'left': mx / width,
        'top': my / height,
        'width': mw / width,
        'height': mh / height
    }


@app.route('/detect', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def upload():
    if 'image' in request.files:
        logging.debug('Saving file')
        file = request.files['image']
        local_name = secure_filename(file.filename)
        local_path = os.path.join('/tmp', local_name)
        file.save(local_path)

        img = cv2.imread(local_path, 0)
        height, width = img.shape[:2]

        markers = runtag.secded.apply(img)

        return jsonify({
            'markers': map(lambda m: format_marker(img, m), markers),
            'name': local_name,
            'width': width,
            'height': height
        })
    return "", 500


@app.route('/img/<name>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_image(name):
    local_name = os.path.join('/tmp', name)
    if os.path.isfile(local_name):
        return send_file(local_name)
    else:
        return "", 404


@app.route('/m/detect', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def detect_mobile():
    detected = []
    for shape_serial in json.loads(request.data):
        shape = decode_shape(shape_serial)
        m_id = runtag.secded.apply_single(shape)

        if m_id > 0:
            detected.append(m_id)

    return Response(json.dumps(detected), content_type='application/json')


def decode_shape(shape_serial):
    shape_bytes = bytearray(base64.b64decode(shape_serial))

    s = shape_bytes[::-1]

    print len(shape_serial), len(s), len(base64.b64decode(shape_serial)), shape_serial

    rows_h = s.pop()
    rows_l = s.pop()
    rows = rows_h * 256 + rows_l

    cols_h = s.pop()
    cols_l = s.pop()
    cols = cols_h * 256 + cols_l

    bit = 0

    portion = 0

    shape = np.zeros((rows, cols), dtype='uint8')

    try:
        for row in range(0, rows):
            for col in range(0, cols):
                if bit % 8 == 0:
                    portion = s.pop()
                    bit = 0

                if portion & 0x80 > 0:
                    shape[row, col] = 255

                portion <<= 1

                bit += 1
    except Exception as e:
        print e

    return shape


if __name__ == '__main__':
    app.run()
