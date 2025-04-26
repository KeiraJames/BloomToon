import requests
import json

API_KEY = "2b10X3YLMd8PNAuKOCVPt7MeUe"
PLANTNET_URL = "https://my-api.plantnet.org/v2/identify/all"

def identify_plant(image_bytes):
    files = {'images': ('image.jpg', image_bytes)}
    params = {'api-key': API_KEY}
    response = requests.post(PLANTNET_URL, files=files, params=params)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            return data["results"][0]["species"]["scientificNameWithoutAuthor"]
        else:
            return None
    else:
        return None

def get_care_info(plant_name, care_data):
    for plant in care_data:
        if plant["Plant Name"].lower() == plant_name.lower():
            return plant
    return None