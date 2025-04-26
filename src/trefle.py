import requests

TREFLE_TOKEN = "knNepnDdvUifCxUKAIbK1PmU0QmWyjk8bFOQMqzBgAI"
TREFLE_URL = "https://trefle.io/api/v1/plants/search"

def get_trefle_plant_info(plant_name):
    params = {
        "token": TREFLE_TOKEN,
        "q": plant_name
    }
    response = requests.get(TREFLE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            return data["data"][0]  # return first matching plant
        else:
            return None
    else:
        return None