##### IMPORTS #####
from tkinter.ttk import Combobox

def unit_dropdown(frame, choices, unit, on_select_u):
    # Creates a unit dropdown
    dropdown = Combobox(frame, values=choices, width=5, state='readonly')
    dropdown.set(unit)
    dropdown.pack(side='left', padx=5)
    dropdown.bind("<<ComboboxSelected>>", on_select_u)

def get_select_unit(root, units, mode):
    # Creates an on_select function for a unit dropdown
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

def get_unit_keys(mac, density, lac, mode):
    # Returns the relevant unit options based on mode
    _dict = get_unit(mac, density, lac, mode)
    choices = list(_dict.keys())
    return choices

def get_unit(mac, d, lac, mode):
    # Returns the relevant unit based on mode
    return mac if mode == "Mass Attenuation Coefficient" else\
           d if mode == "Density" else lac