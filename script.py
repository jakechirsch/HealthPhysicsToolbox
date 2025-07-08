##### IMPORTS #####
import tkinter as tk
from App.app import return_home
from App.style import configure_style
from App.scroll import configure_scrolling
from Utility.Functions.gui_utility import set_mpl_cache_dir

# Configure matplotlib
import matplotlib
matplotlib.use('TkAgg')
set_mpl_cache_dir()

##### WINDOW SETUP #####
root = tk.Tk()
root.title("Health Physics Toolbox")
root.geometry("625x750")
root.configure(bg="#F2F2F2")

# Configures style of app
configure_style()

# Configures scrolling
scrollable_frame = configure_scrolling(root)

# Creates home screen upon launch
return_home(scrollable_frame)

# Runs app
root.mainloop()