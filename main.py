from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    title = 'SimpleWeather'  # Set the window title here

    def build(self):
        return Label(text="Hello, Kivy!")  # Return a Label widget

if __name__ == "__main__":
    MyApp().run()
