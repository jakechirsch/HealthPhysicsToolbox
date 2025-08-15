##### IMPORTS #####
import math
import tkinter as tk
import radioactivedecay as rd
import matplotlib.pyplot as plt

#####################################################################################
# CALCULATIONS SECTION
#####################################################################################

"""
This function is called when the Calculate button is hit.
The function decides what calculation to perform
based on the selected calculation mode.
"""
def handle_calculation(root, mode, isotope, initial, initial_unit, time, time_unit,
                       activity_unit, result_box):
    root.focus()
    match mode:
        case "Activities":
            nuclide_activities(isotope, initial, initial_unit, time, time_unit,
                               activity_unit, result_box)
        case "Plot":
            nuclide_plot(isotope, initial, initial_unit, time, time_unit,
                         activity_unit, result_box)

"""
This function retrieves the activities
given a particular isotope, initial amount, and time.
"""
def nuclide_activities(isotope, initial, initial_unit, time, time_unit,
                       activity_unit, result_box):
    # Clears result box
    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)

    # Error checks
    if is_error(isotope, time, initial, result_box):
        return
    else:
        time = float(time)
        initial = float(initial)

    # Retrieves activities
    t0 = rd.Inventory({isotope: initial}, initial_unit)
    t1 = t0.decay(time, time_unit)
    activities = t1.activities(activity_unit)

    # Fills result box
    for activity in activities:
        result_box.insert(tk.END, f"{activity}, {activities[activity]}\n")
    result_box.config(state="disabled", height=len(activities))

"""
This function retrieves the activities plot
given a particular isotope, initial amount, and time.
"""
def nuclide_plot(isotope, initial, initial_unit, time, time_unit,
                 activity_unit, result_box):
    # Clears result box
    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)

    # Error checks
    if is_error(isotope, time, initial, result_box):
        return
    else:
        time = float(time)
        initial = float(initial)

    # Retrieves plot
    t0 = rd.Inventory({isotope: initial}, initial_unit)
    t0.plot(time, time_unit, yunits=activity_unit)

    # Fills result box
    result_box.insert(tk.END, "Plotted!")
    result_box.config(state="disabled", height=1)

    # Shows plot
    plt.title(isotope, fontsize=12)
    plt.show()

"""
This function handles the error-checking for activities.
The function handles the following errors:
   Non-number time input
   Time cannot be negative
   Non-number initial input
   Initial cannot be negative
   Isotope is stable
The function returns a bool indicating whether or not
an error occurred.
"""
def is_error(isotope, time, initial, result_box):
    # Error check for a non-number time input
    try:
        time = float(time)
    except ValueError:
        result_box.insert(tk.END, "Error: Non-number time input.")
        result_box.config(state="disabled", height=1)
        return True

    # Error check for a negative time input
    if time < 0:
        result_box.insert(tk.END, "Error: Time cannot be negative.")
        result_box.config(state="disabled", height=1)
        return True

    # Error check for a non-number initial input
    try:
        initial = float(initial)
    except ValueError:
        result_box.insert(tk.END, "Error: Non-number initial input.")
        result_box.config(state="disabled", height=1)
        return True

    # Error check for a negative initial input
    if initial < 0:
        result_box.insert(tk.END, "Error: Initial cannot be negative.")
        result_box.config(state="disabled", height=1)
        return True

    # Error check for stable isotope
    if math.isinf(rd.Nuclide(isotope).half_life()):
        result_box.insert(tk.END, "Isotope " + isotope + " is stable.")
        result_box.config(state="disabled", height=1)
        return True

    return False