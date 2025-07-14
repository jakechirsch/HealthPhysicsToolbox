##### IMPORTS #####
import io
from Utility.Functions.math_utility import *
from Utility.Functions.gui_utility import *

#####################################################################################
# UNITS SECTION
#####################################################################################

# Unit choices paired with their factor in relation to the default
mac_numerator = {"mm\u00B2" : 10 ** 2, "cm\u00B2" : 1,
                 "m\u00B2" : 0.01 ** 2}
density_numerator = {"mg" : 1000, "g" : 1, "kg" : 0.001}
lac_numerator= {"1" : 1}
mac_denominator = {"mg" : 1000, "g" : 1, "kg" : 0.001}
density_denominator = {"mm\u00B3" : 10 ** 3, "cm\u00B3" : 1,
                       "m\u00B3" : 0.01 ** 3}
lac_denominator = {"mm" : 10, "cm" : 1, "m" : 0.01}

energy_units = {"eV" : 0.001 ** 2, "keV" : 0.001,
                "MeV" : 1, "GeV" : 1000}

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
If we are finding an attenuation coefficient and multiple
interactions are selected, the function iterates over the interactions
and sums their coefficient components.
Finally, if the calculation did not cause an error,
the result is converted to the desired units, and then
displayed in the result label.
"""
def handle_calculation(root, category, mode, interactions, element,
                       energy_str, result_label, num, den, energy_unit):
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
    result = 0

    if mode == "Mass Attenuation Coefficient":
        for interaction in interactions:
            mac = find_mac(category, interaction, element, energy_target)
            if mac in errors:
                result = mac
                break
            result += mac
    elif mode == "Density":
        result = find_density(category, element, "Mass Attenuation")
    else:
        for interaction in interactions:
            mac = find_mac(category, interaction, element, energy_target)
            if mac in errors:
                result = mac
                break
            result += (mac * find_density(category, element, "Mass Attenuation"))

    # Displays result label
    if not result in errors:
        # Converts result to desired units
        if mode == "Mass Attenuation Coefficient":
            result *= mac_numerator[num]
            result /= mac_denominator[den]
        elif mode == "Density":
            result *= density_numerator[num]
            result /= density_denominator[den]
        else:
            result *= lac_numerator[num]
            result /= lac_denominator[den]
        edit_result(f"{result:.4g}", result_label, num=num, den=den)
    else:
        edit_result(result, result_label)

"""
This function handles finding the mass attenuation coefficient
for the selected item. It is used when the desired final result is the
mass attenuation coefficient as well as the linear attenuation coefficient.
Based on the selected category, it passes on the calculation to either
find_mac_for_element or find_mac_for_material, and then returns the result.
"""
def find_mac(category, interaction, element, energy_target):
    if category in element_choices:
        mac = find_mac_for_element(element, interaction, energy_target)
    elif category in material_choices:
        db_path = resource_path('Data/General Data/Material Composition/' + element + '.csv')
        with open(db_path, 'r') as file:
            mac = find_mac_for_material(file, interaction, energy_target)
    else:
        db_path = get_user_data_path('Attenuation/Photons/_' + element)
        with shelve.open(db_path) as db:
            stored_data = db[element]
            stored_data = stored_data.replace('\\n', '\n')

        # Create file-like object from the stored string
        csv_file_like = io.StringIO(stored_data)

        mac = find_mac_for_material(csv_file_like, interaction, energy_target)

    return mac

"""
This function handles finding the mass attenuation coefficient
for a material, by summing the weighted coefficients of each
material making up the element. It uses find_mac_for_element
to find the coefficient for each element.
"""
def find_mac_for_material(file_like, interaction, energy_target):
    mac = 0
    # Parse file
    reader = csv.DictReader(file_like)

    # Sums each component's weighted T.A.C.
    for row in reader:
        mac_of_element = find_mac_for_element(row['Element'], interaction, energy_target)
        if mac_of_element in errors:
            mac = mac_of_element
            break
        mac_component = float(row['Weight']) * float(mac_of_element)
        mac += mac_component

    return mac

"""
This function handles finding the mass attenuation coefficient
for an element. The data for the particular element is parsed.
The function handles the following errors:
   Energy too low
   Energy too high
If an exact energy match is found, the coefficient component from
the data is returned directly. Otherwise, if the input did not cause
an error, linear interpolation is used with the closest energy value
on each side of the inputted energy value from the data.
"""
def find_mac_for_element(element, interaction, energy_target):
    # Variables for the nearest energy value on either side
    closest_low = 0.0
    closest_high = float('inf')

    # Variables for the T.A.C. of the nearest energy values on either side
    low_coefficient = 0.0
    high_coefficient = float('inf')

    # Opens file
    db_path = resource_path('Data/Modules/Attenuation/Photons/Elements/' + element + '.csv')
    with open(db_path, 'r') as file:
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
    return linear_interpolation(energy_target, closest_low, closest_high,
                                low_coefficient, high_coefficient)