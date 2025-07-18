##### IMPORTS #####
from Utility.Functions.gui_utility import *

# For global access to nodes on electron attenuation advanced screen
advanced_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

def electrons_advanced(root, category, mode, common_el, common_mat, element,
                       material, num, den, energy_unit):
    global advanced_list

    # Makes title frame
    title_frame = make_title_frame(root, "Electron Attenuation")

    # Creates Back button to return to electron attenuation main screen
    back_button = ttk.Button(root, text="Back", style="Maize.TButton",
                             padding=(0, 0),
                             command=lambda: to_main(root, category, mode,
                                                     common_el, common_mat, element,
                                                     material, num, den, energy_unit))
    back_button.config(width=get_width(["Back"]))
    back_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [title_frame, back_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the electron attenuation advanced screen
in preparation for opening a different screen.
"""
def clear_advanced():
    global advanced_list

    # Clears electron attenuation advanced screen
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()

"""
This function transitions from the electron attenuation advanced screen
to the electron attenuation main screen by first clearing the
electron attenuation advanced screen and then creating the
electron attenuation main screen.
It is called when the Back button is hit.
"""
def to_main(root, category, mode, common_el, common_mat, element,
            material, num, den, energy_unit):
    from App.Attenuation.Electrons.electrons_main import electrons_main

    clear_advanced()
    electrons_main(root, category, mode, common_el, common_mat, element,
                   material, num, den, energy_unit)