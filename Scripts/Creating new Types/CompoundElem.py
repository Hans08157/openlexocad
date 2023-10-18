# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom
import random

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

class CompoundElem(lx.Element):
    def getGlobalClassId(self):
        return Base.GlobalId("{985f4422-143a-46b5-828e-7671ffcc0d06}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("CompoundElem", "OpenLxApp.Element")
        
        # Register properties 
        self.setPropertyHeader(lxstr("CompoundElem"), -1)
        self.setPropertyGroupName(lxstr("Compound Parameter"), -1)
        self.length        = self._registerPropertyDouble_Length()
        self.width         = self._registerPropertyDouble_Width()
        self.height        = self._registerPropertyDouble_Height()
        self.lengthCnt     = self._registerPropertyInteger_LengthCnt()
        self.widthCnt      = self._registerPropertyInteger_WidthCnt()
        self.heightCnt     = self._registerPropertyInteger_HeightCnt()
        self.bool1         = self._registerPropertyBool_Default()
        self.bool2         = self._registerPropertyBool_Lockbutton()
        self.colors        = self._registerPropertyEnum_Colors()
        self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())
        
        
    def _registerPropertyDouble_Length(self):
        p = self.registerPropertyDouble("Length", 1.0)
        p.setVisible(True)
        p.setEditable(True)
        p.setTranslationId(-1)
        p.setMinValue(.1)
        p.setMaxValue(1.E06)
        p.setSteps(.1)
        return p
        
    def _registerPropertyDouble_Width(self):
        p = self.registerPropertyDouble("Width", 1.0)
        p.setVisible(True)
        p.setEditable(True)
        p.setTranslationId(-1)
        p.setMinValue(.1)
        p.setMaxValue(1.E06)
        p.setSteps(.1)
        return p
        
    def _registerPropertyDouble_Height(self):
        p = self.registerPropertyDouble("Height", 1.0)
        p.setVisible(True)
        p.setEditable(True)
        p.setTranslationId(-1)
        p.setMinValue(.1)
        p.setMaxValue(1.E06)
        p.setSteps(.1)
        return p
        
    def _registerPropertyInteger_LengthCnt(self):
        p = self.registerPropertyInteger("Length Sect.", 5)
        p.setVisible(True)
        p.setEditable(True)
        p.setTranslationId(-1)
        p.setMinValue(1)
        p.setMaxValue(10)
        p.setSteps(1)
        return p
        
    def _registerPropertyInteger_WidthCnt(self):
        p = self.registerPropertyInteger("Width Sect.", 5)
        p.setVisible(True)
        p.setEditable(True)
        p.setTranslationId(-1)
        p.setMinValue(1)
        p.setMaxValue(10)
        p.setSteps(1)
        return p
        
    def _registerPropertyInteger_HeightCnt(self):
        p = self.registerPropertyInteger("Height Sect.", 5)
        p.setVisible(True)
        p.setEditable(True)
        p.setTranslationId(-1)
        p.setMinValue(1)
        p.setMaxValue(10)
        p.setSteps(1)
        return p
        
    def _registerPropertyBool_Default(self):
        p = self.registerPropertyBool("Bool1", True)
        p.setVisible(True)
        p.setEditable(True)
        p.setStyle(lx.PropertyBool.DEFAULT)
        p.setTranslationId(-1)
        return p
        
    def _registerPropertyBool_Lockbutton(self):
        p = self.registerPropertyBool("Bool3", True)
        p.setVisible(True)
        p.setEditable(True)
        p.setStyle(lx.PropertyBool.LOCKBUTTON)
        p.setTranslationId(-1)
        return p
        
    def _registerPropertyEnum_Colors(self):
        p = self.registerPropertyEnum("Colors", 0)
        p.setVisible(True)
        p.setEditable(True)
        p.setTranslationId(-1)
        p.setEmpty()        
        p.addEntry(lxstr("Single Color"),-1)    # 0
        p.addEntry(lxstr("Two Colors"),-1)      # 1
        p.addEntry(lxstr("Random Colors"),-1)   # 2
        return p

    def buildSubElem(self, aLength, aWidth, aHeight):
        se = lx.SubElement.createIn(doc)
        b = lx.Block.createIn(doc)
        b.setXLength(aLength)
        b.setYLength(aWidth)
        b.setZLength(aHeight)
        se.setGeometry(b)
        return se
      
    def createCompound(self):
        print("Colors Enum: ", self.colors.getValue())
        res = Geom.Precision.linear_Resolution()
        length = self.length.getValue()
        width  = self.width.getValue()
        height = self.height.getValue()
        lCnt   = float(self.lengthCnt.getValue())
        wCnt   = float(self.widthCnt.getValue())
        hCnt   = float(self.heightCnt.getValue())
        if width <= res or height <= res or length <= res or lCnt<1. or wCnt<1. or hCnt<1.:
            return False
        # Build the SubElements        
        for i in range(self.lengthCnt.getValue()):
            for j in range(self.widthCnt.getValue()):
                for k in range(self.heightCnt.getValue()):
                    se = self.buildSubElem(length/lCnt, width/wCnt, height/hCnt)
                    se.translate(Geom.Vec(i*length/lCnt,j*width/wCnt,k*height/hCnt))
                    if self.colors.getValue() == 1 and i%2 == 0: 
                        # "Two Colors" Enum
                        se.setDiffuseColor(Base.Color(255,0,0))
                    elif self.colors.getValue() == 2:
                        # "Random Colors" Enum
                        se.setDiffuseColor(Base.Color(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
                    self.addSubElement(se)
            
    def onPropertyChanged(self, aPropertyName):
        doc.beginEditing()
        self.removeSubElements()
        self.createCompound()       
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
    doc.registerPythonScript(Base.GlobalId("{f955fac7-4935-441d-ac1d-367f80dd053d}"))
    
    comp = CompoundElem(doc)
        
    # Begin editing of the Element
    doc.beginEditing()
    comp.length.setValue(1.)
    comp.width.setValue(1.)
    comp.height.setValue(1.)
    comp.createCompound()
    # End editing of the Element
    doc.endEditing()
    doc.recompute()  
