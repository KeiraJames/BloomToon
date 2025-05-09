import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from api_config import MONGO_URI

uri = MONGO_URI

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['temp_moisture'] 
collection = db['c1']  

def get_latest_stats():
    # Fetch the latest data (no need to count documents or sort, just fetch the most recent entry)
    latest_data = collection.find_one(sort=[('timestamp', -1)])  # Sort by timestamp descending and get the most recent
    return latest_data
    
def get_latest_temperature_and_moisture():
    latest_data = collection.find_one(sort=[('timestamp', -1)])
    if latest_data:
        temperature = latest_data.get("temperature")
        moisture_value = latest_data.get("moisture_value")
        return temperature, moisture_value
    return None, None

# Convert sensor value to percentage (capped at 1000)
def moisture_to_percentage(sensor_value):
    return min(sensor_value, 1000) / 1000 * 100

# Define the plant mood function based on sensor value
def plant_mood(sensor_value):
    if sensor_value <= 400:
        return "I'm thirsty! 🥵", "red"
    elif sensor_value <= 700:
        return "I'm happy! 😊", "green"
    else:
        return "I'm drowning! 😫", "yellow"

st.title("Plant Care Monitor")

# Button to fetch the latest data
if st.button("Give Me Stats Update"):
    data = get_latest_stats()

    if data:
        temperature = data["temperature"]
        moisture_value = data["moisture_value"]
        timestamp = data["timestamp"]

        # Convert timestamp to a readable format
        timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        input_str = timestamp
        input_time = datetime.strptime(input_str, "%Y-%m-%d %H:%M:%S")

        # Current time
        now = datetime.now()

        # Time difference in seconds
        delta = now - input_time
        total_seconds = int(delta.total_seconds())

        # Convert to minutes and seconds
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        # Moisture level as a percentage
        moisture_percentage = moisture_to_percentage(moisture_value)
        mood, color = plant_mood(moisture_value)

        # Output
        st.write(f"**Temperature**: {int(temperature):.0f}°F")
        st.write(f"**Moisture Level**: {moisture_percentage:.1f}%")
        st.write(f"**Last Updated**: {minutes} minutes, {seconds} seconds")
        st.write(f"Plant mood: {mood}")

        # Thermometer bar (colored based on the moisture level)
        st.markdown(f"""
        <div style="width: 100%; background-color: #f0f0f0; border-radius: 25px; height: 30px;">
            <div style="width: {moisture_percentage}%; background-color: {color}; border-radius: 25px; height: 100%;"></div>
        </div>
        """, unsafe_allow_html=True)

        # Plant status based on moisture level
        if moisture_value <= 400:
            st.warning("Your plant needs water!")
        elif moisture_value <= 700:
            st.info("Your plant is doing okay!")
        else:
            st.success("Your plant is happy and hydrated!")
    else:
        st.error("No data available.")
