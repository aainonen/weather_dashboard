# weather/api.py

import requests
from flask import current_app

def fetch_weather():
    api_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': 'Helsinki',
        'appid': current_app.config.get('OPENWEATHER_API_KEY'),
        'units': 'metric'
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Here, you could also add logging
        return {"error": str(e)}
