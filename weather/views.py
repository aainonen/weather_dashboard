from flask import Blueprint, render_template, jsonify
from .api import fetch_weather

main_blueprint = Blueprint('main', __name__, template_folder='../templates')

@main_blueprint.route('/')
def index():
    weather_data = fetch_weather()
    return render_template('index.html', weather=weather_data)

