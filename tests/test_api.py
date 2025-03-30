import requests
import pytest
from weather import create_app
from weather.api import fetch_weather

def dummy_weather_data():
    """Dummy data to simulate a successful API call."""
    return {
        "status": "success",
        "data": {
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

def test_index_success(monkeypatch, client):
    """
    Test the index route of the Flask app for a successful response.
    """
    monkeypatch.setattr("weather.views.fetch_weather", lambda city="Helsinki": dummy_weather_data())

    response = client.get('/?city=Helsinki')
    assert response.status_code == 200

    html = response.data.decode('utf-8')
    # Check that the template rendered the expected content.
    assert "Weather in Helsinki" in html
    assert "10 °C" in html

def test_index_error(monkeypatch, client):
    """
    Test the index route of the Flask app for an error response.
    """
    monkeypatch.setattr("weather.views.fetch_weather", lambda city="InvalidCity": {"status": "error", "message": "City not found."})

    response = client.get('/?city=InvalidCity')
    assert response.status_code == 200

    html = response.data.decode('utf-8')
    # Check that the template rendered the error message.
    assert "Error" in html
    assert "City not found." in html

def dummy_get_success(*args, **kwargs):
    """
    Dummy replacement for requests.get to simulate a successful API response.
    """
    return DummyResponse({
        "main": {"temp": 12, "feels_like": 11, "humidity": 80},
        "weather": [{"description": "cloudy", "icon": "02d"}],
        "wind": {"speed": 4},
        "name": "Helsinki"
    }, 200)

def test_fetch_weather_success(monkeypatch, app):
    """
    Test the fetch_weather function for a successful API call.
    """
    monkeypatch.setattr(requests, "get", dummy_get_success)
    with app.app_context():
        data = fetch_weather("Helsinki")
        assert data["status"] == "success"
        assert "data" in data
        assert data["data"]["name"] == "Helsinki"
        assert data["data"]["main"]["temp"] == 12

def dummy_get_failure(*args, **kwargs):
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
        data = fetch_weather("InvalidCity")
        assert data["status"] == "error"
        assert "Failed to fetch weather data. Please check your connection and try again." in data["message"]

def test_fetch_weather_city_not_found(monkeypatch, app):
    """
    Test the fetch_weather function for a 404 city not found error.
    """
    def dummy_get_404(*args, **kwargs):
        return DummyResponse({"message": "city not found"}, 404)

    monkeypatch.setattr(requests, "get", dummy_get_404)
    with app.app_context():
        data = fetch_weather("NonExistentCity")
        assert data["status"] == "error"
        assert "City 'NonExistentCity' not found" in data["message"]
