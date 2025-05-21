##### IMPORTS #####
import csv
import os
import tkinter as tk

##### WINDOW SETUP #####
root = tk.Tk()
root.title("Coefficient Request")
root.geometry("300x200")

##### HOME SCREEN BUTTONS #####
tac_button = tk.Button(root)

# For global access to nodes on non-home screen
screen_list = []

# Displays the requested coefficient
result_label = tk.Label(root, text="")

# Tracks what screen app is on
# Empty string represents home screen
screen = ""

def total_attenuation_coefficient():
    global tac_button
    global screen
    global screen_list

    # Obtains list of elements and sorts them alphabetically
    x: list[str] = [s[0:2] for s in os.listdir(os.getcwd()+'/attenuation') if s[2:] == '.csv']
    x.sort()

    # Changes to T.A.C. screen
    tac_button.pack_forget()
    screen = "tac"

    # Stores element selection and sets default
    var = tk.StringVar(root)
    var.set('Ac')

    # Creates dropdown menu for element selection
    dropdown = tk.OptionMenu(root, var, *x)
    dropdown.pack(pady=10)

    # Creates label for energy input
    label = tk.Label(root, text="Energy:")
    label.pack()

    # Creates input box for energy input
    entry = tk.Entry(root, width=30)
    entry.config(bg='white', fg='grey')
    entry.pack()

    # Creates calculate button
    calc = tk.Button(root, text="Calculate",
                       command=lambda: find_tac(var.get(), entry.get()))
    calc.pack(pady=5)

    # Creates exit button to return to home screen
    exit_button = tk.Button(root, text="Exit", command=clear)
    exit_button.pack(pady=5)

    # Stores nodes into global list
    screen_list = [dropdown, label, entry, calc, exit_button]

def find_tac(element, energy_str):
    global result_label

    # Removes result label from past calculations
    result_label.pack_forget()

    # Error-check for a non-number energy input
    try:
        energy_target = float(energy_str)
    except ValueError:
        result_label = tk.Label(root, text="Error: Non-number energy input.")
        result_label.pack(pady=5)
        return

    # Variables for the nearest energy value on either side
    closest_low = 0.0
    closest_high = float('inf')

    # Variables for the T.A.C. of the nearest energy values on either side
    low_coefficient = 0.0
    high_coefficient = float('inf')

    # Opens file
    with open('attenuation/' + element + '.csv', 'r') as file:
        # Reads in file in dictionary format
        reader = csv.DictReader(file)

        for row in reader:
            # Retrieves energy value of row
            energy = float(row["Photon Energy"])

            # If energy value matches target exactly, uses
            # the T.A.C. of this row
            if energy == energy_target:
                result_label = tk.Label(root,
                               text=row["Total Attenuation with Coherent Scattering"])
                result_label.pack(pady=5)
                return

            # If energy value is less than the target, uses
            # this energy and its coefficient as the closest
            # value lower than the energy so far, which we know
            # is true because the data is sorted in ascending order
            # by energy
            elif energy < energy_target:
                closest_low = energy
                low_coefficient = float(row["Total Attenuation with Coherent Scattering"])

            # If energy value is greater than the target, uses
            # this energy and its coefficient as the closest
            # value higher than the energy and then exits the loop,
            # which we know is true because the data is sorted in
            # ascending order by energy
            else:
                closest_high = energy
                high_coefficient = float(row["Total Attenuation with Coherent Scattering"])
                break

    # Error-check for an energy input smaller than all data
    if closest_low == 0.0:
        result_label = tk.Label(root, text="Error: Energy too low.")
        result_label.pack(pady=5)
        return

    # Error-check for an energy input larger than all data
    if closest_high == float('inf'):
        result_label = tk.Label(root, text="Error: Energy too high.")
        result_label.pack(pady=5)
        return

    # Uses linear interpolation to find the T.A.C.
    difference = closest_high - closest_low
    percentage = (energy_target - closest_low) / difference
    coefficient = low_coefficient + percentage * (high_coefficient - low_coefficient)
    result_label = tk.Label(root, text=str(coefficient))
    result_label.pack(pady=5)

def clear():
    global screen_list
    global screen

    # Clears screen
    result_label.pack_forget()
    if screen == "tac":
        for node in screen_list:
            node.destroy()

    # Returns home screen
    return_home()
    screen = ""

def return_home():
    global tac_button

    # Creates buttons for home screen
    tac_button = tk.Button(root, text="Total Attenuation Coefficient", command=total_attenuation_coefficient)
    tac_button.pack(pady=5)

# Creates home screen upon launch
return_home()

# Runs app
root.mainloop()