#==========================================
#
# TEXT DIALOG - User can enter a text value
#
#==========================================

import Base
import OpenLxUI as ui

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

# This shows the dialog...
text = lxstr("Enter a text")
value = ui.getTextDialog(text)

# ...dialog has a default text in it...
# default = lxstr("12345678")
# value = ui.getTextDialog(text, default)

# ...input text is hidden (password-style)
# default = lxstr("12345678")
# value = ui.getTextDialog(text, default, 2)

# Display the user input
title = lxstr("Lexocad")
text = lxstr("You have entered: " ) + value.getValue()
ok = ui.showMessageBox(title, text)