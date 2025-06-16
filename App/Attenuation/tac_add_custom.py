##### IMPORTS #####
import shelve
from tkinter import *

# For global access to nodes on custom screen
custom_list = []

def custom_menu(root, common_el, common_mat, element, material, custom_mat,
                selection, mode, interaction, mac_num, d_num, lac_num, mac_den,
                d_den, lac_den, energy_unit):
    global custom_list

    label = Label(root, text="Material Name:")
    entry = Entry(root, width=20)
    entry.config(bg='white', fg='grey')
    label.pack()
    entry.pack()
    label2 = Label(root, text="Density")
    entry2 = Entry(root, width=20)
    entry2.config(bg='white', fg='grey')
    label2.pack()
    entry2.pack()
    label3 = Label(root, text='"Weight","Element"\\n')
    entry3 = Entry(root, width=20)
    entry3.config(bg='white', fg='grey')
    label3.pack()
    entry3.pack()

    # Creates button
    button = Button(root, text="Add",
                    command=lambda: add_custom(root, entry, entry2, entry3))
    button.pack()

    # Creates exit button to return to T.A.C. screen
    exit_button = Button(root, text="Back",
                         command=lambda: advanced_back(root, common_el, common_mat,
                                                       element, material, custom_mat,
                                                       selection, mode, interaction,
                                                       mac_num, d_num, lac_num,
                                                       mac_den, d_den, lac_den, energy_unit))
    exit_button.pack(pady=2)

    # Stores nodes into global list
    custom_list = [label, entry, label2, entry2, label3, entry3, button, exit_button]

def add_custom(root, name_box, density_box, weights_box):
    name = name_box.get()
    density = density_box.get()
    weights = weights_box.get()
    csv_data = '"Weight","Element"\n' + weights

    with shelve.open("Data/Modules/Mass Attenuation/User/Custom Materials") as prefs:
        choices = prefs.get("Custom Materials", [])
        if not name in choices:
            choices.append(name)
        prefs["Custom Materials"] = choices

    # Save to shelve
    with shelve.open('Data/Modules/Mass Attenuation/User/_' + name) as db:
        db[name] = csv_data
        db[name + '_Density'] = density

    name_box.delete(0, END)
    weights_box.delete(0, END)
    density_box.delete(0, END)
    root.focus()

def clear_custom():
    global custom_list

    # Clears advanced
    for node in custom_list:
        node.destroy()
    custom_list.clear()

def advanced_back(root, common_el, common_mat, element, material, custom_mat,
                  selection, mode, interaction, mac_num, d_num, lac_num,
                  mac_den, d_den, lac_den, energy_unit):
    from App.Attenuation.tac_advanced import tac_advanced

    clear_custom()
    print("hi")
    tac_advanced(root, selection=selection, mode=mode,
                 interaction_start=interaction, common_el=common_el,
                 common_mat=common_mat, element=element, material=material,
                 custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                 lac_num=lac_num, mac_den=mac_den, d_den=d_den,
                 lac_den=lac_den, energy_unit=energy_unit)