##### IMPORTS #####
import matplotlib.pyplot as plt
import pandas as pd
from tkinter.ttk import Combobox
from ttkwidgets.autocomplete import AutocompleteCombobox
import defaults
from tac_calculations import *
import os
import subprocess
import platform

##### WINDOW SETUP #####
root = Tk()
root.title("Coefficient Request")
root.geometry("725x400")

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
                                  material="A-150 Tissue-Equivalent Plastic (A150TEP)",
                                  custom_mat=""):
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
    custom_materials = get_choices("Custom Materials")
    if not custom_mat in custom_materials:
        custom_mat = custom_materials[0] if len(custom_materials) > 0 else ""

    # Stores selection and sets default
    var_selection = StringVar(root)
    var_selection.set(selection_start)

    # Stores element/material selection
    var = StringVar(root)
    var.set("" if choices == [] else
            common_el if selection_start == "Common Elements" else
            common_mat if selection_start == "Common Materials" else
            element if selection_start == "All Elements" else
            material if selection_start == "All Materials" else
            custom_mat if selection_start == "Custom Materials" else "")

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
                element if selection == "All Elements" else
                material if selection == "All Materials" else
                custom_mat if selection == "Custom Materials" else "")
        box_width = 5 if selection in element_choices else 35
        dropdown.config(completevalues=choices, width=box_width)
        root.focus()

    # Creates dropdown menu for selection
    selections = ["Common Elements", "All Elements",
                  "Common Materials", "All Materials",
                  "Custom Materials"]
    selection_dropdown = Combobox(top_frame, textvariable=var_selection,
                                  values=selections, width=13, state='readonly')
    selection_dropdown.pack(side="left", padx=5)
    selection_dropdown.bind("<<ComboboxSelected>>", select_selection)

    def on_enter(_):
        nonlocal common_el, common_mat, element, material, custom_mat
        value = dropdown.get()
        selection = var_selection.get()
        if value not in choices:
            dropdown.set("" if choices == [] else
                         common_el if selection == "Common Elements" else
                         common_mat if selection == "Common Materials" else
                         element if selection == "All Elements" else
                         material if selection == "All Materials" else
                         custom_mat if selection == "Custom Materials" else "")
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
            elif selection == "Custom Materials":
                custom_mat = var.get()
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
                                                   custom_mat, var_selection.get(),
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
        choices.sort()
        return choices

    # Obtains list of elements from shelve
    with shelve.open(selection) as prefs:
        choices = prefs.get(selection,
                            defaults.common_elements if selection == "Common Elements"
                            else defaults.common_materials if selection == "Common Materials"
                            else [])
        choices.sort()
        return choices

