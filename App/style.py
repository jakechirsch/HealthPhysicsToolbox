##### IMPORTS #####
import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk, Frame
from Utility.Functions.gui_utility import get_max_string_pixel_width
from App.Attenuation.Photons.photons_choices import get_choices

#####################################################################################
# COLORS SECTION
#####################################################################################

"""
This function configures all of the colors and fonts
for the app's widgets.
"""
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
              fieldbackground=[('readonly', "white"), ('!readonly', "white")])
    style.map("Maize.TCombobox",
              background=[('readonly', "#FFCB05"), ('!readonly', "#FFCB05")])
    style.map("Maize.TCombobox",
              foreground=[('readonly', "black"), ('!readonly', "black")])
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
                    foreground="#00274C",
                    font=("Verdana", 16))
    style.configure("Error.TLabel",
                    background="#F2F2F2",
                    foreground="red")
    style.configure("Success.TLabel",
                    background="#F2F2F2",
                    foreground="black")
    style.configure("Blue.TLabel",
                    background="#F2F2F2",
                    foreground="#00274C",
                    font=("Verdana", 20, "bold"))

#####################################################################################
# SECTION BORDERS SECTION
#####################################################################################

"""
This class represents a full section with a border, title bar, title,
and inside frame for the section's contents.
"""
class SectionFrame(tk.Frame):
    def __init__(self, parent, title="", *args, **kwargs):
        # Transparent-style frame (inherits parent's bg)
        bg_color = "#F2F2F2"
        super().__init__(parent, bg=bg_color, *args, **kwargs)

        # Border frame to simulate an outline
        self.border_frame = tk.Frame(self, bg="#00274C")
        self.border_frame.pack(padx=1, pady=10)

        # Sets the height of the title bar
        font = tk_font.Font(family="Verdana", size=16)
        font_height = font.metrics("linespace")
        title_height = max(24, font_height + 5)

        # Inner frame (blends with background)
        self.inner_frame = tk.Frame(self.border_frame, bg=bg_color)
        self.inner_frame.pack(padx=4, pady=(title_height, 4))

        # Empty frame to set a consistent width for each section
        custom = get_choices("Custom Materials")
        mats = get_choices("All Materials")
        custom_width = (get_max_string_pixel_width(custom,
                        tk_font.nametofont("TkDefaultFont")) // 2 + 20) * 2
        mats_width = (get_max_string_pixel_width(mats,
                      tk_font.nametofont("TkDefaultFont")) // 2 + 20) * 2
        width = max(400, custom_width, mats_width)

        dpi = parent.winfo_fpixels('1i') / 72
        adjusted_width = int(width * dpi)

        width_frame = Frame(self.inner_frame, bg="#F2F2F2", width=adjusted_width)
        width_frame.pack()
        width_frame.pack_propagate(False)

        # Title bar
        self.title_bar = tk.Frame(self.border_frame, bg="#00274C", height=title_height)
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

#####################################################################################
# TOOLTIP SECTION
#####################################################################################

"""
This class represents a tooltip for more information on
a particular module.
"""
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, _):
        if self.tooltip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(
            tw, text=self.text, justify='left', style="Blue.TLabel",
            relief='solid', borderwidth=1,
            font=("Verdana", 12, "normal")
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, _):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None