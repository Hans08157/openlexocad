#===============================================================================
#
# CREATING AN ISHAPEPROFILEDEF
# This profile is used to create all common steel profiles with an I shape
# like HEA, HEB, HEM etc.
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Geom
lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#----------------------------------------------------------------------------------------
# 3a. Create profile from values
#----------------------------------------------------------------------------------------
profile1 = lx.IShapeProfileDef.createIn(doc)
profile1.setOverallWidth(140e-03)
profile1.setOverallDepth(140e-03)
profile1.setWebThickness(7.0e-03)
profile1.setFlangeThickness(12.0e-03)
profile1.setFilletRadius(12.0e-03)
profile1.setProfileName(lxstr("HEB 140"))

#----------------------------------------------------------------------------------------
# 3b. Create profile from name
#----------------------------------------------------------------------------------------
profile2 = lx.IShapeProfileDef.createIn(doc)
profile2.setValuesFromPredefinedSteelProfile(lxstr("HEM 200"))

#----------------------------------------------------------------------------------------
# 4. Create Extrusions  
#----------------------------------------------------------------------------------------
eas1 = lx.ExtrudedAreaSolid.createIn(doc)
eas1.setSweptArea(profile1)
eas1.setExtrudedDirection(Geom.Dir(0,0,1))
eas1.setDepth(3)

eas2 = lx.ExtrudedAreaSolid.createIn(doc)
eas2.setSweptArea(profile2)
eas2.setExtrudedDirection(Geom.Dir(0,0,1))
eas2.setDepth(3)

#--------------------------------------------------------------------
# 5. Create two elements in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem1 = lx.Element.createIn(doc)
elem1.setGeometry(eas1)

elem2 = lx.Element.createIn(doc)
elem2.setGeometry(eas2)
elem2.translate(Geom.Vec(2,0,0))

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()