##### IMPORTS #####
import csv
from tkinter import *
import matplotlib.pyplot as plt
import pandas as pd
from tkinter.ttk import Combobox
from ttkwidgets.autocomplete import AutocompleteCombobox
import defaults
import shelve

##### WINDOW SETUP #####
root = Tk()
root.title("Coefficient Request")
root.geometry("525x275")

##### HOME SCREEN BUTTONS #####
tac_button = Button(root)

### ERROR MESSAGES ###
non_number = "Error: Non-number energy input."
too_low = "Error: Energy too low."
too_high = "Error: Energy too high."
errors = [non_number, too_low, too_high]

# For global access to nodes on non-home screen
screen_list = []
advanced_list = []

# Choices using an element or a material
element_choices = ["Common Elements", "All Elements"]
material_choices = ["Common Materials", "All Materials"]

# Displays the requested coefficient
result_label = Text(root, height=1, borderwidth=0)
result_label.config(bg='white', fg='grey')

def total_attenuation_coefficient(selection_start="Common Elements",
                                  mode_start="Mass Attenuation Coefficient (cm\u00B2/g)",
                                  interaction="Total Attenuation with Coherent Scattering",
                                  common_el="Ag", common_mat="Air (dry, near sea level)",
                                  element="Ac",
                                  material="A-150 Tissue-Equivalent Plastic (A150TEP)"):
    global tac_button
    global screen_list

    choices = get_choices(selection_start)

    box_width = 5 if selection_start in element_choices else 35

    # Stores selection and sets default
    var_selection = StringVar(root)
    var_selection.set(selection_start)

    # Stores element/material selection
    var = StringVar(root)
    var.set(common_el if selection_start == "Common Elements" else
            common_mat if selection_start == "Common Materials" else
            element if selection_start == "All Elements" else material)

    # Changes to T.A.C. screen
    tac_button.pack_forget()

    # Frame for element selection and advanced settings button
    top_frame = Frame(root)
    top_frame.pack(pady=10)

    def select_selection(event):
        nonlocal choices
        nonlocal box_width

        event.widget.selection_clear()
        selection = var_selection.get()
        choices = get_choices(selection)
        var.set(common_el if selection == "Common Elements" else
                common_mat if selection == "Common Materials" else
                element if selection == "All Elements" else material)
        box_width = 5 if selection in element_choices else 35
        dropdown.config(completevalues=choices, width=box_width)
        root.focus()

    # Creates dropdown menu for selection
    selections = ["Common Elements", "All Elements",
                  "Common Materials", "All Materials"]
    selection_dropdown = Combobox(top_frame, textvariable=var_selection,
                                  values=selections, width=13, state='readonly')
    selection_dropdown.pack(side="left", padx=5)
    selection_dropdown.bind("<<ComboboxSelected>>", select_selection)

    def on_enter(_):
        nonlocal common_el, common_mat, element, material
        value = dropdown.get()
        selection = var_selection.get()
        if value not in choices:
            dropdown.set(common_el if selection == "Common Elements" else
                         common_mat if selection == "Common Materials" else
                         element if selection == "All Elements" else material)
        else:
            # Move focus away from the combobox
            selection = var_selection.get()
            if selection == "Common Elements":
                common_el = var.get()
            elif selection == "All Elements":
                element = var.get()
            elif selection == "Common Materials":
                common_mat = var.get()
            elif selection == "All Materials":
                material = var.get()
            root.focus()

    def on_select(event):
        event.widget.selection_clear()
        root.focus()

    # Creates dropdown menu for element selection
    dropdown = AutocompleteCombobox(top_frame, textvariable=var, completevalues=choices,
                                    width=box_width)
    dropdown.pack(side="left", padx=5)
    dropdown.bind('<Return>', on_enter)
    dropdown.bind("<<ComboboxSelected>>", on_select)
    dropdown.bind("<FocusOut>", on_enter)

    # Stores mode and sets default
    var_mode = StringVar(root)
    var_mode.set(mode_start)
    mode = mode_start

    label = Label(root, text="Energy (MeV):")
    entry = Entry(root, width=30)
    entry.config(bg='white', fg='grey')

    def select_mode(event):
        nonlocal label, entry
        nonlocal mode
        event.widget.selection_clear()
        result_label.pack_forget()
        if event.widget.get() == "Density (g/cm\u00B3)"\
           and mode != "Density (g/cm\u00B3)":
            label.pack_forget()
            entry.pack_forget()
        elif mode == "Density (g/cm\u00B3)"\
             and event.widget.get() != "Density (g/cm\u00B3)":
            screen_list.remove(label)
            screen_list.remove(entry)
            label.pack_forget()
            entry.pack_forget()
            calc.pack_forget()
            advanced.pack_forget()
            exit_button.pack_forget()
            label.pack()
            entry.pack()
            calc.pack(pady=5)
            advanced.pack(pady=2)
            exit_button.pack(pady=2)
            screen_list.append(label)
            screen_list.append(entry)
        mode = var_mode.get()
        root.focus()

    # Creates dropdown menu for mode
    mode_choices = ["Mass Attenuation Coefficient (cm\u00B2/g)",
                    "Density (g/cm\u00B3)",
                    "Linear Attenuation Coefficient (cm\u207B\u00B9)"]
    mode_dropdown = Combobox(root, textvariable=var_mode, values=mode_choices, width=26,
                             state='readonly')
    mode_dropdown.pack(pady=5)
    mode_dropdown.bind("<<ComboboxSelected>>", select_mode)

    # Energy input is not necessary if mode is density
    if var_mode.get() != "Density (g/cm\u00B3)":
        label.pack()
        entry.pack()

    # Creates calculate button
    calc = Button(root, text="Calculate",
                  command=lambda: handle_calculation(var_selection.get(), var_mode.get(),
                                                     interaction, var.get(),
                                                     entry.get()))
    calc.pack(pady=5)

    # Creates an advanced settings button
    advanced = Button(root, text="Advanced Settings",
                      command=lambda: tac_advanced(common_el, common_mat, element, material,
                                                   var_selection.get(),
                                                   var_mode.get(), interaction))
    advanced.pack(pady=2)

    # Creates exit button to return to home screen
    exit_button = Button(root, text="Exit", command=exit_to_home)
    exit_button.pack(pady=2)

    # Stores nodes into global list
    screen_list = [top_frame, dropdown, selection_dropdown, mode_dropdown,
                   label, entry, calc, advanced, exit_button]

