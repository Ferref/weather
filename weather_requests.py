import requests
from datetime import datetime

def get_weather(latitude, longitude):
    # Open-Meteo API endpoint and parameters
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
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

        # Return the weather information as a string
        return (f"Current weather as of {weather_time}:\n"
                f"Temperature: {temperature} C\n"
                f"Windspeed: {windspeed} km/h")
    else:
        return "Failed to get weather data."

# For testing purposes
if __name__ == "__main__":
    latitude = float(input("Enter the latitude: "))
    longitude = float(input("Enter the longitude: "))
    print(get_weather(latitude, longitude))
