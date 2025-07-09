##### IMPORTS #####
from App.Attenuation.Photons.photons_add_remove_settings import *
from App.Attenuation.Photons.photons_add_custom import *
from App.Attenuation.Photons.photons_export_settings import *
from Core.Attenuation.Photons.photons_plots import *
from ttkwidgets.autocomplete import AutocompleteCombobox
from App.style import SectionFrame

# For global access to nodes on advanced screen
advanced_list = []

def photons_advanced(root, common_el, common_mat, element, material, custom_mat,
                     selection, mode, interactions_start, mac_num, d_num, lac_num,
                     mac_den, d_den, lac_den, energy_unit):
    global advanced_list

    title_frame = make_title_frame(root, "Photon Attenuation")

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
    a_r_frame = SectionFrame(root, title="Customize Categories")
    a_r_frame.pack()
    inner_a_r_frame = a_r_frame.get_inner_frame()

    # Horizontal frame for add/remove settings
    side_frame = Frame(inner_a_r_frame, bg="#F2F2F2")
    side_frame.pack(pady=(15,5))

    a_r_button = [ttk.Button()]

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

    for i in range(len(interaction_choices)):
        if interaction_choices[i] in interactions_start:
            interaction_vars[i].set(1)

    def make_v_frame():
        v_frame = make_vertical_frame(root, inner_a_r_frame, action_dropdown.get(),
                            category_dropdown.get(), non_common, common,
                            non_common_m, common_m, custom, common_el, common_mat,
                            element, material, custom_mat, selection, mode,
                            [interaction_choices[x] for x in range(len(interaction_choices))
                             if interaction_vars[x].get() == 1], num_units[0], num_units[1],
                            num_units[2], den_units[0], den_units[1], den_units[2],
                            energy_unit, a_r_button)
        return v_frame

    def on_select_options(event):
        nonlocal vertical_frame
        event.widget.selection_clear()
        root.focus()
        vertical_frame.destroy()
        vertical_frame = make_v_frame()

    # Frame for action selection
    action_frame = Frame(side_frame, bg="#F2F2F2")
    action_frame.pack(side="left", padx=5)

    action_label = ttk.Label(action_frame, text="Action:",
                             style="Black.TLabel")
    action_label.pack()

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

    category_label = ttk.Label(category_frame, text="Category:",
                               style="Black.TLabel")
    category_label.pack()

    # Creates dropdown menu for category
    category_choices = ["Common Elements", "Common Materials", "Custom Materials"]
    category_dropdown = ttk.Combobox(category_frame, values=category_choices, justify="center",
                                     state='readonly', style="Maize.TCombobox")
    category_dropdown.config(width=get_width(category_choices))
    category_dropdown.set("Common Elements")
    category_dropdown.pack()
    category_dropdown.bind("<<ComboboxSelected>>", on_select_options)

    # Spacer
    empty_frame1 = make_spacer(root)

    # Frame for interaction type
    interactions_frame = SectionFrame(root, title="Select Interaction Types")
    inner_interactions_frame = interactions_frame.get_inner_frame()
    inner_interactions_frame.config(pady=10)

    # Spacer
    empty_frame2 = Frame()

    # Stores updatable units
    num_units = [mac_num, d_num, lac_num]
    den_units = [mac_den, d_den, lac_den]

    # Frame for specific add/remove settings
    vertical_frame = make_v_frame()

    def set_default():
        safe = False
        for var in interaction_vars:
            if var.get() == 1:
                safe = True
        if not safe:
            var0.set(1)

    def on_select_total_with():
        root.focus()
        if var0.get() == 1:
            for var in interaction_vars:
                if var != var0:
                    var.set(0)
        else:
            set_default()

    def on_select_total_without():
        root.focus()
        if var1.get() == 1:
            for var in interaction_vars:
                if var != var1 and var != var5:
                    var.set(0)
        else:
            set_default()

    def on_select_coherent_scattering():
        root.focus()
        if var5.get() == 1:
            var0.set(0)
        else:
            set_default()

    def on_select(var):
        root.focus()
        if var.get() == 1:
            var0.set(0)
            var1.set(0)
        else:
            set_default()

    if mode != "Density":
        interactions_frame.pack()

        # Checkboxes for each interaction type
        interaction_checkbox(inner_interactions_frame, var0,
                             "Total Attenuation with Coherent Scattering",
                             on_select_total_with)
        interaction_checkbox(inner_interactions_frame, var1,
                             "Total Attenuation without Coherent Scattering",
                             on_select_total_without)
        interaction_checkbox(inner_interactions_frame, var2,
                             "Pair Production in Electron Field", lambda: on_select(var2))
        interaction_checkbox(inner_interactions_frame, var3,
                             "Pair Production in Nuclear Field", lambda: on_select(var3))
        interaction_checkbox(inner_interactions_frame, var4,
                             "Scattering - Incoherent", lambda: on_select(var4))
        interaction_checkbox(inner_interactions_frame, var5,
                             "Scattering - Coherent", on_select_coherent_scattering)
        interaction_checkbox(inner_interactions_frame, var6,
                             "Photo-Electric Absorption", lambda: on_select(var6))

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
    unit_dropdown(unit_side_frame, numerator_choices,
                  get_unit(mac_num, d_num, lac_num, mode), on_select_num)

    # / label
    slash_label = ttk.Label(unit_side_frame, text="/", style="Black.TLabel")
    slash_label.pack(side='left')

    # Creates dropdown menu for denominator unit
    denominator_choices = get_unit_keys(mac_denominator, density_denominator,
                                        lac_denominator, mode)
    unit_dropdown(unit_side_frame, denominator_choices,
                  get_unit(mac_den, d_den, lac_den, mode), on_select_den)

    # Spacer
    empty_frame3 = make_spacer(root)

    # Frame for export menu, references, & help
    bottom_frame = Frame(root, bg="#F2F2F2")
    bottom_frame.pack(pady=5)

    if mode != "Density":
        # Horizontal frame for energy unit settings
        energy_unit_side_frame = Frame(inner_unit_frame, bg="#F2F2F2")
        energy_unit_side_frame.pack(pady=(0, 20))

        # Energy unit label
        energy_unit_label = ttk.Label(energy_unit_side_frame, text="Energy Unit:",
                                      style="Black.TLabel")
        energy_unit_label.pack(side='left', padx=5)

        # Creates dropdown menu for denominator unit
        energy_choices = list(energy_units.keys())
        unit_dropdown(energy_unit_side_frame, energy_choices,
                      energy_unit, on_select_energy)

        # Creates export button
        export_button = ttk.Button(bottom_frame, text="Export Menu", style="Maize.TButton",
                                   padding=(0,0),
                                   command=lambda:
                                   to_export_menu(root, common_el, common_mat, element, material,
                                                  custom_mat, selection, mode,
                                                  [interaction_choices[x]
                                                   for x in range(len(interaction_choices))
                                                   if interaction_vars[x].get() == 1],
                                                  num_units[0], num_units[1], num_units[2],
                                                  den_units[0], den_units[1], den_units[2],
                                                  energy_unit))
        export_button.config(width=get_width(["Export Menu"]))
        export_button.pack(side='left', padx=5)

    # Creates references button
    references_button = ttk.Button(bottom_frame, text="References", style="Maize.TButton",
                                   padding=(0,0),
                                   command=lambda: open_ref(root))
    references_button.config(width=get_width(["References"]))
    references_button.pack(side='left', padx=5)

    # Creates help button
    help_button = ttk.Button(bottom_frame, text="Help", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: open_help(root))
    help_button.config(width=get_width(["Help"]))
    help_button.pack(side='left', padx=5)

    # Creates exit button to return to T.A.C. screen
    exit_button = ttk.Button(root, text="Back", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: to_main(root, pass_saved(common_el, common),
                                                     pass_saved(common_mat, common_m),
                                                     element, material,
                                                     pass_saved(custom_mat, custom),
                                                     selection, mode,
                                                     [interaction_choices[x]
                                                       for x in range(len(interaction_choices))
                                                       if interaction_vars[x].get() == 1],
                                                     num_units[0], num_units[1], num_units[2],
                                                     den_units[0], den_units[1], den_units[2],
                                                     energy_unit))
    exit_button.config(width=get_width(["Back"]))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [title_frame,
                     a_r_frame, a_r_button[0], empty_frame1,
                     interactions_frame, empty_frame2,
                     unit_frame, empty_frame3,
                     bottom_frame, exit_button]

