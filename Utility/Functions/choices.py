##### IMPORTS #####
import csv
import shelve
from Utility.Functions.files import *

# Choices using an element or a material
element_choices = ["Common Elements", "All Elements"]
material_choices = ["Common Materials", "All Materials"]

"""
This function returns the list of items (elements/materials)
in the selected category.
If the category is either All Elements or All Materials,
the choices are read from a Data file.
Otherwise, the choices are retrieved from the user's
shelve data.
If the category is either Custom Elements or Custom Materials,
a default list is read from a Data file which is used
if no user shelve data is stored.
If the category is Custom Materials, the default list is empty.
"""
def get_choices(category, particle):
    choices = []

    if category == "All Materials":
        # Obtains list of items from csv file
        db_path = resource_path('Data/General Data/Density/Materials.csv')
        read_choices(choices, db_path)
        if particle == "Alphas":
            return [choice for choice in choices if "Plutonium" not in choice]
        return choices

    if category == "All Elements":
        # Obtains list of items from csv file
        db_path = resource_path('Data/NIST Coefficients/' + particle + '/Elements.csv')
        read_choices(choices, db_path)
        return choices

    # Obtains list of items from shelve
    db_path = get_user_data_path(category)
    with shelve.open(db_path) as prefs:
        default = []
        if category != "Custom Materials":
            # Obtains list of default items from csv file
            db_path2 = resource_path('Data/General Data/' + category + '.csv')
            read_choices(default, db_path2)
        choices = prefs.get(category, default)
        choices.sort()
        return choices

"""
This function reads the list of items (elements/materials)
from a csv data file.
"""
def read_choices(choices, path):
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] != 'Name':
                choices.append(row[0])