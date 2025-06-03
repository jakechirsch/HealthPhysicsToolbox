##### IMPORTS #####
import csv
from tkinter import *

### ERROR MESSAGES ###
non_number = "Error: Non-number energy input."
too_low = "Error: Energy too low."
too_high = "Error: Energy too high."
errors = [non_number, too_low, too_high]

# Choices using an element or a material
element_choices = ["Common Elements", "All Elements"]
material_choices = ["Common Materials", "All Materials"]

def handle_calculation(selection, mode, interaction, element, energy_str, result_label):
    if element == "":
        return

    # Removes result label from past calculations
    result_label.pack_forget()

    # Energy input in float format
    energy_target = 0.0

    if mode != "Density (g/cm\u00B3)":
        # Error-check for a non-number energy input
        try:
            energy_target = float(energy_str)
        except ValueError:
            edit_result(non_number, result_label)
            result_label.pack(pady=5)
            return

    if mode == "Mass Attenuation Coefficient (cm\u00B2/g)":
        result = find_tac(selection, interaction, element, energy_target)
    elif mode == "Density (g/cm\u00B3)":
        result = find_density(selection, element)
    else:
        tac = find_tac(selection, interaction, element, energy_target)
        if tac in errors:
            result = tac
        else:
            result = tac * find_density(selection, element)

    # Displays result label
    edit_result(f"{result:.4g}", result_label)
    result_label.pack(pady=5)

def find_tac(selection, interaction, element, energy_target):
    if selection in element_choices:
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
    if selection in element_choices:
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

def edit_result(result, result_label):
    # Clears result label and inserts new result
    result_label.config(state="normal")
    result_label.delete("1.0", END)
    result_label.insert(END, result)
    result_label.config(state="disabled")