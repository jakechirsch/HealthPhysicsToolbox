##### IMPORTS #####
import tkinter as tk
from tkinter import ttk
from App.style import SectionFrame
from App.add_custom_menu import add_custom_menu
from Utility.Functions.choices import get_choices
from Utility.Functions.math_utility import energy_units
from Utility.Functions.files import resource_path, open_file
from Utility.Functions.gui_utility import make_vertical_frame
from Utility.Functions.gui_utility import make_spacer, get_width
from App.Dose.Electrons.electrons_export import electrons_export
from Utility.Functions.gui_utility import unit_dropdown, get_unit
from Core.Dose.Electrons.electrons_calculations import sp_denominator
from Utility.Functions.gui_utility import make_title_frame, basic_label
from Utility.Functions.gui_utility import interaction_checkbox, get_interactions
from Utility.Functions.math_utility import density_numerator, density_denominator
from Core.Dose.Electrons.electrons_calculations import sp_e_numerator, sp_l_numerator
from Utility.Functions.gui_utility import make_action_dropdown, make_customize_category_dropdown

# For global access to nodes on electron stopping power advanced screen
advanced_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the electron stopping power advanced screen.
The following sections and widgets are created:
   Module Title (Electron Stopping Power)
   Customize Categories section
   Select Units section
   Export Menu button
   References button
   Help button
   Back button
