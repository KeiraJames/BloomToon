import requests

GEMINI_API_KEY = 'AIzaSyCD3HRndQD3ir_nhNMIZ-ss0EkAEK3DC0U'  
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def send_message(messages):
    payload = {
        "contents": messages
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    else:
        print("Error:", response.status_code, response.text)
        return "Something went wrong."

def chat_with_plant(care_info, user_input):
    personality = {
        "title": care_info["Personality"]["Title"],
        "traits": ", ".join(care_info["Personality"]["Traits"]),
        "prompt": care_info["Personality"]["Prompt"]
    }

    messages = [
        {
            "role": "user",
            "parts": [{
                "text": f"You are a plant with a personality called {personality['title']}. "
                        f"Your traits include {personality['traits']}. {personality['prompt']}"
            }]
        },
        {
            "role": "user",
            "parts": [{"text": user_input}]
        }
    ]

    return send_message(messages)

