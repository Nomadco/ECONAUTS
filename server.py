from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from flask_cors import CORS  # Add this import

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your trained ML model
model = tf.keras.models.load_model("final_model")  # Change to your actual model path
class_names = ["Hazardous", "Organic", "Recyclable"]  # Adjust as per your training data

def preprocess_image(image):
    image = image.resize((224, 224))  # Resize to match model input
    image = np.array(image) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

@app.route("/")
def home():
    return "Flask server is running!"

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400

    try:
        # Verify that the uploaded file is an image
        if not file.content_type.startswith('image/'):
            return jsonify({"error": "Uploaded file is not an image"}), 400

        image = Image.open(io.BytesIO(file.read()))  # Open image
        image = preprocess_image(image)  # Preprocess
        predictions = model.predict(image)[0]  # Get model predictions
        class_index = np.argmax(predictions)  # Get highest probability class
        confidence = float(predictions[class_index])

        response = jsonify({
            "class": class_names[class_index],
            "confidence": confidence
        })
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)