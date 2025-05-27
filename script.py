##### IMPORTS #####
import csv
from tkinter import *

##### WINDOW SETUP #####
root = Tk()
root.title("Coefficient Request")
root.geometry("500x225")

##### HOME SCREEN BUTTONS #####
tac_button = Button(root)

### ERROR MESSAGES ###
non_number = "Error: Non-number energy input."
too_low = "Error: Energy too low."
too_high = "Error: Energy too high."
errors = [non_number, too_low, too_high]

# For global access to nodes on non-home screen
screen_list = []
advanced_list = []

# Displays the requested coefficient
result_label = Text(root, height=1, borderwidth=0)
result_label.config(bg='white', fg='grey')

def total_attenuation_coefficient(selection="Element",
                                  mode="Mass Attenuation Coefficient (cm^2/g)",
                                  interaction="Total Attenuation with Coherent Scattering"):
    global tac_button
    global screen_list

    choices = []

    # Stores element/material selection
    var = StringVar(root)

    if selection == "Element":
        # Obtains list of elements
        with open('attenuation/Elements/Elements.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != 'Name':
                    choices.append(row[0])

        # Sets default element selection
        var.set('Ac')
    else:
        # Obtains list of elements
        with open('attenuation/Materials/Materials.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != 'Name':
                    choices.append(row[0])

        # Sets default material selection
        var.set('Acetone')

    # Changes to T.A.C. screen
    tac_button.pack_forget()

    # Frame for element selection and advanced settings button
    top_frame = Frame(root)
    top_frame.pack(pady=10)

    # Creates dropdown menu for element selection
    dropdown = OptionMenu(top_frame, var, *choices)
    dropdown.pack(side="left", padx=5)

    # Creates an advanced settings button
    advanced = Button(top_frame, text="Advanced Settings",
                      command=lambda: tac_advanced(selection, mode, interaction))
    advanced.pack(side="left", padx=5)

    # Creates label for energy input
    label = Label(root, text="Energy (MeV):")

    # Creates input box for energy input
    entry = Entry(root, width=30)
    entry.config(bg='white', fg='grey')

    # Energy input is not necessary if mode is density
    if mode != "Density (g/cm^3)":
        label.pack()
        entry.pack()

    # Creates calculate button
    calc = Button(root, text="Calculate",
                  command=lambda: handle_calculation(selection, mode, interaction, var.get(), entry.get()))
    calc.pack(pady=5)

    # Creates exit button to return to home screen
    exit_button = Button(root, text="Exit", command=exit_to_home)
    exit_button.pack(pady=5)

    # Stores nodes into global list
    screen_list = [top_frame, dropdown, advanced, label, entry, calc, exit_button]

def tac_advanced(selection_start, mode_start, interaction_start):
    global advanced_list

    # Hides T.A.C. screen
    clear()

    # Stores selection and sets default
    var_selection = StringVar(root)
    var_selection.set(selection_start)

    # Creates dropdown menu for selection
    selection = ["Element", "Material"]
    selection_dropdown = OptionMenu(root, var_selection, *selection)
    selection_dropdown.pack(pady=10)

    # Stores mode and sets default
    var_mode = StringVar(root)
    var_mode.set(mode_start)

    # Creates dropdown menu for mode
    mode_choices = ["Mass Attenuation Coefficient (cm^2/g)", "Density (g/cm^3)",
                    "Linear Attenuation Coefficient (cm^-1)"]
    mode_dropdown = OptionMenu(root, var_mode, *mode_choices)
    mode_dropdown.pack(pady=10)

    # Stores interaction and sets default
    var_interaction = StringVar(root)
    var_interaction.set(interaction_start)

    # Creates dropdown menu for mode
    interaction_choices = ["Total Attenuation with Coherent Scattering",
                    "Total Attenuation without Coherent Scattering",
                    "Pair Production in Electron Field",
                    "Pair Production in Nuclear Field",
                    "Scattering - Incoherent",
                    "Scattering - Coherent",
                    "Photo-Electric Absorption"]
    interaction_dropdown = OptionMenu(root, var_interaction, *interaction_choices)
    interaction_dropdown.pack(pady=10)

    # Creates exit button to return to T.A.C. screen
    exit_button = Button(root, text="Back", command=lambda: tac_back(var_selection.get(),
                                                                     var_mode.get(),
                                                                     var_interaction.get()))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [selection_dropdown, mode_dropdown, interaction_dropdown, exit_button]

def tac_back(selection, mode, interaction):
    clear_advanced()
    total_attenuation_coefficient(selection=selection, mode=mode, interaction=interaction)

def handle_calculation(selection, mode, interaction, element, energy_str):
    global result_label

    # Removes result label from past calculations
    result_label.pack_forget()

    # Energy input in float format
    energy_target = 0.0

    if mode != "Density (g/cm^3)":
        # Error-check for a non-number energy input
        try:
            energy_target = float(energy_str)
        except ValueError:
            edit_result(non_number)
            result_label.pack(pady=5)
            return

    if mode == "Mass Attenuation Coefficient (cm^2/g)":
        result = find_tac(selection, interaction, element, energy_target)
    elif mode == "Density (g/cm^3)":
        result = find_density(selection, element)
    else:
        tac = find_tac(selection, interaction, element, energy_target)
        if tac in errors:
            result = tac
        else:
            result = tac * find_density(selection, element)

    # Displays result label
    edit_result(f"{result:.5g}")
    result_label.pack(pady=5)

def find_tac(selection, interaction, element, energy_target):
    if selection == "Element":
        tac = find_tac_for_element(element, interaction, energy_target)
    else:
        tac = 0
        with open('attenuation/Materials/' + element + '.csv', 'r') as file:
            # Reads in file
            reader = csv.DictReader(file)

            # Sums each component's weighted T.A.C.
            for row in reader:
                tac_of_element = find_tac_for_element(row['Element'], interaction, energy_target)
                if tac_of_element in errors:
                    tac = tac_of_element
                    break
                tac_component = float(row['Weight']) * float(tac_of_element)
                tac += tac_component

    return tac

def find_tac_for_element(element, interaction, energy_target):
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
                return float(row[interaction])

            # If energy value is less than the target, uses
            # this energy and its coefficient as the closest
            # value lower than the energy so far, which we know
            # is true because the data is sorted in ascending order
            # by energy
            elif energy < energy_target:
                closest_low = energy
                low_coefficient = float(row[interaction])

            # If energy value is greater than the target, uses
            # this energy and its coefficient as the closest
            # value higher than the energy and then exits the loop,
            # which we know is true because the data is sorted in
            # ascending order by energy
            else:
                closest_high = energy
                high_coefficient = float(row[interaction])
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
    return coefficient

def find_density(selection, element):
    density = None
    if selection == "Element":
        density = find_density_for_element(element)
    else:
        with open('attenuation/Materials/Materials.csv', 'r') as file:
            # Reads in file
            reader = csv.reader(file)

            # Sums each component's weighted density
            for row in reader:
                if row and row[0] == element:
                    density = float(row[1])
                    break
                density = None
    return density

def find_density_for_element(element):
    with open('attenuation/Elements/Periodic Table of Elements.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row and row['Symbol'] == element:
                return float(row['Density'])
        return None

def edit_result(result):
    # Clears result label and inserts new result
    result_label.config(state="normal")
    result_label.delete("1.0", END)
    result_label.insert(END, result)
    result_label.config(state="disabled")

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
    tac_button = Button(root, text="Total Attenuation Coefficient", command=total_attenuation_coefficient)
    tac_button.pack(pady=5)

def exit_to_home():
    clear()
    return_home()

# Creates home screen upon launch
return_home()

# Runs app
root.mainloop()