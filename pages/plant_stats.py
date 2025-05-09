import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timezone # Added timezone
from api_config import MONGO_URI

# --- Configuration ---
uri = MONGO_URI
client = MongoClient(uri)
db = client['temp_moisture']
collection = db['c1']

# Ring Colors (Progress and Track)
MOISTURE_COLOR = "#FF2D55" # Pink/Red
MOISTURE_TRACK_COLOR = "#591F2E" # Darker, less saturated pink
TEMPERATURE_COLOR = "#A4E803" # Bright Green
TEMPERATURE_TRACK_COLOR = "#4B6A01" # Darker, less saturated green
FRESHNESS_COLOR = "#00C7DD" # Cyan
FRESHNESS_TRACK_COLOR = "#005C67" # Darker, less saturated cyan
WHITE_COLOR = "#FFFFFF"
LIGHT_GREY_TEXT_COLOR = "#A3A3A3" # For subtitles and less prominent text
WATCH_BG_COLOR = "#000000" # Black background for watch face

# Ring Value Configuration
MOISTURE_MAX_RAW = 1000  # Max raw value for moisture sensor for ring scaling
TEMP_DISPLAY_MAX = 100   # Max temperature for ring scaling (e.g., 100°F)
TEMP_DISPLAY_MIN = 32    # Min temperature for ring scaling (e.g., 32°F)
FRESHNESS_MAX_MINUTES = 60 # Data older than this will show an empty ring (e.g., 60 minutes)

# --- Helper Functions ---
def get_latest_stats():
    latest_data = collection.find_one(sort=[('timestamp', -1)])
    return latest_data

