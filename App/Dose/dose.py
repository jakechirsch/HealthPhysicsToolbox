##### IMPORTS #####
from tkinter import ttk
from App.Dose.Photons.photons_main import photons_main
from Utility.Functions.gui_utility import get_width, make_title_frame

# For global access to nodes on dose screen
dose_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function creates the dose screen.
"""
def dose_menu(root):
    global dose_list

    title = make_title_frame(root, "Radiation Dose Data", "Dose")

    # Creates photons button
    photons_button = ttk.Button(root, text="Photons",
                                command=lambda: to_photons(root),
                                style="Maize.TButton", padding=(0,0))
    photons_button.config(width=get_width(["Photons"]))
    photons_button.pack(pady=5)

    # Creates Exit button to return to home screen
    exit_button = ttk.Button(root, text="Exit", style="Maize.TButton",
                             padding=(0, 0),
                             command=lambda: exit_to_home(root))
    exit_button.config(width=get_width(["Exit"]))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    dose_list = [title, photons_button, exit_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the dose screen in preparation
for opening a different screen.
"""
def clear_dose():
    global dose_list

    # Clears home
    for node in dose_list:
        node.destroy()

"""
This function transitions from the dose screen
to the home screen by first clearing the dose screen
and then creating the home screen.
It is called when the Exit button is hit.
"""
def exit_to_home(root):
    root.focus()
    from App.home import return_home
    clear_dose()
    return_home(root)

"""
This function transitions from the dose screen
to the photon energy absorption main screen by first
clearing the dose screen and then creating the
photon energy absorption main screen.
It is called when the Photons button is hit.
"""
def to_photons(root):
    root.focus()
    clear_dose()
    photons_main(root)