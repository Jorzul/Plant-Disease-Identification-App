# user_management.py

import json
from pathlib import Path
import hashlib
import config
USER_DATA_FILE = config.USER_DATA_FILE
FEEDBACK_DATA_FILE = config.FEEDBACK_DATA_FILE

def load_users():
    """Loads users from the JSON file."""
    if USER_DATA_FILE.exists():
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Saves the user dictionary to the JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- User Actions ---
def register_user(name, email, password):
    """Adds a new user to the database with a hashed password."""
    users = load_users()
    if email in users:
        return False  # User already exists

    users[email] = {
        'name': name,
        'password': hash_password(password)
    }
    save_users(users)
    return True

def login_user(email, password):
    """Authenticates a user and returns user info if successful."""
    users = load_users()
    hashed_password = hash_password(password)
    
    if email in users and users[email]['password'] == hashed_password:
        return users[email]
    return None

def email_exists(email):
    """Checks if an email is already registered."""
    users = load_users()
    return email in users

def load_feedback():
    """Loads users from the JSON file."""
    if FEEDBACK_DATA_FILE.exists():
        with open(FEEDBACK_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_feedback(user, date, predicted_class, confidence, satisfied, comment):
    """Appends user feedback to a JSON file."""
    feedbacks = load_feedback()
    if user in feedbacks:
        return False  # User already submitted feedback

    feedbacks[user] = {
        'Date': date,
        'Predicted_Class': predicted_class,
        'Confidence': confidence,
        'Satisfied': satisfied,
        'Comment': comment
    }

    with open(FEEDBACK_DATA_FILE, 'w') as f:
        json.dump(feedbacks, f, indent=4)
    return True