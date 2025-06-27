##### IMPORTS #####
import tkinter as tk
from tkinter import ttk
from App.app import return_home
from App.style import configure_style

##### WINDOW SETUP #####
root = tk.Tk()
root.title("Health Physics Toolbox")
root.geometry("625x725")
root.configure(bg="#D3D3D3")

# Configures style of app
configure_style()

# Wraps whole app in a container for vertical alignment
container = tk.Frame(root, bg="#D3D3D3")
container.pack(fill="both", expand=True)

# Creates canvas
left_frame = tk.Canvas(container, bg="#D3D3D3", highlightthickness=0, bd=0)
left_frame.pack(side="left", fill="both", expand=True)
right_frame = tk.Frame(container, bg="#D3D3D3", highlightthickness=0, bd=0)
right_frame.pack(side="right", fill="y")
canvas = tk.Canvas(left_frame, bg="#D3D3D3", highlightthickness=0, bd=0)
canvas.pack(side="top", fill="both", expand=True)

# Creates scrollbars
scrollbar_y = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
scrollbar_y.pack(side="top", fill="y")
scrollbar_y_visible = True
scrollbar_x = ttk.Scrollbar(left_frame, orient="horizontal", command=canvas.xview)
scrollbar_x.pack(side="bottom", fill="x")
scrollbar_x_visible = True
canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

# Creates a frame inside the canvas
scrollable_frame = tk.Frame(canvas, bg="#D3D3D3")
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# --- Logic to show/hide scrollbar ---
def update_scroll_visibility(event):
    global scrollbar_y_visible, scrollbar_x_visible
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.update_idletasks()
    needs_scrollbar_y = scrollable_frame.winfo_reqheight() > canvas.winfo_height()
    needs_scrollbar_x = scrollable_frame.winfo_reqwidth() > canvas.winfo_width()

    if not needs_scrollbar_x:
        canvas.itemconfig(canvas_window, width=event.width if event else canvas.winfo_width())

    if needs_scrollbar_y and not scrollbar_y_visible:
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_y_visible = True
    elif not needs_scrollbar_y and scrollbar_y_visible:
        scrollbar_y.pack_forget()
        scrollbar_y_visible = False

    if needs_scrollbar_x and not scrollbar_x_visible:
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_x_visible = True
    elif not needs_scrollbar_x and scrollbar_x_visible:
        scrollbar_x.pack_forget()
        scrollbar_x_visible = False

# Bind size changes
scrollable_frame.bind("<Configure>", update_scroll_visibility)
canvas.bind("<Configure>", update_scroll_visibility)

# Makes Canvas scrollable with mouse/pad
def _on_mousewheel(event):
    if scrollbar_y_visible:
        canvas.yview_scroll(-1 * int(event.delta), "units")
    if scrollbar_x_visible:
        canvas.xview_scroll(-1 * int(event.delta), "units")

canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

# Makes Canvas scrollable with up/down keys
def on_up(_):
    if scrollbar_y_visible:
        canvas.yview_scroll(-1, "units")

def on_down(_):
    if scrollbar_y_visible:
        canvas.yview_scroll(1, "units")

def on_left(_):
    if scrollbar_x_visible:
        canvas.xview_scroll(-1, "units")

def on_right(_):
    if scrollbar_x_visible:
        canvas.xview_scroll(1, "units")

root.bind_all("<KeyPress-Up>", on_up)
root.bind_all("<KeyPress-Down>", on_down)
root.bind_all("<KeyPress-Left>", on_left)
root.bind_all("<KeyPress-Right>", on_right)

# Creates home screen upon launch
return_home(scrollable_frame)
update_scroll_visibility(None)

# Runs app
root.mainloop()