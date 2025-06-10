# app.py (Modified)

import streamlit as st
import pandas as pd
import config
import utils
import user_management as um
import re
import datetime
import time
import random
import main_screen

# --- App Layout ---
st.set_page_config(page_title="Plant Disease Identifier", layout="centered")

# --- User Authentication ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
if 'active_tab' not in st.session_state: # New: Initialize active_tab
    st.session_state.active_tab = "Home"

st.title('Plant Disease Identification App')

# Function to change tab
def set_active_tab(tab_name):
    st.session_state.active_tab = tab_name

# --- Page Navigation ---
if not st.session_state.logged_in:
    # Pass the active tab and the setter function to st.tabs
    tab1, tab2, tab3 = st.tabs(["Home", "Login", "Register"])

    with tab1:
        # Render the main home screen, passing the tab setter
        main_screen.render_main_screen(set_active_tab)

    with tab2:
        # Login form content here
        st.subheader("Login to your account")
        with st.form("login_form_tab"):
            email = st.text_input("Email", key="login_email_tab")
            password = st.text_input("Password", type="password", key="login_password_tab")
            submitted = st.form_submit_button("Login")

            if submitted:
                with st.spinner("Logging in..."): # Spinner for login
                    time.sleep(random.uniform(0.1, 1.5))
                    user = um.login_user(email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_name = user['name']
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

    with tab3:
        # Register form content here
        st.subheader("Create a new account")
        with st.form("register_form_tab"):
            name = st.text_input("Name", key="register_name_tab")
            email = st.text_input("Email", key="register_email_tab")
            password = st.text_input("Password", type="password", key="register_password_tab")
            confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password_tab")
            submitted = st.form_submit_button("Register")

            if submitted:
                with st.spinner("Checking..."): # Spinner for login
                    time.sleep(random.uniform(0.1, 1.5))
                    if password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(name) < 3:
                        st.error("Invalid Name. Name should have 3 characters or more.")
                    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                        st.error("Email is not valid.")
                    elif um.email_exists(email):
                        st.warning("Email already registered. Please login.")
                    else:
                        um.register_user(name, email, password)
                        st.success("Registration successful! Please login.")

if st.session_state.logged_in:
    # --- Main App for Logged-in Users ---
    st.sidebar.header(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.text('Thanks for using the Application!')
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.rerun() # Rerun to go back to login page

    # --- Model Loading ---
    model = utils.load_model(config.MODEL_PATH)

    # --- Text ---
    st.subheader('How to use the application')
    st.text('First step: Take a photo of the plant\'s leaf that you want to review.')
    st.text('Second step: Choose the photo and wait for the analysis.')
    st.text('Check the treatment or search the web for further information.')

    # --- File Uploader and Main Logic ---
    uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None and model is not None:
        with st.spinner("Analyzing image and predicting disease..."):
            time.sleep(random.uniform(0.1, 1.5))
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
            'Confidence': [score for score in top_5_scores]
        })

        # Sort for better visual clarity
        chart_data = chart_data.sort_values(by='Confidence', ascending=False)
        chart_data.index += 1

        # Create layout with expander
        with st.expander("Show Alternative Diagnoses", expanded=True):
            st.write("The model considers these as the most likely possibilities, ranked by confidence level:")
            st.dataframe(chart_data.style.format({'Confidence': "{:.2f}%"}), use_container_width=True)
        
        # --- Report Form ---
        st.markdown("---")
        st.subheader("Feedback on Analysis")

        feedback_text = st.text_area("If you have any comments, please type them here:", key="feedback_comments")

        st.write("Are you satisfied with the analysis?")

        col_yes, col_no = st.columns(2)
        with col_yes:
            yes_button = st.button("Yes", key="feedback_yes")
        with col_no:
            no_button = st.button("No", key="feedback_no")

        if yes_button or no_button:
            with st.spinner("Submitting..."):
                time.sleep(random.uniform(0.2, 1.5))
                satisfaction = "Yes" if yes_button else "No"
                if um.save_feedback(st.session_state.user_name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), top_class, f"{top_score:.2f}%", satisfaction, feedback_text):
                    st.success("Thank you for your feedback!")
                else:
                    st.error('You already submitted a feedback.')

    elif model is None:
        st.stop() # Stops the script if the model failed to load