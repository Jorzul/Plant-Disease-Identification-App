import unittest
from unittest.mock import patch, mock_open, ANY
import json
import hashlib
import user_management

class TestUserManagement(unittest.TestCase):

    def setUp(self):
        """Set up a fresh state for each test."""
        # This password hashes to the value stored in test_users
        self.raw_password = "password123"
        self.hashed_password = hashlib.sha256(self.raw_password.encode()).hexdigest()
        
        self.test_users = {
            "test@example.com": {
                "name": "Test User",
                "password": self.hashed_password
            }
        }
        self.test_feedback = {
            "test@example.com": {
                "Date": "2025-06-15",
                "Predicted_Class": "Some Disease",
                "Confidence": 95.5,
                "Satisfied": "Yes",
                "Comment": "Great prediction!"
            }
        }
        
    @patch('user_management.load_users')
    def test_register_user_already_exists(self, mock_load_users):
        """Test that registering a user with an existing email fails."""
        # ARRANGE: a user with this email already exists
        mock_load_users.return_value = self.test_users
        
        # ACT & ASSERT
        result = user_management.register_user("Another Name", "test@example.com", "another_password")
        self.assertFalse(result)

    @patch('user_management.load_users')
    def test_login_user_success(self, mock_load_users):
        """Test that a user can log in with correct credentials."""
        # ARRANGE
        mock_load_users.return_value = self.test_users
        
        # ACT
        user_info = user_management.login_user("test@example.com", self.raw_password)
        
        # ASSERT
        self.assertIsNotNone(user_info)
        self.assertEqual(user_info['name'], "Test User")

    @patch('user_management.load_users')
    def test_login_user_failure(self, mock_load_users):
        """Test that login fails with an incorrect password."""
        # ARRANGE
        mock_load_users.return_value = self.test_users
        
        # ACT
        user_info = user_management.login_user("test@example.com", "wrong_password")
        
        # ASSERT
        self.assertIsNone(user_info)

    @patch('user_management.load_users')
    def test_email_exists(self, mock_load_users):
        """Test that email_exists correctly identifies an existing email."""
        # ARRANGE
        mock_load_users.return_value = self.test_users
        
        # ACT & ASSERT
        self.assertTrue(user_management.email_exists("test@example.com"))
        self.assertFalse(user_management.email_exists("nonexistent@example.com"))

    @patch('user_management.save_feedback')
    @patch('user_management.load_feedback', return_value={})
    def test_save_feedback_success(self, mock_load_feedback, mock_save_feedback):
        """Test that feedback from a new user is saved successfully."""
        result = user_management.save_feedback("new_user@example.com", "2025-06-15", "Class A", 99.9, "Yes", "Works well.")
        self.assertTrue(result)

    @patch('user_management.load_feedback')
    def test_save_feedback_user_already_submitted(self, mock_load_feedback):
        """Test that a user cannot submit feedback more than once."""
        # ARRANGE
        mock_load_feedback.return_value = self.test_feedback

        # ACT & ASSERT
        result = user_management.save_feedback("test@example.com", "2025-06-16", "Class B", 80.0, "No", "Second try.")
        self.assertFalse(result)

if __name__ == '__main__':
    # The arguments are needed to run in some environments, but can be removed if running from command line.
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
