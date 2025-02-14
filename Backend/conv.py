import torch
import onnx

# Load your PyTorch model
model = torch.load("weed_detection.pt", map_location=torch.device('cpu'))
model.eval()

# Create a dummy input tensor with the correct shape
dummy_input = torch.randn(1, 3, 224, 224)  # Adjust shape if needed

# Convert to ONNX
onnx_path = "weed_detection.onnx"
torch.onnx.export(model, dummy_input, onnx_path, input_names=['input'], output_names=['output'], dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})

print("Model converted to ONNX and saved as", onnx_path)
