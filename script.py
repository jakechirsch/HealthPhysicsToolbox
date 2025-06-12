##### IMPORTS #####
from tkinter.ttk import Combobox
from ttkwidgets.autocomplete import AutocompleteCombobox
from Core.Attenuation.tac_plots import *

##### WINDOW SETUP #####
root = Tk()
root.title("Health Physics Toolbox")
root.geometry("725x450")

##### HOME SCREEN BUTTONS #####
tac_button = Button(root)

# For global access to nodes on non-home screen
screen_list = []
advanced_list = []

# Displays the requested coefficient
result_label = Text(root, height=1, borderwidth=0)
result_label.config(bg='white', fg='grey')

def on_select(event):
    event.widget.selection_clear()
    root.focus()

def total_attenuation_coefficient(selection_start="Common Elements",
                                  mode_start="Mass Attenuation Coefficient",
                                  interaction="Total Attenuation with Coherent Scattering",
                                  common_el="Ag", common_mat="Air (dry, near sea level)",
                                  element="Ac",
                                  material="A-150 Tissue-Equivalent Plastic (A150TEP)",
                                  custom_mat="", mac_num="cm\u00B2", d_num="g", lac_num="1",
                                  mac_den="g", d_den="cm\u00B3", lac_den="cm"):
    global tac_button
    global screen_list

    choices = get_choices(selection_start)

    box_width = 5 if selection_start in element_choices else 35

    # Make sure common default choices are valid selections
    common_elements = get_choices("Common Elements")
    if not common_el in common_elements:
        common_el = common_elements[0] if len(common_elements) > 0 else ""
    common_materials = get_choices("Common Materials")
    if not common_mat in common_materials:
        common_mat = common_materials[0] if len(common_materials) > 0 else ""
    custom_materials = get_choices("Custom Materials")
    if not custom_mat in custom_materials:
        custom_mat = custom_materials[0] if len(custom_materials) > 0 else ""

    # Stores selection and sets default
    var_selection = StringVar(root)
    var_selection.set(selection_start)

    # Stores element/material selection
    var = StringVar(root)
    var.set("" if choices == [] else
            common_el if selection_start == "Common Elements" else
            common_mat if selection_start == "Common Materials" else
            element if selection_start == "All Elements" else
            material if selection_start == "All Materials" else
            custom_mat if selection_start == "Custom Materials" else "")

    # Changes to T.A.C. screen
    tac_button.pack_forget()

    # Frame for element selection and advanced settings button
    top_frame = Frame(root)
    top_frame.pack(pady=10)

    def select_selection(event):
        nonlocal choices
        nonlocal box_width

        event.widget.selection_clear()
        selection = var_selection.get()
        choices = get_choices(selection)
        var.set("" if choices == [] else
                common_el if selection == "Common Elements" else
                common_mat if selection == "Common Materials" else
                element if selection == "All Elements" else
                material if selection == "All Materials" else
                custom_mat if selection == "Custom Materials" else "")
        box_width = 5 if selection in element_choices else 35
        dropdown.config(completevalues=choices, width=box_width)
        root.focus()

    # Creates dropdown menu for selection
    selections = ["Common Elements", "All Elements",
                  "Common Materials", "All Materials",
                  "Custom Materials"]
    selection_dropdown = Combobox(top_frame, textvariable=var_selection,
                                  values=selections, width=13, state='readonly')
    selection_dropdown.pack(side="left", padx=5)
    selection_dropdown.bind("<<ComboboxSelected>>", select_selection)

    def on_enter(_):
        nonlocal common_el, common_mat, element, material, custom_mat
        value = dropdown.get()
        selection = var_selection.get()
        if value not in choices:
            dropdown.set("" if choices == [] else
                         common_el if selection == "Common Elements" else
                         common_mat if selection == "Common Materials" else
                         element if selection == "All Elements" else
                         material if selection == "All Materials" else
                         custom_mat if selection == "Custom Materials" else "")
        else:
            # Move focus away from the combobox
            selection = var_selection.get()
            if selection == "Common Elements":
                common_el = var.get()
            elif selection == "All Elements":
                element = var.get()
            elif selection == "Common Materials":
                common_mat = var.get()
            elif selection == "All Materials":
                material = var.get()
            elif selection == "Custom Materials":
                custom_mat = var.get()
            root.focus()

    # Creates dropdown menu for element selection
    dropdown = AutocompleteCombobox(top_frame, textvariable=var, completevalues=choices,
                                    width=box_width)
    dropdown.pack(side="left", padx=5)
    dropdown.bind('<Return>', on_enter)
    dropdown.bind("<<ComboboxSelected>>", on_select)
    dropdown.bind("<FocusOut>", on_enter)

    # Stores mode and sets default
    var_mode = StringVar(root)
    var_mode.set(mode_start)
    mode = mode_start

    label = Label(root, text="Energy (MeV):")
    entry = Entry(root, width=30)
    entry.config(bg='white', fg='grey')

    def select_mode(event):
        nonlocal label, entry
        nonlocal mode
        event.widget.selection_clear()
        result_label.pack_forget()
        if event.widget.get() == "Density"\
           and mode != "Density":
            label.pack_forget()
            entry.pack_forget()
        elif mode == "Density"\
             and event.widget.get() != "Density":
            screen_list.remove(label)
            screen_list.remove(entry)
            label.pack_forget()
            entry.pack_forget()
            calc.pack_forget()
            advanced.pack_forget()
            exit_button.pack_forget()
            label.pack()
            entry.pack()
            calc.pack(pady=5)
            advanced.pack(pady=2)
            exit_button.pack(pady=2)
            screen_list.append(label)
            screen_list.append(entry)
        mode = var_mode.get()
        root.focus()

    # Creates dropdown menu for mode
    mode_choices = ["Mass Attenuation Coefficient",
                    "Density",
                    "Linear Attenuation Coefficient"]
    mode_dropdown = Combobox(root, textvariable=var_mode, values=mode_choices, width=21,
                             state='readonly')
    mode_dropdown.pack(pady=5)
    mode_dropdown.bind("<<ComboboxSelected>>", select_mode)

    # Energy input is not necessary if mode is density
    if var_mode.get() != "Density":
        label.pack()
        entry.pack()

    # Creates calculate button
    calc = Button(root, text="Calculate",
                  command=lambda: handle_calculation(var_selection.get(), var_mode.get(),
                                                     interaction, var.get(),
                                                     entry.get(), result_label,
                                  get_unit(mac_num, d_num, lac_num, var_mode.get()),
                                  get_unit(mac_den, d_den, lac_den, var_mode.get())))
    calc.pack(pady=5)

    # Creates an advanced settings button
    advanced = Button(root, text="Advanced Settings",
                      command=lambda: tac_advanced(common_el, common_mat, element, material,
                                                   custom_mat, var_selection.get(),
                                                   var_mode.get(), interaction,
                                                   mac_num, d_num, lac_num,
                                                   mac_den, d_den, lac_den))
    advanced.pack(pady=2)

    # Creates exit button to return to home screen
    exit_button = Button(root, text="Exit", command=exit_to_home)
    exit_button.pack(pady=2)

    # Stores nodes into global list
    screen_list = [top_frame, dropdown, selection_dropdown, mode_dropdown,
                   label, entry, calc, advanced, exit_button]

