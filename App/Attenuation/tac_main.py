##### IMPORTS #####
from tkinter import *
from ttkwidgets.autocomplete import AutocompleteCombobox
from App.Attenuation.tac_choices import *
from App.Attenuation.tac_unit_settings import *
from Core.Attenuation.tac_calculations import handle_calculation
from Utility.Functions.gui_utility import make_spacer

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
    result_label = Text(root, height=1, borderwidth=0, bd=0, highlightthickness=0, relief='flat')
    result_label.config(bg='black', fg='white')

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

    mode_title = ttk.Label(root, text="Calculation Mode", font=("Verdana", 16),
                           style="Maize.TLabel")
    mode_title.pack(pady=5)

    # Stores mode and sets default
    var_mode = StringVar(root)
    var_mode.set(mode_start)
    mode = mode_start

    # Frame for mode input
    mode_frame = Frame(root, bg="#00274C")
    mode_frame.pack(pady=5)

    # Frame for energy input
    energy_frame = Frame(root, bg="#00274C")

    energy_label = ttk.Label(energy_frame, text="Photon Energy (" + energy_unit + "):",
                      style="White.TLabel")
    energy_entry = ttk.Entry(energy_frame, width=30, style="Maize.TEntry")

    def select_mode(event):
        nonlocal energy_label, energy_entry, energy_title, energy_frame
        nonlocal mode, result_label, empty_frame3
        event.widget.selection_clear()
        result_label.pack_forget()
        if event.widget.get() == "Density" \
                and mode != "Density":
            energy_title.pack_forget()
            energy_frame.pack_forget()
            empty_frame3.pack_forget()
        elif mode == "Density" \
                and event.widget.get() != "Density":
            screen_list.remove(energy_frame)
            energy_frame.pack_forget()
            energy_label.pack_forget()
            energy_entry.pack_forget()
            calc.pack_forget()
            advanced_button.pack_forget()
            exit_button.pack_forget()
            energy_title.pack(pady=5)
            energy_frame.pack(pady=5)
            energy_label.pack()
            energy_entry.pack()
            empty_frame3 = make_spacer(root)
            screen_list.append(empty_frame3)
            calc.pack(pady=5)
            advanced_button.pack(pady=5)
            exit_button.pack(pady=5)
            screen_list.append(energy_frame)
        mode = var_mode.get()
        root.focus()

    mode_label = ttk.Label(mode_frame, text="Calculation Mode:",
                           style="White.TLabel")
    mode_label.pack()

    # Creates dropdown menu for mode
    mode_choices = ["Mass Attenuation Coefficient",
                    "Density",
                    "Linear Attenuation Coefficient"]
    mode_dropdown = ttk.Combobox(mode_frame, textvariable=var_mode, values=mode_choices, width=21,
                                 justify="center", state='readonly', style="Maize.TCombobox")
    mode_dropdown.pack()
    mode_dropdown.bind("<<ComboboxSelected>>", select_mode)

    # Spacer
    empty_frame1 = make_spacer(root)

    select_title = ttk.Label(root, text="Select Element or Material", font=("Verdana", 16),
                             style="Maize.TLabel")
    select_title.pack(pady=5)

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
    main_frame = Frame(root, bg="#00274C")
    main_frame.pack(pady=5)

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

    # Frame for category selection
    category_frame = Frame(main_frame, bg="#00274C")
    category_frame.pack(side="left", padx=5)

    category_label = ttk.Label(category_frame, text="Select Category:",
                               style="White.TLabel")
    category_label.pack()

    # Creates dropdown menu for selection
    selections = ["Common Elements", "All Elements",
                  "Common Materials", "All Materials",
                  "Custom Materials"]
    selection_dropdown = ttk.Combobox(category_frame, textvariable=var_selection,
                                      values=selections, width=13, justify="center",
                                      state='readonly', style="Maize.TCombobox")
    selection_dropdown.pack()
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

    # Frame for item selection
    item_frame = Frame(main_frame, bg="#00274C")
    item_frame.pack(side="left", padx=5)

    item_label = ttk.Label(item_frame, text="Select Item:",
                           style="White.TLabel")
    item_label.pack()

    # Creates dropdown menu for element selection
    dropdown = AutocompleteCombobox(item_frame, textvariable=var, completevalues=choices,
                                    width=box_width, justify="center", style="Maize.TCombobox")
    dropdown.pack()
    dropdown.bind('<Return>', on_enter)
    dropdown.bind("<<ComboboxSelected>>", on_select)
    dropdown.bind("<FocusOut>", on_enter)

    # Spacer
    empty_frame2 = make_spacer(root)

    energy_title = ttk.Label(root, text="Photon Energy", font=("Verdana", 16),
                             style="Maize.TLabel")

    # Spacer
    empty_frame3 = Frame()

    # Energy input is not necessary if mode is density
    if var_mode.get() != "Density":
        energy_title.pack(pady=5)
        energy_frame.pack(pady=5)
        energy_label.pack()
        energy_entry.pack()
        empty_frame3.pack(pady=10)

    # Creates calculate button
    calc = ttk.Button(root, text="Calculate", style="Maize.TButton",
                      padding=(0,0),
                      command=lambda: start_calculation(root,
                                                        var_selection.get(), var_mode.get(),
                                                        interaction, var.get(),
                                                        energy_entry.get(), result_label,
                                      get_unit(mac_num, d_num, lac_num, var_mode.get()),
                                      get_unit(mac_den, d_den, lac_den, var_mode.get()),
                                                        energy_unit))
    calc.pack(pady=5)

    # Creates an advanced settings button
    advanced_button = ttk.Button(root, text="Advanced Settings", style="Maize.TButton",
                                 padding=(9,0),
                                 command=lambda: to_advanced(root, common_el, common_mat,
                                                             element, material, custom_mat,
                                                             var_selection.get(),
                                                             var_mode.get(), interaction,
                                                             mac_num, d_num, lac_num,
                                                             mac_den, d_den, lac_den,
                                                             result_label, energy_unit))
    advanced_button.pack(pady=5)

    # Creates exit button to return to home screen
    exit_button = ttk.Button(root, text="Exit", style="Maize.TButton",
                             padding=(-20,0),
                             command=lambda: exit_to_home(root, result_label))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    screen_list = [mode_title, mode_frame, empty_frame1,
                   select_title, main_frame, empty_frame2,
                   energy_title, energy_frame, empty_frame3,
                   calc, advanced_button, exit_button]

def to_advanced(root, common_el, common_mat, element, material,
             custom_mat, selection, mode, interaction,
             mac_num, d_num, lac_num,
             mac_den, d_den, lac_den,
             result_label, energy_unit):
    root.focus()
    from App.Attenuation.tac_advanced import tac_advanced

    # Hides T.A.C. screen
    clear_screen(result_label)
    tac_advanced(root, common_el, common_mat, element, material,
                 custom_mat, selection, mode, interaction,
                 mac_num, d_num, lac_num,
                 mac_den, d_den, lac_den, energy_unit)

def clear_screen(result_label):
    global screen_list

    # Clears main screen
    result_label.pack_forget()
    for node in screen_list:
        node.destroy()
    screen_list.clear()

def exit_to_home(root, result_label):
    root.focus()
    from App.app import return_home
    clear_screen(result_label)
    return_home(root)

def start_calculation(root, selection, mode, interaction, element, energy_str, result_label,
                       num, den, energy_unit):
    root.focus()
    handle_calculation(selection, mode, interaction, element, energy_str, result_label,
                       num, den, energy_unit)