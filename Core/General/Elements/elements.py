##### IMPORTS #####
import csv
import shelve
from Utility.Functions.files import resource_path
from Utility.Functions.gui_utility import edit_result
from Utility.Functions.files import get_user_data_path
from Utility.Functions.math_utility import atomic_mass_numerator, atomic_mass_denominator

#####################################################################################
# CALCULATIONS SECTION
#####################################################################################

"""
This function is called when the Calculate button is hit.
The function decides what calculation to perform
based on the selected calculation mode.
If the calculation mode is Atomic Mass, the result is
converted to the desired units.
"""
def handle_calculation(root, mode, element, result_box):
    root.focus()

    # Gets atomic mass units from user prefs
    db_path = get_user_data_path("Settings/General/Elements")
    with shelve.open(db_path) as prefs:
        num = prefs.get("am_num", "g")
        den = prefs.get("am_den", "mol")

    path = resource_path('Data/General Data/Periodic Table of Elements.csv')
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row and row['Symbol'] == element:
                result = row[mode]
                break

    if mode != "Atomic Mass":
        edit_result(result, result_box)
    else:
        # Convert to desired unit
        result = float(result)
        result *= atomic_mass_numerator[num]
        result /= atomic_mass_denominator[den]
        edit_result(result, result_box, num, den)