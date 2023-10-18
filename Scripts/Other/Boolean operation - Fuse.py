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

# Collecting the elements to be fused
input = App.vector_Element()
input.push_back(e1)
input.push_back(e2)

# Fuse the elements
output = App.ElementTool.fuse(input,True) 
if(output == None): print("Error in fuse")

output.setDiffuseColor(Base.Color(255,0,0))
output.setTransparency(80)
doc.removeObject(e1)	
doc.removeObject(e2)	
doc.recompute()
