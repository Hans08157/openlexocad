#===============================================================================
#
# CREATING A BOX
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

#--------------------------------------------------------------------
# 4. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem  = lx.Element.createIn(doc)
block = lx.Block.createIn(doc)
elem.setGeometry(block)

#----------------------------------
# 5. Set the geometry's parameters.
#----------------------------------
block.setXLength(5)
block.setYLength(5)
block.setZLength(5)

#--------------------------
# 6. Setting the placement.
#--------------------------
elem.setLocalPlacement(Geom.Ax2(Geom.Pnt(2,3,4),Geom.Dir(0,0,1)))

#--------------------------- 
# 7. Recompute the document.
#---------------------------
doc.recompute()