##### IMPORTS #####
import shelve
from Utility.Functions.gui_utility import get_width, get_user_data_path

def carry_action(action, category, choices, inverse, var, dropdown):
    if action == "Add":
        add_c(category, choices, inverse, var, dropdown)
    elif action == "Remove":
        remove_c(category, choices, inverse, var, dropdown)

def add_c(selection, choices, inverse, var, dropdown):
    db_path = get_user_data_path('Mass Attenuation/' + selection)
    with shelve.open(db_path) as prefs:
        # Adds element to common elements
        element = var.get()
        if element == "":
            return
        inverse.append(element)
        prefs[selection] = inverse

        # Removes element from non-common elements
        choices.remove(element)
        dropdown.config(completevalues=choices, width=get_width(choices))
        var.set(choices[0] if len(choices) > 0 else "")

def remove_c(selection, choices, inverse, var, dropdown):
    db_path = get_user_data_path('Mass Attenuation/' + selection)
    with shelve.open(db_path) as prefs:
        # Removes element from common elements
        element = var.get()
        if element == "":
            return
        choices.remove(element)
        prefs[selection] = choices
        dropdown.config(completevalues=choices, width=get_width(choices))
        var.set(choices[0] if len(choices) > 0 else "")

        # Adds element to non-common elements
        inverse.append(element)