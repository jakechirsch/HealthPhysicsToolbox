##### IMPORTS #####
from tkinter import ttk
from Utility.Functions.gui_utility import get_width

"""
This function makes a Combobox dropdown for units selections.
"""
def unit_dropdown(frame, choices, unit, on_select_u):
    dropdown = ttk.Combobox(frame, values=choices, justify="center", state='readonly',
                            style="Maize.TCombobox")
    dropdown.config(width=get_width(choices))
    dropdown.set(unit)
    dropdown.pack(side='left', padx=5)
    dropdown.bind("<<ComboboxSelected>>", on_select_u)

"""
This function creates and returns a new function to be
called when a unit is selected in a unit dropdown.
"""
def get_select_unit(root, units, mode):
    def on_select_unit(event):
        nonlocal mode
        event.widget.selection_clear()
        root.focus()
        if mode == "Mass Attenuation Coefficient":
            units[0] = event.widget.get()
        elif mode == "Density":
            units[1] = event.widget.get()
        else:
            units[2] = event.widget.get()
    return on_select_unit

"""
This function retrieves the unit choices for a
particular calculation mode.
"""
def get_unit_keys(mac, density, lac, mode):
    _dict = get_unit(mac, density, lac, mode)
    choices = list(_dict.keys())
    return choices

"""
This function returns the relevant item based on the
calculation mode.
It is used in two cases:
1. To retrieve the correct unit out of the saved units
   of each mode
2. To retrieve the correct list of unit choices for the
   selected mode
"""
def get_unit(mac, d, lac, mode):
    return mac if mode == "Mass Attenuation Coefficient" else\
           d if mode == "Density" else lac