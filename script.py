##### IMPORTS #####
import matplotlib.pyplot as plt
import pandas as pd
from tkinter.ttk import Combobox
from ttkwidgets.autocomplete import AutocompleteCombobox
import defaults
import shelve
from tac_calculations import *

##### WINDOW SETUP #####
root = Tk()
root.title("Coefficient Request")
root.geometry("725x350")

##### HOME SCREEN BUTTONS #####
tac_button = Button(root)

# For global access to nodes on non-home screen
screen_list = []
advanced_list = []

# Displays the requested coefficient
result_label = Text(root, height=1, borderwidth=0)
result_label.config(bg='white', fg='grey')

def on_select(event):
    event.widget.selection_clear()
    root.focus()

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

    # Make sure common default choices are valid selections
    common_elements = get_choices("Common Elements")
    if not common_el in common_elements:
        common_el = common_elements[0] if len(common_elements) > 0 else ""
    common_materials = get_choices("Common Materials")
    if not common_mat in common_materials:
        common_mat = common_materials[0] if len(common_materials) > 0 else ""

    # Stores selection and sets default
    var_selection = StringVar(root)
    var_selection.set(selection_start)

    # Stores element/material selection
    var = StringVar(root)
    var.set("" if choices == [] else
            common_el if selection_start == "Common Elements" else
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
        var.set("" if choices == [] else
                common_el if selection == "Common Elements" else
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
            dropdown.set("" if choices == [] else
                         common_el if selection == "Common Elements" else
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
                                                     entry.get(), result_label))
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
                if row and row[0] != 'Name':
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

    # Frame for add common elements option
    e_frame = Frame(root)
    e_frame.pack(pady=10)

    # Frame for add common elements option
    add_ce_frame = Frame(e_frame)
    add_ce_frame.pack(side='left', padx=5)

    add_ce_label = Label(add_ce_frame, text="Add Common Element:")
    add_ce_label.pack()

    # Gets non-common elements
    elements = get_choices("All Elements")
    common = get_choices("Common Elements")
    non_common = [element for element in elements if element not in common]

    # Stores element and sets default
    var_add = StringVar(root)
    var_add.set(non_common[0] if len(non_common) > 0 else "")

    on_enter_add_ce = make_enter(var_add, non_common)
    add_ce_dropdown = make_ac_box(add_ce_frame, var_add, non_common,
                                  on_enter_add_ce, 5)

    # Creates add common element button
    add_ce_button = Button(add_ce_frame, text="Add",
                           command=lambda:add_c("Common Elements", common, non_common, var_add,
                                                add_ce_dropdown, var_remove, remove_ce_dropdown))
    add_ce_button.pack()

    # Frame for remove common elements option
    remove_ce_frame = Frame(e_frame)
    remove_ce_frame.pack(side='left', padx=5)

    remove_ce_label = Label(remove_ce_frame, text="Remove Common Element:")
    remove_ce_label.pack()

    # Stores element and sets default
    var_remove = StringVar(root)
    var_remove.set(common[0] if len(common) > 0 else "")

    on_enter_remove_ce = make_enter(var_remove, common)
    remove_ce_dropdown = make_ac_box(remove_ce_frame, var_remove, common,
                                     on_enter_remove_ce, 5)

    # Creates add common element button
    remove_ce_button = Button(remove_ce_frame, text="Remove",
                              command=lambda: remove_c("Common Elements", common, non_common,
                                                       var_add, add_ce_dropdown, var_remove,
                                                       remove_ce_dropdown))
    remove_ce_button.pack()

    # Frame for add common elements option
    m_frame = Frame(root)
    m_frame.pack(pady=10)

    # Frame for add common elements option
    add_cm_frame = Frame(m_frame)
    add_cm_frame.pack(side='left', padx=5)

    add_cm_label = Label(add_cm_frame, text="Add Common Material:")
    add_cm_label.pack()

    # Gets non-common elements
    materials = get_choices("All Materials")
    common_m = get_choices("Common Materials")
    non_common_m = [material for material in materials if material not in common_m]

    # Stores element and sets default
    var_add_m = StringVar(root)
    var_add_m.set(non_common_m[0] if len(non_common_m) > 0 else "")

    on_enter_add_cm = make_enter(var_add_m, non_common_m)
    add_cm_dropdown = make_ac_box(add_cm_frame, var_add_m, non_common_m,
                                  on_enter_add_cm, 35)

    # Creates add common element button
    add_cm_button = Button(add_cm_frame, text="Add",
                           command=lambda: add_c("Common Materials", common_m, non_common_m,
                                                 var_add_m, add_cm_dropdown, var_remove_m,
                                                 remove_cm_dropdown))
    add_cm_button.pack()

    # Frame for remove common elements option
    remove_cm_frame = Frame(m_frame)
    remove_cm_frame.pack(side='left', padx=5)

    remove_cm_label = Label(remove_cm_frame, text="Remove Common Material:")
    remove_cm_label.pack()

    # Stores element and sets default
    var_remove_m = StringVar(root)
    var_remove_m.set(common_m[0] if len(common_m) > 0 else "")

    on_enter_remove_cm = make_enter(var_remove_m, common_m)
    remove_cm_dropdown = make_ac_box(remove_cm_frame, var_remove_m, common_m,
                                     on_enter_remove_cm, 35)

    # Creates add common element button
    remove_cm_button = Button(remove_cm_frame, text="Remove",
                              command=lambda: remove_c("Common Materials", common_m,
                                                       non_common_m, var_add_m, add_cm_dropdown,
                                                       var_remove_m, remove_cm_dropdown))
    remove_cm_button.pack()

    # Stores interaction and sets default
    var_interaction = StringVar(root)
    var_interaction.set(interaction_start)

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
    interaction_dropdown.bind("<<ComboboxSelected>>", on_select)

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
                         command=lambda: tac_back(common_el if common_el in common
                                                  else common[0] if len(common) > 0 else "",
                                                  common_mat if common_mat in common_m
                                                  else common_m[0] if len(common_m) > 0 else "",
                                                  element, material, selection, mode,
                                                  var_interaction.get()))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [interaction_dropdown, plot_button, add_ce_frame, add_ce_label,
                     add_ce_dropdown, add_ce_button, remove_ce_frame, remove_ce_label,
                     remove_ce_dropdown, remove_ce_button, e_frame, m_frame, add_cm_frame,
                     add_cm_label, add_cm_dropdown, add_cm_button, remove_cm_frame,
                     remove_cm_label, remove_cm_dropdown, remove_cm_button, exit_button]

