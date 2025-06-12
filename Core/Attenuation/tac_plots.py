##### IMPORTS #####
import matplotlib.pyplot as plt
import pandas as pd
from Core.Attenuation.tac_calculations import *

def plot_data(element, selection, mode, interaction, num, den,
              export=False, choice=""):
    cols = ["Photon Energy (MeV)", interaction]
    df = pd.DataFrame(columns=cols)
    if selection in element_choices:
        # Load the CSV file
        df2 = pd.read_csv('Data/Modules/Mass Attenuation/Elements/' + element + '.csv')
        df["Photon Energy (MeV)"] = df2["Photon Energy"]
        df[interaction] = df2[interaction]
    elif selection in material_choices:
        with open('Data/General Data/Material Composition/' + element + '.csv',
                  'r') as file:
            make_df_for_material(file, df, element, selection, interaction)
    else:
        with shelve.open('_' + element) as db:
            stored_data = db[element]
            stored_data = stored_data.replace('\\n', '\n')

        # Create file-like object from the stored string
        csv_file_like = io.StringIO(stored_data)

        make_df_for_material(csv_file_like, df, element, selection, interaction)

    if mode == "Linear Attenuation Coefficient":
        df[interaction] *= find_density(selection, element)
    elif mode == "Density":
        df.loc[:, interaction] = find_density(selection, element)

    if mode == "Mass Attenuation Coefficient":
        df[interaction] *= mac_numerator[num]
        df[interaction] /= mac_denominator[den]
    elif mode == "Density":
        df[interaction] *= density_numerator[num]
        df[interaction] /= density_denominator[den]
    else:
        df[interaction] *= lac_numerator[num]
        df[interaction] /= lac_denominator[den]

    # Plot the data
    plt.plot(df["Photon Energy (MeV)"], df[interaction], marker='o')
    title = element + " - " + interaction
    plt.title(title, fontsize=8.5)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Photon Energy (MeV)')
    y_label = mode + " (" + num + "/" + den + ")"
    plt.ylabel(y_label)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if export:
        if choice == "Plot":
            # Save the plot as a PNG file
            plt.savefig(title + ".png")
            open_file(title + ".png")
        else:
            # Save the data as a CSV file
            unit = " (" + num + "_per_" + den + ")"
            mode += unit
            df.to_csv(element + " - " + mode + ".csv", index=False)
            open_file(element + " - " + mode + ".csv")
    else:
        # Show the plot
        plt.show()

def make_df_for_material(file_like, df, element, selection, interaction):
    # Reads in file
    reader = csv.DictReader(file_like)

    # Create the dataframe
    vals = []
    for row in reader:
        if len(vals) == 0:
            with open('Data/Modules/Mass Attenuation/Elements/' + row['Element'] + '.csv',
                      'r') as file:
                # Reads in file
                reader2 = csv.DictReader(file)

                # Gets energy values to use as dots
                for row2 in reader2:
                    vals.append(float(row2["Photon Energy"]))

        # Finds the T.A.C. at each energy value and adds to dataframe
        for index, val in enumerate(vals):
            x = find_tac(selection, interaction, element, val)
            index_sub = 0
            if x not in errors:
                df.loc[index - index_sub] = [val, x]
            else:
                index_sub += 1