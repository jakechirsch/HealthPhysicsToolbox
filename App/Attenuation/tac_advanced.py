##### IMPORTS #####
from App.Attenuation.tac_add_remove_settings import *
from App.Attenuation.tac_add_custom import *
from App.Attenuation.tac_export_settings import *
from Core.Attenuation.tac_plots import *
from ttkwidgets.autocomplete import AutocompleteCombobox

# For global access to nodes on advanced screen
advanced_list = []

def tac_advanced(root, common_el, common_mat, element, material, custom_mat,
                 selection, mode, interaction_start, mac_num, d_num, lac_num,
                 mac_den, d_den, lac_den, energy_unit):
    global advanced_list

    # Gets common and non-common elements
    elements = get_choices("All Elements")
    common = get_choices("Common Elements")
    non_common = [element for element in elements if element not in common]

    # Gets common and non-common materials
    materials = get_choices("All Materials")
    common_m = get_choices("Common Materials")
    non_common_m = [material for material in materials if material not in common_m]

    # Gets custom materials
    custom = get_choices("Custom Materials")

    a_r_title = ttk.Label(root, text="Add & Remove", font=("Verdana", 16),
                          style="Maize.TLabel")
    a_r_title.pack(pady=5)

    # Frame for add/remove settings
    a_r_frame = Frame(root, bg="#00274C")
    a_r_frame.pack(pady=5)

    # Horizontal frame for add/remove settings
    side_frame = Frame(a_r_frame, bg="#00274C")
    side_frame.pack(pady=5)

    a_r_button = [ttk.Button()]

    def make_v_frame():
        v_frame = make_vertical_frame(root, a_r_frame, side_frame, action_dropdown.get(),
                            category_dropdown.get(), non_common, common,
                            non_common_m, common_m, custom, common_el, common_mat,
                            element, material, custom_mat, selection, mode,
                            interaction_start, num_units[0], num_units[1], num_units[2],
                            den_units[0], den_units[1], den_units[2], energy_unit, a_r_button)
        return v_frame

    def on_select_options(event):
        nonlocal vertical_frame
        event.widget.selection_clear()
        root.focus()
        vertical_frame.destroy()
        vertical_frame = make_v_frame()

    # Frame for action selection
    action_frame = Frame(side_frame, bg="#00274C")
    action_frame.pack(side="left", padx=5)

    action_label = ttk.Label(action_frame, text="Action:",
                             style="White.TLabel")
    action_label.pack()

    # Creates dropdown menu for action
    action_choices = ["Add", "Remove"]
    action_dropdown = ttk.Combobox(action_frame, values=action_choices, width=6, justify="center",
                                   state='readonly', style="Maize.TCombobox")
    action_dropdown.set("Add")
    action_dropdown.pack()
    action_dropdown.bind("<<ComboboxSelected>>", on_select_options)

    # Frame for category selection
    category_frame = Frame(side_frame, bg="#00274C")
    category_frame.pack(side="left", padx=5)

    category_label = ttk.Label(category_frame, text="Select Category:",
                               style="White.TLabel")
    category_label.pack()

    # Creates dropdown menu for category
    category_choices = ["Common Elements", "Common Materials", "Custom Materials"]
    category_dropdown = ttk.Combobox(category_frame, values=category_choices, width=13,
                                     justify="center", state='readonly', style="Maize.TCombobox")
    category_dropdown.set("Common Elements")
    category_dropdown.pack()
    category_dropdown.bind("<<ComboboxSelected>>", on_select_options)

    # Spacer
    empty_frame1 = make_spacer(root)

    interaction_title = ttk.Label(root, text="Interaction Type", font=("Verdana", 16),
                                  style="Maize.TLabel")

    # Frame for interaction type
    interaction_frame = Frame(root, bg="#00274C")

    # Spacer
    empty_frame2 = Frame()

    # Stores updatable units
    num_units = [mac_num, d_num, lac_num]
    den_units = [mac_den, d_den, lac_den]

    # Frame for specific add/remove settings
    vertical_frame = make_v_frame()

    def on_select(event):
        event.widget.selection_clear()
        root.focus()

    # Stores interaction and sets default
    var_interaction = StringVar(root)
    var_interaction.set(interaction_start)

    if mode != "Density":
        interaction_title.pack(pady=5)
        interaction_frame.pack(pady=5)

        interaction_label = ttk.Label(interaction_frame, text="Select Interaction:",
                                      style="White.TLabel")
        interaction_label.pack()
        # Creates dropdown menu for mode
        interaction_choices = ["Total Attenuation with Coherent Scattering",
                               "Total Attenuation without Coherent Scattering",
                               "Pair Production in Electron Field",
                               "Pair Production in Nuclear Field",
                               "Scattering - Incoherent",
                               "Scattering - Coherent",
                               "Photo-Electric Absorption"]
        interaction_dropdown = ttk.Combobox(interaction_frame, textvariable=var_interaction,
                                            values=interaction_choices, width=32,
                                            justify="center", state='readonly',
                                            style="Maize.TCombobox")
        interaction_dropdown.pack()
        interaction_dropdown.bind("<<ComboboxSelected>>", on_select)

        empty_frame2 = make_spacer(root)

    unit_title = ttk.Label(root, text=mode+" Units", font=("Verdana", 16),
                           style="Maize.TLabel")
    unit_title.pack(pady=5)

    # Frame for units
    unit_frame = Frame(root, bg="#00274C")
    unit_frame.pack(pady=5)

    # Units label
    unit_label = ttk.Label(unit_frame, text="Units:", style="White.TLabel")
    unit_label.pack(side='left', padx=5)

    on_select_num = get_select_unit(root, num_units, mode)
    on_select_den = get_select_unit(root, den_units, mode)
    def on_select_energy(event):
        nonlocal energy_unit
        event.widget.selection_clear()
        root.focus()
        energy_unit = event.widget.get()

    # Creates dropdown menu for numerator unit
    numerator_choices = get_unit_keys(mac_numerator, density_numerator,
                                      lac_numerator, mode)
    unit_dropdown(unit_frame, numerator_choices,
                  get_unit(mac_num, d_num, lac_num, mode), on_select_num)

    # / label
    slash_label = ttk.Label(unit_frame, text="/", style="White.TLabel")
    slash_label.pack(side='left')

    # Creates dropdown menu for denominator unit
    denominator_choices = get_unit_keys(mac_denominator, density_denominator,
                                        lac_denominator, mode)
    unit_dropdown(unit_frame, denominator_choices,
                  get_unit(mac_den, d_den, lac_den, mode), on_select_den)

    # Spacer
    empty_frame3 = make_spacer(root)

    energy_unit_title = ttk.Label(root, text="Energy Unit", font=("Verdana", 16),
                                  style="Maize.TLabel")

    # Frame for energy unit
    energy_unit_frame = Frame(root, bg="#00274C")

    export_button = Button()

    # Spacer
    empty_frame4 = Frame()

    export_title = ttk.Label(root, text="Export Options", font=("Verdana", 16),
                             style="Maize.TLabel")

    # Spacer
    empty_frame5 = Frame()

    if mode != "Density":
        energy_unit_title.pack(pady=5)
        energy_unit_frame.pack(pady=5)

        # Energy unit label
        energy_unit_label = ttk.Label(energy_unit_frame, text="Energy Unit:",
                                      style="White.TLabel")
        energy_unit_label.pack(side='left', padx=5)

        # Creates dropdown menu for denominator unit
        energy_choices = list(energy_units.keys())
        unit_dropdown(energy_unit_frame, energy_choices,
                      energy_unit, on_select_energy)

        empty_frame4 = make_spacer(root)

        export_title.pack(pady=5)

        # Creates export button
        export_button = ttk.Button(root, text="Export Menu", style="Maize.TButton",
                                   padding=(0,0),
                                   command=lambda:
                                   to_export_menu(root, common_el, common_mat, element, material,
                                                  custom_mat, selection, mode, var_interaction.get(),
                                                  num_units[0], num_units[1], num_units[2],
                                                  den_units[0], den_units[1], den_units[2],
                                                  energy_unit))
        export_button.pack(pady=5)

        empty_frame5 = make_spacer(root)

    # Frame for references & help
    bottom_frame = Frame(root, bg="#00274C")
    bottom_frame.pack(pady=5)

    # Creates references button
    references_button = ttk.Button(bottom_frame, text="References", style="Maize.TButton",
                                   padding=(-10,0),
                                   command=lambda: open_file('Utility/Modules/Mass Attenuation/References.txt'))
    references_button.pack(side='left', padx=5)

    # Creates help button
    help_button = ttk.Button(bottom_frame, text="Help", style="Maize.TButton",
                             padding=(-20,0),
                             command=lambda: open_file('Utility/Modules/Mass Attenuation/Help.txt'))
    help_button.pack(side='left', padx=5)

    # Creates exit button to return to T.A.C. screen
    exit_button = ttk.Button(root, text="Back", style="Maize.TButton",
                             padding=(-20,0),
                             command=lambda: tac_back(root, pass_saved(common_el, common),
                                                      pass_saved(common_mat, common_m),
                                                      element, material,
                                                      pass_saved(custom_mat, custom),
                                                      selection, mode,
                                                      var_interaction.get(), num_units[0],
                                                      num_units[1], num_units[2], den_units[0],
                                                      den_units[1], den_units[2], energy_unit))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [a_r_title, a_r_frame, a_r_button[0], empty_frame1,
                     interaction_title, interaction_frame, empty_frame2,
                     unit_title, unit_frame, empty_frame3,
                     energy_unit_title, energy_unit_frame, empty_frame4,
                     export_title, export_button, empty_frame5,
                     bottom_frame, exit_button]

