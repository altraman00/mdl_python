# -*- coding: UTF-8 -*-

# -*- coding: UTF-8 -*-

import json
# -*- coding: utf-8 -*-
import os

import cv2
import numpy as np
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

characters = "fdamzc5psyb6q4ugkjx2vhet8w9n7r3oi"


def decode(y):
    y = np.argmax(np.array(y), axis=2)[:, 0]
    return ''.join([characters[x] for x in y])


from tensorflow.keras.models import *
from tensorflow.keras.layers import *

width, height = 128, 64
n_len = 4
n_class = len(characters)
input_tensor = Input((height, width, 3))
x = input_tensor
for i, n_cnn in enumerate([2, 2, 2, 2, 2]):
    for j in range(n_cnn):
        x = Conv2D(32 * 2 ** min(i, 3), kernel_size=3, padding='same', kernel_initializer='he_uniform')(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
    x = MaxPooling2D(2)(x)
x = Flatten()(x)
x = [Dense(n_class, activation='softmax', name='c%d' % (i + 1))(x) for i in range(n_len)]
model = Model(inputs=input_tensor, outputs=x)
# model.load_weights('./ok_model/yzm.h5')
model.load_weights('ok_model/yzm.h5')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>图片上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def bytes2cv(im):
    '''二进制图片转cv2
    :param im: 二进制图片数据，bytes
    :return: cv2图像，numpy.ndarray
    '''
    return cv2.imdecode(np.fromstring(im, "uint8"), 1)

# 判断文件夹存不存在，不存在则创建
def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], "images/" + filename)


@app.route('/ImageUpdate', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            create_dir_not_exist('images')

            store_path = os.path.join(app.config['UPLOAD_FOLDER'], "images", filename)
            file.save(store_path)
            image_data = cv2.imread(store_path)
            image_data = cv2.resize(image_data, (128, 64))
            image_data = image_data * 1.0 / 255
            t = model.predict(np.asarray([image_data]))
            result = decode(t)
            return json.dumps({"result": result}, ensure_ascii=False)
    return html


if __name__ == '__main__':
    # app.run(host='10.27.0.3',port=8080,threaded=False)
    # 在阿里云上要设置为内网地址，然后外部通过外网地址访问
    app.run(host='10.27.0.95', port=8080, threaded=False)
