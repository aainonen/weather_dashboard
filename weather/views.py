import re
import logging
from flask import Blueprint, render_template, request, current_app
from .api import fetch_weather
from .extensions import limiter  # Import limiter from extensions.py

main_blueprint = Blueprint('main', __name__, template_folder='../templates')

def is_valid_city(city):
    """Validate the city name to allow letters (including Finnish characters), spaces, and hyphens."""
    return bool(re.match(r"^[a-zA-ZäöåÄÖÅ\s\-]+$", city))

@main_blueprint.route('/')
@limiter.limit("10 per minute")  # Limit to 10 requests per minute
@limiter.limit("100 per hour")  # Limit to 100 requests per hour
def index():
    # Get the city from the query parameters, default to the configured default city
    city = request.args.get('city', '').strip() or current_app.config.get('DEFAULT_CITY', 'Helsinki')

    # Validate the city name length
    if len(city) > 50:
        logging.warning(f"City name too long: {city}")
        return render_template('index.html', weather={"status": "error", "message": "The city name you entered is too long. Please enter a shorter name."})

    # Validate the city name format
    if not is_valid_city(city):
        logging.warning(f"Invalid city name: {city}")
        return render_template('index.html', weather={"status": "error", "message": "The city name you entered contains invalid characters. Please try again."})

    # Fetch weather data for the specified city
    weather_response = fetch_weather(city)

    # Handle API errors
    if weather_response["status"] == "error":
        logging.error(f"Error fetching weather for city '{city}': {weather_response['message']}")
        return render_template('index.html', weather=weather_response)

    # Render the weather data
    return render_template('index.html', weather=weather_response, city=city)
