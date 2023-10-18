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
myColor = Base.Color(255, 0, 0)
myAngle = math.radians(90)
myCoord = Geom.Pnt(10,0,10)

# Get the active document
doc = App.castToDocument(App.GetApplication().getActiveDocument())

# Create a new "Material" and assign our color to it
mat = App.createMaterial(doc)
mat.diffuseColor.setValue(myColor)

# Create a new "Text Style" and assign the above material to it
ts = App.createTextStyle(doc)
r = ts.setProperty("textMaterial", mat)

# Create a new "Text 2d" and assign
txt = App.castToGeometry(doc.createObjectFromTypeName("Mesh::SingleLineText2d"))
r = txt.setProperty("textString",myText)
r = txt.setProperty("textStyle",ts)
ele = App.createElement(doc)
ele.setGeometry(txt)

# Move/Rotate the text
ele.placement.rotate(Geom.Ax1(Geom.Pnt(0,0,0), Geom.Dir(1, 0, 0)), myAngle, Base.CoordSpace_WCS)
ele.placement.translate(Geom.Vec(myCoord.xyz()), Base.CoordSpace_WCS)

doc.recompute()