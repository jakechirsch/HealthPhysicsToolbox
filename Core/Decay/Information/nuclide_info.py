##### IMPORTS #####
import radioactivedecay as rd
from Utility.Functions.files import save_file
from Utility.Functions.gui_utility import edit_result

#####################################################################################
# CALCULATIONS SECTION
#####################################################################################

"""
This function is called when the Calculate button is hit.
The function decides what calculation to perform
based on the selected calculation mode.
"""
def handle_calculation(root, mode, isotope, result_box):
    root.focus()
    match mode:
        case "Decay Scheme":
            nuclide_decay_scheme(isotope, result_box)
        case "Half Life":
            nuclide_half_life(isotope, result_box)

"""
This function retrieves the decay scheme plot
given a particular isotope.
"""
def nuclide_decay_scheme(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    fig, ax = nuc.plot()
    save_file(fig, "Plot", result_box, isotope, "decay_scheme", True)

"""
This function retrieves the half-life
given a particular isotope.
"""
def nuclide_half_life(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.half_life('s') # Time unit : seconds
    edit_result(f"{result} s", result_box)