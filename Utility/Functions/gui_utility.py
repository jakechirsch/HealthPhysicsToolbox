##### IMPORTS #####
from tkinter import *
from tkinter import ttk
import os
import subprocess
import platform
import tkinter.font as tk_font
import sys
from pathlib import Path

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
    result_label.delete("1.0", END)
    result_label.insert(END, result)
    unit = num + "/" + den
    if num == "1":
        unit = den + "\u207B\u00B9"
    if not result in errors:
        result_label.insert(END, " ")
        result_label.insert(END, unit)
    result_label.config(state="disabled")

"""
This function makes an empty "spacer" frame with y-padding.
This is used to control the space between sections.
"""
def make_spacer(root):
    spacer = Frame(root, bg="#F2F2F2")
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
This function is used to make an overall module title.
The titles also have a tooltip for more info.
The title label and tooltip are packed into a frame and returned.
"""
def make_title_frame(root, title):
    from App.style import Tooltip

    title_frame = Frame(root, bg="#F2F2F2")
    title_frame.pack()

    title = ttk.Label(title_frame, text=title, style="Blue.TLabel")
    title.pack(side="left", padx=2, pady=(20, 10))

    info_icon = ttk.Label(title_frame, text="\u24D8", style="Blue.TLabel", cursor="hand2")
    info_icon.pack(side="left", padx=2, pady=(20, 10))
    Tooltip(info_icon, "Info")

    return title_frame

"""
This function makes a basic label and packs it in the provided frame.
"""
def basic_label(frame, text):
    label = ttk.Label(frame, text=text, style="Black.TLabel")
    label.pack()

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

#####################################################################################
# FONT SECTION
#####################################################################################

"""
This function measures each string in a list in the provided font
and returns the widest string's measurement.
"""
def get_max_string_pixel_width(strings, font):
    return max(font.measure(s) for s in strings) if len(strings) > 0 else 2

"""
This function converts the widest string in a list to a pixel width.
Used for determining dropbox width to fit the longest option.
"""
def get_width(choices):
    # Measures the width of the longest dropdown option in the device's default font
    font = tk_font.nametofont("TkDefaultFont")  # or the font you set in the style
    max_width_px = get_max_string_pixel_width(choices, font)

    # Convert pixels to character width approx
    avg_char_width = font.measure("0")
    char_width = int(max_width_px / avg_char_width) + 2  # +2 for padding/margin

    return char_width

#####################################################################################
# FILES SECTION
#####################################################################################

"""
This function opens a file given the path to the file.
Used for opening References.txt, Help.txt, or exported plot/data.
"""
def open_file(path):
    if platform.system() == 'Windows':
        os.startfile(path)
    elif platform.system() == 'Darwin':  # macOS
        subprocess.run(['open', path])
    else:  # Assume Linux or Unix
        subprocess.run(['xdg-open', path])

"""
This function finds the true path to a file given the relative path.
Used for opening a data file, References.txt, or Help.txt.
This function is necessary due to potential path differences depending
on whether you are running in an IDE/terminal or an executable.
"""
def resource_path(relative_path):
    # Returns absolute path to bundled resource
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

"""
This function finds the true path to user data given the relative path.
Used for opening a shelve db file.
This function is necessary due to potential path differences depending
on whether you are running in an IDE/terminal or an executable.
"""
def get_user_data_path(relative_path):
    # Return a path in a writable location
    if getattr(sys, 'frozen', False):
        # If bundled with PyInstaller, get folder of the executable
        base_dir = Path(sys.executable).parent
    else:
        # If running as script
        base_dir = Path(sys.argv[0]).resolve().parent

    full_path = base_dir / "UserData" / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure subdirectories exist
    return str(full_path)

"""
This function configures matplotlib in advance.
This saves time when trying to load advanced settings while
using the app.
"""
def set_mpl_cache_dir():
    if getattr(sys, 'frozen', False):
        # Use a bundled folder inside the executable's directory
        base_dir = Path(sys.executable).parent
        cache_dir = base_dir / "matplotlib_cache"
    else:
        # When running as script, use normal cache dir
        cache_dir = Path.home() / ".matplotlib"

    # Make sure the directory exists
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Tell matplotlib to use this directory for its config (including font cache)
    os.environ["MPLCONFIGDIR"] = str(cache_dir)