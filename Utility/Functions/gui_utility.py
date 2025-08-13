##### IMPORTS #####
import platform
import tkinter as tk
from tkinter import ttk
import tkinter.font as font

#####################################################################################
# ERRORS SECTION
#####################################################################################

### ERROR MESSAGES ###
no_selection = "Error: No selected item."
non_number = "Error: Non-number energy input."
too_low = "Error: Energy too low."
too_high = "Error: Energy too high."
errors = [no_selection, non_number, too_low, too_high]

#####################################################################################
# GUI SECTION
#####################################################################################

"""
This function edits the contents of the result label.
The label needs to be enabled at the start and disabled
at the end in order to prevent the user from being able
to input text.
The previous results are cleared and then the new
results are inserted. If the text being displayed is not
an error, the unit is assed to the end.
"""
def edit_result(result, result_label, num="", den=""):
    # Clears result label and inserts new result
    result_label.config(state="normal")
    result_label.delete("1.0", tk.END)
    result_label.insert(tk.END, result)
    unit = num + "/" + den
    if num == "1":
        unit = den + "\u207B\u00B9"
    if not result in errors and num != "":
        result_label.insert(tk.END, " ")
        result_label.insert(tk.END, unit)
    result_label.config(state="disabled")

"""
This function makes an empty "spacer" frame with y-padding.
This is used to control the space between sections.
"""
def make_spacer(root):
    spacer = tk.Frame(root, bg="#F2F2F2")
    spacer.pack(pady=6)
    return spacer

"""
This function makes a checkbox for an interaction type.
Used for the interaction settings in both the advanced settings
and the export menu.
There is no padding in between checkboxes.
"""
def interaction_checkbox(frame, variable, interaction, command):
    check = ttk.Checkbutton(frame, text=interaction, variable=variable,
                            style="Maize.TCheckbutton", command=command)
    check.pack(anchor="w")

"""
This function makes a Combobox dropdown for units selections.
"""
def unit_dropdown(frame, choices, unit, on_select_u):
    dropdown = ttk.Combobox(frame, values=choices, justify="center", state='readonly',
                            style="Maize.TCombobox")
    dropdown.config(width=get_width(choices))
    dropdown.set(unit)
    dropdown.pack(side='left', padx=5)
    dropdown.bind("<<ComboboxSelected>>", on_select_u)

"""
This function is used to make an overall module title.
The titles also have a tooltip for more info.
The title label and tooltip are packed into a frame and returned.
"""
def make_title_frame(root, title, module):
    from App.style import Tooltip

    title_frame = tk.Frame(root, bg="#F2F2F2")
    title_frame.pack()

    title = ttk.Label(title_frame, text=title, style="Blue.TLabel")
    title.pack(side="left", padx=2, pady=(20, 10))

    info_icon = ttk.Label(title_frame, text="\u24D8", style="Blue.TLabel", cursor="hand2")
    info_icon.pack(side="left", padx=2, pady=(20, 10))
    Tooltip(info_icon, module)

    return title_frame

"""
This function makes a basic label and packs it in the provided frame.
"""
def basic_label(frame, text):
    label = ttk.Label(frame, text=text, style="Black.TLabel")
    label.pack()

"""
This function makes a horizontal frame with a label and an entry.
It is used for both the Enter Material Name and Enter Density sections
in Export menus.
"""
def make_entry_line(frame, text):
    # Creates font
    monospace_font = font.Font(family="Menlo", size=12)

    # Input/output box width
    entry_width = 22 if platform.system() == "Windows" else 32

    label = ttk.Label(frame, text=text, style="Black.TLabel")
    entry = tk.Entry(frame, width=entry_width, insertbackground="black",
                     background="white", foreground="black",
                     borderwidth=3, bd=3, highlightthickness=0, relief='solid',
                     font=monospace_font)
    label.pack(side="left", padx=(0,5))
    entry.pack(side="left", padx=(5,0), pady=20)
    return entry

def make_weights_line(frame):
    # Creates font
    monospace_font = font.Font(family="Menlo", size=12)

    # Input/output box width
    entry_width = 16 if platform.system() == "Windows" else 20

    # Frame for element weights example
    ex_frame = tk.Frame(frame, bg="#F2F2F2")
    ex_frame.pack(side="left", padx=(0,30))

    # Element weights label
    basic_label(ex_frame, "Element Weights:")

    # Element weights entry
    entry = tk.Text(frame, width=entry_width, height=10, bg='white', fg='black',
                    insertbackground="black", borderwidth=3, bd=3,
                    highlightthickness=0, relief='solid', font=monospace_font)
    entry.pack(side="left", padx=(30,0), pady=20)

    # Make element weights example
    basic_label(ex_frame, "")
    basic_label(ex_frame, "Example:")
    basic_label(ex_frame, "0.30, Pb")
    basic_label(ex_frame, "0.55, Si")
    basic_label(ex_frame, "0.13, O")
    basic_label(ex_frame, "0.02, K")

    return entry

#####################################################################################
# FULL FRAME SECTION
#####################################################################################

