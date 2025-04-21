import sys
import os

# Add the path to src so Python can find chatbot.py
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from chatbot import chat_with_plant

# Sample mock plant care data
mock_care_info = {
    "Plant Name": "Aloe Vera",
    "Light Requirements": "Bright, indirect sunlight",
    "Watering": "Allow soil to dry completely between watering",
    "Humidity Preferences": "Low humidity",
    "Temperature Range": "55-80°F (13-27°C)",
    "Feeding Schedule": "Once a month during spring and summer",
    "Toxicity": "Mildly toxic to pets",
    "Additional Care": "Avoid overwatering. Use well-draining soil.",
    "Personality": {
        "Title": "The Independent Healer",
        "Traits": ["Resilient", "Low-maintenance", "Helpful"],
        "Prompt": "You are a calm and wise plant who enjoys solitude and gives healing advice."
    }
}

# Test user input
user_input = "Do you like being near a window?"

# Get chatbot response
response = chat_with_plant(mock_care_info, user_input)

# Show the result
print("Plant says:", response)

