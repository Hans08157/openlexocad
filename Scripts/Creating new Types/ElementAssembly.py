# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

    
class MyElementAssembly(lx.ElementAssembly):
    def getGlobalClassId(self):
        return Base.GlobalId("{096743D5-52F4-4873-B50B-790AAE6A6B75}")

    def __init__(self, aArg): 
        lx.ElementAssembly.__init__(self, aArg)
        self.registerPythonClass("MyElementAssembly", "OpenLxApp.ElementAssembly")
        # Register properties 
        self.setPropertyHeader(lxstr("MyElementAssembly"), -1)
        self.setPropertyGroupName(lxstr("Assembly Parameter"), -1)
        self.length = self.registerPropertyDouble("Length",   \
                                                   1.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
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
        self.beamWidth = self.registerPropertyDouble("Beam Width", \
                                                   0.1, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1) 
        self.nbBeams = self.registerPropertyInteger("Number of Beams", \
                                                   3, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())
      
    def addBeams(self):
        print("addBeams")
        res = Geom.Precision.linear_Resolution()
        length = self.length.getValue()
        width  = self.width.getValue()
        height = self.height.getValue()
        beamWidth = self.beamWidth.getValue()
        nbBeams = self.nbBeams.getValue()
        if width <= res or height <= res or length <= res or nbBeams < 2:
            print("Error1")
            return False
        if nbBeams*beamWidth > width:
            print("Error2")
            print(nbBeams * beamWidth)
            return False
        # Build the Beams
        delta = (width-beamWidth) / (nbBeams-1)
        for i in range(nbBeams):
            beam = lx.Beam.buildFrom2Points(doc, .1, .2, Geom.Pnt(0,0,0), Geom.Pnt(length,0,0))
            beam.setPlacementRelativeTo(self)
            beam.translate(Geom.Vec(0, i*delta, 0))
            self.addToAssembly(lx.castToElement(beam))

            
    def removeBeams(self):
        print("removeBeams")
        beams = self.getAssembledElements()
        for b in beams:
            self.removeFromAssembly(b)
            doc.removeObject(b)
            
    def onPropertyChanged(self, aPropertyName):
        """
        Is called when a Property has changed.
        """   
        doc.beginEditing()        
        self.removeBeams()
        block = self.addBeams()
        doc.endEditing()
        doc.recompute()      

    
if __name__ == "__main__":   
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{D0672BB6-E849-40F5-B51F-1AA188EF3281}"))
    
    assembly = MyElementAssembly(doc)
    
    # Begin editing of the Element
    doc.beginEditing()
    assembly.setUserName(lxstr("Test Assembly"))
    assembly.length.setValue(1.)
    assembly.width.setValue(1.)
    assembly.height.setValue(1.)
    assembly.addBeams()
    
    thisScript = lx.Application.getInstance().getActiveScript()
    if thisScript.isDragAndDropped():
        pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0,0,1))
    else:
        pos = Geom.Ax2(Geom.Pnt(0,0,0), Geom.Dir(0,0,1))
        
    assembly.setLocalPlacement(pos)
    # End editing of the Element
    doc.endEditing()
    doc.recompute()   
    