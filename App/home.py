##### IMPORTS #####
from tkinter import ttk
from App.Shielding.shielding import shielding_menu
from Utility.Functions.gui_utility import get_width

# For global access to nodes on home screen
home_list = []

"""
This function clears the home screen in preparation
for opening a different screen.
"""
def clear_home():
    global home_list

    # Clears home
    for node in home_list:
        node.destroy()

"""
This function creates the home screen.
"""
def return_home(root):
    global home_list

    title = ttk.Label(root, text="Health Physics Toolbox", style="Blue.TLabel")
    title.pack(pady=5)

    # Creates button for shielding menu
    shielding_button = ttk.Button(root, text="Attenuation and Range Data",
                                  command=lambda: shielding(root),
                                  style="Maize.TButton", padding=(0,0))
    shielding_button.config(width=get_width(["Attenuation and Range Data"]))
    shielding_button.pack(pady=5)

    # Stores nodes into global list
    home_list = [shielding_button, title]

"""
This function transitions from the home screen
to the shielding screen by first clearing the
home screen and then creating the shielding screen.
It is called when the Attenuation and Range Data button is hit.
"""
def shielding(root):
    root.focus()
    clear_home()
    shielding_menu(root)