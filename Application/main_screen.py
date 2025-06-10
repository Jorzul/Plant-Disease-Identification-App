# main_screen.py (Modified)

import streamlit as st
import user_management as um

def render_main_screen(set_active_tab_callback): # Added callback argument
    """Renders the main home screen content within Streamlit."""

    # Custom CSS for the new dark theme
    st.markdown("""
    <style>
        /* General body styling */
        .stApp {
            background-color: #111827; /* Dark Blue-Gray */
        }

        /* Hero section styling */
        .hero-section {
            padding: 2rem 1rem;
            text-align: center;
            background-color: #1F2937; /* Darker Blue-Gray */
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        }
        .hero-title {
            font-size: 2.5rem;
            text-align: center;
            font-weight: 800;
            color: #F9FAFB; /* Off-White */
        }
        .hero-title .highlight {
            color: #22c55e; /* Bright Green */
        }
        .hero-subtitle {
            font-size: 1.125rem;
            color: #9CA3AF; /* Light Gray */
            max-width: 600px;
            margin: 1rem auto 0;
        }

        /* Section styling */
        .section {
            background-color: #1F2937; /* Darker Blue-Gray */
            padding: 2rem 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        }
        .section-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-title {
            font-size: 1.875rem;
            font-weight: 800;
            color: #FFFFFF; /* White */
        }
        .section-subtitle {
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            color: #22c55e; /* Bright Green */
        }
        
        /* General paragraph text color within sections */
        .section p {
            color: #D1D5DB; /* Light Gray */
        }

        /* "How It Works" step styling */
        .step {
            text-align: center;
            padding: 1rem;
        }
        .step-number {
            background-color: #22c55e;
            color: #111827;
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0 auto 1rem;
        }
        .step-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #F9FAFB; /* Off-White */
            margin-bottom: 0.5rem;
        }
        .step-description {
            color: #9CA3AF; /* Light Gray */
        }
        
        /* Feature card styling */
        .feature-card {
            background-color: #374151; /* Gray */
            padding: 1.5rem;
            border-radius: 0.5rem;
            text-align: center;
            height: 100%;
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #22c55e;
        }
        .feature-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #F9FAFB;
        }
        .feature-card .step-description { /* Reusing step-description class */
             color: #D1D5DB;
        }


        /* Feedback card styling */
        .feedback-card {
            background-color: #1F2937;
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            margin-bottom: 1rem;
            border-left: 5px solid #22c55e;
        }
        .feedback-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }
        .feedback-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background-color: #10B981;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-right: 1rem;
        }
        .feedback-user {
            font-weight: 600;
            color: #F9FAFB;
        }
        .feedback-date {
            font-size: 0.875rem;
            color: #9CA3AF;
        }
        .feedback-comment {
            font-style: italic;
            color: #D1D5DB;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            padding: 2rem 1rem;
            color: #9CA3AF;
            font-size: 0.875rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Hero Section ---
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">
            <span>Identify Plant Diseases</span>
            <span class="highlight">Instantly.</span>
        </h1>
        <p>
            Snap a photo of a plant leaf, and our AI will analyze it to detect diseases and provide you with treatment information.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- About Section ---
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <h2 class="section-subtitle">About Us</h2>
            <p class="section-title">A smart solution for healthy plants.</p>
        </div>
        <p style="text-align: center; max-width: 700px; margin: 0 auto; color: #D1D5DB;">
            Our application leverages the power of Convolutional Neural Networks (CNNs) to identify a wide range of plant diseases from simple leaf images. We aim to provide farmers, gardeners, and plant enthusiasts with an easy-to-use tool for quick diagnosis and effective treatment.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    
    # --- How It Works Section ---
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <h2 class="section-subtitle">How It Works</h2>
            <p class="section-title">Three simple steps to a diagnosis.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="step">
            <div class="step-number">1</div>
            <h3 class="step-title">Take a Photo</h3>
            <p class="step-description">Capture a clear image of the plant's leaf you want to analyze.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="step">
            <div class="step-number">2</div>
            <h3 class="step-title">Upload & Analyze</h3>
            <p class="step-description">Upload your photo. Our CNN model will process it to predict the disease.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="step">
            <div class="step-number">3</div>
            <h3 class="step-title">Get Results</h3>
            <p class="step-description">Receive the diagnosis, confidence score, and treatment options.</p>
        </div>
        """, unsafe_allow_html=True)
        
    # --- Key Features Section ---
    st.markdown("""
    <div class="section" style="background-color: transparent; border: none;">
        <div class="section-header">
            <h2 class="section-subtitle">Key Features</h2>
            <p class="section-title">Everything you need for plant care.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👁️</div>
            <h3 class="feature-title">High-Accuracy Detection</h3>
            <p class="step-description">Utilizes a powerful CNN model for precise disease identification.</p>
        </div>
        """, unsafe_allow_html=True)
    with f_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">ℹ️</div>
            <h3 class="feature-title">Detailed Information</h3>
            <p class="step-description">Provides descriptions and treatment advice for detected diseases.</p>
        </div>
        """, unsafe_allow_html=True)
    with f_col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Alternative Diagnoses</h3>
            <p class="step-description">See the top 5 most likely diseases to better understand the analysis.</p>
        </div>
        """, unsafe_allow_html=True)


    # --- Feedback Section ---
    st.markdown("""
    <div class="section" style="margin-top: 2rem;">
        <div class="section-header">
            <h2 class="section-subtitle">User Feedback</h2>
            <p class="section-title">What our users are saying.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    feedbacks = um.load_feedback()
    if feedbacks:
        # Create two columns for a more organized layout
        feedback_col1, feedback_col2 = st.columns(2)
        feedback_items = list(feedbacks.items())
        
        for i, (user, feedback) in enumerate(feedback_items):
            card_html = f"""
            <div class="feedback-card">
                <div class="feedback-header">
                    <div class="feedback-avatar">{user[0].upper()}</div>
                    <div>
                        <div class="feedback-user">{user}</div>
                        <div class="feedback-date">{feedback.get('Date', '')}</div>
                    </div>
                </div>
                <p class="feedback-comment">"{feedback.get('Comment', 'No comment provided.')}"</p>
            </div>
            """
            if i % 2 == 0:
                with feedback_col1:
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                with feedback_col2:
                    st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.info("No feedback has been submitted yet.")

    # --- Footer ---
    st.markdown("""
    <div class="footer">
        <p>&copy; 2025 Jorza Ionut. All rights reserved. Built with Streamlit.</p>
    </div>
    """, unsafe_allow_html=True)