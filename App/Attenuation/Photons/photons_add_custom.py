##### IMPORTS #####
from Core.Attenuation.Photons.photons_custom import *
from Utility.Functions.gui_utility import *
from tkinter import *
from tkinter import ttk, font
from App.style import SectionFrame

# For global access to nodes on photon attenuation add custom screen
add_custom_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the photon attenuation add custom screen.
The following sections and widgets are created:
   Module Title (Photon Attenuation)
   Enter Material Name section
   Enter Density section
   Enter Element Weights section
   Enter Material in Database section
   Back button
This function contains all of the logic involving these widgets'
behaviors.
The sections and widgets are stored in add_custom_list so they can be
accessed later by clear_add_custom.
"""
def photons_add_custom(root, common_el, common_mat, element, material, custom_mat,
                       category, mode, interactions, mac_num, d_num, lac_num, mac_den,
                       d_den, lac_den, energy_unit):
    global add_custom_list

    # Makes title frame
    title_frame = make_title_frame(root, "Photon Attenuation")

    # Creates font for element weights entry
    monospace_font = font.Font(family="Menlo", size=12)

    # Frame for material name
    material_frame = SectionFrame(root, title="Enter Material Name")
    material_frame.pack()
    inner_material_frame = material_frame.get_inner_frame()
    mat_frame = Frame(inner_material_frame, bg="#F2F2F2")
    mat_frame.pack()
    entry = make_line(mat_frame, "Material Name:", monospace_font)

    # Spacer
    empty_frame1 = make_spacer(root)

    # Frame for density
    density_frame = SectionFrame(root, title="Enter Density")
    density_frame.pack()
    inner_density_frame = density_frame.get_inner_frame()
    den_frame = Frame(inner_density_frame, bg="#F2F2F2")
    den_frame.pack()
    entry2 = make_line(den_frame, f"Density ({d_num}/{d_den}):", monospace_font)

    # Spacer
    empty_frame2 = make_spacer(root)

    # Frame for element weights
    weights_frame = SectionFrame(root, title="Enter Element Weights")
    weights_frame.pack()
    inner_weights_frame = weights_frame.get_inner_frame()
    w_frame = Frame(inner_weights_frame, bg="#F2F2F2")
    w_frame.pack()

    # Frame for element weights example
    ex_frame = Frame(w_frame, bg="#F2F2F2")
    ex_frame.pack(side="left", padx=(0,30))

    # Element weights label
    basic_label(ex_frame, "Element Weights:")

    # Element weights entry
    entry_width = 16 if platform.system() == "Windows" else 20
    entry3 = Text(w_frame, width=entry_width, height=10, bg='white', fg='black',
                  insertbackground="black", borderwidth=3, bd=3,
                  highlightthickness=0, relief='solid', font=monospace_font)
    entry3.pack(side="left", padx=(30,0), pady=20)

    # Make element weights example
    basic_label(ex_frame, "")
    basic_label(ex_frame, "Example:")
    basic_label(ex_frame, "0.30, Pb")
    basic_label(ex_frame, "0.55, Si")
    basic_label(ex_frame, "0.13, O")
    basic_label(ex_frame, "0.02, K")

    # Spacer
    empty_frame3 = make_spacer(root)

    # Frame for options
    options_frame = SectionFrame(root, title="Enter Material in Database")
    options_frame.pack()
    inner_options_frame = options_frame.get_inner_frame()

    # Variable to hold normalize option
    var_normalize = IntVar()

    # Creates checkbox for normalizing weights
    normalize = ttk.Checkbutton(inner_options_frame, text="Normalize", variable=var_normalize,
                                style="Maize.TCheckbutton", command=lambda: root.focus())
    normalize.pack(pady=(10,5))

    # Creates Add Material button
    add_button = ttk.Button(inner_options_frame, text="Add Material", style="Maize.TButton",
                        padding=(0,0),
                        command=lambda: add_custom(root, entry, entry2, entry3,
                                                   error_label, var_normalize.get(),
                                                   d_num, d_den))
    add_button.config(width=get_width(["Add Material"]))
    add_button.pack(pady=5)

    # Creates error label for bad input
    error_label = ttk.Label(inner_options_frame, text="", style="Error.TLabel")
    error_label.pack(pady=(5,10))

    # Creates Back button to return to photon attenuation advanced screen
    back_button = ttk.Button(root, text="Back", style="Maize.TButton", padding=(0,0),
                             command=lambda: advanced_back(root, common_el, common_mat,
                                                           element, material, custom_mat,
                                                           category, mode, interactions,
                                                           mac_num, d_num, lac_num,
                                                           mac_den, d_den, lac_den, energy_unit))
    back_button.config(width=get_width(["Back"]))
    back_button.pack(pady=5)

    # Stores nodes into global list
    add_custom_list = [title_frame,
                       material_frame, empty_frame1,
                       density_frame, empty_frame2,
                       weights_frame, empty_frame3,
                       options_frame, back_button]

#####################################################################################
# HELPER SECTION
#####################################################################################

"""
This function makes a horizontal frame with a label and an entry.
It is used for both the Enter Material Name and Enter Density sections.
"""
def make_line(frame, text, monospace_font):
    entry_width = 28 if platform.system() == "Windows" else 32
    label = ttk.Label(frame, text=text, style="Black.TLabel")
    entry = Entry(frame, width=entry_width, insertbackground="black",
                  background="white", foreground="black",
                  borderwidth=3, bd=3, highlightthickness=0, relief='solid',
                  font=monospace_font)
    label.pack(side="left", padx=(0,5))
    entry.pack(side="left", padx=(5,0), pady=20)
    return entry

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the photon attenuation add custom screen
in preparation for opening a different screen.
"""
def clear_add_custom():
    global add_custom_list

    # Clears photon attenuation add custom screen
    for node in add_custom_list:
        node.destroy()
    add_custom_list.clear()

"""
This function transitions from the photon attenuation add custom screen
to the photon attenuation advanced screen by first clearing the
photon attenuation add custom screen and then creating the
photon attenuation advanced screen.
It is called when the Back button is hit.
"""
def advanced_back(root, common_el, common_mat, element, material, custom_mat,
                  category, mode, interactions, mac_num, d_num, lac_num,
                  mac_den, d_den, lac_den, energy_unit):
    from App.Attenuation.Photons.photons_advanced import photons_advanced

    clear_add_custom()
    photons_advanced(root, category=category, mode=mode,
                     interactions_start=interactions, common_el=common_el,
                     common_mat=common_mat, element=element, material=material,
                     custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                     lac_num=lac_num, mac_den=mac_den, d_den=d_den,
                     lac_den=lac_den, energy_unit=energy_unit)