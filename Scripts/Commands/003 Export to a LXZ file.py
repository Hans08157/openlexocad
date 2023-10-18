#==============================================================================
#
# EXPORT FILE - The simplest way to save some element to a file is by using the
# function "Export visible elements". In this example we:
# - hide all elements that do not need to be exported
# - invoke the command to save the "visible elements"
#
#==============================================================================

import Base, Geom
import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()
lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

# Do something with the scene (e.g. create some objects or import them from a file)

sphere = lx.Sphere.createIn(doc)
sphere.setRadius(5)
element1 = lx.Element.createIn(doc)
element1.setGeometry(sphere)

cylinder = lx.RightCircularCylinder.createIn(doc)
cylinder.setHeight(5)
cylinder.setRadius(2.5)
element2 = lx.Element.createIn(doc)
element2.setGeometry(cylinder)
# ---------------------------------------------------------------------------------

# Hide the unwanted element(s)
element2.setVisible(False) #print "Id:" + element.getId() + " - Name:" + name

# Export the visible elements
lCmd = cmd.CmdExportLXZFile(True)
lCmd.redo()

# Use "cmd.CmdExportCAZFile(True)" to have Lexocad asking for a file