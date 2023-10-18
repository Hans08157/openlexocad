#===============================================================================
#
# GET CURVE PARAMETERS FROM EDGE
#
#===============================================================================

import  Geom, Topo
import  OpenLxApp as lx

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#----------------------------------------------------------------------------------------
# 1. Get arc parameter  
#----------------------------------------------------------------------------------------
l = lx.createArc3Points(doc, Geom.Pnt(0,0,0), Geom.Pnt(10,10,0), Geom.Pnt(0,20,0))
e = lx.Element.createIn(doc)
e.setGeometry(l)
doc.recompute()

edges = Topo.ShapeTool.getEdges(e.getShape())
ed1 = edges[0]

res = Topo.EdgeTool.getArcParameters(ed1)
res.ok
if res.ok:
   print(res.startParam)
   print(res.endParam)
   print(res.circle)

else:
   print("Could not get Arc parameter")

#----------------------------------------------------------------------------------------
# 2. Get line parameter  
#----------------------------------------------------------------------------------------   
l = lx.createStraight(doc, Geom.Pnt(0,0,0), Geom.Pnt(0,20,0))
e = lx.Element.createIn(doc)
e.setGeometry(l)
doc.recompute()

edges = Topo.ShapeTool.getEdges(e.getShape())
ed1 = edges[0]

res = Topo.EdgeTool.getLineParameters(ed1)
res.ok
if res.ok:
   print(res.startParam)
   print(res.endParam)
   print(res.scale)
   print(res.line)

else:
   print("Could not get line parameter")
