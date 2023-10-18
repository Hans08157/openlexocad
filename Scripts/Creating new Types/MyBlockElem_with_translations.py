# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()


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


def on_Take_Length_Button_clicked(aBlockElem):
    print("on_Take_Length_Button_clicked")
    pp = pick2Points()
    if not pp:
        pass
    dist = pp[0].distance(pp[1])
    aBlockElem.length.setValue(dist)
    aBlockElem.modifyElem()
    print("name: ", aBlockElem.name)


class MyBlockElem(lx.Element):
    def getGlobalClassId(self):
        return Base.GlobalId("{00fdf8c1-06c4-4653-b4fa-1784f9f07746}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("MyBlockElem", "OpenLxApp.Element")
        # Register properties 
        self.setPropertyHeader(lxstr("MyBlockElem"), -1)
        self.setPropertyGroupName(lxstr("Block Parameter"), -1)
        self.length = self.registerPropertyDouble("Length",   \
                                                   1.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -217)  
        self.width  = self.registerPropertyDouble("Width", \
                                                   1.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -197)
        self.height = self.registerPropertyDouble("Height", \
                                                   1.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -198) 
        self.testButton = self.registerPropertyButton("Take Length", \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self.hasVoid = self.registerPropertyBool("Has Void", \
                                                   False, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self.myName = self.registerPropertyString("Name", \
                                                   lxstr("Block Name"), \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -214)
        self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())
       
    def createBlock(self):
        res = Geom.Precision.linear_Resolution()
        length = self.length.getValue()
        width  = self.width.getValue()
        height = self.height.getValue()
        if width <= res or height <= res or length <= res:
            return False
        # Build the geometry
        block = lx.Block(self.getDocument())
        block.setXLength(self.length.getValue())
        block.setYLength(self.width.getValue())
        block.setZLength(self.height.getValue())
        return block
    
    def modifyElem(self):
        block = self.createBlock()
        if block:
            self.setGeometry(block)        
            
    def onPropertyChanged(self, aPropertyName):
        """
        Is called when a Property has changed.
        """   
        doc.beginEditing()        
        if aPropertyName == "Take Length":
            on_Take_Length_Button_clicked(self)           
        else:
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
            old = self.length.getValue()
            self.length.setValue(old*x)
            self.modifyElem()      
        if not Geom.GeomTools.isEqual(y,1.):
            print("Scaling in Y")
            old = self.width.getValue()
            self.width.setValue(old*y)
            self.modifyElem() 
        if not Geom.GeomTools.isEqual(z,1.):
            print("Scaling in Z")
            old = self.height.getValue()
            self.height.setValue(old*z)
            self.modifyElem()
            
        self.translateAfterScaled(aVec, aScaleBasePnt)
        doc.endEditing()
        doc.recompute()
    
if __name__ == "__main__":   
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{099fa031-897d-4163-a168-a62038c92e91}"))
    
    blockElem = MyBlockElem(doc)
    
    # Begin editing of the Element
    doc.beginEditing()
    blockElem.length.setValue(1.)
    blockElem.width.setValue(1.)
    blockElem.height.setValue(1.)
    b = blockElem.createBlock()
    blockElem.setGeometry(b)
    
    thisScript = lx.Application.getInstance().getActiveScript()
    if thisScript.isDragAndDropped():
        pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0,0,1))
    else:
        pos = Geom.Ax2(Geom.Pnt(0,0,0), Geom.Dir(0,0,1))
        
    blockElem.setLocalPlacement(pos)
    # End editing of the Element
    doc.endEditing()
    doc.recompute()   
    