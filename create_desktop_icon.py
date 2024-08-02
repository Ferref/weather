import winshell
import os

def create_shortcut():
    desktop = winshell.desktop()
    path = os.path.join(desktop, "SimpleWeather.lnk")
    target = os.path.join(os.getcwd(), "main.py")
    icon = os.path.join(os.getcwd(), "icon_nobg.png")
    winshell.CreateShortcut(
        Path=path,
        Target=target,
        Icon=(icon, 0),
        Description="SimpleWeather Application"
    )

create_shortcut()
