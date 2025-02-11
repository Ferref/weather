from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.uix.slider import Slider
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

class WeatherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = max(20, int(Window.width * 0.04))  # Initialize font_size
        self.title_font_color = (0, 0, 0, 1)  # Initialize title font color to black
        self.info_font_color = (0, 0, 0, 1)  # Initialize info font color to black
        self.build_ui()

    def build_ui(self):
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            self.bg_color = Color(0, 0, 0, 1)
            self.bg = Rectangle(size=Window.size)
            self.layout.bind(size=self._update_rect, pos=self._update_rect)

        self.logo = Image(source='icon_nobg.png', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(self.logo)
        
        animation = Animation(opacity=0, duration=0.5)
        animation.bind(on_complete=self.fade_background)
        animation.start(self.logo)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.bg.size = instance.size
        self.bg.pos = instance.pos

    def fade_background(self, *args):
        self.bg_color.a = 1
        anim = Animation(a=0, duration=0.5)
        anim.bind(on_complete=self._change_background_image)
        anim.start(self.bg_color)

    def _change_background_image(self, *args):
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(source='background.jpg', size=Window.size)
            self.layout.bind(size=self._update_rect, pos=self._update_rect)
        self.build_main_layout()

    def build_main_layout(self, *args):
        self.layout.remove_widget(self.logo)

        self.main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint=(0.9, 0.9))
        self.main_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.country_button = Button(text='Choose Country', size_hint=(1, 0.1), font_size=self.font_size, color=self.title_font_color)
        self.country_button.bind(on_release=self.show_countries)

        self.city_button = Button(text='Choose City', size_hint=(1, 0.1), font_size=self.font_size, color=self.title_font_color)
        self.city_button.bind(on_release=self.show_cities)
        self.city_button.disabled = True

        self.weather_label = Label(text="Weather info will be shown here", size_hint=(1, 0.6), font_size=self.font_size, color=self.info_font_color)

        self.settings_button = Button(text='Settings', size_hint=(1, 0.1), font_size=self.font_size, color=self.title_font_color)
        self.settings_button.bind(on_release=self.go_to_settings)

        self.main_layout.add_widget(self.country_button)
        self.main_layout.add_widget(self.city_button)
        self.main_layout.add_widget(self.weather_label)
        self.main_layout.add_widget(self.settings_button)

        self.layout.add_widget(self.main_layout)

    def show_countries(self, instance):
        self.country_dropdown = DropDown()
        btn = Button(text='Hungary', size_hint_y=None, height=dp(44), font_size=self.font_size)
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
            btn = Button(text=display_city.capitalize(), size_hint_y=None, height=dp(44), font_size=self.font_size)
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

    def go_to_settings(self, instance):
        self.manager.current = 'settings'

    def update_font_properties(self):
        if hasattr(self, 'country_button'):
            self.country_button.font_size = self.font_size
            self.country_button.color = self.title_font_color
        if hasattr(self, 'city_button'):
            self.city_button.font_size = self.font_size
            self.city_button.color = self.title_font_color
        if hasattr(self, 'weather_label'):
            self.weather_label.font_size = self.font_size
            self.weather_label.color = self.info_font_color
        if hasattr(self, 'settings_button'):
            self.settings_button.font_size = self.font_size
            self.settings_button.color = self.title_font_color

class SettingsScreen(Screen):
    def __init__(self, weather_screen, **kwargs):
        super().__init__(**kwargs)
        self.weather_screen = weather_screen
        self.build_ui()

    def build_ui(self):
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint=(0.9, 0.9))
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.font_size_label = Label(text='Font Size', size_hint=(1, 0.1), font_size=self.weather_screen.font_size)
        self.font_size_slider = Slider(min=10, max=50, value=self.weather_screen.font_size, size_hint=(1, 0.1))
        self.font_size_slider.bind(value=self.on_font_size_change)

        self.title_color_label = Label(text='Title Font Color', size_hint=(1, 0.1), font_size=self.weather_screen.font_size)
        self.title_color_layout = self.build_color_buttons(self.on_title_color_change)

        self.info_color_label = Label(text='Info Font Color', size_hint=(1, 0.1), font_size=self.weather_screen.font_size)
        self.info_color_layout = self.build_color_buttons(self.on_info_color_change)

        self.back_button = Button(text='Back', size_hint=(1, 0.1), font_size=self.weather_screen.font_size)
        self.back_button.bind(on_release=self.go_back)

        self.layout.add_widget(self.font_size_label)
        self.layout.add_widget(self.font_size_slider)
        self.layout.add_widget(self.title_color_label)
        self.layout.add_widget(self.title_color_layout)
        self.layout.add_widget(self.info_color_label)
        self.layout.add_widget(self.info_color_layout)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def build_color_buttons(self, on_color_change_callback):
        colors = {
            "Black": (0, 0, 0, 1),
            "Red": (1, 0, 0, 1),
            "Green": (0, 1, 0, 1),
            "Blue": (0, 0, 1, 1),
            "Yellow": (1, 1, 0, 1),
            "Cyan": (0, 1, 1, 1),
            "Magenta": (1, 0, 1, 1),
            "White": (1, 1, 1, 1)
        }
        color_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, 0.2))
        for color_name, color_value in colors.items():
            btn = Button(background_color=color_value, size_hint=(None, 1), width=dp(40))
            btn.bind(on_release=lambda instance, clr=color_value: on_color_change_callback(clr))
            color_layout.add_widget(btn)
        return color_layout

    def on_font_size_change(self, instance, value):
        self.weather_screen.font_size = int(value)
        self.weather_screen.update_font_properties()

    def on_title_color_change(self, color):
        self.weather_screen.title_font_color = color
        self.weather_screen.update_font_properties()

    def on_info_color_change(self, color):
        self.weather_screen.info_font_color = color
        self.weather_screen.update_font_properties()

    def go_back(self, instance):
        self.manager.current = 'weather'

class MyApp(App):
    title = 'WeatherBunny'
    icon = 'icon_nobg.png'

    def build(self):
        self.sm = ScreenManager()

        self.weather_screen = WeatherScreen(name='weather')
        self.settings_screen = SettingsScreen(self.weather_screen, name='settings')

        self.sm.add_widget(self.weather_screen)
        self.sm.add_widget(self.settings_screen)

        return self.sm

if __name__ == "__main__":
    MyApp().run()
