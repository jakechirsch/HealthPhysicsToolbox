##### IMPORTS #####
import platform
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from App.style import AutocompleteCombobox, SectionFrame
from Utility.Functions.choices import get_choices, get_isotopes
from Utility.Functions.gui_utility import make_spacer, get_width
from Core.Decay.Calculator.nuclide_calc import handle_calculation
from Utility.Functions.gui_utility import basic_label, make_title_frame, unit_dropdown

# For global access to nodes on photon attenuation main screen
calc_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

def decay_calc_main(root, mode_start="Activities", element="Ac", isotope="Ac-223"):
    global calc_list

    # Makes title frame
    title_frame = make_title_frame(root, "Decay Calculator", "Decay/Calculator")

    # Creates font for result label and energy entry
    monospace_font = font.Font(family="Menlo", size=12)

    # Gets the item options
    element_list = get_choices("All Elements", "Decay", "")

    # Stores mode and sets default
    var_mode = tk.StringVar(root)
    var_mode.set(mode_start)
    mode = mode_start

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
        result_box.config(state="disabled", height=1)

        root.focus()

    # Creates dropdown menu for mode
    mode_choices = ["Activities",
                    "Plot"]
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

    # Frame for details
    details_frame = SectionFrame(root, title="Input Details")
    details_frame.pack()
    inner_details_frame = details_frame.get_inner_frame()

    # Horizontal frame for time
    time_side_frame = tk.Frame(inner_details_frame, bg="#F2F2F2")
    time_side_frame.pack(pady=20)

    # Time label
    time_label = ttk.Label(time_side_frame, text="Time:", style="Black.TLabel")
    time_label.pack(side='left', padx=5)

    # Variable to hold time unit input
    time_unit = "s"

    # Input box width
    small_entry_width = 7 if platform.system() == "Windows" else 8

    # Time input
    time_input = tk.Entry(time_side_frame, width=small_entry_width, insertbackground="black",
                          background="white", foreground="black", borderwidth=3, bd=3,
                          highlightthickness=0, relief='solid', font=monospace_font)
    time_input.pack(side='left', padx=5)

    # Possible unit choices
    time_choices = ['µs', 'ms', 's', 'm', 'h', 'd', 'y']

    # Logic for when a time is selected
    def on_select_time_unit(event):
        nonlocal time_unit
        event.widget.selection_clear()
        root.focus()
        time_unit = event.widget.get()

    # Creates dropdown menu for time unit
    unit_dropdown(time_side_frame, time_choices, "s", on_select_time_unit)

    # Horizontal frame for initial amount
    initial_side_frame = tk.Frame(inner_details_frame, bg="#F2F2F2")
    initial_side_frame.pack(pady=20)

    # Initial amount label
    initial_label = ttk.Label(initial_side_frame, text="Initial Amount:", style="Black.TLabel")
    initial_label.pack(side='left', padx=5)

    # Variable to hold initial unit type input
    initial_type = "Activity (Bq)"

    # Variable to hold initial amount unit input
    initial_unit = "Bq"

    # Initial amount input
    initial_input = tk.Entry(initial_side_frame, width=small_entry_width, insertbackground="black",
                             background="white", foreground="black", borderwidth=3, bd=3,
                             highlightthickness=0, relief='solid', font=monospace_font)
    initial_input.pack(side='left', padx=5)

    # Possible unit types
    initial_types = ["Activity (Bq)",
                     "Activity (Ci)",
                     "Activity (dpm)",
                     "Mass",
                     "Moles",
                     "Nuclei Number"]

    # Logic for when an initial type is selected
    def on_select_initial_type(event):
        nonlocal initial_type, initial_unit
        event.widget.selection_clear()
        new_type = event.widget.get()

        # Adjusts unit choices
        unit_choices = initial_choices[new_type]
        if initial_type != new_type:
            initial_unit = default_choices[new_type]
            initial_type = new_type
        initial_unit_dropdown.set(initial_unit)
        initial_unit_dropdown.config(values=unit_choices, width=get_width(unit_choices))

        initial_type = event.widget.get()
        root.focus()

    # Creates dropdown menu for initial amount unit type
    unit_dropdown(initial_side_frame, initial_types, "Activity (Bq)", on_select_initial_type)

    # Possible unit choices
    default_choices = {
        "Activity (Bq)": "Bq",
        "Activity (Ci)": "Ci",
        "Activity (dpm)": "dpm",
        "Mass": "g",
        "Moles": "mol",
        "Nuclei Number": "num"
    }
    initial_choices = {
        "Activity (Bq)" : ["pBq", "nBq", "µBq", "mBq", "Bq", "kBq", "MBq", "GBq", "TBq"],
        "Activity (Ci)" : ["pCi", "nCi", "µCi", "mCi", "Ci", "kCi", "MCi", "GCi", "TCi"],
        "Activity (dpm)" : ["dpm"],
        "Mass" : ["pg", "ng", "µg", "mg", "g", "kg", "t"],
        "Moles" : ["pmol", "nmol", "µmol", "mmol", "mol", "kmol", "Mmol"],
        "Nuclei Number" : ["num"]
    }

    # Logic for when an initial amount unit is selected
    def on_select_initial_unit(event):
        nonlocal initial_unit
        event.widget.selection_clear()
        root.focus()
        initial_unit = event.widget.get()

    # Creates dropdown menu for initial amount unit
    initial_unit_dropdown = ttk.Combobox(initial_side_frame, values=initial_choices[initial_type],
                                         justify="center", state='readonly',
                                         style="Maize.TCombobox")
    initial_unit_dropdown.config(width=get_width(initial_choices[initial_type]))
    initial_unit_dropdown.set("Bq")
    initial_unit_dropdown.pack(side='left', padx=5)
    initial_unit_dropdown.bind("<<ComboboxSelected>>", on_select_initial_unit)

    # Horizontal frame for initial amount
    activity_side_frame = tk.Frame(inner_details_frame, bg="#F2F2F2")
    activity_side_frame.pack(pady=20)

    # Initial amount label
    activity_label = ttk.Label(activity_side_frame, text="Activity Unit:", style="Black.TLabel")
    activity_label.pack(side='left', padx=5)

    # Variable to hold activity unit type input
    activity_type = "Activity (Bq)"

    # Variable to hold activity unit input
    activity_unit = "Bq"

    # Possible unit types
    activity_types = ["Activity (Bq)",
                      "Activity (Ci)",
                      "Activity (dpm)"]

    # Logic for when an activity type is selected
    def on_select_activity_type(event):
        nonlocal activity_type, activity_unit
        event.widget.selection_clear()
        new_type = event.widget.get()

        # Adjusts unit choices
        unit_choices = initial_choices[new_type]
        if activity_type != new_type:
            activity_unit = default_choices[new_type]
            activity_type = new_type
        activity_unit_dropdown.set(activity_unit)
        activity_unit_dropdown.config(values=unit_choices, width=get_width(unit_choices))

        activity_type = event.widget.get()
        root.focus()

    # Creates dropdown menu for activity unit type
    unit_dropdown(activity_side_frame, activity_types, "Activity (Bq)", on_select_activity_type)

    # Logic for when an activity unit is selected
    def on_select_initial_unit(event):
        nonlocal initial_unit
        event.widget.selection_clear()
        root.focus()
        initial_unit = event.widget.get()

    # Creates dropdown menu for initial amount unit
    activity_unit_dropdown = ttk.Combobox(activity_side_frame, values=initial_choices[activity_type],
                                          justify="center", state='readonly',
                                          style="Maize.TCombobox")
    activity_unit_dropdown.config(width=get_width(initial_choices[activity_type]))
    activity_unit_dropdown.set("Bq")
    activity_unit_dropdown.pack(side='left', padx=5)
    activity_unit_dropdown.bind("<<ComboboxSelected>>", on_select_initial_unit)

    # Spacer
    empty_frame3 = make_spacer(root)

    # Input/output box width
    entry_width = 28 if platform.system() == "Windows" else 32

    # Frame for result
    result_frame = SectionFrame(root, title=mode_start)
    result_frame.pack()
    inner_result_frame = result_frame.get_inner_frame()

    # Creates Calculate button
    calc_button = ttk.Button(inner_result_frame, text="Calculate",
                             style="Maize.TButton", padding=(0,0),
                             command=lambda: handle_calculation(root, mode, isotope,
                                                            initial_input.get(), initial_unit,
                                                                time_input.get(), time_unit,
                                                                activity_unit,
                                                                result_box))
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
    calc_list = [title_frame,
                 mode_frame, empty_frame1,
                 nuclide_frame, empty_frame2,
                 details_frame, empty_frame3,
                 result_frame, exit_button]


#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the decay calculator main screen
in preparation for opening a different screen.
"""

def clear_main():
    global calc_list

    # Clears decay calculator main screen
    for node in calc_list:
        node.destroy()
    calc_list.clear()

"""
This function transitions from the decay calculator main screen
to the home screen by first clearing the decay calculator main screen
and then creating the home screen.
It is called when the Exit button is hit.
"""

def exit_to_home(root):
    root.focus()
    from App.home import return_home
    clear_main()
    return_home(root)