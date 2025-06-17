##### IMPORTS #####
from tkinter import *
from ttkwidgets.autocomplete import AutocompleteCombobox
from App.Attenuation.tac_choices import *
from App.Attenuation.tac_unit_settings import *
from Core.Attenuation.tac_calculations import handle_calculation

# For global access to nodes on T.A.C. screen
screen_list = []

def total_attenuation_coefficient(root, selection_start="Common Elements",
                                  mode_start="Mass Attenuation Coefficient",
                                  interaction="Total Attenuation with Coherent Scattering",
                                  common_el="Ag", common_mat="Air (dry, near sea level)",
                                  element="Ac",
                                  material="A-150 Tissue-Equivalent Plastic (A150TEP)",
                                  custom_mat="", mac_num="cm\u00B2", d_num="g", lac_num="1",
                                  mac_den="g", d_den="cm\u00B3", lac_den="cm",
                                  energy_unit="MeV"):
    global screen_list

    # Displays the requested coefficient
    result_label = Text(root, height=1, borderwidth=0)
    result_label.config(bg='white', fg='grey')

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

    # Frame for type selection and element/material
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

    def on_select(event):
        event.widget.selection_clear()
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

    label = Label(root, text="Energy (" + energy_unit + "):")
    entry = Entry(root, width=30)
    entry.config(bg='white', fg='grey')

    def select_mode(event):
        nonlocal label, entry
        nonlocal mode
        nonlocal result_label
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
            advanced_button.pack_forget()
            exit_button.pack_forget()
            label.pack()
            entry.pack()
            calc.pack(pady=5)
            advanced_button.pack(pady=2)
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
                                  get_unit(mac_den, d_den, lac_den, var_mode.get()),
                                                     energy_unit))
    calc.pack(pady=5)

    # Creates an advanced settings button
    advanced_button = Button(root, text="Advanced Settings",
                      command=lambda: to_advanced(root, common_el, common_mat, element,
                                                  material, custom_mat,
                                                  var_selection.get(),
                                                  var_mode.get(), interaction,
                                                  mac_num, d_num, lac_num,
                                                  mac_den, d_den, lac_den,
                                                  result_label, energy_unit))
    advanced_button.pack(pady=2)

    # Creates exit button to return to home screen
    exit_button = Button(root, text="Exit",
                         command=lambda: exit_to_home(root, result_label))
    exit_button.pack(pady=2)

    # Stores nodes into global list
    screen_list = [top_frame, dropdown, selection_dropdown, mode_dropdown,
                   label, entry, calc, advanced_button, exit_button]

def to_advanced(root, common_el, common_mat, element, material,
             custom_mat, selection, mode, interaction,
             mac_num, d_num, lac_num,
             mac_den, d_den, lac_den,
             result_label, energy_unit):
    from App.Attenuation.tac_advanced import tac_advanced

    # Hides T.A.C. screen
    clear_screen(result_label)
    tac_advanced(root, common_el, common_mat, element, material,
                 custom_mat, selection, mode, interaction,
                 mac_num, d_num, lac_num,
                 mac_den, d_den, lac_den, energy_unit)

def clear_screen(result_label):
    global screen_list

    # Clears screen
    result_label.pack_forget()
    for node in screen_list:
        node.destroy()
    screen_list.clear()

def exit_to_home(root, result_label):
    from App.app import return_home
    clear_screen(result_label)
    return_home(root)