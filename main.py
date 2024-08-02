from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import weather_requests  # Import the weather_requests module
from locations import hungarian_cities  # Import the cities data from locations.py

class MyApp(App):
    title = 'SimpleWeather'  # Set the window title here

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create TextInput for country
        self.country_input = TextInput(hint_text='Enter Country', size_hint=(1, 0.1))
        self.country_input.bind(text=self.on_country_text)

        # Create TextInput for city
        self.city_input = TextInput(hint_text='Enter City', size_hint=(1, 0.1))
        self.city_input.bind(text=self.on_city_text)

        self.city_dropdown = DropDown()
        self.city_button = Button(text='Select City', size_hint=(1, 0.1))
        self.city_button.bind(on_release=self.city_dropdown.open)

        self.weather_label = Label(text="Weather info will be shown here", size_hint=(1, 0.8))

        self.layout.add_widget(self.country_input)
        self.layout.add_widget(self.city_input)
        self.layout.add_widget(self.city_button)
        self.layout.add_widget(self.weather_label)

        return self.layout

    def on_country_text(self, instance, value):
        # We only support Hungary for now
        value = value.lower().strip()
        if value != 'hungary':
            self.weather_label.text = "Currently, we only support Hungary."
            self.city_dropdown.dismiss()
        else:
            self.weather_label.text = ""

    def on_city_text(self, instance, value):
        value = value.lower().strip()
        self.city_dropdown.dismiss()
        self.city_dropdown.clear_widgets()

        for city in hungarian_cities.keys():
            if value in city:
                btn = Button(text=city.capitalize(), size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.update_weather('Hungary', btn.text))
                self.city_dropdown.add_widget(btn)
        
        Clock.schedule_once(self.open_city_dropdown, 0.1)

    def open_city_dropdown(self, dt):
        self.city_dropdown.open(self.city_input)

    def update_weather(self, country, city):
        city = city.lower()
        self.city_input.text = city.capitalize()
        self.city_dropdown.dismiss()

        latitude, longitude = hungarian_cities[city]

        # Get the weather data
        weather_info = weather_requests.get_weather(latitude, longitude)

        # Update the label with the weather information
        self.weather_label.text = weather_info

if __name__ == "__main__":
    MyApp().run()
