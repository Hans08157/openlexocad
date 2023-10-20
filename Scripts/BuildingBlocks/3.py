# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString
epsilon = 0.0001
doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))

class Dormer1Elem(lx.Element):
    def getGlobalClassId(self):
        return Base.GlobalId("{0BB77184-EE5D-46E0-83F4-FC9318EEDB72}")

    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Dormer1Elem", "OpenLxApp.Element")
        # Register properties 
        self.setPropertyHeader(lxstr("Dormer1"), -1)
        self.setPropertyGroupName(lxstr("Dormer1 parameter"), -1)

        self._length = self.registerPropertyDouble("Length", \
                                                   4.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self._width = self.registerPropertyDouble("Width", \
                                                  4.0, \
                                                  lx.Property.VISIBLE, \
                                                  lx.Property.EDITABLE, \
                                                  -1)
        self._height = self.registerPropertyDouble("Height", \
                                                   4.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)

        self._topHeight = self.registerPropertyDouble("Top", \
                                                      1.0, \
                                                      lx.Property.VISIBLE, \
                                                      lx.Property.EDITABLE, \
                                                      -1)

        self._offset1 = self.registerPropertyDouble("Side", \
                                                    1.0, \
                                                    lx.Property.VISIBLE, \
                                                    lx.Property.EDITABLE, \
                                                    -1)

        self._offset2 = self.registerPropertyDouble("Front", \
                                                    1.0, \
                                                    lx.Property.VISIBLE, \
                                                    lx.Property.EDITABLE, \
                                                    -1)

        
        self._updateGeometry()

    def setLength(self, length):
        self._length.setValue(clamp(length, self._offset2.getValue(), 10000.0))
        self._updateGeometry()

    def length(self):
        return self._length.getValue()

    def setWidth(self, width):
        self._width.setValue(clamp(width, self._offset1.getValue() * 2.0, 10000.0))
        self._updateGeometry()

    def width(self):
        return self._width.getValue()

    def setHeight(self, height):
        self._height.setValue(clamp(height, self._topHeight.getValue(), 10000.0))
        self._updateGeometry()

    def height(self):
        return self._height.getValue()

    def setTopHeight(self, topHeight):
        self._topHeight.setValue(clamp(topHeight, 0.001, 10000.0))
        self._updateGeometry()

    def topHeight(self):
        return self._topHeight.getValue()

    def setOffset1(self, offset1):
        self._offset1.setValue(clamp(offset1, 0.001, self._width.getValue() * 0.5 - epsilon))
        self._updateGeometry()

    def offset1(self):
        return self._topHeight.getValue()

    def setOffset2(self, offset2):
        self._offset2.setValue(clamp(offset2, 0.001, self._length.getValue()))
        self._updateGeometry()

    def offset2(self):
        return self._offset2.getValue()

    def createDormer1(self, doc):

        # Build the geometry
        l = self._length.getValue()
        w = self._width.getValue()
        h = self._height.getValue()
        td = self._topHeight.getValue()
        off1 = self._offset1.getValue()
        off2 = self._offset2.getValue()

        vtxList = []
        indexList = []

        if off1 < epsilon:
            off1 = 0.00001

        f = (off1 * td) / (w * 0.5)

        ch = (td * ((w * 0.5) - off1)) / (w * 0.5)

        vtxList.append(Geom.Pnt(off2, off1, 0.0))
        vtxList.append(Geom.Pnt(off2, w - off1, 0.0))

        vtxList.append(Geom.Pnt(off2, off1, h - td - f))
        vtxList.append(Geom.Pnt(off2, w - off1, h - td - f))
        vtxList.append(Geom.Pnt(l, w - off1, h - td - f))
        vtxList.append(Geom.Pnt(l, off1, h - td - f))

        vtxList.append(Geom.Pnt(0.0, 0.0, h - td))
        vtxList.append(Geom.Pnt(0.0, w, h - td))
        vtxList.append(Geom.Pnt(l, w, h - td))
        vtxList.append(Geom.Pnt(l, 0.0, h - td))

        vtxList.append(Geom.Pnt(0.0, w * 0.5, h))
        vtxList.append(Geom.Pnt(l, w * 0.5, h))

        vtxList.append(Geom.Pnt(off2, w * 0.5, h - td - f + ch))

        def createFaceWithFourPnt(d, c, b, a):
            indexList.append(a)
            indexList.append(b)
            indexList.append(c)
            indexList.append(d)
            indexList.append(-2)
            indexList.append(-1)

        def createFaceWithFifePnt(e, d, c, b, a):
            indexList.append(a)
            indexList.append(b)
            indexList.append(c)
            indexList.append(d)
            indexList.append(e)
            indexList.append(-2)
            indexList.append(-1)

        def createFaceWithThreePnt(c, b, a):
            indexList.append(a)
            indexList.append(b)
            indexList.append(c)
            indexList.append(-2)
            indexList.append(-1)

        createFaceWithThreePnt(1, 4, 3)
        createFaceWithFourPnt(3, 4, 8, 7)
        createFaceWithFourPnt(7, 8, 11, 10)
        createFaceWithFourPnt(11, 9, 6, 10)
        createFaceWithFourPnt(2, 6, 9, 5)
        createFaceWithThreePnt(0, 2, 5)
        createFaceWithFourPnt(2, 12, 10, 6)
        createFaceWithFourPnt(3, 7, 10, 12)
        createFaceWithFifePnt(3, 12, 2, 0, 1)

        geom = lx.FacetedBrep.createIn(doc)
        geom.setPoints(vtxList)
        geom.setModel(indexList)

        return geom
    
    def modifyElem(self):
        block = self.createDormer1(doc)
        if block:
            self.setGeometry(block)

    def _updateGeometry(self):

        geom = self.createDormer1(doc)
        self.setGeometry(geom)

        doc.endEditing()
        doc.recompute()

    def onPropertyChanged(self, aPropertyName):

        doc = self.getDocument()
        doc.beginEditing()

        if aPropertyName == "Length":
            self.setLength(self._length.getValue())
        elif aPropertyName == "Width":
            self.setWidth(self._width.getValue())
        elif aPropertyName == "Height":
            self.setHeight(self._height.getValue())
        elif aPropertyName == "Top":
            self.setTopHeight(self._topHeight.getValue())
        elif aPropertyName == "Side":
            self.setOffset1(self._offset1.getValue())
        elif aPropertyName == "Front":
            self.setOffset2(self._offset2.getValue())
        
    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        doc.beginEditing()
        if not Geom.GeomTools.isEqual(x, 1.):
            old = self._length.getValue()
            self._length.setValue(old*x)
            self.modifyElem()      
        if not Geom.GeomTools.isEqual(y, 1.):
            old = self._width.getValue()
            self._width.setValue(old*y)
            self.modifyElem() 
        if not Geom.GeomTools.isEqual(z, 1.):
            old = self._height.getValue()
            self._height.setValue(old*z)
            self.modifyElem()
            
        self.translateAfterScaled(aVec, aScaleBasePnt)
        doc.endEditing()
        doc.recompute()
    
if __name__ == "__main__":   
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{25DDB135-4D14-4CC8-85AA-56D9819E69E7}"))
    
    dormer1Elem = Dormer1Elem(doc)
    
    # Begin editing of the Element
    doc.beginEditing()

    b = dormer1Elem.createDormer1(doc)
    dormer1Elem.setGeometry(b)

    thisScript = lx.Application.getInstance().getActiveScript()
    if thisScript.isDragAndDropped():
        pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
    else:
        pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

    dormer1Elem.setLocalPlacement(pos)

    # End editing of the Element
    doc.endEditing()
    doc.recompute()