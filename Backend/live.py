import cv2
import torch
import base64
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO
from ultralytics import YOLO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load YOLOv8 Model
model = YOLO("best.pt")  

# Open Webcam
cap = cv2.VideoCapture(0)

def detect_and_stream():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run YOLOv8 detection
        results = model(frame)

        # Draw detections on frame
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                conf = float(box.conf[0])  # Confidence score
                cls = int(box.cls[0])  # Class index

                # Draw rectangle and label
                label = f"{model.names[cls]}: {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert frame to base64 for streaming
        _, buffer = cv2.imencode(".jpg", frame)
        frame_base64 = base64.b64encode(buffer).decode("utf-8")
        socketio.emit("video_frame", {"image": frame_base64})  # Send frame to frontend

@socketio.on("connect")
def connect():
    print("Client connected")
    socketio.start_background_task(detect_and_stream)  # Start video detection

@app.route("/")
def index():
    return render_template("index.html")  # Load the frontend page

if __name__ == "__main__":
    socketio.run(app, debug=True)
