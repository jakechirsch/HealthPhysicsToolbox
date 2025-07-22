##### IMPORTS #####
import csv
import shelve
import io
from Utility.Functions.gui_utility import *

# Choices using an element or a material
element_choices = ["Common Elements", "All Elements"]
material_choices = ["Common Materials", "All Materials"]

#####################################################################################
# UNITS SECTION
#####################################################################################

density_numerator = {"mg" : 1000, "g" : 1, "kg" : 0.001}
density_denominator = {"mm\u00B3" : 10 ** 3, "cm\u00B3" : 1,
                       "m\u00B3" : 0.01 ** 3}
energy_units = {"eV" : 0.001 ** 2, "keV" : 0.001,
                "MeV" : 1, "GeV" : 1000}

#####################################################################################
# MATH SECTION
#####################################################################################

"""
This function performs linear interpolation on the provided arguments.
The nearest data are provided (near_low -> val_low) and (near_high -> val_high).
The target is also provided and its value is calculated and returned.
"""
def linear_interpolation(target, near_low, near_high, val_low, val_high):
    difference = near_high - near_low
    percentage = (target - near_low) / difference
    value = val_low + percentage * (val_high - val_low)
    return value

#####################################################################################
# DATA SECTION
#####################################################################################

"""
This function finds the density of the provided item.
If the category is Custom Materials, the density is retrieved
from shelve, where the user-inputted density is stored.
Otherwise, the density is retrieved from the data.
"""
def find_density(category, item, module):
    if category == "Custom Materials":
        db_path = get_user_data_path(module + '/_' + item)
        with shelve.open(db_path) as db:
            return float(db[item + '_Density'])

    name = 'Elements' if category in element_choices else 'Materials'
    db_path = resource_path('Data/General Data/Density/' + name + '.csv')
    with open(db_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row and row['Name'] == item:
                return float(row['Density'])

    return None

"""
This function handles finding a value from the raw data for the selected item.
Based on the selected category, it passes on the calculation to either
find_data_for_element or find_data_for_material, and then returns the result.
"""
def find_data(category, column, element, energy_target, particle):
    if category in element_choices:
        result = find_data_for_element(element, column, energy_target, particle)
    elif category in material_choices:
        db_path = resource_path('Data/General Data/Material Composition/' + element + '.csv')
        with open(db_path, 'r') as file:
            result = find_data_for_material(file, column, energy_target, particle)
    else:
        db_path = get_user_data_path('Attenuation/' + particle + '/_' + element)
        with shelve.open(db_path) as db:
            stored_data = db[element]
            stored_data = stored_data.replace('\\n', '\n')

        # Create file-like object from the stored string
        csv_file_like = io.StringIO(stored_data)

        result = find_data_for_material(csv_file_like, column,
                                        energy_target, particle)

    return result

"""
This function handles finding a value from the raw data for a material,
by summing the weighted values of each material making up the element.
It uses find_data_for_element to find the coefficient for each element.
"""
def find_data_for_material(file_like, column, energy_target, particle):
    result = 0
    # Parse file
    reader = csv.DictReader(file_like)

    # Sums each component's weighted value
    for row in reader:
        result_of_element = find_data_for_element(row['Element'], column,
                                                  energy_target, particle)
        if result_of_element in errors:
            result = result_of_element
            break
        result_component = float(row['Weight']) * float(result_of_element)
        result += result_component

    return result

"""
This function handles finding a value from the raw data for an element.
The data for the particular element is parsed.
The function handles the following errors:
   Energy too low
   Energy too high
If an exact energy match is found, the coefficient component from
the data is returned directly. Otherwise, if the input did not cause
an error, linear interpolation is used with the closest energy value
on each side of the inputted energy value from the data.
"""
def find_data_for_element(element, column, energy_target, particle):
    # Variables for the nearest energy value on either side
    closest_low = 0.0
    closest_high = float('inf')

    # Variables for the coefficients of the nearest energy values on either side
    low_coefficient = 0.0
    high_coefficient = float('inf')

    # Retrieves name of energy column
    energy_col = "Photon Energy" if particle == "Photons" else "Kinetic Energy"

    # Opens file
    db_path = resource_path('Data/Modules/Attenuation/' + particle + '/Elements/' + element + '.csv')
    with open(db_path, 'r') as file:
        # Reads in file in dictionary format
        reader = csv.DictReader(file)

        for row in reader:
            # Retrieves energy value of row
            energy = float(row[energy_col])

            # If energy value matches target exactly, uses
            # the coefficient of this row
            if energy == energy_target:
                return float(row[column])

            # If energy value is less than the target, uses
            # this energy and its coefficient as the closest
            # value lower than the energy so far, which we know
            # is true because the data is sorted in ascending order
            # by energy
            elif energy < energy_target:
                closest_low = energy
                low_coefficient = float(row[column])

            # If energy value is greater than the target, uses
            # this energy and its coefficient as the closest
            # value higher than the energy and then exits the loop,
            # which we know is true because the data is sorted in
            # ascending order by energy
            else:
                closest_high = energy
                high_coefficient = float(row[column])
                break

    # Error-check for an energy input smaller than all data
    if closest_low == 0.0:
        return too_low

    # Error-check for an energy input larger than all data
    if closest_high == float('inf'):
        return too_high

    # Uses linear interpolation to find the exact coefficient
    return linear_interpolation(energy_target, closest_low, closest_high,
                                low_coefficient, high_coefficient)