from flask import Flask, request, jsonify
import numpy as np
import tensorflow.lite as tflite
from PIL import Image
import io

app = Flask(__name__)

# Load TFLite model
interpreter = tflite.Interpreter(model_path="best.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_image(image):
    """Preprocess image to match model input."""
    image = image.resize((input_details[0]['shape'][1], input_details[0]['shape'][2]))
    image = np.array(image, dtype=np.float32) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))
    
    input_data = preprocess_image(image)

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Convert output to JSON response
    return jsonify({"predictions": output_data.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
