import requests
from flask import current_app
import logging

def fetch_weather(city='Helsinki'):
    """
    Fetch current weather data for a given city using the OpenWeatherMap API.
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
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # If the response is successful, return the weather data
        return {"status": "success", "data": response.json()}

    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors
        if response.status_code == 404:
            logging.error("City not found: %s", city)
            return {"status": "error", "message": f"City '{city}' not found. Please check the spelling."}
        else:
            logging.error("HTTP error occurred: %s", http_err)
            return {"status": "error", "message": "An error occurred while fetching weather data. Please try again later."}

    except requests.exceptions.RequestException as req_err:
        # Handle other request-related errors
        logging.error("Request error occurred: %s", req_err)
        return {"status": "error", "message": "Failed to fetch weather data. Please check your connection and try again."}
