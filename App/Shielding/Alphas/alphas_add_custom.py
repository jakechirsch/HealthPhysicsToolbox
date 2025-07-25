##### IMPORTS #####
from Utility.Functions.custom import *
from Utility.Functions.gui_utility import *
from tkinter import *
from tkinter import ttk
from App.style import SectionFrame

# For global access to nodes on alpha range add custom screen
add_custom_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the alpha range add custom screen.
The following sections and widgets are created:
   Module Title (Alpha Range)
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
def alphas_add_custom(root, category, mode, common_el, common_mat, element,
                         material, custom_mat, csda_num, d_num, csda_den, d_den,
                         energy_unit):
    global add_custom_list

    # Makes title frame
    title_frame = make_title_frame(root, "Alpha Range")

    # Frame for material name
    material_frame = SectionFrame(root, title="Enter Material Name")
    material_frame.pack()
    inner_material_frame = material_frame.get_inner_frame()
    mat_frame = Frame(inner_material_frame, bg="#F2F2F2")
    mat_frame.pack()
    entry = make_entry_line(mat_frame, "Material Name:")

    # Spacer
    empty_frame1 = make_spacer(root)

    # Frame for density
    density_frame = SectionFrame(root, title="Enter Density")
    density_frame.pack()
    inner_density_frame = density_frame.get_inner_frame()
    den_frame = Frame(inner_density_frame, bg="#F2F2F2")
    den_frame.pack()
    entry2 = make_entry_line(den_frame, f"Density ({d_num}/{d_den}):")

    # Spacer
    empty_frame2 = make_spacer(root)

    # Frame for element weights
    weights_frame = SectionFrame(root, title="Enter Element Weights")
    weights_frame.pack()
    inner_weights_frame = weights_frame.get_inner_frame()
    w_frame = Frame(inner_weights_frame, bg="#F2F2F2")
    w_frame.pack()
    entry3 = make_weights_line(w_frame)

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
                                                   d_num, d_den, "Alphas"))
    add_button.config(width=get_width(["Add Material"]))
    add_button.pack(pady=5)

    # Creates error label for bad input
    error_label = ttk.Label(inner_options_frame, text="", style="Error.TLabel")
    error_label.pack(pady=(5,10))

    # Creates Back button to return to alpha range advanced screen
    back_button = ttk.Button(root, text="Back", style="Maize.TButton", padding=(0,0),
                             command=lambda: advanced_back(root, category, mode,
                                                           common_el, common_mat, element,
                                                           material, custom_mat, csda_num,
                                                           d_num, csda_den, d_den,
                                                           energy_unit))
    back_button.config(width=get_width(["Back"]))
    back_button.pack(pady=5)

    # Stores nodes into global list
    add_custom_list = [title_frame,
                       material_frame, empty_frame1,
                       density_frame, empty_frame2,
                       weights_frame, empty_frame3,
                       options_frame, back_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the alpha range add custom screen
in preparation for opening a different screen.
"""
def clear_add_custom():
    global add_custom_list

    # Clears alpha range add custom screen
    for node in add_custom_list:
        node.destroy()
    add_custom_list.clear()

"""
This function transitions from the alpha range add custom screen
to the alpha range advanced screen by first clearing the
alpha range add custom screen and then creating the
alpha range advanced screen.
It is called when the Back button is hit.
"""
def advanced_back(root, category, mode, common_el, common_mat, element,
                  material, custom_mat, csda_num, d_num, csda_den, d_den,
                  energy_unit):
    from App.Shielding.Alphas.alphas_advanced import alphas_advanced

    clear_add_custom()
    alphas_advanced(root, category, mode, common_el, common_mat, element,
                    material, custom_mat, csda_num, d_num, csda_den, d_den,
                    energy_unit)