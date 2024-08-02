from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Rectangle
import weather_requests  # Import the weather_requests module
from locations import hungarian_cities  # Import the cities data from locations.py

class MyApp(App):
    title = 'SimpleWeather'  # Set the window title here

    def build(self):
        self.root = FloatLayout()

        with self.root.canvas.before:
            self.bg = Image(source='background.jpg', allow_stretch=True, keep_ratio=False)
            self.bg.size = Window.size
            self.bg.pos = self.root.pos
            self.root.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint=(0.8, 0.8))
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Create Button for country
        self.country_button = Button(text='Choose Country', size_hint=(1, 0.1), font_name='cool_font.ttf', font_size='20sp')
        self.country_button.bind(on_release=self.show_countries)

        # Create Button for city
        self.city_button = Button(text='Choose City', size_hint=(1, 0.1), font_name='cool_font.ttf', font_size='20sp')
        self.city_button.bind(on_release=self.show_cities)
        self.city_button.disabled = True  # Initially disabled until country is chosen

        self.weather_label = Label(text="Weather info will be shown here", size_hint=(1, 0.8), font_name='cool_font.ttf', font_size='20sp')

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
        btn = Button(text='Hungary', size_hint_y=None, height=dp(44), font_name='cool_font.ttf', font_size='18sp')
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
            btn = Button(text=city.capitalize(), size_hint_y=None, height=dp(44), font_name='cool_font.ttf', font_size='18sp')
            btn.bind(on_release=lambda btn: self.select_city(btn.text))
            self.city_dropdown.add_widget(btn)
        self.city_dropdown.open(self.city_button)

    def select_city(self, city):
        self.city_button.text = city
        self.city_dropdown.dismiss()

        latitude, longitude = hungarian_cities[city.lower()]

        # Get the weather data
        weather_info = weather_requests.get_weather(latitude, longitude)

        # Update the label with the weather information
        self.weather_label.text = weather_info

if __name__ == "__main__":
    MyApp().run()
