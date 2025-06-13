##### IMPORTS #####
from tkinter import *
from App.app import return_home

##### WINDOW SETUP #####
root = Tk()
root.title("Health Physics Toolbox")
root.geometry("725x450")
root.configure(bg="#00274C")

# Creates home screen upon launch
return_home(root)

# Runs app
root.mainloop()