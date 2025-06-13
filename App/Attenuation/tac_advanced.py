##### IMPORTS #####
from App.Attenuation.tac_choices import *
from App.Attenuation.tac_unit_settings import *
from App.Attenuation.tac_add_remove_settings import *
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

    # Frame for add/remove settings
    top_frame = Frame(root)
    top_frame.pack(pady=5)

    def on_select_options(event):
        nonlocal vertical_frame
        event.widget.selection_clear()
        root.focus()
        vertical_frame.destroy()
        vertical_frame = Frame(top_frame)
        vertical_frame.pack(side='left', padx=5)
        make_vertical_frame(root, vertical_frame, action_dropdown.get(),
                            category_dropdown.get(), non_common, common,
                            non_common_m, common_m, custom)

    # Creates dropdown menu for action
    action_choices = ["Add", "Remove"]
    action_dropdown = Combobox(top_frame, values=action_choices, width=6, state='readonly')
    action_dropdown.set("Add")
    action_dropdown.pack(side='left', padx=5)
    action_dropdown.bind("<<ComboboxSelected>>", on_select_options)

    # Creates dropdown menu for category
    category_choices = ["Common Elements", "Common Materials", "Custom Materials"]
    category_dropdown = Combobox(top_frame, values=category_choices, width=13, state='readonly')
    category_dropdown.set("Common Elements")
    category_dropdown.pack(side='left', padx=5)
    category_dropdown.bind("<<ComboboxSelected>>", on_select_options)

    # Frame for specific add/remove settings
    vertical_frame = Frame(top_frame)
    vertical_frame.pack(side='left', padx=5)
    make_vertical_frame(root, vertical_frame, action_dropdown.get(),
                        category_dropdown.get(), non_common, common,
                        non_common_m, common_m, custom)

    def on_select(event):
        event.widget.selection_clear()
        root.focus()

    interaction_dropdown = Combobox()

    # Stores interaction and sets default
    var_interaction = StringVar(root)
    var_interaction.set(interaction_start)

    if mode != "Density":
        # Creates dropdown menu for mode
        interaction_choices = ["Total Attenuation with Coherent Scattering",
                               "Total Attenuation without Coherent Scattering",
                               "Pair Production in Electron Field",
                               "Pair Production in Nuclear Field",
                               "Scattering - Incoherent",
                               "Scattering - Coherent",
                               "Photo-Electric Absorption"]
        interaction_dropdown = Combobox(root, textvariable=var_interaction,
                                        values=interaction_choices, width=32, state='readonly')
        interaction_dropdown.pack(pady=10)
        interaction_dropdown.bind("<<ComboboxSelected>>", on_select)

    # Frame for units
    unit_frame = Frame(root)
    unit_frame.pack(pady=5)

    # Units label
    unit_label = Label(unit_frame, text="Units:")
    unit_label.pack(side='left', padx=5)

    num_units = [mac_num, d_num, lac_num]
    den_units = [mac_den, d_den, lac_den]
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
    slash_label = Label(unit_frame, text="/")
    slash_label.pack(side='left')

    # Creates dropdown menu for denominator unit
    denominator_choices = get_unit_keys(mac_denominator, density_denominator,
                                        lac_denominator, mode)
    unit_dropdown(unit_frame, denominator_choices,
                  get_unit(mac_den, d_den, lac_den, mode), on_select_den)

    # Frame for units
    energy_unit_frame = Frame(root)
    energy_unit_frame.pack(pady=5 if mode != "Density" else 0)

    # Frame for export options
    export_frame = Frame(root)
    export_frame.pack(pady=5 if mode != "Density" else 0)

    if mode != "Density":
        # Energy unit label
        unit_label = Label(energy_unit_frame, text="Energy Unit:")
        unit_label.pack(side='left', padx=5)

        # Creates dropdown menu for denominator unit
        energy_choices = list(energy_units.keys())
        unit_dropdown(energy_unit_frame, energy_choices,
                      energy_unit, on_select_energy)

        export_label = Label(export_frame, text="Export Options:")
        export_label.pack(side="left", padx=5)

        # Creates dropdown menu for export
        export_choices = ["Plot", "Data"]
        export_dropdown = Combobox(export_frame, values=export_choices, width=6, state='readonly')
        export_dropdown.set("Plot")
        export_dropdown.pack(side="left", padx=5)
        export_dropdown.bind("<<ComboboxSelected>>", on_select)

        # Creates export button
        export_button = Button(export_frame, text="Export",
                               command=lambda:
                               plot_data(common_el if selection == "Common Elements" else
                                         common_mat if selection == "Common Materials" else
                                         element if selection == "All Elements" else
                                         material if selection == "All Materials" else
                                         custom_mat if selection == "Custom Materials"
                                         else "", selection, mode, var_interaction.get(),
                                         get_unit(num_units[0], num_units[1],
                                                  num_units[2], mode),
                                         get_unit(den_units[0], den_units[1],
                                                  den_units[2], mode),
                                         energy_unit, export_dropdown.get()))
        export_button.pack(side="left", padx=5)

    # Frame for references & help
    bottom_frame = Frame(root)
    bottom_frame.pack(pady=2)

    # Creates references button
    references_button = Button(bottom_frame, text="References",
                               command=lambda: open_file('Utility/Modules/Mass Attenuation/References.txt'))
    references_button.pack(side='left', padx=5)

    # Creates help button
    help_button = Button(bottom_frame, text="Help",
                         command=lambda: open_file('Utility/Modules/Mass Attenuation/Help.txt'))
    help_button.pack(side='left', padx=5)

    # Creates exit button to return to T.A.C. screen
    exit_button = Button(root, text="Back",
                         command=lambda: tac_back(root, pass_saved(common_el, common),
                                                  pass_saved(common_mat, common_m),
                                                  element, material,
                                                  pass_saved(custom_mat, custom),
                                                  selection, mode,
                                                  var_interaction.get(), num_units[0],
                                                  num_units[1], num_units[2], den_units[0],
                                                  den_units[1], den_units[2], energy_unit))
    exit_button.pack(pady=2)

    # Stores nodes into global list
    advanced_list = [interaction_dropdown, exit_button, unit_frame,
                     energy_unit_frame, top_frame, bottom_frame,
                     export_frame]