def tac_advanced(common_el, common_mat, element, material, custom_mat,
                 selection, mode, interaction_start):
    global advanced_list

    # Hides T.A.C. screen
    clear()

    # Gets common and non-common elements
    elements = get_choices("All Elements")
    common = get_choices("Common Elements")
    non_common = [element for element in elements if element not in common]

    # Gets common and non-common materials
    materials = get_choices("All Materials")
    common_m = get_choices("Common Materials")
    non_common_m = [material for material in materials if material not in common_m]

    # Gets custom materials
    custom = get_choices("Custom Materials")

    # Frame for add/remove settings
    top_frame = Frame(root)
    top_frame.pack(pady=10)

    def on_select_options(event):
        nonlocal vertical_frame
        on_select(event)
        vertical_frame.destroy()
        vertical_frame = Frame(top_frame)
        vertical_frame.pack(side='left', padx=5)
        make_vertical_frame(vertical_frame, action_dropdown.get(), category_dropdown.get(),
                            non_common, common, non_common_m, common_m, custom)

    # Creates dropdown menu for action
    action_choices = ["Add", "Remove"]
    action_dropdown = Combobox(top_frame, values=action_choices, width=6, state='readonly')
    action_dropdown.set("Add")
    action_dropdown.pack(side='left', padx=5)
    action_dropdown.bind("<<ComboboxSelected>>", on_select_options)

    # Creates dropdown menu for category
    category_choices = ["Common Elements", "Common Materials", "Custom Materials"]
    category_dropdown = Combobox(top_frame, values=category_choices, width=13, state='readonly')
    category_dropdown.set("Common Elements")
    category_dropdown.pack(side='left', padx=5)
    category_dropdown.bind("<<ComboboxSelected>>", on_select_options)

    # Frame for specific add/remove settings
    vertical_frame = Frame(top_frame)
    vertical_frame.pack(side='left', padx=5)
    make_vertical_frame(vertical_frame, action_dropdown.get(), category_dropdown.get(),
                        non_common, common, non_common_m, common_m, custom)

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
                                                   else material if selection == "All Materials"
                                                   else custom_mat
                                                   if selection == "Custom Materials"
                                                   else "",
                                                   selection, mode, var_interaction.get()))
    plot_button.pack(pady=5)

    # Frame for references & help
    bottom_frame = Frame(root)
    bottom_frame.pack(pady=10)

    # Creates references button
    references_button = Button(bottom_frame, text="References",
                               command=lambda: open_file('References.txt'))
    references_button.pack(side='left', padx=5)

    # Creates help button
    help_button = Button(bottom_frame, text="Help",
                         command=lambda: open_file('Help.txt'))
    help_button.pack(side='left', padx=5)

    # Creates exit button to return to T.A.C. screen
    exit_button = Button(root, text="Back",
                         command=lambda: tac_back(common_el if common_el in common
                                                  else common[0] if len(common) > 0 else "",
                                                  common_mat if common_mat in common_m
                                                  else common_m[0] if len(common_m) > 0 else "",
                                                  element, material,
                                                  custom_mat if custom_mat in custom
                                                  else custom[0] if len(custom) > 0 else "",
                                                  selection, mode,
                                                  var_interaction.get()))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    advanced_list = [interaction_dropdown, plot_button,
                     exit_button, top_frame, bottom_frame]

def make_vertical_frame(vertical_frame, action, category,
                        non_common, common, non_common_m, common_m, custom):
    label = Label(vertical_frame,
                  text=action + " " + \
                       category + ":")
    label.pack()

    # Stores element and sets default
    var = StringVar(root)
    choices = []
    inverse = []
    width = 5
    if action == "Add" and category == "Common Elements":
        var.set(non_common[0] if len(non_common) > 0 else "")
        choices = non_common
        inverse = common
    elif action == "Add" and category == "Common Materials":
        var.set(non_common_m[0] if len(non_common_m) > 0 else "")
        choices = non_common_m
        inverse = common_m
        width = 35
    elif action == "Remove" and category == "Common Elements":
        var.set(common[0] if len(common) > 0 else "")
        choices = common
        inverse = non_common
    elif action == "Remove" and category == "Common Materials":
        var.set(common_m[0] if len(common_m) > 0 else "")
        choices = common_m
        inverse = non_common_m
        width = 35
    elif action == "Remove" and category == "Custom Materials":
        var.set(custom[0] if len(custom) > 0 else "")
        choices = custom
        width = 35

    if action == "Add" and category == "Custom Materials":
        label = Label(vertical_frame, text="Material Name:")
        entry = Entry(vertical_frame, width=20)
        entry.config(bg='white', fg='grey')
        label.pack()
        entry.pack()
        label2 = Label(vertical_frame, text='"Weight","Element"\\n')
        entry2 = Entry(vertical_frame, width=20)
        entry2.config(bg='white', fg='grey')
        label2.pack()
        entry2.pack()
        label3 = Label(vertical_frame, text="Density (g/cm\u00B3)")
        entry3 = Entry(vertical_frame, width=20)
        entry3.config(bg='white', fg='grey')
        label3.pack()
        entry3.pack()

        # Creates button
        button = Button(vertical_frame, text=action,
                        command=lambda: add_custom(entry, entry2, entry3))
        button.pack()
    else:
        on_enter = make_enter(var, choices)
        dropdown = make_ac_box(vertical_frame, var, choices,
                               on_enter, width)

        # Creates button
        if action == "Remove" and category == "Custom Materials":
            button = Button(vertical_frame, text=action,
                            command=lambda: carry_action(action, category,
                                                         choices, [var.get()], var, dropdown))
        else:
            button = Button(vertical_frame, text=action,
                            command=lambda: carry_action(action, category,
                                                         choices, inverse, var, dropdown))
        button.pack()

