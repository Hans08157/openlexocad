#===============================================================================
#
# CREATING A RECTANGLE (TRIMMED PLANE)
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
rect = lx.createRectangularTrimmedPlane(doc, Geom.Pln(), 10, 10)

#--------------------------------------------------------------------
# 4. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(rect)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()