##### IMPORTS #####
import platform
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from App.style import SectionFrame
from App.scroll import scroll_to_top
from Utility.Functions.gui_utility import make_exit_button
from Utility.Functions.choices import get_choices, get_isotopes
from Core.Decay.Calculator.nuclide_calc import handle_calculation
from Utility.Functions.gui_utility import make_item_dropdown, make_category_dropdown
from Utility.Functions.gui_utility import make_dropdown, result_label, make_result_box
from Utility.Functions.gui_utility import basic_label, make_title_frame, make_unit_dropdown
from Utility.Functions.gui_utility import make_spacer, get_width, get_item, valid_saved

# For global access to nodes on decay calculator main screen
main_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the decay calculator main screen.
The following sections and widgets are created:
   Module Title (Decay Calculator)
   Select Calculation Mode section
   Select Nuclide section
   Input Details section
   Result section (title dependent on Calculation Mode)
   Exit button
This function contains all of the logic involving these widgets'
behaviors.
The sections and widgets are stored in main_list so they can be
accessed later by clear_main.
"""
def decay_calc_main(root, category="Common Elements", mode="Activities",
                    common_el="Ag", element="Ac"):
    global main_list

    # Makes title frame
    title_frame = make_title_frame(root, "Decay Calculator", "Decay/Calculator")

    # Creates font for result label and energy entry
    monospace_font = font.Font(family="Menlo", size=12)

    # Gets the element options
    choices = get_choices(category, "Decay", "")

    # Gets common elements
    common_elements = get_choices("Common Elements", "Decay", "")

    # Make sure common element is a valid selection
    common_el = valid_saved(common_el, common_elements)

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
        result_box.config(state="disabled", height=1)

        root.focus()

    # Creates dropdown menu for mode
    mode_choices = ["Activities",
                    "Plot"]
    _ = make_dropdown(inner_mode_frame, var_mode, mode_choices, select_mode, pady=20)

    # Spacer
    empty_frame1 = make_spacer(root)

    # Frame for nuclide selection
    nuclide_frame = SectionFrame(root, title="Select Nuclide")
    nuclide_frame.pack()
    inner_nuclide_frame = nuclide_frame.get_inner_frame()

    # Stores category selection and sets default
    var_category = tk.StringVar(root)
    var_category.set(category)

    # Logic for when an element category is selected
    def select_category(event):
        nonlocal choices, category, common_el, element, isotope

        event.widget.selection_clear()
        previous_element = get_item(category, common_el, "", element, "", "")
        category = var_category.get()

        # Updates element dropdown to match category
        choices = get_choices(category, "Decay", "")
        selected_element = get_item(category, common_el, "", element, "", "")
        var_element.set(selected_element)
        element_dropdown.set_completion_list(choices)
        element_dropdown.config(values=choices, width=get_width(choices))

        # Updates isotope dropdown to match element
        isotopes = get_isotopes(selected_element)
        if category == "Common Elements":
            if common_el != previous_element:
                isotope = isotopes[0]
        elif category == "All Elements":
            if element != previous_element:
                isotope = isotopes[0]
        var_isotope.set(isotope)
        isotope_dropdown.config(values=isotopes, width=get_width(isotopes))

        root.focus()

    # Frame for element category selection
    category_frame = tk.Frame(inner_nuclide_frame, bg="#F2F2F2")
    category_frame.pack(pady=(15, 5))

    # Category label
    basic_label(category_frame, "Category:")

    # Creates dropdown menu for category selection
    make_category_dropdown(category_frame, var_category, select_category, False)

    # Horizontal frame for nuclide selection
    nuclide_side_frame = tk.Frame(inner_nuclide_frame, bg="#F2F2F2")
    nuclide_side_frame.pack(pady=(20,30))

    # Logic for when enter is hit when using the element autocomplete combobox
    def on_enter(_):
        nonlocal common_el, element, isotope
        value = var_element.get()

        if value not in choices:
            # Falls back on default if invalid item is typed in
            var_element.set(get_item(category, common_el, "", element, "", ""))
        else:
            # Adjusts isotopes
            isotopes = get_isotopes(value)
            if category == "All Elements":
                if element != value:
                    isotope = isotopes[0]
                    element = value
            else:
                if common_el != value:
                    isotope = isotopes[0]
                    common_el = value
            var_isotope.set(isotope)
            isotope_dropdown.config(values=isotopes, width=get_width(isotopes))

        element_dropdown.selection_clear()
        element_dropdown.icursor(tk.END)

    # Logic for when an element is selected
    def on_select_element(event):
        nonlocal common_el, element, isotope

        event.widget.selection_clear()
        value = var_element.get()

        # Adjusts isotopes
        isotopes = get_isotopes(value)
        if category == "All Elements":
            if element != value:
                isotope = isotopes[0]
                element = value
        else:
            if common_el != value:
                isotope = isotopes[0]
                common_el = value
        var_isotope.set(isotope)
        isotope_dropdown.config(values=isotopes, width=get_width(isotopes))

        root.focus()

    # Frame for element selection
    element_frame = tk.Frame(nuclide_side_frame, bg="#F2F2F2")
    element_frame.pack(side="left", padx=5)

    # Element label
    basic_label(element_frame, "Element:")

    # Stores element selection and sets default
    var_element = tk.StringVar(root)
    var_element.set(get_item(category, common_el, "", element, "", ""))

    # Creates dropdown menu for element
    element_dropdown = make_item_dropdown(root, element_frame, var_element,
                                          choices, on_enter, on_select_element)

    # Logic for when an isotope is selected
    def on_select_isotope(event):
        nonlocal isotope

        event.widget.selection_clear()
        isotope = var_isotope.get()
        root.focus()

    # Frame for isotope selection
    isotope_frame = tk.Frame(nuclide_side_frame, bg="#F2F2F2")
    isotope_frame.pack(side="left", padx=5)

    # Isotope label
    basic_label(isotope_frame, "Isotope:")

    # Retrieves isotopes for current element
    isotope_choices = get_isotopes(get_item(category, common_el, "", element, "", ""))
    isotope = isotope_choices[0]

    # Stores isotope and sets default
    var_isotope = tk.StringVar(root)
    var_isotope.set(isotope)

    # Creates dropdown menu for isotope
    isotope_dropdown = make_dropdown(isotope_frame, var_isotope, isotope_choices,
                                     on_select_isotope)

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
    time_choices = ['μs', 'ms', 's', 'm', 'h', 'd', 'y']

    # Logic for when a time is selected
    def on_select_time_unit(event):
        nonlocal time_unit
        event.widget.selection_clear()
        root.focus()
        time_unit = event.widget.get()

    # Stores time unit and sets default
    var_time = tk.StringVar(root)
    var_time.set("s")

    # Creates dropdown menu for time unit
    _ = make_unit_dropdown(time_side_frame, var_time, time_choices, on_select_time_unit)

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

    # Stores initial amount type and sets default
    var_initial_type = tk.StringVar(root)
    var_initial_type.set("Activity (Bq)")

    # Creates dropdown menu for initial amount unit type
    _ = make_unit_dropdown(initial_side_frame, var_initial_type, initial_types, on_select_initial_type)

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
        "Activity (Bq)" : ["pBq", "nBq", "μBq", "mBq", "Bq", "kBq", "MBq", "GBq", "TBq"],
        "Activity (Ci)" : ["pCi", "nCi", "μCi", "mCi", "Ci", "kCi", "MCi", "GCi", "TCi"],
        "Activity (dpm)" : ["dpm"],
        "Mass" : ["pg", "ng", "μg", "mg", "g", "kg", "t"],
        "Moles" : ["pmol", "nmol", "μmol", "mmol", "mol", "kmol", "Mmol"],
        "Nuclei Number" : ["num"]
    }

    # Logic for when an initial amount unit is selected
    def on_select_initial_unit(event):
        nonlocal initial_unit
        event.widget.selection_clear()
        root.focus()
        initial_unit = event.widget.get()

    # Stores initial amount unit and sets default
    var_initial = tk.StringVar(root)
    var_initial.set("Bq")

    # Creates dropdown menu for initial amount unit
    initial_unit_dropdown = make_unit_dropdown(initial_side_frame, var_initial, initial_choices[initial_type],
                                               on_select_initial_unit)

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

    # Stores activity type and sets default
    var_activity_type = tk.StringVar(root)
    var_activity_type.set("Activity (Bq)")

    # Creates dropdown menu for activity unit type
    _ = make_unit_dropdown(activity_side_frame, var_activity_type, activity_types, on_select_activity_type)

    # Logic for when an activity unit is selected
    def on_select_activity_unit(event):
        nonlocal initial_unit
        event.widget.selection_clear()
        root.focus()
        initial_unit = event.widget.get()

    # Stores activity unit and sets default
    var_activity = tk.StringVar(root)
    var_activity.set("Bq")

    # Creates dropdown menu for initial amount unit
    activity_unit_dropdown = make_unit_dropdown(activity_side_frame, var_activity, initial_choices[activity_type],
                                                on_select_activity_unit)

    # Spacer
    empty_frame3 = make_spacer(root)

    # Frame for result
    result_frame = SectionFrame(root, title=mode)
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
    result_label(inner_result_frame)

    # Displays the result of calculation
    result_box = make_result_box(inner_result_frame)

    # Creates Advanced Settings button
    advanced_button = ttk.Button(root, text="Advanced Settings",
                                 style="Maize.TButton", padding=(0,0),
                                 command=lambda: to_advanced(root, category, mode,
                                                             common_el, element))
    advanced_button.config(width=get_width(["Advanced Settings"]))
    advanced_button.pack(pady=5)

    # Creates Exit button to return to home screen
    exit_button = make_exit_button(root, lambda: exit_to_home(root))

    # Stores nodes into global list
    main_list = [title_frame,
                 mode_frame, empty_frame1,
                 nuclide_frame, empty_frame2,
                 details_frame, empty_frame3,
                 result_frame, advanced_button, exit_button]


#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the decay calculator main screen
in preparation for opening a different screen.
"""

def clear_main():
    global main_list

    # Clears decay calculator main screen
    for node in main_list:
        node.destroy()
    main_list.clear()

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
    scroll_to_top()

"""
This function transitions from the decay calculator main screen
to the decay calculator advanced screen by first clearing the
decay calculator main screen and then creating the
decay calculator advanced screen.
It is called when the Advanced Settings button is hit.
"""
def to_advanced(root, category, mode, common_el, element):
    root.focus()
    from App.Decay.Calculator.decay_calc_advanced import decay_calc_advanced

    clear_main()
    decay_calc_advanced(root, category, mode, common_el, element)
    scroll_to_top()