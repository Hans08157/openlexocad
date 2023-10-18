#===============================================================================
#
# COPYING AND GROUPING ELEMENTS
#
#===============================================================================

import App, Base, Geom, Part
import math

doc = App.castToDocument(App.GetApplication().getActiveDocument())

#-----------------------------------
# Creating and positioning the body.
#-----------------------------------
body = Part.createBox(doc)
elem = App.createElement(doc)
elem.setGeometry(body)
elem.setUserName(Base.StringTool.toString("Body"))

body.length.setValue(2.5)
body.width.setValue(3.5)
body.height.setValue(1.5)

#------------------------------------
# Creating and positioning 1st wheel.
#------------------------------------
wheel = Part.createCylinder(doc)
elem1 = App.createElement(doc)
elem1.setGeometry(wheel)
elem1.setUserName(Base.StringTool.toString("Wheel 1"))

wheel.height.setValue(0.5)
wheel.radius.setValue(0.5)

elem1.placement.translate(Geom.Vec(-0.25, 0.75, 0), Base.CoordSpace_LCS)
axis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 1, 0))
elem1.placement.rotate(axis, math.radians(90), Base.CoordSpace_LCS)

#-----------------------------------
# Copying and positioning 2nd wheel.
#-----------------------------------
elem2 = doc.copyObject(elem1)
elem2 = App.castToElement(elem2)
elem2.setUserName(Base.StringTool.toString("Wheel 2"))

elem2.placement.translate(Geom.Vec(0, 2, 0), Base.CoordSpace_WCS)

#-----------------------------------
# Copying and positioning 3nd wheel.
#-----------------------------------
elem3 = doc.copyObject(elem1)
elem3 = App.castToElement(elem3)
elem3.setUserName(Base.StringTool.toString("Wheel 3"))

elem3.placement.translate(Geom.Vec(2.5, 0, 0), Base.CoordSpace_WCS)

#-----------------------------------
# Copying and positioning 4th wheel.
#-----------------------------------
elem4 = doc.copyObject(elem2)
elem4 = App.castToElement(elem4)
elem4.setUserName(Base.StringTool.toString("Wheel 4"))

elem4.placement.translate(Geom.Vec(2.5, 0, 0), Base.CoordSpace_WCS)

#----------
# Grouping.
#----------
group = App.createGroup(doc)
App.addToGroup(group, elem)
App.addToGroup(group, elem1)
App.addToGroup(group, elem2)
App.addToGroup(group, elem3)
App.addToGroup(group, elem4)

#-----------------------
# Rotating all together.
#-----------------------
axis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 1, 0))
trsf = Geom.Trsf()
trsf.setRotation(axis, math.radians(-30))
children = App.vector_Element()
group.getAllElements(children)
for child in children:
  child.placement.transform(trsf)

doc.recompute()