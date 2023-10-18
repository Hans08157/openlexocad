import OpenLxApp as lx
import Geom

doc = lx.Application.getInstance().getActiveDocument()

def createWall(aLength, aWidth, aHeight):
    rect = lx.RectangleProfileDef.createIn(doc)
    rect.setXDim(aLength)
    rect.setYDim(aWidth)
    
    ext = lx.ExtrudedAreaSolid.createIn(doc)
    ext.setSweptArea(rect)
    ext.setDepth(aHeight)
    ext.setExtrudedDirection(Geom.Dir(0,0,1))
    
    pos = Geom.Ax2(Geom.Pnt(0,0,0), Geom.Dir(0,0,1), Geom.Dir(1,0,0))
    ext.setPosition(pos)
    
    wall = lx.WallStandardCase.createIn(doc)
    wall.setGeometry(ext)
    return wall
    
def createOpeningElement(aLength, aWidth, aHeight, aSillHeight):
    rect = lx.RectangleProfileDef.createIn(doc)
    rect.setXDim(aLength)
    rect.setYDim(aHeight)
    
    ext = lx.ExtrudedAreaSolid.createIn(doc)
    ext.setSweptArea(rect)
    ext.setDepth(aWidth)
    ext.setExtrudedDirection(Geom.Dir(0,0,1))
    
    loc = Geom.Pnt(0, aWidth/2., aHeight/2.+aSillHeight)
    xDir = Geom.Dir(1,0,0)
    yDir = Geom.Dir(0,0,1)
    zDir = xDir.crossed(yDir)
    pos = Geom.Ax2(loc, zDir, xDir)
    ext.setPosition(pos)
    
    opening = lx.OpeningElement.createIn(doc)
    opening.setGeometry(ext)
    return opening
    

if __name__ == "__main__":
    wall = createWall(5,.2,2.8)
    opening = createOpeningElement(1,.2,1.2,1)
    wall.addOpeningElement(opening)
    doc.recompute()
    

    


