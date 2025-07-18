##### IMPORTS #####
import matplotlib.pyplot as plt
import pandas as pd
from Core.Attenuation.Photons.photons_calculations import *
from tkinter.filedialog import asksaveasfilename

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
columns to the desired unit. If L.A.C. is the selected
calculation mode, we also need to multiply the interaction
columns by the item's density.
Then, if the select export type is plot, we call
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
    if len(interactions) == 0:
        error_label.config(style="Error.TLabel", text="Error: No interactions selected.")
        return

    error_label.config(style="Error.TLabel", text="")

    # Sets up columns for dataframe
    energy_col = "Photon Energy (" + energy_unit + ")"
    cols = [energy_col]
    for interaction in interactions:
        cols.append(interaction)

    df = pd.DataFrame(columns=cols)
    if category in element_choices:
        # Load the CSV file
        db_path = resource_path('Data/Modules/Attenuation/Photons/Elements/' + element + '.csv')
        df2 = pd.read_csv(db_path)

        # Converts energy column to desired energy unit
        df[energy_col] = df2["Photon Energy"]
        df[energy_col] /= energy_units[energy_unit]

        for interaction in interactions:
            df[interaction] = df2[interaction]
    elif category in material_choices:
        db_path = resource_path('Data/General Data/Material Composition/' + element + '.csv')
        with open(db_path, 'r') as file:
            make_df_for_material(file, df, element, category, interactions)
    else:
        db_path = get_user_data_path('Attenuation/Photons/_' + element)
        with shelve.open(db_path) as db:
            stored_data = db[element]
            stored_data = stored_data.replace('\\n', '\n')

        # Create file-like object from the stored string
        csv_file_like = io.StringIO(stored_data)

        make_df_for_material(csv_file_like, df, element, category, interactions)

    # Convert to desired unit
    if mode == "Mass Attenuation Coefficient":
        for interaction in interactions:
            df[interaction] *= mac_numerator[num]
            df[interaction] /= mac_denominator[den]
    else:
        density = find_density(category, element, "Attenuation/Photons")
        for interaction in interactions:
            df[interaction] *= density
            df[interaction] *= lac_numerator[num]
            df[interaction] /= lac_denominator[den]

    unit = " (" + num + "/" + den + ")"
    if num == "1":
        unit = " (" + den + "\u207B\u00B9)"

    if choice == "Plot":
        configure_plot(interactions, df, energy_col, unit, element, mode)
        if save == 1:
            save_file(plt, choice, error_label, element)
        else:
            error_label.config(style="Success.TLabel", text=choice + " exported!")
            plt.show()
    else:
        for interaction in interactions:
            df.rename(columns={interaction: interaction+unit}, inplace=True)
        save_file(df, choice, error_label, element)

#####################################################################################
# PLOT SECTION
#####################################################################################

"""
This function configures the plot that is being exported
using the dataframe and other information.
First, the plot is cleared from any previous exports.
Then, we plot each interaction column against the data column.
The title, legend, and axis titles are all configured
and the axis scales are set to logarithmic.
"""
def configure_plot(interactions, df, energy_col, unit, element, mode):
    # Clear from past plots
    plt.clf()

    # Plot the data
    for interaction in interactions:
        plt.plot(df[energy_col], df[interaction], marker='o', label=interaction)
    plt.title(element + " - " + mode + unit, fontsize=8.5)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.xlabel(energy_col)
    plt.ylabel(mode + unit)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

#####################################################################################
# SAVING SECTION
#####################################################################################

"""
This function is called when the exported file is
going to be saved. It prompts the user to select
a file name and location, and handles the error of
the user canceling the export. If the export is not
canceled, the file is saved with the selected name
and location and then opened.
"""
def save_file(obj, choice, error_label, element):
    file_format = ".csv"
    if choice == "Plot":
        file_format = ".png"

    # Show the "Save As" dialog
    file_path = asksaveasfilename(
        defaultextension=file_format,
        filetypes=[(file_format[1:].upper() + " files", "*" + file_format)],
        title="Save " + file_format[1:].upper() + " As...",
        initialfile=element.lower().replace(" ", "_") + "_attenuation_" + choice.lower()
    )

    # If the user selected a path, save the file
    if file_path:
        if choice == "Plot":
            obj.savefig(file_path)
        else:
            obj.to_csv(file_path, index=False)
        error_label.config(style="Success.TLabel", text=choice + " exported!")
        open_file(file_path)
    else:
        error_label.config(style="Error.TLabel", text="Export canceled.")

#####################################################################################
# DATA SECTION
#####################################################################################

"""
This function fills out the dataframe when we are
exporting data for a material. First, we retrieve
the energy values for the dataframe by taking the values
from the raw data of the first element and then removing
any values that are out of range for any of the remaining
elements. Then, for each energy value, we get the M.A.C. values
for the rest of the row by calling the find_mac function
with each interaction. If L.A.C. is the selected calculation mode,
the export_data function will handle the conversion by multiplying
these rows by the density.
"""
def make_df_for_material(file_like, df, element, category, interactions):
    # Reads in file
    reader = csv.DictReader(file_like)

    # Create the dataframe
    vals = []
    for row in reader:
        db_path = resource_path('Data/Modules/Attenuation/Photons/Elements/' + row['Element'] + '.csv')
        if len(vals) == 0:
            with open(db_path, 'r') as file:
                # Reads in file
                reader2 = csv.DictReader(file)

                # Gets energy values to use as dots
                for row2 in reader2:
                    vals.append(float(row2["Photon Energy"]))
        else:
            with open(db_path, 'r') as file:
                # Reads in file
                reader2 = csv.DictReader(file)

                new_vals = []
                # Gets energy values to use as dots
                for row2 in reader2:
                    new_vals.append(float(row2["Photon Energy"]))
                max_val = max(new_vals)
                min_val = min(new_vals)
                for val in vals:
                    if val > max_val or val < min_val:
                        vals.remove(val)

        # Finds the T.A.C. at each energy value and adds to dataframe
        for index, val in enumerate(vals):
            row = [val]
            for interaction in interactions:
                x = find_data(category, interaction, element, val, "Photons")
                row.append(x)
            df.loc[index] = row