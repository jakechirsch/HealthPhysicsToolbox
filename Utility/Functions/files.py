##### IMPORTS #####
import os
import sys
import platform
import subprocess
from pathlib import Path
from tkinter.filedialog import asksaveasfilename
from Utility.Functions.gui_utility import edit_result

#####################################################################################
# OPEN SECTION
#####################################################################################

"""
This function opens a file given the path to the file.
Used for opening References.txt, Help.txt, or exported plot/data.
"""
def open_file(path):
    if platform.system() == 'Windows':
        os.startfile(path)
    elif platform.system() == 'Darwin':  # macOS
        subprocess.run(['open', path])
    else:  # Assume Linux or Unix
        subprocess.run(['xdg-open', path])

"""
This function finds the true path to a file given the relative path.
Used for opening a data file, References.txt, or Help.txt.
This function is necessary due to potential path differences depending
on whether you are running in an IDE/terminal or an executable.
"""
def resource_path(relative_path):
    # Returns absolute path to bundled resource
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

"""
This function finds the true path to user data given the relative path.
Used for opening a shelve db file.
This function is necessary due to potential path differences depending
on whether you are running in an IDE/terminal or an executable.
"""
def get_user_data_path(relative_path):
    # Return a path in a writable location
    if getattr(sys, 'frozen', False):
        # If bundled with PyInstaller, get folder of the executable
        base_dir = Path(sys.executable).parent
    else:
        # If running as script
        base_dir = Path(sys.argv[0]).resolve().parent

    full_path = base_dir / "UserData" / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure subdirectories exist
    return str(full_path)

"""
This function configures matplotlib in advance.
This saves time when trying to load advanced settings while
using the app.
"""
def set_mpl_cache_dir():
    if getattr(sys, 'frozen', False):
        # Use a bundled folder inside the executable's directory
        base_dir = Path(sys.executable).parent
        cache_dir = base_dir / "matplotlib_cache"
    else:
        # When running as script, use normal cache dir
        cache_dir = Path.home() / ".matplotlib"

    # Make sure the directory exists
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Tell matplotlib to use this directory for its config (including font cache)
    os.environ["MPLCONFIGDIR"] = str(cache_dir)

#####################################################################################
# SAVE SECTION
#####################################################################################

"""
This function is called when the exported file is
going to be saved. It prompts the user to select
a file name and location, and handles the error of
the user canceling the export. If the export is not
canceled, the file is saved with the selected name
and location and then opened.
"""
def save_file(obj, choice, error_label, item, name, decay = False):
    file_format = ".csv"
    if choice == "Plot":
        file_format = ".png"

    # Show the "Save As" dialog
    file_path = asksaveasfilename(
        defaultextension=file_format,
        filetypes=[(file_format[1:].upper() + " files", "*" + file_format)],
        title="Save " + file_format[1:].upper() + " As...",
        initialfile=item.lower().replace(" ", "_") + "_" + name + "_" + choice.lower()
    )

    # If the user selected a path, save the file
    if file_path:
        if choice == "Plot":
            obj.savefig(file_path)
        else:
            obj.to_csv(file_path, index=False)
        if decay:
            edit_result("Plot exported!", error_label)
        else:
            error_label.config(style="Success.TLabel", text=choice + " exported!")
        open_file(file_path)
    else:
        if decay:
            edit_result("Export canceled.", error_label)
        else:
            error_label.config(style="Error.TLabel", text="Export canceled.")