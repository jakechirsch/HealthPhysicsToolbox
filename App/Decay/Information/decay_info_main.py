##### IMPORTS #####
import platform
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from App.style import AutocompleteCombobox, SectionFrame
from Utility.Functions.choices import get_choices, get_isotopes
from Utility.Functions.gui_utility import make_spacer, get_width
from Core.Decay.Information.nuclide_info import handle_calculation
from Utility.Functions.gui_utility import basic_label, make_title_frame

# For global access to nodes on decay information main screen
main_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the decay information main screen.
The following sections and widgets are created:
   Module Title (Decay Information)
   Select Calculation Mode section
   Select Nuclide section
   Result section (title dependent on Calculation Mode)
   Exit button
This function contains all of the logic involving these widgets'
behaviors.
The sections and widgets are stored in main_list so they can be
accessed later by clear_main.
"""
def decay_info_main(root, mode="Decay Scheme", element="Ac", isotope="Ac-223"):
    global main_list

    # Makes title frame
    title_frame = make_title_frame(root, "Decay Information", "Decay/Information")

    # Creates font for result label and energy entry
    monospace_font = font.Font(family="Menlo", size=12)

    # Gets the item options
    element_list = get_choices("All Elements", "Decay", "")

    # Stores mode and sets default
    var_mode = tk.StringVar(root)
    var_mode.set(mode)

    # Frame for mode input
    mode_frame = SectionFrame(root, title="Select Calculation Mode")
    mode_frame.pack()
    inner_mode_frame = mode_frame.get_inner_frame()

    # Logic for when a Calculation Mode is selected
    def select_mode(event):
        nonlocal mode
        event.widget.selection_clear()

        # Update mode variable and fixes result section title
        mode = var_mode.get()
        result_frame.change_title(mode)

        # Clear result label
        result_box.config(state="normal")
        result_box.delete("1.0", tk.END)
        result_box.config(state="disabled")

        root.focus()

    # Creates dropdown menu for mode
    mode_choices = ["Decay Scheme",
                    "Half Life",
                    "Progeny",
                    "Branching Fractions",
                    "Decay Modes",
                    "Proton Number",
                    "Nucleon Number",
                    "Atomic Mass"]
    mode_dropdown = ttk.Combobox(inner_mode_frame, textvariable=var_mode,
                                 values=mode_choices, justify="center",
                                 state='readonly', style="Maize.TCombobox")
    mode_dropdown.config(width=get_width(mode_choices))
    mode_dropdown.pack(pady=20)
    mode_dropdown.bind("<<ComboboxSelected>>", select_mode)

    # Spacer
    empty_frame1 = make_spacer(root)

    # Frame for nuclide selection
    nuclide_frame = SectionFrame(root, title="Select Nuclide")
    nuclide_frame.pack()
    inner_nuclide_frame = nuclide_frame.get_inner_frame()

    # Horizontal frame for nuclide selection
    nuclide_side_frame = tk.Frame(inner_nuclide_frame, bg="#F2F2F2")
    nuclide_side_frame.pack(pady=(20,30))

    # Logic for when enter is hit when using the element autocomplete combobox
    def on_enter(_):
        nonlocal element, isotope
        value = element_dropdown.get()

        if value not in element_list:
            # Falls back on default if invalid item is typed in
            element_dropdown.set(element)
        else:
            # Adjusts isotopes
            isotopes = get_isotopes(value)
            if element != value:
                isotope = isotopes[0]
                element = value
            isotope_dropdown.set(isotope)
            isotope_dropdown.config(values=isotopes, width=get_width(isotopes))
            element = var_element.get()

        element_dropdown.selection_clear()
        element_dropdown.icursor(tk.END)

    # Logic for when an element is selected
    def on_select_element(event):
        nonlocal element, isotope

        event.widget.selection_clear()
        new_element = element_dropdown.get()

        # Adjusts isotopes
        isotopes = get_isotopes(new_element)
        if element != new_element:
            isotope = isotopes[0]
            element = new_element
        isotope_dropdown.set(isotope)
        isotope_dropdown.config(values=isotopes, width=get_width(isotopes))

        root.focus()

    # Frame for element selection
    element_frame = tk.Frame(nuclide_side_frame, bg="#F2F2F2")
    element_frame.pack(side="left", padx=5)

    # Element label
    basic_label(element_frame, "Element:")

    # Stores element selection and sets default
    var_element = tk.StringVar(root)
    var_element.set(element)

    # Creates dropdown menu for element
    element_dropdown = AutocompleteCombobox(element_frame, textvariable=var_element,
                                            values=element_list, justify="center",
                                            style="Maize.TCombobox")
    element_dropdown.set_completion_list(element_list)
    element_dropdown.config(width=get_width(element_list))
    element_dropdown.set(element_list[0])
    element_dropdown.pack()
    element_dropdown.bind('<Return>', on_enter)
    element_dropdown.bind("<<ComboboxSelected>>", on_select_element)
    element_dropdown.bind("<FocusOut>", on_enter)

    # Logic for when an isotope is selected
    def on_select_isotope(event):
        nonlocal isotope

        event.widget.selection_clear()
        isotope = isotope_dropdown.get()
        root.focus()

    # Frame for isotope selection
    category_frame = tk.Frame(nuclide_side_frame, bg="#F2F2F2")
    category_frame.pack(side="left", padx=5)

    # Isotope label
    basic_label(category_frame, "Isotope:")

    # Creates dropdown menu for isotope
    isotope_choices = get_isotopes(element)
    isotope_dropdown = ttk.Combobox(category_frame, values=isotope_choices, justify="center",
                                    state='readonly', style="Maize.TCombobox")
    isotope_dropdown.config(width=get_width(isotope_choices))
    isotope_dropdown.set(isotope_choices[0])
    isotope_dropdown.pack()
    isotope_dropdown.bind("<<ComboboxSelected>>", on_select_isotope)

    # Spacer
    empty_frame2 = make_spacer(root)

    # Input/output box width
    entry_width = 28 if platform.system() == "Windows" else 32

    # Frame for result
    result_frame = SectionFrame(root, title=mode)
    result_frame.pack()
    inner_result_frame = result_frame.get_inner_frame()

    # Creates Calculate button
    calc_button = ttk.Button(inner_result_frame, text="Calculate",
                             style="Maize.TButton", padding=(0,0),
                             command=lambda: handle_calculation(root, mode, isotope, result_box))
    calc_button.config(width=get_width(["Calculate"]))
    calc_button.pack(pady=(20,5))

    # Result label
    result_label = ttk.Label(inner_result_frame, text="Result:",
                             style="Black.TLabel")
    result_label.pack(pady=(5,1))

    # Displays the result of calculation
    result_box = tk.Text(inner_result_frame, height=1, borderwidth=3, bd=3,
                         highlightthickness=0, relief='solid')
    result_box.config(bg='white', fg='black', state="disabled", width=entry_width,
                      font=monospace_font)
    result_box.pack(pady=(1,20))

    # Creates Exit button to return to home screen
    exit_button = ttk.Button(root, text="Exit", style="Maize.TButton",
                             padding=(0,0),
                             command=lambda: exit_to_home(root))
    exit_button.config(width=get_width(["Exit"]))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    main_list = [title_frame,
                 mode_frame, empty_frame1,
                 nuclide_frame, empty_frame2,
                 result_frame, exit_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the decay information main screen
in preparation for opening a different screen.
"""
def clear_main():
    global main_list

    # Clears decay information main screen
    for node in main_list:
        node.destroy()
    main_list.clear()

"""
This function transitions from the decay information main screen
to the home screen by first clearing the decay information main screen
and then creating the home screen.
It is called when the Exit button is hit.
"""
def exit_to_home(root):
    root.focus()
    from App.home import return_home
    clear_main()
    return_home(root)