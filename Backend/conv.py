from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("maize_dataset.pt")  # Replace with your model file

# Export to ONNX format
model.export(format="onnx")
