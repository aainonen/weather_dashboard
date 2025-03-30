import requests
from flask import current_app
import logging

def fetch_weather(city='Helsinki'):
    """
    Fetch weather data for a given city using the OpenWeatherMap API.

    Args:
        city (str): The name of the city to fetch weather for. Defaults to 'Helsinki'.

    Returns:
        dict: JSON response containing weather data or an error message.
    """
    api_url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = current_app.config.get('OPENWEATHER_API_KEY')

    if not api_key:
        logging.error("OpenWeather API key is missing in the configuration.")
        return {"status": "error", "message": "API key is missing"}

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        logging.error("Failed to fetch weather data for %s: %s", city, e)
        return {"status": "error", "message": str(e)}
