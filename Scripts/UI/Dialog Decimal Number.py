#==================================================
#
# DOUBLE DIALOG - User can enter an decimal number
#
#==================================================

import Base
import OpenLxUI as ui

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString


# This shows the dialog...
text = lxstr("Enter a number")
value = ui.getDoubleDialog(text)

# ...dialog has a default number in it...
# value = ui.getDoubleDialog(text, 1)

# ...dialog has numbers with 3 decimals
# value = ui.getDoubleDialog(text, 1, 3)

# ...dialog has a minimum and maximum value.
# value = ui.getDoubleDialog(text, 1, 3, -10, 10)

# Display the user input
title = lxstr("Lexocad")
text = lxstr("You have entered: " + str( value.getValue() ))
ok = ui.showMessageBox(title, text)