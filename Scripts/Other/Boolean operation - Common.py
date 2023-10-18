# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom

app = lx.Application.getInstance()
doc = app.getActiveDocument() 

# Create first element
e1 = lx.Element.createIn(doc)
block1 = lx.Block.createIn(doc)
block1.setYLength(3)
block1.setZLength(4)
block1.setXLength(5) 
e1.setGeometry(block1)

# Create second element
e2 = lx.Element.createIn(doc)
block2 = lx.Block.createIn(doc)
block2.setYLength(3)
block2.setZLength(3)
block2.setXLength(3)
e2.setGeometry(block2)
e2.translate(Geom.Vec(2,2,0),Geom.CoordSpace_WCS)

# We need to recompute the document here to calculate
# the topology of the elements. Only then they can be cut
doc.recompute()

# Create a vector to hold the result of the cutting operation
res = lx.vector_Element()

# Cut base (soft) with tool (hard) element
if lx.bop_common(e1,e2,res) != 0:
	print("Error in common")
else:	
	# On success remove e2 and change appearance of result
	doc.removeObject(e1)	
	doc.removeObject(e2)	
	for i in res:
		i.setDiffuseColor(Base.Color(255,0,0))
		i.setTransparency(80)

doc.recompute()