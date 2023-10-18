#===============================================================================
#
# COPYING AN ELEMENT
#
#===============================================================================

import Geom
import OpenLxApp as lx
import OpenLxUI  as ui

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#----------------------
# Creating 1st element.
#----------------------

cylinder = lx.RightCircularCylinder.createIn(doc)
elem1 = lx.Element.createIn(doc)
elem1.setGeometry(cylinder)

cylinder.setHeight(0.5)
cylinder.setRadius(0.5)

#-------------------------------------
# Copying and positioning 2nd element.
#-------------------------------------

elem2 = elem1.copy()
elem2.translate(Geom.Vec(0, 2, 0), Geom.CoordSpace_WCS)
doc.recompute()