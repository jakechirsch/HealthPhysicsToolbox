##### IMPORTS #####
from App.style import SectionFrame
from Utility.Functions.gui_utility import *
from Utility.Functions.choices import *
from Core.Decay.Information.nuclide_info import *

# For global access to nodes on photon attenuation main screen
info_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

def decay_info_main(root, element="Ac", isotope="Ac-223"):
    global info_list

    # Makes title frame
    title_frame = make_title_frame(root, "Decay Information", "Decay/Information")

    # Gets the item options
    element_list = get_choices("All Elements", "Decay", "")

    # Frame for nuclide selection
    nuclide_frame = SectionFrame(root, title="Select Nuclide")
    nuclide_frame.pack()
    inner_nuclide_frame = nuclide_frame.get_inner_frame()

    # Horizontal frame for nuclide selection
    nuclide_side_frame = Frame(inner_nuclide_frame, bg="#F2F2F2")
    nuclide_side_frame.pack(pady=(20,30))

    # Logic for when an element is selected
    def on_select_element(event):
        nonlocal element, isotope

        event.widget.selection_clear()
        new_element = element_dropdown.get()

        isotopes = get_isotopes(new_element)
        if element != new_element:
            isotope = isotopes[0]
            element = new_element
        isotope_dropdown.set(isotope)
        isotope_dropdown.config(values=isotopes, width=get_width(isotopes))

        root.focus()

    # Frame for element selection
    element_frame = Frame(nuclide_side_frame, bg="#F2F2F2")
    element_frame.pack(side="left", padx=5)

    # Element label
    basic_label(element_frame, "Element:")

    # Creates dropdown menu for element
    element_dropdown = ttk.Combobox(element_frame, values=element_list, justify="center",
                                    state='readonly', style="Maize.TCombobox")
    element_dropdown.config(width=get_width(element_list))
    element_dropdown.set(element_list[0])
    element_dropdown.pack()
    element_dropdown.bind("<<ComboboxSelected>>", on_select_element)

    # Logic for when an isotope is selected
    def on_select_isotope(event):
        nonlocal isotope

        event.widget.selection_clear()
        isotope = isotope_dropdown.get()
        root.focus()

    # Frame for isotope selection
    category_frame = Frame(nuclide_side_frame, bg="#F2F2F2")
    category_frame.pack(side="left", padx=5)

    # Isotope label
    basic_label(category_frame, "Isotope:")

    # Creates dropdown menu for isotope
    isotope_choices = get_isotopes(element)
    isotope_dropdown = ttk.Combobox(category_frame, values=isotope_choices, justify="center",
                                    state='readonly', style="Maize.TCombobox")
    isotope_dropdown.config(width=get_width(isotope_choices))
    isotope_dropdown.set(isotope_choices[0])
    isotope_dropdown.pack()
    isotope_dropdown.bind("<<ComboboxSelected>>", on_select_isotope)

    # Creates Advanced Settings button
    plot_button = ttk.Button(root, text="Plot",
                                 style="Maize.TButton", padding=(0,0),
                                 command=lambda: plot_nuclide(isotope))
    plot_button.config(width=get_width(["Plot"]))
    plot_button.pack(pady=5)

    # Creates Exit button to return to home screen
    exit_button = ttk.Button(root, text="Exit", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: exit_to_home(root))
    exit_button.config(width=get_width(["Exit"]))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    info_list = [title_frame,
                 nuclide_frame,
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