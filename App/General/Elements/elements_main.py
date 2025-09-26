##### IMPORTS #####
import tkinter as tk
from tkinter import ttk
from App.style import SectionFrame
from Utility.Functions.gui_utility import make_exit_button
from Core.General.Elements.elements import handle_calculation
from Utility.Functions.gui_utility import make_spacer, get_width
from Utility.Functions.logic_utility import get_item, valid_saved
from Utility.Functions.choices import get_choices, read_pt_columns
from Utility.Functions.gui_utility import make_dropdown, make_result_box
from Utility.Functions.gui_utility import make_item_dropdown, make_category_dropdown
from Utility.Functions.gui_utility import basic_label, result_label, make_title_frame

# For global access to nodes on elements main screen
main_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

def elements_main(root, category="Common Elements", mode="Atomic Number",
                  common_el="Ag", element="Ac", am_num="g", am_den="mol"):
    global main_list

    # Makes title frame
    title_frame = make_title_frame(root, "Element Information", "General/Elements")

    # Gets the element options
    choices = get_choices(category, "General", "")

    # Gets common elements
    common_elements = get_choices("Common Elements", "General", "")

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
        result_box.config(state="disabled")

        root.focus()

    # Creates dropdown menu for mode
    mode_choices = []
    read_pt_columns(mode_choices)
    _ = make_dropdown(inner_mode_frame, var_mode, mode_choices, select_mode, pady=20)

    # Spacer
    empty_frame1 = make_spacer(root)

    # Frame for element selection
    main_element_frame = SectionFrame(root, title="Select Element")
    main_element_frame.pack()
    inner_element_frame = main_element_frame.get_inner_frame()

    # Stores category selection and sets default
    var_category = tk.StringVar(root)
    var_category.set(category)

    # Logic for when an element category is selected
    def select_category(event):
        nonlocal choices, category, common_el, element

        event.widget.selection_clear()
        category = var_category.get()

        # Updates element dropdown to match category
        choices = get_choices(category, "General", "")
        var_element.set(get_item(category, common_el, "", element, "", ""))
        element_dropdown.set_completion_list(choices)
        element_dropdown.config(values=choices, width=get_width(choices))
        root.focus()

    # Frame for element category selection
    category_frame = tk.Frame(inner_element_frame, bg="#F2F2F2")
    category_frame.pack(pady=(15,5))

    # Category label
    basic_label(category_frame, "Category:")

    # Creates dropdown menu for category selection
    make_category_dropdown(category_frame, var_category, select_category, False)

    # Logic for when enter is hit when using the element autocomplete combobox
    def on_enter(_):
        nonlocal common_el, element
        value = var_element.get()

        if value not in choices:
            # Falls back on default if invalid element is typed in
            var_element.set(get_item(category, common_el, "", element, "", ""))
        else:
            # Stores most recent items
            if category == "All Elements":
                element = value
            else:
                common_el = value

        element_dropdown.selection_clear()
        element_dropdown.icursor(tk.END)

    # Frame for element selection
    element_frame = tk.Frame(inner_element_frame, bg="#F2F2F2")
    element_frame.pack(pady=(5,20))

    # Element label
    basic_label(element_frame, "Element:")

    # Stores element selection and sets default
    var_element = tk.StringVar(root)
    var_element.set(get_item(category, common_el, "", element, "", ""))

    # Creates dropdown menu for element
    element_dropdown = make_item_dropdown(root, element_frame, var_element, choices, on_enter)

    # Spacer
    empty_frame2 = make_spacer(root)

    # Frame for result
    result_frame = SectionFrame(root, title=mode)
    result_frame.pack()
    inner_result_frame = result_frame.get_inner_frame()

    # Creates Calculate button
    calc_button = ttk.Button(inner_result_frame, text="Calculate",
                             style="Maize.TButton", padding=(0,0),
                             command=lambda: handle_calculation(root, mode, var_element.get(),
                                                                result_box, am_num, am_den))
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
                                                             common_el, element,
                                                             am_num, am_den))
    advanced_button.config(width=get_width(["Advanced Settings"]))
    advanced_button.pack(pady=5)

    # Creates Exit button to return to home screen
    exit_button = make_exit_button(root, lambda: exit_to_home(root))

    # Stores nodes into global list
    main_list = [title_frame,
                 mode_frame, empty_frame1,
                 main_element_frame, empty_frame2,
                 result_frame, advanced_button, exit_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the elements main screen
in preparation for opening a different screen.
"""
def clear_main():
    global main_list

    # Clears elements main screen
    for node in main_list:
        node.destroy()
    main_list.clear()

"""
This function transitions from the elements main screen
to the home screen by first clearing the elements main screen
and then creating the home screen.
It is called when the Exit button is hit.
"""
def exit_to_home(root):
    root.focus()
    from App.home import return_home
    clear_main()
    return_home(root)

"""
This function transitions from the elements main screen
to the elements advanced screen by first clearing the
elements main screen and then creating the
elements advanced screen.
It is called when the Advanced Settings button is hit.
"""
def to_advanced(root, category, mode, common_el, element, am_num, am_den):
    root.focus()
    from App.General.Elements.elements_advanced import elements_advanced

    clear_main()
    elements_advanced(root, category, mode, common_el, element, am_num, am_den)