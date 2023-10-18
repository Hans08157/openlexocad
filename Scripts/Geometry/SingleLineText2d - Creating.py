#===============================================================================
#
# CREATING A SINGLE LINE TEXT 2D
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import Base
import OpenLxApp as lx

#----------------------------
# 2. Get the active document.
#----------------------------
app = lx.Application.getInstance()
doc = app.getActiveDocument()

#------------------------------------
# 3. Create the text in the document.
#------------------------------------
txt = lx.SingleLineText2d.createIn(doc)

#------------------------------
# 4. Set the text's parameters.
#------------------------------
txt.setColor(Base.Color(255,0,0))
txt.setFontBold()
txt.setFontItalic()
txt.setFontName("Arial")
txt.setFontSize(24)
txt.setFontStretch(2)
txt.setScale(200)
txt.setText("Lexocad")

#----------------------------------------------------------------
# 5. Create an element in the document and assign the text to it.
#----------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(txt)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()