def get_choices(selection):
    choices = []

    if selection == "All Elements" or selection == "All Materials":
        # Obtains list of elements from csv file
        name = "Elements" if selection == "All Elements" else "Materials"
        with open('Data/General Data/Density/' + name + '.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] != 'Name':
                    choices.append(row[0])
        return choices

    # Obtains list of elements from shelve
    with shelve.open(selection) as prefs:
        default = []
        if selection != "Custom Materials":
            with open('Data/Modules/Mass Attenuation/' + selection + '.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] != 'Name':
                        default.append(row[0])
        choices = prefs.get(selection, default)
        choices.sort()
        return choices

def tac_advanced(common_el, common_mat, element, material, custom_mat,
                 selection, mode, interaction_start, mac_num, d_num, lac_num,
                 mac_den, d_den, lac_den):
    global advanced_list

    # Hides T.A.C. screen
    clear()

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
        on_select(event)
        vertical_frame.destroy()
        vertical_frame = Frame(top_frame)
        vertical_frame.pack(side='left', padx=5)
        make_vertical_frame(vertical_frame, action_dropdown.get(), category_dropdown.get(),
                            non_common, common, non_common_m, common_m, custom)

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
    make_vertical_frame(vertical_frame, action_dropdown.get(), category_dropdown.get(),
                        non_common, common, non_common_m, common_m, custom)

    # Stores interaction and sets default
    var_interaction = StringVar(root)
    var_interaction.set(interaction_start)

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
    on_select_num = get_select_unit(num_units, mode)
    on_select_den = get_select_unit(den_units, mode)

    # Creates dropdown menu for numerator unit
    numerator_choices = get_unit_keys(mac_numerator, density_numerator,
                                      lac_numerator, mode)
    unit_dropdown(unit_frame, numerator_choices,
                  mac_num, d_num, lac_num, mode, on_select_num)

    # / label
    slash_label = Label(unit_frame, text="/")
    slash_label.pack(side='left')

    # Creates dropdown menu for denominator unit
    denominator_choices = get_unit_keys(mac_denominator, density_denominator,
                                        lac_denominator, mode)
    unit_dropdown(unit_frame, denominator_choices,
                  mac_den, d_den, lac_den, mode, on_select_den)

    # Creates plot button
    plot_button = Button(root, text="Plot",
                         command=lambda: plot_data(common_el if selection == "Common Elements"
                                                   else common_mat if
                                                   selection == "Common Materials"
                                                   else element if selection == "All Elements"
                                                   else material if selection == "All Materials"
                                                   else custom_mat
                                                   if selection == "Custom Materials"
                                                   else "",
                                                   selection, mode, var_interaction.get(),
                                                   get_unit(num_units[0], num_units[1],
                                                            num_units[2], mode),
                                                   get_unit(den_units[0], den_units[1],
                                                            den_units[2], mode)))
    plot_button.pack(pady=2)

    # Frame for export options
    export_frame = Frame(root)
    export_frame.pack(pady=5)

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
                           command=lambda: plot_data(common_el if selection == "Common Elements"
                                                     else common_mat if
                                                     selection == "Common Materials"
                                                     else element if selection == "All Elements"
                                                     else material if selection == "All Materials"
                                                     else custom_mat
                                                     if selection == "Custom Materials"
                                                     else "",
                                                     selection, mode, var_interaction.get(),
                                                     get_unit(num_units[0], num_units[1],
                                                              num_units[2], mode),
                                                     get_unit(den_units[0], den_units[1],
                                                              den_units[2], mode),
                                                     export=True, choice=export_dropdown.get()))
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
                         command=lambda: tac_back(pass_saved(common_el, common),
                                                  pass_saved(common_mat, common_m),
                                                  element, material,
                                                  pass_saved(custom_mat, custom),
                                                  selection, mode,
                                                  var_interaction.get(), num_units[0],
                                                  num_units[1], num_units[2], den_units[0],
                                                  den_units[1], den_units[2]))
    exit_button.pack(pady=2)

    # Stores nodes into global list
    advanced_list = [interaction_dropdown, plot_button, exit_button,
                     unit_frame, top_frame, bottom_frame, export_frame]

