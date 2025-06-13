##### IMPORTS #####
import io
from Utility.Functions.math_utility import *
from Utility.Functions.gui_utility import *

# Unit choices related to their factor in relation to the default
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

def handle_calculation(selection, mode, interaction, element, energy_str, result_label,
                       num, den, energy_unit):
    if element == "":
        return

    # Removes result label from past calculations
    result_label.pack_forget()

    # Energy input in float format
    energy_target = 0.0

    if mode != "Density":
        # Error-check for a non-number energy input
        try:
            energy_target = float(energy_str)
        except ValueError:
            edit_result(non_number, result_label)
            result_label.pack(pady=5)
            return

    energy_target *= energy_units[energy_unit]

    if mode == "Mass Attenuation Coefficient":
        result = find_tac(selection, interaction, element, energy_target)
    elif mode == "Density":
        result = find_density(selection, element)
    else:
        tac = find_tac(selection, interaction, element, energy_target)
        if tac in errors:
            result = tac
        else:
            result = tac * find_density(selection, element)

    # Displays result label
    if not result in errors:
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
    result_label.pack(pady=5)

def find_tac(selection, interaction, element, energy_target):
    if selection in element_choices:
        tac = find_tac_for_element(element, interaction, energy_target)
    elif selection in material_choices:
        with open('Data/General Data/Material Composition/' + element + '.csv', 'r') as file:
            tac = find_tac_for_material(file, interaction, energy_target)
    else:
        with shelve.open('_' + element) as db:
            stored_data = db[element]
            stored_data = stored_data.replace('\\n', '\n')

        # Create file-like object from the stored string
        csv_file_like = io.StringIO(stored_data)

        tac = find_tac_for_material(csv_file_like, interaction, energy_target)

    return tac

def find_tac_for_material(file_like, interaction, energy_target):
    tac = 0
    # Parse file
    reader = csv.DictReader(file_like)

    # Sums each component's weighted T.A.C.
    for row in reader:
        tac_of_element = find_tac_for_element(row['Element'], interaction, energy_target)
        if tac_of_element in errors:
            tac = tac_of_element
            break
        tac_component = float(row['Weight']) * float(tac_of_element)
        tac += tac_component

    return tac

def find_tac_for_element(element, interaction, energy_target):
    # Variables for the nearest energy value on either side
    closest_low = 0.0
    closest_high = float('inf')

    # Variables for the T.A.C. of the nearest energy values on either side
    low_coefficient = 0.0
    high_coefficient = float('inf')

    # Opens file
    with open('Data/Modules/Mass Attenuation/Elements/' + element + '.csv', 'r') as file:
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