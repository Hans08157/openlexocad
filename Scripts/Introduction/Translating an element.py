#===============================================================================
#
# TRANSLATING AN ELEMENT
#
#===============================================================================

import Geom
import OpenLxApp as lx
import OpenLxUI  as ui

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#--------------------
# Creating first Block.
#--------------------
block1 = lx.Block.createIn(doc)
elem1  = lx.Element.createIn(doc)
elem1.setGeometry(block1)

origin1 = Geom.Pnt(0, 0, 0)
zDir1 = Geom.Dir(0, 0, 1)
xDir1 = Geom.Dir(1, 1, 0) # This rotates the Block 45 deg. around the Z-Axis

axis1 = Geom.Ax2(origin1, zDir1, xDir1)
elem1.setLocalPlacement(axis1)

#---------------------
# Creating second Block.
#---------------------
block2 = lx.Block.createIn(doc)
elem2  = lx.Element.createIn(doc)
elem2.setGeometry(block2)

origin2 = Geom.Pnt(0, 0, 0)
zDir2 = Geom.Dir(0, 0, 1)
xDir2 = Geom.Dir(1, 0, 0)

axis2 = Geom.Ax2(origin2, zDir2, xDir2)
elem2.setLocalPlacement(axis2)

#-------------------------------------------------------------------------------
# An element can be translated from its actual position, according to  a  vector
# and its local coordinates system (LCS) or the world coordinate system (WCS).
#-------------------------------------------------------------------------------
x = 5; y = 0; z = 0
translation = Geom.Vec(x, y, z) # Defining a translation of 5 along X-Axis.
elem1.translate(translation, Geom.CoordSpace_LCS) # Translating first Block (LCS)
elem2.translate(translation, Geom.CoordSpace_WCS) # Translating second Block (WCS)

#----------------------
# See the difference...
#----------------------
doc.recompute()