import logging
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from crossdomain import crossdomain
import os.path
import cv2
import runtag.secded
from flask import send_file

app = Flask(__name__)


def format_marker(img, m):
    height, width = img.shape[:2]

    mx1, my1 = m[1][0]
    mx3, my3 = m[1][2]

    mw = abs(mx3 - mx1)
    mh = abs(my3 - my1)

    return {
        'id': m[0],
        'left': mx1/width,
        'top': my1/height,
        'width': mw/width,
        'height': mh/height
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


if __name__ == '__main__':
    app.run()
