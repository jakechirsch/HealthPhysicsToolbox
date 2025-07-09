##### IMPORTS #####
import csv
import shelve
from Utility.Functions.gui_utility import resource_path, get_user_data_path

# Choices using an element or a material
element_choices = ["Common Elements", "All Elements"]
material_choices = ["Common Materials", "All Materials"]

def get_choices(selection):
    choices = []

    if selection == "All Elements" or selection == "All Materials":
        # Obtains list of elements from csv file
        name = "Elements" if selection == "All Elements" else "Materials"
        db_path = resource_path('Data/General Data/Density/' + name + '.csv')
        with open(db_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] != 'Name':
                    choices.append(row[0])
        return choices

    # Obtains list of elements from shelve
    db_path = get_user_data_path('Mass Attenuation/' + selection)
    with shelve.open(db_path) as prefs:
        default = []
        if selection != "Custom Materials":
            db_path2 = resource_path('Data/Modules/Mass Attenuation/' + selection + '.csv')
            with open(db_path2, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] != 'Name':
                        default.append(row[0])
        choices = prefs.get(selection, default)
        choices.sort()
        return choices