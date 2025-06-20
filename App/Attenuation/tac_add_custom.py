##### IMPORTS #####
from App.Attenuation.tac_choices import *
from Core.Attenuation.tac_calculations import *
from tkinter import ttk

# For global access to nodes on custom screen
custom_list = []

def custom_menu(root, common_el, common_mat, element, material, custom_mat,
                selection, mode, interaction, mac_num, d_num, lac_num, mac_den,
                d_den, lac_den, energy_unit):
    global custom_list

    material_title = ttk.Label(root, text="Material Name", font=("Verdana", 16),
                           style="Maize.TLabel")
    material_title.pack(pady=5)

    material_frame = Frame(root, bg="#00274C")
    material_frame.pack(pady=5)

    entry = make_line(material_frame, "Material Name:")

    # Spacer
    empty_frame1 = make_spacer(root)

    density_title = ttk.Label(root, text="Density", font=("Verdana", 16),
                              style="Maize.TLabel")
    density_title.pack(pady=5)

    density_frame = Frame(root, bg="#00274C")
    density_frame.pack(pady=5)

    entry2 = make_line(density_frame, f"Density ({d_num}/{d_den}):")

    # Spacer
    empty_frame2 = make_spacer(root)

    weights_title = ttk.Label(root, text="Element Weights", font=("Verdana", 16),
                              style="Maize.TLabel")
    weights_title.pack(pady=5)

    weights_frame = Frame(root, bg="#00274C")
    weights_frame.pack(pady=5)

    ex_frame = Frame(weights_frame, bg="#00274C")
    ex_frame.pack(side="left", padx=5)

    label = ttk.Label(ex_frame, text="Element Weights:", style="White.TLabel")
    entry3 = Text(weights_frame, width=20, height=10, bg='white', fg='grey',
                  insertbackground="black", borderwidth=0, bd=0,
                  highlightthickness=0, relief='flat')
    label.pack()
    entry3.pack(side="left", padx=5)

    example_label(ex_frame, "")
    example_label(ex_frame, "Example:")
    example_label(ex_frame, "0.30, Pb")
    example_label(ex_frame, "0.55, Si")
    example_label(ex_frame, "0.13, O")
    example_label(ex_frame, "0.02, K")

    # Spacer
    empty_frame3 = make_spacer(root)

    normalize_title = ttk.Label(root, text="Options", font=("Verdana", 16),
                                style="Maize.TLabel")
    normalize_title.pack(pady=5)

    # Variable to hold normalize option
    var_normalize = IntVar()

    normalize = ttk.Checkbutton(root, text="Normalize", variable=var_normalize,
                                style="Maize.TCheckbutton")
    normalize.pack(pady=5)

    # Spacer
    empty_frame4 = make_spacer(root)

    # Creates button
    button = ttk.Button(root, text="Add Material", style="Maize.TButton", padding=(-10,0),
                        command=lambda: add_custom(root, entry, entry2, entry3,
                                                   error_label, var_normalize.get(),
                                                   d_num, d_den))
    button.pack(pady=5)

    # Creates exit button to return to T.A.C. screen
    exit_button = ttk.Button(root, text="Back", style="Maize.TButton", padding=(-20,0),
                             command=lambda: advanced_back(root, common_el, common_mat,
                                                           element, material, custom_mat,
                                                           selection, mode, interaction,
                                                           mac_num, d_num, lac_num,
                                                           mac_den, d_den, lac_den, energy_unit))
    exit_button.pack(pady=5)

    # Creates error label for bad input
    error_label = ttk.Label(root, text="", style="Error.TLabel")
    error_label.pack(pady=5)

    # Stores nodes into global list
    custom_list = [material_title, material_frame, empty_frame1,
                   density_title, density_frame, empty_frame2,
                   weights_title, weights_frame, empty_frame3,
                   normalize_title, normalize, empty_frame4,
                   button, exit_button, error_label]

def make_line(frame, text):
    label = ttk.Label(frame, text=text, style="White.TLabel")
    entry = ttk.Entry(frame, width=20, style="Maize.TEntry")
    label.pack(side="left", padx=5)
    entry.pack(side="left", padx=5)
    return entry

