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
def createBox(pntFrom, pntTo, size):
    height = pntFrom.distance(pntTo)    
    block = lx.Block.createIn(doc)
    block.setXLength(size)
    block.setYLength(size)
    block.setZLength(height)
    elem = lx.Element.createIn(doc)
    elem.setGeometry(block)
    pos1 = Geom.Ax2(Geom.Pnt(-size/2., -size/2., 0.), Geom.Dir(0,0,1))
    block.setPosition(pos1) # This is needed to shift the origin of the block from the lower left conrner to the lower center point (like a cylinder/cone)
   
    v = Geom.Vec(pntFrom, pntTo)
    pos2 = Geom.Ax2(pntFrom, Geom.Dir(v))
    elem.setTransform(computeTrsf(pos2))
    

#------------------------------------------------------------------------------
app = lx.Application.getInstance()
doc = app.getActiveDocument() 

createBox(Geom.Pnt(0,0,0), Geom.Pnt( 10,   0,   0), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(-10,   0,   0), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(  0,  10,   0), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(  0, -10,   0), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(  0,   0,  10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(  0,   0, -10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt( 10,  10,   0), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(-10, -10,   0), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt( 10,   0,  10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(-10,   0, -10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(  0,  10,  10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(  0, -10, -10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt( 10,  10,  10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt( 10,  10, -10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt( 10, -10, -10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(-10, -10, -10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(-10, -10,  10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(-10,  10,  10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt( 10, -10,  10), 1)
createBox(Geom.Pnt(0,0,0), Geom.Pnt(-10,  10, -10), 1)
doc.recompute() 