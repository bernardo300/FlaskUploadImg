import os

from flask import Flask, flash, jsonify, render_template, request, send_from_directory
from flask_uploads import IMAGES, UploadSet, configure_uploads
import cv2
import numpy as np

from PIL import Image
import io


app = Flask(__name__)
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
app.config["SECRET_KEY"] = os.urandom(24)
configure_uploads(app, photos)


@app.route("/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        image = request.files['photo']
        #photos.save(image)
        img = Image.open(image)
        numpy_image = np.array(img)

        opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
        pencilDraw(opencv_image)

        flash("Photo saved successfully.")
        return render_template('upload.html', uploaded_image='draw.png')
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)


@ app.route("/files", methods=['GET'])
def list_files():
    files = []
    arquivos = []
    for filename in os.listdir('static/img/'):
        path = os.path.join('static/img/'+filename)
        if os.path.isfile(path):
            files.append(filename)
            arquivos.append(filename)
    return render_template('download.html', arquivos=arquivos)


@ app.route("/files/<path:path>")
def get_file(path):
    return send_from_directory('static/img/', path, as_attachment=True)


def pencilDraw(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray_inv = 255 - img_gray
    img_blur = cv2.GaussianBlur(img_gray_inv, (21, 21), 0, 0)
    img_blend = cv2.divide(img_gray, 255 - img_blur, scale=256)
    cv2.imwrite('static/img/draw.png', img_blend)


if __name__ == '__main__':
    app.run(debug=True)
