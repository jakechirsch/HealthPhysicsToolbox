##### IMPORTS #####
import shelve
from tkinter import *

def carry_action(action, category, choices, inverse, var, dropdown):
    if action == "Add":
        add_c(category, choices, inverse, var, dropdown)
    elif action == "Remove":
        remove_c(category, choices, inverse, var, dropdown)

def add_custom(root, name_box, density_box, weights_box):
    name = name_box.get()
    density = density_box.get()
    weights = weights_box.get()
    csv_data = '"Weight","Element"\n' + weights

    with shelve.open("Custom Materials") as prefs:
        choices = prefs.get("Custom Materials", [])
        if not name in choices:
            choices.append(name)
        prefs["Custom Materials"] = choices

    # Save to shelve
    with shelve.open('_' + name) as db:
        db[name] = csv_data
        db[name + '_Density'] = density

    name_box.delete(0, END)
    weights_box.delete(0, END)
    density_box.delete(0, END)
    root.focus()

def add_c(selection, choices, inverse, var, dropdown):
    with shelve.open(selection) as prefs:
        # Adds element to common elements
        element = var.get()
        if element == "":
            return
        inverse.append(element)
        prefs[selection] = inverse

        # Removes element from non-common elements
        choices.remove(element)
        dropdown.config(completevalues=choices)
        var.set(choices[0] if len(choices) > 0 else "")

def remove_c(selection, choices, inverse, var, dropdown):
    with shelve.open(selection) as prefs:
        # Removes element from common elements
        element = var.get()
        if element == "":
            return
        choices.remove(element)
        prefs[selection] = choices
        dropdown.config(completevalues=choices)
        var.set(choices[0] if len(choices) > 0 else "")

        # Adds element to non-common elements
        inverse.append(element)