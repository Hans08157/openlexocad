import math, copy, traceback

# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

epsilon = 0.0001
pi2 = math.pi * 0.5


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))

def baseVecTranslate(pt, baseVec, dist):
    return Geom.Pnt(
        pt.x() + (baseVec.x() * dist),
        pt.y() + (baseVec.y() * dist),
        pt.z() + (baseVec.z() * dist)
    )

def vecsAreSame(v1, v2, tolerance = epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)

def solveSquare(a, b, c):
    # a*x^2 + b*x + c = 0

    d = b * b - 4.0 * a * c
    if d > epsilon:     # D > 0
        dSqr = math.sqrt(d)
        rev2A = 1.0 / (2.0 * a)

        x1 = (-b + dSqr) * rev2A
        x2 = (-b - dSqr) * rev2A

        return [x1, x2]
    elif d > -epsilon:  # D = 0
        return [-b / (2.0 * a)]
    else:
        []

def printVal(name, val):
    print ("{} = {}".format(name, val))

def printVec(name, val):
    print("{}: ({}, {}, {})".format(name, val.x(), val.y(), val.z()))


def printVec2D(name, val):
    print("{}: ({}, {})".format(name, val.x(), val.y()))


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
            raise RuntimeError("FacetedModelAssembler.endModel() must be called after FacetedModelAssembler.beginModel()")

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
            raise RuntimeError("FacetedModelAssembler.beginFace() must be called between FacetedModelAssembler.beginModel() and FacetedModelAssembler.endModel()")

        if self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.beginFace() is called twice")

        self._insideFaceCreation = True

    def addVertex(self, pos):
        if not self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.addVertex() must be called between FacetedModelAssembler.beginFace() and FacetedModelAssembler.endFace()")

        ptIndex = self._insertPoint(pos)
        self._indexList.append(ptIndex)

    def addVertexList(self, posList):
        if not self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.addVertexList() must be called between FacetedModelAssembler.beginFace() and FacetedModelAssembler.endFace()")

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
            raise RuntimeError("FacetedModelAssembler.addExtrusionBridgeNeg() must be called outside of face assembly process")

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

