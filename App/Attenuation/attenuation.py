##### IMPORTS #####
from tkinter import ttk
from App.Attenuation.Photons.photons_main import photons_main
from Utility.Functions.gui_utility import get_width, make_title_frame

# For global access to nodes on attenuation screen
attenuation_list = []

"""
This function clears the attenuation screen in preparation
for opening a different screen.
"""
def clear_attenuation():
    global attenuation_list

    # Clears home
    for node in attenuation_list:
        node.destroy()

"""
This function creates the attenuation screen.
"""
def attenuation_menu(root):
    global attenuation_list

    title = make_title_frame(root, "Attenuation and Range Data")

    # Creates buttons for home screen
    photons_button = ttk.Button(root, text="Photons",
                            command=lambda: to_photons(root), style="Maize.TButton",
                            padding=(0,0))
    photons_button.config(width=get_width(["Photons"]))
    photons_button.pack(pady=5)
    attenuation_list = [photons_button, title]

"""
This function transitions from the attenuation screen
to the photon attenuation main screen by first
clearing the attenuation screen and then creating the
photon attenuation main screen.
It is called when the Photons button is hit.
"""
def to_photons(root):
    root.focus()
    clear_attenuation()
    photons_main(root)