##### IMPORTS #####
from App.Shielding.Photons.photons_add_custom import *
from App.Shielding.Photons.photons_export import *

# For global access to nodes on photon attenuation advanced screen
advanced_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the photon attenuation advanced screen.
The following sections and widgets are created:
   Module Title (Photon Attenuation)
   Customize Categories section
   Select Interaction Types section (only when Calculation Mode is not Density)
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
def photons_advanced(root, category, mode, interactions_start, common_el, common_mat,
                     element, material, custom_mat, mac_num, d_num, lac_num,
                     mac_den, d_den, lac_den, energy_unit):
    global advanced_list

    # Makes title frame
    title_frame = make_title_frame(root, "Photon Attenuation")

    # Gets common and non-common elements
    elements = get_choices("All Elements", "Photons")
    common = get_choices("Common Elements", "Photons")
    non_common = [element for element in elements if element not in common]

    # Gets common and non-common materials
    materials = get_choices("All Materials", "Photons")
    common_m = get_choices("Common Materials", "Photons")
    non_common_m = [material for material in materials if material not in common_m]

    # Gets custom materials
    custom = get_choices("Custom Materials", "Photons")

    # Frame for add/remove settings
    a_r_frame = SectionFrame(root, title="Customize Categories")
    a_r_frame.pack()
    inner_a_r_frame = a_r_frame.get_inner_frame()

    # Horizontal frame for add/remove settings
    side_frame = Frame(inner_a_r_frame, bg="#F2F2F2")
    side_frame.pack(pady=(15,5))

    # Action button
    a_r_button = [ttk.Button()]

    # List of interactions
    interaction_choices = ["Total Attenuation with Coherent Scattering",
                           "Total Attenuation without Coherent Scattering",
                           "Pair Production in Electron Field",
                           "Pair Production in Nuclear Field",
                           "Scattering - Incoherent",
                           "Scattering - Coherent",
                           "Photo-Electric Absorption"]

    # Variables for each interaction type
    var0 = IntVar()
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    interaction_vars = [var0, var1, var2, var3, var4, var5, var6]

    # Selects the previously selected interactions
    for i in range(len(interaction_choices)):
        if interaction_choices[i] in interactions_start:
            interaction_vars[i].set(1)

    # Simplifies calls to make_vertical_frame
    def make_v_frame():
        to_custom = lambda: to_custom_menu(root, category, mode,
                                get_interactions(interaction_choices, interaction_vars),
                                           common_el, common_mat,
                                           element, material, custom_mat,
                                    num_units[0], num_units[1], num_units[2],
                                    den_units[0], den_units[1], den_units[2],
                                           energy_unit)
        return make_vertical_frame(root, inner_a_r_frame, action_dropdown.get(),
                                   category_dropdown.get(), non_common, common,
                                   non_common_m, common_m, custom, a_r_button,
                                   to_custom, "Shielding/Photons")

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
    num_units = [mac_num, d_num, lac_num]
    den_units = [mac_den, d_den, lac_den]

    # Frame for specific add/remove settings
    vertical_frame = make_v_frame()

    # Spacer
    empty_frame1 = make_spacer(root)

    # Frame for interaction type
    interactions_frame = SectionFrame(root, title="Select Interaction Types")
    inner_interactions_frame = interactions_frame.get_inner_frame()
    inner_interactions_frame.config(pady=10)

    # Spacer
    empty_frame2 = Frame()

    # Ensures at least one interaction type is selected
    # If user tries to select none,
    # Total Attenuation with Coherent Scattering
    # is automatically selected
    def set_default():
        safe = False
        for var in interaction_vars:
            if var.get() == 1:
                safe = True
        if not safe:
            var0.set(1)

    # Logic for when Total Attenuation with Coherent Scattering is selected
    def on_select_total_with():
        root.focus()
        if var0.get() == 1:
            for var in interaction_vars:
                if var != var0:
                    var.set(0)
        else:
            set_default()

    # Logic for when Total Attenuation without Coherent Scattering is selected
    def on_select_total_without():
        root.focus()
        if var1.get() == 1:
            for var in interaction_vars:
                if var != var1 and var != var5:
                    var.set(0)
        else:
            set_default()

    # Logic for when Scattering - Coherent is selected
    def on_select_coherent_scattering():
        root.focus()
        if var5.get() == 1:
            var0.set(0)
        else:
            set_default()

    # Logic for when any other interaction is selected
    def on_select(var):
        root.focus()
        if var.get() == 1:
            var0.set(0)
            var1.set(0)
        else:
            set_default()

    # Select Interaction Types section is only created if
    # Calculation Mode is not Density
    if mode != "Density":
        interactions_frame.pack()

        checks = Frame(inner_interactions_frame, bg="#F2F2F2")
        checks.pack()

        # Checkboxes for each interaction type
        interaction_checkbox(checks, var0,
                             "Total Attenuation with Coherent Scattering",
                             on_select_total_with)
        interaction_checkbox(checks, var1,
                             "Total Attenuation without Coherent Scattering",
                             on_select_total_without)
        interaction_checkbox(checks, var2,
                             "Pair Production in Electron Field", lambda: on_select(var2))
        interaction_checkbox(checks, var3,
                             "Pair Production in Nuclear Field", lambda: on_select(var3))
        interaction_checkbox(checks, var4,
                             "Scattering - Incoherent", lambda: on_select(var4))
        interaction_checkbox(checks, var5,
                             "Scattering - Coherent", on_select_coherent_scattering)
        interaction_checkbox(checks, var6,
                             "Photo-Electric Absorption", lambda: on_select(var6))

        # Spacer
        empty_frame2 = make_spacer(root)

    # Frame for units
    unit_frame = SectionFrame(root, title="Select Units")
    unit_frame.pack()
    inner_unit_frame = unit_frame.get_inner_frame()

    # Horizontal frame for unit settings
    unit_side_frame = Frame(inner_unit_frame, bg="#F2F2F2")
    unit_side_frame.pack(pady=20)

    # Units label
    unit_label = ttk.Label(unit_side_frame, text=mode+" Units:", style="Black.TLabel")
    unit_label.pack(side='left', padx=5)

    # Logic for when a unit is selected
    def get_select_unit(units):
        def on_select_unit(event):
            event.widget.selection_clear()
            root.focus()
            if mode == "Mass Attenuation Coefficient":
                units[0] = event.widget.get()
            elif mode == "Density":
                units[1] = event.widget.get()
            else:
                units[2] = event.widget.get()
        return on_select_unit
    on_select_num = get_select_unit(num_units)
    on_select_den = get_select_unit(den_units)

    # Mode choices
    mode_choices = ["Mass Attenuation Coefficient",
                    "Density",
                    "Linear Attenuation Coefficient"]

    # Possible unit choices
    num_choices = [mac_numerator, density_numerator, lac_numerator]
    den_choices = [mac_denominator, density_denominator, lac_denominator]

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
    empty_frame3 = make_spacer(root)

    # Frame for Export Menu, References, & Help
    bottom_frame = Frame(root, bg="#F2F2F2")
    bottom_frame.pack(pady=5)

    # Energy Unit options are only created if
    # Calculation Mode is not Density
    if mode != "Density":
        # Horizontal frame for energy unit settings
        energy_unit_side_frame = Frame(inner_unit_frame, bg="#F2F2F2")
        energy_unit_side_frame.pack(pady=(0, 20))

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
                                   get_interactions(interaction_choices, interaction_vars),
                                                  common_el, common_mat, element, material,
                                                  custom_mat,
                                                  num_units[0], num_units[1], num_units[2],
                                                  den_units[0], den_units[1], den_units[2],
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

    # Creates Back button to return to photon attenuation main screen
    back_button = ttk.Button(root, text="Back", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: to_main(root, category, mode,
                            get_interactions(interaction_choices, interaction_vars),
                                                     valid_saved(common_el, common),
                                                     valid_saved(common_mat, common_m),
                                                     element, material,
                                                     valid_saved(custom_mat, custom),
                                                num_units[0], num_units[1], num_units[2],
                                                den_units[0], den_units[1], den_units[2],
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
This function clears the photon attenuation advanced screen
in preparation for opening a different screen.
"""
def clear_advanced():
    global advanced_list

    # Clears photon attenuation advanced screen
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()

"""
This function transitions from the photon attenuation advanced screen
to the photon attenuation main screen by first clearing the
photon attenuation advanced screen and then creating the
photon attenuation main screen.
It is called when the Back button is hit.
"""
def to_main(root, category, mode, interactions, common_el, common_mat,
            element, material, custom_mat, mac_num, d_num, lac_num,
            mac_den, d_den, lac_den, energy_unit):
    from App.Shielding.Photons.photons_main import photons_main

    clear_advanced()
    photons_main(root, category, mode, interactions, common_el, common_mat,
                 element, material, custom_mat, mac_num, d_num, lac_num,
                 mac_den, d_den, lac_den, energy_unit)

"""
This function transitions from the photon attenuation advanced screen
to the photon attenuation add custom screen by first clearing the
photon attenuation advanced screen and then creating the
photon attenuation add custom screen.
It is called when the Add Custom Materials button is hit.
"""
def to_custom_menu(root, category, mode, interactions, common_el, common_mat,
                   element, material, custom_mat, mac_num, d_num, lac_num,
                   mac_den, d_den, lac_den, energy_unit):
    clear_advanced()
    photons_add_custom(root, category, mode, interactions, common_el, common_mat,
                       element, material, custom_mat, mac_num, d_num, lac_num,
                       mac_den, d_den, lac_den, energy_unit)

"""
This function transitions from the photon attenuation advanced screen
to the photon attenuation export screen by first clearing the
photon attenuation advanced screen and then creating the
photon attenuation export screen.
It is called when the Export Menu button is hit.
"""
def to_export_menu(root, category, mode, interactions, common_el, common_mat,
                   element, material, custom_mat, mac_num, d_num, lac_num,
                   mac_den, d_den, lac_den, energy_unit):
    clear_advanced()
    photons_export(root, category, mode, interactions, common_el, common_mat,
                   element, material, custom_mat, mac_num, d_num, lac_num,
                   mac_den, d_den, lac_den, energy_unit)

"""
This function opens the photon attenuation References.txt file.
"""
def open_ref(root):
    root.focus()
    db_path = resource_path('Utility/Modules/Shielding/Photons/References.txt')
    open_file(db_path)

"""
This function opens the photon attenuation Help.txt file.
"""
def open_help(root):
    root.focus()
    db_path = resource_path('Utility/Modules/Shielding/Photons/Help.txt')
    open_file(db_path)