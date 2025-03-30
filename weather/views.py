import re
from flask import Blueprint, render_template, request
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
    city = request.args.get('city', 'Helsinki')

    # Validate the city name length
    if len(city) > 50:
        return render_template('index.html', weather={"status": "error", "message": "City name is too long."})

    # Validate the city name format
    if not is_valid_city(city):
        return render_template('index.html', weather={"status": "error", "message": "Invalid city name."})

    # Fetch weather data for the specified city
    weather_response = fetch_weather(city)

    return render_template('index.html', weather=weather_response, city=city)
