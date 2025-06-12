import tensorflow as tf
import streamlit as st
import numpy as np
from PIL import Image

def load_model(path):
    """Loads the Keras model with error handling."""
    try:
        model = tf.keras.models.load_model(path)
        return model
    except (IOError, ImportError) as e:
        st.error(f"Error loading model: {e}. Make sure '{path}' is in the correct directory.")
        return None

def process_and_predict(image_file, model, data_category, img_width, img_height):
    """
    Processes the uploaded image and returns prediction results.
    """
    # Open the image
    image = Image.open(image_file).convert("RGB")
    
    # Preprocess the image
    image_resized = image.resize((img_width, img_height))
    img_array = tf.keras.utils.img_to_array(image_resized)
    img_batched = tf.expand_dims(img_array, 0)

    # Predict
    predictions = model.predict(img_batched)
    scores = predictions[0]

    # --- Get Top Prediction ---
    top_prediction_index = np.argmax(scores)
    top_prediction_class = data_category[top_prediction_index]
    top_prediction_score = 100 * np.max(scores)
    
    # --- Get Top 5 Predictions ---
    top_5_indices = np.argsort(scores)[-5:][::-1]
    top_5_scores = [100 * scores[i] for i in top_5_indices]
    top_5_classes = [data_category[i].replace('___', ' - ') for i in top_5_indices]

    return image, top_prediction_class, top_prediction_score, top_5_classes, top_5_scores