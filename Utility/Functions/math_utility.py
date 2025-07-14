##### IMPORTS #####
import csv
import shelve
from Utility.Functions.gui_utility import resource_path, get_user_data_path

# Choices using an element or a material
element_choices = ["Common Elements", "All Elements"]
material_choices = ["Common Materials", "All Materials"]

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