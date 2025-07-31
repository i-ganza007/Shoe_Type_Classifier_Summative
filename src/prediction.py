import numpy as np
from tensorflow.keras.models import load_model
from preprocessing import preprocess_image_for_prediction
import os

model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "second_80_percent_model_ian_g_cnn_model.h5")
model = load_model(model_path)

class_labels = ['Boot', 'Sandal', 'Shoe']

def predict_image(image_path, threshold=0.7):
    img_array = preprocess_image_for_prediction(image_path)
    predictions = model.predict(img_array)
    
    predicted_index = np.argmax(predictions)
    confidence = float(np.max(predictions))

    if confidence < threshold:
        return {
            "predicted_class": "Not a Shoe",
            "confidence": confidence
        }

    predicted_class = class_labels[predicted_index]
    return {
        "predicted_class": predicted_class,
        "confidence": confidence
    }
