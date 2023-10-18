#===============================================================================
#
# CREATING AN ARC (3 POINTS)
#
#===============================================================================

#-----------------------------
# 1. Import Lexocad libraries.
#-----------------------------
# OpenLexocad libraries
import OpenLxApp as lx
import Geom

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()   

#------------------------------------
# 3. Define three points for the arc.
#------------------------------------
start  = Geom.Pnt(0, 0, 0)
middle = Geom.Pnt(5, 0, 0)
end    = Geom.Pnt(5, 5, 0)

#--------------------------------------
# 4. Create a geometry in the document.
#--------------------------------------
arc3Points = lx.createArc3Points(doc, start, middle, end)

#--------------------------------------------------------------------
# 5. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(arc3Points)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()