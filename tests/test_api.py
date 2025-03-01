import json
import requests
import pytest
from weather import create_app
from weather.api import fetch_weather

def dummy_weather_data():
    """Dummy data to simulate a successful API call."""
    return {
        "name": "Helsinki",
        "main": {
            "temp": 10,
            "feels_like": 8,
            "humidity": 75
        },
        "weather": [
            {"description": "clear sky", "icon": "01d"}
        ],
        "wind": {"speed": 5}
    }

class DummyResponse:
    def __init__(self, json_data, status_code):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(f"{self.status_code} error")

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(monkeypatch, client):
    """
    Test the index route of the Flask app.
    Monkeypatch fetch_weather in the views module to return dummy weather data.
    """
    monkeypatch.setattr("weather.views.fetch_weather", lambda: dummy_weather_data())

    response = client.get('/')
    assert response.status_code == 200

    html = response.data.decode('utf-8')
    # Check that the template rendered the expected content.
    assert "Weather in Helsinki" in html
    assert "10 °C" in html  # This should now pass if the dummy data is used.

def dummy_get_success(url, params):
    """
    Dummy replacement for requests.get to simulate a successful API response.
    """
    return DummyResponse({
        "name": "Helsinki",
        "main": {"temp": 12, "feels_like": 11, "humidity": 80},
        "weather": [{"description": "cloudy", "icon": "02d"}],
        "wind": {"speed": 4}
    }, 200)

def test_fetch_weather_success(monkeypatch, app):
    """
    Test the fetch_weather function for a successful API call.
    Use monkeypatch to override requests.get with dummy_get_success.
    """
    monkeypatch.setattr(requests, "get", dummy_get_success)
    with app.app_context():
        data = fetch_weather()
        assert "name" in data
        assert data["name"] == "Helsinki"
        assert "main" in data
        assert data["main"]["temp"] == 12

def dummy_get_failure(url, params):
    """
    Dummy replacement for requests.get to simulate an API failure.
    """
    raise requests.exceptions.RequestException("API failure simulated")

def test_fetch_weather_failure(monkeypatch, app):
    """
    Test the fetch_weather function handling a failure scenario.
    """
    monkeypatch.setattr(requests, "get", dummy_get_failure)
    with app.app_context():
        data = fetch_weather()
        assert "error" in data
        assert "API failure simulated" in data["error"]

