##### IMPORTS #####
import csv
import tkinter as tk

##### WINDOW SETUP #####
root = tk.Tk()
root.title("Coefficient Request")
root.geometry("500x200")

##### HOME SCREEN BUTTONS #####
tac_button = tk.Button(root)

### ERROR MESSAGES ###
non_number = "Error: Non-number energy input."
too_low = "Error: Energy too low."
too_high = "Error: Energy too high."
errors = [non_number, too_low, too_high]

# For global access to nodes on non-home screen
screen_list = []
advanced_list = []

# Displays the requested coefficient
result_label = tk.Label(root, text="")

def total_attenuation_coefficient(mode="Element"):
    global tac_button
    global screen_list

    x = []

    # Stores element/material selection
    var = tk.StringVar(root)

    if mode == "Element":
        # Obtains list of elements
        with open('attenuation/Elements/Elements.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != 'Name':
                    x.append(row[0])

        # Sets default element selection
        var.set('Ac')
    else:
        # Obtains list of elements
        with open('attenuation/Materials/Materials.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != 'Name':
                    x.append(row[0])

        # Sets default element selection
        var.set('Acetone')

    # Changes to T.A.C. screen
    tac_button.pack_forget()

    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)

    # Creates dropdown menu for element selection
    dropdown = tk.OptionMenu(top_frame, var, *x)
    dropdown.pack(side="left", padx=5)

    # Creates an advanced settings button
    advanced = tk.Button(top_frame, text="Advanced Settings",
                       command=lambda: tac_advanced(mode))
    advanced.pack(side="left", padx=5)

    # Creates label for energy input
    label = tk.Label(root, text="Energy:")
    label.pack()

    # Creates input box for energy input
    entry = tk.Entry(root, width=30)
    entry.config(bg='white', fg='grey')
    entry.pack()

    # Creates calculate button
    calc = tk.Button(root, text="Calculate",
                       command=lambda: find_tac(mode, var.get(), entry.get()))
    calc.pack(pady=5)

    # Creates exit button to return to home screen
    exit_button = tk.Button(root, text="Exit", command=exit_to_home)
    exit_button.pack(pady=5)

    # Stores nodes into global list
    screen_list = [top_frame, dropdown, advanced, label, entry, calc, exit_button]

def tac_advanced(mode_start):
    global advanced_list

    # Hides T.A.C. screen
    clear()

    # Stores mode selection and sets default
    var = tk.StringVar(root)
    var.set(mode_start)

    # Creates dropdown menu for mode
    mode = ["Element", "Material"]
    dropdown = tk.OptionMenu(root, var, *mode)
    dropdown.pack(pady=10)

    # Creates exit button to return to T.A.C. screen
    exit_button = tk.Button(root, text="Back", command=lambda: tac_back(var.get()))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [dropdown, exit_button]

def tac_back(mode):
    clear_advanced()
    total_attenuation_coefficient(mode=mode)

def find_tac(mode, element, energy_str):
    global result_label

    # Removes result label from past calculations
    result_label.pack_forget()

    # Error-check for a non-number energy input
    try:
        energy_target = float(energy_str)
    except ValueError:
        result_label = tk.Label(root, text=non_number)
        result_label.pack(pady=5)
        return

    if mode == "Element":
        tac = calculate_tac_for_element(element, energy_target)

        # Displays result label
        result_label = tk.Label(root, text=tac)
        result_label.pack(pady=5)
    else:
        tac = 0
        with open('attenuation/Materials/' + element + '.csv', 'r') as file:
            # Reads in file
            reader = csv.DictReader(file)

            # Sums each component's weighted T.A.C.
            for row in reader:
                tac_of_element = calculate_tac_for_element(row['Element'], energy_target)
                if tac_of_element in errors:
                    tac = tac_of_element
                    break
                tac_component = float(row['Weight']) * float(tac_of_element)
                tac += tac_component

        # Displays result label
        result_label = tk.Label(root, text=tac)
        result_label.pack(pady=5)

def calculate_tac_for_element(element, energy_target):
    # Variables for the nearest energy value on either side
    closest_low = 0.0
    closest_high = float('inf')

    # Variables for the T.A.C. of the nearest energy values on either side
    low_coefficient = 0.0
    high_coefficient = float('inf')

    # Opens file
    with open('attenuation/Elements/' + element + '.csv', 'r') as file:
        # Reads in file in dictionary format
        reader = csv.DictReader(file)

        for row in reader:
            # Retrieves energy value of row
            energy = float(row["Photon Energy"])

            # If energy value matches target exactly, uses
            # the T.A.C. of this row
            if energy == energy_target:
                return row["Total Attenuation with Coherent Scattering"]

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
        return too_low

    # Error-check for an energy input larger than all data
    if closest_high == float('inf'):
        return too_high

    # Uses linear interpolation to find the T.A.C.
    difference = closest_high - closest_low
    percentage = (energy_target - closest_low) / difference
    coefficient = low_coefficient + percentage * (high_coefficient - low_coefficient)
    return str(coefficient)

def clear():
    global screen_list

    # Clears screen
    result_label.pack_forget()
    for node in screen_list:
        node.destroy()
    screen_list.clear()

def clear_advanced():
    global screen_list

    # Clears screen
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()

def return_home():
    global tac_button

    # Creates buttons for home screen
    tac_button = tk.Button(root, text="Total Attenuation Coefficient", command=total_attenuation_coefficient)
    tac_button.pack(pady=5)

def exit_to_home():
    clear()
    return_home()

# Creates home screen upon launch
return_home()

# Runs app
root.mainloop()