class Dormer2(lx.Element):
    _classID = Base.GlobalId("{C16CB96B-F35B-46BB-A103-EF13C7F0DA81}")

    _propHeader = "Dormer 2"
    _propGroupName = "Dormer 2"

    _lengthPropName = "Length"
    _widthPropName = "Width"
    _heightPropName = "Height"

    _offsetFrontPropName = "H Front"
    _horizontalTopPropName = "H Top"
    _offsetSidePropName = "H Side"

    _topPropName = "V Top"
    _bottomPropName = "V Below top"

    def getGlobalClassId(self):
        return Dormer2._classID

    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Dormer2", "OpenLxApp.Element")

        self._insidePropUpdate = False

        self.setPropertyHeader(lxstr(Dormer2._propHeader), -1)
        self.setPropertyGroupName(lxstr(Dormer2._propGroupName), -1)

        self._length = self.registerPropertyDouble(Dormer2._lengthPropName,
                                                   4.0,
                                                   lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE,
                                                   -1)

        self._width = self.registerPropertyDouble(Dormer2._widthPropName,
                                                  4.0,
                                                  lx.Property.VISIBLE,
                                                  lx.Property.EDITABLE,
                                                  -1)

        self._height = self.registerPropertyDouble(Dormer2._heightPropName,
                                                   4.0,
                                                   lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE,
                                                   -1)

        self._offsetFront = self.registerPropertyDouble(Dormer2._offsetFrontPropName,
                                                     1.0,
                                                     lx.Property.VISIBLE,
                                                     lx.Property.EDITABLE,
                                                     -1)

        self._horizontalTop = self.registerPropertyDouble(Dormer2._horizontalTopPropName,
                                                1.0,
                                                lx.Property.VISIBLE,
                                                lx.Property.EDITABLE,
                                                -1)

        self._offsetSide = self.registerPropertyDouble(Dormer2._offsetSidePropName,
                                                    1.0,
                                                    lx.Property.VISIBLE,
                                                    lx.Property.EDITABLE,
                                                    -1)

        self._top = self.registerPropertyDouble(Dormer2._topPropName,
                                                            1.0,
                                                            lx.Property.VISIBLE,
                                                            lx.Property.EDITABLE,
                                                            -1)

        self._bottom = self.registerPropertyDouble(Dormer2._bottomPropName,
                                                            1.0,
                                                            lx.Property.VISIBLE,
                                                            lx.Property.EDITABLE,
                                                            -1)

        

        self._updateGeometry()

    def _createGeometry(self, doc):
        length = self._length.getValue()
        width = self._width.getValue()
        height = self._height.getValue()

        o1 = self._offsetFront.getValue()
        o2 = self._offsetSide.getValue()

        top = self._top.getValue()
        horizontalTop = self._horizontalTop.getValue()
        bottom = self._bottom.getValue()

        pointList = []

        pointList.append(Geom.Pnt(-length + o1, (width * 0.5) - o2, 0.0))
        pointList.append(Geom.Pnt(-length + o1, -(width * 0.5) + o2, 0.0))
        pointList.append(Geom.Pnt(-length + o1, (width * 0.5) - o2, height - top - bottom))
        pointList.append(Geom.Pnt(-length + o1, -(width * 0.5) + o2, height - top - bottom))

        pointList.append(Geom.Pnt(-length, width * 0.5, height - top))
        pointList.append(Geom.Pnt(-length, -width * 0.5, height - top))
        pointList.append(Geom.Pnt(-length + horizontalTop, 0.0, height))

        pointList.append(Geom.Pnt(0.0, -(width * 0.5) + o2, height - top - bottom))
        pointList.append(Geom.Pnt(0.0, width * 0.5 - o2, height - top - bottom))
        pointList.append(Geom.Pnt(0.0, -width * 0.5, height - top))
        pointList.append(Geom.Pnt(0.0, width * 0.5, height - top))

        pointList.append(Geom.Pnt(0.0, 0.0, height))

        mdl = FacetedModelAssembler(doc)
        mdl.beginModel()

        if height - bottom - top <= epsilon:
            mdl.beginFace()
            mdl.addVertex(pointList[2])
            mdl.addVertex(pointList[3])
            mdl.addVertex(pointList[5])
            mdl.addVertex(pointList[4])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[4])
            mdl.addVertex(pointList[5])
            mdl.addVertex(pointList[6])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[3])
            mdl.addVertex(pointList[7])
            mdl.addVertex(pointList[9])
            mdl.addVertex(pointList[5])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[2])
            mdl.addVertex(pointList[4])
            mdl.addVertex(pointList[10])
            mdl.addVertex(pointList[8])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[6])
            mdl.addVertex(pointList[11])
            mdl.addVertex(pointList[10])
            mdl.addVertex(pointList[4])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[5])
            mdl.addVertex(pointList[9])
            mdl.addVertex(pointList[11])
            mdl.addVertex(pointList[6])
            mdl.endFace()
        else:

            mdl.beginFace()
            mdl.addVertex(pointList[0])
            mdl.addVertex(pointList[1])
            mdl.addVertex(pointList[3])
            mdl.addVertex(pointList[2])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[2])
            mdl.addVertex(pointList[3])
            mdl.addVertex(pointList[5])
            mdl.addVertex(pointList[4])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[4])
            mdl.addVertex(pointList[5])
            mdl.addVertex(pointList[6])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[7])
            mdl.addVertex(pointList[3])
            mdl.addVertex(pointList[1])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[3])
            mdl.addVertex(pointList[7])
            mdl.addVertex(pointList[9])
            mdl.addVertex(pointList[5])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[0])
            mdl.addVertex(pointList[2])
            mdl.addVertex(pointList[8])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[2])
            mdl.addVertex(pointList[4])
            mdl.addVertex(pointList[10])
            mdl.addVertex(pointList[8])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[6])
            mdl.addVertex(pointList[11])
            mdl.addVertex(pointList[10])
            mdl.addVertex(pointList[4])
            mdl.endFace()

            mdl.beginFace()
            mdl.addVertex(pointList[5])
            mdl.addVertex(pointList[9])
            mdl.addVertex(pointList[11])
            mdl.addVertex(pointList[6])
            mdl.endFace()

        return mdl.endModel()

    def _updateGeometry(self):
        doc = self.getDocument()

        with EditMode(doc):
            geom = self._createGeometry(doc)
            self.setGeometry(geom)

    def setLength(self, length):
        with EditMode(self.getDocument()):
            self._length.setValue(clamp(length, self.minLength(), 100000.0))
            self._updateGeometry()

    def length(self):
        return self._length.getValue()

    def minLength(self):
        first = self._top.getValue()
        second = self._horizontalTop.getValue()
        if first < second:
            return second
        return first

    def setWidth(self, width):
        with EditMode(self.getDocument()):
            self._width.setValue(max(self.minWidth(), width))
            self._updateGeometry()

    def width(self):
        return self._width.getValue()

    def minWidth(self):
        o2 = self._offsetSide.getValue()
        return o2 * 2.0 + 0.01

    def setHeight(self, height):
        with EditMode(self.getDocument()):
            self._height.setValue(max(self.minHeight(), height))
            self._updateGeometry()

    def height(self):
        return self._height.getValue()

    def minHeight(self):
        top = self._top.getValue()
        bottom = self._bottom.getValue()
        return top + bottom + epsilon

    def setOffsetFront(self, offsetFront):
        with EditMode(self.getDocument()):
            self._offsetFront.setValue(clamp(offsetFront, 0.001, self._length.getValue()))
            self._updateGeometry()

    def offsetFront(self):
        return self._offsetFront.getValue()

    def setOffsetSide(self, offsetSide):
        with EditMode(self.getDocument()):
            self._offsetSide.setValue(clamp(offsetSide, 0.001, self.maxOffsetSide()))
            self._updateGeometry()

    def offsetSide(self):
        return self._offsetSide.getValue()

    def maxOffsetSide(self):
        return self._width.getValue() * 0.5 - epsilon

    def setTop(self, top):
        with EditMode(self.getDocument()):
            self._top.setValue(clamp(top, 0.001, self.maxTop()))
            self._updateGeometry()

    def top(self):
        return self._top.getValue()

    def maxTop(self):
        return self._height.getValue() - self._bottom.getValue()

    def setHorizontalTop(self, horTop):
        with EditMode(self.getDocument()):
            self._horizontalTop.setValue(clamp(horTop, 0.001, self.length()))
            # if self._horizontalTop.getValue() < -self._length.getValue():
            #     self._horizontalTop.setValue()
            self._updateGeometry()

    def horizontalTop(self):
        return self._horizontalTop.getValue()

    def setBottom(self, bottom):
        with EditMode(self.getDocument()):
            self._bottom.setValue(clamp(bottom, 0.001, self.maxBottom()))
            self._updateGeometry()

    def bottom(self):
        return self._bottom.getValue()

    def maxBottom(self):
        return self._height.getValue() - self._top.getValue() - epsilon

    def onPropertyChanged(self, aPropertyName):
        if not self._insidePropUpdate:
            self._insidePropUpdate = True

            if aPropertyName == Dormer2._lengthPropName:
                self.setLength(self._length.getValue())
            elif aPropertyName == Dormer2._widthPropName:
                self.setWidth(self._width.getValue())
            elif aPropertyName == Dormer2._heightPropName:
                self.setHeight(self._height.getValue())
            elif aPropertyName == Dormer2._offsetFrontPropName:
                self.setOffsetFront(self._offsetFront.getValue())
            elif aPropertyName == Dormer2._offsetSidePropName:
                self.setOffsetSide(self._offsetSide.getValue())
            elif aPropertyName == Dormer2._topPropName:
                self.setTop(self._top.getValue())
            elif aPropertyName == Dormer2._bottomPropName:
                self.setBottom(self._bottom.getValue())
            elif aPropertyName == Dormer2._horizontalTopPropName:
                self.setHorizontalTop(self._horizontalTop.getValue())

            self._insidePropUpdate = False

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(self.getDocument()):
            if not Geom.GeomTools.isEqual(x, 1.):
                old = self._length.getValue()
                self.setLength(old * x)
            if not Geom.GeomTools.isEqual(y, 1.):
                old = self._width.getValue()
                self.setWidth(old * y)
            if not Geom.GeomTools.isEqual(z, 1.):
                old = self._height.getValue()
                self.setHeight(old * z)

            self.translateAfterScaled(aVec, aScaleBasePnt)

if __name__ == "__main__":
    app = lx.Application.getInstance()
    doc = app.getActiveDocument()
    uiapp = ui.UIApplication.getInstance()
    uidoc = uiapp.getUIDocument(doc)

    doc.registerPythonScript(Base.GlobalId("{EC3BD827-B4F2-4932-8D50-E492DF92CB0A}"))

    try:
        stais = Dormer2(doc)
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
        else:
            pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

        stais.setLocalPlacement(pos)
    except Exception as e:
        print(e.message)
        traceback.print_exc()
    finally:
        doc.recompute()