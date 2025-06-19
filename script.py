##### IMPORTS #####
from tkinter import Tk
from App.app import return_home
from App.style import configure_style

##### WINDOW SETUP #####
root = Tk()
root.title("Health Physics Toolbox")
root.geometry("625x375")
root.configure(bg="#00274C")

# Configures style of app
configure_style()

# Creates home screen upon launch
return_home(root)

# Runs app
root.mainloop()