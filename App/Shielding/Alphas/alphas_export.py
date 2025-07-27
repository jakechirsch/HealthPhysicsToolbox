##### IMPORTS #####
from Core.Shielding.Alphas.alphas_plots import *
from App.style import SectionFrame

# For global access to nodes on alpha range export screen
export_list = []

#####################################################################################
# MENU SECTION
#####################################################################################

"""
This function sets up the alpha range export screen.
The following sections and widgets are created:
   Module Title (Alpha Range)
   Export Options section
   Back button
This function contains all of the logic involving these widgets'
behaviors.
The sections and widgets are stored in export_list so they can be
accessed later by clear_export.
"""
def alphas_export(root, category, mode, common_el, common_mat, element,
                  material, custom_mat, csda_num, d_num, csda_den, d_den,
                  energy_unit):
    global export_list

    # Makes title frame
    title_frame = make_title_frame(root, "Alpha Range", "Shielding/Alphas")

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
    mode_choices = ["CSDA Range",
                    "Density"]

    # Stores units in list
    num_units = [csda_num, d_num]
    den_units = [csda_den, d_den]

    # Creates Export button
    export_button = ttk.Button(inner_options_frame, text="Export", style="Maize.TButton",
                               padding=(0,0),
                               command=lambda:
                               export_data(root,
                               get_item(category, common_el, common_mat,
                                        element, material, custom_mat),
                                           category, mode,
                               get_unit(num_units, mode_choices, mode),
                               get_unit(den_units, mode_choices, mode),
                                           energy_unit, export_dropdown.get(),
                                           var_save.get(), error_label))
    export_button.config(width=get_width(["Export"]))
    export_button.pack(pady=(10,5))

    # Creates error label for bad input
    error_label = ttk.Label(inner_options_frame, text="", style="Error.TLabel")
    error_label.pack(pady=(5,10))

    # Creates Back button to return to alpha range advanced screen
    back_button = ttk.Button(root, text="Back", style="Maize.TButton", padding=(0,0),
                             command=lambda: advanced_back(root, category, mode,
                                                           common_el, common_mat, element,
                                                           material, custom_mat, csda_num,
                                                           d_num, csda_den, d_den,
                                                           energy_unit))
    back_button.config(width=get_width(["Back"]))
    back_button.pack(pady=5)

    # Stores nodes into global list
    export_list = [title_frame,
                   options_frame, back_button]

#####################################################################################
# NAVIGATION SECTION
#####################################################################################

"""
This function clears the alpha range export screen
in preparation for opening a different screen.
"""
def clear_export():
    global export_list

    # Clears alpha range export screen
    for node in export_list:
        node.destroy()
    export_list.clear()

"""
This function transitions from the alpha range export screen
to the alpha range advanced screen by first clearing the
alpha range export screen and then creating the
alpha range advanced screen.
It is called when the Back button is hit.
"""
def advanced_back(root, category, mode, common_el, common_mat, element,
                  material, custom_mat, csda_num, d_num, csda_den, d_den,
                  energy_unit):
    from App.Shielding.Alphas.alphas_advanced import alphas_advanced

    clear_export()
    alphas_advanced(root, category, mode, common_el, common_mat, element,
                       material, custom_mat, csda_num, d_num, csda_den, d_den,
                       energy_unit)