def make_vertical_frame(root, top_frame, side_frame, action, category,
                        non_common, common, non_common_m, common_m, custom,
                        common_el, common_mat, element, material, custom_mat,
                        selection, mode, interaction, mac_num, d_num, lac_num, mac_den,
                        d_den, lac_den, energy_unit, button
                        ):
    button[0].destroy()
    vertical_frame = Frame(side_frame, bg="#00274C")
    vertical_frame.pack(side='left', padx=5)

    if category != "Custom Materials" or action != "Add":
        item_label = ttk.Label(vertical_frame, text="Select Item:",
                          style="White.TLabel")
        item_label.pack()

    # Stores element and sets default
    var = StringVar(root)
    choices = []
    inverse = []
    width = 5
    if action == "Add" and category == "Common Elements":
        var.set(non_common[0] if len(non_common) > 0 else "")
        choices = non_common
        inverse = common
    elif action == "Add" and category == "Common Materials":
        var.set(non_common_m[0] if len(non_common_m) > 0 else "")
        choices = non_common_m
        inverse = common_m
        width = 35
    elif action == "Remove" and category == "Common Elements":
        var.set(common[0] if len(common) > 0 else "")
        choices = common
        inverse = non_common
    elif action == "Remove" and category == "Common Materials":
        var.set(common_m[0] if len(common_m) > 0 else "")
        choices = common_m
        inverse = non_common_m
        width = 35
    elif action == "Remove" and category == "Custom Materials":
        var.set(custom[0] if len(custom) > 0 else "")
        choices = custom
        width = 35

    if action == "Add" and category == "Custom Materials":
        # Creates button
        button[0] = ttk.Button(top_frame, text="Add Custom Materials", style="Maize.TButton",
                               padding=(0,0),
                               command=lambda: to_custom_menu(root, common_el=common_el,
                                                              common_mat=common_mat,
                                                              element=element,
                                                              material=material,
                                                              custom_mat=custom_mat,
                                                              selection=selection, mode=mode,
                                                              interaction=interaction,
                                                              mac_num=mac_num, d_num=d_num,
                                                              lac_num=lac_num, mac_den=mac_den,
                                                              d_den=d_den, lac_den=lac_den,
                                                              energy_unit=energy_unit))
        button[0].pack(pady=5)
    else:
        def on_select(event):
            event.widget.selection_clear()
            root.focus()

        def on_enter(_):
            value = var.get()
            if value not in choices:
                var.set(choices[0] if len(choices) > 0 else "")
            else:
                # Move focus away from the combobox
                root.focus()

        dropdown = AutocompleteCombobox(vertical_frame, textvariable=var,
                                        completevalues=choices, width=width,
                                        justify="center", style="Maize.TCombobox")
        dropdown.pack()
        dropdown.bind('<Return>', on_enter)
        dropdown.bind("<<ComboboxSelected>>", on_select)
        dropdown.bind("<FocusOut>", on_enter)

        # Creates button
        if action == "Remove" and category == "Custom Materials":
            button[0] = ttk.Button(top_frame, text=action, style="Maize.TButton",
                                   padding=(-20,0),
                                   command=lambda: carry_action(action, category,
                                                                choices, [var.get()], var,
                                                                dropdown))
        else:
            button[0] = ttk.Button(top_frame, text=action, style="Maize.TButton",
                                   padding=(-20,0),
                                   command=lambda: carry_action(action, category,
                                                                choices, inverse, var,
                                                                dropdown))
        button[0].pack(pady=5)

    return vertical_frame

