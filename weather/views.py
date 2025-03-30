from flask import Blueprint, render_template
from .api import fetch_weather

main_blueprint = Blueprint('main', __name__, template_folder='../templates')

@main_blueprint.route('/')
def index():
    # Fetch weather data (default city is Helsinki)
    weather_response = fetch_weather()

    # Pass the entire response (status, data, or message) to the template
    return render_template('index.html', weather=weather_response)
