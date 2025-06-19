##### IMPORTS #####
from Core.Attenuation.tac_plots import *
from App.Attenuation.tac_unit_settings import *

# For global access to nodes on export screen
export_list = []

def export_menu(root, common_el, common_mat, element, material, custom_mat,
                selection, mode, interaction_start, mac_num, d_num, lac_num,
                mac_den, d_den, lac_den, energy_unit):
    global export_list

    def on_select_export(event):
        nonlocal var_save
        event.widget.selection_clear()
        root.focus()
        if event.widget.get() == "Data":
            var_save.set(1)
            save.config(state="disabled")
        else:
            save.config(state="normal")

    export_label = ttk.Label(root, text="Export Options:", style="Maize.TLabel")
    export_label.pack(pady=2)

    # Creates dropdown menu for export
    export_choices = ["Plot", "Data"]
    export_dropdown = ttk.Combobox(root, values=export_choices, width=4,
                                   justify="center", state='readonly',
                                   style="Maize.TCombobox")
    export_dropdown.set("Plot")
    export_dropdown.pack(pady=2)
    export_dropdown.bind("<<ComboboxSelected>>", on_select_export)

    interactions_frame = Frame(root, bg="#00274C")
    interactions_frame.pack(pady=2)

    # Variables for each interaction type
    var0 = IntVar()
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()

    # Checkboxes for each interaction type
    interaction_checkbox(interactions_frame, var0, "Total Attenuation with Coherent Scattering")
    interaction_checkbox(interactions_frame, var1, "Total Attenuation without Coherent Scattering")
    interaction_checkbox(interactions_frame, var2, "Pair Production in Electron Field")
    interaction_checkbox(interactions_frame, var3, "Pair Production in Nuclear Field")
    interaction_checkbox(interactions_frame, var4, "Scattering - Incoherent")
    interaction_checkbox(interactions_frame, var5, "Scattering - Coherent")
    interaction_checkbox(interactions_frame, var6, "Photo-Electric Absorption")

    # Checkbox for saving file
    var_save = IntVar()
    var_save.set(1)

    save = ttk.Checkbutton(root, text="Save file", variable=var_save,
                           style="Maize.TCheckbutton")
    save.pack(pady=2)

    # Creates export button
    export_button = ttk.Button(root, text="Export", style="Maize.TButton",
                               padding=(-20,0),
                               command=lambda:
                               plot_data(common_el if selection == "Common Elements" else
                                         common_mat if selection == "Common Materials" else
                                         element if selection == "All Elements" else
                                         material if selection == "All Materials" else
                                         custom_mat if selection == "Custom Materials"
                                         else "", selection, mode,
                                         get_interactions(var0, var1, var2, var3, var4, var5, var6),
                                         get_unit(mac_num, d_num, lac_num, mode),
                                         get_unit(mac_den, d_den, lac_den, mode),
                                         energy_unit, export_dropdown.get(),
                                         var_save.get(), error_label))
    export_button.pack(pady=5)

    # Creates error label for bad input
    error_label = ttk.Label(root, text="", style="Error.TLabel")
    error_label.pack(pady=2)

    # Creates exit button to return to T.A.C. screen
    exit_button = ttk.Button(root, text="Back", style="Maize.TButton", padding=(-20,0),
                             command=lambda: advanced_back(root, common_el, common_mat,
                                                           element, material, custom_mat,
                                                           selection, mode, interaction_start,
                                                           mac_num, d_num, lac_num,
                                                           mac_den, d_den, lac_den, energy_unit))
    exit_button.pack(pady=2)

    export_list = [export_label, export_dropdown, export_button, exit_button,
                   interactions_frame, error_label, save]

def interaction_checkbox(frame, variable, interaction):
    check = ttk.Checkbutton(frame, text=interaction, variable=variable,
                            style="Maize.TCheckbutton")
    check.pack()

def get_interactions(var0, var1, var2, var3, var4, var5, var6):
    interactions = []
    if var0.get() == 1:
        interactions.append("Total Attenuation with Coherent Scattering")
    if var1.get() == 1:
        interactions.append("Total Attenuation without Coherent Scattering")
    if var2.get() == 1:
        interactions.append("Pair Production in Electron Field")
    if var3.get() == 1:
        interactions.append("Pair Production in Nuclear Field")
    if var4.get() == 1:
        interactions.append("Scattering - Incoherent")
    if var5.get() == 1:
        interactions.append("Scattering - Coherent")
    if var6.get() == 1:
        interactions.append("Photo-Electric Absorption")
    return interactions

def clear_export():
    global export_list

    # Clears export screen
    for node in export_list:
        node.destroy()
    export_list.clear()

def advanced_back(root, common_el, common_mat, element, material, custom_mat,
                  selection, mode, interaction_start, mac_num, d_num, lac_num,
                  mac_den, d_den, lac_den, energy_unit):
    from App.Attenuation.tac_advanced import tac_advanced

    clear_export()
    tac_advanced(root, selection=selection, mode=mode,
                 interaction_start=interaction_start, common_el=common_el,
                 common_mat=common_mat, element=element, material=material,
                 custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                 lac_num=lac_num, mac_den=mac_den, d_den=d_den,
                 lac_den=lac_den, energy_unit=energy_unit)