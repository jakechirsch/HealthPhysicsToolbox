##### IMPORTS #####
import shelve
from tkinter import *

def add_custom(root, name_box, density_box, weights_box):
    name = name_box.get()
    density = density_box.get()
    weights = weights_box.get()
    csv_data = '"Weight","Element"\n' + weights

    with shelve.open("Data/Modules/Mass Attenuation/User/Custom Materials") as prefs:
        choices = prefs.get("Custom Materials", [])
        if not name in choices:
            choices.append(name)
        prefs["Custom Materials"] = choices

    # Save to shelve
    with shelve.open('Data/Modules/Mass Attenuation/User/_' + name) as db:
        db[name] = csv_data
        db[name + '_Density'] = density

    name_box.delete(0, END)
    weights_box.delete(0, END)
    density_box.delete(0, END)
    root.focus()