import tensorflow as tf
from tensorflow.keras.models import load_model
import json
import numpy as np

import json

class_names = ["Hazardous", "Organic", "Recyclable"]  # Replace with actual class names
with open("class_names.json", "w") as f:
    json.dump(class_names, f)


def predict_single_image(image_path):
    # Load class names
    with open('class_names.json', 'r') as f:
        class_names = json.load(f)
    
    # Load model
    model = load_model('final_model')
    
    # Load and preprocess the image
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, (224, 224))
    img = tf.cast(img, tf.float32) / 255.0
    img = tf.expand_dims(img, 0)  # Add batch dimension
    
    # Make prediction
    predictions = model.predict(img)
    predicted_class_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_idx]
    
    print(f"\nPrediction Results:")
    print(f"Class: {class_names[predicted_class_idx]}")
    print(f"Confidence: {confidence:.2%}")
    
    # Print all class probabilities
    print("\nAll class probabilities:")
    for class_name, prob in zip(class_names, predictions[0]):
        print(f"{class_name}: {prob:.2%}")

# Use the function
image_path = "models/test/Recyclable/R_10024.jpg"  # Replace with your image path
predict_single_image(image_path)