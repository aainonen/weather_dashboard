# weather_dashboard

A simple Flask web application coding project that displays current weather data using the OpenWeatherMap API.

## Overview

The Weather Dashboard is a lightweight web application built with Flask. It fetches weather data for a default location (Helsinki) from the OpenWeatherMap API and displays it in a clean, responsive interface. This project demonstrates basic web development concepts including API integration, template rendering, and testing with pytest.

## Features

- **Current Weather Display:**
  View temperature, feels-like, weather conditions, humidity, and wind speed.
- **Flask Integration:**
  Utilizes Flask's blueprint system for a modular code structure.
- **Configurable API Key:**
  Securely manage your OpenWeatherMap API key using environment variables.
- **Testing:**
  Unit tests using pytest ensure code reliability and facilitate future enhancements.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/aainonen/weather_dashboard.git
   cd weather_dashboard

2. **Create and Activate a Vritual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install dependencies:**
   ``
   pip install -r requirements.txt
   ``

## Configuration
Before running the app, set your OpenWeatherMap API key as an environment variable. You can do this by running:
   ``
   export OPENWEATHER_API_KEY=your_actual_api_key_here
   ``

Alternatively, create a .env file and use a tool like python-dotenv to load your configuration.

## Running the Application
To start the Flask web app locally, run:
   ``
   python app.py
   ``
   
By default, the app will be available at http://127.0.0.1:5000.

## Testing
This project uses [pytest](https://pytest.org/) for testing. To run tests locally:
1. Activate your virtual environment.
2. Set `PYTHONPATH` to the project root: `export PYTHONPATH=.`
3. Run `pytest` in the project root.

For detailed testing instructions, see [TESTING.md](TESTING.md).
