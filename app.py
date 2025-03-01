import requests

def fetch_weather():
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': 'Helsinki',
        'appid': '1d949f320bdd304935f3d987ea0635a8',
        'units': 'metric'
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
        weather_data = response.json()
        print("Weather data for Helsinki:")
        print(weather_data)
    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)

if __name__ == '__main__':
    fetch_weather()
