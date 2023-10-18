#===============================================================================
#
# DISCLAIMER
#
# Some methods used in this script are not part of the official API and may be
# not available in the future (i.e. creating objects by type name and accessing
# properties by name).
#  
#===============================================================================

import math
import App, Base, Geom

# Our Parameters
myText = "<TEXT GOES HERE>"
myColor = Base.Color(0, 255, 0)
myCoord = Geom.Pnt(5,0,5)
myWidth = 10

# Get the active document
doc = App.castToDocument(App.GetApplication().getActiveDocument())

# Create a new "Material" and assign our color to it
mat = App.createMaterial(doc)
mat.diffuseColor.setValue(myColor)

# Create a new "Text Style" and assign the above material to it
ts = App.createTextStyle(doc)
r = ts.setProperty("textMaterial", mat)

# Create a new "Text 2d" and assign
txt = App.castToGeometry(doc.createObjectFromTypeName("Mesh::SingleLineText3d"))
r = txt.setProperty("textString",myText)
r = txt.setProperty("textStyle",ts)
r = txt.setProperty("width",myWidth)
ele = App.createElement(doc)
ele.setGeometry(txt)

# Move the text
ele.placement.translate(Geom.Vec(myCoord.xyz()), Base.CoordSpace_WCS)

doc.recompute()