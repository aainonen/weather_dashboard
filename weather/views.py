# weather/views.py

import re
import logging
from flask import Blueprint, render_template, request, current_app, g
from .api import fetch_weather
from .extensions import limiter

main_blueprint = Blueprint('main', __name__, template_folder='../templates')


def is_valid_city(city):
    """Validate the city name to allow letters (including Finnish characters), spaces, and hyphens."""
    return bool(re.match(r'^[a-zA-ZäöåÄÖÅ\s\-]+$', city))


@main_blueprint.route('/')
@limiter.limit('10 per minute')
@limiter.limit('100 per hour')
def index():
    city = (
        request.args.get('city', '').strip() or
        current_app.config.get('DEFAULT_CITY', 'Helsinki')
    )
    g.search_location = city

    if len(city) > 50:
        logging.warning(f'City name too long: {city}')
        return render_template(
            'index.html',
            weather={
                'status': 'error',
                'message': (
                    'The city name you entered is too long. '
                    'Please enter a shorter name.'
                )
            }
        )

    if not is_valid_city(city):
        logging.warning(f'Invalid city name: {city}')
        return render_template(
            'index.html',
            weather={
                'status': 'error',
                'message': (
                    'The city name you entered contains invalid characters. '
                    'Please try again.'
                )
            }
        )

    weather_response = fetch_weather(city)
    if weather_response['status'] == 'error':
        logging.error(
            f"Error fetching weather for city '{city}': "
            f"{weather_response['message']}"
        )
        return render_template(
            'index.html',
            weather=weather_response
        )

    return render_template(
        'index.html',
        weather=weather_response,
        city=city
    )
