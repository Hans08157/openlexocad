#===============================================================================
#
# CREATING AN ELEMENT
#
#===============================================================================

#-----------------------------
# 1. Import Lexocad libraries.
#-----------------------------

import OpenLxApp as lx
import OpenLxUI  as ui

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#--------------------------------------
# 3. Create a geometry in the document.
#--------------------------------------
block = lx.Block.createIn(doc)

#--------------------------------------------------------------------
# 4. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(block)

#----------------------------------
# 5. Set the geometry's parameters.
#----------------------------------
block.setXLength(5)
block.setYLength(5)
block.setZLength(5)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()