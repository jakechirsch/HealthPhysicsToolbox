##### IMPORTS #####
import matplotlib.pyplot as plt
import pandas as pd
from Core.Dose.Electrons.electrons_calculations import *

#####################################################################################
# EXPORT SECTION
#####################################################################################

"""
This function is called when the Export button is hit.
The function handles the following errors:
   No selected item
   No interactions selected
If neither error is applicable, a dataframe is set up
with a column for energy as well as a column for each of
the selected interactions.
If we are working with an element, we copy these columns
from the raw data, converting the energy column to the
desired energy unit. Otherwise, we pass on the work of
filling out the dataframe to the make_df_for_material function.
Once the dataframe is filled out, we convert the interaction
columns to the desired unit.
Then, if the selected export type is Plot, we call
configure_plot.
Finally, if the file is meant to be saved, we pass on the
work to the save_file function. Otherwise, we show the plot.
"""
def export_data(root, element, category, mode, interactions, num, den,
                energy_unit, choice, save, error_label):
    root.focus()

    # Error-check for no selected item
    if element == "":
        error_label.config(style="Error.TLabel", text=no_selection)
        return

    # Error-check for no interactions selected
    if mode == "Stopping Power" and len(interactions) == 0:
        error_label.config(style="Error.TLabel", text="Error: No interactions selected.")
        return

    error_label.config(style="Error.TLabel", text="")

    # Sets up columns for dataframe
    energy_col = "Electron Energy (" + energy_unit + ")"
    cols = [energy_col]
    if mode == "Stopping Power":
        for interaction in interactions:
            cols.append(interaction)
    else:
        cols.append(mode)

    df = pd.DataFrame(columns=cols)
    if category in element_choices:
        # Load the CSV file
        db_path = resource_path('Data/NIST Coefficients/Electrons/Elements/' + element + '.csv')
        df2 = pd.read_csv(db_path)

        df[energy_col] = df2["Kinetic Energy"]

        if mode == "Stopping Power":
            for interaction in interactions:
                df[interaction] = df2[interaction]
        else:
            df[mode] = df2[mode]
    elif category in material_choices:
        db_path = resource_path('Data/General Data/Material Composition/' + element + '.csv')
        with open(db_path, 'r') as file:
            make_df_for_material(file, df, element, category, mode, interactions)
    else:
        db_path = get_user_data_path('Custom Materials/_' + element)
        with shelve.open(db_path) as db:
            stored_data = db[element]
            stored_data = stored_data.replace('\\n', '\n')

        # Create file-like object from the stored string
        csv_file_like = io.StringIO(stored_data)

        make_df_for_material(csv_file_like, df, element, category, mode, interactions)

    # Converts energy column to desired energy unit
    df[energy_col] /= energy_units[energy_unit]

    # Convert to desired unit
    if mode == "Stopping Power":
        for interaction in interactions:
            df[interaction] *= sp_e_numerator[num.split(" ", 1)[0]]
            df[interaction] *= sp_l_numerator[num.split(" ", 2)[2]]
            df[interaction] /= sp_denominator[den]

    unit = " (" + num + "/" + den + ")"
    mode_col = mode
    if mode == "Stopping Power":
        mode_col += unit

    if choice == "Plot":
        configure_plot(interactions, df, energy_col, mode_col, element)
        if save == 1:
            save_file(plt, choice, error_label, element, "stopping")
        else:
            error_label.config(style="Success.TLabel", text=choice + " exported!")
            plt.show()
    else:
        if mode == "Stopping Power":
            for interaction in interactions:
                df.rename(columns={interaction: interaction+unit}, inplace=True)
        save_file(df, choice, error_label, element, "stopping")

#####################################################################################
# PLOT SECTION
#####################################################################################

"""
This function configures the plot that is being exported
using the dataframe and other information.
First, the plot is cleared from any previous exports.
Then, we plot each interaction column against the data column.
The title and axis titles are all configured
and the axis scales are set to logarithmic.
"""
def configure_plot(interactions, df, energy_col, mode_col, element):
    # Clear from past plots
    plt.clf()

    # Plot the data
    if mode_col.split(" ", 1)[0] == "Stopping":
        for interaction in interactions:
            plt.plot(df[energy_col], df[interaction], marker='o', label=interaction)
    else:
        plt.plot(df[energy_col], df[mode_col], marker='o', label=mode_col)
    plt.title(element + " - " + mode_col, fontsize=8.5)
    plt.xscale('log')
    plt.yscale('log')
    if mode_col.split(" ", 1)[0] == "Stopping":
        plt.legend()
    plt.xlabel(energy_col)
    plt.ylabel(mode_col)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

#####################################################################################
# DATA SECTION
#####################################################################################

"""
This function fills out the dataframe when we are
exporting data for a material. First, we retrieve
the energy values for the dataframe by taking the values
from the raw data of the first element and then removing
any values that are out of range for any of the remaining
elements. Then, for each energy value, we get the corresponding
interaction value for the rest of the row by calling the find_data function
with each interaction.
"""
def make_df_for_material(file_like, df, element, category, mode, interactions):
    # Reads in file
    reader = csv.DictReader(file_like)

    # Create the dataframe
    vals = []
    for row in reader:
        db_path = resource_path('Data/NIST Coefficients/Electrons/Elements/' + row['Element'] + '.csv')
        if len(vals) == 0:
            with open(db_path, 'r') as file:
                # Reads in file
                reader2 = csv.DictReader(file)

                # Gets energy values to use as dots
                for row2 in reader2:
                    vals.append(float(row2["Kinetic Energy"]))
        else:
            with open(db_path, 'r') as file:
                # Reads in file
                reader2 = csv.DictReader(file)

                new_vals = []
                # Gets energy values to use as dots
                for row2 in reader2:
                    new_vals.append(float(row2["Kinetic Energy"]))
                max_val = max(new_vals)
                min_val = min(new_vals)
                vals = [val for val in vals if min_val <= val <= max_val]

    # Finds the data for mode at each energy value and adds to dataframe
    for index, val in enumerate(vals):
        row = [val]
        if mode == "Stopping Power":
            for interaction in interactions:
                x = find_data(category, interaction, element, val, "Electrons")
                row.append(x)
        else:
            x = find_data(category, mode, element, val, "Electrons")
            row.append(x)
        df.loc[index] = row