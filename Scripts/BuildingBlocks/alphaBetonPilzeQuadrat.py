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


def printVal(name, val):
    print("{} = {}".format(name, val))


def printVec(name, val):
    print("{}: ({}, {}, {})".format(name, val.x(), val.y(), val.z()))


def printVec2D(name, val):
    print("{}: ({}, {})".format(name, val.x(), val.y()))


def printPnt(name, pnt):
    print("{}: [{}, {}, {}]".format(name, pnt.x(), pnt.y(), pnt.z()))


def printPnt2d(name, pnt):
    print("{}: [{}, {}]".format(name, pnt.x(), pnt.y()))


def vecsAreSame(v1, v2, tolerance=epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)


def printPolyline(name, ptList):
    print("{}:".format(name))

    for pt in ptList:
        print("    ({}, {}, {})".format(pt.x(), pt.y(), pt.z()))


def printElemHierarchy(name, rootElem):
    outStr = name + ":\n  "
    outStr += rootElem + "\n"

    subElemList = rootElem.getSubElements()
    for subElem in subElemList:
        outStr += "  |-" + subElem + "\n"

    print(outStr)


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
        for index in range(pointListLen):
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

        for edge in range(clearEdgeCount):
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

        for edge in range(clearEdgeCount):
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

class BetonPilzQuadrat(lx.Column):

    _classID = "{131D4E97-0816-43AC-81DF-3E1B1E836B4F}"
    _headerPropName = "Beton Pilz Rechteckig"
    _groupPropName = "Beton Pilz Rechteckig Parameter"

    # Parameters property names
    _poleLengthPropName = "a column"
    _poleWidthPropName = "b column"
    _totalHeightPropName = "Total height"
    _aPropName  = "a"
    _bPropName  = "b"
    _APropName  = "A"
    _BPropName  = "B"
    _HkPropName = "hk"
    _vPropName  = "v"

    def getGlobalClassId(self):
        return Base.GlobalId("{2436C5CE-30F1-4461-BDF3-5D546B094737}")

    def __init__(self, aArg):
        lx.Column.__init__(self, aArg)
        self.setPredefinedType(lx.Column.ColumnTypeEnum_COLUMN)
        self.registerPythonClass("BetonPilzQuadrat", "OpenLxApp.Column")
        # Register properties
        self.setPropertyHeader(lxstr(BetonPilzQuadrat._headerPropName), -1)
        self.setPropertyGroupName(lxstr(BetonPilzQuadrat._groupPropName), -1)

        self._A = self.registerPropertyDouble(BetonPilzQuadrat._APropName, 0.5, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._B = self.registerPropertyDouble(BetonPilzQuadrat._BPropName, 0.5, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._a = self.registerPropertyDouble(BetonPilzQuadrat._aPropName, 0.35, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._b = self.registerPropertyDouble(BetonPilzQuadrat._bPropName, 0.35, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._poleLenght = self.registerPropertyDouble(BetonPilzQuadrat._poleLengthPropName, 0.3, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._poleWidth = self.registerPropertyDouble(BetonPilzQuadrat._poleWidthPropName, 0.3, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._Hk = self.registerPropertyDouble(BetonPilzQuadrat._HkPropName, 0.05, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._v = self.registerPropertyDouble(BetonPilzQuadrat._vPropName, 0.075, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._totalHeight = self.registerPropertyDouble(BetonPilzQuadrat._totalHeightPropName, 3.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._setAllSteps()
        
        self._updateGeometry()

    def _setAllSteps(self):
        self._totalHeight.setSteps(0.1)
        self._poleWidth.setSteps(0.1)
        self._poleLenght.setSteps(0.1)
        self._a.setSteps(0.1)
        self._b.setSteps(0.1)
        self._A.setSteps(0.1)
        self._B.setSteps(0.1)
        self._Hk.setSteps(0.01)
        self._v.setSteps(0.01)

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

    def set_a(self, param):
        epsilon = self._poleLenght.getValue()
        maxValue = self._A.getValue()
        with EditMode(self.getDocument()):
            self._a.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def set_b(self, param):
        epsilon = self._poleWidth.getValue()
        maxValue = self._B.getValue()
        with EditMode(self.getDocument()):
            self._b.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def set_A(self, param):
        epsilon = self._a.getValue()
        with EditMode(self.getDocument()):
            self._A.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def set_B(self, param):
        epsilon = self._b.getValue()
        with EditMode(self.getDocument()):
            self._B.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def set_totalHeight(self, param):
        with EditMode(self.getDocument()):
            self._totalHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def set_poleWidth(self, param):
        maxValue = self._b.getValue()
        with EditMode(self.getDocument()):
            self._poleWidth.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def set_poleLength(self, param):
        maxValue = self._a.getValue()
        with EditMode(self.getDocument()):
            self._poleLenght.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def set_Hk(self, param):
        with EditMode(self.getDocument()):
            self._Hk.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def set_v(self, param):
        with EditMode(self.getDocument()):
            self._v.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def _createSquarePole(self):
        poleHeight = self._totalHeight.getValue() - self._Hk.getValue() * 2 - self._v.getValue()
        poleWidth = self._poleWidth.getValue()
        poleLength = self._poleLenght.getValue()

        _dir = Geom.Dir(0.0, 0.0, 1.0)

        pointList = []
        pointList.append(Geom.Pnt(poleLength * 0.5, -poleWidth * 0.5, 0.0))
        pointList.append(Geom.Pnt(poleLength * 0.5, poleWidth * 0.5, 0.0))
        pointList.append(Geom.Pnt(-poleLength * 0.5, poleWidth * 0.5, 0.0))
        pointList.append(Geom.Pnt(-poleLength * 0.5, -poleWidth * 0.5, 0.0))

        self.addSubElement(self._createExtrudedSubElement(pointList, poleHeight, _dir))

    def _createSquarePilze(self):
        doc = self.getDocument()
        poleHeight = self._totalHeight.getValue() - self._Hk.getValue() * 2 - self._v.getValue()
        poleWidth = self._poleWidth.getValue()
        poleLength = self._poleLenght.getValue()
        a = self._a.getValue()
        b = self._b.getValue()
        A = self._A.getValue()
        B = self._B.getValue()
        Hk = self._Hk.getValue()
        v = self._v.getValue()

        pnt0 = Geom.Pnt(poleLength * 0.5, -poleWidth * 0.5, poleHeight) # 0
        pnt1 = Geom.Pnt(poleLength * 0.5, poleWidth * 0.5, poleHeight)
        pnt2 = Geom.Pnt(-poleLength * 0.5, poleWidth * 0.5, poleHeight)
        pnt3 = Geom.Pnt(-poleLength * 0.5, -poleWidth * 0.5, poleHeight)

        # overhang faces
        pnt4 = Geom.Pnt(a * 0.5, -b * 0.5, poleHeight) # 4
        pnt5 = Geom.Pnt(a * 0.5, b * 0.5, poleHeight)
        pnt6 = Geom.Pnt(-a * 0.5, b * 0.5, poleHeight)
        pnt7 = Geom.Pnt(-a * 0.5, -b * 0.5, poleHeight)

        # bottom Hk
        pnt8 = Geom.Pnt(a * 0.5, -b * 0.5, poleHeight + Hk)  # 8
        pnt9 = Geom.Pnt(a * 0.5, b * 0.5, poleHeight + Hk)
        pnt10 = Geom.Pnt(-a * 0.5, b * 0.5, poleHeight + Hk)
        pnt11 = Geom.Pnt(-a * 0.5, -b * 0.5, poleHeight + Hk)

        # top V
        pnt12 = Geom.Pnt(A * 0.5, -B * 0.5, poleHeight + Hk + v)  # 12
        pnt13 = Geom.Pnt(A * 0.5, B * 0.5, poleHeight + Hk + v)
        pnt14 = Geom.Pnt(-A * 0.5, B * 0.5, poleHeight + Hk + v)
        pnt15 = Geom.Pnt(-A * 0.5, -B * 0.5, poleHeight + Hk + v)

        # top Hk
        pnt16 = Geom.Pnt(A * 0.5, -B * 0.5, poleHeight + Hk + v + Hk)  # 16
        pnt17 = Geom.Pnt(A * 0.5, B * 0.5, poleHeight + Hk + v + Hk)
        pnt18 = Geom.Pnt(-A * 0.5, B * 0.5, poleHeight + Hk + v + Hk)
        pnt19 = Geom.Pnt(-A * 0.5, -B * 0.5, poleHeight + Hk + v + Hk)

        fma = FacetedModelAssembler(doc)
        fma.beginModel()
        # bottom faces
        fma.beginFace()
        fma.addVertexList([pnt0, pnt1, pnt5, pnt4])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt1, pnt2, pnt6, pnt5])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt2, pnt3, pnt7, pnt6])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt3, pnt0, pnt4, pnt7])
        fma.endFace()

        # bot Hk faces
        fma.beginFace()
        fma.addVertexList([pnt4, pnt5, pnt9, pnt8])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt5, pnt6, pnt10, pnt9])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt6, pnt7, pnt11, pnt10])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt7, pnt4, pnt8, pnt11])
        fma.endFace()

        # v faces
        fma.beginFace()
        fma.addVertexList([pnt8, pnt9, pnt13, pnt12])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt9, pnt10, pnt14, pnt13])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt10, pnt11, pnt15, pnt14])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt11, pnt8, pnt12, pnt15])
        fma.endFace()

        # top Hk faces

        fma.beginFace()
        fma.addVertexList([pnt12, pnt13, pnt17, pnt16])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt13, pnt14, pnt18, pnt17])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt14, pnt15, pnt19, pnt18])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt15, pnt12, pnt16, pnt19])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt16, pnt17, pnt18, pnt19])
        fma.endFace()

        geom = fma.endModel()

        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)

        self.addSubElement(subElem)

    def _createGeometry(self):
        self._createSquarePole()
        self._createSquarePilze()

    def _updateGeometry(self):
        doc = self.getDocument()

        with EditMode(doc):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == BetonPilzQuadrat._totalHeightPropName:
            self.set_totalHeight(self._totalHeight.getValue())
        elif aPropertyName == BetonPilzQuadrat._poleLengthPropName:
            self.set_poleLength(self._poleLenght.getValue())
        elif aPropertyName == BetonPilzQuadrat._poleWidthPropName:
            self.set_poleWidth(self._poleWidth.getValue())
        elif aPropertyName == BetonPilzQuadrat._aPropName:
            self.set_a(self._a.getValue())
        elif aPropertyName == BetonPilzQuadrat._bPropName:
            self.set_b(self._b.getValue())
        elif aPropertyName == BetonPilzQuadrat._APropName:
            self.set_A(self._A.getValue())
        elif aPropertyName == BetonPilzQuadrat._BPropName:
            self.set_B(self._B.getValue())
        elif aPropertyName == BetonPilzQuadrat._vPropName:
            self.set_v(self._v.getValue())
        elif aPropertyName == BetonPilzQuadrat._HkPropName:
            self.set_Hk(self._Hk.getValue())
        elif aPropertyName == BetonPilzQuadrat._overHangPropName:
            self.set_overHang(self._overHang.getValue())

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
    doc.registerPythonScript(Base.GlobalId("{204DADAB-06AA-40C8-AF6B-BB7DE79D8D32}"))

    try:
        compound = BetonPilzQuadrat(doc)
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
