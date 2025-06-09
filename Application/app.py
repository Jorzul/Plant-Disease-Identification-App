# app.py

import streamlit as st
import pandas as pd
import config
import utils

# --- App Layout ---
st.sidebar.header("Hello, Guest!")
st.sidebar.button("Logout") # This is a placeholder

st.header('🌿 Plant Disease Identification')
st.write('Upload an image of a plant leaf to identify potential diseases.')

# --- Model Loading ---
model = utils.load_model(config.MODEL_PATH)

# --- File Uploader and Main Logic ---
uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and model is not None:
    # Process the image and get predictions
    image, top_class, top_score, top_5_classes, top_5_scores = utils.process_and_predict(
        uploaded_file, model, config.DATA_CATEGORY, config.IMG_WIDTH, config.IMG_HEIGHT
    )
    
    # --- Display Results ---
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption='Uploaded Image', width=200)

    with col2:
        st.subheader("Top Prediction")
        st.success(f"**{top_class.replace('___', ' - ')}**")
        st.write(f"Confidence: **{top_score:.2f}%**")

    # --- Display Disease Information ---
    st.markdown("---")
    st.subheader("Disease Information & Recommendations")
    info = config.DISEASE_INFO.get(top_class, {
        'description': 'No detailed information available for this category.',
        'treatment': 'General advice: ensure proper watering, fertilization, and air circulation. Consult a local agricultural extension for specific advice.',
        'link': 'https://www.google.com'
    })
    
    with st.expander("Show Details", expanded=True):
        st.markdown(f"**Description:** {info['description']}")
        st.markdown(f"**Suggested Treatment:** {info['treatment']}")
        st.markdown(f"**More info:** {info['link']}")

    # --- Display Top-5 Predictions Chart ---
    st.markdown("---")
    st.subheader("Alternative Diagnoses")

    # Prepare and format chart data
    chart_data = pd.DataFrame({
        'Disease': top_5_classes,
        'Confidence': [score for score in top_5_scores]  # Convert to percentage
    })

    # Sort for better visual clarity
    chart_data = chart_data.sort_values(by='Confidence')
    chart_data.index += 1

    # Create layout with expander
    with st.expander("Show Alternative Diagnoses", expanded=True):
        st.write("The model considers these as the most likely possibilities, ranked by confidence level:")

        # Optional: Display data table
        st.dataframe(chart_data.style.format({'Confidence': "{:.2f}%"}), use_container_width=True)

elif model is None:
    st.stop() # Stops the script if the model failed to load