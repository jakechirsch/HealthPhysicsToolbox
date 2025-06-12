##### IMPORTS #####
import csv
import shelve

# Choices using an element or a material
element_choices = ["Common Elements", "All Elements"]
material_choices = ["Common Materials", "All Materials"]

def linear_interpolation(target, near_low, near_high, val_low, val_high):
    difference = near_high - near_low
    percentage = (target - near_low) / difference
    value = val_low + percentage * (val_high - val_low)
    return value

def find_density(selection, element):
    density = None
    if selection == "Custom Materials":
        with shelve.open('_' + element) as db:
            density = float(db[element + '_Density'])
    else:
        name = 'Elements' if selection in element_choices else 'Materials'
        with open('Data/General Data/Density/' + name + '.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row and row['Name'] == element:
                    density = float(row['Density'])
    return density