##### IMPORTS #####
from Utility.Functions.math_utility import *

#####################################################################################
# UNITS SECTION
#####################################################################################

# Unit choices paired with their factor in relation to the default
csda_numerator = {"mg" : 1000, "g" : 1, "kg" : 0.001}
csda_denominator = {"mm\u00B2" : 10 ** 2, "cm\u00B2" : 1,
                    "m\u00B2" : 0.01 ** 2}

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
the result is converted to the desired units, and then
displayed in the result label.
"""
def handle_calculation(root, category, mode, element, energy_str,
                       result_label, warning_label, num, den, energy_unit):
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
        result = range_energy_curve(energy_target, energy_unit, warning_label)
    elif mode == "Density":
        result = find_density(category, element, "Attenuation/Electrons")
    else:
        result = find_data(category, mode, element, energy_target, "Electrons")

    # Displays result label
    if not result in errors:
        # Converts result to desired units
        if mode == "CSDA Range" or mode == "Range-Energy Curve":
            result *= csda_numerator[num]
            result /= csda_denominator[den]
        elif mode == "Density":
            result *= density_numerator[num]
            result /= density_denominator[den]
        edit_result(f"{result:.4g}", result_label, num=num, den=den)
    else:
        edit_result(result, result_label)

"""
This function calculates the range-energy curve value
given a particular energy value.
"""
def range_energy_curve(energy, energy_unit, warning_label):
    warning_label.config(text="")

    # Error-check for a negative energy input
    if energy < 0:
        return too_low

    # Warning for model being inaccurate
    if energy < 0.001 or energy > 10:
        # Convert energy back to original unit
        low = 0.001 / energy_units[energy_unit]
        high = 10 / energy_units[energy_unit]

        # Remove float rounding error
        if abs(low - 1000) < 0.001:
            low = 1000.0

        # Scientific notation for large number
        if high > 10000:
            high = f"{high:.0e}"

        warning_label.config(text="Warning: Model is only accurate with input in ["
                                  + str(low).rstrip('0').rstrip('.') + ", "
                                  + str(high).rstrip('0').rstrip('.') + "].")

    # Model
    if energy <= 0.8:
        return 0.407 * pow(energy, 1.38)
    return 0.542 * energy - 0.133