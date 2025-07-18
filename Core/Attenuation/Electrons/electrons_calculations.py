##### IMPORTS #####
from Utility.Functions.math_utility import *

#####################################################################################
# CALCULATIONS SECTION
#####################################################################################

"""
This function is called when the Calculate button is hit.
The function handles the following errors:
   No selected item
   Non-number energy input
If neither error is applicable, the energy input
is converted to MeV to match the raw data.
Then, the function decides what calculation to perform
based on the selected calculation mode.
Finally, if the calculation did not cause an error,
[To Do: [the result is converted to the desired units]], and then
displayed in the result label.
"""
def handle_calculation(root, category, mode, element, energy_str,
                       result_label, num, den, energy_unit):
    root.focus()

    # Error-check for no selected item
    if element == "":
        edit_result(no_selection, result_label)
        return

    # Energy input in float format
    energy_target = 0.0

    if mode != "Density":
        # Error-check for a non-number energy input
        try:
            energy_target = float(energy_str)
        except ValueError:
            edit_result(non_number, result_label)
            return

    # Converts energy_target to MeV to comply with the raw data
    energy_target *= energy_units[energy_unit]

    if mode == "Range-Energy Curve":
        result = ""
    elif mode == "Density":
        result = find_density(category, element, "Attenuation/Electrons")
    else:
        result = find_data(category, mode, element, energy_target, "Electrons")

    # Displays result label
    if not result in errors:
        # To Do: Converts result to desired units
        edit_result(f"{result:.4g}", result_label, num=num, den=den)
    else:
        edit_result(result, result_label)