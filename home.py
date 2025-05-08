import streamlit as st
from streamlit_autorefresh import st_autorefresh
from PIL import Image
import os

# Sidebar logo
st.sidebar.image("bloomBotLogo.jpg", width=200)

# Background and font styling
st.markdown("""
<style>
    .stApp {
        background-color: #556B2F;
        color: white;
    }
    h1 {
        font-size: 48px;
        font-weight: bold;
        color: #F0FFF0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<h1>Welcome to Bloom Bot HQ</h1>", unsafe_allow_html=True)

# Image carousel setup
image_folder = "/Users/stephenoke/Downloads/plants"
image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))])
image_paths = [os.path.join(image_folder, file) for file in image_files]

if image_paths:
    count = st_autorefresh(interval=3000, key="auto-refresh")
    index = count % len(image_paths)
    st.image(Image.open(image_paths[index]), use_container_width=True)
else:
    st.warning("No images found in the folder.")
