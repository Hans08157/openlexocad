# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import traceback, math

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

def qstr(str):
   return Base.StringTool.toQString(lxstr(str))
#Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))

def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))

class EditMode:
    def __init__(self, doc):
        if doc is None:
            raise RuntimeError("Document is None.")

        self._doc = doc
        self._exitEditing = False

    def __enter__(self):
        if not self._doc.isEditing():
            self._doc.beginEditing()
            self._exitEditing = True
        else:
            self._exitEditing = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._exitEditing:
            self._doc.endEditing()
            self._doc.recompute()

class Pergola(lx.Element):

    _color = Base.Color(255, 214, 0)

    def getGlobalClassId(self):
        return Base.GlobalId("{2b1f9edf-de7c-4de6-a13d-7ea149601a82}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Pergola", "OpenLxApp.Element")
        
        # Register properties 
        self.setPropertyHeader(lxstr("Pergola"), 35)
        self.setPropertyGroupName(lxstr("Pergola Parameter"), 36)
        self._length = self.registerPropertyDouble("Length", 6.0, lx.Property.VISIBLE, lx.Property.EDITABLE, 37)
        self._width = self.registerPropertyDouble("Width", 3.0, lx.Property.VISIBLE, lx.Property.EDITABLE, 38)
        self._height = self.registerPropertyDouble("Height", 2.5, lx.Property.VISIBLE, lx.Property.EDITABLE, 39)
        self._numCol = self.registerPropertyInteger("Number Column", 3, lx.Property.VISIBLE, lx.Property.EDITABLE, 40)
        self._sectCol = self.registerPropertyDouble("Section Column", 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, 41)
        self._widthBeam = self.registerPropertyDouble("Width Beam", 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, 42)
        self._heightBeam = self.registerPropertyDouble("Height Beam", 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, 43)
        self._widthStrut = self.registerPropertyDouble("Width Strut", 0.075, lx.Property.VISIBLE, lx.Property.EDITABLE, 44)
        self._heightStrut = self.registerPropertyDouble("Height Strut", 0.15, lx.Property.VISIBLE, lx.Property.EDITABLE, 45)
        self._numJoist = self.registerPropertyInteger("Number Joist", 12, lx.Property.VISIBLE, lx.Property.EDITABLE, 46)
        self._distJoist = self.registerPropertyDouble("Joist Distance", 0.536, lx.Property.VISIBLE, lx.Property.NOT_EDITABLE, 47)
        self._widthJoist = self.registerPropertyDouble("Width Joist", 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, 48)
        self._heightJoist = self.registerPropertyDouble("Height Joist", 0.175, lx.Property.VISIBLE, lx.Property.EDITABLE, 49)
        self._numCol.setMinValue(2)
        self._numJoist.setMinValue(2)
        self._setAllSteps()

        self._updateGeometry()

        
        
    def _setAllSteps(self):
        self._length.setSteps(0.1)
        self._width.setSteps(0.1)
        self._height.setSteps(0.1)
        self._sectCol.setSteps(0.01)
        self._widthBeam.setSteps(0.01)
        self._heightBeam.setSteps(0.01)
        self._widthStrut.setSteps(0.01)
        self._heightStrut.setSteps(0.01)
        self._widthJoist.setSteps(0.01)
        self._heightJoist.setSteps(0.01)


    @staticmethod
    def _createSubElement(listPoint, heightStep, dir):
        face = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(face, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)
        return subElem

    @staticmethod
    def _createExtrudedGeom(listPoint, heightStep, dir):
        face = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(face, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        return geom

    def _createColumns(self):
        length = self._length.getValue()
        width  = self._width.getValue()
        height = self._height.getValue()
        numCol = self._numCol.getValue()
        sectCol = self._sectCol.getValue()
        widthBeam =  self._widthBeam.getValue()
        heightBeam = self._heightBeam.getValue()
        heightJoist = self._heightJoist.getValue()
        pnt1 = Geom.Pnt( width, 0, 0)
        pnt2 = Geom.Pnt( width, 0, height - heightJoist - heightBeam)
        pnt3 = Geom.Pnt( width - widthBeam, 0, height - heightJoist - heightBeam)
        pnt4 = Geom.Pnt( width - widthBeam, 0, height - heightJoist)
        pnt5 = Geom.Pnt( width - sectCol, 0, height - heightJoist)
        pnt6 = Geom.Pnt( width - sectCol, 0, 0)
        dir = Geom.Dir(0.0, 1.0, 0.0)
        firstCol = self._createSubElement([pnt1, pnt2, pnt3, pnt4, pnt5, pnt6], sectCol, dir)
        firstCol.setDiffuseColor(self._color)
        self.addSubElement(firstCol)
        step = (length - sectCol) / (numCol-1)
        for i in range(1, numCol):
            geom = self._createExtrudedGeom([pnt1, pnt2, pnt3, pnt4, pnt5, pnt6], sectCol, dir)
            secondCol = lx.SubElement.createIn(doc)
            secondCol.setGeometry(geom)
            secondCol.translate(Geom.Vec(0, step * i, 0))
            secondCol.setDiffuseColor(self._color)
            self.addSubElement(secondCol)


    def _createBeams(self):
        length = self._length.getValue()
        width  = self._width.getValue()
        height = self._height.getValue()
        widthBeam =  self._widthBeam.getValue()
        heightBeam = self._heightBeam.getValue()
        heightJoist = self._heightJoist.getValue()
        pnt1 = Geom.Pnt( width, 0, height - heightJoist - heightBeam)
        pnt2 = Geom.Pnt( width, 0, height - heightJoist)
        pnt3 = Geom.Pnt( width - widthBeam, 0, height - heightJoist)
        pnt4 = Geom.Pnt( width - widthBeam, 0, height - heightJoist - heightBeam)
        dir = Geom.Dir(0.0, 1.0, 0.0)
        beam = self._createSubElement([pnt1, pnt2, pnt3, pnt4], length, dir)
        beam.setDiffuseColor(self._color)
        self.addSubElement(beam)

    def _createStruts(self):
        length = self._length.getValue()
        width = self._width.getValue()
        height = self._height.getValue()
        sectCol = self._sectCol.getValue()
        widthStrut = self._widthStrut.getValue()
        heightStrut = self._heightStrut.getValue()
        heightJoist = self._heightJoist.getValue()
        pnt1 = Geom.Pnt(width - sectCol, 0, height - heightJoist - 1.0)
        pnt2 = Geom.Pnt(width - sectCol, 0, height - heightJoist - 1.0 + heightStrut*math.sqrt(2.))
        pnt3 = Geom.Pnt(width - sectCol - 1.0 +heightStrut*math.sqrt(2.), 0, height - heightJoist)
        pnt4 = Geom.Pnt(width - sectCol - 1.0, 0, height - heightJoist)
        dir = Geom.Dir(0.0, 1.0, 0.0)
        firstStrut = self._createSubElement([pnt1, pnt2, pnt3, pnt4], widthStrut, dir)
        firstStrut.setDiffuseColor(self._color)
        self.addSubElement(firstStrut)
        geom = self._createExtrudedGeom([pnt1, pnt2, pnt3, pnt4], widthStrut, dir)
        secondStrut = lx.SubElement.createIn(doc)
        secondStrut.setGeometry(geom)
        secondStrut.translate(Geom.Vec(0, length - widthStrut, 0))
        secondStrut.setDiffuseColor(self._color)
        self.addSubElement(secondStrut)


    def _createJoits(self):
        length = self._length.getValue()
        width = self._width.getValue()
        height = self._height.getValue()
        numJoist = self._numJoist.getValue()
        widthJoist = self._widthJoist.getValue()
        heightJoist = self._heightJoist.getValue()
        pnt1 = Geom.Pnt(width, 0, height - heightJoist)
        pnt2 = Geom.Pnt(width, 0, height)
        pnt3 = Geom.Pnt(0, 0, height)
        pnt4 = Geom.Pnt(0, 0, height - heightJoist)
        dir = Geom.Dir(0.0, 1.0, 0.0)
        firstJoist = self._createSubElement([pnt1, pnt2, pnt3, pnt4], widthJoist, dir)
        firstJoist.setDiffuseColor(self._color)
        self.addSubElement(firstJoist)
        step = (length - widthJoist)/(numJoist-1)
        for i in range(1, numJoist):
            geom = self._createExtrudedGeom([pnt1, pnt2, pnt3, pnt4], widthJoist, dir)
            secondJoist = lx.SubElement.createIn(doc)
            secondJoist.setGeometry(geom)
            secondJoist.translate(Geom.Vec(0, step * i, 0))
            secondJoist.setDiffuseColor(self._color)
            self.addSubElement(secondJoist)



    def createCompound(self):
        self._createColumns()
        self._createBeams()
        self._createStruts()
        self._createJoits()

    def setLength(self, p):
        minV1 = self._sectCol.getValue() * self._numCol.getValue()
        minV2 = self._widthJoist.getValue() * self._numJoist.getValue()
        minV = minV1 * (minV1 > minV2) + minV2 * (minV1 <= minV2)
        with EditMode(self.getDocument()):
            self._length.setValue(clamp(p, minV, 1e04))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def setWidth(self, p):
        minV = self._sectCol.getValue()+1.05
        with EditMode(self.getDocument()):
            self._width.setValue(clamp(p, minV, 1e04))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def setHeight(self, p):
        minV = self._heightJoist.getValue()+1.05
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(p, minV, 1e04))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def setNumCol(self, p):
        minV = self._numCol.getMinValue()
        maxV = int(self._length.getValue() // self._sectCol.getValue())
        #print(maxV)
        with EditMode(self.getDocument()):
            self._numCol.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setSectCol(self, p):
        minV = self._widthBeam.getMinValue() + 0.01
        maxV1 = self._width.getValue() - 1.01
        maxV2 = self._length.getValue() / self._numCol.getValue() - 0.01
        maxV = maxV1 * (maxV1 < maxV2) + maxV2 * (maxV1 >= maxV2)
        with EditMode(self.getDocument()):
            self._sectCol.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setWidthBeam(self, p):
        maxV = self._sectCol.getValue() - 0.01
        with EditMode(self.getDocument()):
            self._widthBeam.setValue(clamp(p, 0.01, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setHeightBeam(self, p):
        maxV = 0.98
        with EditMode(self.getDocument()):
            self._heightBeam.setValue(clamp(p, 0.01, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setWidthStrut(self, p):
        maxV = self._widthJoist.getValue() - 0.01
        with EditMode(self.getDocument()):
            self._widthStrut.setValue(clamp(p, 0.01, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setHeightStrut(self, p):
        maxV = 1.0 / math.sqrt(2.) - 0.01
        with EditMode(self.getDocument()):
            self._heightStrut.setValue(clamp(p, 0.01, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setNumJoist(self, p):
        minV = self._numJoist.getMinValue()
        maxV = int(self._length.getValue() // self._widthJoist.getValue())
        with EditMode(self.getDocument()):
            self._numJoist.setValue(clamp(p, minV, maxV))
            self._distJoist.setValue((self._length.getValue() - self._widthJoist.getValue())/(p-1))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setWidthJoist(self, p):
        maxV = self._length.getValue() / self._numJoist.getValue() - 0.01
        print(maxV)
        with EditMode(self.getDocument()):
            self._widthJoist.setValue(clamp(p, 0.01, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setHeightJoist(self, p):
        maxV = self._height.getValue() - 1.01
        with EditMode(self.getDocument()):
            self._heightJoist.setValue(clamp(p, 0.01, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))



    def _updateGeometry(self):
        doc = self.getDocument()
        with EditMode(doc):
            self.removeSubElements()
            self.createCompound()
            #self.setDiffuseColor(Base.Color(255, 214, 0))

    def onPropertyChanged(self, aPropertyName):
        #doc.beginEditing()
        if aPropertyName == "Length":
            self.setLength(self._length.getValue())
        elif aPropertyName == "Width":
            self.setWidth(self._width.getValue())
        elif aPropertyName == "Height":
            self.setHeight(self._height.getValue())
        elif aPropertyName == "Number Column":
            self.setNumCol(self._numCol.getValue())
        elif aPropertyName == "Section Column":
            self.setSectCol(self._sectCol.getValue())
        elif aPropertyName == "Width Beam":
            self.setWidthBeam(self._widthBeam.getValue())
        elif aPropertyName == "Height Beam":
            self.setHeightBeam(self._heightBeam.getValue())
        elif aPropertyName == "Width Strut":
            self.setWidthStrut(self._widthStrut.getValue())
        elif aPropertyName == "Height Strut":
            self.setHeightStrut(self._heightStrut.getValue())
        elif aPropertyName == "Number Joist":
            self.setNumJoist(self._numJoist.getValue())
        elif aPropertyName == "Width Joist":
            self.setWidthJoist(self._widthJoist.getValue())
        elif aPropertyName == "Height Joist":
            self.setHeightJoist(self._heightJoist.getValue())
        else:
            pass
        self._updateGeometry()


    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(self.getDocument()):
            if not Geom.GeomTools.isEqual(x, 1.):
                print("Scaling in X")
                old = self._width.getValue()
                self.setWidth(old * x)
            if not Geom.GeomTools.isEqual(y, 1.):
                print("Scaling in Y")
                old = self._length.getValue()
                self.setLength(old * y)
            if not Geom.GeomTools.isEqual(z, 1.):
                print("Scaling in Z")
                old = self._height.getValue()
                self.setHeight(old * z)

            self.translateAfterScaled(aVec, aScaleBasePnt)

    
if __name__ == "__main__":    
    doc.registerPythonScript(Base.GlobalId("{d4d9ac16-ed37-4681-8008-d41cf47a0fdb}"))

    try:
        per = Pergola(doc)
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
            per.setLocalPlacement(pos)
    except Exception as e:
        print("{}".format(e))
        traceback.print_exc()
    finally:
        doc.recompute()

