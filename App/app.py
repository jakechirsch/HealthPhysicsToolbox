##### IMPORTS #####
from tkinter import ttk
from App.Attenuation.tac_main import total_attenuation_coefficient

# For global access to nodes on home screen
home_list = []

def clear_home():
    global home_list

    # Clears home
    for node in home_list:
        node.destroy()

def return_home(root):
    global home_list

    title = ttk.Label(root, text="Health Physics Toolbox", font=("Verdana", 16),
                      style="White.TLabel")
    title.pack(pady=5)

    # Creates buttons for home screen
    tac_button = ttk.Button(root, text="Attenuation Coefficients",
                            command=lambda: tac(root), style="Maize.TButton",
                            padding=(0,0))
    tac_button.pack(pady=5)
    home_list = [tac_button, title]

def tac(root):
    root.focus()
    clear_home()
    total_attenuation_coefficient(root)