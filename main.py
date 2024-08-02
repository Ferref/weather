from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import weather_requests  # Import the weather_requests module
from locations import hungarian_cities  # Import the cities data from locations.py

def replace_accented_characters(text):
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ö': 'o', 'ő': 'o', 'ú': 'u', 'ü': 'u', 'ű': 'u'
    }
    for accented_char, replacement_char in replacements.items():
        text = text.replace(accented_char, replacement_char)
    return text

class MyApp(App):
    title = 'SimpleWeather'  # Set the window title here

    def build(self):
        self.root = FloatLayout()

        with self.root.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(source='background.jpg', size=Window.size)
            self.root.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint=(0.8, 0.8))
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Create Button for country
        self.country_button = Button(text='Choose Country', size_hint=(1, 0.1), font_name='white.otf', font_size='40sp')
        self.country_button.bind(on_release=self.show_countries)

        # Create Button for city
        self.city_button = Button(text='Choose City', size_hint=(1, 0.1), font_name='white.otf', font_size='40sp')
        self.city_button.bind(on_release=self.show_cities)
        self.city_button.disabled = True  # Initially disabled until country is chosen

        self.weather_label = Label(text="Weather info will be shown here", size_hint=(1, 0.8), font_name='white.otf', font_size='40sp', color=(0, 0, 0, 1))

        self.layout.add_widget(self.country_button)
        self.layout.add_widget(self.city_button)
        self.layout.add_widget(self.weather_label)

        self.root.add_widget(self.layout)

        return self.root

    def _update_rect(self, instance, value):
        self.bg.size = instance.size
        self.bg.pos = instance.pos

    def show_countries(self, instance):
        self.country_dropdown = DropDown()
        btn = Button(text='Hungary', size_hint_y=None, height=dp(44), font_name='white.otf', font_size='30sp')
        btn.bind(on_release=lambda btn: self.select_country(btn.text))
        self.country_dropdown.add_widget(btn)
        self.country_dropdown.open(self.country_button)

    def select_country(self, country):
        self.country_button.text = country
        self.country_dropdown.dismiss()
        self.city_button.disabled = False
        self.weather_label.text = ""

    def show_cities(self, instance):
        self.city_dropdown = DropDown()
        for city in hungarian_cities.keys():
            display_city = replace_accented_characters(city)  # Use English alphabet for display
            btn = Button(text=display_city.capitalize(), size_hint_y=None, height=dp(44), font_name='white.otf', font_size='30sp')
            btn.bind(on_release=lambda btn: self.select_city(btn.text))
            self.city_dropdown.add_widget(btn)
        self.city_dropdown.open(self.city_button)

    def select_city(self, city):
        city_key = replace_accented_characters(city.lower())  # Ensure lookup key is correct
        original_city = [orig_city for orig_city in hungarian_cities.keys() if replace_accented_characters(orig_city) == city_key]
        
        if original_city:
            latitude, longitude = hungarian_cities[original_city[0]]
            self.city_button.text = city.capitalize()
            self.city_dropdown.dismiss()

            # Get the weather data
            weather_info = weather_requests.get_weather(latitude, longitude)

            # Update the label with the weather information
            self.weather_label.text = weather_info
        else:
            self.weather_label.text = "City not found."

if __name__ == "__main__":
    MyApp().run()
