##### IMPORTS #####
from Core.Attenuation.tac_plots import *
from App.Attenuation.tac_unit_settings import *
from App.style import SectionFrame

# For global access to nodes on export screen
export_list = []

def export_menu(root, common_el, common_mat, element, material, custom_mat,
                selection, mode, interactions, mac_num, d_num, lac_num,
                mac_den, d_den, lac_den, energy_unit):
    global export_list

    # Frame for interactions
    interactions_frame = SectionFrame(root, title="Interaction Types")
    interactions_frame.pack(padx=10, pady=10)
    inner_interactions_frame = interactions_frame.get_inner_frame()
    inner_interactions_frame.config(padx=20, pady=10)

    def on_select():
        root.focus()

    # Variables for each interaction type
    var0 = IntVar()
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()

    # Checkboxes for each interaction type
    interaction_checkbox(inner_interactions_frame, var0,
                         "Total Attenuation with Coherent Scattering", on_select)
    interaction_checkbox(inner_interactions_frame, var1,
                         "Total Attenuation without Coherent Scattering", on_select)
    interaction_checkbox(inner_interactions_frame, var2,
                         "Pair Production in Electron Field", on_select)
    interaction_checkbox(inner_interactions_frame, var3,
                         "Pair Production in Nuclear Field", on_select)
    interaction_checkbox(inner_interactions_frame, var4,
                         "Scattering - Incoherent", on_select)
    interaction_checkbox(inner_interactions_frame, var5,
                         "Scattering - Coherent", on_select)
    interaction_checkbox(inner_interactions_frame, var6,
                         "Photo-Electric Absorption", on_select)

    # Spacer
    empty_frame1 = make_spacer(root)

    def save():
        root.focus()

    # Checkbox for saving file
    var_save = IntVar()
    var_save.set(1)

    # Frame for options
    options_frame = SectionFrame(root, title="Options")
    options_frame.pack(padx=10, pady=10)
    inner_options_frame = options_frame.get_inner_frame()

    save = ttk.Checkbutton(inner_options_frame, text="Save File", variable=var_save,
                           style="Maize.TCheckbutton", command=save)
    save.pack(padx=133, pady=5)

    export_type_frame = Frame(inner_options_frame, bg="#D3D3D3")
    export_type_frame.pack(pady=5)

    def on_select_export(event):
        nonlocal var_save
        event.widget.selection_clear()
        root.focus()
        if event.widget.get() == "Data":
            var_save.set(1)
            save.config(state="disabled")
        else:
            save.config(state="normal")

    export_label = ttk.Label(export_type_frame, text="Select Export Type:", style="Black.TLabel")
    export_label.pack()

    # Creates dropdown menu for export
    export_choices = ["Plot", "Data"]
    export_dropdown = ttk.Combobox(export_type_frame, values=export_choices,
                                   justify="center", state='readonly',
                                   style="Maize.TCombobox")
    export_dropdown.config(width=get_width(export_choices))
    export_dropdown.set("Plot")
    export_dropdown.pack()
    export_dropdown.bind("<<ComboboxSelected>>", on_select_export)

    # Creates export button
    export_button = ttk.Button(inner_options_frame, text="Export", style="Maize.TButton",
                               padding=(0,0),
                               command=lambda:
                               plot_data(root,
                                         common_el if selection == "Common Elements" else
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
    export_button.config(width=get_width(["Export"]))
    export_button.pack(pady=5)

    # Creates error label for bad input
    error_label = ttk.Label(inner_options_frame, text="", style="Error.TLabel")
    error_label.pack(pady=5)

    # Creates exit button to return to T.A.C. screen
    exit_button = ttk.Button(root, text="Back", style="Maize.TButton", padding=(0,0),
                             command=lambda: advanced_back(root, common_el, common_mat,
                                                           element, material, custom_mat,
                                                           selection, mode, interactions,
                                                           mac_num, d_num, lac_num,
                                                           mac_den, d_den, lac_den, energy_unit))
    exit_button.config(width=get_width(["Back"]))
    exit_button.pack(pady=5)

    export_list = [interactions_frame, empty_frame1,
                   options_frame, exit_button]

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
                  selection, mode, interactions, mac_num, d_num, lac_num,
                  mac_den, d_den, lac_den, energy_unit):
    from App.Attenuation.tac_advanced import tac_advanced

    clear_export()
    tac_advanced(root, selection=selection, mode=mode,
                 interactions_start=interactions, common_el=common_el,
                 common_mat=common_mat, element=element, material=material,
                 custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                 lac_num=lac_num, mac_den=mac_den, d_den=d_den,
                 lac_den=lac_den, energy_unit=energy_unit)