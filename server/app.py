from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/api/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    image_file = request.files['image']

    try:
        # Load image and conver to OpenCV format
        pil_image = Image.open(image_file.stream).convert('RGB')
        image_np = np.array(pil_image)

        #Convert to grayscale and apply thresholding
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Convert back to PIL for pytesseract
        processed_image = Image.fromarray(thresh)

        # OCR
        text = pytesseract.image_to_string(processed_image)
        return jsonify({'ingredientsText': text})
    
    except Exception as e:
        print("OCR Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