This function contains all of the logic involving these widgets'
behaviors.
The sections and widgets are stored in advanced_list so they can be
accessed later by clear_advanced.
"""
def electrons_advanced(root, category, mode, interactions, common_el,
                       common_mat, element, material, custom_mat,
                       sp_num, d_num, sp_den, d_den, energy_unit):
    global advanced_list

    # Makes title frame
    title_frame = make_title_frame(root, "Electron Stopping Power", "Dose/Electrons")

    # Gets common and non-common elements
    elements = get_choices("All Elements", "Dose", "Electrons")
    common = get_choices("Common Elements", "Dose", "Electrons")
    non_common = [element for element in elements if element not in common]

    # Gets common and non-common materials
    materials = get_choices("All Materials", "Dose", "Electrons")
    common_m = get_choices("Common Materials", "Dose", "Electrons")
    non_common_m = [material for material in materials if material not in common_m]

    # Gets custom materials
    custom = get_choices("Custom Materials", "Dose", "Electrons")

    # Frame for add/remove settings
    a_r_frame = SectionFrame(root, title="Customize Categories")
    a_r_frame.pack()
    inner_a_r_frame = a_r_frame.get_inner_frame()

    # Horizontal frame for add/remove settings
    side_frame = tk.Frame(inner_a_r_frame, bg="#F2F2F2")
    side_frame.pack(pady=(15, 5))

    # Action button
    a_r_button = [ttk.Button()]

    # List of interactions
    interaction_choices = ["Stopping Power - Total",
                           "Stopping Power - Collision",
                           "Stopping Power - Radiative"]

    # Variables for each interaction type
    var0 = tk.IntVar()
    var1 = tk.IntVar()
    var2 = tk.IntVar()
    interaction_vars = [var0, var1, var2]

    # Selects the previously selected interactions
    for i in range(len(interaction_choices)):
        if interaction_choices[i] in interactions:
            interaction_vars[i].set(1)

    # Simplifies calls to make_vertical_frame
    def make_v_frame():
        to_custom = lambda: to_custom_menu(root, category, mode,
                            get_interactions(interaction_choices, interaction_vars),
                                           common_el, common_mat,
                                           element, material, custom_mat,
                                           num_e_units[0] + " * " + num_l_units[0],
                                           num_e_units[3], den_units[0], den_units[3],
                                           energy_unit)
        return make_vertical_frame(root, inner_a_r_frame, var_action.get(),
                                   var_customize_category.get(), non_common, common,
                                   non_common_m, common_m, custom, a_r_button,
                                   to_custom)

    # Logic for when an action or category is selected
    def on_select_options(event):
        nonlocal vertical_frame
        event.widget.selection_clear()
        root.focus()
        vertical_frame.destroy()
        vertical_frame = make_v_frame()

    # Frame for action selection
    action_frame = tk.Frame(side_frame, bg="#F2F2F2")
    action_frame.pack(side="left", padx=5)

    # Action label
    basic_label(action_frame, "Action:")

    # Stores action and sets default
    var_action = tk.StringVar(root)
    var_action.set("Add")

    # Creates dropdown menu for action
    _ = make_action_dropdown(action_frame, var_action, on_select_options)

    # Frame for category selection
    category_frame = tk.Frame(side_frame, bg="#F2F2F2")
    category_frame.pack(side="left", padx=5)

    # Category label
    basic_label(category_frame, "Category:")

    # Stores customize category and sets default
    var_customize_category = tk.StringVar(root)
    var_customize_category.set("Common Elements")

    # Creates dropdown menu for customize category
    _ = make_customize_category_dropdown(category_frame, var_customize_category, on_select_options)

    # Stores updatable units
    num_e_units = [sp_num.split(" ", 1)[0], "", "", d_num]
    num_l_units = [sp_num.split(" ", 2)[2], "", "", d_num]
    den_units = [sp_den, "", "", d_den]

    # Frame for specific add/remove settings
    vertical_frame = make_v_frame()

    # Spacer
    empty_frame1 = make_spacer(root)

    # Frame for interaction type
    interactions_frame = SectionFrame(root, title="Select Interaction Types")
    inner_interactions_frame = interactions_frame.get_inner_frame()
    inner_interactions_frame.config(pady=10)

    # Spacer
    empty_frame2 = tk.Frame()

    # Ensures at least one interaction type is selected
    # If user tries to select none,
    # Stopping Power - Total
    # is automatically selected
    def set_default():
        safe = False
        for var in interaction_vars:
            if var.get() == 1:
                safe = True
        if not safe:
            var0.set(1)

    # Logic for when Stopping Power - Total is selected
    def on_select_total():
        root.focus()
        if var0.get() == 1:
            for var in interaction_vars:
                if var != var0:
                    var.set(0)
        else:
            set_default()

    # Logic for when any other interaction is selected
    def on_select(var):
        root.focus()
        if var.get() == 1:
            var0.set(0)
        else:
            set_default()

    # Select Interaction Types section is only created if
    # Calculation Mode is Stopping Power
    if mode == "Stopping Power":
        interactions_frame.pack()

        checks = tk.Frame(inner_interactions_frame, bg="#F2F2F2")
        checks.pack()

        # Checkboxes for each interaction type
        interaction_checkbox(checks, var0, "Stopping Power - Total",
                             on_select_total)
        interaction_checkbox(checks, var1, "Stopping Power - Collision",
                             lambda: on_select(var1))
        interaction_checkbox(checks, var2, "Stopping Power - Radiative",
                             lambda: on_select(var2))

        # Spacer
        empty_frame2 = make_spacer(root)

    # Frame for units
    unit_frame = SectionFrame(root, title="Select Units")
    unit_frame.pack()
    inner_unit_frame = unit_frame.get_inner_frame()

    if mode != "Radiation Yield" and mode != "Density Effect Delta":
        # Horizontal frame for unit settings
        unit_side_frame = tk.Frame(inner_unit_frame, bg="#F2F2F2")
        unit_side_frame.pack(pady=(20,0) if mode != "Density" else 20)

        # Units label
        unit_label = ttk.Label(unit_side_frame, text=mode + " Units:", style="Black.TLabel")
        unit_label.pack(side='left', padx=5)

        # Logic for when a unit is selected
        def get_select_unit(units):
            def on_select_unit(event):
                event.widget.selection_clear()
                root.focus()
                if mode == "Stopping Power":
                    units[0] = event.widget.get()
                elif mode == "Density":
                    units[3] = event.widget.get()
            return on_select_unit
        on_select_e_num = get_select_unit(num_e_units)
        on_select_l_num = get_select_unit(num_l_units)
        on_select_den = get_select_unit(den_units)

        # Mode choices
        mode_choices = ["Stopping Power",
                        "Radiation Yield",
                        "Density Effect Delta",
                        "Density"]

        # Possible unit choices
        num_e_choices = [sp_e_numerator, [], [], density_numerator]
        num_l_choices = [sp_l_numerator, [], [], density_numerator]
        den_choices = [sp_denominator, [], [], density_denominator]

        # Creates dropdown menu for numerator unit
        numerator_e_choices = list(get_unit(num_e_choices, mode_choices, mode).keys())
        unit_dropdown(unit_side_frame, numerator_e_choices,
                      get_unit(num_e_units, mode_choices, mode), on_select_e_num)

        if mode == "Stopping Power":
            # * label
            slash_label = ttk.Label(unit_side_frame, text="*", style="Black.TLabel")
            slash_label.pack(side='left')

            # Creates dropdown menu for numerator unit
            numerator_l_choices = list(get_unit(num_l_choices, mode_choices, mode).keys())
            unit_dropdown(unit_side_frame, numerator_l_choices,
                          get_unit(num_l_units, mode_choices, mode), on_select_l_num)

        # / label
        slash_label = ttk.Label(unit_side_frame, text="/", style="Black.TLabel")
        slash_label.pack(side='left')

        # Creates dropdown menu for denominator unit
        denominator_choices = list(get_unit(den_choices, mode_choices, mode).keys())
        unit_dropdown(unit_side_frame, denominator_choices,
                      get_unit(den_units, mode_choices, mode), on_select_den)

    # Spacer
    empty_frame3 = make_spacer(root)

    # Frame for Export Menu, References, & Help
    bottom_frame = tk.Frame(root, bg="#F2F2F2")
    bottom_frame.pack(pady=5)

    # Energy Unit options are only created if
    # Calculation Mode is not Density
    if mode != "Density":
        # Horizontal frame for energy unit settings
        energy_unit_side_frame = tk.Frame(inner_unit_frame, bg="#F2F2F2")
        energy_unit_side_frame.pack(pady=20)

        # Energy unit label
        energy_unit_label = ttk.Label(energy_unit_side_frame, text="Energy Unit:",
                                      style="Black.TLabel")
        energy_unit_label.pack(side='left', padx=5)

        # Logic for when an energy unit is selected
        def on_select_energy(event):
            nonlocal energy_unit
            event.widget.selection_clear()
            root.focus()
            energy_unit = event.widget.get()

        # Creates dropdown menu for energy unit
        energy_choices = list(energy_units.keys())
        unit_dropdown(energy_unit_side_frame, energy_choices,
                      energy_unit, on_select_energy)

        # Creates Export Menu button
        export_button = ttk.Button(bottom_frame, text="Export Menu", style="Maize.TButton",
                                   padding=(0,0),
                                   command=lambda:
                                   to_export_menu(root, category, mode,
                            get_interactions(interaction_choices, interaction_vars),
                                                  common_el, common_mat,
                                                  element, material, custom_mat,
                                                  num_e_units[0] + " * " + num_l_units[0],
                                                  num_e_units[3], den_units[0], den_units[3],
                                                  energy_unit))
        export_button.config(width=get_width(["Export Menu"]))
        export_button.pack(side='left', padx=5)

    # Creates References button
    references_button = ttk.Button(bottom_frame, text="References", style="Maize.TButton",
                                   padding=(0,0),
                                   command=lambda: open_ref(root))
    references_button.config(width=get_width(["References"]))
    references_button.pack(side='left', padx=5)

    # Creates Help button
    help_button = ttk.Button(bottom_frame, text="Help", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: open_help(root))
    help_button.config(width=get_width(["Help"]))
    help_button.pack(side='left', padx=5)

    # Creates Back button to return to electron stopping power main screen
    back_button = ttk.Button(root, text="Back", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: to_main(root, category, mode,
                             get_interactions(interaction_choices, interaction_vars),
                                                     common_el, common_mat,
                                                     element, material, custom_mat,
                                                     num_e_units[0] + " * " + num_l_units[0],
                                                     num_e_units[3],
                                                     den_units[0], den_units[3],
                                                     energy_unit))
    back_button.config(width=get_width(["Back"]))
    back_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [title_frame,
                     a_r_frame, a_r_button[0], empty_frame1,
                     interactions_frame, empty_frame2,
                     unit_frame, empty_frame3,
                     bottom_frame, back_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the electron stopping power advanced screen
in preparation for opening a different screen.
"""
def clear_advanced():
    global advanced_list

    # Clears electron stopping power advanced screen
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()