def make_enter(var, choices):
    def on_enter(_):
        value = var.get()
        if value not in choices:
            var.set(choices[0] if len(choices) > 0 else "")
        else:
            # Move focus away from the combobox
            root.focus()
    return on_enter

def make_ac_box(frame, var, choices, enter, width):
    dropdown = AutocompleteCombobox(frame, textvariable=var,
                                    completevalues=choices, width=width)
    dropdown.pack()
    dropdown.bind('<Return>', enter)
    dropdown.bind("<<ComboboxSelected>>", on_select)
    dropdown.bind("<FocusOut>", enter)
    return dropdown

def add_c(selection, common, non_common, var_add, add_c_dropdown, var_remove, remove_c_dropdown):
    with shelve.open(selection) as prefs:
        # Adds element to common elements
        element = var_add.get()
        if element == "":
            return
        choices = prefs.get(selection, defaults.common_elements if selection == "Common Elements"
                                       else defaults.common_materials)
        choices.append(element)
        if not choices is common:
            common.append(element)
        prefs[selection] = choices
        remove_c_dropdown.config(completevalues=choices)
        if var_remove.get() == "":
            var_remove.set(element)

        # Removes element from non-common elements
        non_common.remove(element)
        add_c_dropdown.config(completevalues=non_common)
        var_add.set(non_common[0] if len(non_common) > 0 else "")

def remove_c(selection, common, non_common, var_add, add_c_dropdown, var_remove, remove_c_dropdown):
    with shelve.open(selection) as prefs:
        # Removes element from common elements
        element = var_remove.get()
        if element == "":
            return
        choices = prefs.get(selection, defaults.common_elements if selection == "Common Elements"
                                       else defaults.common_materials)
        choices.remove(element)
        if not choices is common:
            common.remove(element)
        prefs[selection] = choices
        remove_c_dropdown.config(completevalues=choices)
        var_remove.set(choices[0] if len(choices) > 0 else "")

        # Adds element to non-common elements
        non_common.append(element)
        add_c_dropdown.config(completevalues=non_common)
        if var_add.get() == "":
            var_add.set(element)

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