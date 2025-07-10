##### IMPORTS #####
from Core.Attenuation.Photons.photons_plots import *
from App.Attenuation.Photons.photons_unit_settings import *
from App.style import SectionFrame

# For global access to nodes on photon attenuation export screen
export_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

def photons_export(root, common_el, common_mat, element, material, custom_mat,
                   selection, mode, interactions, mac_num, d_num, lac_num,
                   mac_den, d_den, lac_den, energy_unit):
    global export_list

    title_frame = make_title_frame(root, "Photon Attenuation")

    # Frame for interactions
    interactions_frame = SectionFrame(root, title="Select Interaction Types")
    interactions_frame.pack()
    inner_interactions_frame = interactions_frame.get_inner_frame()
    inner_interactions_frame.config(pady=10)

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

    # Checkbox for saving file
    var_save = IntVar()
    var_save.set(1)

    # Frame for options
    options_frame = SectionFrame(root, title="Export Options")
    options_frame.pack()
    inner_options_frame = options_frame.get_inner_frame()

    save = ttk.Checkbutton(inner_options_frame, text="Save File", variable=var_save,
                           style="Maize.TCheckbutton", command=lambda: root.focus())
    save.pack(pady=(10,5))

    export_type_frame = Frame(inner_options_frame, bg="#F2F2F2")
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

    export_label = ttk.Label(export_type_frame, text="Export Type:", style="Black.TLabel")
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
                               export_data(root,
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
    export_button.pack(pady=(10,5))

    # Creates error label for bad input
    error_label = ttk.Label(inner_options_frame, text="", style="Error.TLabel")
    error_label.pack(pady=(5,10))

    # Creates exit button to return to photon attenuation advanced screen
    exit_button = ttk.Button(root, text="Back", style="Maize.TButton", padding=(0,0),
                             command=lambda: advanced_back(root, common_el, common_mat,
                                                           element, material, custom_mat,
                                                           selection, mode, interactions,
                                                           mac_num, d_num, lac_num,
                                                           mac_den, d_den, lac_den,
                                                           energy_unit))
    exit_button.config(width=get_width(["Back"]))
    exit_button.pack(pady=5)

    export_list = [title_frame,
                   interactions_frame, empty_frame1,
                   options_frame, exit_button]

#####################################################################################
# HELPER SECTION
#####################################################################################

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

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the photon attenuation export screen
in preparation for opening a different screen.
"""
def clear_export():
    global export_list

    # Clears photon attenuation export screen
    for node in export_list:
        node.destroy()
    export_list.clear()

"""
This function transitions from the photon attenuation export screen
to the photon attenuation advanced screen by first clearing the
photon attenuation export screen and then creating the
photon attenuation advanced screen.
It is called when the Back button is hit.
"""
def advanced_back(root, common_el, common_mat, element, material, custom_mat,
                  selection, mode, interactions, mac_num, d_num, lac_num,
                  mac_den, d_den, lac_den, energy_unit):
    from App.Attenuation.Photons.photons_advanced import photons_advanced

    clear_export()
    photons_advanced(root, selection=selection, mode=mode,
                     interactions_start=interactions, common_el=common_el,
                     common_mat=common_mat, element=element, material=material,
                     custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                     lac_num=lac_num, mac_den=mac_den, d_den=d_den,
                     lac_den=lac_den, energy_unit=energy_unit)