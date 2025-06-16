##### IMPORTS #####
import shelve

def carry_action(action, category, choices, inverse, var, dropdown):
    if action == "Add":
        add_c(category, choices, inverse, var, dropdown)
    elif action == "Remove":
        remove_c(category, choices, inverse, var, dropdown)

def add_c(selection, choices, inverse, var, dropdown):
    with shelve.open('Data/Modules/Mass Attenuation/User/' + selection) as prefs:
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
    with shelve.open('Data/Modules/Mass Attenuation/User/' + selection) as prefs:
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