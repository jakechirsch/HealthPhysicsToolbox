##### IMPORTS #####
import radioactivedecay as rd
import matplotlib.pyplot as plt

def plot_nuclide(isotope):
    nuc = rd.Nuclide(isotope)
    nuc.plot()  # Generates the plot
    plt.show()  # Displays it