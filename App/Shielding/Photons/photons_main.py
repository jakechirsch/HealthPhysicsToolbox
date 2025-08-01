##### IMPORTS #####
from App.style import AutocompleteCombobox
from Core.Shielding.Photons.photons_calculations import handle_calculation
from Utility.Functions.gui_utility import *
from Utility.Functions.choices import *
from App.style import SectionFrame

# For global access to nodes on photon attenuation main screen
main_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the photon attenuation main screen.
The following sections and widgets are created:
   Module Title (Photon Attenuation)
   Select Calculation Mode section
   Select Interacting Medium section
   Input Energy section (only when Calculation Mode is not Density)
   Result section (title dependent on Calculation Mode)
   Advanced Settings button
   Exit button
This function contains all of the logic involving these widgets'
behaviors.
The sections and widgets are stored in main_list so they can be
accessed later by clear_main.
"""
def photons_main(root, category_start="Common Elements",
                 mode_start="Mass Attenuation Coefficient",
                 interactions=None, common_el="Ag",
                 common_mat="Air (dry, near sea level)", element="Ac",
                 material="A-150 Tissue-Equivalent Plastic (A150TEP)",
                 custom_mat="", mac_num="cm\u00B2", d_num="g", lac_num="1",
                 mac_den="g", d_den="cm\u00B3", lac_den="cm",
                 energy_unit="MeV"):
    global main_list

    # Sets default interaction - Total Attenuation with Coherent Scattering
    if interactions is None or not interactions:
        interactions = ["Total Attenuation with Coherent Scattering"]

    # Makes title frame
    title_frame = make_title_frame(root, "Photon Attenuation", "Shielding/Photons")

    # Creates font for result label and energy entry
    monospace_font = font.Font(family="Menlo", size=12)

    # Frame for result
    result_frame = SectionFrame(root, title=mode_start)
    inner_result_frame = result_frame.get_inner_frame()

    # Input/output box width
    entry_width = 28 if platform.system() == "Windows" else 32

    # Displays the result of calculation
    result_label = ttk.Label(inner_result_frame, text="Result:",
                             style="Black.TLabel")
    result_box = Text(inner_result_frame, height=1, borderwidth=3, bd=3,
                      highlightthickness=0, relief='solid')
    result_box.config(bg='white', fg='black', state="disabled", width=entry_width,
                      font=monospace_font)

    # Gets the item options
    choices = get_choices(category_start, "Shielding", "Photons")

    # Gets customizable categories
    common_elements = get_choices("Common Elements", "Shielding", "Photons")
    common_materials = get_choices("Common Materials", "Shielding", "Photons")
    custom_materials = get_choices("Custom Materials", "Shielding", "Photons")

    # Make sure default choices are valid selections
    common_el = valid_saved(common_el, common_elements)
    common_mat = valid_saved(common_mat, common_materials)
    custom_mat = valid_saved(custom_mat, custom_materials)

    # Stores mode and sets default
    var_mode = StringVar(root)
    var_mode.set(mode_start)
    mode = mode_start

    # Frame for mode input
    mode_frame = SectionFrame(root, title="Select Calculation Mode")
    mode_frame.pack()
    inner_mode_frame = mode_frame.get_inner_frame()

    # Frame for energy input
    energy_frame = SectionFrame(root, title="Input Energy")
    inner_energy_frame= energy_frame.get_inner_frame()

    # Energy label
    energy_label = ttk.Label(inner_energy_frame,
                             text="Photon Energy (" + energy_unit + "):",
                             style="Black.TLabel")
    energy_entry = Entry(inner_energy_frame, width=entry_width, insertbackground="black",
                         background="white", foreground="black", borderwidth=3, bd=3,
                         highlightthickness=0, relief='solid', font=monospace_font)

    # Logic for when a Calculation Mode is selected
    def select_mode(event):
        nonlocal mode, empty_frame3
        event.widget.selection_clear()

        if event.widget.get() == "Density" \
                and mode != "Density":
            # Gets rid of input energy section when switching to density mode
            energy_frame.pack_forget()
            empty_frame3.pack_forget()
        elif mode == "Density" \
                and event.widget.get() != "Density":
            # Reset in preparation to re-add input energy section in correct place
            main_list.remove(empty_frame3)
            energy_frame.pack_forget()
            result_frame.pack_forget()
            advanced_button.pack_forget()
            exit_button.pack_forget()

            # Creates input energy section when switching away from density mode
            energy_frame.pack()
            energy_label.pack(pady=(15,1))
            energy_entry.pack(pady=(1,20))

            # Spacer
            empty_frame3 = make_spacer(root)
            main_list.append(empty_frame3)

            # Re-adds everything below input energy section
            result_frame.pack()
            advanced_button.pack(pady=5)
            exit_button.pack(pady=5)

        # Update mode variable and fixes result section title
        mode = var_mode.get()
        result_frame.change_title(mode)

        # Clear result label
        result_box.config(state="normal")
        result_box.delete("1.0", END)
        result_box.config(state="disabled")

        root.focus()

    # Creates dropdown menu for mode
    mode_choices = ["Mass Attenuation Coefficient",
                    "Density",
                    "Linear Attenuation Coefficient"]
    mode_dropdown = ttk.Combobox(inner_mode_frame, textvariable=var_mode,
                                 values=mode_choices, justify="center",
                                 state='readonly', style="Maize.TCombobox")
    mode_dropdown.config(width=get_width(mode_choices))
    mode_dropdown.pack(pady=20)
    mode_dropdown.bind("<<ComboboxSelected>>", select_mode)

    # Spacer
    empty_frame1 = make_spacer(root)

    # Stores category selection and sets default
    var_category = StringVar(root)
    var_category.set(category_start)

    # Stores element/material selection and sets default
    var = StringVar(root)
    var.set(get_item(category_start, common_el, common_mat, element, material, custom_mat))

    # Frame for interacting medium category and item
    main_frame = SectionFrame(root, title="Select Interacting Medium")
    main_frame.pack()
    inner_main_frame = main_frame.get_inner_frame()

    # Logic for when an interacting medium category is selected
    def select_category(event):
        nonlocal choices

        event.widget.selection_clear()
        category = var_category.get()

        # Updates item dropdown to match category
        choices = get_choices(category, "Shielding", "Photons")
        var.set(get_item(category, common_el, common_mat, element, material, custom_mat))
        item_dropdown.set_completion_list(choices)
        item_dropdown.config(values=choices, width=get_width(choices))
        root.focus()

    # Frame for interacting medium category selection
    category_frame = Frame(inner_main_frame, bg="#F2F2F2")
    category_frame.pack(pady=(15,5))

    # Category label
    basic_label(category_frame, "Category:")

    # Creates dropdown menu for interacting medium category selection
    categories = ["Common Elements", "All Elements",
                  "Common Materials", "All Materials",
                  "Custom Materials"]
    category_dropdown = ttk.Combobox(category_frame, textvariable=var_category,
                                     values=categories, justify="center",
                                     state='readonly', style="Maize.TCombobox")
    category_dropdown.config(width=get_width(categories))
    category_dropdown.pack()
    category_dropdown.bind("<<ComboboxSelected>>", select_category)

    # Logic for when enter is hit when using the item autocomplete combobox
    def on_enter(_):
        nonlocal common_el, common_mat, element, material, custom_mat
        value = item_dropdown.get()
        category = var_category.get()
        if value not in choices:
            # Falls back on default if invalid item is typed in
            item_dropdown.set(get_item(category, common_el, common_mat,
                                       element, material, custom_mat))
        else:
            # Stores most recent items
            if category == "Common Elements":
                common_el = var.get()
            elif category == "All Elements":
                element = var.get()
            elif category == "Common Materials":
                common_mat = var.get()
            elif category == "All Materials":
                material = var.get()
            elif category == "Custom Materials":
                custom_mat = var.get()

        item_dropdown.selection_clear()
        item_dropdown.icursor(END)

    # Logic for when an interacting medium item is selected
    def on_select(event):
        event.widget.selection_clear()
        root.focus()

    # Frame for interacting medium item selection
    item_frame = Frame(inner_main_frame, bg="#F2F2F2")
    item_frame.pack(pady=(5,20))

    # Item label
    basic_label(item_frame, "Item:")

    # Creates dropdown menu for interacting medium item selection
    item_dropdown = AutocompleteCombobox(item_frame, textvariable=var, values=choices,
                                         justify="center", style="Maize.TCombobox")
    item_dropdown.set_completion_list(choices)
    item_dropdown.config(width=get_width(choices))
    item_dropdown.pack()
    item_dropdown.bind('<Return>', on_enter)
    item_dropdown.bind("<<ComboboxSelected>>", on_select)
    item_dropdown.bind("<FocusOut>", on_enter)

    # Spacer
    empty_frame2 = make_spacer(root)

    # Spacer
    empty_frame3 = Frame()

    # Input Energy section is created if Calculation Mode is not Density
    if mode != "Density":
        energy_frame.pack()
        energy_label.pack(pady=(15,1))
        energy_entry.pack(pady=(1,20))

        # Spacer
        empty_frame3 = make_spacer(root)

    result_frame.pack()

    # Stores units in list
    num_units = [mac_num, d_num, lac_num]
    den_units = [mac_den, d_den, lac_den]

    # Creates Calculate button
    calc_button = ttk.Button(inner_result_frame, text="Calculate",
                             style="Maize.TButton", padding=(0,0),
                             command=lambda: handle_calculation(root,
                                                                var_category.get(), mode,
                                                                interactions, var.get(),
                                                                energy_entry.get(), result_box,
                                                get_unit(num_units, mode_choices, mode),
                                                get_unit(den_units, mode_choices, mode),
                                                                energy_unit))
    calc_button.config(width=get_width(["Calculate"]))
    calc_button.pack(pady=(20,5))

    # Puts result display under Calculate button
    result_label.pack(pady=(5,1))
    result_box.pack(pady=(1,20))

    # Creates Advanced Settings button
    advanced_button = ttk.Button(root, text="Advanced Settings",
                                 style="Maize.TButton", padding=(0,0),
                                 command=lambda: to_advanced(root, var_category.get(),
                                                             mode, interactions,
                                                             common_el, common_mat,
                                                             element, material, custom_mat,
                                                             mac_num, d_num, lac_num,
                                                             mac_den, d_den, lac_den,
                                                             energy_unit))
    advanced_button.config(width=get_width(["Advanced Settings"]))
    advanced_button.pack(pady=5)

    # Creates Exit button to return to home screen
    exit_button = ttk.Button(root, text="Exit", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: exit_to_home(root))
    exit_button.config(width=get_width(["Exit"]))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    main_list = [title_frame,
                 mode_frame, empty_frame1,
                 main_frame, empty_frame2,
                 energy_frame, empty_frame3,
                 result_frame, advanced_button, exit_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the photon attenuation main screen
in preparation for opening a different screen.
"""
def clear_main():
    global main_list

    # Clears photon attenuation main screen
    for node in main_list:
        node.destroy()
    main_list.clear()

"""
This function transitions from the photon attenuation main screen
to the home screen by first clearing the photon attenuation main screen
and then creating the home screen.
It is called when the Exit button is hit.
"""
def exit_to_home(root):
    root.focus()
    from App.home import return_home
    clear_main()
    return_home(root)

"""
This function transitions from the photon attenuation main screen
to the photon attenuation advanced screen by first clearing the
photon attenuation main screen and then creating the
photon attenuation advanced screen.
It is called when the Advanced Settings button is hit.
"""
def to_advanced(root, category, mode, interactions, common_el, common_mat,
                element, material, custom_mat, mac_num, d_num, lac_num,
                mac_den, d_den, lac_den, energy_unit):
    root.focus()
    from App.Shielding.Photons.photons_advanced import photons_advanced

    clear_main()
    photons_advanced(root, category, mode, interactions, common_el, common_mat,
                     element, material, custom_mat, mac_num, d_num, lac_num,
                     mac_den, d_den, lac_den, energy_unit)