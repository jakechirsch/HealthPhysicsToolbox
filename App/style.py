##### IMPORTS #####
import tkinter as tk
from tkinter import ttk, Frame

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
    style.map("Maize.TCombobox",
              background=[('readonly', "#FFCB05"), ('!readonly', "#FFCB05")])
    style.configure("Maize.TCheckbutton",
                    background="#F2F2F2",
                    foreground="#00274C")
    style.map("Maize.TCheckbutton",
              background=[('active', "#F2F2F2")])
    style.configure("White.TLabel",
                    background="#00274C",
                    foreground="white",
                    font=("Verdana", 16))
    style.configure("Black.TLabel",
                    background="#F2F2F2",
                    foreground="black")
    style.configure("Home.TLabel",
                    background="#F2F2F2",
                    foreground="#00274C")
    style.configure("Error.TLabel",
                    background="#F2F2F2",
                    foreground="red")
    style.configure("Success.TLabel",
                    background="#F2F2F2",
                    foreground="black")
    style.configure("Maize.TLabel",
                    background="#00274C",
                    foreground="#FFCB05")

class SectionFrame(tk.Frame):
    def __init__(self, parent, title="", *args, **kwargs):
        # Transparent-style frame (inherits parent's bg)
        bg_color = "#F2F2F2"
        super().__init__(parent, bg=bg_color, *args, **kwargs)

        # Border frame to simulate an outline
        self.border_frame = tk.Frame(self, bg="#00274C")
        self.border_frame.pack(padx=1, pady=10)

        # Inner frame (blends with background)
        self.inner_frame = tk.Frame(self.border_frame, bg=bg_color)
        self.inner_frame.pack(padx=4, pady=(22, 4))

        # Empty frame to set a consistent width for each section
        width_frame = Frame(self.inner_frame, bg="#F2F2F2")
        width_frame.pack(padx=200)

        # Title bar
        self.title_bar = tk.Frame(self.border_frame, bg="#00274C", height=22)
        self.title_bar.place(x=0, y=0, relwidth=1)

        self.title_label = ttk.Label(
            self.title_bar, text=title, style="White.TLabel"
        )
        self.title_label.pack()
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")

    def get_inner_frame(self):
        return self.inner_frame

    def change_title(self, title):
        self.title_label.destroy()
        self.title_label = ttk.Label(
            self.title_bar, text=title, style="White.TLabel"
        )
        self.title_label.pack()
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")