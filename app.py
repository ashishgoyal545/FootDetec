from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
import io

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('display_image', filename=filename))
    return render_template('upload.html')

import random

def detect_feet(image_path):
    """
    Estimates foot size based on image dimensions.
    Replace this with your actual foot detection logic.
    """
    img = Image.open(image_path)
    width, height = img.size
    # Estimate foot size based on image dimensions (placeholder logic)
    foot_size = (width + height) / 20  # Example: average dimension divided by 20
    return foot_size, img

@app.route('/uploads/<filename>')
def display_image(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        foot_size, processed_image = detect_feet(image_path)

        # Save the processed image to a BytesIO object
        img_io = io.BytesIO()
        processed_image.save(img_io, 'PNG')
        img_io.seek(0)

        # Convert the BytesIO object to a base64 string
        import base64
        data_uri = base64.b64encode(img_io.read()).decode('utf-8')

        return render_template('display.html', filename=filename, image_data=data_uri, foot_size=foot_size)
    except FileNotFoundError:
        return "Image not found. Please upload an image first."

@app.route('/index')
def index():
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
