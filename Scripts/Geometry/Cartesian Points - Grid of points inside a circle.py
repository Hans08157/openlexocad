#===============================================================================
#
# CREATING A CIRCLE AND AN EVENLY SPACED GRID OF POINT INSIDE OF IT
#
#===============================================================================
import math
import OpenLxApp as lx
import OpenLxUI  as ui
import Topo, Geom, Draw

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#---------------------------------------------------------------------
# 1. We create a circle in a way we've already seen in other examples.
#---------------------------------------------------------------------
radius = 10.

geometry = lx.Circle.createIn(doc)
geometry.setRadius(radius)

elem = lx.Element.createIn(doc)
elem.setGeometry(geometry)
doc.recompute()

#----------------------------------------------------------------
# 2. We create a face out of the geometry: it will be used later.
#----------------------------------------------------------------
shape = geometry.getShape()
face = Topo.FaceTool.makeFace(Topo.ShapeTool.isSingleWire(shape))

# If your geometry is a surface, then replace the block above with:
# shape = geometry.getShape()
# face = Topo.FaceTool.isSingleFace(shape)

#------------------------------------------------------------------------------------------
# 3. We compute a regular grid of points, but only those inside the circle will be created.
#------------------------------------------------------------------------------------------
bbox = elem.getBoundingBox()

spacing = 1.
startX = bbox.GetXmin()
startY = bbox.GetYmin()
lengthX = bbox.GetXsize()
lengthY = bbox.GetYsize()
numintervalX = math.floor(lengthX / spacing)
numintervalY = math.floor(lengthY / spacing)
dX = lengthX / numintervalX
dY = lengthY / numintervalY
for i in range(int(numintervalY + 1)):
 for j in range(int(numintervalX + 1)):
    pnt = Geom.Pnt(startX + dX * j, startY + dY * i, 0.)
    if Topo.FaceTool.isValidPointForFace(pnt, face): # This function tests if the given point is inside the given face
     cPnt = lx.CartesianPoint.createIn(doc)
     cPnt.setPoint(pnt)
     e = lx.Element.createIn(doc)
     e.setGeometry(cPnt)
     e.getDrawStyle().setPointSize(2)
     
doc.recompute()