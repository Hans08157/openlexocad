#===============================================================================
#
# EXTRUSION OF CIRCLE
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Geom
import math

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#----------------------------------------------------------------------------------------
# 3. Create profile  
#----------------------------------------------------------------------------------------
profile = lx.CircleProfileDef.createIn(doc)
profile.setRadius(2)
eas = lx.ExtrudedAreaSolid.createIn(doc)
eas.setSweptArea(profile)
eas.setExtrudedDirection(Geom.Dir(0,0,1))
eas.setDepth(3)

#--------------------------------------------------------------------
# 6. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(eas)

#--------------------------- 
# 7. Recompute the document.
#---------------------------
doc.recompute()