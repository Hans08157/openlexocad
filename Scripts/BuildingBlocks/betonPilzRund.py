# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import math, copy, traceback

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString
doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

epsilon = 0.001
maxValue = 10000


def solveSquare(a, b, c):
    # a*x^2 + b*x + c = 0

    d = b * b - 4.0 * a * c
    if d > epsilon:  # D > 0
        dSqr = math.sqrt(d)
        rev2A = 1.0 / (2.0 * a)

        x1 = (-b + dSqr) * rev2A
        x2 = (-b - dSqr) * rev2A

        return [x1, x2]
    elif d > -epsilon:  # D = 0
        x = -b / (2.0 * a)

        return [x]
    else:
        return []


def qstr(str):
    return Base.StringTool.toQString(lxstr(str))
# Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


def baseVecTranslate(pt, baseVec, dist):
    return Geom.Pnt(
        pt.x() + (baseVec.x() * dist),
        pt.y() + (baseVec.y() * dist),
        pt.z() + (baseVec.z() * dist)
    )


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

class FacetedModelAssembler:
    def __init__(self, doc):
        self._doc = doc
        if doc is None:
            raise ValueError("doc is None")

        self._pointList = None
        self._indexList = None

        self._insideFaceCreation = False

    def _insertPoint(self, pt):
        pointListLen = len(self._pointList)

        # Try to find this point in the list
        for index in xrange(pointListLen):
            if vecsAreSame(pt, self._pointList[index]):
                # print "[{}, {}, {}]: Found existing index - {}".format(pt.x(), pt.y(), pt.z(), index)
                return index

        # print "[{}, {}, {}]: Inserted new index - {}".format(pt.x(), pt.y(), pt.z(), pointListLen)

        # This point is not yet in the list
        self._pointList.append(Geom.Pnt(pt))
        return pointListLen

    def beginModel(self):
        if self._pointList is not None:
            raise RuntimeError("FacetedModelAssembler.beginModel() is called twice")

        self._pointList = Geom.vector_Pnt()
        self._indexList = []

    def endModel(self):
        if self._pointList is None:
            raise RuntimeError(
                "FacetedModelAssembler.endModel() must be called after FacetedModelAssembler.beginModel()")

        if self._insideFaceCreation:
            raise RuntimeError("Face must be closed before calling FacetedModelAssembler.endModel()")

        geom = lx.FacetedBrep.createIn(self._doc)
        geom.setPoints(self._pointList)
        geom.setModel(self._indexList)

        self._pointList = None
        self._indexList = None

        return geom

    def beginFace(self):
        if self._pointList is None:
            raise RuntimeError(
                "FacetedModelAssembler.beginFace() must be called between FacetedModelAssembler.beginModel() and FacetedModelAssembler.endModel()")

        if self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.beginFace() is called twice")

        self._insideFaceCreation = True

    def addVertex(self, pos):
        if not self._insideFaceCreation:
            raise RuntimeError(
                "FacetedModelAssembler.addVertex() must be called between FacetedModelAssembler.beginFace() and FacetedModelAssembler.endFace()")

        ptIndex = self._insertPoint(pos)
        self._indexList.append(ptIndex)

    def addVertexList(self, posList):
        if not self._insideFaceCreation:
            raise RuntimeError(
                "FacetedModelAssembler.addVertexList() must be called between FacetedModelAssembler.beginFace() and FacetedModelAssembler.endFace()")

        for pos in posList:
            ptIndex = self._insertPoint(pos)
            self._indexList.append(ptIndex)

    def endFace(self):
        if not self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.endFace() must be called after FacetedModelAssembler.beginFace()")

        self._indexList.append(-2)
        self._indexList.append(-1)

        self._insideFaceCreation = False

    def addExtrusionBridgeNeg(self, startEdge, endEdge, closed):
        if self._insideFaceCreation:
            raise RuntimeError(
                "FacetedModelAssembler.addExtrusionBridgeNeg() must be called outside of face assembly process")

        vtxCount = len(startEdge)
        if len(endEdge) != vtxCount:
            raise RuntimeError("Edge numbers must be equal.")

        if closed:
            minClearEdgeCount = 2
        else:
            minClearEdgeCount = 1

        clearEdgeCount = vtxCount - 1
        if clearEdgeCount < minClearEdgeCount:
            raise RuntimeError("There are too few edges.")

        for edge in xrange(clearEdgeCount):
            self.beginFace()

            self.addVertex(startEdge[edge])
            self.addVertex(endEdge[edge])
            self.addVertex(endEdge[edge + 1])
            self.addVertex(startEdge[edge + 1])

            self.endFace()

        if closed:
            self.beginFace()

            self.addVertex(startEdge[clearEdgeCount])
            self.addVertex(endEdge[clearEdgeCount])
            self.addVertex(endEdge[0])
            self.addVertex(startEdge[0])

            self.endFace()

    def addExtrusionBridgePos(self, startEdge, endEdge, closed):
        if self._insideFaceCreation:
            raise RuntimeError(
                "FacetedModelAssembler.addExtrusionBridgePos() must be called outside of face assembly process")

        vtxCount = len(startEdge)
        if len(endEdge) != vtxCount:
            raise RuntimeError("Edge numbers must be equal.")

        if closed:
            minClearEdgeCount = 2
        else:
            minClearEdgeCount = 1

        clearEdgeCount = vtxCount - 1
        if clearEdgeCount < minClearEdgeCount:
            raise RuntimeError("There are too few edges.")

        for edge in xrange(clearEdgeCount):
            self.beginFace()

            self.addVertex(startEdge[edge])
            self.addVertex(startEdge[edge + 1])
            self.addVertex(endEdge[edge + 1])
            self.addVertex(endEdge[edge])

            self.endFace()

        if closed:
            self.beginFace()

            self.addVertex(startEdge[clearEdgeCount])
            self.addVertex(startEdge[0])
            self.addVertex(endEdge[0])
            self.addVertex(endEdge[clearEdgeCount])

            self.endFace()

