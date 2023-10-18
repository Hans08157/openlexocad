import App, Base, Geom, Part

doc = App.castToDocument(App.GetApplication().getActiveDocument())

e = App.createElement(doc)

pnts = Geom.vector_Pnt()
pnts.append(Geom.Pnt(0,0,0))
pnts.append(Geom.Pnt(10,10,0))
pnts.append(Geom.Pnt(15,12,0))
pnts.append(Geom.Pnt(16,20,0))
pnts.append(Geom.Pnt(7,28,0))
pnts.append(Geom.Pnt(2,32,0))

poly = Part.createPolyline(doc)
poly.points.setValue(pnts)
e.setGeometry(poly)

doc.recompute()

# Create offset
s = e.getShape()
w = App.ShapeTool.isSingleWire(s)
if w != None:
    right_curve = Part.createOffsetCurveFromWire(doc,w,Geom.Dir(0,0,1),1)
    left_curve = Part.createOffsetCurveFromWire(doc,w,Geom.Dir(0,0,1),-1)
    if right_curve != None:
        offset_e = App.createElement(doc)
        offset_e.setDiffuseColor(Base.Color(255,0,0))
        offset_e.setGeometry(right_curve)
    if left_curve != None:
        offset_e = App.createElement(doc)
        offset_e.setDiffuseColor(Base.Color(0,255,0))
        offset_e.setGeometry(left_curve)
		
doc.recompute()