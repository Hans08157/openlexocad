#===============================================================================
#
# SETTING THE VISUAL APPEARANCE OF AN ELEMENT
#
#===============================================================================

#-----------------------------
# 1. Import Lexocad libraries.
#-----------------------------
import Base
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

#---------------------------------
# 5. Define the visual appearance.
#---------------------------------
red = 255; green = 0; blue = 0
transparency = 50
lineThickness = 5

#----------------------------------
# 6. Set the values to the element.
#----------------------------------
elem.setDiffuseColor(Base.Color(red, green, blue))
elem.setTransparency(transparency)
elem.setLineWidth(lineThickness)

#--------------------------- 
# 7. Recompute the document.
#---------------------------
doc.recompute()