from flask import Flask, render_template, request
import os
from PIL import Image
import cv2
import argparse

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

parser = argparse.ArgumentParser(description='Foot size detection app')
parser.add_argument('--port', type=int, default=5000, help='Port to run the app on')
args = parser.parse_args()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', message='No file part')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template('upload.html', message='No selected file')
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            # Process the image and get the foot size
            foot_size = detect_foot_size(filename)
            return render_template('upload.html', message='File uploaded successfully', foot_size=foot_size)
    return render_template('upload.html')

def detect_foot_size(image_path):
    # Load the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Edge detection
    edges = cv2.Canny(img, 100, 200)
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the largest contour (assuming it's the foot)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        # Calculate the perimeter of the contour
        perimeter = cv2.arcLength(largest_contour, True)
        # Estimate the foot size based on the perimeter (placeholder)
        foot_size = f"Estimated foot size: {perimeter:.2f}"
    else:
        foot_size = "No foot detected"
    return foot_size

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=args.port)
