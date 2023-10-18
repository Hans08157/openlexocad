#==================================================================
#
# ITEM DIALOG - User can choose between a list of predefined items
#
#==================================================================

import Base, Gui

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

items = Base.vector_String()
items.append(lxstr("Box"))
items.append(lxstr("Cone"))
items.append(lxstr("Sphere"))

# This is working too:
# items = Geom.vector_String(["Box", "Cone", "Sphere"])

# This shows the dialog...
text = lxstr("Choose an item")
value = Gui.getItemDialog(text, items)

# ...dialog has "Sphere" as default value (index is stating from 0)...
# value = Gui.getItemDialog(text, items, 2)

# ...if "True" is specified the user can enter its own text: otherwise, the user may only select one of the existing items.
# value = Gui.getItemDialog(text, items, 2, True)

# Display the user choice
title = lxstr("Lexocad")
text = lxstr("You have chosen: ") + value.getValue()
ok = Gui.showMessageBox(title, text)