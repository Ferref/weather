from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
import weather_requests
from locations import hungarian_cities
from datetime import datetime

def replace_accented_characters(text):
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ö': 'o', 'ő': 'o', 'ú': 'u', 'ü': 'u', 'ű': 'u'
    }
    for accented_char, replacement_char in replacements.items():
        text = text.replace(accented_char, replacement_char)
    return text

class MyApp(App):
    title = 'WeatherBunny'
    icon = 'icon_nobg.png'

    def build(self):
        self.root = FloatLayout()

        with self.root.canvas.before:
            self.bg_color = Color(0, 0, 0, 1)  # Set background color to black initially
            self.bg = Rectangle(size=Window.size)
            self.root.bind(size=self._update_rect, pos=self._update_rect)

        self.logo = Image(source='icon_nobg.png', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.root.add_widget(self.logo)
        
        animation = Animation(opacity=0, duration=0.5)  # Speed up the initial animation
        animation.bind(on_complete=self.fade_background)
        animation.start(self.logo)

        return self.root

    def _update_rect(self, instance, value):
        self.bg.size = instance.size
        self.bg.pos = instance.pos

    def fade_background(self, *args):
        self.bg_color.a = 1
        anim = Animation(a=0, duration=0.5)  # Speed up the fade animation
        anim.bind(on_complete=self._change_background_image)
        anim.start(self.bg_color)

    def _change_background_image(self, *args):
        with self.root.canvas.before:
            Color(1, 1, 1, 1)  # Ensure the color is set to white for the image
            self.bg = Rectangle(source='background.jpg', size=Window.size)
            self.root.bind(size=self._update_rect, pos=self._update_rect)
        self.build_main_layout()

    def build_main_layout(self, *args):
        self.root.remove_widget(self.logo)

        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint=(0.9, 0.9))
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Make font size responsive based on window size
        self.font_size = max(20, int(Window.width * 0.04))
        self.font_color = (0, 0, 0, 1)  # Default font color to black

        self.country_button = Button(text='Choose Country', size_hint=(1, 0.1), font_name='white.otf', font_size=self.font_size)
        self.country_button.bind(on_release=self.show_countries)

        self.city_button = Button(text='Choose City', size_hint=(1, 0.1), font_name='white.otf', font_size=self.font_size)
        self.city_button.bind(on_release=self.show_cities)
        self.city_button.disabled = True

        self.weather_label = Label(text="Weather info will be shown here", size_hint=(1, 0.6), font_name='white.otf', font_size=self.font_size, color=self.font_color)

        self.layout.add_widget(self.country_button)
        self.layout.add_widget(self.city_button)
        self.layout.add_widget(self.weather_label)

        # Add buttons to adjust font size and color
        self.font_size_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=dp(10))
        self.increase_font_size_button = Button(text='A+', on_release=self.increase_font_size)
        self.decrease_font_size_button = Button(text='A-', on_release=self.decrease_font_size)
        self.change_font_color_button = Button(text='Change Color', on_release=self.change_font_color)
        
        self.font_size_layout.add_widget(self.increase_font_size_button)
        self.font_size_layout.add_widget(self.decrease_font_size_button)
        self.font_size_layout.add_widget(self.change_font_color_button)
        
        self.layout.add_widget(self.font_size_layout)

        self.root.add_widget(self.layout)

    def show_countries(self, instance):
        self.country_dropdown = DropDown()
        btn = Button(text='Hungary', size_hint_y=None, height=dp(44), font_name='white.otf', font_size=self.font_size)
        btn.bind(on_release=lambda btn: self.select_country(btn.text))
        self.country_dropdown.add_widget(btn)
        self.country_dropdown.open(self.country_button)
        
        animation = Animation(opacity=1, duration=0.5)
        animation.start(self.country_dropdown)

    def select_country(self, country):
        self.country_button.text = country
        self.country_dropdown.dismiss()
        self.city_button.disabled = False
        self.weather_label.text = ""

    def show_cities(self, instance):
        self.city_dropdown = DropDown()
        for city in hungarian_cities.keys():
            display_city = replace_accented_characters(city)
            btn = Button(text=display_city.capitalize(), size_hint_y=None, height=dp(44), font_name='white.otf', font_size=self.font_size)
            btn.bind(on_release=lambda btn: self.select_city(btn.text))
            self.city_dropdown.add_widget(btn)
        self.city_dropdown.open(self.city_button)
        
        animation = Animation(opacity=1, duration=0.5)
        animation.start(self.city_dropdown)

    def select_city(self, city):
        city_key = replace_accented_characters(city.lower())
        original_city = [orig_city for orig_city in hungarian_cities.keys() if replace_accented_characters(orig_city) == city_key]
        
        if original_city:
            latitude, longitude = hungarian_cities[original_city[0]]
            self.city_button.text = city.capitalize()
            self.city_dropdown.dismiss()
            
            weather_info = weather_requests.get_weather(latitude, longitude)
            weekday = datetime.now().strftime("%A")
            self.weather_label.text = f"{weekday}: {weather_info}"
        else:
            self.weather_label.text = "City not found."
        
        animation = Animation(opacity=1, duration=0.5)
        animation.start(self.weather_label)

    def increase_font_size(self, instance):
        self.font_size += 2
        self.update_font_properties()

    def decrease_font_size(self, instance):
        self.font_size -= 2
        self.update_font_properties()

    def change_font_color(self, instance):
        self.font_color = (1, 0, 0, 1) if self.font_color == (0, 0, 0, 1) else (0, 0, 0, 1)  # Toggle between black and red
        self.update_font_properties()

    def update_font_properties(self):
        self.country_button.font_size = self.font_size
        self.city_button.font_size = self.font_size
        self.weather_label.font_size = self.font_size
        self.weather_label.color = self.font_color

if __name__ == "__main__":
    MyApp().run()
