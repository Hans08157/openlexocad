#===============================================================================
#
# CREATING A SECTION OF SPHERE ("PARMESAN CHEESE")
# 
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Geom

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#--------------------------------------
# 3. Create a geometry in the document.
#--------------------------------------
sphere = lx.Sphere.createIn(doc)

#--------------------------------------------------------------------
# 4. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(sphere)

#----------------------------------
# 5. Set the geometry's parameters.
#----------------------------------
sphere.setRadius(5)

#----------------------
# 6. Setting the color.
#----------------------
myColor = Base.Color(255, 255, 0)
elem.setDiffuseColor(myColor)

#--------------------------- 
# 7. Recompute the document.
#---------------------------
doc.recompute()