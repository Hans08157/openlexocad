#===============================================================================
#
# CREATING A CARTESIAN POINT
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Topo, Geom, Draw

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#--------------------------------------
# 3. Create a geometry in the document.
#--------------------------------------
pnt = lx.CartesianPoint.createIn(doc)

#----------------------------------
# 4. Set the geometry's parameters.
#----------------------------------
pnt.setPoint(Geom.Pnt(0,0,10))

#--------------------------------------------------------------------
# 5. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(pnt)

#---------------------------------------
# 6. Assign a "draw style" (point size).
#---------------------------------------
ds = elem.getDrawStyle()
ds.setPointSize(10)
elem.setDrawStyle(ds)

#--------------------------- 
# 7. Recompute the document.
#---------------------------
doc.recompute()