#===============================================================================
#
# COMMANDS are functionalities of Lexocad that are connected to buttons, menu
# entries, keyboard shortcuts and so on.
#
# In Python they are triggered by calling doc.runCommand(cmd). These commands
# are added to the undo/redo stack.
# If you don't want to put the command on the undo/redo stack it is possible
# to call the command directly by calling cmd.redo().
# 
#
# Using a command without parameters will usually show its corresponding dialog.
#
#===============================================================================


import Base, Geom
import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

c = lx.RightCircularCylinder.createIn(doc)
c.setRadius(2.5)
c.setHeight(5)
elem = lx.Element.createIn(doc)
elem.setGeometry(c)
doc.recompute()

xLines = 8; yLines = 8

#=== CODE RELATED TO COMMANDS ===#

cmd = cmd.CmdAddIsoParamLines(elem, xLines, yLines)
# cmd = cmd.CmdAddIsoParamLines() # Using the default constructor opens up a dialog to manually enter the values.
doc.runCommand(cmd)

lines = cmd.getIsoParamLineElements()
for l in lines:
    l.setDiffuseColor(Base.Color(255, 0, 0))

#================================#

doc.removeObject(elem)
doc.recompute()