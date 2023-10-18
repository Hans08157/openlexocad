# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom
import math

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

def printPnt(aMsg, aPnt):
    print("Point: ", aMsg, " ", aPnt.x(), " ", aPnt.y(), " ", aPnt.z())


def pick2Points():
    pnts = []
    ui.showStatusBarMessage(lxstr("Pick first point")) 
    ok = uidoc.pickPoint()
    if ok:
        pp1 = uidoc.getPickedPoint()
        pnts.append(pp1)
        uidoc.drawRubberBand(pp1)
        ui.showStatusBarMessage(lxstr("Pick second point")) 
        ok = uidoc.pickPoint()
        if ok :
            pp2 = uidoc.getPickedPoint()
            pnts.append(pp2)
            uidoc.removeRubberBand()
            return pnts
    
    uidoc.removeRubberBand()
    ui.resetStatusBarMessage() 
    return False
    
def pick1Point():
    ui.showStatusBarMessage(lxstr("Pick second point")) 
    ok = uidoc.pickPoint()
    if ok:
        p = uidoc.getPickedPoint()
    else:
        p = False
    ui.resetStatusBarMessage() 
    return p
    
    
def createArc(aDoc, aCenterPnt, aRadius, aTrim1, aTrim2):
    print("Create Arc")
    circle = lx.Circle(doc)
    circle.setRadius(aRadius)
    circle.setPosition(Geom.Ax2(aCenterPnt, Geom.Dir(0,0,1)))
    tc = lx.TrimmedCurve(doc)
    tc.setBasisCurve(circle)
    tc.setTrim1(aTrim1)
    tc.setTrim2(aTrim2)
    seg = lx.CompositeCurveSegment(doc)
    seg.setParentCurve(tc)
    return seg
 
class PointedArch(lx.Element):
    def getGlobalClassId(self):
        return Base.GlobalId("{AF66A951-EDD8-43AC-A162-48E4E7165240}")
        
    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("PointedArch", "OpenLxApp.Element")
        # Register properties 
        self.setPropertyHeader(lxstr("Pointed Arch"), -1)
        self.setPropertyGroupName(lxstr("Arch Parameter"), -1)
        self.excess = self.registerPropertyDouble("Excess",   \
                                                   0.5, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.NOT_EDITABLE, \
                                                   -1)  
        self.width  = self.registerPropertyDouble("Width", \
                                                   1.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self.height = self.registerPropertyDouble("Height", \
                                                   1.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1) 
        self.hasBottomLine = self.registerPropertyBool("Bottom Line", \
                                                   False, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1) 
        # TODO Depth Thickness
        self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())
 
        
    def createCompositeCurve(self):
        width     = self.width.getValue()
        height    = self.height.getValue()
        if width < 1e-04 or height < 1e-04:
            return False
            
        halfDist  = width/2.
        leftPnt   = Geom.Pnt(-halfDist,0,0)
        rightPnt  = Geom.Pnt( halfDist,0,0)
        midPnt    = Geom.Pnt(0,0,0)
        midPntH   = Geom.Pnt(0,height,0)
        midPntNH  = Geom.Pnt(0,-height,0)
        rightCirc = Geom.Circ()
        if not Geom.GeomTools.makeCircleFrom3Points(midPntH, rightPnt, midPntNH, rightCirc):
            print("Cannot create right circle")
            return
            
        leftCirc = Geom.Circ()
        if not Geom.GeomTools.makeCircleFrom3Points(midPntH, leftPnt, midPntNH, leftCirc):
            print("Cannot create left circle")
            return
            
        rightCenter = Geom.Pnt( halfDist-rightCirc.radius(),0,0)
        leftCenter  = Geom.Pnt(-halfDist+rightCirc.radius(),0,0)
        radius      = rightCirc.radius()
        
        if Geom.GeomTools.isEqual(halfDist-radius,0.):
            angle = math.pi/2.
        else:
            angle = math.atan(height/abs(halfDist-radius))        
        self.excess.setValue(radius/width)

        seg1 = createArc(doc, rightCenter, radius, 0, angle)
        seg2 = createArc(doc, leftCenter, radius, math.pi-angle, math.pi)        
        cc   = lx.CompositeCurve(doc)
        cc.addSegment(seg1)
        cc.addSegment(seg2)
        
        if self.hasBottomLine.getValue():
            seg3 = lx.createLineSegment(doc,leftPnt,rightPnt)
            cc.addSegment(seg3)
            
        return cc    
        
    def buildElem(self, aPL, aPR): 
        cc = self.createCompositeCurve()
        self.setGeometry(cc)        
        xDir = Geom.Dir(aPL.xyz() - aPR.xyz())
        yDir = Geom.Dir(0,0,1)
        zDir = xDir.crossed(yDir)
        pos = Geom.Ax2(Geom.GeomTools.midpoint(aPL,aPR), zDir, yDir, xDir)
        self.setLocalPlacement(pos)
    
    def modifyElem(self):        
        res = Geom.Precision.linear_Resolution()
        if self.width.getValue() <= res or self.height.getValue() <= res:
            print("Invalid values")
            return False
 
        cc = self.createCompositeCurve()
        self.setGeometry(cc)        
            
    def onPropertyChanged(self, aPropertyName):
        doc.beginEditing()
        self.modifyElem()        
        doc.endEditing()
        doc.recompute()
        
    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        doc.beginEditing()
        if not Geom.GeomTools.isEqual(x,1.):
            print("Scaling in X")
            old = self.width.getValue()
            self.width.setValue(old*x)
            self.modifyElem()      
        if not Geom.GeomTools.isEqual(y,1.):
            print("Scaling in Y")
            old = self.height.getValue()
            self.height.setValue(old*y)
            self.modifyElem() 
        if not Geom.GeomTools.isEqual(z,1.):
            print("Scaling in Z")

        self.translateAfterScaled(aVec, aScaleBasePnt)
        doc.endEditing()
        doc.recompute()
    
if __name__ == "__main__":    
    doc.registerPythonScript(Base.GlobalId("{fa5ed926-ab36-4c5d-bbff-654287c842f6}"))  
    
    thisScript = lx.Application.getInstance().getActiveScript()
    pp = False
    
    if thisScript.isDragAndDropped():
        uidoc.drawRubberBand(thisScript.getInsertionPoint())
        p2 = pick1Point()
        if p2:
            pp = []
            pp.append(thisScript.getInsertionPoint())
            pp.append(p2)
        uidoc.removeRubberBand()
    else:
        pp = pick2Points()
       
   
    if pp:
        dist = pp[0].distance(pp[1])
        heightVal = ui.getDoubleDialog(lxstr("Enter Height"), dist, 1, 1e-04)
        if pp and not heightVal.isNull():
            print("Values entered")
            doc.beginEditing()
            pointedArch = PointedArch(doc)
            pointedArch.height.setValue(heightVal.getValue())
            pointedArch.width.setValue(pp[0].distance(pp[1]))
            pointedArch.buildElem(pp[0], pp[1])
            doc.endEditing()
            doc.recompute() 
        else:
            print("Bad values entered!")
    