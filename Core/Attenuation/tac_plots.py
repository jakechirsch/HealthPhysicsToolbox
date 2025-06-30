##### IMPORTS #####
import matplotlib.pyplot as plt
import pandas as pd
from Core.Attenuation.tac_calculations import *
from tkinter.filedialog import asksaveasfilename

def plot_data(root, element, selection, mode, interactions, num, den,
              energy_unit, choice, save, error_label):
    root.focus()
    if element == "":
        error_label.config(style="Error.TLabel", text="Error: No element or material selected.")
        return
    if len(interactions) == 0:
        error_label.config(style="Error.TLabel", text="Error: No interactions selected.")
        return
    error_label.config(style="Error.TLabel", text="")
    energy_col = "Photon Energy (" + energy_unit + ")"
    cols = [energy_col]
    for interaction in interactions:
        cols.append(interaction)
    df = pd.DataFrame(columns=cols)
    if selection in element_choices:
        # Load the CSV file
        db_path = resource_path('Data/Modules/Mass Attenuation/Elements/' + element + '.csv')
        df2 = pd.read_csv(db_path)
        df[energy_col] = df2["Photon Energy"]
        df[energy_col] /= energy_units[energy_unit]
        for interaction in interactions:
            df[interaction] = df2[interaction]
    elif selection in material_choices:
        db_path = resource_path('Data/General Data/Material Composition/' + element + '.csv')
        with open(db_path, 'r') as file:
            make_df_for_material(file, df, element, selection, interactions)
    else:
        db_path = get_user_data_path('Mass Attenuation/_' + element)
        with shelve.open(db_path) as db:
            stored_data = db[element]
            stored_data = stored_data.replace('\\n', '\n')

        # Create file-like object from the stored string
        csv_file_like = io.StringIO(stored_data)

        make_df_for_material(csv_file_like, df, element, selection, interactions)

    for interaction in interactions:
        if mode == "Mass Attenuation Coefficient":
            df[interaction] *= mac_numerator[num]
            df[interaction] /= mac_denominator[den]
        else:
            df[interaction] *= find_density(selection, element, "Mass Attenuation")
            df[interaction] *= lac_numerator[num]
            df[interaction] /= lac_denominator[den]

    # Clear from past plots
    plt.clf()

    # Plot the data
    for interaction in interactions:
        plt.plot(df[energy_col], df[interaction], marker='o', label=interaction)
    unit = " (" + num + "/" + den + ")"
    title = element + " - " + mode + unit
    plt.title(title, fontsize=8.5)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.xlabel(energy_col)
    y_label = mode + " (" + num + "/" + den + ")"
    plt.ylabel(y_label)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save == 1:
        if choice == "Plot":
            save_file(plt, choice, error_label, element)
        else:
            for interaction in interactions:
                df.rename(columns={interaction: interaction+unit}, inplace=True)
            save_file(df, choice, error_label, element)
    else:
        plt.show()
        error_label.config(style="Success.TLabel", text=choice + " exported!")

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

def make_df_for_material(file_like, df, element, selection, interactions):
    # Reads in file
    reader = csv.DictReader(file_like)

    # Create the dataframe
    vals = []
    for row in reader:
        db_path = resource_path('Data/Modules/Mass Attenuation/Elements/' + row['Element'] + '.csv')
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
                x = find_tac(selection, interaction, element, val)
                row.append(x)
            df.loc[index] = row