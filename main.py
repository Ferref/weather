from kivy.app import App
from kivy.uix.label import Label
import weather_requests  # Import the weather module

class MyApp(App):
    title = 'SimpleWeather'  # Set the window title here

    def build(self):
        country = 'HU'  # Replace with user input or predefined values
        city = 'Budapest'  # Replace with user input or predefined values
        username = 'YOUR_GEONAMES_USERNAME'  # Replace with your GeoNames username

        # Get the weather data
        weather_info = weather_requests.get_weather(country, city, username)

        # Return a Label widget with the weather information
        return Label(text=weather_info)

if __name__ == "__main__":
    MyApp().run()
