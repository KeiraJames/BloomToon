import streamlit as st
from streamlit_autorefresh import st_autorefresh
from PIL import Image
import os
css = """
 <style>
    p2 {color: black;
    font-size: 45px;
    font-weight: bold;}
    h2 {color: black;}
    p {color: green;
    italic: true;}
"""
st.markdown(css, unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .stApp {
    background: linear-gradient(135deg, #e0f7e9 25%, #a5d6a7 25%, #a5d6a7 50%, #e0f7e9 50%, #e0f7e9 75%, #a5d6a7 75%, #a5d6a7 100% );
    background-size: 200% 200%;
    animation: wave 10s ease infinite;
    height: 100vh;
    }
    @keyframes wave{
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Home 🏠 <Logo>")
# st.sidebar.image("bloomBotLogo.png", width=200)

st.write('<p2> Welcome to Bloom Bot HQ </p2>', unsafe_allow_html=True)
st.markdown('<p> Take a picture of your plant, pass it into our AI and get a personalised raising plan for your plant. </p>', unsafe_allow_html=True)
st.markdown('<p> Navigate through the sidebar to explore the app! </p>', unsafe_allow_html=True)

count = st_autorefresh(interval=3000, key="auto-refresh")

image_folder = "/Users/stephenoke/Downloads/plants"
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))])
image_paths = [os.path.join(image_folder, file) for file in image_files]

# Cycle through images
index = count % len(image_paths)

st.image(Image.open(image_paths[index]), use_container_width=True)

if st.button("Use The AI"):
    st.markdown("[Use our AI](./3_chatbot)", unsafe_allow_html=True)
else:
    st.write("Check it out!")