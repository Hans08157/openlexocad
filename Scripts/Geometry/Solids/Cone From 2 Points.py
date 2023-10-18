import math, time
import OpenLxApp as lx
import OpenLxUI  as ui
import Geom
#------------------------------------------------------------------------------
def computeTrsf(ax2):
	matrix = Geom.Mat()
	matrix.setIdentity()
	matrix.setCol(1, ax2.xDirection().xyz())
	matrix.setCol(2, ax2.yDirection().xyz())
	matrix.setCol(3, ax2.direction().xyz())
	return Geom.Trsf(matrix, ax2.location().xyz(), 1.)
#------------------------------------------------------------------------------
def createCone(pntFrom, pntTo, radius):
	height = pntFrom.distance(pntTo)
	cone = lx.RightCircularCone.createIn(doc)
	cone.setHeight(height)
	cone.setBottomRadius(radius)
	elem = lx.Element.createIn(doc)
	elem.setGeometry(cone)
	
	v = Geom.Vec(pntFrom, pntTo)
	ax2 = Geom.Ax2(pntFrom, Geom.Dir(v))
	elem.setTransform(computeTrsf(ax2))		

#------------------------------------------------------------------------------

app = lx.Application.getInstance()
doc = app.getActiveDocument()
createCone(Geom.Pnt(0,0,0), Geom.Pnt( 10,   0,   0), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(-10,   0,   0), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(  0,  10,   0), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(  0, -10,   0), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(  0,   0,  10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(  0,   0, -10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt( 10,  10,   0), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(-10, -10,   0), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt( 10,   0,  10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(-10,   0, -10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(  0,  10,  10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(  0, -10, -10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt( 10,  10,  10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt( 10,  10, -10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt( 10, -10, -10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(-10, -10, -10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(-10, -10,  10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(-10,  10,  10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt( 10, -10,  10), 1)
createCone(Geom.Pnt(0,0,0), Geom.Pnt(-10,  10, -10), 1)
doc.recompute()