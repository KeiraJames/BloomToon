import streamlit as st
import base64
import json
import requests
from io import BytesIO
# ===== Streamlit Setup =====
st.set_page_config(page_title="Plant Buddy", layout="wide")

#===== CSS for Styling =====
css = """
<style>
    h2 {color: black;}
    p {color: green; font-style: italic;}
</style>
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
# ===== API Setup =====
TREFLE_TOKEN=  "knNepnDdvUifCxUKAIbK1PmU0QmWyjk8bFOQMqzBgAI"
PLANTNET_API_KEY = "2b10kkj7DqqszQJvssiBpCxgzu"
PLANTNET_URL = "https://my-api.plantnet.org/v2/identify/all"
TREFLE_SEARCH_URL = "https://trefle.io/api/v1/plants/search"
TREFLE_DETAIL_URL = "https://trefle.io/api/v1/plants"

def identify_plant(image_bytes):
    files = {'images': ('image.jpg', image_bytes)}
    params = {'api-key': PLANTNET_API_KEY}
    response = requests.post(PLANTNET_URL, files=files, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["species"]["scientificNameWithoutAuthor"]
    return None

def get_trefle_plant_info(scientific_name):
    params = {"token": TREFLE_TOKEN, "q": scientific_name}
    response = requests.get(TREFLE_SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            return data["data"][0]
    return None

def get_trefle_details_by_id(plant_id):
    url = f"{TREFLE_DETAIL_URL}/{plant_id}"
    response = requests.get(url, params={"token": TREFLE_TOKEN})
    if response.status_code == 200:
        return response.json()["data"]
    return None

def get_care_info(plant_name, care_data):
    for plant in care_data:
        if plant["Plant Name"].lower() == plant_name.lower():
            return plant
    return None

# ===== Load Plant Care JSON =====
with open("plants_with_personality-3.json", "r") as f:
    care_data = json.load(f)



# ===== Session State Setup =====
if "saved_photos" not in st.session_state:
    st.session_state.saved_photos = {}
if "temp_photo" not in st.session_state:
    st.session_state.temp_photo = None
if "saving_mode" not in st.session_state:
    st.session_state.saving_mode = False
if "temp_plant_name" not in st.session_state:
    st.session_state.temp_plant_name = ""
if "temp_care_info" not in st.session_state:
    st.session_state.temp_care_info = None
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# ===== Sidebar Navigation =====
tab = st.sidebar.radio("📚 Navigation", ["📥 Upload & Identify", "🪴 View Saved Plants"])

# ===== Upload & Identify Tab =====
if tab == "📥 Upload & Identify":
    st.title("📥 Upload a Plant Photo")

    if st.session_state.temp_photo is None:
        uploaded_file = st.file_uploader("Upload a plant photo", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            st.session_state.temp_photo = uploaded_file
            st.session_state.chat_log = []
            st.rerun()

    elif st.session_state.temp_photo and not st.session_state.saving_mode:
        image_bytes = st.session_state.temp_photo.getvalue()
        st.image(image_bytes, caption="Uploaded Plant", use_container_width=True)

        with st.spinner("🔍 Identifying plant..."):
            plant_name = identify_plant(image_bytes)

        if plant_name:
            st.session_state.temp_plant_name = plant_name
            st.subheader(f"🌱 Identified Plant: *{plant_name}*")

            with st.spinner("📡 Fetching care info from Trefle..."):
                trefle_match = get_trefle_plant_info(plant_name)

                if trefle_match:
                    trefle_detail = get_trefle_details_by_id(trefle_match["id"])
                    st.session_state.temp_care_info = trefle_detail

                    st.markdown(f"**Scientific Name:** {trefle_detail.get('scientific_name', 'N/A')}")
                    st.markdown(f"**Common Name:** {trefle_detail.get('common_name', 'N/A')}")
                    st.markdown(f"**Family:** {trefle_detail.get('family_common_name', 'N/A')}")
                    st.markdown(f"**Growth Habit:** {trefle_detail.get('main_species', {}).get('growth', {}).get('habit', 'N/A')}")
                    st.markdown(f"**Water Needs:** {trefle_detail.get('main_species', {}).get('growth', {}).get('precipitation_minimum', {}).get('cm', 'N/A')} cm min")
                    st.markdown(f"**Lifespan:** {trefle_detail.get('main_species', {}).get('specifications', {}).get('lifespan', 'N/A')}")

                    trefle_image = trefle_detail.get('image_url') or trefle_detail.get('main_species', {}).get('images', [{}])[0].get('image_url')
                    if trefle_image:
                        st.image(trefle_image, caption="Trefle Image", use_container_width=True)

                    # Chat prompt
                    st.divider()
                    st.subheader("🧠 Chat with your plant:")
                    prompt = st.text_input("Say something to your plant:")
                    if prompt:
                        response = f"{plant_name} says: 🌿 I hear you! You said: '{prompt}'"
                        st.session_state.chat_log.append(("You", prompt))
                        st.session_state.chat_log.append((plant_name, response))

                    for speaker, msg in st.session_state.chat_log:
                        st.markdown(f"**{speaker}:** {msg}")

                    # Save / Discard Buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 Save"):
                            st.session_state.saving_mode = True
                            st.rerun()
                    with col2:
                        if st.button("🗑️ Discard"):
                            st.session_state.temp_photo = None
                            st.session_state.temp_plant_name = ""
                            st.session_state.temp_care_info = None
                            st.session_state.chat_log = []
                            st.success("Photo discarded. Upload another plant.")
                            st.rerun()

                else:
                    st.error("❌ Could not find matching data on Trefle.io")
                    st.session_state.temp_photo = None
        else:
            st.error("💔 Could not identify the plant. Try another photo.")
            st.session_state.temp_photo = None

    elif st.session_state.saving_mode:
        st.image(st.session_state.temp_photo, caption="Confirm Save", use_container_width=True)
        name_input = st.text_input("Enter a name to save this plant")

        if name_input and st.button("✅ Confirm Save"):
            encoded = base64.b64encode(st.session_state.temp_photo.getvalue()).decode()
            mime_type = st.session_state.temp_photo.type
            data_url = f"data:{mime_type};base64,{encoded}"

            st.session_state.saved_photos[name_input] = {
                "image": data_url,
                "plant_name": st.session_state.temp_plant_name,
                "care_info": st.session_state.temp_care_info,
                "chat_log": st.session_state.chat_log
            }

            # Reset temp state
            st.session_state.temp_photo = None
            st.session_state.temp_plant_name = ""
            st.session_state.temp_care_info = None
            st.session_state.chat_log = []
            st.session_state.saving_mode = False

            st.success(f"🌟 Saved as '{name_input}'!")
            st.rerun()

# ===== View Saved Plants Tab =====
elif tab == "🪴 View Saved Plants":
    st.title("🪴 Your Saved Plants")

    options = list(st.session_state.saved_photos.keys())
    selected = st.sidebar.selectbox("Choose a saved plant:", [""] + options)

    if selected:
        entry = st.session_state.saved_photos[selected]
        st.subheader(f"📸 {selected}")
        st.image(entry["image"], use_container_width=True)

        if "plant_name" in entry:
            st.markdown(f"**Plant Identified:** {entry['plant_name']}")
        if "care_info" in entry and entry["care_info"]:
            care = entry["care_info"]
            st.markdown(f"**Light:** {care['Light Requirements']}")
            st.markdown(f"**Watering:** {care['Watering']}")
            st.markdown(f"**Humidity:** {care['Humidity Preferences']}")
            st.markdown(f"**Temperature:** {care['Temperature Range']}")
            st.markdown(f"**Feeding:** {care['Feeding Schedule']}")
            st.markdown(f"**Toxicity:** {care['Toxicity']}")
            st.markdown(f"**Additional Care:** {care['Additional Care']}")
            st.markdown(f"**Personality:** *{care['Personality']['Title']}* - {', '.join(care['Personality']['Traits'])}")
            st.markdown(f"*{care['Personality']['Prompt']}*")

        if "chat_log" in entry:
            st.subheader("🧠 Chat History")
            for speaker, msg in entry["chat_log"]:
                st.markdown(f"**{speaker}:** {msg}")