def get_select_unit(units, mode):
    def on_select_unit(event):
        nonlocal mode
        event.widget.selection_clear()
        root.focus()
        if mode == "Mass Attenuation Coefficient":
            units[0] = event.widget.get()
        elif mode == "Density":
            units[1] = event.widget.get()
        else:
            units[2] = event.widget.get()
    return on_select_unit

def unit_dropdown(frame, choices, mac, d, lac, mode, on_select_u):
    dropdown = Combobox(frame, values=choices, width=5, state='readonly')
    dropdown.set(get_unit(mac, d, lac, mode))
    dropdown.pack(side='left', padx=5)
    dropdown.bind("<<ComboboxSelected>>", on_select_u)

def get_unit_keys(mac, density, lac, mode):
    _dict = get_unit(mac, density, lac, mode)
    choices = list(_dict.keys())
    return choices

def pass_saved(saved, choices):
    return saved if saved in choices else choices[0] if len(choices) > 0 else ""

def get_unit(mac, d, lac, mode):
    return mac if mode == "Mass Attenuation Coefficient" else\
           d if mode == "Density" else lac

def make_vertical_frame(vertical_frame, action, category,
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
                        command=lambda: add_custom(entry, entry2, entry3))
        button.pack()
    else:
        on_enter = make_enter(var, choices)
        dropdown = make_ac_box(vertical_frame, var, choices,
                               on_enter, width)

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