def pass_saved(saved, choices):
    return saved if saved in choices else choices[0] if len(choices) > 0 else ""

def tac_back(root, common_el, common_mat, element, material, custom_mat,
             selection, mode, interaction, mac_num, d_num, lac_num,
             mac_den, d_den, lac_den, energy_unit):
    from App.Attenuation.tac_main import total_attenuation_coefficient

    clear_advanced()
    total_attenuation_coefficient(root, selection_start=selection, mode_start=mode,
                                  interaction=interaction, common_el=common_el,
                                  common_mat=common_mat, element=element, material=material,
                                  custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                                  lac_num=lac_num, mac_den=mac_den, d_den=d_den,
                                  lac_den=lac_den, energy_unit=energy_unit)

def clear_advanced():
    global advanced_list

    # Clears advanced screen
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()

def to_custom_menu(root, common_el, common_mat, element, material, custom_mat,
                   selection, mode, interaction, mac_num, d_num, lac_num, mac_den,
                   d_den, lac_den, energy_unit):
    clear_advanced()
    custom_menu(root, common_el, common_mat, element, material, custom_mat,
                selection, mode, interaction, mac_num, d_num, lac_num, mac_den,
                d_den, lac_den, energy_unit)

def to_export_menu(root, common_el, common_mat, element, material, custom_mat,
                   selection, mode, interaction_start, mac_num, d_num, lac_num,
                   mac_den, d_den, lac_den, energy_unit):
    clear_advanced()
    export_menu(root, common_el, common_mat, element, material, custom_mat,
                selection, mode, interaction_start, mac_num, d_num, lac_num,
                mac_den, d_den, lac_den, energy_unit)