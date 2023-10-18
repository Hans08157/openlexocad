#==================================================
#
# INTEGER DIALOG - User can enter an integer number
#
#==================================================

import Base
import OpenLxUI as ui

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

# This shows the dialog...
text = lxstr("Enter a number")
value = ui.getIntDialog(text)

# ...dialog has a default number in it...
# value = ui.getIntDialog(text, 1)

# ...dialog has a "step" value (the amount by which the values change as the user presses the arrow buttons to increment or decrement the value)
# value = ui.getIntDialog(text, 1, 2)

# ...dialog has a minimum and maximum value.
# value = ui.getIntDialog(text, 1, 2, -10, 10)

# Display the user input
title = lxstr("Lexocad")
text = Blxstr("You have entered: " + str( value.getValue() ))
ok = ui.showMessageBox(title, text)