def make_vertical_frame(root, top_frame, action, category,
                        non_common, common, non_common_m, common_m, custom,
                        common_el, common_mat, element, material, custom_mat,
                        selection, mode, interactions, mac_num, d_num, lac_num, mac_den,
                        d_den, lac_den, energy_unit, button):
    button[0].destroy()
    vertical_frame = Frame(top_frame, bg="#F2F2F2")
    vertical_frame.pack(pady=(5,20))

    if category != "Custom Materials" or action != "Add":
        item_label = ttk.Label(vertical_frame, text="Item:",
                          style="Black.TLabel")
        item_label.pack()

    # Stores element and sets default
    var = StringVar(root)
    choices = []
    inverse = []
    if action == "Add" and category == "Common Elements":
        var.set(non_common[0] if len(non_common) > 0 else "")
        choices = non_common
        inverse = common
    elif action == "Add" and category == "Common Materials":
        var.set(non_common_m[0] if len(non_common_m) > 0 else "")
        choices = non_common_m
        inverse = common_m
    elif action == "Remove" and category == "Common Elements":
        var.set(common[0] if len(common) > 0 else "")
        choices = common
        inverse = non_common
    elif action == "Remove" and category == "Common Materials":
        var.set(common_m[0] if len(common_m) > 0 else "")
        choices = common_m
        inverse = non_common_m
    elif action == "Remove" and category == "Custom Materials":
        var.set(custom[0] if len(custom) > 0 else "")
        choices = custom

    if action == "Add" and category == "Custom Materials":
        # Creates button
        button[0] = ttk.Button(vertical_frame, text="Add Custom Materials",
                               style="Maize.TButton", padding=(0,0),
                               command=lambda: to_custom_menu(root, common_el=common_el,
                                                              common_mat=common_mat,
                                                              element=element,
                                                              material=material,
                                                              custom_mat=custom_mat,
                                                              selection=selection, mode=mode,
                                                              interactions=interactions,
                                                              mac_num=mac_num, d_num=d_num,
                                                              lac_num=lac_num, mac_den=mac_den,
                                                              d_den=d_den, lac_den=lac_den,
                                                              energy_unit=energy_unit))
        button[0].config(width=get_width(["Add Custom Materials"]))
        button[0].pack(pady=(10,0))
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
                                        completevalues=choices, justify="center",
                                        style="Maize.TCombobox")
        dropdown.config(width=get_width(choices))
        dropdown.pack()
        dropdown.bind('<Return>', on_enter)
        dropdown.bind("<<ComboboxSelected>>", on_select)
        dropdown.bind("<FocusOut>", on_enter)

        # Creates button
        if action == "Remove" and category == "Custom Materials":
            inverse = [var.get()]
        button[0] = ttk.Button(vertical_frame, text=action,
                               style="Maize.TButton", padding=(0,0),
                               command=lambda: do_action(root, action, category,
                                                         choices, inverse, var,
                                                         dropdown))
        button[0].config(width=get_width([action]))
        button[0].pack(pady=(10,0))

    return vertical_frame

