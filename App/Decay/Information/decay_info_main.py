##### IMPORTS #####
from Utility.Functions.gui_utility import *

# For global access to nodes on photon attenuation main screen
info_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

def decay_info_main(root):
    global info_list

    # Makes title frame
    title_frame = make_title_frame(root, "Decay Information", "Decay/Information")

    # Creates Exit button to return to home screen
    exit_button = ttk.Button(root, text="Exit", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: exit_to_home(root))
    exit_button.config(width=get_width(["Exit"]))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    info_list = [title_frame,
                 exit_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the decay information main screen
in preparation for opening a different screen.
"""
def clear_main():
    global info_list

    # Clears decay information main screen
    for node in info_list:
        node.destroy()
    info_list.clear()

"""
This function transitions from the decay information main screen
to the home screen by first clearing the decay information main screen
and then creating the home screen.
It is called when the Exit button is hit.
"""
def exit_to_home(root):
    root.focus()
    from App.home import return_home
    clear_main()
    return_home(root)