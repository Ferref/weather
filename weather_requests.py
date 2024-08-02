import requests
from datetime import datetime

def get_weather():
    # Open-Meteo API endpoint and parameters for Budapest
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': 47.4979,  # Latitude for Budapest
        'longitude': 19.0402, # Longitude for Budapest
        'current_weather': True
    }
    
    # Make the request to the Open-Meteo API
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'current_weather' in data:
        weather = data['current_weather']
        temperature = weather['temperature']
        windspeed = weather['windspeed']
        weather_time = datetime.fromisoformat(weather['time'])

        # Print the weather information
        print(f"Current weather in Budapest as of {weather_time}:")
        print(f"Temperature: {temperature}°C")
        print(f"Windspeed: {windspeed} km/h")
    else:
        print("Failed to get weather data for Budapest.")

if __name__ == "__main__":
    get_weather()
