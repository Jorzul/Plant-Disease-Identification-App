import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from PIL import Image
import io
import utils

class TestUtils(unittest.TestCase):

    def setUp(self):
        """Set up a mock model and test data."""
        # Create a mock Keras model
        self.mock_model = MagicMock()
        # Configure the predict method to return a sample prediction
        self.mock_model.predict.return_value = np.array([[0.1, 0.2, 0.6, 0.05, 0.05]]) # 5 classes

        self.data_category = ['Apple - Scab', 'Apple - Black rot', 'Apple - Cedar apple rust', 'Apple - healthy', 'Background']
        self.img_width = 224
        self.img_height = 224

        # Create a dummy image in memory
        self.image_file = io.BytesIO()
        Image.new('RGB', (self.img_width, self.img_height)).save(self.image_file, 'PNG')
        self.image_file.seek(0) # Reset buffer to the beginning

    @patch('utils.tf.keras.models.load_model')
    def test_load_model_success(self, mock_load):
        """Test that the model loads successfully."""
        mock_load.return_value = "Mocked Model"
        model = utils.load_model("fake/path/model.h5")
        self.assertEqual(model, "Mocked Model")

    @patch('utils.tf.keras.models.load_model', side_effect=IOError("File not found"))
    @patch('utils.st.error')
    def test_load_model_failure(self, mock_st_error, mock_load):
        """Test that an error is reported if the model file is not found."""
        model = utils.load_model("bad/path/model.h5")
        self.assertIsNone(model)
        # Check that streamlit's error function was called
        mock_st_error.assert_called_once()

    def test_process_and_predict(self):
        """Test the image processing and prediction logic."""
        (image,
         top_prediction_class,
         top_prediction_score,
         top_5_classes,
         top_5_scores) = utils.process_and_predict(self.image_file,
                                                    self.mock_model,
                                                    self.data_category,
                                                    self.img_width,
                                                    self.img_height)

        # Verify model was called once
        self.mock_model.predict.assert_called_once()

        # Check top prediction
        self.assertEqual(top_prediction_class, 'Apple - Cedar apple rust')
        self.assertAlmostEqual(top_prediction_score, 60.0, places=1)

        # Check top 5 predictions (or as many as are available)
        self.assertEqual(len(top_5_classes), 5)
        self.assertEqual(len(top_5_scores), 5)

        # Check the order of top 5
        self.assertEqual(top_5_classes[0], 'Apple - Cedar apple rust')
        self.assertEqual(top_5_classes[1], 'Apple - Black rot')

        # Check that scores are correctly calculated
        self.assertAlmostEqual(top_5_scores[0], 60.0, places=1)
        self.assertAlmostEqual(top_5_scores[1], 20.0, places=1)
        self.assertAlmostEqual(top_5_scores[2], 10.0, places=1)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)