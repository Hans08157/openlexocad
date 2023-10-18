#===============================================================================
#
# DELETING AN ELEMENT
#
#===============================================================================

import OpenLxApp as lx
import OpenLxUI  as ui

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#--------------------------------------
# First create the element.
#--------------------------------------
block = lx.Block.createIn(doc)
elem  = lx.Element.createIn(doc)
elem.setGeometry(block)
doc.recompute()

# Do whatever you want with the element

#--------------------------- 
# Delete the element.
#---------------------------
doc.removeObject(elem)
doc.recompute()