def make_vertical_frame(root, vertical_frame, action, category,
                        non_common, common, non_common_m, common_m, custom):
    label = Label(vertical_frame,
                  text=action + " " + \
                       category + ":")
    label.pack()

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
        label = Label(vertical_frame, text="Material Name:")
        entry = Entry(vertical_frame, width=20)
        entry.config(bg='white', fg='grey')
        label.pack()
        entry.pack()
        label2 = Label(vertical_frame, text="Density")
        entry2 = Entry(vertical_frame, width=20)
        entry2.config(bg='white', fg='grey')
        label2.pack()
        entry2.pack()
        label3 = Label(vertical_frame, text='"Weight","Element"\\n')
        entry3 = Entry(vertical_frame, width=20)
        entry3.config(bg='white', fg='grey')
        label3.pack()
        entry3.pack()

        # Creates button
        button = Button(vertical_frame, text=action,
                        command=lambda: add_custom(root, entry, entry2, entry3))
        button.pack()
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
                                        completevalues=choices, width=width)
        dropdown.pack()
        dropdown.bind('<Return>', on_enter)
        dropdown.bind("<<ComboboxSelected>>", on_select)
        dropdown.bind("<FocusOut>", on_enter)

        # Creates button
        if action == "Remove" and category == "Custom Materials":
            button = Button(vertical_frame, text=action,
                            command=lambda: carry_action(action, category,
                                                         choices, [var.get()], var, dropdown))
        else:
            button = Button(vertical_frame, text=action,
                            command=lambda: carry_action(action, category,
                                                         choices, inverse, var, dropdown))
        button.pack()

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

    # Clears advanced
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()