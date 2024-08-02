from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

class MyApp(App):
    def build(self):
        Window.set_title("SimpleWeather")  # Set the window title here
        return Label(text="Hello, Kivy!")

if __name__ == "__main__":
    MyApp().run()
