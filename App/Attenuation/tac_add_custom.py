##### IMPORTS #####
from App.Attenuation.tac_choices import *
from Core.Attenuation.tac_calculations import *
from tkinter import ttk, font
from App.style import SectionFrame

# For global access to nodes on custom screen
custom_list = []

def custom_menu(root, common_el, common_mat, element, material, custom_mat,
                selection, mode, interactions, mac_num, d_num, lac_num, mac_den,
                d_den, lac_den, energy_unit):
    global custom_list

    title_frame = make_title_frame(root, "Photon Attenuation")

    monospace_font = font.Font(family="Menlo", size=12)

    material_frame = SectionFrame(root, title="Enter Material Name")
    material_frame.pack()
    inner_material_frame = material_frame.get_inner_frame()

    entry = make_line(inner_material_frame, "Material Name:", 12)

    # Spacer
    empty_frame1 = make_spacer(root)

    density_frame = SectionFrame(root, title="Enter Density")
    density_frame.pack()
    inner_density_frame = density_frame.get_inner_frame()

    entry2 = make_line(inner_density_frame, f"Density ({d_num}/{d_den}):", 9)

    # Spacer
    empty_frame2 = make_spacer(root)

    weights_frame = SectionFrame(root, title="Enter Element Weights")
    weights_frame.pack()
    inner_weights_frame = weights_frame.get_inner_frame()

    ex_frame = Frame(inner_weights_frame, bg="#F2F2F2")
    ex_frame.pack(side="left", padx=33)

    label = ttk.Label(ex_frame, text="Element Weights:", style="Black.TLabel")
    entry3 = Text(inner_weights_frame, width=20, height=10, bg='white', fg='black',
                  insertbackground="black", borderwidth=3, bd=3,
                  highlightthickness=0, relief='solid', font=monospace_font)
    label.pack()
    entry3.pack(side="left", padx=33, pady=10)

    example_label(ex_frame, "")
    example_label(ex_frame, "Example:")
    example_label(ex_frame, "0.30, Pb")
    example_label(ex_frame, "0.55, Si")
    example_label(ex_frame, "0.13, O")
    example_label(ex_frame, "0.02, K")

    # Spacer
    empty_frame3 = make_spacer(root)

    def norm():
        root.focus()

    options_frame = SectionFrame(root, title="Custom Materials Options")
    options_frame.pack()
    inner_options_frame = options_frame.get_inner_frame()

    # Variable to hold normalize option
    var_normalize = IntVar()

    normalize = ttk.Checkbutton(inner_options_frame, text="Normalize", variable=var_normalize,
                                style="Maize.TCheckbutton", command=norm)
    normalize.pack(pady=(10,5))

    # Creates button
    button = ttk.Button(inner_options_frame, text="Add Material", style="Maize.TButton",
                        padding=(0,0),
                        command=lambda: add_custom(root, entry, entry2, entry3,
                                                   error_label, var_normalize.get(),
                                                   d_num, d_den))
    button.config(width=get_width(["Add Material"]))
    button.pack(pady=5)

    # Creates error label for bad input
    error_label = ttk.Label(inner_options_frame, text="", style="Error.TLabel")
    error_label.pack(pady=(5,10))

    # Creates exit button to return to T.A.C. screen
    exit_button = ttk.Button(root, text="Back", style="Maize.TButton", padding=(0,0),
                             command=lambda: advanced_back(root, common_el, common_mat,
                                                           element, material, custom_mat,
                                                           selection, mode, interactions,
                                                           mac_num, d_num, lac_num,
                                                           mac_den, d_den, lac_den, energy_unit))
    exit_button.config(width=get_width(["Back"]))
    exit_button.pack(pady=5)

    # Stores nodes into global list
    custom_list = [title_frame,
                   material_frame, empty_frame1,
                   density_frame, empty_frame2,
                   weights_frame, empty_frame3,
                   options_frame, exit_button]

def make_line(frame, text, pad):
    monospace_font = font.Font(family="Menlo", size=12)
    label = ttk.Label(frame, text=text, style="Black.TLabel")
    entry = Entry(frame, width=32, insertbackground="black",
                  background="white", foreground="black",
                  borderwidth=3, bd=3, highlightthickness=0, relief='solid',
                  font=monospace_font)
    label.pack(side="left", padx=(20, pad))
    entry.pack(side="left", padx=(pad, 2), pady=20)
    return entry

def add_custom(root, name_box, density_box, weights_box, error_label, normalize,
               d_num, d_den):
    root.focus()
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

    db_path = get_user_data_path('Mass Attenuation/Custom Materials')
    with shelve.open(db_path) as prefs:
        choices = prefs.get("Custom Materials", [])
        if not name in choices:
            choices.append(name)
        prefs["Custom Materials"] = choices

    # Save to shelve
    db_path2 = get_user_data_path('Mass Attenuation/_' + name)
    with shelve.open(db_path2) as db:
        db[name] = csv_data
        db[name + '_Density'] = str(float(density) * density_denominator[d_den] / density_numerator[d_num])

    name_box.delete(0, END)
    weights_box.delete("1.0", "end")
    density_box.delete(0, END)

def example_label(frame, text):
    label = ttk.Label(frame, text=text, style="Black.TLabel")
    label.pack()

def clear_custom():
    global custom_list

    # Clears custom screen
    for node in custom_list:
        node.destroy()
    custom_list.clear()

def advanced_back(root, common_el, common_mat, element, material, custom_mat,
                  selection, mode, interactions, mac_num, d_num, lac_num,
                  mac_den, d_den, lac_den, energy_unit):
    from App.Attenuation.tac_advanced import tac_advanced

    clear_custom()
    tac_advanced(root, selection=selection, mode=mode,
                 interactions_start=interactions, common_el=common_el,
                 common_mat=common_mat, element=element, material=material,
                 custom_mat=custom_mat, mac_num=mac_num, d_num=d_num,
                 lac_num=lac_num, mac_den=mac_den, d_den=d_den,
                 lac_den=lac_den, energy_unit=energy_unit)