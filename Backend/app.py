from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import torch
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  

model = YOLO("best.pt") 

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    image = Image.open(image_file).convert("RGB")
    image_cv = np.array(image)

    # Perform inference
    results = model(image_cv)

    # Draw bounding boxes on the image
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            cv2.rectangle(image_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)  
            label = f"{result.names[int(box.cls[0])]} {box.conf[0]:.2f}"
            cv2.putText(image_cv, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Convert processed image to bytes
    processed_image = Image.fromarray(image_cv)
    img_io = io.BytesIO()
    processed_image.save(img_io, "JPEG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