"""
This function creates a vertical frame dependent on the
action and category for Customize Categories settings.
If action is Add and category is Custom Materials,
we create the Add Custom Materials button to direct
to the photon attenuation add custom screen.
Otherwise, we find the choices for the selected
action and category, and create a label, an item dropdown,
and a button to carry out the action.
"""
def make_vertical_frame(root, top_frame, action, category_ar,
                        non_common, common, non_common_m, common_m, custom,
                        button, to_custom):
    from App.style import AutocompleteCombobox
    from Utility.Functions.customize import carry_action

    # Clear previous button
    button[0].destroy()

    # Make vertical frame
    vertical_frame = tk.Frame(top_frame, bg="#F2F2F2")
    vertical_frame.pack(pady=(5,20))

    if action == "Add" and category_ar == "Custom Materials":
        # Creates Add Custom Materials button
        button[0] = ttk.Button(vertical_frame, text="Add Custom Materials",
                               style="Maize.TButton", padding=(0,0),
                               command=lambda: to_custom())
        button[0].config(width=get_width(["Add Custom Materials"]))
        button[0].pack(pady=(10,0))
        return vertical_frame

    # Stores item
    var = tk.StringVar(root)
    choices = []
    inverse = []
    if action == "Add" and category_ar == "Common Elements":
        var.set(valid_saved("", non_common))
        choices = non_common
        inverse = common
    elif action == "Add" and category_ar == "Common Materials":
        var.set(valid_saved("", non_common_m))
        choices = non_common_m
        inverse = common_m
    elif action == "Remove" and category_ar == "Common Elements":
        var.set(valid_saved("", common))
        choices = common
        inverse = non_common
    elif action == "Remove" and category_ar == "Common Materials":
        var.set(valid_saved("", common_m))
        choices = common_m
        inverse = non_common_m
    elif action == "Remove" and category_ar == "Custom Materials":
        var.set(valid_saved("", custom))
        choices = custom

    # Item label
    basic_label(vertical_frame, "Item:")

    # Logic for when an interacting medium item is selected
    def on_select(event):
        event.widget.selection_clear()
        root.focus()

    # Logic for when enter is hit when using the item autocomplete combobox
    def on_enter(_):
        value = var.get()
        value = valid_saved(value, choices)
        var.set(value)
        item_dropdown.selection_clear()
        item_dropdown.icursor(tk.END)

    # Creates dropdown menu for interacting medium item selection
    # to be added or removed
    item_dropdown = AutocompleteCombobox(vertical_frame, textvariable=var,
                                         values=choices, justify="center",
                                         style="Maize.TCombobox")
    item_dropdown.set_completion_list(choices)
    item_dropdown.config(width=get_width(choices))
    item_dropdown.pack()
    item_dropdown.bind('<Return>', on_enter)
    item_dropdown.bind("<<ComboboxSelected>>", on_select)
    item_dropdown.bind("<FocusOut>", on_enter)

    # Creates button
    button[0] = ttk.Button(vertical_frame, text=action,
                           style="Maize.TButton", padding=(0,0),
                           command=lambda: carry_action(root, action, category_ar,
                                                        choices, inverse, var,
                                                        item_dropdown))
    button[0].config(width=get_width([action]))
    button[0].pack(pady=(10,0))

    return vertical_frame

#####################################################################################
# LOGIC SECTION
#####################################################################################

"""
This function returns the list of selected interactions
given the list of all interactions and the list of the
variables storing whether or not each interaction is selected.
"""
def get_interactions(interaction_choices, interaction_vars):
    return [interaction_choices[x] for x in range(len(interaction_choices))
            if interaction_vars[x].get() == 1]

"""
This function defaults a saved item choice to the first in the list
of options in case it was removed from the category. If the list of
options is empty, it defaults to an empty string.
"""
def valid_saved(saved, choices):
    return saved if saved in choices else choices[0] if len(choices) > 0 else ""

"""
This function returns the correct saved item based on the selected category.
"""
def get_item(category, common_el, common_mat, element, material, custom_mat):
    return common_el if category == "Common Elements" else\
           common_mat if category == "Common Materials" else\
           element if category == "All Elements" else\
           material if category == "All Materials" else\
           custom_mat if category == "Custom Materials" else ""

"""
This function returns the relevant item based on the
calculation mode.
It is used in two cases:
1. To retrieve the correct unit out of the saved units
   of each mode
2. To retrieve the correct list of unit choices for the
   selected mode
"""
def get_unit(units, modes, mode):
    return dict(zip(modes, units))[mode]

#####################################################################################
# FONT SECTION
#####################################################################################

"""
This function measures each string in a list in the provided font
and returns the widest string's measurement.
"""
def get_max_string_pixel_width(strings, font_obj):
    return max(font_obj.measure(s) for s in strings) if len(strings) > 0 else 2

"""
This function converts the widest string in a list to a pixel width.
Used for determining dropbox width to fit the longest option.
"""
def get_width(choices):
    # Measures the width of the longest dropdown option in the device's default font
    font_obj = font.nametofont("TkDefaultFont")  # or the font you set in the style
    max_width_px = get_max_string_pixel_width(choices, font_obj)

    # Convert pixels to character width approx
    avg_char_width = font_obj.measure("0")
    char_width = int(max_width_px / avg_char_width) + 2  # +2 for padding/margin

    return char_width