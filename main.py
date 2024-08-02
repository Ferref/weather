from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import weather_requests  # Import the weather_requests module

# Predefined list of Hungarian cities with corresponding latitude and longitude
hungarian_cities = {
    "Budapest": (47.4979, 19.0402),
    "Debrecen": (47.5316, 21.6273),
    "Szeged": (46.2530, 20.1414),
    "Miskolc": (48.1030, 20.7784),
    "Pécs": (46.0727, 18.2323),
    "Győr": (47.6875, 17.6504),
    "Nyíregyháza": (47.9554, 21.7167),
    "Kecskemét": (46.8964, 19.6897),
    "Székesfehérvár": (47.1944, 18.4084),
    "Szombathely": (47.2307, 16.6218),
    "Szolnok": (47.1860, 20.1904),
    "Tatabánya": (47.5699, 18.4031),
    "Kaposvár": (46.3591, 17.7963),
    "Érd": (47.3866, 18.9135),
    "Veszprém": (47.0935, 17.9090),
    "Békéscsaba": (46.6769, 21.0878),
    "Zalaegerszeg": (46.8417, 16.8439),
    "Sopron": (47.6815, 16.5845),
    "Eger": (47.9025, 20.3772),
    "Nagykanizsa": (46.4530, 16.9910),
    "Dunaújváros": (46.9633, 18.9398),
    "Hódmezővásárhely": (46.4202, 20.3198),
    "Szigetszentmiklós": (47.3434, 19.0470),
    "Dunakeszi": (47.6364, 19.1381),
    "Cegléd": (47.1734, 19.7996),
    "Baja": (46.1781, 18.9533),
    "Salgótarján": (48.0982, 19.8031),
    "Budaörs": (47.4614, 18.9583),
    "Ózd": (48.2170, 20.2894),
    "Gyula": (46.6455, 21.2854)
}

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
        if value.lower() != 'hungary':
            self.weather_label.text = "Currently, we only support Hungary."
            self.city_dropdown.dismiss()
        else:
            self.weather_label.text = ""

    def on_city_text(self, instance, value):
        self.city_dropdown.dismiss()
        self.city_dropdown.clear_widgets()

        for city in hungarian_cities.keys():
            if value.lower() in city.lower():
                btn = Button(text=city, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.update_weather('Hungary', btn.text))
                self.city_dropdown.add_widget(btn)
        
        Clock.schedule_once(self.open_city_dropdown, 0.1)

    def open_city_dropdown(self, dt):
        self.city_dropdown.open(self.city_input)

    def update_weather(self, country, city):
        self.city_input.text = city
        self.city_dropdown.dismiss()

        latitude, longitude = hungarian_cities[city]

        # Get the weather data
        weather_info = weather_requests.get_weather(latitude, longitude)

        # Update the label with the weather information
        self.weather_label.text = weather_info

if __name__ == "__main__":
    MyApp().run()
