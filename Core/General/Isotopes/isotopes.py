##### IMPORTS #####
import radioactivedecay as rd
from Utility.Functions.gui_utility import edit_result
from Utility.Functions.math_utility import atomic_mass_numerator, atomic_mass_denominator

#####################################################################################
# CALCULATIONS SECTION
#####################################################################################

"""
This function is called when the Calculate button is hit.
The function decides what calculation to perform
based on the selected calculation mode.
"""
def handle_calculation(root, mode, isotope, result_box, num, den):
    root.focus()
    match mode:
        case "Proton Number":
            nuclide_proton_number(isotope, result_box)
        case "Nucleon Number":
            nuclide_nucleon_number(isotope, result_box)
        case "Atomic Mass":
            nuclide_atomic_mass(isotope, result_box, num, den)

"""
This function retrieves the proton number
given a particular isotope.
"""
def nuclide_proton_number(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.Z
    edit_result(result, result_box)

"""
This function retrieves the nucleon number
given a particular isotope.
"""
def nuclide_nucleon_number(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.A
    edit_result(result, result_box)

"""
This function retrieves the atomic mass
given a particular isotope.
The result is then converted to the desired units.
"""
def nuclide_atomic_mass(isotope, result_box, num, den):
    nuc = rd.Nuclide(isotope)
    result = nuc.atomic_mass
    result *= atomic_mass_numerator[num]
    result /= atomic_mass_denominator[den]
    edit_result(result, result_box, num, den)