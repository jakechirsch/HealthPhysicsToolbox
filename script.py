##### IMPORTS #####
from tkinter import Tk, Frame
from App.app import return_home
from App.style import configure_style

##### WINDOW SETUP #####
root = Tk()
root.title("Health Physics Toolbox")
root.geometry("625x600")
root.configure(bg="#00274C")

# Configures style of app
configure_style()

# Wraps whole app in a container for vertical alignment
container = Frame(root, bg="#00274C")
container.pack(expand=True)

# Creates home screen upon launch
return_home(container)

# Runs app
root.mainloop()