class BetonPilzRund(lx.Column):

    _classID = "{08C0DF09-7469-48B9-A45A-EEEB04AC7C3D}"
    _headerPropName = "Columnhead Square"
    _groupPropName = "Columnhead Square Parameter"

    # Parameters property names
    # _poleWidthPropName = "b column"
    _RPropName = "r upper part"
    _rPropName = "r lower part"
    _poleRadiusPropName = "r column"
    _HkPropName = "h collar"
    _vPropName = "h bevel"
    _heightPropName = "h column"
    _totalHeightPropName = "h total"


    def getGlobalClassId(self):
        return Base.GlobalId(BetonPilzRund._classID)

    def __init__(self, aArg):
        lx.Column.__init__(self, aArg)
        self.setPredefinedType(lx.Column.ColumnTypeEnum_COLUMN)
        self.registerPythonClass("BetonPilzRund", "OpenLxApp.Column")
        # Register properties
        self.setPropertyHeader(lxstr(BetonPilzRund._headerPropName), -1)
        self.setPropertyGroupName(lxstr(BetonPilzRund._groupPropName), -1)

        self._R = self.registerPropertyDouble(BetonPilzRund._RPropName, 0.5, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._r = self.registerPropertyDouble(BetonPilzRund._rPropName, 0.35, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._poleRadius = self.registerPropertyDouble(BetonPilzRund._poleRadiusPropName, 0.3, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._Hk = self.registerPropertyDouble(BetonPilzRund._HkPropName, 0.15, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._v = self.registerPropertyDouble(BetonPilzRund._vPropName, 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._height = self.registerPropertyDouble(BetonPilzRund._heightPropName, 2.5, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._totalHeight = self.registerPropertyDouble(BetonPilzRund._totalHeightPropName, 3.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._insidePropertyChange = False

        self._setAllSteps()
        
        self._updateGeometry()

    def _setAllSteps(self):
        self._R.setSteps(0.01)
        self._r.setSteps(0.01)
        self._poleRadius.setSteps(0.01)
        self._Hk.setSteps(0.01)
        self._v.setSteps(0.01)
        self._height.setSteps(0.01)
        self._totalHeight.setSteps(0.01)

    def buildSubElemLine(aDoc, aFromPnt, aToPnt):
        res = Geom.Vec(aToPnt.xyz() - aFromPnt.xyz())
        dir = Geom.Dir(res.normalized())
        line = lx.Line.createIn(aDoc)
        line.setPoint(aFromPnt)
        line.setDirection(dir)
        tc = lx.TrimmedCurve.createIn(aDoc)
        tc.setBasisCurve(line)
        tc.setTrim1(0)
        tc.setTrim2(res.magnitude())
        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(tc)
        return elem

    @staticmethod
    def _createExtrudedSubElement(listPoint, heightStep, dir):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)
        return subElem


    def setR(self, R):
        with EditMode(self.getDocument()):
            self._R.setValue(clamp(R, self.minR(), self.maxR()))
            self._updateGeometry()
        if R < self.minR():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif R > self.maxR():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def minR(self):
        return self._r.getValue()

    def maxR(self):
        return 10000.0

    def setr(self, r):
        with EditMode(self.getDocument()):
            self._r.setValue(clamp(r, self.minr(), self.maxr()))
            self._updateGeometry()
        if r < self.minr():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif r > self.maxr():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def minr(self):
        return self._poleRadius.getValue()

    def maxr(self):
        return self._R.getValue()

    def setPoleRadius(self, poleRadius):
        with EditMode(self.getDocument()):
            self._poleRadius.setValue(clamp(poleRadius, self.minPoleRadius(), self.maxPoleRadius()))
            self._updateGeometry()
        if poleRadius < self.minPoleRadius():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif poleRadius > self.maxPoleRadius():
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def minPoleRadius(self):
        return epsilon

    def maxPoleRadius(self):
        return self._r.getValue()

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

    def _createGeometry(self):
        doc = self.getDocument()
        columnHeight = self._totalHeight.getValue() - self._v.getValue() - (self._Hk.getValue() * 2.0)
        R = self._R.getValue()
        r = self._r.getValue()
        columnR = self._poleRadius.getValue()
        Hk = self._Hk.getValue()
        v = self._v.getValue()
        totalHeight = self._totalHeight.getValue()

        pnt0TopCircle = Geom.Pnt(-R, 0.0, totalHeight - Hk)
        pnt1TopCircle = Geom.Pnt(0.0, -R, totalHeight - Hk)
        pnt2TopCircle = Geom.Pnt(R, 0.0, totalHeight - Hk)
        pnt3TopCircle = Geom.Pnt(0.0, R, totalHeight - Hk)

        pnt0BottomCircle = Geom.Pnt(-r, 0.0, totalHeight - Hk - v)
        pnt1BottomCircle = Geom.Pnt(0.0, -r, totalHeight - Hk - v)
        pnt2BottomCircle = Geom.Pnt(r, 0.0, totalHeight - Hk - v)
        pnt3BottomCircle = Geom.Pnt(0.0, r, totalHeight - Hk - v)

        listFace = Topo.vector_Face(4)

        edgeListRightSmooth = Topo.vector_Edge(4)
        edgeListRightSmooth[0] = Topo.EdgeTool.makeArcOfCircle(pnt1TopCircle, pnt2TopCircle, pnt3TopCircle)
        edgeListRightSmooth[1] = Topo.EdgeTool.makeEdge(pnt3TopCircle, pnt3BottomCircle)
        edgeListRightSmooth[2] = Topo.EdgeTool.makeArcOfCircle(pnt3BottomCircle, pnt2BottomCircle, pnt1BottomCircle)
        edgeListRightSmooth[3] = Topo.EdgeTool.makeEdge(pnt1BottomCircle, pnt1TopCircle)
        rightSmoothWire = Topo.WireTool.makeWire(edgeListRightSmooth, Geom.Precision.linear_Resolution())
        rightSmoothFace = Topo.FaceTool.makeFace(rightSmoothWire, Geom.Precision.linear_Resolution())
        listFace[0] = rightSmoothFace

        edgeListLeftSmooth = Topo.vector_Edge(4)
        edgeListLeftSmooth[0] = Topo.EdgeTool.makeArcOfCircle(pnt1BottomCircle, pnt0BottomCircle, pnt3BottomCircle)
        edgeListLeftSmooth[1] = Topo.EdgeTool.makeEdge(pnt3BottomCircle, pnt3TopCircle)
        edgeListLeftSmooth[2] = Topo.EdgeTool.makeArcOfCircle(pnt3TopCircle, pnt0TopCircle, pnt1TopCircle)
        edgeListLeftSmooth[3] = Topo.EdgeTool.makeEdge(pnt1TopCircle, pnt1BottomCircle)
        leftSmoothWire = Topo.WireTool.makeWire(edgeListLeftSmooth, Geom.Precision.linear_Resolution())
        leftSmoothFace = Topo.FaceTool.makeFace(leftSmoothWire, Geom.Precision.linear_Resolution())
        listFace[1] = leftSmoothFace

        edgeListTop = Topo.vector_Edge(2)
        edgeListTop[0] = Topo.EdgeTool.makeArcOfCircle(pnt0TopCircle, pnt1TopCircle, pnt2TopCircle)
        edgeListTop[1] = Topo.EdgeTool.makeArcOfCircle(pnt2TopCircle, pnt3TopCircle, pnt0TopCircle)
        topWire = Topo.WireTool.makeWire(edgeListTop, Geom.Precision.linear_Resolution())
        topFace = Topo.FaceTool.makeFace(topWire, Geom.Precision.linear_Resolution())
        listFace[2] = topFace

        edgeListBottom = Topo.vector_Edge(2)
        edgeListBottom[0] = Topo.EdgeTool.makeArcOfCircle(pnt0BottomCircle, pnt1BottomCircle, pnt2BottomCircle)
        edgeListBottom[1] = Topo.EdgeTool.makeArcOfCircle(pnt2BottomCircle, pnt3BottomCircle, pnt0BottomCircle)
        bottomWire = Topo.WireTool.makeWire(edgeListBottom, Geom.Precision.linear_Resolution())
        bottomFace = Topo.FaceTool.makeFace(bottomWire, Geom.Precision.linear_Resolution())
        listFace[3] = bottomFace

        listShape = Topo.ShapeTool.makeShape(listFace)

        geom = lx.AdvancedBrep.createIn(doc)
        geom.setShape(listShape)

        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(geom)
        self.addSubElement(elem)

        faceTopBeam = Topo.FaceTool.extrudedFace(topFace, Geom.Dir(0.0, 0.0, 1.0), Hk)
        geomTopBeam = lx.AdvancedBrep.createIn(doc)
        geomTopBeam.setShape(faceTopBeam)
        topElem = lx.SubElement.createIn(doc)
        topElem.setGeometry(geomTopBeam)
        self.addSubElement(topElem)


        faceBottomBeam = Topo.FaceTool.extrudedFace(bottomFace, Geom.Dir(0.0, 0.0, -1.0), Hk)
        geomBottomBeam = lx.AdvancedBrep.createIn(doc)
        geomBottomBeam.setShape(faceBottomBeam)
        bottomElem = lx.SubElement.createIn(doc)
        bottomElem.setGeometry(geomBottomBeam)
        self.addSubElement(bottomElem)

        #column
        pnt0ColumnCircle = Geom.Pnt(-columnR, 0.0, totalHeight - Hk - v - Hk)
        pnt1ColumnCircle = Geom.Pnt(0.0, -columnR, totalHeight - Hk - v - Hk)
        pnt2ColumnCircle = Geom.Pnt(columnR, 0.0, totalHeight - Hk - v - Hk)
        pnt3ColumnCircle = Geom.Pnt(0.0, columnR, totalHeight - Hk - v - Hk)

        edgeListColumn = Topo.vector_Edge(2)
        edgeListColumn[0] = Topo.EdgeTool.makeArcOfCircle(pnt0ColumnCircle, pnt1ColumnCircle, pnt2ColumnCircle)
        edgeListColumn[1] = Topo.EdgeTool.makeArcOfCircle(pnt2ColumnCircle, pnt3ColumnCircle, pnt0ColumnCircle)
        columnWire = Topo.WireTool.makeWire(edgeListColumn, Geom.Precision.linear_Resolution())
        columnFace = Topo.FaceTool.makeFace(columnWire, Geom.Precision.linear_Resolution())
        faceColumn = Topo.FaceTool.extrudedFace(columnFace, Geom.Dir(0.0, 0.0, -1.0), columnHeight)
        geomColumn = lx.AdvancedBrep.createIn(doc)
        geomColumn.setShape(faceColumn)
        columnElem = lx.SubElement.createIn(doc)
        columnElem.setGeometry(geomColumn)
        self.addSubElement(columnElem)

    def _updateGeometry(self):
        doc = self.getDocument()

        with EditMode(doc):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if not self._insidePropertyChange:
            self._insidePropertyChange = True
            if aPropertyName == BetonPilzRund._RPropName:
                self.setR(self._R.getValue())

            elif aPropertyName == BetonPilzRund._rPropName:
                self.setr(self._r.getValue())

            elif aPropertyName == BetonPilzRund._poleRadiusPropName:
                self.setPoleRadius(self._poleRadius.getValue())

            elif aPropertyName == BetonPilzRund._HkPropName:
                self.setHk(self._Hk.getValue())

            elif aPropertyName == BetonPilzRund._vPropName:
                self.setV(self._v.getValue())

            elif aPropertyName == BetonPilzRund._heightPropName:
                self.setHeight(self._height.getValue())

            elif aPropertyName == BetonPilzRund._totalHeightPropName:
                self.setTotalHeight(self._totalHeight.getValue())
            self._insidePropertyChange = False

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
    doc.registerPythonScript(Base.GlobalId("{CD60A2E8-5C24-4410-A496-F5E43A77F4EF}"))

    try:
        compound = BetonPilzRund(doc)
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
        else:
            pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

        compound.setLocalPlacement(pos)
    except Exception as e:
        # print(e.message)
        traceback.print_exc()
    finally:
        doc.recompute()
