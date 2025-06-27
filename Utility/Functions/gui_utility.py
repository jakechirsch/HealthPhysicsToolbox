##### IMPORTS #####
from tkinter import *
from tkinter import ttk
import os
import subprocess
import platform
import tkinter.font as tk_font

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