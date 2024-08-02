from kivy.app import App
from kivy.uix.label import Label
import weather_requests  # Import the weather_requests module

class MyApp(App):
    title = 'SimpleWeather'  # Set the window title here

    def build(self):
        latitude = 47.4979  # Replace with user input or predefined values
        longitude = 19.0402  # Replace with user input or predefined values

        # Get the weather data
        weather_info = weather_requests.get_weather(latitude, longitude)

        # Return a Label widget with the weather information
        return Label(text=weather_info)

if __name__ == "__main__":
    MyApp().run()