def add_custom(name_box, weights_box, density_box):
    name = name_box.get()
    weights = weights_box.get()
    density = density_box.get()
    csv_data = '"Weight","Element"\n' + weights

    with shelve.open("Custom Materials") as prefs:
        choices = prefs.get("Custom Materials", [])
        if not name in choices:
            choices.append(name)
        prefs["Custom Materials"] = choices

    # Save to shelve
    with shelve.open('_' + name) as db:
        db[name] = csv_data
        db[name + '_Density'] = density

    name_box.delete(0, END)
    weights_box.delete(0, END)
    density_box.delete(0, END)
    root.focus()

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

def carry_action(action, category, choices, inverse, var, dropdown):
    if action == "Add":
        add_c(category, choices, inverse, var, dropdown)
    elif action == "Remove":
        remove_c(category, choices, inverse, var, dropdown)

def add_c(selection, choices, inverse, var, dropdown):
    with shelve.open(selection) as prefs:
        # Adds element to common elements
        element = var.get()
        if element == "":
            return
        inverse.append(element)
        prefs[selection] = inverse

        # Removes element from non-common elements
        choices.remove(element)
        dropdown.config(completevalues=choices)
        var.set(choices[0] if len(choices) > 0 else "")

def remove_c(selection, choices, inverse, var, dropdown):
    with shelve.open(selection) as prefs:
        # Removes element from common elements
        element = var.get()
        if element == "":
            return
        choices.remove(element)
        prefs[selection] = choices
        dropdown.config(completevalues=choices)
        var.set(choices[0] if len(choices) > 0 else "")

        # Adds element to non-common elements
        inverse.append(element)

def plot_data(element, selection, mode, interaction):
    cols = ["Photon Energy", interaction]
    df = pd.DataFrame(columns=cols)
    if selection in element_choices:
        # Load the CSV file
        df = pd.read_csv('attenuation/Elements/' + element + '.csv')
    elif selection in material_choices:
        with open('attenuation/Materials/' + element + '.csv', 'r') as file:
            make_df_for_material(file, df, element, selection, interaction)
    else:
        with shelve.open('_' + element) as db:
            stored_data = db[element]
            stored_data = stored_data.replace('\\n', '\n')

        # Create file-like object from the stored string
        csv_file_like = io.StringIO(stored_data)

        make_df_for_material(csv_file_like, df, element, selection, interaction)

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

def make_df_for_material(file_like, df, element, selection, interaction):
    # Reads in file
    reader = csv.DictReader(file_like)

    # Create the dataframe
    vals = []
    for row in reader:
        with open('attenuation/Elements/' + row['Element'] + '.csv', 'r') as file:
            # Reads in file
            reader2 = csv.DictReader(file)

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

def tac_back(common_el, common_mat, element, material, custom_mat,
             selection, mode, interaction):
    clear_advanced()
    total_attenuation_coefficient(selection_start=selection, mode_start=mode,
                                  interaction=interaction, common_el=common_el,
                                  common_mat=common_mat, element=element, material=material,
                                  custom_mat=custom_mat)

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

def open_file(path):
    if platform.system() == 'Windows':
        os.startfile(path)
    elif platform.system() == 'Darwin':  # macOS
        subprocess.run(['open', path])
    else:  # Assume Linux or Unix
        subprocess.run(['xdg-open', path])

# Creates home screen upon launch
return_home()

# Runs app
root.mainloop()