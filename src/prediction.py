import numpy as np
from tensorflow.keras.models import load_model
from preprocessing import preprocess_image_for_prediction
import os

# Load the trained model
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "second_80_percent_model_ian_g_cnn_model.h5")
model = load_model(model_path)

# Class labels (make sure this order matches your training generator's class indices)
class_labels = ['Boot', 'Sandal', 'Shoe']

def predict_image(image_path):
    img_array = preprocess_image_for_prediction(image_path)
    predictions = model.predict(img_array)
    predicted_class = class_labels[np.argmax(predictions)]
    confidence = float(np.max(predictions))
    return {
        "predicted_class": predicted_class,
        "confidence": confidence
    }
