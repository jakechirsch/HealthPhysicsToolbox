##### IMPORTS #####
from tkinter import ttk

def configure_style():
    # Configure the style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Maize.TButton",
                    background="#FFCB05",
                    foreground="black")
    style.configure("Maize.TCombobox",
                    background="#FFCB05",
                    foreground="black")
    style.configure("Maize.TCheckbutton",
                    background="#00274C",
                    foreground="#FFCB05")
    style.map("Maize.TCheckbutton",
              background=[('active', "#00274C")])
    style.configure("White.TLabel",
                    background="#00274C",
                    foreground="white")
    style.configure("Maize.TEntry",
                    fieldbackground="black",
                    foreground="white",
                    bordercolor="#00274C")
    style.configure("Error.TLabel",
                    background="#00274C",
                    foreground="red")
    style.configure("Success.TLabel",
                    background="#00274C",
                    foreground="black")
    style.configure("Maize.TLabel",
                    background="#00274C",
                    foreground="#FFCB05")