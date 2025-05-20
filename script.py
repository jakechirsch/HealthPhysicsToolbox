import csv
import os
import tkinter as tk

root = tk.Tk()
root.title("Coefficient Request")
root.geometry("300x200")

tac_button = tk.Button(root)
tac_screen = []
screen = ""

def total_attenuation_coefficient():
    global tac_button
    global screen
    global tac_screen
    x: list[str] = [s[0:2] for s in os.listdir(os.getcwd()+'/attenuation') if s[2:] == '.csv']
    x.sort()

    tac_button.pack_forget()
    screen = "tac"

    var = tk.StringVar(root)
    var.set('Ac')
    
    dropdown = tk.OptionMenu(root, var, *x)
    dropdown.pack(pady=10)

    label = tk.Label(root, text="Energy:")
    label.pack()

    entry = tk.Entry(root, width=30)
    entry.config(bg='white', fg='grey')
    entry.pack()

    calc = tk.Button(root, text="Calculate",
                       command=lambda: find_tac(var.get(), entry.get()))
    calc.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=clear)
    exit_button.pack(pady=5)

    tac_screen = [dropdown, label, entry, calc, exit_button]

def find_tac(element, energy_str):
    global result_label
    result_label.pack_forget()
    try:
        energy_target = float(energy_str)
    except ValueError:
        result_label = tk.Label(root, text="Error: Non-number energy input.")
        result_label.pack(pady=5)
        return
    closest_low = 0.0
    closest_high = float('inf')
    low_coefficient = 0.0
    high_coefficient = float('inf')
    with open('attenuation/' + element + '.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            energy = float(row["Photon Energy"])
            if energy == energy_target:
                result_label = tk.Label(root,
                               text=row["Total Attenuation with Coherent Scattering"])
                result_label.pack(pady=5)
                return
            elif energy_target > energy:
                closest_low = energy
                low_coefficient = float(row["Total Attenuation with Coherent Scattering"])
            else:
                closest_high = energy
                high_coefficient = float(row["Total Attenuation with Coherent Scattering"])
                break
    if closest_low == 0.0:
        result_label = tk.Label(root, text="Error: Energy too low.")
        result_label.pack(pady=5)
        return
    if closest_high == float('inf'):
        result_label = tk.Label(root, text="Error: Energy too high.")
        result_label.pack(pady=5)
        return
    difference = closest_high - closest_low
    percentage = (energy_target - closest_low) / difference
    coefficient = low_coefficient + percentage * (high_coefficient - low_coefficient)
    result_label = tk.Label(root, text=str(coefficient))
    result_label.pack(pady=5)

def clear():
    global tac_screen
    global screen
    if screen == "tac":
        for node in tac_screen:
            node.destroy()
    return_home()
    screen = ""
    result_label.pack_forget()

def return_home():
    global tac_button
    tac_button = tk.Button(root, text="Total Attenuation Coefficient", command=total_attenuation_coefficient)
    tac_button.pack(pady=5)

return_home()

result_label = tk.Label(root, text="")

root.mainloop()