def pass_saved(saved, choices):
    return saved if saved in choices else choices[0] if len(choices) > 0 else ""

def to_main(root, common_el, common_mat, element, material, custom_mat,
            selection, mode, interactions, mac_num, d_num, lac_num,
            mac_den, d_den, lac_den, energy_unit):
    from App.Attenuation.Photons.photons_main import photons_main

    clear_advanced()
    photons_main(root, selection_start=selection, mode_start=mode,
                 interactions=interactions, common_el=common_el,
                 common_mat=common_mat, element=element, material=material,
                 custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                 lac_num=lac_num, mac_den=mac_den, d_den=d_den,
                 lac_den=lac_den, energy_unit=energy_unit)

"""
This function clears the photon attenuation advanced screen
in preparation for opening a different screen.
"""
def clear_advanced():
    global advanced_list

    # Clears advanced screen
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()

def to_custom_menu(root, common_el, common_mat, element, material, custom_mat,
                   selection, mode, interactions, mac_num, d_num, lac_num, mac_den,
                   d_den, lac_den, energy_unit):
    clear_advanced()
    photons_add_custom(root, common_el, common_mat, element, material, custom_mat,
                       selection, mode, interactions, mac_num, d_num, lac_num, mac_den,
                       d_den, lac_den, energy_unit)

def to_export_menu(root, common_el, common_mat, element, material, custom_mat,
                   selection, mode, interactions, mac_num, d_num, lac_num,
                   mac_den, d_den, lac_den, energy_unit):
    clear_advanced()
    photons_export(root, common_el, common_mat, element, material, custom_mat,
                   selection, mode, interactions, mac_num, d_num, lac_num,
                   mac_den, d_den, lac_den, energy_unit)

def open_ref(root):
    root.focus()
    db_path = resource_path('Utility/Modules/Mass Attenuation/References.txt')
    open_file(db_path)

def open_help(root):
    root.focus()
    db_path = resource_path('Utility/Modules/Mass Attenuation/Help.txt')
    open_file(db_path)

def do_action(root, action, category, choices, inverse, var, dropdown):
    root.focus()
    carry_action(action, category, choices, inverse, var, dropdown)