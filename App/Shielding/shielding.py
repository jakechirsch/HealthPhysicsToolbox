##### IMPORTS #####
from tkinter import ttk
from App.Shielding.Photons.photons_main import photons_main
from App.Shielding.Electrons.electrons_main import electrons_main
from Utility.Functions.gui_utility import get_width, make_title_frame

# For global access to nodes on shielding screen
shielding_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function creates the shielding screen.
"""
def shielding_menu(root):
    global shielding_list

    title = make_title_frame(root, "Attenuation and Range Data")

    # Creates photons button
    photons_button = ttk.Button(root, text="Photons",
                                command=lambda: to_photons(root),
                                style="Maize.TButton", padding=(0,0))
    photons_button.config(width=get_width(["Photons"]))
    photons_button.pack(pady=5)

    # Creates electrons button
    electrons_button = ttk.Button(root, text="Electrons",
                                  command=lambda: to_electrons(root),
                                  style="Maize.TButton", padding=(0,0))
    electrons_button.config(width=get_width(["Electrons"]))
    electrons_button.pack(pady=5)

    # Stores nodes into global list
    shielding_list = [title, photons_button, electrons_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the shielding screen in preparation
for opening a different screen.
"""
def clear_shielding():
    global shielding_list

    # Clears home
    for node in shielding_list:
        node.destroy()

"""
This function transitions from the shielding screen
to the photon attenuation main screen by first
clearing the shielding screen and then creating the
photon attenuation main screen.
It is called when the Photons button is hit.
"""
def to_photons(root):
    root.focus()
    clear_shielding()
    photons_main(root)

"""
This function transitions from the shielding screen
to the electron range main screen by first
clearing the shielding screen and then creating the
electron range main screen.
It is called when the Electrons button is hit.
"""
def to_electrons(root):
    root.focus()
    clear_shielding()
    electrons_main(root)