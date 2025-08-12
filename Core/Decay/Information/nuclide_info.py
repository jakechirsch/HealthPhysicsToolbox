##### IMPORTS #####
import radioactivedecay as rd
import matplotlib.pyplot as plt
from Utility.Functions.gui_utility import edit_result

def handle_calculation(mode, isotope, result_box):
    match mode:
        case "Plot":
            nuclide_plot(isotope, result_box)
        case "Half Life":
            nuclide_half_life(isotope, result_box)
        case "Progeny":
            nuclide_progeny(isotope, result_box)
        case "Branching Fractions":
            nuclide_branching_fractions(isotope, result_box)
        case "Decay Modes":
            nuclide_decay_modes(isotope, result_box)
        case "Proton Number":
            nuclide_proton_number(isotope, result_box)
        case "Nucleon Number":
            nuclide_nucleon_number(isotope, result_box)
        case "Atomic Mass":
            nuclide_atomic_mass(isotope, result_box)

def nuclide_plot(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    edit_result("Plotted!", result_box)
    nuc.plot()  # Generates the plot
    plt.show()  # Displays it

def nuclide_half_life(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.half_life('s')
    edit_result(f"{result} s", result_box)

def nuclide_progeny(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.progeny()
    edit_result(", ".join(result), result_box)

def nuclide_branching_fractions(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.branching_fractions()
    result = [str(x) for x in result]
    edit_result(", ".join(result), result_box)

def nuclide_decay_modes(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.decay_modes()
    edit_result(", ".join(result), result_box)

def nuclide_proton_number(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.Z
    edit_result(result, result_box)

def nuclide_nucleon_number(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.A
    edit_result(result, result_box)

def nuclide_atomic_mass(isotope, result_box):
    nuc = rd.Nuclide(isotope)
    result = nuc.atomic_mass
    edit_result(result, result_box, num="g", den="mol")