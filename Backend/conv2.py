import torch
import cv2
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
import io

app = Flask(__name__)

# 🔹 Load YOLOv5 Model from torch.hub
MODEL_PATH = "your_model.pt"  # Change this to your model path
try:
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=True)
    model.conf = 0.5  # Confidence threshold (adjust if needed)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

def draw_boxes(image, results):
    """Draws bounding boxes on the image."""
    for det in results.xyxy[0]:  # detections in (xmin, ymin, xmax, ymax, confidence, class)
        x_min, y_min, x_max, y_max, conf, cls = det.tolist()
        label = model.names[int(cls)]  # Get class label (maize or weed)

        # Draw rectangle
        cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
        cv2.putText(image, f"{label} {conf:.2f}", (int(x_min), int(y_min) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']

    try:
        img = Image.open(io.BytesIO(image.read())).convert("RGB")
        img_cv = np.array(img)  # Convert PIL to NumPy array

        # 🔹 Run inference
        results = model(img, size=640)

        # 🔹 Draw bounding boxes
        img_cv = draw_boxes(img_cv, results)

        # Convert to JPEG
        _, buffer = cv2.imencode('.jpg', img_cv)
        response_image = buffer.tobytes()

        return response_image, 200, {'Content-Type': 'image/jpeg'}

    except Exception as e:
        return jsonify({'error': 'Model inference failed', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
