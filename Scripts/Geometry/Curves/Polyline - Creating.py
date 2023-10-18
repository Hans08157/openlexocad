#===============================================================================
#
# CREATING A POLYLINE
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Geom

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#--------------------------------------
# 3. Create a geometry in the document.
#--------------------------------------
pl = lx.Polyline.createIn(doc)

#--------------------------------------------------------------------
# 4. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(pl)

#------------------------------------
# 5. Create a vector of points.    
#------------------------------------
points = Geom.vector_Pnt()
points.append(Geom.Pnt(0, 0, 0))
points.append(Geom.Pnt(5, 0, 0))
points.append(Geom.Pnt(10, 10, 0))

#----------------------------------
# 6. Set the points.
#----------------------------------
pl.setPoints(points)

#--------------------------- 
# 7. Recompute the document.
#---------------------------
doc.recompute()