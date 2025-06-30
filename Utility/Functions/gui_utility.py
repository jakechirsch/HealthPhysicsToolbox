##### IMPORTS #####
from tkinter import *
from tkinter import ttk
import os
import subprocess
import platform
import tkinter.font as tk_font
import sys
from pathlib import Path

### ERROR MESSAGES ###
non_number = "Error: Non-number energy input."
too_low = "Error: Energy too low."
too_high = "Error: Energy too high."
errors = [non_number, too_low, too_high]

def edit_result(result, result_label, num="", den=""):
    # Clears result label and inserts new result
    result_label.config(state="normal")
    result_label.delete("1.0", END)
    result_label.insert(END, result)
    if not result in errors:
        result_label.insert(END, " ")
        result_label.insert(END, num)
        result_label.insert(END, "/")
        result_label.insert(END, den)
    result_label.config(state="disabled")

def open_file(path):
    if platform.system() == 'Windows':
        os.startfile(path)
    elif platform.system() == 'Darwin':  # macOS
        subprocess.run(['open', path])
    else:  # Assume Linux or Unix
        subprocess.run(['xdg-open', path])

def resource_path(relative_path):
    # Returns absolute path to bundled resource
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

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

def make_spacer(root):
    spacer = Frame(root, bg="#D3D3D3")
    spacer.pack(pady=8)
    return spacer

def interaction_checkbox(frame, variable, interaction, command):
    check = ttk.Checkbutton(frame, text=interaction, variable=variable,
                            style="Maize.TCheckbutton", command=command)
    check.pack()

def get_max_string_pixel_width(strings, font):
    return max(font.measure(s) for s in strings) if len(strings) > 0 else 2

def get_width(choices):
    # Measures the width of the longest dropdown option in the device's default font
    font = tk_font.nametofont("TkDefaultFont") # or the font you set in the style
    max_width_px = get_max_string_pixel_width(choices, font)

    # Convert pixels to character width approx
    avg_char_width = font.measure("0")
    char_width = int(max_width_px / avg_char_width) + 2 # +2 for padding/margin

    return char_width