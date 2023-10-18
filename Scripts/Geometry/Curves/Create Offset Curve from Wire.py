import OpenLxApp as lx
import OpenLxUI  as ui
import Geom, Topo

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

p1 = Geom.Pnt(0,0,0)
p2 = Geom.Pnt(10,0,0)
p3 = Geom.Pnt(10,10,0)
p4 = Geom.Pnt(0,10,0)

e1 = Topo.EdgeTool.makeEdge(p1,p2) 
e2 = Topo.EdgeTool.makeEdge(p2,p3) 
e3 = Topo.EdgeTool.makeEdge(p3,p4) 
e4 = Topo.EdgeTool.makeEdge(p4,p1) 

wire = Topo.WireTool.makeWire(e1)   
Topo.WireTool.addEdge(wire, e2)
Topo.WireTool.addEdge(wire, e3)
Topo.WireTool.addEdge(wire, e4)

baseCurve   = lx.createCompositeCurveFromWire(doc, wire)
offsetCurve = lx.createOffsetCurveFromWire(doc, wire, Geom.Dir(0,0,1), 1)
if curve and offsetCurve:
    e1 = lx.Element.createIn(doc)
    e1.setGeometry(baseCurve)
    e2 = lx.Element.createIn(doc)
    e2.setGeometry(offsetCurve)
    doc.recompute()