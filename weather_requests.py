import requests
from datetime import datetime

def get_coordinates(country, city, username):
    # GeoNames API endpoint and parameters
    geonames_url = 'http://api.geonames.org/searchJSON'
    params = {
        'q': city,
        'country': country,
        'maxRows': 1,
        'username': username
    }
    
    # Make the request to the GeoNames API
    response = requests.get(geonames_url, params=params)
    data = response.json()
    
    if 'geonames' in data and len(data['geonames']) > 0:
        location = data['geonames'][0]
        return location['lat'], location['lng']
    else:
        print("Failed to get coordinates for the city.")
        return None, None

def get_weather(country, city, username):
    lat, lon = get_coordinates(country, city, username)
    if not lat or not lon:
        return "Unable to fetch coordinates for the specified location."

    # Open-Meteo API endpoint and parameters
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
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
        return (f"Current weather in {city}, {country} as of {weather_time}:\n"
                f"Temperature: {temperature}°C\n"
                f"Windspeed: {windspeed} km/h")
    else:
        return "Failed to get weather data."

# For testing purposes
if __name__ == "__main__":
    country = input("Enter the country code (e.g., HU for Hungary): ")
    city = input("Enter the city name: ")
    username = 'YOUR_GEONAMES_USERNAME'  # Replace with your GeoNames username
    print(get_weather(country, city, username))
