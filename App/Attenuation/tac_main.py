##### IMPORTS #####
from tkinter import *
from ttkwidgets.autocomplete import AutocompleteCombobox
from App.Attenuation.tac_choices import *
from App.Attenuation.tac_unit_settings import *
from Core.Attenuation.tac_calculations import handle_calculation
from Utility.Functions.gui_utility import make_spacer, get_width
from App.style import SectionFrame

# For global access to nodes on T.A.C. screen
screen_list = []

def total_attenuation_coefficient(root, selection_start="Common Elements",
                                  mode_start="Mass Attenuation Coefficient",
                                  interactions=None, common_el="Ag",
                                  common_mat="Air (dry, near sea level)", element="Ac",
                                  material="A-150 Tissue-Equivalent Plastic (A150TEP)",
                                  custom_mat="", mac_num="cm\u00B2", d_num="g", lac_num="1",
                                  mac_den="g", d_den="cm\u00B3", lac_den="cm",
                                  energy_unit="MeV"):
    global screen_list

    if interactions is None or not interactions:
        interactions = ["Total Attenuation with Coherent Scattering"]

    # Frame for result
    result_frame = SectionFrame(root, title="Result")
    inner_result_frame = result_frame.get_inner_frame()

    # Displays the requested coefficient
    result = ttk.Label(inner_result_frame, text="Result:",
                       style="Black.TLabel")
    result_label = Text(inner_result_frame, height=1, borderwidth=0, bd=0,
                        highlightthickness=0, relief='flat')
    result_label.config(bg='black', fg='white', state="disabled", width=32)

    choices = get_choices(selection_start)

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

    # Stores mode and sets default
    var_mode = StringVar(root)
    var_mode.set(mode_start)
    mode = mode_start

    # Frame for mode input
    mode_frame = SectionFrame(root, title="Calculation Mode")
    mode_frame.pack(padx=10, pady=10)
    inner_mode_frame = mode_frame.get_inner_frame()

    # Frame for energy input
    energy_frame = SectionFrame(root, title="Photon Energy", width=1000)
    inner_energy_frame= energy_frame.get_inner_frame()

    energy_label = ttk.Label(inner_energy_frame, text="Photon Energy (" + energy_unit + "):",
                             style="Black.TLabel")
    energy_entry = ttk.Entry(inner_energy_frame, width=25, style="Maize.TEntry")

    def select_mode(event):
        nonlocal energy_label, energy_entry, energy_frame
        nonlocal mode, result_label, empty_frame3, result
        event.widget.selection_clear()
        if event.widget.get() == "Density" \
                and mode != "Density":
            energy_frame.pack_forget()
            empty_frame3.pack_forget()
        elif mode == "Density" \
                and event.widget.get() != "Density":
            screen_list.remove(energy_frame)
            energy_frame.pack_forget()
            energy_label.pack_forget()
            energy_entry.pack_forget()
            result_frame.pack_forget()
            calc_button.pack_forget()
            result.pack_forget()
            result_label.pack_forget()
            advanced_button.pack_forget()
            exit_button.pack_forget()
            energy_frame.pack(padx=10, pady=10)
            energy_label.pack(pady=(5,0))
            energy_entry.pack(pady=(0,5))
            empty_frame3 = make_spacer(root)
            screen_list.append(empty_frame3)
            result_frame.pack(padx=10, pady=10)
            calc_button.pack(pady=5)
            result.pack(pady=(5,0))
            result_label.pack(pady=(0,5))
            advanced_button.pack(pady=5)
            exit_button.pack(pady=5)
            screen_list.append(energy_frame)
        mode = var_mode.get()
        root.focus()

    # Creates dropdown menu for mode
    mode_choices = ["Mass Attenuation Coefficient",
                    "Density",
                    "Linear Attenuation Coefficient"]
    mode_dropdown = ttk.Combobox(inner_mode_frame, textvariable=var_mode, values=mode_choices,
                                 justify="center", state='readonly', style="Maize.TCombobox")
    mode_dropdown.config(width=get_width(mode_choices))
    mode_dropdown.pack(pady=20)
    mode_dropdown.bind("<<ComboboxSelected>>", select_mode)

    # Spacer
    empty_frame1 = make_spacer(root)

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
    main_frame = SectionFrame(root, title="Select Element or Material", width=1000)
    main_frame.pack(padx=10, pady=10)
    inner_main_frame = main_frame.get_inner_frame()

    def select_selection(event):
        nonlocal choices

        event.widget.selection_clear()
        selection = var_selection.get()
        choices = get_choices(selection)
        var.set("" if choices == [] else
                common_el if selection == "Common Elements" else
                common_mat if selection == "Common Materials" else
                element if selection == "All Elements" else
                material if selection == "All Materials" else
                custom_mat if selection == "Custom Materials" else "")
        dropdown.config(completevalues=choices, width=get_width(choices))
        root.focus()

    # Frame for category selection
    category_frame = Frame(inner_main_frame, bg="#F2F2F2")
    category_frame.pack(pady=(15,5))

    category_label = ttk.Label(category_frame, text="Select Category:",
                               style="Black.TLabel")
    category_label.pack()

    # Creates dropdown menu for selection
    selections = ["Common Elements", "All Elements",
                  "Common Materials", "All Materials",
                  "Custom Materials"]
    selection_dropdown = ttk.Combobox(category_frame, textvariable=var_selection,
                                      values=selections, justify="center",
                                      state='readonly', style="Maize.TCombobox")
    selection_dropdown.config(width=get_width(selections))
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
    item_frame = Frame(inner_main_frame, bg="#F2F2F2")
    item_frame.pack(pady=(5,20))

    item_label = ttk.Label(item_frame, text="Select Item:",
                           style="Black.TLabel")
    item_label.pack()

    # Creates dropdown menu for element selection
    dropdown = AutocompleteCombobox(item_frame, textvariable=var, completevalues=choices,
                                    justify="center", style="Maize.TCombobox")
    dropdown.config(width=get_width(choices))
    dropdown.pack()
    dropdown.bind('<Return>', on_enter)
    dropdown.bind("<<ComboboxSelected>>", on_select)
    dropdown.bind("<FocusOut>", on_enter)

    # Spacer
    empty_frame2 = make_spacer(root)

    # Spacer
    empty_frame3 = Frame()

    # Energy input is not necessary if mode is density
    if var_mode.get() != "Density":
        energy_frame.pack(padx=10, pady=10)
        energy_label.pack(pady=(5,0))
        energy_entry.pack(pady=(0,5))
        empty_frame3 = make_spacer(root)

    result_frame.pack(padx=10, pady=10)

    # Creates calculate button
    calc_button = ttk.Button(inner_result_frame, text="Calculate", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: start_calculation(root,
                                                        var_selection.get(), var_mode.get(),
                                                        interactions, var.get(),
                                                        energy_entry.get(), result_label,
                                      get_unit(mac_num, d_num, lac_num, var_mode.get()),
                                      get_unit(mac_den, d_den, lac_den, var_mode.get()),
                                                        energy_unit))
    calc_button.config(width=get_width(["Calculate"]))
    calc_button.pack(pady=5)

    result.pack(pady=(5,0))
    result_label.pack(pady=(0,5))

    # Creates an advanced settings button
    advanced_button = ttk.Button(root, text="Advanced Settings", style="Maize.TButton",
                                 padding=(0,0),
                                 command=lambda: to_advanced(root, common_el, common_mat,
                                                             element, material, custom_mat,
                                                             var_selection.get(),
                                                             var_mode.get(), interactions,
                                                             mac_num, d_num, lac_num,
                                                             mac_den, d_den, lac_den,
                                                             result_label, energy_unit))
    advanced_button.config(width=get_width(["Advanced Settings"]))
    advanced_button.pack(pady=5)

    # Creates exit button to return to home screen
    exit_button = ttk.Button(root, text="Exit", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: exit_to_home(root, result_label))
    exit_button.config(width=get_width(["Exit"]))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    screen_list = [mode_frame, empty_frame1,
                   main_frame, empty_frame2,
                   energy_frame, empty_frame3,
                   result_frame, advanced_button, exit_button]

def to_advanced(root, common_el, common_mat, element, material,
             custom_mat, selection, mode, interactions,
             mac_num, d_num, lac_num,
             mac_den, d_den, lac_den,
             result_label, energy_unit):
    root.focus()
    from App.Attenuation.tac_advanced import tac_advanced

    # Hides T.A.C. screen
    clear_screen(result_label)
    tac_advanced(root, common_el, common_mat, element, material,
                 custom_mat, selection, mode, interactions,
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

def start_calculation(root, selection, mode, interactions, element, energy_str, result_label,
                       num, den, energy_unit):
    root.focus()
    handle_calculation(selection, mode, interactions, element, energy_str, result_label,
                       num, den, energy_unit)