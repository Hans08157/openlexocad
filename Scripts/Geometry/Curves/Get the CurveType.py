#===============================================================================
#
# GET THE CURVETYPE OF AN EDGE
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Geom, Topo

st = Topo.ShapeTool
et = Topo.EdgeTool

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#---------------------------------------
# 3. Creating some points for the curve.
#---------------------------------------
p1 = Geom.Pnt(0, 0, 0)
p2 = Geom.Pnt(5, 5, 0)
p3 = Geom.Pnt(5, 0, 0)

#----------------------------------------------------------------------------------------
# 4. Create the CompositeCurve and add the CompositeCureveSegments to it.
# All segments must be contiguous or the curve will be invalid and won't be drawn.    
#----------------------------------------------------------------------------------------
compcurve = lx.CompositeCurve.createIn(doc)
compcurve.addSegment(lx.createLineSegment(doc, p1, p2))
compcurve.addSegment(lx.createArc3PointsSegment(doc, p2, p3, p1))

#--------------------------------------------------------------------
# 6. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(compcurve)

#--------------------------- 
# 7. Recompute the document.
#---------------------------
doc.recompute()

shape = elem.getShape()
edges = st.getEdges(shape)

for i in range(edges.size()):
   ct = et.getGeomCurveType(edges[i])
   if not ct.ok:
      continue
	  
   if ct.type == Geom.CurveType_LINE: print("LINE")
   if ct.type == Geom.CurveType_CIRCLE: print("CIRCLE")
   if ct.type == Geom.CurveType_ELLIPSE: print("ELLIPSE")
   if ct.type == Geom.CurveType_PARABOLA: print("PARABOLA")
   if ct.type == Geom.CurveType_BEZIERCURVE: print("BEZIERCURVE")
   if ct.type == Geom.CurveType_BSPLINECURVE: print("BSPLINECURVE")
   if ct.type == Geom.CurveType_OTHERCURVE: print("OTHERCURVE")
