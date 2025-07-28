##### IMPORTS #####
from Utility.Functions.gui_utility import *
from Utility.Functions.choices import *
from App.style import SectionFrame, AutocompleteCombobox
from Core.Shielding.Electrons.electrons_calculations import handle_calculation

# For global access to nodes on electron range main screen
main_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the electron range main screen.
The following sections and widgets are created:
   Module Title (Electron Range)
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
def electrons_main(root, category_start="Common Elements",
                   mode_start="CSDA Range", common_el="Ag",
                   common_mat="Air (dry, near sea level)", element="Ac",
                   material="A-150 Tissue-Equivalent Plastic (A150TEP)",
                   custom_mat="", csda_num="g", d_num="g", rec_num="g",
                   csda_den="cm\u00B2", d_den="cm\u00B3", rec_den="cm\u00B2",
                   energy_unit="MeV"):
    global main_list

    # Makes title frame
    title_frame = make_title_frame(root, "Electron Range", "Shielding/Electrons")

    # Creates font for result label and energy entry
    monospace_font = font.Font(family="Menlo", size=12)

    # Gets the item options
    choices = get_choices(category_start, "Electrons")

    # Gets customizable categories
    common_elements = get_choices("Common Elements", "Electrons")
    common_materials = get_choices("Common Materials", "Electrons")
    custom_materials = get_choices("Custom Materials", "Electrons")

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

    # Logic to remove main frame
    def add_main_frame():
        nonlocal empty_frame2, empty_frame3

        # Fixes mode dropdown padding
        mode_dropdown.pack(pady=20)

        # Reset in preparation to re-add main frame in correct place
        main_list.remove(empty_frame2)
        main_list.remove(empty_frame3)
        empty_frame2.pack_forget()
        energy_frame.pack_forget()
        empty_frame3.pack_forget()
        result_frame.pack_forget()
        advanced_button.pack_forget()
        exit_button.pack_forget()

        # Creates main frame
        main_frame.pack()

        # Spacer
        empty_frame2 = make_spacer(root)
        main_list.append(empty_frame2)

        # Re-adds everything below input energy section
        energy_frame.pack()
        empty_frame3 = make_spacer(root)
        main_list.append(empty_frame3)
        result_frame.pack()
        advanced_button.pack(pady=5)
        exit_button.pack(pady=5)

    # Logic for when a Calculation Mode is selected
    def select_mode(event):
        nonlocal mode, empty_frame2, empty_frame3
        event.widget.selection_clear()
        warning_label.config(text="")

        if event.widget.get() != "Range-Energy Curve" \
                and mode == "Range-Energy Curve":
            # Gets rid of result label when switching off Range-Energy Curve mode
            range_label.pack_forget()
            range_result.pack_forget()
            range_check.pack_forget()

            add_main_frame()
        elif mode != "Range-Energy Curve" \
             and event.widget.get() == "Range-Energy Curve":
            # Creates range label
            mode_dropdown.pack(pady=(20,10))
            range_check.pack(pady=(0,20))
            var_range.set(0)

            # Forgets select interacting medium frame
            main_frame.pack_forget()
            empty_frame2.pack_forget()

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

        # Clear range label
        range_result.config(state="normal")
        range_result.delete("1.0", END)
        range_result.config(state="disabled")

        root.focus()

    # Creates dropdown menu for mode
    mode_choices = ["CSDA Range",
                    "Range-Energy Curve",
                    "Radiation Yield",
                    "Density Effect Delta",
                    "Density"]
    mode_dropdown = ttk.Combobox(inner_mode_frame, textvariable=var_mode,
                                 values=mode_choices, justify="center",
                                 state='readonly', style="Maize.TCombobox")
    mode_dropdown.config(width=get_width(mode_choices))
    mode_dropdown.pack(pady=20)
    mode_dropdown.bind("<<ComboboxSelected>>", select_mode)

    # Stores whether to find linear range for Range-Energy Curve mode
    var_range = IntVar()
    var_range.set(0)

    def range_hit():
        root.focus()
        if var_range.get() == 1:
            # Reset in preparation to re-add range box in correct place
            warning_label.pack_forget()

            # Adds frame to select interacting medium
            add_main_frame()

            # Adds range box
            range_label.pack(pady=(5,1))
            range_result.pack(pady=(1,0))

            # Re-adds warning label below range box
            warning_label.pack(pady=(1,5))
        else:
            # Forgets range box
            range_label.pack_forget()
            range_result.pack_forget()

            # Forgets select interacting medium frame
            main_frame.pack_forget()
            empty_frame2.pack_forget()

    # Creates checkbox for finding range
    range_check = ttk.Checkbutton(inner_mode_frame, text="Find Linear Range?",
                                  variable=var_range, style="Maize.TCheckbutton",
                                  command=lambda: range_hit())

    if mode == "Range-Energy Curve":
        # Displays the range option
        mode_dropdown.pack(pady=(20,10))
        range_check.pack(pady=(0,20))

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
    if mode != "Range-Energy Curve":
        main_frame.pack()
    inner_main_frame = main_frame.get_inner_frame()

    # Logic for when an interacting medium category is selected
    def select_category(event):
        nonlocal choices

        event.widget.selection_clear()
        category = var_category.get()

        # Updates item dropdown to match category
        choices = get_choices(category, "Electrons")
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
    empty_frame2 = Frame()
    if mode != "Range-Energy Curve":
        empty_frame2 = make_spacer(root)

    # Frame for energy input
    energy_frame = SectionFrame(root, title="Input Energy")
    inner_energy_frame = energy_frame.get_inner_frame()

    # Input/output box width
    entry_width = 28 if platform.system() == "Windows" else 32

    # Energy label
    energy_label = ttk.Label(inner_energy_frame, text="Electron Energy (" + energy_unit + "):",
                             style="Black.TLabel")
    energy_entry = Entry(inner_energy_frame, width=entry_width, insertbackground="black",
                         background="white", foreground="black", borderwidth=3, bd=3,
                         highlightthickness=0, relief='solid', font=monospace_font)

    empty_frame3 = Frame()

    # Input Energy section is created if Calculation Mode is not Density
    if mode != "Density":
        energy_frame.pack()
        energy_label.pack(pady=(15,1))
        energy_entry.pack(pady=(1,20))

        # Spacer
        empty_frame3 = make_spacer(root)

    # Frame for result
    result_frame = SectionFrame(root, title=mode_start)
    result_frame.pack()
    inner_result_frame = result_frame.get_inner_frame()

    # Stores units in list
    num_units = [csda_num, rec_num, "", "", d_num]
    den_units = [csda_den, rec_den, "", "", d_den]

    # Creates Calculate button
    calc_button = ttk.Button(inner_result_frame, text="Calculate",
                             style="Maize.TButton", padding=(0,0),
                             command=lambda: handle_calculation(root, var_category.get(),
                                                                mode, var.get(),
                                                                energy_entry.get(),
                                                                result_box, warning_label,
                                                get_unit(num_units, mode_choices, mode),
                                                get_unit(den_units, mode_choices, mode),
                                                                energy_unit, range_result))
    calc_button.config(width=get_width(["Calculate"]))
    calc_button.pack(pady=(20,5))

    # Displays the result of calculation
    result_label = ttk.Label(inner_result_frame, text="Result:",
                             style="Black.TLabel")
    result_box = Text(inner_result_frame, height=1, borderwidth=3, bd=3,
                      highlightthickness=0, relief='solid')
    result_box.config(bg='white', fg='black', state="disabled", width=entry_width,
                      font=monospace_font)
    result_label.pack(pady=(5,1))
    result_box.pack(pady=(1,0))

    # Creates range result box
    range_label = ttk.Label(inner_result_frame, text="Linear Range:",
                            style="Black.TLabel")
    range_result = Text(inner_result_frame, height=1, borderwidth=3, bd=3,
                        highlightthickness=0, relief='solid')
    range_result.config(bg='white', fg='black', state="disabled", width=entry_width,
                        font=monospace_font)

    # Creates warning label for bad input
    warning_label = ttk.Label(inner_result_frame, text="", style="Error.TLabel")
    warning_label.pack(pady=(1,5))

    # Creates Advanced Settings button
    advanced_button = ttk.Button(root, text="Advanced Settings",
                                 style="Maize.TButton", padding=(0,0),
                                 command=lambda: to_advanced(root, var_category.get(),
                                                             mode, common_el, common_mat,
                                                             element, material, custom_mat,
                                                             csda_num, d_num, rec_num,
                                                             csda_den, d_den, rec_den,
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
This function clears the electron range main screen
in preparation for opening a different screen.
"""
def clear_main():
    global main_list

    # Clears electron range main screen
    for node in main_list:
        node.destroy()
    main_list.clear()

"""
This function transitions from the electron range main screen
to the home screen by first clearing the electron range main screen
and then creating the home screen.
It is called when the Exit button is hit.
"""
def exit_to_home(root):
    root.focus()
    from App.home import return_home
    clear_main()
    return_home(root)

"""
This function transitions from the electron range main screen
to the electron range advanced screen by first clearing the
electron range main screen and then creating the
electron range advanced screen.
It is called when the Advanced Settings button is hit.
"""
def to_advanced(root, category, mode, common_el, common_mat, element,
                material, custom_mat, csda_num, d_num, rec_num, csda_den, d_den,
                rec_den, energy_unit):
    root.focus()
    from App.Shielding.Electrons.electrons_advanced import electrons_advanced

    clear_main()
    electrons_advanced(root, category, mode, common_el, common_mat, element,
                       material, custom_mat, csda_num, d_num, rec_num, csda_den, d_den,
                       rec_den, energy_unit)