def calculate_time_difference_minutes(timestamp_val):
    # Ensure timestamp_val is a datetime object, assuming it's UTC from DB
    if isinstance(timestamp_val, (int, float)):
        data_time_utc = datetime.fromtimestamp(timestamp_val, timezone.utc)
    elif isinstance(timestamp_val, datetime):
        if timestamp_val.tzinfo is None: # If naive, assume UTC
            data_time_utc = timestamp_val.replace(tzinfo=timezone.utc)
        else:
            data_time_utc = timestamp_val.astimezone(timezone.utc)
    else:
        return 0 # Or raise error

    now_utc = datetime.now(timezone.utc)
    delta = now_utc - data_time_utc
    return int(delta.total_seconds() // 60)

# Convert sensor value to percentage (capped at 1000)
def moisture_to_display_percentage(sensor_value):
    return min(sensor_value, MOISTURE_MAX_RAW) / MOISTURE_MAX_RAW * 100

def plant_mood(sensor_value):
    if sensor_value <= 400:
        return "I'm thirsty! 🥵", "red"
    elif sensor_value <= 700:
        return "I'm happy! 😊", "green"
    else:
        return "I'm drowning! 😫", "yellow"

# --- HTML/CSS Generation ---
def get_ring_html_css():
    # Define CSS once
    # Note: CSS for the progress indicator dot is tricky and might need fine-tuning.
    # The ::before pseudo-element is used for the track, and the main background for progress.
    # A small div is used for the indicator dot.
    css = f"""
<style>
    .watch-face-grid {{
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 20px; /* Gap between watch faces */
    }}
    .watch-face-container {{
        background-color: {WATCH_BG_COLOR};
        padding: 15px;
        border-radius: 18px; /* Rounded corners for the watch body */
        width: 220px; /* Fixed width for each watch face */
        height: auto; /* Adjust height based on content */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
        color: {WHITE_COLOR};
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .watch-header {{
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 5px;
        margin-bottom: 10px;
    }}
    .ring-title {{
        font-size: 16px;
        font-weight: 600;
    }}
    .ring-timestamp {{
        font-size: 14px;
        color: {LIGHT_GREY_TEXT_COLOR};
    }}
    .ring-outer-circle {{
        width: 150px; /* Diameter of the ring */
        height: 150px;
        border-radius: 50%;
        position: relative; /* For positioning inner content and indicator */
        display: flex;
        align-items: center;
        justify-content: center;
        /* Track is a full circle of track_color, progress is overlaid by conic-gradient */
        /* Using a pseudo-element for the track for better layering */
    }}

    .ring-outer-circle::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 50%;
        padding: 12px; /* This creates the thickness of the ring. (Ring Diameter - Inner Hole Diameter) / 2 */
        background-clip: content-box; /* Background only applied to content area (the hole) */
        /* Set the track color here if using this method */
    }}

    .ring-progress {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        position: relative;
        /* Conic gradient for progress. Starts from 12 o'clock (270deg or -90deg) */
        /* background-image: conic-gradient(from -90deg, var(--progress-color) 0% var(--progress-percent), var(--track-color) var(--progress-percent) 100%); */
    }}
    
    .ring-inner-content {{
        position: absolute;
        color: {WHITE_COLOR};
        text-align: center;
    }}
    .ring-value {{
        font-size: 40px;
        font-weight: 500;
        line-height: 1.1;
    }}
    .ring-goal-text {{
        font-size: 12px;
        color: {LIGHT_GREY_TEXT_COLOR};
        text-transform: uppercase;
    }}
    .progress-indicator-dot {{
        width: 10px;
        height: 10px;
        background-color: {WHITE_COLOR};
        border-radius: 50%;
        position: absolute;
        /* Positioned at 12 o'clock on the edge of the ring's track, then rotated */
        top: 6px; /* Half of (ring_thickness - dot_diameter), if dot is on the track. Here, approx. (12px padding - dot_height/2)*/
        left: 50%;
        transform-origin: center calc(75px - 6px); /* Rotate around center of ring (150px/2 - top_offset) */
        /* transform: translateX(-50%) rotate(var(--dot-rotation-deg)); Set dynamically */
    }}

    .ring-dots {{
        margin-top: 10px;
        font-size: 18px;
    }}
    .ring-dots .dot-dim {{ color: #444; }}

    .ring-description {{
        font-size: 12px;
        color: {LIGHT_GREY_TEXT_COLOR};
        margin-top: 15px;
        text-align: left; /* Or center if preferred */
        width: 90%;
        line-height: 1.4;
    }}
</style>
    """
    return css

def generate_ring_html(title, value_text, goal_text, progress_percent,
                         color, track_color, timestamp_str, description, dot_index=0):
    # Cap progress percent between 0 and 100 for display
    progress_percent_capped = max(0, min(progress_percent, 100))
    
    # Angle for the dot: conic-gradient starts at -90deg (12 o'clock)
    # Rotation angle for dot: (progress_percent_capped / 100) * 360
    dot_rotation_deg = (progress_percent_capped / 100) * 360

    # Dots representation
    dots_html = "".join([
        f'<span class="dot-main" style="color:{color};">•</span> ' if i == dot_index
        else '<span class="dot-dim">•</span> '
        for i in range(3) # Assuming 3 rings/dots
    ])
    
    # Inline style for dynamic parts of the ring progress and dot
    # Using CSS variables for dynamic properties in style attribute
    ring_style = f"background-image: conic-gradient(from -90deg, {color} 0% {progress_percent_capped}%, {track_color} {progress_percent_capped}% 100%);"
    dot_style = f"transform: translateX(-50%) rotate({dot_rotation_deg}deg);"


    html = f"""
<div class="watch-face-container">
    <div class="watch-header">
        <span class="ring-title" style="color:{color};">{title}</span>
        <span class="ring-timestamp">{timestamp_str}</span>
    </div>
    <div class="ring-outer-circle">
        <div class="ring-progress" style="{ring_style}">
             <div class="progress-indicator-dot" style="{dot_style}"></div>
        </div>
        <div class="ring-inner-content">
            <div class="ring-value">{value_text}</div>
            <div class="ring-goal-text">{goal_text}</div>
        </div>
    </div>
    <div class="ring-dots">{dots_html}</div>
    <div class="ring-description">{description}</div>
</div>
    """
    return html

# --- Streamlit App ---
st.set_page_config(layout="wide") # Use wide layout for better spacing
st.title("Plant Care Monitor")

# Inject CSS
st.markdown(get_ring_html_css(), unsafe_allow_html=True)

if st.button("Give Me Stats Update"):
    data = get_latest_stats()

    if data:
        temperature_val = data.get("temperature", 0)
        moisture_val = data.get("moisture_value", 0)
        timestamp_epoch = data.get("timestamp", datetime.now(timezone.utc).timestamp())

        # Data processing for rings
        data_dt_utc = datetime.fromtimestamp(timestamp_epoch, timezone.utc)
        data_timestamp_H_M = data_dt_utc.strftime('%H:%M')
        minutes_since_update = calculate_time_difference_minutes(data_dt_utc)

        # 1. Moisture Ring
        moisture_progress = moisture_to_display_percentage(moisture_val)
        moisture_desc = f"""
        Measures active soil moisture. Current value: {moisture_val}.
        Goal is optimal hydration, typically between 400-700 raw units.
        """

        # 2. Temperature Ring
        # Normalize temperature to a 0-100% scale for the ring display
        temp_range = TEMP_DISPLAY_MAX - TEMP_DISPLAY_MIN
        if temp_range <= 0: temp_range = 1 # Avoid division by zero
        temperature_progress = ((temperature_val - TEMP_DISPLAY_MIN) / temp_range) * 100
        temperature_progress = max(0, min(temperature_progress, 100)) # Clamp
        temp_desc = f"""
        Current ambient temperature: {temperature_val}°F.
        Ideal range for many plants is 65-75°F. Ring shows temp relative to {TEMP_DISPLAY_MIN}-{TEMP_DISPLAY_MAX}°F.
        """

        # 3. Data Freshness Ring
        # Progress is inverse of age: fresher = fuller ring
        freshness_progress = max(0, (1 - (minutes_since_update / FRESHNESS_MAX_MINUTES))) * 100
        freshness_desc = f"""
        Indicates data recency. Last update was {minutes_since_update} min(s) ago.
        Fresher data provides a more current snapshot of plant conditions.
        """
        
        # Mood and warnings
        mood_text, _ = plant_mood(moisture_val)
        
        # Display rings in columns
        # We'll put the HTML generation inside st.markdown within columns
        # For dynamic content, the HTML string itself is built with the data

        col1_html = generate_ring_html(
            title="Moisture",
            value_text=str(int(moisture_val)),
            goal_text=f"OF {MOISTURE_MAX_RAW} RAW",
            progress_percent=moisture_progress,
            color=MOISTURE_COLOR,
            track_color=MOISTURE_TRACK_COLOR,
            timestamp_str=data_timestamp_H_M,
            description=moisture_desc,
            dot_index=0
        )
        col2_html = generate_ring_html(
            title="Temperature",
            value_text=str(int(temperature_val)),
            goal_text=f"OF {TEMP_DISPLAY_MAX}°F SCALE",
            progress_percent=temperature_progress,
            color=TEMPERATURE_COLOR,
            track_color=TEMPERATURE_TRACK_COLOR,
            timestamp_str=data_timestamp_H_M,
            description=temp_desc,
            dot_index=1
        )
        col3_html = generate_ring_html(
            title="Data Age",
            value_text=str(minutes_since_update),
            goal_text="MINS AGO",
            progress_percent=freshness_progress,
            color=FRESHNESS_COLOR,
            track_color=FRESHNESS_TRACK_COLOR,
            timestamp_str=data_timestamp_H_M,
            description=freshness_desc,
            dot_index=2
        )

        st.markdown(f'<div class="watch-face-grid">{col1_html}{col2_html}{col3_html}</div>', unsafe_allow_html=True)
        
        st.markdown("---") # Separator
        st.subheader("Plant Status Summary")
        st.write(f"**Plant Mood**: {mood_text}")
        if moisture_val <= 400:
            st.warning("Your plant needs water!")
        elif moisture_val <= 700:
            st.info("Your plant is doing okay!")
        else:
            st.error("Your plant might be overwatered! Check soil.") # Changed to error for drowning

    else:
        st.error("No data available from the database.")

else:
    st.info("Click the button to fetch the latest plant stats.")
