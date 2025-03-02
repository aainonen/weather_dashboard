# Weather Dashboard

A simple Flask web application that displays current weather data using the OpenWeatherMap API, now fully containerized with Docker.

## Overview

The Weather Dashboard is a lightweight web application built with Flask. It fetches weather data for a default location (Helsinki) from the OpenWeatherMap API and displays it in a clean, responsive interface. This project demonstrates basic web development concepts including API integration, template rendering, unit testing with pytest, and containerization with Docker.


## Features

- **Current Weather Display:**
  View temperature, feels-like, weather conditions, humidity, and wind speed.
- **Flask Integration:**
  Uses Flask's blueprint system for a modular code structure.
- **Configurable API Key:**
  Securely manage your OpenWeatherMap API key using environment variables.
- **Testing:**
  Unit tests using [pytest](https://pytest.org/) ensure code reliability.
- **Dockerization:**
  Containerized using Docker for consistent environments and simplified deployment.

## Installation

### For Local Development

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/aainonen/weather_dashboard.git
   cd weather_dashboard

2. **Create and Activate a Virtual Environment:**
   ``
   python3 -m venv venv
   source venv/bin/activate
   ``
   
3. **Install Dependencies:**
   ``
   pip install -r requirements.txt
   ``

## Configuration
Before running the app, set your OpenWeatherMap API key.

- **Option 1: Environment Variable:**
   ``
   export OPENWEATHER_API_KEY=your_actual_api_key_here
   ``

- **Option 2: Using a .env File:**
Create a .env file in the project root with:
   ``
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ``
(Make sure your .env file is listed in .gitignore to keep it private.)

A sample file named .env.example is provided to show the required variables.


## Running the Application
### Locally (Without Docker)
To start the Flask web app locally, run:
   ``
   python app.py
   ``
   
By default, the app will be available at http://127.0.0.1:5000.

### Using Docker Compose
The project is fully containerized. To build and run the app in Docker:

1. Ensure Docker and Docker Compose are installed.
2. Run:
   ``
   docker compose up --build
   ``

Docker Compose will automatically load environment variables from your .env file.
The app will be accessible at http://localhost:8000.

## Testing
This project uses [pytest](https://pytest.org/) for testing. To run tests locally:
1. Activate your virtual environment.
2. Set `PYTHONPATH` to the project root: `export PYTHONPATH=.`
3. Run `pytest` in the project root.

For detailed testing instructions, see [TESTING.md](TESTING.md).
