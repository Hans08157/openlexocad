# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom

app = lx.Application.getInstance()
doc = app.getActiveDocument() 

# Create soft element
block = lx.Block.createIn(doc)
block.setYLength(1.)
block.setZLength(2.)
block.setXLength(10.)

sElement = lx.Element.createIn(doc)
sElement.setGeometry(block)

# Create hard elements
hElements = lx.vector_Element()

cylinder1 = lx.RightCircularCylinder.createIn(doc)
cylinder1.setHeight(2.)
cylinder1.setRadius(1.)

hElement1 = lx.Element.createIn(doc)
hElement1.setGeometry(cylinder1)
hElement1.translate(Geom.Vec(0., 0.5, 0.),Geom.CoordSpace_WCS)
hElements.push_back(hElement1)

cylinder2 = lx.RightCircularCylinder.createIn(doc)
cylinder2.setHeight(2.)
cylinder2.setRadius(1.)

hElement2 = lx.Element.createIn(doc)
hElement2.setGeometry(cylinder2)
hElement2.translate(Geom.Vec(5., 0.5, 0.),Geom.CoordSpace_WCS)
hElements.push_back(hElement2)

cylinder3 = lx.RightCircularCylinder.createIn(doc)
cylinder3.setHeight(2.)
cylinder3.setRadius(1.)

hElement3 = lx.Element.createIn(doc)
hElement3.setGeometry(cylinder3)
hElement3.translate(Geom.Vec(10., 0.5, 0.),Geom.CoordSpace_WCS)
hElements.push_back(hElement3)

# We need to recompute the document here to calculate
# the topology of the elements. Only then they can be cut
doc.recompute()

# Create a vector to hold the result of the cutting operation
resultingElements = lx.vector_Element()

# Cut base (soft) with tool (hard) elements
if lx.bop_cut(sElement, hElements, resultingElements) != 0:
	print("Error in cut")

doc.recompute()