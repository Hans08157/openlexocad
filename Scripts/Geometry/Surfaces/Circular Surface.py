#===============================================================================
#
# CREATING A CIRCULAR SURFACE
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Geom, Topo
import math

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#-------------------------------------
# 3. Define the geometry's parameters.
#-------------------------------------
position = Geom.Ax2(Geom.Pnt(0., 0., 0.), Geom.Dir(0., 0., 1.))
radius = 10.

#--------------------------------------
# 4. Create a geometry in the document.
#--------------------------------------
plane = lx.Plane.createIn(doc)
plane.setPosition(position)

circ  = lx.Circle.createIn(doc)
circ.setRadius(radius)

tc = lx.TrimmedCurve.createIn(doc)
tc.setBasisCurve(circ)
tc.setTrim1(0)
tc.setTrim2(2*math.pi)

surface = lx.CurveBoundedPlane.createIn(doc)
surface.setBasisSurface(plane)
surface.setOuterBoundary(tc)

#--------------------------------------------------------------------
# 5. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(surface)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()