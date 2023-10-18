#===============================================================================
#
# CREATING A SURFACE FROM ARBITRARY POINTS
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Topo, Geom

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#---------------------------------------------
# 3. Create the points and a face out of them.
#---------------------------------------------
pnts = Geom.vector_Pnt()
pnts.append(Geom.Pnt( 0, 0, 0))
pnts.append(Geom.Pnt(10, 0, 0))
pnts.append(Geom.Pnt(10,10, 0))

face = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(pnts))

#--------------------------------------
# 4. Create a geometry in the document.
#--------------------------------------
geo = lx.createCurveBoundedPlaneFromFace(doc, face)

#--------------------------------------------------------------------
# 5. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(geo)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()