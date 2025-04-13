import requests
import logging
from flask import current_app
from datetime import datetime, timedelta
import pytz

def fetch_weather(city='Helsinki'):
    """
    Fetch current weather and forecast data for a given city using the OpenWeatherMap API.
    """
    api_key = current_app.config.get('OPENWEATHER_API_KEY')
    if not api_key:
        logging.error("OpenWeather API key is missing in the configuration.")
        return {"status": "error", "message": "API key is missing"}

    # URLs for current weather and forecast
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    try:
        # --- 1) Current weather ---
        current_response = requests.get(current_weather_url, params={
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }, timeout=10)
        current_response.raise_for_status()
        current_weather = current_response.json()

        # Ensure the response contains the required keys
        if not all(key in current_weather for key in ["name", "main", "weather", "wind"]):
            logging.error("Invalid current weather data received from API.")
            return {"status": "error", "message": "Invalid current weather data received from API."}

        # --- 2) 5-day forecast (3-hour increments) ---
        forecast_response = requests.get(forecast_url, params={
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Ensure the response contains the required keys
        if "list" not in forecast_data:
            logging.error("Invalid forecast data received from API.")
            return {"status": "error", "message": "Invalid forecast data received from API."}

        # --- 3) Time zone: Europe/Helsinki ---
        helsinki_tz = pytz.timezone("Europe/Helsinki")
        now_in_hel = datetime.now(helsinki_tz)
        today = now_in_hel.date()
        tomorrow = today + timedelta(days=1)

        # Helper function to convert UTC timestamp to Helsinki local time
        def to_helsinki_local(dt_string):
            utc_dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
            return utc_dt.replace(tzinfo=pytz.utc).astimezone(helsinki_tz)

        # --- 4) Today's Weather ---
        today_summary = [{"data": current_weather, "time": now_in_hel.strftime("%H:%M")}]

        # Add the next 4 time-points (3-hour intervals)
        forecast_for_today = [
            entry for entry in forecast_data['list']
            if datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S").date() == today
        ]
        for entry in forecast_for_today:
            forecast_time = to_helsinki_local(entry['dt_txt'])
            if forecast_time > now_in_hel and len(today_summary) < 5:
                today_summary.append({
                    "data": entry,
                    "time": forecast_time.strftime("%H:%M")
                })

        # --- 5) Tomorrow's Weather ---
        tomorrow_summary = {"upper_row": [], "lower_row": []}

        # Desired hours for tomorrow's weather
        upper_row_hours = [6, 9, 12, 15]  # Early morning, morning, noon, afternoon
        lower_row_hours = [18, 21, 0]     # Early evening, evening, night

        forecast_for_tomorrow = [
            entry for entry in forecast_data['list']
            if datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S").date() == tomorrow
        ]
        for entry in forecast_for_tomorrow:
            forecast_time = to_helsinki_local(entry['dt_txt'])
            hour = forecast_time.hour
            if hour in upper_row_hours:
                tomorrow_summary["upper_row"].append({
                    "data": entry,
                    "time": forecast_time.strftime("%H:%M")
                })
            elif hour in lower_row_hours:
                tomorrow_summary["lower_row"].append({
                    "data": entry,
                    "time": forecast_time.strftime("%H:%M")
                })

        # --- 6) Return everything to the template ---
        return {
            "status": "success",
            "current": current_weather,
            "today_date_str": now_in_hel.strftime("%a %d.%m.%Y"),
            "tomorrow_date_str": (now_in_hel + timedelta(days=1)).strftime("%a %d.%m.%Y"),
            "today": today_summary,
            "tomorrow": tomorrow_summary
        }

    except requests.exceptions.HTTPError as http_err:
        if current_response.status_code == 404:
            return {
                "status": "error",
                "message": f"City '{city}' not found. Please check the city name and try again."
            }
        logging.error("HTTP error occurred: %s", http_err)
        return {
            "status": "error",
            "message": "An error occurred while fetching weather data. Please try again later."
        }
    except requests.exceptions.RequestException as req_err:
        logging.error("Request error occurred: %s", req_err)
        return {
            "status": "error",
            "message": "Failed to fetch weather data. Please check your connection and try again."
        }