"""
This function transitions from the electron stopping power advanced screen
to the electron stopping power main screen by first clearing the
electron stopping power advanced screen and then creating the
electron stopping power main screen.
It is called when the Back button is hit.
"""
def to_main(root, category, mode, interactions, common_el, common_mat,
            element, material, custom_mat, sp_num, d_num, sp_den,
            d_den, energy_unit):
    from App.Dose.Electrons.electrons_main import electrons_main

    clear_advanced()
    electrons_main(root, category, mode, interactions, common_el, common_mat,
                   element, material, custom_mat, sp_num, d_num, sp_den,
                   d_den, energy_unit)

"""
This function transitions from the electron stopping power advanced screen
to the add custom materials menu by first clearing the
electron stopping power advanced screen and then creating the
add custom materials menu.
It is called when the Add Custom Materials button is hit.
"""
def to_custom_menu(root, category, mode, interactions, common_el, common_mat,
                   element, material, custom_mat, sp_num, d_num, sp_den,
                   d_den, energy_unit):
    clear_advanced()
    back = lambda: electrons_advanced(root, category, mode, interactions, common_el,
                                      common_mat, element, material, custom_mat,
                                      sp_num, d_num, sp_den, d_den, energy_unit)
    add_custom_menu(root, d_num, d_den, back)

"""
This function transitions from the electron stopping power advanced screen
to the electron stopping power export screen by first clearing the
electron stopping power advanced screen and then creating the
electron stopping power export screen.
It is called when the Export Menu button is hit.
"""
def to_export_menu(root, category, mode, interactions, common_el, common_mat,
                   element, material, custom_mat, sp_num, d_num, sp_den,
                   d_den, energy_unit):
    clear_advanced()
    electrons_export(root, category, mode, interactions, common_el, common_mat,
                     element, material, custom_mat, sp_num, d_num, sp_den,
                     d_den, energy_unit)

"""
This function opens the electron stopping power References.txt file.
"""
def open_ref(root):
    root.focus()
    db_path = resource_path('Utility/Modules/Dose/Electrons/References.txt')
    open_file(db_path)

"""
This function opens the electron stopping power Help.txt file.
"""
def open_help(root):
    root.focus()
    db_path = resource_path('Utility/Modules/Dose/Electrons/Help.txt')
    open_file(db_path)