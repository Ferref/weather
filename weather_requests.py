import requests
from datetime import datetime

def get_weather(latitude, longitude):
    # Open-Meteo API endpoint and parameters
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': True,
        'daily': 'temperature_2m_max,temperature_2m_min',
        'timezone': 'auto'
    }

    # Make the request to the Open-Meteo API
    response = requests.get(url, params=params)
    data = response.json()

    if 'current_weather' in data and 'daily' in data:
        weather = data['current_weather']
        temperature = weather['temperature']
        windspeed = weather['windspeed']
        weather_time = datetime.fromisoformat(weather['time'])

        # Extract forecast data
        forecast_days = data['daily']['time']
        forecast_max_temps = data['daily']['temperature_2m_max']
        forecast_min_temps = data['daily']['temperature_2m_min']

        forecast = "5-day Forecast:\n"
        for i in range(len(forecast_days)):
            day = datetime.fromisoformat(forecast_days[i]).strftime('%Y-%m-%d')
            max_temp = forecast_max_temps[i]
            min_temp = forecast_min_temps[i]
            forecast += f"{day}: Max Temp: {max_temp} C, Min Temp: {min_temp} C\n"

        # Return the weather information as a string
        return (f"Current weather as of {weather_time}:\n"
                f"Temperature: {temperature} C\n"
                f"Windspeed: {windspeed} km/h\n\n"
                f"{forecast}")
    else:
        return "Failed to get weather data."

# For testing purposes
if __name__ == "__main__":
    latitude = float(input("Enter the latitude: "))
    longitude = float(input("Enter the longitude: "))
    print(get_weather(latitude, longitude))
