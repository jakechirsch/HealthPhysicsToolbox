##### IMPORTS #####
from tkinter import *
from App.Attenuation.tac_main import total_attenuation_coefficient

##### WINDOW SETUP #####
root = Tk()
root.title("Health Physics Toolbox")
root.geometry("725x450")

##### HOME SCREEN BUTTONS #####
tac_button = Button(root)
home_list = []

def clear_home():
    global home_list

    # Clears home
    for node in home_list:
        node.destroy()

def return_home():
    global tac_button

    # Creates buttons for home screen
    tac_button = Button(root, text="Total Attenuation Coefficient", command=tac)
    tac_button.pack(pady=5)
    home_list.append(tac_button)

def tac():
    clear_home()
    total_attenuation_coefficient(root)

# Creates home screen upon launch
return_home()

# Runs app
root.mainloop()