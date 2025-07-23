##### IMPORTS #####
import matplotlib.pyplot as plt
import pandas as pd
from Core.Shielding.Electrons.electrons_calculations import *

#####################################################################################
# EXPORT SECTION
#####################################################################################

"""
This function is called when the Export button is hit.
The function handles the following errors:
   No selected item
If the error is not applicable, a dataframe is set up
with a column for energy as well as a column for the mode.
If we are working with an element and the selected calculation
mode is not Range-Energy Curve, we copy these columns
from the raw data, converting the energy column to the
desired energy unit. If the calculation mode is Range-Energy
Curve, we calculate each of the values. If we are working with
a material, we pass on the work of filling out the dataframe
to the make_df_for_material function.
Once the dataframe is filled out, we convert the mode column
to the desired unit.
Then, if the select export type is plot, we call
configure_plot.
Finally, if the file is meant to be saved, we pass on the
work to the save_file function. Otherwise, we show the plot.
"""
def export_data(root, element, category, mode, num, den,
                energy_unit, choice, save, error_label):
    root.focus()

    # Error-check for no selected item
    if element == "":
        error_label.config(style="Error.TLabel", text=no_selection)
        return

    error_label.config(style="Error.TLabel", text="")

    # Sets up columns for dataframe
    energy_col = "Electron Energy (" + energy_unit + ")"
    unit = " (" + num + "/" + den + ")"
    if num == "1":
        unit = " (" + den + "\u207B\u00B9)"
    mode_col = mode
    if mode == "CSDA Range" or mode == "Range-Energy Curve":
        mode_col += unit
    cols = [energy_col, mode_col]

    df = pd.DataFrame(columns=cols)
    if category in element_choices:
        # Load the CSV file
        db_path = resource_path('Data/Modules/Shielding/Electrons/Elements/' + element + '.csv')
        df2 = pd.read_csv(db_path)

        df[energy_col] = df2["Kinetic Energy"]

        if mode != "Range-Energy Curve":
            df[mode_col] = df2[mode]
        else:
            min_val = 0.001
            max_val = 10
            df = df[df[energy_col] <= max_val]
            df = df[df[energy_col] >= min_val]
            for index, row in df.iterrows():
                row[mode_col] = range_energy_curve(float(row[energy_col]),
                                                   energy_unit, None)
                df.loc[index] = [row[energy_col], row[mode_col]]
    elif category in material_choices:
        db_path = resource_path('Data/General Data/Material Composition/' + element + '.csv')
        with open(db_path, 'r') as file:
            make_df_for_material(file, df, element, category, mode, energy_unit)
    else:
        db_path = get_user_data_path('Shielding/Electrons/_' + element)
        with shelve.open(db_path) as db:
            stored_data = db[element]
            stored_data = stored_data.replace('\\n', '\n')

        # Create file-like object from the stored string
        csv_file_like = io.StringIO(stored_data)

        make_df_for_material(csv_file_like, df, element, category, mode, energy_unit)

    # Converts energy column to desired energy unit
    df[energy_col] /= energy_units[energy_unit]

    # Convert to desired unit
    if mode == "CSDA Range" or mode == "Range-Energy Curve":
        df[mode_col] *= csda_numerator[num]
        df[mode_col] /= csda_denominator[den]

    if choice == "Plot":
        configure_plot(df, energy_col, mode_col, element)
        if save == 1:
            save_file(plt, choice, error_label, element, "range")
        else:
            error_label.config(style="Success.TLabel", text=choice + " exported!")
            plt.show()
    else:
        save_file(df, choice, error_label, element, "range")

#####################################################################################
# PLOT SECTION
#####################################################################################

"""
This function configures the plot that is being exported
using the dataframe and other information.
First, the plot is cleared from any previous exports.
Then, we plot the mode column against the data column.
The title and axis titles are all configured
and the axis scales are set to logarithmic.
"""
def configure_plot(df, energy_col, mode_col, element):
    # Clear from past plots
    plt.clf()

    for index, row in df.iterrows():
        print(row[energy_col], row[mode_col])

    # Plot the data
    plt.plot(df[energy_col], df[mode_col], marker='o', label=mode_col)
    plt.title(element + " - " + mode_col, fontsize=8.5)
    plt.xscale('log')
    plt.yscale('log')
    #plt.legend()
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
calculation mode value by calling the find_data function
with the mode. If Range-Energy Curve is the selected calculation mode,
then instead of finding the values in the data, we calculate them.
"""
def make_df_for_material(file_like, df, element, category, mode, energy_unit):
    # Reads in file
    reader = csv.DictReader(file_like)

    # Create the dataframe
    vals = []
    for row in reader:
        db_path = resource_path('Data/Modules/Shielding/Electrons/Elements/' + row['Element'] + '.csv')
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
                for val in vals:
                    if val > max_val or val < min_val:
                        vals.remove(val)

    # Gets rid of bad R.E.C. energy values
    if mode == "Range-Energy Curve":
        for val in vals:
            min_val = 0.001 / energy_units[energy_unit]
            max_val = 10 / energy_units[energy_unit]
            if val > max_val or val < min_val:
                vals.remove(val)

    # Finds the data for mode at each energy value and adds to dataframe
    for index, val in enumerate(vals):
        if mode == "Range-Energy Curve":
            x = range_energy_curve(val, energy_unit, None)
        else:
            x = find_data(category, mode, element, val, "Electrons")
        row = [val, x]
        df.loc[index] = row