##### IMPORTS #####
from tkinter import ttk
from App.Attenuation.attenuation import attenuation_menu
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

    title = ttk.Label(root, text="Health Physics Toolbox", style="Home.TLabel")
    title.pack(pady=5)

    # Creates buttons for home screen
    tac_button = ttk.Button(root, text="Attenuation and Range Data",
                            command=lambda: tac(root), style="Maize.TButton",
                            padding=(0,0))
    tac_button.config(width=get_width(["Attenuation and Range Data"]))
    tac_button.pack(pady=5)
    home_list = [tac_button, title]

"""
This function transitions from the home screen
to the attenuation screen by first clearing the
home screen and then creating the attenuation screen.
It is called when the Attenuation Coefficients button is hit.
"""
def tac(root):
    root.focus()
    clear_home()
    attenuation_menu(root)