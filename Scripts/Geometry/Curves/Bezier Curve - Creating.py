#===============================================================================
#
# CREATING A BEZIER CURVE
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
bc = lx.BezierCurve.createIn(doc)

#--------------------------------------------------------------------
# 4. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(bc)

#----------------------------------
# 5. Set the geometry's parameters. 
#----------------------------------
pnts = Geom.vector_Pnt()
pnts.append(Geom.Pnt(0,10,0))
pnts.append(Geom.Pnt(0,0,0))
pnts.append(Geom.Pnt(10,0,0))
pnts.append(Geom.Pnt(10,0,10))
pnts.append(Geom.Pnt(0,0,10))
pnts.append(Geom.Pnt(0,0,20))
pnts.append(Geom.Pnt(10,0,20))
pnts.append(Geom.Pnt(20,0,25))
pnts.append(Geom.Pnt(30,0,20))
pnts.append(Geom.Pnt(40,0,20))
pnts.append(Geom.Pnt(40,0,10))
pnts.append(Geom.Pnt(30,0,10))
pnts.append(Geom.Pnt(30,0,0))
pnts.append(Geom.Pnt(40,0,0))
pnts.append(Geom.Pnt(40,10,0))

bc.setControlPointsList(pnts)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()