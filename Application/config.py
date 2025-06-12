import json
from pathlib import Path

# --- Model Configuration ---
# A dictionary to hold the names and paths of the available models.
# The keys are the names that will be displayed to the user.
# The values are the file paths to the corresponding .keras models.
MODEL_PATHS = {
    "LeafSnap": 'C:/Users/User/FruitsCCNs/models/PlantsLeaves_classify_2.keras',
    "MobileNetV2": 'C:/Users/User/OneDrive/Documents/GitHub/Plant-Disease-Identification-App/models/PlantsLeaves_classify_MobileNetV2.keras',
    "EfficientNetV2": 'C:/Users/User/OneDrive/Documents/GitHub/Plant-Disease-Identification-App/models/PlantsLeaves_classify_EfficientNetV2.keras'
}

# --- Image Dimensions ---
IMG_HEIGHT = 180
IMG_WIDTH = 180

# --- Data Files ---
USER_DATA_FILE = Path("users.json")
FEEDBACK_DATA_FILE = Path("feedbacks.json")

# Load the categories from the JSON file
try:
    with open('C:/Users/User/OneDrive/Documents/GitHub/Plant-Disease-Identification-App/Application/disease_categories.json', 'r') as file:
        DATA_CATEGORY = json.load(file)
except FileNotFoundError:
    DATA_CATEGORY = [] # If the file is not found, use an empty list.

# Load disease information from a JSON file.
try:
    with open('C:/Users/User/OneDrive/Documents/GitHub/Plant-Disease-Identification-App/Application/disease_info.json', 'r') as file:
        DISEASE_INFO = json.load(file)
except FileNotFoundError:
    DISEASE_INFO = {} # If the file is not found, use an empty dictionary.

