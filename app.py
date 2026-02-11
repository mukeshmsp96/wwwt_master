#!/usr/bin/env python

import logging
import os

import flask
from flask import request

logging.basicConfig()

os.environ['FLASK_DEBUG'] = 'true'

app = flask.Flask(__name__)

FILE_SECRET = 'h20tavyWvchAlZko21t0X0lH93VJCQBn'


@app.route('/image/<file_name>', methods=['GET'])
def get_image(file_name):
    secret = request.headers['X-Image-Secret']

    with open(f'images/{file_name}.png', 'rb') as f:
        if secret != FILE_SECRET:
            logging.info(f'bad file secret! {secret}')
            return '', 403

        return f.read()


@app.route('/image/<file_name>', methods=['POST'])
def save_image(file_name):
    secret = request.headers['X-Image-Secret']

    with open(f'images/{file_name}.png', 'wb') as f:
        if secret != FILE_SECRET:
            logging.info(f'bad file secret! {secret}')
            return '', 403

        f.write(request.data)

        return ''


app.run('0.0.0.0', port=int(os.environ['APP_PORT']))
