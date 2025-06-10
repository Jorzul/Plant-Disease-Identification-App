import json
from pathlib import Path

MODEL_PATH = 'C:/Users/User/FruitsCCNs/Application/PlantsLeaves_classify.keras'
IMG_HEIGHT = 180
IMG_WIDTH = 180
USER_DATA_FILE = Path("users.json")
FEEDBACK_DATA_FILE = Path("feedbacks.json")

# A list of all possible disease categories the model can predict.
DATA_CATEGORY = [
        'Apple Black Rot', 'Apple Cedar Rust', 'Apple Scab', 'Cherry Powdery Mildew', 'Corn Cercospora Leaf Spot', 
        'Corn Common Rust', 'Corn Northern Leaf Blight', 'Grape Black Measles', 'Grape Black Rot', 'Grape Leaf Blight', 
        'Healthy Apple', 'Healthy Blueberry', 'Healthy Cherry', 'Healthy Corn', 'Healthy Grape', 'Healthy Peach', 'Healthy Pepper Bell', 
        'Healthy Potato', 'Healthy Raspberry', 'Healthy Soybean', 'Healthy Strawberry', 'Healthy Tomato', 'No Leaf Image', 
        'Orange Haunglongbing (Citrus Greening)', 'Peach Bacterial Spot', 'Pepper Bell Bacterial Spot', 'Potato Early Blight', 
        'Potato Late Blight', 'Squash Powdery Mildew', 'Strawberry Leaf Scorch', 'Tomato Bacterial Spot', 'Tomato Early Blight', 
        'Tomato Late Blight', 'Tomato Leaf Mold', 'Tomato Mosaic Virus', 'Tomato Septoria Leaf Spot', 'Tomato Spider Mites', 
        'Tomato Target Spot', 'Tomato Yellow Leaf Curl Virus'
    ]

with open('C:/Users/User/FruitsCCNs/Application/disease_info.json', 'r') as file:
    DISEASE_INFO = json.load(file)
