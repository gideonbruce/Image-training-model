import tensorflow as tf

# Load the TensorFlow model
converter = tf.lite.TFLiteConverter.from_saved_model("saved_model")  

# Set optimizations for smaller size and faster inference
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convert and save the TFLite model
tflite_model = converter.convert()
with open("maize_dataset.tflite", "wb") as f:
    f.write(tflite_model)

print("Model conversion successful! Saved as maize_dataset.tflite")
