import App, Base, Geom, Part

doc = App.castToDocument(App.GetApplication().getActiveDocument())

# Create first element
e1 = App.createElement(doc)
box1 = Part.createBox(doc)
box1.width.setValue(3)
box1.height.setValue(4)
box1.length.setValue(5) 
e1.setGeometry(box1)

# Create second element
e2 = App.createElement(doc)
box2 = Part.createBox(doc)
box2.width.setValue(3)
box2.height.setValue(3)
box2.length.setValue(3)
e2.setGeometry(box2)
e2.placement.translate(Geom.Vec(2,2,0),Base.CoordSpace_WCS)

# We need to recompute the document here to calculate
# the topology of the elements. Only then they can be cut
doc.recompute()

# Create a vector to hold the result of the cutting operation
res = App.vector_Element()

# Cut base (soft) with tool (hard) element
if App.ElementTool.cut(e1,e2,res) != 0:
	print("Error in cut")
else:	
	# On success remove e2 and change appearance of result
	doc.removeObject(e2)	
	for i in res:
		i.setDiffuseColor(Base.Color(255,0,0))
		i.setTransparency(80)

doc.recompute()