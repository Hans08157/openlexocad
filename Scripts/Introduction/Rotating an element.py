#===============================================================================
#
# ROTATING AN ELEMENT
#
#===============================================================================

import Base, Geom
import OpenLxApp as lx
import OpenLxUI  as ui

import math

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#--------------------
# Creating first Block.
#--------------------
block1 = lx.Block.createIn(doc)
elem1 = lx.Element.createIn(doc)
elem1.setGeometry(block1)

origin1 = Geom.Pnt(5, 0, 0)
zDir1 = Geom.Dir(0, 0, 1)
xDir1 = Geom.Dir(1, 0, 0)

axis1 = Geom.Ax2(origin1, zDir1, xDir1)
elem1.setLocalPlacement(axis1)

red = 255; green = 0; blue = 0
myColor = Base.Color(red, green, blue)
elem1.setDiffuseColor(myColor)

#---------------------
# Creating second Block.
#---------------------
block2 = lx.Block.createIn(doc)
elem2 = lx.Element.createIn(doc)
elem2.setGeometry(block2)

origin2 = Geom.Pnt(5, 0, 0)
zDir2 = Geom.Dir(0, 0, 1)
xDir2 = Geom.Dir(1, 0, 0)

axis2 = Geom.Ax2(origin2, zDir2, xDir2)
elem2.setLocalPlacement(axis2)

#-------------------------------------------------------------------------------
# An element can be rotated around an axis, according to its  local  coordinates 
# system (LCS) or the world coordinate system (WCS).
#-------------------------------------------------------------------------------
ang = math.radians(45)
rotationPoint = Geom.Pnt(0, 0, 0)

xAxis = Geom.Ax1(rotationPoint, Geom.Dir(1, 0, 0))
yAxis = Geom.Ax1(rotationPoint, Geom.Dir(0, 1, 0))
zAxis = Geom.Ax1(rotationPoint, Geom.Dir(0, 0, 1))

elem1.rotate(xAxis, ang, Geom.CoordSpace_LCS) # Rotating the first Block (LCS)
elem1.rotate(yAxis, ang, Geom.CoordSpace_LCS) #
elem1.rotate(zAxis, ang, Geom.CoordSpace_LCS) #

elem2.rotate(xAxis, ang, Geom.CoordSpace_WCS) # Rotating the second Block (WCS)
elem2.rotate(yAxis, ang, Geom.CoordSpace_WCS) #
elem2.rotate(zAxis, ang, Geom.CoordSpace_WCS) #

#----------------------
# See the difference...
#----------------------
doc.recompute()