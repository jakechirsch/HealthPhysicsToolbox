##### IMPORTS #####
from tkinter import *
from App.Attenuation.tac_main import total_attenuation_coefficient

# For global access to nodes on home screen
home_list = []

def clear_home():
    global home_list

    # Clears home
    for node in home_list:
        node.destroy()

def return_home(root):
    # Creates buttons for home screen
    tac_button = Button(root, text="Total Attenuation Coefficient",
                        command=lambda: tac(root))
    tac_button.pack(pady=5)
    home_list.append(tac_button)

def tac(root):
    clear_home()
    total_attenuation_coefficient(root)