##### IMPORTS #####
import shelve
from Utility.Functions.gui_utility import *
from Utility.Functions.files import *

"""
This function is called when the Add/Remove button is hit and
passes on the work to the individualized functions depending
on the action.
"""
def carry_action(root, action, category, choices, inverse, var, dropdown, module):
    root.focus()
    if action == "Add":
        add_c(category, choices, inverse, var, dropdown, module)
    elif action == "Remove":
        remove_c(category, choices, inverse, var, dropdown, module)

"""
This function adds a common element or common material
to the user's saved data, assuming an item is selected.
The item is appended to the common list and the user data is updated.
The item is then removed from the non_common list.
Finally, the non_common dropdown is updated accordingly.
"""
def add_c(category, non_common, common, var, dropdown, module):
    db_path = get_user_data_path(module + '/' + category)
    with shelve.open(db_path) as prefs:
        # Adds item to common
        item = var.get()
        if item == "":
            return
        common.append(item)
        common.sort()
        prefs[category] = common

        # Removes item from non-common
        non_common.remove(item)

        # Update non_common dropdown
        dropdown.config(values=non_common, width=get_width(non_common))
        var.set(valid_saved("", non_common))

"""
This function removes a common element or common material
to the user's saved data, assuming an item is selected.
The item is removed from the common list and the user data is updated.
The common dropdown is then updated accordingly.
Finally, the item is appended to the non_common list.
"""
def remove_c(category, common, non_common, var, dropdown, module):
    db_path = get_user_data_path(module + '/' + category)
    with shelve.open(db_path) as prefs:
        # Removes item from common
        item = var.get()
        if item == "":
            return
        common.remove(item)
        prefs[category] = common

        # Update common dropdown
        dropdown.config(values=common, width=get_width(common))
        var.set(valid_saved("", common))

        # Adds item to non-common
        non_common.append(item)
        non_common.sort()