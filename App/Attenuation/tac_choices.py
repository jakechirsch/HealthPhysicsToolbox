##### IMPORTS #####
import csv
import shelve

# Choices using an element or a material
element_choices = ["Common Elements", "All Elements"]
material_choices = ["Common Materials", "All Materials"]

def get_choices(selection):
    choices = []

    if selection == "All Elements" or selection == "All Materials":
        # Obtains list of elements from csv file
        name = "Elements" if selection == "All Elements" else "Materials"
        with open('Data/General Data/Density/' + name + '.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] != 'Name':
                    choices.append(row[0])
        return choices

    # Obtains list of elements from shelve
    with shelve.open('Data/Modules/Mass Attenuation/User/' + selection) as prefs:
        default = []
        if selection != "Custom Materials":
            with open('Data/Modules/Mass Attenuation/' + selection + '.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] != 'Name':
                        default.append(row[0])
        choices = prefs.get(selection, default)
        choices.sort()
        return choices