def get_choices(selection):
    choices = []

    if selection == "All Elements" or selection == "All Materials":
        # Obtains list of elements from csv file
        name = "Elements" if selection == "All Elements" else "Materials"
        with open('attenuation/' + name + '/' + name + '.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != 'Name':
                    choices.append(row[0])
        return choices

    # Obtains list of elements from shelve
    with shelve.open(selection) as prefs:
        return prefs.get(selection, defaults.common_elements if selection == "Common Elements"
                                    else defaults.common_materials)

def tac_advanced(common_el, common_mat, element, material, selection, mode, interaction_start):
    global advanced_list

    # Hides T.A.C. screen
    clear()

    # Stores interaction and sets default
    var_interaction = StringVar(root)
    var_interaction.set(interaction_start)

    def select_interaction(event):
        event.widget.selection_clear()
        root.focus()

    # Creates dropdown menu for mode
    interaction_choices = ["Total Attenuation with Coherent Scattering",
                           "Total Attenuation without Coherent Scattering",
                           "Pair Production in Electron Field",
                           "Pair Production in Nuclear Field",
                           "Scattering - Incoherent",
                           "Scattering - Coherent",
                           "Photo-Electric Absorption"]
    interaction_dropdown = Combobox(root, textvariable=var_interaction,
                                    values=interaction_choices, width=32, state='readonly')
    interaction_dropdown.pack(pady=10)
    interaction_dropdown.bind("<<ComboboxSelected>>", select_interaction)

    # Creates plot button
    plot_button = Button(root, text="Plot",
                         command=lambda: plot_data(common_el if selection == "Common Elements"
                                                   else common_mat if
                                                        selection == "Common Materials"
                                                   else element if selection == "All Elements"
                                                   else material,
                                         selection, mode, var_interaction.get()))
    plot_button.pack(pady=5)

    # Creates exit button to return to T.A.C. screen
    exit_button = Button(root, text="Back",
                         command=lambda: tac_back(common_el, common_mat, element, material,
                                                  selection, mode,
                                                  var_interaction.get()))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [interaction_dropdown, plot_button, exit_button]

def plot_data(element, selection, mode, interaction):
    cols = ["Photon Energy", interaction]
    df = pd.DataFrame(columns=cols)
    if selection in material_choices:
        with open('attenuation/Materials/' + element + '.csv', 'r') as file:
            # Reads in file
            reader = csv.DictReader(file)

            # Create the dataframe
            vals = []
            for row in reader:
                with open('attenuation/Elements/' + row['Element'] + '.csv', 'r') as file2:
                    # Reads in file
                    reader2 = csv.DictReader(file2)

                    # Gets energy values to use as dots
                    if len(vals) == 0:
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
    else:
        # Load the CSV file
        df = pd.read_csv('attenuation/Elements/' + element + '.csv')

    if mode == "Linear Attenuation Coefficient (cm\u207B\u00B9)":
        df[interaction] *= find_density(selection, element)
    elif mode == "Density (g/cm\u00B3)":
        df[interaction][:] = find_density(selection, element)

    # Plot the data
    plt.plot(df["Photon Energy"], df[interaction], marker='o')
    plt.title(element + " - " + interaction, fontsize=8.5)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Photon Energy (MeV)')
    plt.ylabel(mode)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()

def tac_back(common_el, common_mat, element, material, selection, mode, interaction):
    clear_advanced()
    total_attenuation_coefficient(selection_start=selection, mode_start=mode,
                                  interaction=interaction, common_el=common_el,
                                  common_mat=common_mat, element=element, material=material)

def handle_calculation(selection, mode, interaction, element, energy_str):
    global result_label

    # Removes result label from past calculations
    result_label.pack_forget()

    # Energy input in float format
    energy_target = 0.0

    if mode != "Density (g/cm\u00B3)":
        # Error-check for a non-number energy input
        try:
            energy_target = float(energy_str)
        except ValueError:
            edit_result(non_number)
            result_label.pack(pady=5)
            return

    if mode == "Mass Attenuation Coefficient (cm\u00B2/g)":
        result = find_tac(selection, interaction, element, energy_target)
    elif mode == "Density (g/cm\u00B3)":
        result = find_density(selection, element)
    else:
        tac = find_tac(selection, interaction, element, energy_target)
        if tac in errors:
            result = tac
        else:
            result = tac * find_density(selection, element)

    # Displays result label
    edit_result(f"{result:.4g}")
    result_label.pack(pady=5)

def find_tac(selection, interaction, element, energy_target):
    if selection in element_choices:
        tac = find_tac_for_element(element, interaction, energy_target)
    else:
        tac = 0
        with open('attenuation/Materials/' + element + '.csv', 'r') as file:
            # Reads in file
            reader = csv.DictReader(file)

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
    with open('attenuation/Elements/' + element + '.csv', 'r') as file:
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
    difference = closest_high - closest_low
    percentage = (energy_target - closest_low) / difference
    coefficient = low_coefficient + percentage * (high_coefficient - low_coefficient)
    return coefficient

def find_density(selection, element):
    density = None
    if selection in element_choices:
        density = find_density_for_element(element)
    else:
        with open('attenuation/Materials/Materials.csv', 'r') as file:
            # Reads in file
            reader = csv.reader(file)

            # Sums each component's weighted density
            for row in reader:
                if row and row[0] == element:
                    density = float(row[1])
                    break
                density = None
    return density

def find_density_for_element(element):
    with open('attenuation/Elements/Periodic Table of Elements.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row and row['Symbol'] == element:
                return float(row['Density'])
        return None

def edit_result(result):
    # Clears result label and inserts new result
    result_label.config(state="normal")
    result_label.delete("1.0", END)
    result_label.insert(END, result)
    result_label.config(state="disabled")

def clear():
    global screen_list

    # Clears screen
    result_label.pack_forget()
    for node in screen_list:
        node.destroy()
    screen_list.clear()

def clear_advanced():
    global screen_list

    # Clears screen
    for node in advanced_list:
        node.destroy()
    advanced_list.clear()

def return_home():
    global tac_button

    # Creates buttons for home screen
    tac_button = Button(root, text="Total Attenuation Coefficient",
                        command=total_attenuation_coefficient)
    tac_button.pack(pady=5)

def exit_to_home():
    clear()
    return_home()

# Creates home screen upon launch
return_home()

# Runs app
root.mainloop()