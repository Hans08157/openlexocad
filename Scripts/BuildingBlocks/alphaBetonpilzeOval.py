# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import math

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()
epsilon = 0.0001

def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))

def qstr(str):
   return Base.StringTool.toQString(lxstr(str))
#Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))

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


class AlphaBetonpilzeOval(lx.Column):
    _AParamName = "l upper part"
    _BParamName = "w upper part"
    _aParamName = "l lower part"
    _bParamName = "w lower part"
    _aColumnParamName = "l column"
    _bColumnParamName = "w column"
    _hkPropName = "h collar"
    _vPropName = "h bevel"
    _heightPropName = "h column"
    _totalHeightPropName = "h total"

    def getGlobalClassId(self):
        return Base.GlobalId("{6748843F-F8EE-4D0B-92B1-806F9DF67A60}")

    def __init__(self, aArg):
        lx.Column.__init__(self, aArg)
        self.setPredefinedType(lx.Column.ColumnTypeEnum_COLUMN)
        self.registerPythonClass("AlphaBetonpilzeOval", "OpenLxApp.Column")
        # Register properties
        self.setPropertyHeader(lxstr("Column head Oval"), -1)
        self.setPropertyGroupName(lxstr("Column head Oval Parameter"), -1)

        self._A = self.registerPropertyDouble(self._AParamName, 0.5, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._B = self.registerPropertyDouble(self._BParamName, 0.7, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._a = self.registerPropertyDouble(self._aParamName, 0.35, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._b = self.registerPropertyDouble(self._bParamName, 0.55, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._aColumn = self.registerPropertyDouble(self._aColumnParamName, 0.21, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._bColumn = self.registerPropertyDouble(self._bColumnParamName, 0.33, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._Hk = self.registerPropertyDouble(self._hkPropName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._v = self.registerPropertyDouble(self._vPropName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._height = self.registerPropertyDouble(self._heightPropName, 2.7, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._totalHeight = self.registerPropertyDouble(self._totalHeightPropName, 3.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._A.setSteps(0.01)
        self._B.setSteps(0.01)
        self._a.setSteps(0.01)
        self._b.setSteps(0.01)
        self._aColumn.setSteps(0.01)
        self._bColumn.setSteps(0.01)
        self._Hk.setSteps(0.01)
        self._v.setSteps(0.01)
        self._height.setSteps(0.01)
        self._totalHeight.setSteps(0.01)

        

        self._updateGeometry()

    def setA(self, A):
        with EditMode(self.getDocument()):
            self._A.setValue(clamp(A, self.minA(), self.maxA()))
            self._updateGeometry()
        if A < self.minA():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif A > self.maxA():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def minA(self):
        return epsilon

    def maxA(self):
        return self._B.getValue() - epsilon

    def setB(self, B):
        with EditMode(self.getDocument()):
            self._B.setValue(clamp(B, self.minB(), self.maxB()))
            self._updateGeometry()
        if B < self.minB():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif B > self.maxB():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def minB(self):
        return self._A.getValue() + epsilon

    def maxB(self):
        return 1000.0

    def seta(self, a):
        with EditMode(self.getDocument()):
            self._a.setValue(clamp(a, self.mina(), self.maxa()))
            self._updateGeometry()
        if a < self.mina():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif a > self.maxa():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def mina(self):
        return epsilon

    def maxa(self):
        return self._b.getValue() - epsilon

    def setb(self, b):
        with EditMode(self.getDocument()):
            self._b.setValue(clamp(b, self.minb(), self.maxb()))
            self._updateGeometry()
        if b < self.minb():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif b > self.maxb():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def minb(self):
        return self._a.getValue() + epsilon

    def maxb(self):
        return 1000.0

    def setaColumn(self, aColumn):
        with EditMode(self.getDocument()):
            self._aColumn.setValue(clamp(aColumn, self.minaColumn(), self.maxaColumn()))
            self._updateGeometry()
        if aColumn < self.minaColumn():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif aColumn > self.maxaColumn():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def minaColumn(self):
        return epsilon

    def maxaColumn(self):
        return self._bColumn.getValue() - epsilon

    def setbColumn(self, bColumn):
        with EditMode(self.getDocument()):
            self._bColumn.setValue(clamp(bColumn, self.minbColumn(), self.maxbColumn()))
            self._updateGeometry()
        if bColumn < self.minbColumn():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif bColumn > self.maxbColumn():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def minbColumn(self):
        return self._aColumn.getValue() + epsilon

    def maxbColumn(self):
        return 1000.0


    def setHk(self, Hk):
        with EditMode(self.getDocument()):
            self._Hk.setValue(clamp(Hk, self.minHk(), self.maxHk()))
            self._totalHeight.setValue((self._Hk.getValue() * 2.0) + self._height.getValue() + self._v.getValue())
            self._updateGeometry()
        if Hk < self.minHk():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif Hk > self.maxHk():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def minHk(self):
        return epsilon

    def maxHk(self):
        return (self._totalHeight.getValue() - self._v.getValue()) * 0.5

    def setV(self, v):
        with EditMode(self.getDocument()):
            self._v.setValue(clamp(v, self.minV(), self.maxV()))
            self._totalHeight.setValue((self._Hk.getValue() * 2.0) + self._height.getValue() + self._v.getValue())
            self._updateGeometry()
        if v < self.minV():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif v > self.maxV():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def minV(self):
        return epsilon

    def maxV(self):
        return self._totalHeight.getValue() - (self._Hk.getValue() * 2.0)

    def setHeight(self, height):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(height, self.minHeight(), self.maxHeight()))
            self._totalHeight.setValue((self._Hk.getValue() * 2.0) + height + self._v.getValue())
            self._updateGeometry()
        if height < self.minHeight():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif height > self.maxHeight():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def minHeight(self):
        return epsilon

    def maxHeight(self):
        return 1000.0

    def setTotalHeight(self, totalHeight):
        with EditMode(self.getDocument()):
            self._totalHeight.setValue(clamp(totalHeight, self.minTotalHeight(), self.maxTotalHeight()))
            self._height.setValue(totalHeight - self._v.getValue() - (self._Hk.getValue() * 2.0))
            self._updateGeometry()
        if totalHeight < self.minTotalHeight():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif totalHeight > self.maxTotalHeight():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def minTotalHeight(self):
        return self._v.getValue() + (self._Hk.getValue() * 2.0) + epsilon

    def maxTotalHeight(self):
        return 1000.0


    def addEdgeFace(self, face):
        geom = lx.createCurveBoundedPlaneFromFace(doc, face)
        topCoverElem = lx.SubElement.createIn(doc)
        topCoverElem.setGeometry(geom)
        self.addSubElement(topCoverElem)

    @staticmethod
    def _createSubElement(listPoint, heightStep, dir):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)
        return subElem

    def createCompound(self):
        A = self._A.getValue()
        B = self._B.getValue()
        a = self._a.getValue()
        b = self._b.getValue()
        aColumn = self._aColumn.getValue()
        bColumn = self._bColumn.getValue()

        hk = self._Hk.getValue()
        h = self._totalHeight.getValue()
        v = self._v.getValue()

        A2 = A * 0.5
        B2 = B * 0.5
        a2 = a * 0.5
        b2 = b * 0.5
        a2Column = aColumn * 0.5
        b2Column = bColumn * 0.5

        pnt0 = Geom.Pnt(0.0, -B2, h - hk)
        pnt1 = Geom.Pnt(A2, -B2 + A2, h - hk)
        pnt2 = Geom.Pnt(A2, B2 - A2, h - hk)
        pnt3 = Geom.Pnt(0.0, B2, h - hk)
        pnt4 = Geom.Pnt(-A2, B2 - A2, h - hk)
        pnt5 = Geom.Pnt(-A2, -B2 + A2, h - hk)

        pnt6 = Geom.Pnt(0.0, -b2, h - hk - v)
        pnt7 = Geom.Pnt(a2, -b2 + a2, h - hk - v)
        pnt8 = Geom.Pnt(a2, b2 - a2, h - hk - v)
        pnt9 = Geom.Pnt(0.0, b2, h - hk - v)
        pnt10 = Geom.Pnt(-a2, b2 - a2, h - hk - v)
        pnt11 = Geom.Pnt(-a2, a2 - b2, h - hk - v)

        listFace = Topo.vector_Face(6)

        #smooth
        #left
        edgeListLeftSmooth = Topo.vector_Edge(4)
        edgeListLeftSmooth[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt0, pnt1)
        edgeListLeftSmooth[1] = Topo.EdgeTool.makeEdge(pnt1, pnt7)
        edgeListLeftSmooth[2] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt6, pnt11)
        edgeListLeftSmooth[3] = Topo.EdgeTool.makeEdge(pnt11, pnt5)
        leftSmoothWire = Topo.WireTool.makeWire(edgeListLeftSmooth, Geom.Precision.linear_Resolution())
        leftSmoothFace = Topo.FaceTool.makeFace(leftSmoothWire, Geom.Precision.linear_Resolution())
        listFace[0] = leftSmoothFace

        #right
        edgeListRightSmooth = Topo.vector_Edge(4)
        edgeListRightSmooth[0] = Topo.EdgeTool.makeArcOfCircle(pnt2, pnt3, pnt4)
        edgeListRightSmooth[1] = Topo.EdgeTool.makeEdge(pnt4, pnt10)
        edgeListRightSmooth[2] = Topo.EdgeTool.makeArcOfCircle(pnt10, pnt9, pnt8)
        edgeListRightSmooth[3] = Topo.EdgeTool.makeEdge(pnt8, pnt2)
        rightSmoothWire = Topo.WireTool.makeWire(edgeListRightSmooth, Geom.Precision.linear_Resolution())
        rightSmoothFace = Topo.FaceTool.makeFace(rightSmoothWire, Geom.Precision.linear_Resolution())
        listFace[1] = rightSmoothFace

        #top
        edgeListTop = Topo.vector_Edge(4)
        edgeListTop[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt0, pnt1)
        edgeListTop[1] = Topo.EdgeTool.makeEdge(pnt1, pnt2)
        edgeListTop[2] = Topo.EdgeTool.makeArcOfCircle(pnt2, pnt3, pnt4)
        edgeListTop[3] = Topo.EdgeTool.makeEdge(pnt4, pnt5)
        topWire = Topo.WireTool.makeWire(edgeListTop, Geom.Precision.linear_Resolution())
        topFace = Topo.FaceTool.makeFace(topWire, Geom.Precision.linear_Resolution())
        listFace[2] = topFace

        # bot
        edgeListBack = Topo.vector_Edge(4)
        edgeListBack[0] = Topo.EdgeTool.makeArcOfCircle(pnt11, pnt6, pnt7)
        edgeListBack[1] = Topo.EdgeTool.makeEdge(pnt7, pnt8)
        edgeListBack[2] = Topo.EdgeTool.makeArcOfCircle(pnt8, pnt9, pnt10)
        edgeListBack[3] = Topo.EdgeTool.makeEdge(pnt10, pnt11)
        backWire = Topo.WireTool.makeWire(edgeListBack, Geom.Precision.linear_Resolution())
        backFace = Topo.FaceTool.makeFace(backWire, Geom.Precision.linear_Resolution())
        listFace[3] = backFace

        faceTopBeam = Topo.FaceTool.extrudedFace(topFace, Geom.Dir(0.0, 0.0, 1.0), hk)

        geomTopBeam = lx.AdvancedBrep.createIn(doc)
        geomTopBeam.setShape(faceTopBeam)
        topElem = lx.SubElement.createIn(doc)
        topElem.setGeometry(geomTopBeam)
        self.addSubElement(topElem)

        faceBottomBeam = Topo.FaceTool.extrudedFace(backFace, Geom.Dir(0.0, 0.0, -1.0), hk)
        geomBottomBeam = lx.AdvancedBrep.createIn(doc)
        geomBottomBeam.setShape(faceBottomBeam)
        bottomElem = lx.SubElement.createIn(doc)
        bottomElem.setGeometry(geomBottomBeam)
        self.addSubElement(bottomElem)

        #front
        edgeListFront = Topo.vector_Edge(4)
        edgeListFront[0] = Topo.EdgeTool.makeEdge(pnt2, pnt1)
        edgeListFront[1] = Topo.EdgeTool.makeEdge(pnt1, pnt7)
        edgeListFront[2] = Topo.EdgeTool.makeEdge(pnt7, pnt8)
        edgeListFront[3] = Topo.EdgeTool.makeEdge(pnt8, pnt2)
        frontWire = Topo.WireTool.makeWire(edgeListFront, Geom.Precision.linear_Resolution())
        frontFace = Topo.FaceTool.makeFace(frontWire, Geom.Precision.linear_Resolution())
        listFace[4] = frontFace

        #back
        edgeListBack = Topo.vector_Edge(4)
        edgeListBack[0] = Topo.EdgeTool.makeEdge(pnt5, pnt4)
        edgeListBack[1] = Topo.EdgeTool.makeEdge(pnt4, pnt10)
        edgeListBack[2] = Topo.EdgeTool.makeEdge(pnt10, pnt11)
        edgeListBack[3] = Topo.EdgeTool.makeEdge(pnt11, pnt5)
        backWire = Topo.WireTool.makeWire(edgeListBack, Geom.Precision.linear_Resolution())
        backFace = Topo.FaceTool.makeFace(backWire, Geom.Precision.linear_Resolution())
        listFace[5] = backFace

        listShape = Topo.ShapeTool.makeShape(listFace)

        geom = lx.AdvancedBrep.createIn(doc)
        geom.setShape(listShape)

        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(geom)
        self.addSubElement(elem)

        #column
        pnt6Column = Geom.Pnt(0.0, -b2Column, h - hk - v - hk)
        pnt7Column = Geom.Pnt(a2Column, -b2Column + a2Column, h - hk - v - hk)
        pnt8Column = Geom.Pnt(a2Column, b2Column - a2Column, h - hk - v - hk)
        pnt9Column = Geom.Pnt(0.0, b2Column, h - hk - v - hk)
        pnt10Column = Geom.Pnt(-a2Column, b2Column - a2Column, h - hk - v - hk)
        pnt11Column = Geom.Pnt(-a2Column, a2Column - b2Column, h - hk - v - hk)

        edgeListColumn = Topo.vector_Edge(4)
        edgeListColumn[0] = Topo.EdgeTool.makeArcOfCircle(pnt11Column, pnt6Column, pnt7Column)
        edgeListColumn[1] = Topo.EdgeTool.makeEdge(pnt7Column, pnt8Column)
        edgeListColumn[2] = Topo.EdgeTool.makeArcOfCircle(pnt8Column, pnt9Column, pnt10Column)
        edgeListColumn[3] = Topo.EdgeTool.makeEdge(pnt10Column, pnt11Column)
        columnWire = Topo.WireTool.makeWire(edgeListColumn, Geom.Precision.linear_Resolution())
        columnFace = Topo.FaceTool.makeFace(columnWire, Geom.Precision.linear_Resolution())

        faceColumn = Topo.FaceTool.extrudedFace(columnFace, Geom.Dir(0.0, 0.0, -1.0), h - hk - hk - v)
        geomColumn = lx.AdvancedBrep.createIn(doc)
        geomColumn.setShape(faceColumn)
        columnElem = lx.SubElement.createIn(doc)
        columnElem.setGeometry(geomColumn)
        self.addSubElement(columnElem)


    def _updateGeometry(self):

        doc = self.getDocument()
        with EditMode(doc):
            self.removeSubElements()
            self.createCompound()


    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == self._AParamName:
            self.setA(self._A.getValue())
        elif aPropertyName == self._BParamName:
            self.setB(self._B.getValue())
        elif aPropertyName == self._aParamName:
            self.seta(self._a.getValue())
        elif aPropertyName == self._bParamName:
            self.setb(self._b.getValue())
        elif aPropertyName == self._aColumnParamName:
            self.setaColumn(self._aColumn.getValue())
        elif aPropertyName == self._bColumnParamName:
            self.setbColumn(self._bColumn.getValue())
        elif aPropertyName == self._hkPropName:
            self.setHk(self._Hk.getValue())
        elif aPropertyName == self._vPropName:
            self.setV(self._v.getValue())
        elif aPropertyName == self._heightPropName:
            self.setHeight(self._height.getValue())
        elif aPropertyName == self._totalHeightPropName:
            self.setTotalHeight(self._totalHeight.getValue())

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        doc.beginEditing()
        if not Geom.GeomTools.isEqual(x, 1.):
            old = self._length.getValue()
            self._length.setValue(old * x)
            self.modifyElem()
        if not Geom.GeomTools.isEqual(y, 1.):
            old = self._width.getValue()
            self._width.setValue(old * y)
            self.modifyElem()
        if not Geom.GeomTools.isEqual(z, 1.):
            old = self._height.getValue()
            self._height.setValue(old * z)
            self.modifyElem()

        self.translateAfterScaled(aVec, aScaleBasePnt)
        doc.endEditing()
        doc.recompute()


if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{37521742-6ECA-4755-AFC1-7383020E0044}"))

    beamElem = AlphaBetonpilzeOval(doc)

    thisScript = lx.Application.getInstance().getActiveScript()
    if thisScript.isDragAndDropped():
        pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
    else:
        pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

    beamElem.setLocalPlacement(pos)

    # End editing of the Element
    doc.endEditing()
    doc.recompute()
