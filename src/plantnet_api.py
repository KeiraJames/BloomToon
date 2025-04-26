import requests

import requests

class PlantNetAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.PLANTNET_URL = "https://my-api.plantnet.org/v2/identify/all"

    def identify_plant(self, image_path, organ='leaf'):
        try:
            with open(image_path, 'rb') as f:
                files = [('images', (image_path, f, 'image/jpeg'))]
                data = {'organs': organ}
                params = {'api-key': self.api_key}

                response = requests.post(self.PLANTNET_URL, files=files, data=data, params=params)
        except FileNotFoundError:
            return "Image file not found."

        if response.status_code == 200:
            data = response.json()
            if "results" in data and data["results"]:
                plant_name = data["results"][0]["species"]["scientificNameWithoutAuthor"]
                score = data["results"][0]["score"]
                return f"Identified plant: {plant_name} (score: {score:.2f})"
            else:
                return "No plant match found."
        else:
            return f"Error: {response.status_code} - {response.text}"
