##### IMPORTS #####
from Core.Shielding.Photons.photons_plots import *
from App.style import SectionFrame

# For global access to nodes on photon attenuation export screen
export_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the photon attenuation export screen.
The following sections and widgets are created:
   Module Title (Photon Attenuation)
   Select Interaction Types section
   Export Options section
   Back button
This function contains all of the logic involving these widgets'
behaviors.
The sections and widgets are stored in export_list so they can be
accessed later by clear_export.
"""
def photons_export(root, category, mode, interactions, common_el, common_mat,
                   element, material, custom_mat, mac_num, d_num, lac_num,
                   mac_den, d_den, lac_den, energy_unit):
    global export_list

    # Makes title frame
    title_frame = make_title_frame(root, "Photon Attenuation")

    # Frame for interactions
    interactions_frame = SectionFrame(root, title="Select Interaction Types")
    interactions_frame.pack()
    inner_interactions_frame = interactions_frame.get_inner_frame()
    inner_interactions_frame.config(pady=10)

    # Logic for when an interaction type is selected
    on_select = lambda: root.focus()

    # List of interactions
    interaction_choices = ["Total Attenuation with Coherent Scattering",
                           "Total Attenuation without Coherent Scattering",
                           "Pair Production in Electron Field",
                           "Pair Production in Nuclear Field",
                           "Scattering - Incoherent",
                           "Scattering - Coherent",
                           "Photo-Electric Absorption"]

    # Variables for each interaction type
    var0 = IntVar()
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    interaction_vars = [var0, var1, var2, var3, var4, var5, var6]

    checks = Frame(inner_interactions_frame, bg="#F2F2F2")
    checks.pack()

    # Checkboxes for each interaction type
    interaction_checkbox(checks, var0,
                         "Total Attenuation with Coherent Scattering", on_select)
    interaction_checkbox(checks, var1,
                         "Total Attenuation without Coherent Scattering", on_select)
    interaction_checkbox(checks, var2,
                         "Pair Production in Electron Field", on_select)
    interaction_checkbox(checks, var3,
                         "Pair Production in Nuclear Field", on_select)
    interaction_checkbox(checks, var4,
                         "Scattering - Incoherent", on_select)
    interaction_checkbox(checks, var5,
                         "Scattering - Coherent", on_select)
    interaction_checkbox(checks, var6,
                         "Photo-Electric Absorption", on_select)

    # Spacer
    empty_frame1 = make_spacer(root)

    # Stores whether file is saved and sets default
    var_save = IntVar()
    var_save.set(1)

    # Frame for options
    options_frame = SectionFrame(root, title="Export Options")
    options_frame.pack()
    inner_options_frame = options_frame.get_inner_frame()

    # Creates checkbox for saving file
    save = ttk.Checkbutton(inner_options_frame, text="Save File", variable=var_save,
                           style="Maize.TCheckbutton", command=lambda: root.focus())
    save.pack(pady=(10,5))

    # Frame for export type
    export_type_frame = Frame(inner_options_frame, bg="#F2F2F2")
    export_type_frame.pack(pady=5)

    # Export label
    basic_label(export_type_frame, "Export Type:")

    # Logic for when an export type is selected
    def on_select_export(event):
        nonlocal var_save
        event.widget.selection_clear()
        root.focus()
        if event.widget.get() == "Data":
            # Forces user to save file if export type is Data
            var_save.set(1)
            save.config(state="disabled")
        else:
            save.config(state="normal")

    # Creates dropdown menu for export type
    export_choices = ["Plot", "Data"]
    export_dropdown = ttk.Combobox(export_type_frame, values=export_choices,
                                   justify="center", state='readonly',
                                   style="Maize.TCombobox")
    export_dropdown.config(width=get_width(export_choices))
    export_dropdown.set("Plot")
    export_dropdown.pack()
    export_dropdown.bind("<<ComboboxSelected>>", on_select_export)

    # Mode choices
    mode_choices = ["Mass Attenuation Coefficient",
                    "Density",
                    "Linear Attenuation Coefficient"]

    # Stores units in list
    num_units = [mac_num, d_num, lac_num]
    den_units = [mac_den, d_den, lac_den]

    # Creates Export button
    export_button = ttk.Button(inner_options_frame, text="Export", style="Maize.TButton",
                               padding=(0,0),
                               command=lambda:
                               export_data(root,
                               get_item(category, common_el, common_mat,
                                        element, material, custom_mat),
                                           category, mode,
                               get_interactions(interaction_choices, interaction_vars),
                               get_unit(num_units, mode_choices, mode),
                               get_unit(den_units, mode_choices, mode),
                                           energy_unit, export_dropdown.get(),
                                           var_save.get(), error_label))
    export_button.config(width=get_width(["Export"]))
    export_button.pack(pady=(10,5))

    # Creates error label for bad input
    error_label = ttk.Label(inner_options_frame, text="", style="Error.TLabel")
    error_label.pack(pady=(5,10))

    # Creates Back button to return to photon attenuation advanced screen
    back_button = ttk.Button(root, text="Back", style="Maize.TButton", padding=(0,0),
                             command=lambda: advanced_back(root, category, mode,
                                                           interactions, common_el,
                                                           common_mat, element,
                                                           material, custom_mat,
                                                           mac_num, d_num, lac_num,
                                                           mac_den, d_den, lac_den,
                                                           energy_unit))
    back_button.config(width=get_width(["Back"]))
    back_button.pack(pady=5)

    # Stores nodes into global list
    export_list = [title_frame,
                   interactions_frame, empty_frame1,
                   options_frame, back_button]

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
def advanced_back(root, category, mode, interactions, common_el, common_mat,
                  element, material, custom_mat, mac_num, d_num, lac_num,
                  mac_den, d_den, lac_den, energy_unit):
    from App.Shielding.Photons.photons_advanced import photons_advanced

    clear_export()
    photons_advanced(root, category, mode, interactions, common_el, common_mat,
                     element, material, custom_mat, mac_num, d_num, lac_num,
                     mac_den, d_den, lac_den, energy_unit)