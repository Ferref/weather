import winshell
import os

def create_shortcut():
    try:
        # Get the path to the desktop
        desktop = winshell.desktop()
        # Define the path for the shortcut
        path = os.path.join(desktop, "SimpleWeather.lnk")
        # Define the target path (where the shortcut points to)
        target = os.path.join(os.getcwd(), "main.py")
        # Define the icon path
        icon = os.path.join(os.getcwd(), "icon_nobg.ico")

        # Create the shortcut
        winshell.CreateShortcut(
            Path=path,
            Target=target,
            Icon=(icon, 0),
            Description="SimpleWeather Application"
        )

        print(f"Shortcut created successfully at {path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to create the shortcut
create_shortcut()
