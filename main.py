from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import weather_requests  # Import the weather_requests module

# Predefined list of countries and their cities with corresponding latitude and longitude
locations = {
    "Hungary": {
        "Budapest": (47.4979, 19.0402),
        "Debrecen": (47.5316, 21.6273),
        "Szeged": (46.2530, 20.1414),
        "Miskolc": (48.1030, 20.7784),
        "Pécs": (46.0727, 18.2323)
    }
}

class MyApp(App):
    title = 'SimpleWeather'  # Set the window title here

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.country_dropdown = DropDown()
        self.city_dropdown = DropDown()

        self.country_button = Button(text='Choose Country', size_hint=(1, 0.1))
        self.country_button.bind(on_release=self.country_dropdown.open)

        for country in locations.keys():
            btn = Button(text=country, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_country(btn.text))
            self.country_dropdown.add_widget(btn)

        self.city_button = Button(text='Choose City', size_hint=(1, 0.1))
        self.city_button.bind(on_release=self.city_dropdown.open)

        self.weather_label = Label(text="Weather info will be shown here", size_hint=(1, 0.8))

        self.layout.add_widget(self.country_button)
        self.layout.add_widget(self.city_button)
        self.layout.add_widget(self.weather_label)

        return self.layout

    def select_country(self, country):
        self.country_button.text = country
        self.country_dropdown.dismiss()
        
        self.city_button.text = 'Choose City'
        self.city_dropdown.clear_widgets()

        for city in locations[country].keys():
            btn = Button(text=city, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.update_weather(country, btn.text))
            self.city_dropdown.add_widget(btn)

    def update_weather(self, country, city):
        self.city_button.text = city
        self.city_dropdown.dismiss()

        latitude, longitude = locations[country][city]

        # Get the weather data
        weather_info = weather_requests.get_weather(latitude, longitude)

        # Update the label with the weather information
        self.weather_label.text = weather_info

if __name__ == "__main__":
    MyApp().run()
