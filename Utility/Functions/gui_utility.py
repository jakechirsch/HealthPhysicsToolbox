##### IMPORTS #####
from tkinter import *
import os
import subprocess
import platform

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
    spacer = Frame(root, bg="#00274C")
    spacer.pack(pady=10)
    return spacer