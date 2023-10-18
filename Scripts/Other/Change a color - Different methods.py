#===============================================================================
#
# CHANGING THE (DIFFUSE) COLOR
#
#===============================================================================

#-----------------------------
# 1. Import Lexocad libraries.
#-----------------------------
import App, Base, Part

#----------------------------
# 2. Get the active document.
#----------------------------
doc = App.castToDocument(App.GetApplication().getActiveDocument())

#--------------------------------------
# 3. Create a geometry in the document.
#--------------------------------------
box = Part.createBox(doc)

#--------------------------------------------------------------------
# 4. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = App.createElement(doc)
elem.setGeometry(box)

#---------------------------------------------
# 5. Define a color, assign it to the element.
#---------------------------------------------
myColor = Base.Color(255, 0, 0)
elem.setDiffuseColor(myColor)

#----------------------------------------------------
# 5a. EXAMPLE FOR CHANGING "RGB" VALUES ALL TOGETHER.
#     Remember to reassign the color to the element.
#----------------------------------------------------
red = 255; green = 255; blue = 0
myColor.setRgb(red, green, blue)
elem.setDiffuseColor(myColor)

#-------------------------------------------
# 5b. EXAMPLE FOR CHANGING ONE SINGLE VALUE.
#     Remember to reassign the color.
#-------------------------------------------
myColor.setBlue(255)
elem.setDiffuseColor(myColor)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()