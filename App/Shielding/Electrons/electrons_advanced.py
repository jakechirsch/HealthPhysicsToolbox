##### IMPORTS #####
from App.add_custom_menu import *
from App.Shielding.Electrons.electrons_export import *

# For global access to nodes on electron range advanced screen
advanced_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the electron range advanced screen.
The following sections and widgets are created:
   Module Title (Electron Range)
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
def electrons_advanced(root, category, mode, common_el, common_mat, element,
                       material, custom_mat, csda_num, d_num, rec_num, csda_den, d_den,
                       rec_den, energy_unit):
    global advanced_list

    # Makes title frame
    title_frame = make_title_frame(root, "Electron Range", "Shielding/Electrons")

    # Gets common and non-common elements
    elements = get_choices("All Elements", "Electrons")
    common = get_choices("Common Elements", "Electrons")
    non_common = [element for element in elements if element not in common]

    # Gets common and non-common materials
    materials = get_choices("All Materials", "Electrons")
    common_m = get_choices("Common Materials", "Electrons")
    non_common_m = [material for material in materials if material not in common_m]

    # Gets custom materials
    custom = get_choices("Custom Materials", "Electrons")

    # Frame for add/remove settings
    a_r_frame = SectionFrame(root, title="Customize Categories")
    a_r_frame.pack()
    inner_a_r_frame = a_r_frame.get_inner_frame()

    # Horizontal frame for add/remove settings
    side_frame = Frame(inner_a_r_frame, bg="#F2F2F2")
    side_frame.pack(pady=(15, 5))

    # Action button
    a_r_button = [ttk.Button()]

    # Simplifies calls to make_vertical_frame
    def make_v_frame():
        to_custom = lambda: to_custom_menu(root, category, mode,
                                           common_el, common_mat,
                                           element, material, custom_mat,
                                           num_units[0], num_units[4], num_units[1],
                                           den_units[0], den_units[4], den_units[1],
                                           energy_unit)
        return make_vertical_frame(root, inner_a_r_frame, action_dropdown.get(),
                                   category_dropdown.get(), non_common, common,
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
    action_frame = Frame(side_frame, bg="#F2F2F2")
    action_frame.pack(side="left", padx=5)

    # Action label
    basic_label(action_frame, "Action:")

    # Creates dropdown menu for action
    action_choices = ["Add", "Remove"]
    action_dropdown = ttk.Combobox(action_frame, values=action_choices, justify="center",
                                   state='readonly', style="Maize.TCombobox")
    action_dropdown.config(width=get_width(action_choices))
    action_dropdown.set("Add")
    action_dropdown.pack()
    action_dropdown.bind("<<ComboboxSelected>>", on_select_options)

    # Frame for category selection
    category_frame = Frame(side_frame, bg="#F2F2F2")
    category_frame.pack(side="left", padx=5)

    # Category label
    basic_label(category_frame, "Category:")

    # Creates dropdown menu for category
    category_choices = ["Common Elements", "Common Materials", "Custom Materials"]
    category_dropdown = ttk.Combobox(category_frame, values=category_choices, justify="center",
                                     state='readonly', style="Maize.TCombobox")
    category_dropdown.config(width=get_width(category_choices))
    category_dropdown.set("Common Elements")
    category_dropdown.pack()
    category_dropdown.bind("<<ComboboxSelected>>", on_select_options)

    # Stores updatable units
    num_units = [csda_num, rec_num, "", "", d_num]
    den_units = [csda_den, rec_den, "", "", d_den]

    # Frame for specific add/remove settings
    vertical_frame = make_v_frame()

    # Spacer
    empty_frame1 = make_spacer(root)

    # Frame for units
    unit_frame = SectionFrame(root, title="Select Units")
    unit_frame.pack()
    inner_unit_frame = unit_frame.get_inner_frame()

    if mode != "Radiation Yield" and mode != "Density Effect Delta":
        # Horizontal frame for unit settings
        unit_side_frame = Frame(inner_unit_frame, bg="#F2F2F2")
        unit_side_frame.pack(pady=(20,0) if mode != "Density" else 20)

        # Units label
        unit_label = ttk.Label(unit_side_frame, text=mode + " Units:", style="Black.TLabel")
        unit_label.pack(side='left', padx=5)

        # Logic for when a unit is selected
        def get_select_unit(units):
            def on_select_unit(event):
                event.widget.selection_clear()
                root.focus()
                if mode == "CSDA Range":
                    units[0] = event.widget.get()
                elif mode == "Density":
                    units[4] = event.widget.get()
                elif mode == "Range-Energy Curve":
                    units[1] = event.widget.get()
            return on_select_unit
        on_select_num = get_select_unit(num_units)
        on_select_den = get_select_unit(den_units)

        # Mode choices
        mode_choices = ["CSDA Range",
                        "Range-Energy Curve",
                        "Radiation Yield",
                        "Density Effect Delta",
                        "Density"]

        # Possible unit choices
        num_choices = [csda_numerator, csda_numerator, [], [], density_numerator]
        den_choices = [csda_denominator, csda_denominator, [], [], density_denominator]

        # Creates dropdown menu for numerator unit
        numerator_choices = list(get_unit(num_choices, mode_choices, mode).keys())
        unit_dropdown(unit_side_frame, numerator_choices,
                      get_unit(num_units, mode_choices, mode), on_select_num)

        # / label
        slash_label = ttk.Label(unit_side_frame, text="/", style="Black.TLabel")
        slash_label.pack(side='left')

        # Creates dropdown menu for denominator unit
        denominator_choices = list(get_unit(den_choices, mode_choices, mode).keys())
        unit_dropdown(unit_side_frame, denominator_choices,
                      get_unit(den_units, mode_choices, mode), on_select_den)

    # Spacer
    empty_frame2 = make_spacer(root)

    # Frame for Export Menu, References, & Help
    bottom_frame = Frame(root, bg="#F2F2F2")
    bottom_frame.pack(pady=5)

    # Energy Unit options are only created if
    # Calculation Mode is not Density
    if mode != "Density":
        # Horizontal frame for energy unit settings
        energy_unit_side_frame = Frame(inner_unit_frame, bg="#F2F2F2")
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

        # Creates dropdown menu for denominator unit
        energy_choices = list(energy_units.keys())
        unit_dropdown(energy_unit_side_frame, energy_choices,
                      energy_unit, on_select_energy)

        # Creates Export Menu button
        export_button = ttk.Button(bottom_frame, text="Export Menu", style="Maize.TButton",
                                   padding=(0,0),
                                   command=lambda:
                                   to_export_menu(root, category, mode,
                                                  common_el, common_mat,
                                                  element, material, custom_mat,
                                                  num_units[0], num_units[4], num_units[1],
                                                  den_units[0], den_units[4], den_units[1],
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

    # Creates Back button to return to electron range main screen
    back_button = ttk.Button(root, text="Back", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: to_main(root, category, mode, common_el,
                                                     common_mat, element, material,
                                                     custom_mat,
                                                num_units[0], num_units[4], num_units[1],
                                                den_units[0], den_units[4], den_units[1],
                                                     energy_unit))
    back_button.config(width=get_width(["Back"]))
    back_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [title_frame,
                     a_r_frame, a_r_button[0], empty_frame1,
                     unit_frame, empty_frame2,
                     bottom_frame, back_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the electron range advanced screen
in preparation for opening a different screen.
"""
def clear_advanced():
    global advanced_list

    # Clears electron range advanced screen
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()

"""
This function transitions from the electron range advanced screen
to the electron range main screen by first clearing the
electron range advanced screen and then creating the
electron range main screen.
It is called when the Back button is hit.
"""
def to_main(root, category, mode, common_el, common_mat, element,
            material, custom_mat, csda_num, d_num, rec_num, csda_den, d_den, rec_den,
            energy_unit):
    from App.Shielding.Electrons.electrons_main import electrons_main

    clear_advanced()
    electrons_main(root, category, mode, common_el, common_mat, element,
                   material, custom_mat, csda_num, d_num, rec_num, csda_den, d_den,
                   rec_den, energy_unit)

"""
This function transitions from the electron range advanced screen
to the electron range add custom screen by first clearing the
electron range advanced screen and then creating the
electron range add custom screen.
It is called when the Add Custom Materials button is hit.
"""
def to_custom_menu(root, category, mode, common_el, common_mat, element,
                   material, custom_mat, csda_num, d_num, rec_num, csda_den, d_den,
                   rec_den, energy_unit):
    clear_advanced()
    back = lambda: electrons_advanced(root, category, mode, common_el, common_mat, element,
                                      material, custom_mat, csda_num, d_num, rec_num, csda_den,
                                      d_den, rec_den, energy_unit)
    add_custom_menu(root, d_num, d_den, back)

"""
This function transitions from the electron range advanced screen
to the electron range export screen by first clearing the
electron range advanced screen and then creating the
electron range export screen.
It is called when the Export Menu button is hit.
"""
def to_export_menu(root, category, mode, common_el, common_mat, element,
                   material, custom_mat, csda_num, d_num, rec_num, csda_den, d_den,
                   rec_den, energy_unit):
    clear_advanced()
    electrons_export(root, category, mode, common_el, common_mat, element,
                     material, custom_mat, csda_num, d_num, rec_num, csda_den, d_den,
                     rec_den, energy_unit)

"""
This function opens the electron range References.txt file.
"""
def open_ref(root):
    root.focus()
    db_path = resource_path('Utility/Modules/Shielding/Electrons/References.txt')
    open_file(db_path)

"""
This function opens the electron range Help.txt file.
"""
def open_help(root):
    root.focus()
    db_path = resource_path('Utility/Modules/Shielding/Electrons/Help.txt')
    open_file(db_path)