def add_custom(root, name_box, density_box, weights_box, error_label, normalize,
               d_num, d_den):
    name = name_box.get()

    # Error check for no material name
    if name == "":
        error_label.config(style="Error.TLabel", text="Error: No material name provided.")
        return

    # Error check for lengthy material name
    if len(name) > 50:
        error_label.config(style="Error.TLabel", text="Error: Maximum material name length exceeded.")
        return

    density = density_box.get()

    if density == "":
        error_label.config(style="Error.TLabel", text="Error: No density provided.")
        return

    # Error check for a non-number density input
    try:
        _ = float(density)
    except ValueError:
        error_label.config(style="Error.TLabel", text="Error: Non-number density input.")
        return

    if float(density) <= 0:
        error_label.config(style="Error.TLabel", text="Error: Density must be positive.")
        return

    weights = weights_box.get("1.0", "end-1c")

    cleaned_input = '\n'.join(
        ','.join(field.strip() for field in line.split(','))
        for line in weights.strip().splitlines()
    )

    # Error check for no weights
    if cleaned_input == "":
        error_label.config(style="Error.TLabel", text="Error: No element weights provided.")
        return

    csv_data = '"Weight","Element"\n' + cleaned_input

    # Create file-like object from the stored string
    csv_file_like = io.StringIO(csv_data)

    reader = csv.reader(csv_file_like)
    elements = get_choices("All Elements")
    weights_sum = 0

    for row in reader:
        # Error check for bad rows
        if not (len(row) == 2):
            error_label.config(style="Error.TLabel",
                               text="Error: Each line must have a weight, a comma, and an element.")
            return

        # Error check for a non-number weight input
        try:
            if row[0] != "Weight":
                weights_sum += float(row[0])
        except ValueError:
            error_label.config(style="Error.TLabel", text="Error: Non-number weight input.")
            return

        # Error check for an element weight outside (0, 1]
        if row[0] != "Weight" and (float(row[0]) > 1 or float(row[0]) <= 0):
            error_label.config(style="Error.TLabel", text="Error: Weights must be in range (0, 1].")
            return

        # Error check for an invalid element
        if row[1] != "Element" and not row[1] in elements:
            error_label.config(style="Error.TLabel", text="Error: Invalid element: " + row[1] + ".")
            return

    # Error check for weights that do not sum to 1
    if weights_sum != 1:
        if normalize == 0:
            error_label.config(style="Error.TLabel",
                               text="Error: Element weights do not sum to 1; select normalize to fix.")
            return
        else:
            csv_data2 = ""

            # Create file-like object from the stored string
            csv_file_like2 = io.StringIO(csv_data)

            reader2 = csv.reader(csv_file_like2)
            for row in reader2:
                row[0] = row[0].strip()
                if row[0] != "Weight":
                    row[0] = str(float(row[0]) / weights_sum)
                csv_data2 += row[0].strip() + ","
                csv_data2 += row[1].strip() + "\n"
            csv_data = csv_data2.rstrip("\n")

    error_label.config(style="Success.TLabel", text="Material added!")

    with shelve.open("Data/Modules/Mass Attenuation/User/Custom Materials") as prefs:
        choices = prefs.get("Custom Materials", [])
        if not name in choices:
            choices.append(name)
        prefs["Custom Materials"] = choices

    # Save to shelve
    with shelve.open('Data/Modules/Mass Attenuation/User/_' + name) as db:
        db[name] = csv_data
        db[name + '_Density'] = str(float(density) * density_denominator[d_den] / density_numerator[d_num])

    name_box.delete(0, END)
    weights_box.delete("1.0", "end")
    density_box.delete(0, END)
    root.focus()

def example_label(frame, text):
    label = ttk.Label(frame, text=text, style="White.TLabel")
    label.pack()

def clear_custom():
    global custom_list

    # Clears custom screen
    for node in custom_list:
        node.destroy()
    custom_list.clear()

def advanced_back(root, common_el, common_mat, element, material, custom_mat,
                  selection, mode, interaction, mac_num, d_num, lac_num,
                  mac_den, d_den, lac_den, energy_unit):
    from App.Attenuation.tac_advanced import tac_advanced

    clear_custom()
    tac_advanced(root, selection=selection, mode=mode,
                 interaction_start=interaction, common_el=common_el,
                 common_mat=common_mat, element=element, material=material,
                 custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                 lac_num=lac_num, mac_den=mac_den, d_den=d_den,
                 lac_den=lac_den, energy_unit=energy_unit)