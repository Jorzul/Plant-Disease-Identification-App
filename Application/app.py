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
st.set_page_config(page_title="LeafSnap", layout="centered")

# --- User Authentication ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
if 'active_page' not in st.session_state:
    st.session_state.active_page = "Home"

# --- Styling ---
st.markdown("""
    <style>
            .title {
                text-align: center;
                font-size: 5em;
                color: #4CAF50;
                font-weight: bold;
                margin-bottom: 20px;
            }
            div[data-testid="column"] {
            text-align: center;
            }
            .st-emotion-cache-8atqhb {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .st-emotion-cache-ktz07o {
                background-color: #4CAF50; /* Green background */
                color: #d6f7d4; /* White text */
                font-size: 20px; /* Larger font size */
                font-weight: bold;
                padding: 10px 24px; /* Larger padding */
                border-radius: 8px; /* Rounded corners */
                width: 100%; /* Make buttons fill the column width */
                border: none; /* Remove default border */
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* Add a subtle shadow */
                transition: 0.3s; /* Smooth transition for hover effect */
            }
            .st-emotion-cache-ktz07o:hover {
                background-color: green; /* Darker green on hover */
                box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
                color: #8afa83 /* Larger shadow on hover */
            }
    </style>""", unsafe_allow_html=True)
st.markdown('<div class="title">LeafSnap</div>', unsafe_allow_html=True)

# Function to change page
def set_active_page(page_name):
    st.session_state.active_page = page_name

# --- Authentication and Navigation ---
if not st.session_state.logged_in:
    # Create centered navigation buttons
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.markdown('<div class="nav-button">', unsafe_allow_html=True)
        st.button("Home", on_click=set_active_page, args=("Home",))
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="nav-button">', unsafe_allow_html=True)
        st.button("Login", on_click=set_active_page, args=("Login",))
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="nav-button">', unsafe_allow_html=True)
        st.button("Register", on_click=set_active_page, args=("Register",))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")

    # Render the appropriate page based on selection
    if st.session_state.active_page == "Home":
        main_screen.render_main_screen(set_active_page)
    elif st.session_state.active_page == "Login":
        st.subheader("Login to your account")
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login")

            if submitted:
                with st.spinner("Logging in..."):
                    time.sleep(random.uniform(0.1, 1.5))
                    user = um.login_user(email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_name = user['name']
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

    elif st.session_state.active_page == "Register":
        st.subheader("Create a new account")
        with st.form("register_form"):
            name = st.text_input("Name", key="register_name")
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")
            submitted = st.form_submit_button("Register")

            if submitted:
                with st.spinner("Checking..."):
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
                        set_active_page("Login")

# --- Main App for Logged-in Users ---
if st.session_state.logged_in:
    # --- Sidebar ---
    st.sidebar.header(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.text('Thanks for using LeafSnap!')

    # --- Model Selection ---
    st.sidebar.subheader("Select Model")
    # Create a selectbox with model names from the config file.
    model_name = st.sidebar.selectbox(
        "Choose a model for prediction:",
        list(config.MODEL_PATHS.keys())
    )
    
    st.sidebar.subheader("How to use")
    with st.sidebar.expander("Show instructions"):
        st.sidebar.markdown("1. Choose the prediction model from the dropdown above.")
        st.sidebar.markdown("2. Upload an image of a plant's leaf.")
        st.sidebar.markdown("3. Wait for the analysis to complete.")
        st.sidebar.markdown("4. Review the diagnosis and treatment recommendations.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.rerun()

    # --- Model Loading with Caching ---
    # @st.cache_resource is used to cache the loaded model.
    # This means the model is loaded only once per selection, making the app faster.
    @st.cache_resource
    def load_selected_model(name):
        model_path = config.MODEL_PATHS[name]
        return utils.load_model(model_path)

    model = load_selected_model(model_name)

    # --- File Uploader and Main Logic ---
    uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None and model is not None:
        with st.spinner(f"Using {model_name} to analyze image..."):
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
            'treatment': 'General advice: ensure proper watering, fertilization, and air circulation.',
            'link': 'No link available.'
        })
        
        with st.expander("Show Details", expanded=True):
            st.markdown(f"**Description:** {info['description']}")
            st.markdown(f"**Suggested Treatment:** {info['treatment']}")
            st.markdown(f"**More info:** ({info['link']})")

        # --- Display Top-5 Predictions Chart ---
        st.markdown("---")
        st.subheader("Alternative Diagnoses")

        chart_data = pd.DataFrame({
            'Disease': top_5_classes,
            'Confidence': [score for score in top_5_scores]
        })
        chart_data = chart_data.sort_values(by='Confidence', ascending=False)
        chart_data.index += 1

        with st.expander("Show Alternative Diagnoses", expanded=True):
            st.write("The model considers these as the most likely possibilities, ranked by confidence:")
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
        st.error(f"Could not load the {model_name} model. Please check the model path in config.py and ensure the file is not corrupted.")
        st.stop()