def add_custom(name_box, density_box, weights_box):
    name = name_box.get()
    density = density_box.get()
    weights = weights_box.get()
    csv_data = '"Weight","Element"\n' + weights

    with shelve.open("Custom Materials") as prefs:
        choices = prefs.get("Custom Materials", [])
        if not name in choices:
            choices.append(name)
        prefs["Custom Materials"] = choices

    # Save to shelve
    with shelve.open('_' + name) as db:
        db[name] = csv_data
        db[name + '_Density'] = density

    name_box.delete(0, END)
    weights_box.delete(0, END)
    density_box.delete(0, END)
    root.focus()

def make_enter(var, choices):
    def on_enter(_):
        value = var.get()
        if value not in choices:
            var.set(choices[0] if len(choices) > 0 else "")
        else:
            # Move focus away from the combobox
            root.focus()
    return on_enter

def make_ac_box(frame, var, choices, enter, width):
    dropdown = AutocompleteCombobox(frame, textvariable=var,
                                    completevalues=choices, width=width)
    dropdown.pack()
    dropdown.bind('<Return>', enter)
    dropdown.bind("<<ComboboxSelected>>", on_select)
    dropdown.bind("<FocusOut>", enter)
    return dropdown

def carry_action(action, category, choices, inverse, var, dropdown):
    if action == "Add":
        add_c(category, choices, inverse, var, dropdown)
    elif action == "Remove":
        remove_c(category, choices, inverse, var, dropdown)

def add_c(selection, choices, inverse, var, dropdown):
    with shelve.open(selection) as prefs:
        # Adds element to common elements
        element = var.get()
        if element == "":
            return
        inverse.append(element)
        prefs[selection] = inverse

        # Removes element from non-common elements
        choices.remove(element)
        dropdown.config(completevalues=choices)
        var.set(choices[0] if len(choices) > 0 else "")

def remove_c(selection, choices, inverse, var, dropdown):
    with shelve.open(selection) as prefs:
        # Removes element from common elements
        element = var.get()
        if element == "":
            return
        choices.remove(element)
        prefs[selection] = choices
        dropdown.config(completevalues=choices)
        var.set(choices[0] if len(choices) > 0 else "")

        # Adds element to non-common elements
        inverse.append(element)

def tac_back(common_el, common_mat, element, material, custom_mat,
             selection, mode, interaction, mac_num, d_num, lac_num,
             mac_den, d_den, lac_den):
    clear_advanced()
    total_attenuation_coefficient(selection_start=selection, mode_start=mode,
                                  interaction=interaction, common_el=common_el,
                                  common_mat=common_mat, element=element, material=material,
                                  custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                                  lac_num=lac_num, mac_den=mac_den, d_den=d_den, lac_den=lac_den)

def clear():
    global screen_list

    # Clears screen
    result_label.pack_forget()
    for node in screen_list:
        node.destroy()
    screen_list.clear()

def clear_advanced():
    global screen_list

    # Clears screen
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()

def return_home():
    global tac_button

    # Creates buttons for home screen
    tac_button = Button(root, text="Total Attenuation Coefficient",
                        command=total_attenuation_coefficient)
    tac_button.pack(pady=5)

def exit_to_home():
    clear()
    return_home()

# Creates home screen upon launch
return_home()

# Runs app
root.mainloop()