#===============================================================================
#
# EXTRUDE A FACE (SURFACE) GIVEN A DIRCETION AND A LENGTH
#
#===============================================================================

#-----------------------------
# 1. Import Lexocad libraries.
#-----------------------------
import Base, Geom, Topo
import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString
st    = Topo.ShapeTool
ft    = Topo.FaceTool
wt    = Topo.WireTool

#----------------------------
# 2. Get the active document.
#----------------------------

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#---------------------------------------------
# 3. Create the points and a face out of them.
#---------------------------------------------
pnts = Geom.vector_Pnt()
pnts.append(Geom.Pnt( 0, 0, 0))
pnts.append(Geom.Pnt(10, 0, 0))
pnts.append(Geom.Pnt(10,10, 0))

face = ft.makeFace(wt.makePolygon(pnts))

#--------------------------------------
# 4. Create a geometry in the document.
#--------------------------------------
geo = lx.createCurveBoundedPlaneFromFace(doc, face)

#--------------------------------------------------------------------
# 5. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(geo)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()

#--------------------------
# 7. Perform the extrusion.
#--------------------------
length = 5.                 # Length of the extrusion
faceIdx = 0                 # Extrude the first (and unique) face (index 0) of the element
dir = Geom.Dir(0., 0., 1.)  # Direction of extrusion (global "up" Z+)

cmd = cmd.CmdExtrudeFace(elem, faceIdx, dir, length)
cmd.redo()