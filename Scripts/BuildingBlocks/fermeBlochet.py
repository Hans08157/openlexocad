# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import math, traceback

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


class Line2D:
    def __init__(self, pt, dir):
        self._pt = Geom.Pnt2d(pt.x(), pt.y())
        self._dir = dir.normalized()

    @staticmethod
    def from2Points(pt1, pt2):
        dir = Geom.Vec2d(pt2.x() - pt1.x(), pt2.y() - pt1.y())
        return Line2D(pt1, dir)

    def point(self):
        return self._pt

    def paramPoint(self, t):
        x = self._pt.x() + t * self._dir.x()
        y = self._pt.y() + t * self._dir.y()

        return Geom.Pnt2d(x, y)

    def direction(self):
        return self._dir

    def normal(self):
        return Geom.Vec2d(-self._dir.y(), self._dir.x())  # Direction is already normalized

    def offset(self, dVec):
        return Line2D(self._pt.translated(dVec), self._dir)

    def normalOffset(self, offs):
        normVec = self.normal()
        normVec.scale(offs)

        return self.offset(normVec)

    def findX(self, y):
        printVec2D("pt", self._pt)
        printVec2D("dir", self._dir)

        yDir = self._dir.y()
        if math.fabs(yDir) < epsilon:
            raise ZeroDivisionError("Line is parallel to Y axis.")

        t = (y - self._pt.y()) / yDir
        return self._pt.x() + t * self._dir.x()

    def findY(self, x):
        xDir = self._dir.x()
        if math.fabs(xDir) < epsilon:
            raise ZeroDivisionError("Line is parallel to X axis.")

        t = (x - self._pt.x()) / xDir
        return self._pt.y() + t * self._dir.y()

    def distanceToPointSq(self, pt):
        ptVec = Geom.Vec2d(self._pt, pt)
        ptVecLenSq = ptVec.squareMagnitude()

        printVec2D("distanceToPointSq() ptVec", ptVec)
        printVal("distanceToPointSq() ptVecLenSq", ptVecLenSq)

        projVecLenSq = ptVec * self._dir
        projVecLenSq *= projVecLenSq  # self._dir is already normalized, so we don't need to divide on ||self._dir||

        return ptVecLenSq - projVecLenSq

    def distanceToPoint(self, pt):
        return math.sqrt(self.distanceToPointSq(pt))

    def classifyPoint(self, pt):
        normVec = self.normal()
        ptDir = Geom.Vec2d(self._pt, pt)

        return math.copysign(1.0, normVec * ptDir)

    def signedDistToPoint(self, pt):
        return self.distanceToPoint(pt) * self.classifyPoint(pt)

    @staticmethod
    def collinear(l1, l2):
        if math.fabs(l2._dir.x()) < epsilon:
            return bool(math.fabs(l1._dir.x()) < epsilon)
        if math.fabs(l2._dir.y()) < epsilon:
            return bool(math.fabs(l1._dir.y()) < epsilon)

        return bool(math.fabs((l1._dir.x() / l2._dir.x()) - (l1._dir.y() / l2._dir.y())) < epsilon)

    @staticmethod
    def intersect(l1, l2):
        if Line2D.collinear(l1, l2):
            return None

        dx = l2._pt.x() - l1._pt.x()
        dy = l2._pt.y() - l1._pt.y()

        if math.fabs(l2._dir.y()) > epsilon:
            t = (dx * l2._dir.y() - dy * l2._dir.x()) / (l1._dir.x() * l2._dir.y() - l1._dir.y() * l2._dir.x())
            return l1.paramPoint(t)
        else:
            t = (dy * l1._dir.x() - dx * l1._dir.y()) / (l1._dir.y() * l2._dir.x())
            return l2.paramPoint(t)


class CoordSystem2D:
    def __init__(self, origin, u, v):
        self._origin = Geom.Pnt(origin)

        self._u = Geom.Vec(u)
        self._v = Geom.Vec(v)

    def toGlobal(self, localX, localY):
        return Geom.Pnt(
            self._origin.x() + self._u.x() * localX + self._v.x() * localY,
            self._origin.y() + self._u.y() * localX + self._v.y() * localY,
            0.0
        )


class PolylineData:
    SegmType_Line = 0
    SegmType_Arc = 1

    _closedSuffix = "_closed"
    _ptListSuffix = "_points"
    _edgeListSuffix = "_edges"

    class _Segment:
        def __init__(self, type, data):
            self.type = type
            self.data = data

    class _LineSegmData:
        def __init__(self, startIndex, closeSegm=False):
            self.startIndex = startIndex

            if not closeSegm:
                self.endIndex = startIndex + 1
            else:
                self.endIndex = 0

    class _ArcSegmData:
        def __init__(self, ptList, p1Index, closeSegm=False):
            self.p1Index = p1Index
            self.p2Index = p1Index + 1
            if not closeSegm:
                self.p3Index = p1Index + 2
            else:
                self.p3Index = 0

            self.arc = Arc3Pnt(ptList[self.p1Index], ptList[self.p2Index], ptList[self.p3Index])

    def __init__(self):
        self._closed = False

        self._ptList = []
        self._segmList = []

    @staticmethod
    def fromElement(lineElem):
        newPD = PolylineData()

        edges = Topo.ShapeTool.getEdges(lineElem.getShape())

        firstEdge = True
        startIndex = 0
        for edgeIndex in xrange(len(edges)):
            edge = edges[edgeIndex]

            edgeTypeRes = Topo.EdgeTool.getGeomCurveType(edge)
            if not edgeTypeRes.ok:
                raise RuntimeError("Can't get edge type")

            if edgeTypeRes.type == Geom.CurveType_LINE:
                lineParamRes = Topo.EdgeTool.getLineParameters(edge)
                if not lineParamRes.ok:
                    raise RuntimeError("Can't get line parameters")

                p1Res = Topo.EdgeTool.d0(edge, lineParamRes.startParam)
                if not p1Res.ok:
                    raise RuntimeError("Can't get line start point")
                if firstEdge:
                    newPD._ptList.append(Geom.Pnt(p1Res.p))
                    firstEdge = False

                p2Res = Topo.EdgeTool.d0(edge, lineParamRes.endParam)
                if not p2Res.ok:
                    raise RuntimeError("Can't get line end point")
                newPD._ptList.append(Geom.Pnt(p2Res.p))

                segmData = PolylineData._LineSegmData(startIndex, False)
                newPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))

                startIndex += 1
            elif edgeTypeRes.type == Geom.CurveType_CIRCLE:
                arcParamsRes = Topo.EdgeTool.getArcParameters(edge)
                if not arcParamsRes.ok:
                    raise RuntimeError("Can't get arc parameters")

                p1Res = Topo.EdgeTool.d0(edge, arcParamsRes.startParam)
                if not p1Res.ok:
                    raise RuntimeError("Can't get arc start point")
                if firstEdge:
                    newPD._ptList.append(Geom.Pnt(p1Res.p))
                    firstEdge = False

                middleParam = (arcParamsRes.startParam + arcParamsRes.endParam) * 0.5
                p2Res = Topo.EdgeTool.d0(edge, middleParam)
                if not p2Res.ok:
                    raise RuntimeError("Can't get arc middle point")
                newPD._ptList.append(Geom.Pnt(p2Res.p))

                p3Res = Topo.EdgeTool.d0(edge, arcParamsRes.endParam)
                if not p3Res.ok:
                    raise RuntimeError("Can't get arc end point")
                newPD._ptList.append(Geom.Pnt(p3Res.p))

                segmData = PolylineData._ArcSegmData(newPD._ptList, startIndex, False)
                newPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))

                startIndex += 2
            else:
                raise RuntimeError("Unsupported edge type")

        return newPD

    @staticmethod
    def forAssembly(startPt):
        newPD = PolylineData()
        newPD._ptList.append(Geom.Pnt(startPt))

        return newPD

    def appendLineSegment(self, endPt):
        if self._closed:
            raise RuntimeError("Polyline is already closed")

        startIndex = len(self._ptList) - 1
        self._ptList.append(Geom.Pnt(endPt))

        segmData = PolylineData._LineSegmData(startIndex)
        self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))

    def appendArcSegment(self, middlePt, endPt):
        if self._closed:
            raise RuntimeError("Polyline is already closed")

        startIndex = len(self._ptList) - 1
        self._ptList.append(Geom.Pnt(middlePt))
        self._ptList.append(Geom.Pnt(endPt))

        segmData = PolylineData._ArcSegmData(self._ptList, startIndex)
        self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))

    def closeWithLine(self):
        if self._closed:
            raise RuntimeError("Polyline is already closed")

        startIndex = len(self._ptList) - 1

        segmData = PolylineData._LineSegmData(startIndex, True)
        self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))

        self._closed = True

    def closeWithArc(self, middlePt):
        if self._closed:
            raise RuntimeError("Polyline is already closed")

        startIndex = len(self._ptList) - 1
        self._ptList.append(Geom.Pnt(middlePt))

        segmData = PolylineData._ArcSegmData(self._ptList, startIndex, True)
        self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))

        self._closed = True

    def isClosed(self):
        return self._closed

    def pointCount(self):
        return len(self._ptList)

    def point(self, id):
        return self._ptList[id]

    def segmentCount(self):
        return len(self._segmList)

    def segmentType(self, id):
        return self._segmList[id].type

    def segmStartPt(self, id):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
        else:
            startPtId = self._segmList[id].data.p1Index

        return self._ptList[startPtId]

    def segmStartTangent(self, id, normalize=False):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
            endPtId = self._segmList[id].data.endIndex

            tangVec = Geom.Vec(self._ptList[startPtId], self._ptList[endPtId])
            if normalize:
                tangVec.normalize()

            return tangVec
        else:
            return self._segmList[id].data.arc.startTangent()

    def segmStartBisector(self, id, normalize=False):
        if id <= 0:
            return self.segmStartTangent(id, normalize)
        else:
            prevTang = self.segmEndTangent(id - 1, True)
            currTang = self.segmStartTangent(id, True)

            bisect = prevTang + currTang
            if normalize:
                bisect.normalize()

            return bisect

    def segmEndPt(self, id):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.endIndex
        else:
            startPtId = self._segmList[id].data.p3Index

        return self._ptList[startPtId]

    def segmEndTangent(self, id, normalize=False):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
            endPtId = self._segmList[id].data.endIndex

            tangVec = Geom.Vec(self._ptList[endPtId], self._ptList[startPtId])
            if normalize:
                tangVec.normalize()

            return tangVec
        else:
            return self._segmList[id].data.arc.endTangent()

    def segmEndBisector(self, id, normalize=False):
        lastSegmId = len(self._segmList)
        if id >= lastSegmId:
            return self.segmEndTangent(id, normalize)
        else:
            currTang = self.segmEndTangent(id, True)
            nextTang = self.segmStartTangent(id + 1, True)

            bisect = currTang + nextTang
            if normalize:
                bisect.normalize()

            return bisect

    def segmArc(self, id):
        if self._segmList[id].type == PolylineData.SegmType_Arc:
            return self._segmList[id].data.arc
        else:
            raise TypeError("Segment is not of arc type")

    def _buildEdgeList(self):
        edgeList = []

        for edge in self._segmList:
            edgeList.append(int(edge.type))

        return edgeList

    def _buildSegmentList(self, edgeList):
        self._segmList = []

        segmCount = len(edgeList)
        lastSegmId = segmCount - 1

        startIndex = 0
        for edge in xrange(lastSegmId):
            edgeType = edgeList[edge]

            if edgeType == PolylineData.SegmType_Line:
                segmData = PolylineData._LineSegmData(startIndex, False)
                self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))

                startIndex += 1
            elif edgeType == PolylineData.SegmType_Arc:
                segmData = PolylineData._ArcSegmData(self._ptList, startIndex, False)
                self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))

                startIndex += 2
            else:
                self._segmList = None
                return

        # Last edge
        edgeType = edgeList[lastSegmId]

        if edgeType == PolylineData.SegmType_Line:
            segmData = PolylineData._LineSegmData(startIndex, self._closed)
            self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))
        elif edgeType == PolylineData.SegmType_Arc:
            segmData = PolylineData._ArcSegmData(self._ptList, startIndex, self._closed)
            self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))
        else:
            self._segmList = None
            return

    @staticmethod
    def prepareParamSet(paramSet, name):
        closedParamName = name + PolylineData._closedSuffix
        ptListParamName = name + PolylineData._ptListSuffix
        edgeListParamName = name + PolylineData._edgeListSuffix

        paramSet.setParameter(closedParamName, False)
        paramSet.setParameter(ptListParamName, None)
        paramSet.setParameter(edgeListParamName, None)

    def writeIntoParamSet(self, paramSet, name):
        closedParamName = name + PolylineData._closedSuffix
        ptListParamName = name + PolylineData._ptListSuffix
        edgeListParamName = name + PolylineData._edgeListSuffix

        paramSet.setParameter(closedParamName, self._closed, False)
        paramSet.setParameter(ptListParamName, self._ptList, False)
        paramSet.setParameter(edgeListParamName, self._buildEdgeList(), False)

    @staticmethod
    def fromParamSet(paramSet, name):
        closedParamName = name + PolylineData._closedSuffix
        ptListParamName = name + PolylineData._ptListSuffix
        edgeListParamName = name + PolylineData._edgeListSuffix

        if not paramSet.hasParameter(closedParamName) or \
                not paramSet.hasParameter(ptListParamName) or \
                not paramSet.hasParameter(edgeListParamName):
            return None

        newPD = PolylineData()

        newPD._closed = paramSet.getBoolParameter(closedParamName)

        newPD._ptList = paramSet.getPointListParameter(ptListParamName)
        if newPD._ptList is None:
            return None

        newPD._buildSegmentList(paramSet.getIntListParameter(edgeListParamName))
        if newPD._segmList is None:
            return None

        return newPD

    def makeCopy(self):
        copyPD = PolylineData()

        copyPD._closed = self._closed

        for pt in self._ptList:
            copyPD._ptList.append(Geom.Pnt(pt))

        for segm in self._segmList:
            if segm.type == PolylineData.SegmType_Line:
                closeSegm = bool(segm.data.endIndex == 0)
                lineData = PolylineData._LineSegmData(segm.data.startIndex, closeSegm)

                copyPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, lineData))
            elif segm.type == PolylineData.SegmType_Arc:
                closeSegm = bool(segm.data.p3Index == 0)
                arcData = PolylineData._ArcSegmData(copyPD._ptList, segm.data.p1Index, closeSegm)

                copyPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, arcData))

        return copyPD


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


class FermeBlochet(lx.Element):
    _classID = "{131D4E97-0816-43AC-81DF-3E1B1E836B4F}"
    _headerPropName = "Ferme Blochet"
    _groupPropName = "Ferme Blochet"

    # Parameters
    _largeurExterieureMurPN = "Largeur exterieure mur"
    _epaisseurMurPN = "Epaisseur mur"
    _hauteurEncuvementGauchePN = "Hauteur encuvement gauche"
    _hauteurEncuvementDroitPN = "Hauteur encuvement droit"
    _penteCouvertureGauchePN = "Pente couverture gauche"
    _penteCouvertureDroitePN = "Pente couverture droite"
    _hauteurSablierePN = "Hauteur sabliere"
    _largeurSablierePN = "Largeur sabliere"
    _hauteurDelardementSablierePN = "Hauteur delardement sabliere"
    _hauteurPannesIntermediairesPN = "Hauteur pannes intermediaires"
    _hauteurPanneFaitierePN = "Hauteur panne faitiere"
    _epaisseurPanneFaitierePN = "Epaisseur panne faitiere"
    _delardementFaitierePN = "Delardement faitiere"
    _epaisseurArbaletrierPN = "Epaisseur arbaletrier"
    _hauteurArbaletrierPN = "Hauteur arbaletrier"
    _sectionAuCarrePoinconPN = "Section au carre poincon"
    _jeuPoinconPourPassageFaitierePN = "Jeu poincon pour passage fairiere"
    _epaisseurEntraitPN = "Epaisseur entrait"
    _hauteurEntraitPN = "Hauteur entrait"
    _hauteurSousEntraitPN = "Hauteur sous entrait"
    _epaisseurBlochetPN = "Epaisseur blochet"
    _hauteurBlochetPN = "Hauteur blochet"
    _depassementBlochetEtEntraitPN = "Depassement blochet et entrait"
    _epaisseurJambeDeForcePN = "Epaisseur jambe de force"
    _hauteurJambeDeForcePN = "Hauteur jambe de force"
    _longueurJambeDeForcePN = "Longueur jambe de force"
    _hauteurSemellePN = "Hauteur semelle"
    _largeurSemellePN = "Largeur semelle"
    _longueurSemellePN = "Longueur semelle"
    _surlongueurSemellePN = "Surlongueur semelle"
    _profondeurEmbrevementPN = "Profondeur embrevement"

    def getGlobalClassId(self):
        return Base.GlobalId(FermeBlochet._classID)


    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("FermeBlochet", "OpenLxApp.Element")
        # Register properties

        self.setPropertyHeader(lxstr(FermeBlochet._headerPropName), -1)
        self.setPropertyGroupName(lxstr(FermeBlochet._groupPropName), -1)

        self._largeurExterieureMur = self.registerPropertyDouble(FermeBlochet._largeurExterieureMurPN, 8.0, \
                                                                 lx.Property.VISIBLE, \
                                                                 lx.Property.EDITABLE, \
                                                                 -1)
        self._epaisseurMur = self.registerPropertyDouble(FermeBlochet._epaisseurMurPN, \
                                                         0.2, \
                                                         lx.Property.VISIBLE, \
                                                         lx.Property.EDITABLE, \
                                                         -1)
        self._hauteurEncuvementGauche = self.registerPropertyDouble(FermeBlochet._hauteurEncuvementGauchePN, \
                                                                    0.4, \
                                                                    lx.Property.VISIBLE, \
                                                                    lx.Property.EDITABLE, \
                                                                    -1)
        self._hauteurEncuvementDroit = self.registerPropertyDouble(FermeBlochet._hauteurEncuvementDroitPN, \
                                                                   0.4, \
                                                                   lx.Property.VISIBLE, \
                                                                   lx.Property.EDITABLE, \
                                                                   -1)
        self._penteCouvertureGauche = self.registerPropertyDouble(FermeBlochet._penteCouvertureGauchePN, \
                                                                  45.0, \
                                                                  lx.Property.VISIBLE, \
                                                                  lx.Property.EDITABLE, \
                                                                  -1)
        self._penteCouvertureDroite = self.registerPropertyDouble(FermeBlochet._penteCouvertureDroitePN, \
                                                                  45.0, \
                                                                  lx.Property.VISIBLE, \
                                                                  lx.Property.EDITABLE, \
                                                                  -1)
        self._hauteurSabliere = self.registerPropertyDouble(FermeBlochet._hauteurSablierePN, \
                                                            0.05, \
                                                            lx.Property.VISIBLE, \
                                                            lx.Property.EDITABLE, \
                                                            -1)
        self._largeurSabliere = self.registerPropertyDouble(FermeBlochet._largeurSablierePN, \
                                                            0.15, \
                                                            lx.Property.VISIBLE, \
                                                            lx.Property.EDITABLE, \
                                                            -1)
        self._hauteurDelardementSabliere = self.registerPropertyDouble(FermeBlochet._hauteurDelardementSablierePN, \
                                                                       0.01, \
                                                                       lx.Property.VISIBLE, \
                                                                       lx.Property.EDITABLE, \
                                                                       -1)
        self._hauteurPannesIntermediaires = self.registerPropertyDouble(FermeBlochet._hauteurPannesIntermediairesPN, \
                                                                        0.225, \
                                                                        lx.Property.VISIBLE, \
                                                                        lx.Property.EDITABLE, \
                                                                        -1)
        self._hauteurPanneFaitiere = self.registerPropertyDouble(FermeBlochet._hauteurPanneFaitierePN, \
                                                                 0.225, \
                                                                 lx.Property.VISIBLE, \
                                                                 lx.Property.EDITABLE, \
                                                                 -1)
        self._epaisseurPanneFaitiere = self.registerPropertyDouble(FermeBlochet._epaisseurPanneFaitierePN, \
                                                                   0.075, \
                                                                   lx.Property.VISIBLE, \
                                                                   lx.Property.EDITABLE, \
                                                                   -1)
        self._delardementFaitiere = self.registerPropertyDouble(FermeBlochet._delardementFaitierePN, \
                                                                0.01, \
                                                                lx.Property.VISIBLE, \
                                                                lx.Property.EDITABLE, \
                                                                -1)
        self._epaisseurArbaletrier = self.registerPropertyDouble(FermeBlochet._epaisseurArbaletrierPN, \
                                                                 0.068, \
                                                                 lx.Property.VISIBLE, \
                                                                 lx.Property.EDITABLE, \
                                                                 -1)
        self._hauteurArbaletrier = self.registerPropertyDouble(FermeBlochet._hauteurArbaletrierPN, \
                                                               0.215, \
                                                               lx.Property.VISIBLE, \
                                                               lx.Property.EDITABLE, \
                                                               -1)
        self._sectionAuCarrePoincon = self.registerPropertyDouble(FermeBlochet._sectionAuCarrePoinconPN, \
                                                                  0.14, \
                                                                  lx.Property.VISIBLE, \
                                                                  lx.Property.EDITABLE, \
                                                                  -1)
        self._jeuPoinconPourPassageFaitiere = self.registerPropertyDouble(FermeBlochet._jeuPoinconPourPassageFaitierePN, \
                                                                          0.002, \
                                                                          lx.Property.VISIBLE, \
                                                                          lx.Property.EDITABLE, \
                                                                          -1)
        self._epaisseurEntrait = self.registerPropertyDouble(FermeBlochet._epaisseurEntraitPN, \
                                                             0.045, \
                                                             lx.Property.VISIBLE, \
                                                             lx.Property.EDITABLE, \
                                                             -1)
        self._hauteurEntrait = self.registerPropertyDouble(FermeBlochet._hauteurEntraitPN, \
                                                           0.19, \
                                                           lx.Property.VISIBLE, \
                                                           lx.Property.EDITABLE, \
                                                           -1)
        self._hauteurSousEntrait = self.registerPropertyDouble(FermeBlochet._hauteurSousEntraitPN, \
                                                               2.6, \
                                                               lx.Property.VISIBLE, \
                                                               lx.Property.EDITABLE, \
                                                               -1)
        self._epaisseurBlochet = self.registerPropertyDouble(FermeBlochet._epaisseurBlochetPN, \
                                                             0.045, \
                                                             lx.Property.VISIBLE, \
                                                             lx.Property.EDITABLE, \
                                                             -1)
        self._hauteurBlochet = self.registerPropertyDouble(FermeBlochet._hauteurBlochetPN, \
                                                           0.19, \
                                                           lx.Property.VISIBLE, \
                                                           lx.Property.EDITABLE, \
                                                           -1)
        self._depassementBlochetEtEntrait = self.registerPropertyDouble(FermeBlochet._depassementBlochetEtEntraitPN, \
                                                                        0.05, \
                                                                        lx.Property.VISIBLE, \
                                                                        lx.Property.EDITABLE, \
                                                                        -1)
        self._epaisseurJambeDeForce = self.registerPropertyDouble(FermeBlochet._epaisseurJambeDeForcePN, \
                                                                  0.068, \
                                                                  lx.Property.VISIBLE, \
                                                                  lx.Property.EDITABLE, \
                                                                  -1)
        self._hauteurJambeDeForce = self.registerPropertyDouble(FermeBlochet._hauteurJambeDeForcePN, \
                                                                0.215, \
                                                                lx.Property.VISIBLE, \
                                                                lx.Property.EDITABLE, \
                                                                -1)
        self._longueurJambeDeForce = self.registerPropertyDouble(FermeBlochet._longueurJambeDeForcePN, \
                                                                 1.6, \
                                                                 lx.Property.VISIBLE, \
                                                                 lx.Property.EDITABLE, \
                                                                 -1)
        self._hauteurSemelle = self.registerPropertyDouble(FermeBlochet._hauteurSemellePN, \
                                                           0.068, \
                                                           lx.Property.VISIBLE, \
                                                           lx.Property.EDITABLE, \
                                                           -1)
        self._largeurSemelle = self.registerPropertyDouble(FermeBlochet._largeurSemellePN, \
                                                           0.215, \
                                                           lx.Property.VISIBLE, \
                                                           lx.Property.EDITABLE, \
                                                           -1)
        self._longueurSemelle = self.registerPropertyDouble(FermeBlochet._longueurSemellePN, \
                                                            1.2, \
                                                            lx.Property.VISIBLE, \
                                                            lx.Property.EDITABLE, \
                                                            -1)
        self._surlongueurSemelle = self.registerPropertyDouble(FermeBlochet._surlongueurSemellePN, \
                                                               0.1, \
                                                               lx.Property.VISIBLE, \
                                                               lx.Property.EDITABLE, \
                                                               -1)
        self._profondeurEmbrevement = self.registerPropertyDouble(FermeBlochet._profondeurEmbrevementPN, \
                                                                  0.03, \
                                                                  lx.Property.VISIBLE, \
                                                                  lx.Property.EDITABLE, \
                                                                  -1)

        self._largeurExterieureMur.setSteps(0.2)
        self._epaisseurMur.setSteps(0.1)
        self._hauteurEncuvementGauche.setSteps(0.05)
        self._hauteurEncuvementDroit.setSteps(0.05)
        self._hauteurSabliere.setSteps(0.01)
        self._largeurSabliere.setSteps(0.01)
        self._hauteurDelardementSabliere.setSteps(0.01)
        self._hauteurPannesIntermediaires.setSteps(0.025)
        self._hauteurPanneFaitiere.setSteps(0.01)
        self._epaisseurPanneFaitiere.setSteps(0.01)
        self._delardementFaitiere.setSteps(0.01)
        self._epaisseurArbaletrier.setSteps(0.01)
        self._hauteurArbaletrier.setSteps(0.01)
        self._sectionAuCarrePoincon.setSteps(0.02)
        self._jeuPoinconPourPassageFaitiere.setSteps(0.001)
        self._epaisseurEntrait.setSteps(0.01)
        self._hauteurEntrait.setSteps(0.01)
        self._hauteurSousEntrait.setSteps(0.05)
        self._epaisseurBlochet.setSteps(0.01)
        self._hauteurBlochet.setSteps(0.01)
        self._depassementBlochetEtEntrait.setSteps(0.01)
        self._epaisseurJambeDeForce.setSteps(0.01)
        self._hauteurJambeDeForce.setSteps(0.01)
        self._longueurJambeDeForce.setSteps(0.01)
        self._largeurSemelle.setSteps(0.01)
        self._hauteurSemelle.setSteps(0.05)
        self._longueurSemelle.setSteps(0.1)
        self._surlongueurSemelle.setSteps(0.1)
        self._profondeurEmbrevement.setSteps(0.01)

        
        self._updateGeometry()

    @staticmethod
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
    def _createSubElement(listPoint, heightStep, dir):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)
        return subElem

    "Setter methods"
    def setLargeurExterieureMur(self, param):
        p16 = self._sectionAuCarrePoincon.getValue()
        p19 = self._hauteurEntrait.getValue()
        p20 = self._hauteurSousEntrait.getValue()

        lineList = self._createAdditionalLines()
        horPnt1 = Geom.Pnt2d(2.0, p19 + p20)
        horPnt2 = Geom.Pnt2d(2.0, p19 + p20 + 0.01)
        horLine = Line2D.from2Points(horPnt1, horPnt2)

        intPnt = Line2D.intersect(lineList[2], horLine)

        minVal = (intPnt.x() * 2.0) + p16


        with EditMode(self.getDocument()):
            self._largeurExterieureMur.setValue(clamp(param, minVal, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setEpaisseurMur(self, param):
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()

        lineList = self._createAdditionalLines()
        lArbLine = lineList[2]
        horLine = Line2D.from2Points(Geom.Pnt2d(0.0, p27), Geom.Pnt2d(0.1, p27))
        intPnt = Line2D.intersect(lArbLine, horLine)

        maxValue = p26 / math.sin(p5) - (p29 - intPnt.x())

        with EditMode(self.getDocument()):
            self._epaisseurMur.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param >= maxValue - 0.001:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))

    def setHauteurEncuvementGauche(self, param):
        epsilon = self._hauteurSemelle.getValue()
        p2 = self._epaisseurMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p25 = self._hauteurJambeDeForce.getValue()
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()

        lJambePnt1 = Geom.Pnt2d(p29 + p2, p27)
        lArbLine = Line2D.from2Points(
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5), p3),
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5) + math.cos(p5),
                       p3 + math.sin(p5)))

        leftDir = lArbLine.direction()
        lPnt1 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + ((p15 + p10) / math.sin(p5)), p3)

        a = leftDir.x() ** 2 + leftDir.y() ** 2
        b = 2 * (leftDir.x() * (lPnt1.x() - lJambePnt1.x()) + leftDir.y() * (lPnt1.y() - lJambePnt1.y()))
        c = (lPnt1.x() - lJambePnt1.x()) ** 2 + (lPnt1.y() - lJambePnt1.y()) ** 2 - p26 ** 2

        parameterList = solveSquare(a, b, c)
        t = parameterList[0]
        x = leftDir.x() * t + lPnt1.x()
        y = leftDir.y() * t + lPnt1.y()

        leftJambeLine = Line2D.from2Points(lJambePnt1, Geom.Pnt2d(x, y))
        offsetLine1 = leftJambeLine.normalOffset(p25)  #/ math.sin(self._calcJambeAngle()))

        controlIntersection = Line2D.intersect(offsetLine1, lArbLine)

        maxValue = controlIntersection.y()

        with EditMode(self.getDocument()):
            self._hauteurEncuvementGauche.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setHauteurEncuvementDroit(self, param):
        epsilon = self._hauteurSemelle.getValue()
        p1 = self._largeurExterieureMur.getValue()
        p2 = self._epaisseurMur.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p25 = self._hauteurJambeDeForce.getValue()
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()

        rJambePnt0 = Geom.Pnt2d(p1 - p2 - p29, p27)
        rArbLine = Line2D.from2Points(
            Geom.Pnt2d(p1 + (math.cos(p6) * p7 / math.sin(p6)) - ((p15 + p10) / math.sin(p6)), p4),
            Geom.Pnt2d(p1 + (math.cos(p6) * p7 / math.sin(p6)) - ((p15 + p10) / math.sin(p6)) - math.cos(p6),
                       p4 + math.sin(p6)))

        rightDir = rArbLine.direction()
        rPnt1 = Geom.Pnt2d(p1 + (math.cos(p6) * p7 / math.sin(p6)) - ((p15 + p10) / math.sin(p6)), p4)

        a1 = rightDir.x() ** 2 + rightDir.y() ** 2
        b1 = 2 * (rightDir.x() * (rPnt1.x() - rJambePnt0.x()) + rightDir.y() * (rPnt1.y() - rJambePnt0.y()))
        c1 = (rPnt1.x() - rJambePnt0.x()) ** 2 + (rPnt1.y() - rJambePnt0.y()) ** 2 - p26 ** 2

        parameterList = solveSquare(a1, b1, c1)
        t1 = parameterList[0]
        x1 = rightDir.x() * t1 + rPnt1.x()
        y1 = rightDir.y() * t1 + rPnt1.y()

        rightJambeLine = Line2D.from2Points(rJambePnt0, Geom.Pnt2d(x1, y1))
        offsetLine2 = rightJambeLine.normalOffset(-p25)  #/ math.sin(self._calcJambeAngle()))

        controlIntersection2 = Line2D.intersect(offsetLine2, rArbLine)

        maxValue = controlIntersection2.y()

        with EditMode(self.getDocument()):
            self._hauteurEncuvementDroit.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big."))

    def setPenteCouvertureGauche(self, param):
        p19 = self._hauteurEntrait.getValue()
        p20 = self._hauteurSousEntrait.getValue()
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p10 = self._hauteurPannesIntermediaires.getValue()
        p14 = self._epaisseurArbaletrier.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p16 = self._sectionAuCarrePoincon.getValue()

        lineList = self._createBaseLines()
        allowableHeight = p19 + p20
        minVal = None

        intersectPoint = Line2D.intersect(lineList[2], lineList[5])

        pnt9 = Geom.Pnt(p14 * 0.5, intersectPoint.x() + p16 * 0.5,
                        intersectPoint.y() - (p16 * 0.5 * math.sin(p6) / math.cos(p6)) - p15 / math.cos(p6) - p10 / math.cos(p6))
        # print "minVal - ", minVal, " pnt9.z() - ", pnt9.z()

        if pnt9.z() <= allowableHeight:
            pass

        with EditMode(self.getDocument()):
            self._penteCouvertureGauche.setValue(clamp(param, minVal, maxValue))
            self._updateGeometry()

        if param <= minVal:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        if param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setPenteCouvetureDroite(self, param):
        with EditMode(self.getDocument()):
            self._penteCouvertureDroite.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setHauteurSabliere(self, param):
        p9 = self._hauteurDelardementSabliere.getValue()
        p22 = self._hauteurBlochet.getValue()

        epsilon = p9 + 0.001
        maxValue = p22 - p9

        with EditMode(self.getDocument()):
            self._hauteurSabliere.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small."))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big."))

    def setLargeurSabliere(self, param):
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()

        mVal = -(math.cos(p5) * p7) / math.sin(p5) + p10 / math.sin(p5)
        mVal2 = -(math.cos(p6) * p7) / math.sin(p6) + p10 / math.sin(p6)
        maxValue = min(mVal, mVal2)
        epsilon = 0.001

        with EditMode(self.getDocument()):
            self._largeurSabliere.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small."))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big."))

    def setHauteurDelardementSabliere(self, param):
        p7 = self._hauteurSabliere.getValue()

        epsilon = 0.00
        maxValue = p7 - 0.001

        with EditMode(self.getDocument()):
            self._hauteurDelardementSabliere.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value can not be less than 0.0"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big."))

    def setHauteurPannesIntermediaires(self, param):
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p19 = self._hauteurEntrait.getValue()
        p20 = self._hauteurSousEntrait.getValue()

        epsilon = 0.000

        lineList = self._createBaseLines()
        intPnt = Line2D.intersect(lineList[2], lineList[5])

        maxValue = (intPnt.y() - (p19 + p20)) / math.sin(p5) if p5 > p6 else (intPnt.y() - (p19 + p20)) / math.sin(p6)

        with EditMode(self.getDocument()):
            self._hauteurPannesIntermediaires.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setHauteurPanneFaitiere(self, param):
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p16 = self._sectionAuCarrePoincon.getValue()
        p19 = self._hauteurEntrait.getValue()
        p20 = self._hauteurSousEntrait.getValue()
        linelist = self._createBaseLines()

        intPnt = Line2D.intersect(linelist[2], linelist[5])
        advZ1 = p16 * 0.5 * math.tan(p5)
        advZ2 = p16 * 0.5 * math.tan(p6)
        if p6 > p5:
            maxValue = intPnt.y() - (p19 + p20 + advZ1)
        else:
            maxValue = intPnt.y() - (p19 + p20 + advZ2)

        with EditMode(self.getDocument()):
            self._hauteurPanneFaitiere.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setEpaisseurPanneFaitiere(self, param):
        maxValue = self._sectionAuCarrePoincon.getValue() - 0.001

        with EditMode(self.getDocument()):
            self._epaisseurPanneFaitiere.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setDelardementFaitiere(self, param):
        epsilon = 0.000
        maxValue = self._hauteurPannesIntermediaires.getValue()

        with EditMode(self.getDocument()):
            self._delardementFaitiere.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setEpaisseurArbaletrier(self, param):
        maxValue = self._sectionAuCarrePoincon.getValue()
        with EditMode(self.getDocument()):
            self._epaisseurArbaletrier.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big."))

    def setHauteurArbaletrier(self, param):
        epsilon = self._profondeurEmbrevement.getValue() + 0.01

        with EditMode(self.getDocument()):
            self._hauteurArbaletrier.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setSectionAuCarrePoincon(self, param):
        epsilon = self._epaisseurPanneFaitiere.getValue() + 0.005

        with EditMode(self.getDocument()):
            self._sectionAuCarrePoincon.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setJeuPoinonPourPassageFaitiere(self, param):
        epsilon = 0.000
        maxValue = self._sectionAuCarrePoincon.getValue() - self._epaisseurPanneFaitiere.getValue()
        with EditMode(self.getDocument()):
            self._jeuPoinconPourPassageFaitiere.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setEpaisseurEntrait(self, param):
        epsilon = 0.001
        with EditMode(self.getDocument()):
            self._epaisseurEntrait.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setHauteurEntrait(self, param):
        p20 = self._hauteurSousEntrait.getValue()
        epsilon = 0.001

        lineList = self._createAdditionalLines()
        intPoint = Line2D.intersect(lineList[2], lineList[5])

        maxValue = intPoint.y() - p20

        with EditMode(self.getDocument()):
            self._hauteurEntrait.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setHauteurSousEntrait(self, param):
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p19 = self._hauteurEntrait.getValue()
        p22 = self._hauteurBlochet.getValue()

        leftH = p3 + p22
        rightH = p4 + p22
        epsilon = leftH if leftH > rightH else rightH

        lineList = self._createAdditionalLines()
        intPoint = Line2D.intersect(lineList[2], lineList[5])
        maxValue = intPoint.y() - p19

        with EditMode(self.getDocument()):
            self._hauteurSousEntrait.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))

    def setEpaisseurBlochet(self, param):
        with EditMode(self.getDocument()):
            self._epaisseurBlochet.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setHauteurBlochet(self, param):
        p1 = self._largeurExterieureMur.getValue()
        p2 = self._epaisseurMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p9 = self._hauteurDelardementSabliere.getValue()
        p25 = self._hauteurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()
        epsilon = p7 - p9 + 0.001

        lineList = self._createBaseLines()
        lArbLine = lineList[2]
        rArbline = lineList[5]

        lJambePnt = Geom.Pnt2d(p29 + p2 - p25 / math.sin(p5), p27)
        rJambePnt = Geom.Pnt2d(p1 - p2 - p29 + p25 / math.sin(p6), p27)

        jambeList = self._findJambePoints()
        lJambeLine = Line2D.from2Points(lJambePnt, Geom.Pnt2d(jambeList[0].y(), jambeList[0].z()))
        rJambeLine = Line2D.from2Points(rJambePnt, Geom.Pnt2d(jambeList[2].y(), jambeList[2].z()))

        leftInt = Line2D.intersect(lArbLine, lJambeLine)
        rightInt = Line2D.intersect(rArbline, rJambeLine)

        if p3 >= p4:
            maxValue = leftInt.y() - p3 - p27
        else:
            maxValue = rightInt.y() - p4 - p27

        with EditMode(self.getDocument()):
            self._hauteurBlochet.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setDepassementBlochetEtEntrait(self, param):
        epsilon = 0.000

        with EditMode(self.getDocument()):
            self._depassementBlochetEtEntrait.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))

    def setEpaisseurJambeDeForce(self, param):
        maxValue = self._epaisseurArbaletrier.getValue()
        with EditMode(self.getDocument()):
            self._epaisseurJambeDeForce.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setHauteurJambeDeForce(self, param):
        p1 = self._largeurExterieureMur.getValue()
        p2 = self._epaisseurMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p14 = self._epaisseurArbaletrier.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p16 = self._sectionAuCarrePoincon.getValue()
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()
        p31 = self._profondeurEmbrevement.getValue()

        # Lines
        firstLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5), p3)
        secondLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + math.cos(p5), p3 + math.sin(p5))

        firstRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6), p4)
        secondRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - math.cos(p6), p4 + math.sin(p6))

        leftALine = Line2D.from2Points(firstLeftPnt, secondLeftPnt)
        rightALine = Line2D.from2Points(firstRightPnt, secondRightPnt)

        intersectPoint = Line2D.intersect(leftALine, rightALine)

        lJambePnt1 = Geom.Pnt2d(p29 + p2, p27)

        lArbLine = Line2D.from2Points(
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5), p3),
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5) + math.cos(p5),
                       p3 + math.sin(p5)))

        leftDir = lArbLine.direction()
        lPnt1 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + ((p15 + p10) / math.sin(p5)), p3)

        a = leftDir.x() ** 2 + leftDir.y() ** 2
        b = 2 * (leftDir.x() * (lPnt1.x() - lJambePnt1.x()) + leftDir.y() * (lPnt1.y() - lJambePnt1.y()))
        c = (lPnt1.x() - lJambePnt1.x()) ** 2 + (lPnt1.y() - lJambePnt1.y()) ** 2 - p26 ** 2

        parameterList = solveSquare(a, b, c)
        t = parameterList[0]

        x = leftDir.x() * t + lPnt1.x()
        y = leftDir.y() * t + lPnt1.y()

        leftArbIntPnt0 = Geom.Pnt(p14 * 0.5, x, y)

        pnt5 = Geom.Pnt(p14 * 0.5, intersectPoint.x() - p16 * 0.5, intersectPoint.y() -
                        (p16 * 0.5 * math.sin(p5) / math.cos(p5)) - p15 / math.cos(p5) - p10 / math.cos(p5))
        lJambePnt1 = Geom.Pnt2d(p29 + p2, p27)

        lBotVec = Geom.Vec2d(Geom.Pnt2d(leftArbIntPnt0.y(), leftArbIntPnt0.z()),
                             Geom.Pnt2d(lJambePnt1.x(), lJambePnt1.y()))
        lTopVec = Geom.Vec2d(Geom.Pnt2d(leftArbIntPnt0.y(), leftArbIntPnt0.z()), Geom.Pnt2d(pnt5.y(), pnt5.z()))

        alpha = lBotVec.angle(lTopVec)
        angle = math.radians(((360.0 - math.degrees(alpha)) / 2))  # - math.radians(90.0))

        jambeAngle = self._calcJambeAngle()

        epsilon = p31 / math.sin(angle)
        maxValue = (p29 + p2 - ((p15 + p10) / math.sin(p5))) / math.sin(jambeAngle)

        with EditMode(self.getDocument()):
            self._hauteurJambeDeForce.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setLongueurJambeDeForce(self, param):
        p1 = self._largeurExterieureMur.getValue()
        p2 = self._epaisseurMur.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p16 = self._sectionAuCarrePoincon.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()

        lineList = self._createAdditionalLines()
        intPnt = Line2D.intersect(lineList[2], lineList[5])
        height = intPnt.y() - p27
        width = p1 * 0.5 - p16 - p2 - p29
        maxValue = math.sqrt(height**2 + width**2)

        lineList = self._createAdditionalLines()
        lArbLine = lineList[2]
        horLine = Line2D.from2Points(Geom.Pnt2d(0.0, p27), Geom.Pnt2d(0.1, p27))
        intPnt1 = Line2D.intersect(lArbLine, horLine)
        minVal = math.cos(p5) * (p2 + p29 - intPnt1.x())

        with EditMode(self.getDocument()):
            self._longueurJambeDeForce.setValue(clamp(param, minVal + 0.001, maxValue))
            self._updateGeometry()
        if param < minVal:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setHauteurSemelle(self, param):
        maxValue = min(self._hauteurEncuvementDroit.getValue(), self._hauteurEncuvementGauche.getValue())

        with EditMode(self.getDocument()):
            self._hauteurSemelle.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big."))

    def setLargeurSemelle(self, param):
        minValue = self._epaisseurJambeDeForce.getValue()

        with EditMode(self.getDocument()):
            self._largeurSemelle.setValue(clamp(param, minValue, maxValue))
            self._updateGeometry()
        if param <= minValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is to big"))

    def setLongueurSemelle(self, param):
        p1 = self._largeurExterieureMur.getValue()
        p2 = self._epaisseurMur.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p10 = self._hauteurPannesIntermediaires.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p25 = self._hauteurJambeDeForce.getValue()
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()

        # lineList = self._createAdditionalLines()
        # lArbLine = lineList[2]
        horLine = Line2D.from2Points(Geom.Pnt2d(0.0, p27), Geom.Pnt2d(0.1, p27))
        angle = self._calcJambeAngle()
        minVal = (p2 + p29) - p25 / math.sin(angle)

        lineList2 = self._createBaseLines()
        lBaseLine = lineList2[2]
        intPnt2 = Line2D.intersect(lBaseLine, horLine)
        leng = p26 + p15 + p10
        b = leng / math.cos(p5)

        maxValue = min(p1 * 0.5, b - p2 - math.fabs(intPnt2.x()) - 0.01)

        with EditMode(self.getDocument()):
            self._longueurSemelle.setValue(clamp(param, minVal, maxValue))
            self._updateGeometry()
        if param < minVal:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setSurlongueurSemelle(self, param):
        p1 = self._largeurExterieureMur.getValue()
        epaisseurMur = self._epaisseurMur.getValue()
        semelleLength = self._largeurSemelle.getValue()
        semelleWidth = self._longueurSemelle.getValue()
        semelleSurWidth = self._surlongueurSemelle.getValue()
        controlPoint = Geom.Pnt(semelleLength * 0.5, epaisseurMur + semelleWidth + semelleSurWidth, 0.0)
        epsilon = 0.02
        maxValue = p1 * 0.5

        with EditMode(self.getDocument()):
            self._surlongueurSemelle.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value can not be less than 0.02"))
        if controlPoint.y() > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big."))

    def setProfondeurEmbrevement(self, param):
        p1 = self._largeurExterieureMur.getValue()
        p2 = self._epaisseurMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p14 = self._epaisseurArbaletrier.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p16 = self._sectionAuCarrePoincon.getValue()
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()

        # Lines
        firstLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5), p3)
        secondLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + math.cos(p5), p3 + math.sin(p5))

        firstRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6), p4)
        secondRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - math.cos(p6), p4 + math.sin(p6))

        leftALine = Line2D.from2Points(firstLeftPnt, secondLeftPnt)
        rightALine = Line2D.from2Points(firstRightPnt, secondRightPnt)

        intersectPoint = Line2D.intersect(leftALine, rightALine)

        lJambePnt1 = Geom.Pnt2d(p29 + p2, p27)

        lArbLine = Line2D.from2Points(
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5), p3),
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5) + math.cos(p5),
                       p3 + math.sin(p5)))

        leftDir = lArbLine.direction()
        lPnt1 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + ((p15 + p10) / math.sin(p5)), p3)

        a = leftDir.x() ** 2 + leftDir.y() ** 2
        b = 2 * (leftDir.x() * (lPnt1.x() - lJambePnt1.x()) + leftDir.y() * (lPnt1.y() - lJambePnt1.y()))
        c = (lPnt1.x() - lJambePnt1.x()) ** 2 + (lPnt1.y() - lJambePnt1.y()) ** 2 - p26 ** 2

        parameterList = solveSquare(a, b, c)
        t = parameterList[0]

        x = leftDir.x() * t + lPnt1.x()
        y = leftDir.y() * t + lPnt1.y()

        leftArbIntPnt0 = Geom.Pnt(p14 * 0.5, x, y)

        pnt5 = Geom.Pnt(p14 * 0.5, intersectPoint.x() - p16 * 0.5, intersectPoint.y() -
                        (p16 * 0.5 * math.sin(p5) / math.cos(p5)) - p15 / math.cos(p5) - p10 / math.cos(p5))
        lJambePnt1 = Geom.Pnt2d(p29 + p2, p27)

        lBotVec = Geom.Vec2d(Geom.Pnt2d(leftArbIntPnt0.y(), leftArbIntPnt0.z()),
                             Geom.Pnt2d(lJambePnt1.x(), lJambePnt1.y()))
        lTopVec = Geom.Vec2d(Geom.Pnt2d(leftArbIntPnt0.y(), leftArbIntPnt0.z()), Geom.Pnt2d(pnt5.y(), pnt5.z()))

        alpha = lBotVec.angle(lTopVec)
        angle = math.radians(((360.0 - math.degrees(alpha)) / 2) - math.radians(90.0))

        minValue = 0.001
        maxValue = p15 / math.sin(angle)

        with EditMode(self.getDocument()):
            self._profondeurEmbrevement.setValue(clamp(param, minValue, maxValue))
            self._updateGeometry()
        if param <= minValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))


    """Calculation methods."""
    def _calcJambeAngle(self):
        p2 = self._epaisseurMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()

        lJambePnt1 = Geom.Pnt2d(p29 + p2, p27)

        lArbLine = Line2D.from2Points(
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5), p3),
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5) + math.cos(p5),
                       p3 + math.sin(p5)))

        leftDir = lArbLine.direction()
        lPnt1 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + ((p15 + p10) / math.sin(p5)), p3)

        a = leftDir.x() ** 2 + leftDir.y() ** 2
        b = 2 * (leftDir.x() * (lPnt1.x() - lJambePnt1.x()) + leftDir.y() * (lPnt1.y() - lJambePnt1.y()))
        c = (lPnt1.x() - lJambePnt1.x()) ** 2 + (lPnt1.y() - lJambePnt1.y()) ** 2 - p26 ** 2

        parameterList = solveSquare(a, b, c)
        t = parameterList[0]

        x = leftDir.x() * t + lPnt1.x()
        y = leftDir.y() * t + lPnt1.y()

        # Calculating jambe angle
        jambeVec = Geom.Vec2d(lJambePnt1, Geom.Pnt2d(x, y))
        jambeHorVec = Geom.Vec2d(lJambePnt1, Geom.Pnt2d(lJambePnt1.x() + 0.1, lJambePnt1.y()))
        jambAngle = jambeHorVec.angle(jambeVec)

        return jambAngle

    def _maxValueJambeInclination(self):
        """[0] is a left max value of indent, [1] - right max value."""
        p1 = self._largeurExterieureMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()

        lArbLine = Line2D.from2Points(
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5), p3),
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5) + math.cos(p5),
                       p3 + math.sin(p5)))

        rArbLine = Line2D.from2Points(
            Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - p15 / math.sin(p5) - p10 / math.sin(p5), p4),
            Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - p15 / math.sin(p5) - p10 / math.sin(p5) - math.cos(p6),
                       p4 + math.sin(p6)))

        horizontalLine = Line2D.from2Points(Geom.Pnt2d(0.0, p27), Geom.Pnt2d(0.1, p27))

        leftInt = Line2D.intersect(lArbLine, horizontalLine)
        rightInt = Line2D.intersect(rArbLine, horizontalLine)

        leftX = p26 / math.sin(p5)
        rightX = p26 / math.sin(p6)

        return [leftInt.x() + leftX, rightInt.x() - rightX]

    def _findJambePoints(self):
        """Returns two pairs of points(0,1) - left, (2,3) - right."""
        p1 = self._largeurExterieureMur.getValue()
        p2 = self._epaisseurMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p14 = self._epaisseurArbaletrier.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p16 = self._sectionAuCarrePoincon.getValue()
        p24 = self._epaisseurJambeDeForce.getValue()
        p25 = self._hauteurJambeDeForce.getValue()
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()

        defaultX = p14 * 0.5

        # Lines
        firstLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5), p3)
        secondLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + math.cos(p5), p3 + math.sin(p5))

        firstRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6), p4)
        secondRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - math.cos(p6), p4 + math.sin(p6))

        leftALine = Line2D.from2Points(firstLeftPnt, secondLeftPnt)
        rightALine = Line2D.from2Points(firstRightPnt, secondRightPnt)

        intersectPoint = Line2D.intersect(leftALine, rightALine)

        pnt5 = Geom.Pnt(defaultX, intersectPoint.x() - p16 * 0.5,
                        intersectPoint.y() - (p16 * 0.5 * math.sin(p5) / math.cos(p5)) - p15 / math.cos(
                            p5) - p10 / math.cos(p5))

        pnt9 = Geom.Pnt(defaultX, intersectPoint.x() + p16 * 0.5,
                        intersectPoint.y() - (p16 * 0.5 * math.sin(p6) / math.cos(p6)) - p15 / math.cos(
                            p6) - p10 / math.cos(p6))

        # Jambes de force.
        lJambePnt1 = Geom.Pnt2d(p29 + p2, p27)

        rJambePnt0 = Geom.Pnt2d(p1 - p2 - p29, p27)

        lArbLine = Line2D.from2Points(
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5), p3),
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5) + math.cos(p5),
                       p3 + math.sin(p5)))

        leftDir = lArbLine.direction()
        lPnt1 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + ((p15 + p10) / math.sin(p5)), p3)

        a = leftDir.x() ** 2 + leftDir.y() ** 2
        b = 2 * (leftDir.x() * (lPnt1.x() - lJambePnt1.x()) + leftDir.y() * (lPnt1.y() - lJambePnt1.y()))
        c = (lPnt1.x() - lJambePnt1.x()) ** 2 + (lPnt1.y() - lJambePnt1.y()) ** 2 - p26 ** 2

        parameterList = solveSquare(a, b, c)
        t = parameterList[0]

        x = leftDir.x() * t + lPnt1.x()
        y = leftDir.y() * t + lPnt1.y()

        leftArbIntPnt0 = Geom.Pnt(p14 * 0.5, x, y)

        leftJambeLine = Line2D.from2Points(lJambePnt1, Geom.Pnt2d(x, y))
        offsetLine1 = leftJambeLine.normalOffset(p25)  #/ math.sin(self._calcJambeAngle()))

        controlIntersection = Line2D.intersect(offsetLine1, lArbLine)

        leftArbIntPnt1 = Geom.Pnt(p14 * 0.5, controlIntersection.x(), controlIntersection.y())

        lJambePnt1 = Geom.Pnt(p24 * 0.5, lJambePnt1.x(), lJambePnt1.y())

        # Profondeur
        lBotVec = Geom.Vec2d(Geom.Pnt2d(leftArbIntPnt0.y(), leftArbIntPnt0.z()),
                             Geom.Pnt2d(lJambePnt1.y(), lJambePnt1.z()))
        lTopVec = Geom.Vec2d(Geom.Pnt2d(leftArbIntPnt0.y(), leftArbIntPnt0.z()), Geom.Pnt2d(pnt5.y(), pnt5.z()))
        lBotVec.normalize()
        lTopVec.normalize()
        lProfVec = lBotVec.added(lTopVec)
        lProfVec.normalize()

        # Right jambe de force.
        rArbLine = Line2D.from2Points(
            Geom.Pnt2d(p1 + (math.cos(p6) * p7 / math.sin(p6)) - ((p15 + p10) / math.sin(p6)), p4),
            Geom.Pnt2d(p1 + (math.cos(p6) * p7 / math.sin(p6)) - ((p15 + p10) / math.sin(p6)) - math.cos(p6),
                       p4 + math.sin(p6)))

        rightDir = rArbLine.direction()
        rPnt1 = Geom.Pnt2d(p1 + (math.cos(p6) * p7 / math.sin(p6)) - ((p15 + p10) / math.sin(p6)), p4)

        a1 = rightDir.x() ** 2 + rightDir.y() ** 2
        b1 = 2 * (rightDir.x() * (rPnt1.x() - rJambePnt0.x()) + rightDir.y() * (rPnt1.y() - rJambePnt0.y()))
        c1 = (rPnt1.x() - rJambePnt0.x()) ** 2 + (rPnt1.y() - rJambePnt0.y()) ** 2 - p26 ** 2

        parameterList = solveSquare(a1, b1, c1)
        t1 = parameterList[0]
        x1 = rightDir.x() * t1 + rPnt1.x()
        y1 = rightDir.y() * t1 + rPnt1.y()

        rightArbIntPnt0 = Geom.Pnt(p14 * 0.5, x1, y1)

        rightJambeLine = Line2D.from2Points(rJambePnt0, Geom.Pnt2d(x1, y1))
        offsetLine2 = rightJambeLine.normalOffset(-p25)  #/ math.sin(self._calcJambeAngle()))

        controlIntersection2 = Line2D.intersect(offsetLine2, rArbLine)

        rightArbIntPnt1 = Geom.Pnt(p14 * 0.5, controlIntersection2.x(), controlIntersection2.y())

        '''Translating to 3 dimensional point objects'''
        rJambePnt0 = Geom.Pnt(p24 * 0.5, rJambePnt0.x(), rJambePnt0.y())

        '''Profondeur'''
        rBotVec = Geom.Vec2d(Geom.Pnt2d(rightArbIntPnt0.y(), rightArbIntPnt0.z()),
                             Geom.Pnt2d(rJambePnt0.y(), rJambePnt0.z()))
        rTopVec = Geom.Vec2d(Geom.Pnt2d(rightArbIntPnt0.y(), rightArbIntPnt0.z()), Geom.Pnt2d(pnt9.y(), pnt9.z()))
        rBotVec.normalize()
        rTopVec.normalize()
        rProfVec = rBotVec.added(rTopVec)
        rProfVec.normalize()

        return [leftArbIntPnt0, leftArbIntPnt1, rightArbIntPnt0, rightArbIntPnt1]

    def _createAdditionalLines(self):
        """This method returns four points that form two additional lines, and two Line2d objects."""
        p1 = self._largeurExterieureMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p15 = self._hauteurArbaletrier.getValue()

        lPnt0 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5), p3)
        lPnt1 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5) + math.cos(p5),
                       p3 + math.sin(p5))

        lArbLine = Line2D.from2Points(lPnt0, lPnt1)

        rPnt0 = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - p15 / math.sin(p5) - p10 / math.sin(p5), p4)
        rPnt1 = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - p15 / math.sin(p5) - p10 / math.sin(p5) - math.cos(p6),
                       p4 + math.sin(p6))

        rArbLine = Line2D.from2Points(rPnt0, rPnt1)

        return [lPnt0, lPnt1, lArbLine, rPnt0, rPnt1, rArbLine]

    def _createBaseLines(self):
        """[2] is a left line, [5] is right line. [0],[1] are points that form left line.
         [3],[4] are points that form right line"""
        p1 = self._largeurExterieureMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()

        firstLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5), p3)
        secondLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + math.cos(p5), p3 + math.sin(p5))

        firstRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6), p4)
        secondRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - math.cos(p6), p4 + math.sin(p6))

        leftALine = Line2D.from2Points(firstLeftPnt, secondLeftPnt)
        rightALine = Line2D.from2Points(firstRightPnt, secondRightPnt)

        return [firstLeftPnt, secondLeftPnt, leftALine, firstRightPnt, secondRightPnt, rightALine]


    """Geometry methods"""
    def _createPoincon(self):
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p11 = self._hauteurPanneFaitiere.getValue()
        p12 = self._epaisseurPanneFaitiere.getValue()
        p13 = self._delardementFaitiere.getValue()
        p14 = self._epaisseurArbaletrier.getValue()
        p16 = self._sectionAuCarrePoincon.getValue()
        p17 = self._jeuPoinconPourPassageFaitiere.getValue()
        p19 = self._hauteurEntrait.getValue()
        p20 = self._hauteurSousEntrait.getValue()

        linesList = self._createBaseLines()
        leftALine = linesList[2]
        rightALine = linesList[5]
        intPnt = Line2D.intersect(leftALine, rightALine)

        # Constants
        defaultX = p14 * 0.5
        defaultY = p16 * 0.5
        halfLength = p16 * 0.5
        halfWidth = p16 * 0.5

        topPntY = (p16 - (p12 + p17)) * 0.5
        leftSlope = topPntY * math.tan(p5)
        rightSlope = topPntY * math.tan(p6)

        leftControlPnt = Geom.Pnt(defaultX, intPnt.x() - defaultY,
                                  intPnt.y() - (defaultY * math.sin(p5) / math.cos(p5)))
        rightControlPnt = Geom.Pnt(defaultX, intPnt.x() + defaultY,
                                   intPnt.y() - (defaultY * math.sin(p6) / math.cos(p6)))

        # Calculating coordinates for building points
        pnt0 = Geom.Pnt(defaultX, intPnt.x() - halfWidth, p20)
        pnt1 = Geom.Pnt(defaultX, intPnt.x() + halfWidth, p20)
        pnt2 = Geom.Pnt(-defaultX, intPnt.x() + halfWidth, p20)
        pnt3 = Geom.Pnt(-defaultX, intPnt.x() - halfWidth, p20)

        pnt4 = Geom.Pnt(defaultX, intPnt.x() - halfWidth, p20 + p19)
        pnt5 = Geom.Pnt(defaultX, intPnt.x() + halfWidth, p20 + p19)
        pnt6 = Geom.Pnt(-defaultX, intPnt.x() + halfWidth, p20 + p19)
        pnt7 = Geom.Pnt(-defaultX, intPnt.x() - halfWidth, p20 + p19)

        pnt8 = Geom.Pnt(halfLength, intPnt.x() - halfWidth, p20 + p19)
        pnt9 = Geom.Pnt(halfLength, intPnt.x() + halfWidth, p20 + p19)
        pnt10 = Geom.Pnt(-halfLength, intPnt.x() + halfWidth, p20 + p19)
        pnt11 = Geom.Pnt(-halfLength, intPnt.x() - halfWidth, p20 + p19)

        pnt16 = Geom.Pnt(halfLength, leftControlPnt.y(), leftControlPnt.z())
        pnt17 = Geom.Pnt(halfLength, rightControlPnt.y(), rightControlPnt.z())
        pnt18 = Geom.Pnt(-halfLength, rightControlPnt.y(), rightControlPnt.z())
        pnt19 = Geom.Pnt(-halfLength, leftControlPnt.y(), leftControlPnt.z())

        pnt20 = Geom.Pnt(halfLength, leftControlPnt.y() + topPntY, leftControlPnt.z() + leftSlope)
        pnt21 = Geom.Pnt(halfLength, rightControlPnt.y() - topPntY, rightControlPnt.z() + rightSlope)
        pnt22 = Geom.Pnt(-halfLength, rightControlPnt.y() - topPntY, rightControlPnt.z() + rightSlope)
        pnt23 = Geom.Pnt(-halfLength, leftControlPnt.y() + topPntY, leftControlPnt.z() + leftSlope)

        pnt12 = Geom.Pnt(halfLength, leftControlPnt.y() + topPntY, leftControlPnt.z() + leftSlope - p11 + p13 + p17)
        pnt13 = Geom.Pnt(halfLength, rightControlPnt.y() - topPntY, rightControlPnt.z() + rightSlope - p11 + p13 + p17)
        pnt14 = Geom.Pnt(-halfLength, rightControlPnt.y() - topPntY, rightControlPnt.z() + rightSlope - p11 + p13 + p17)
        pnt15 = Geom.Pnt(-halfLength, leftControlPnt.y() + topPntY, leftControlPnt.z() + leftSlope - p11 + p13 + p17)

        if p5 > p6:
            pnt12.setZ(pnt13.z())
            pnt15.setZ(pnt14.z())
        elif p6 > p5:
            pnt13.setZ(pnt12.z())
            pnt14.setZ(pnt15.z())

        # Building faces
        fma = FacetedModelAssembler(doc)

        fma.beginModel()

        fma.beginFace()
        fma.addVertexList([pnt3, pnt2, pnt1, pnt0])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt0, pnt1, pnt5, pnt4])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt8, pnt4, pnt5, pnt9])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt2, pnt3, pnt7, pnt6])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt1, pnt2, pnt6, pnt10, pnt18, pnt17, pnt9, pnt5])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt11, pnt10, pnt6, pnt7])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt0, pnt4, pnt8, pnt16, pnt19, pnt11, pnt7, pnt3])
        fma.endFace()

        # upper faces
        fma.beginFace()
        fma.addVertexList([pnt21, pnt17, pnt18, pnt22])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt20, pnt23, pnt19, pnt16])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt20, pnt12, pnt15, pnt23])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt12, pnt13, pnt14, pnt15])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt13, pnt21, pnt22, pnt14])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt8, pnt9, pnt17, pnt21, pnt13, pnt12, pnt20, pnt16])
        fma.endFace()

        fma.beginFace()
        fma.addVertexList([pnt10, pnt11, pnt19, pnt23, pnt15, pnt14, pnt22, pnt18])
        fma.endFace()

        geom = fma.endModel()

        poincon = lx.SubElement.createIn(doc)
        poincon.setGeometry(geom)

        self.addSubElement(poincon)

    def _createEntrait(self):
        p1 = self._largeurExterieureMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p14 = self._epaisseurArbaletrier.getValue()
        p18 = self._epaisseurEntrait.getValue()
        p19 = self._hauteurEntrait.getValue()
        p20 = self._hauteurSousEntrait.getValue()
        p23 = self._depassementBlochetEtEntrait.getValue()

        defaultX = p14 * 0.5

        leftLinePnt0 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + (p10 / math.sin(p5)), p3)
        leftLinePnt1 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + (p10 / math.sin(p5)) + math.cos(p5), p3 + math.sin(p5))
        rightLinePnt0 = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - p10 / math.sin(p6), p4)
        rightLinePnt1 = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - p10 / math.sin(p6) - math.cos(p6), p4 + math.sin(p6))

        leftALine = Line2D.from2Points(leftLinePnt0, leftLinePnt1)
        rightALine = Line2D.from2Points(rightLinePnt0, rightLinePnt1)

        linePnt0 = Line2D.intersect(leftALine, rightALine)
        linePnt1 = Geom.Pnt2d(linePnt0.x(), p20)
        linePnt2 = Geom.Pnt2d(linePnt0.x() + 0.1, p20)
        linePnt3 = Geom.Pnt2d(linePnt0.x(), p20 + p19)
        linePnt4 = Geom.Pnt2d(linePnt0.x() + 0.1, p20 + p19)

        lowerMiddleLine = Line2D.from2Points(linePnt1, linePnt2)
        upperMiddleLine = Line2D.from2Points(linePnt3, linePnt4)

        leftIntersectionPoint = Line2D.intersect(lowerMiddleLine, leftALine)
        rightIntersectionPoint = Line2D.intersect(lowerMiddleLine, rightALine)
        upleftIntersectionPoint = Line2D.intersect(upperMiddleLine, leftALine)
        uprightIntersectionPoint = Line2D.intersect(upperMiddleLine, rightALine)

        pnt0 = Geom.Pnt(defaultX, rightIntersectionPoint.x() + p23, rightIntersectionPoint.y())
        pnt1 = Geom.Pnt(defaultX, uprightIntersectionPoint.x() + p23, uprightIntersectionPoint.y())
        pnt2 = Geom.Pnt(defaultX, upleftIntersectionPoint.x() - p23, upleftIntersectionPoint.y())
        pnt3 = Geom.Pnt(defaultX, leftIntersectionPoint.x() - p23, leftIntersectionPoint.y())

        pnt4 = Geom.Pnt(-defaultX, rightIntersectionPoint.x() + p23, rightIntersectionPoint.y())
        pnt5 = Geom.Pnt(-defaultX, uprightIntersectionPoint.x() + p23, uprightIntersectionPoint.y())
        pnt6 = Geom.Pnt(-defaultX, upleftIntersectionPoint.x() - p23, upleftIntersectionPoint.y())
        pnt7 = Geom.Pnt(-defaultX, leftIntersectionPoint.x() - p23, leftIntersectionPoint.y())

        self.addSubElement(self._createSubElement([pnt3, pnt2, pnt1, pnt0], p18, Geom.Dir(1.0, 0.0, 0.0)))
        self.addSubElement(self._createSubElement([pnt4, pnt5, pnt6, pnt7], p18, Geom.Dir(-1.0, 0.0, 0.0)))

    def _createArbaletriersEtJambeDeForce(self):
        p1 = self._largeurExterieureMur.getValue()
        p2 = self._epaisseurMur.getValue()
        p3 = self._hauteurEncuvementGauche.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p10 = self._hauteurPannesIntermediaires.getValue()
        p14 = self._epaisseurArbaletrier.getValue()
        p15 = self._hauteurArbaletrier.getValue()
        p16 = self._sectionAuCarrePoincon.getValue()
        p24 = self._epaisseurJambeDeForce.getValue()
        p25 = self._hauteurJambeDeForce.getValue()
        p26 = self._longueurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()
        p29 = self._longueurSemelle.getValue()
        p31 = self._profondeurEmbrevement.getValue()

        defaultX = p14 * 0.5

        # Lines
        firstLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5), p3)
        secondLeftPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + math.cos(p5), p3 + math.sin(p5))

        firstRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6), p4)
        secondRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - math.cos(p6), p4 + math.sin(p6))

        leftALine = Line2D.from2Points(firstLeftPnt, secondLeftPnt)
        rightALine = Line2D.from2Points(firstRightPnt, secondRightPnt)

        intersectPoint = Line2D.intersect(leftALine, rightALine)

        # Left points
        pnt0 = Geom.Pnt(defaultX, - (math.cos(p5) * p7) / math.sin(p5) + p10 / math.sin(p5), p3)
        pnt1 = Geom.Pnt(defaultX, - (math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + (p10 / math.sin(p5)), p3)
        pnt5 = Geom.Pnt(defaultX, intersectPoint.x() - p16 * 0.5, intersectPoint.y() - (p16 * 0.5 * math.sin(p5) / math.cos(p5)) - p15 / math.cos(p5) - p10 / math.cos(p5))
        pnt6 = Geom.Pnt(defaultX, intersectPoint.x() - p16 * 0.5, intersectPoint.y() - (p16 * 0.5 * math.sin(p5) / math.cos(p5)) - p10 / math.cos(p5))

        # Right points
        pnt7 = Geom.Pnt(defaultX, p1 + (math.cos(p6) * p7) / math.sin(p6) - (p10 / math.sin(p6)), p4)
        pnt8 = Geom.Pnt(defaultX, intersectPoint.x() + p16 * 0.5, intersectPoint.y() - (p16 * 0.5 * math.sin(p6) / math.cos(p6)) - p10 / math.cos(p6))
        pnt9 = Geom.Pnt(defaultX, intersectPoint.x() + p16 * 0.5, intersectPoint.y() - (p16 * 0.5 * math.sin(p6) / math.cos(p6)) - p15 / math.cos(p6) - p10 / math.cos(p6))
        pnt13 = Geom.Pnt(defaultX, p1 + (math.cos(p6) * p7) / math.sin(p6) - p15 / math.sin(p6) - (p10 / math.sin(p6)), p4)

        # Jambes de force.
        lJambePnt1 = Geom.Pnt2d(p29 + p2, p27)
        rJambePnt0 = Geom.Pnt2d(p1 - p2 - p29, p27)

        lArbLine = Line2D.from2Points(
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5), p3),
            Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + p15 / math.sin(p5) + p10 / math.sin(p5) + math.cos(p5), p3 + math.sin(p5)))

        leftDir = lArbLine.direction()
        lPnt1 = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + ((p15 + p10) / math.sin(p5)), p3)

        a = leftDir.x() ** 2 + leftDir.y() ** 2
        b = 2 * (leftDir.x() * (lPnt1.x() - lJambePnt1.x()) + leftDir.y() * (lPnt1.y() - lJambePnt1.y()))
        c = (lPnt1.x() - lJambePnt1.x()) ** 2 + (lPnt1.y() - lJambePnt1.y()) ** 2 - p26 ** 2

        parameterList = solveSquare(a, b, c)
        t = parameterList[0]

        x = leftDir.x() * t + lPnt1.x()
        y = leftDir.y() * t + lPnt1.y()

        #Calculating jambe angle
        jambeVec = Geom.Vec2d(lJambePnt1, Geom.Pnt2d(x, y))
        jambeHorVec = Geom.Vec2d(lJambePnt1, Geom.Pnt2d(lJambePnt1.x() + 0.1, lJambePnt1.y()))

        jambAngle = jambeHorVec.angle(jambeVec)

        lJambePnt0 = Geom.Pnt2d(p29 + p2 - p25 / math.sin(jambAngle), p27)
        rJambePnt1 = Geom.Pnt2d(p1 - p2 - p29 + p25 / math.sin(jambAngle), p27)

        leftArbIntPnt0 = Geom.Pnt(p14 * 0.5, x, y)
        leftJambeIntPnt0 = Geom.Pnt(p24 * 0.5, x, y)

        leftJambeLine = Line2D.from2Points(lJambePnt1, Geom.Pnt2d(x, y))
        offsetLine1 = leftJambeLine.normalOffset(p25)  #/ math.sin(jambAngle))

        controlIntersection = Line2D.intersect(offsetLine1, lArbLine)

        leftArbIntPnt1 = Geom.Pnt(p14 * 0.5, controlIntersection.x(), controlIntersection.y())
        leftJambeIntPnt1 = Geom.Pnt(p24 * 0.5, controlIntersection.x(), controlIntersection.y())

        lJambePnt1 = Geom.Pnt(p24 * 0.5, lJambePnt1.x(), lJambePnt1.y())
        lJambePnt0 = Geom.Pnt(p24 * 0.5, lJambePnt0.x(), lJambePnt0.y())

        # Profondeur
        lBotVec = Geom.Vec2d(Geom.Pnt2d(leftArbIntPnt0.y(), leftArbIntPnt0.z()),
                             Geom.Pnt2d(lJambePnt1.y(), lJambePnt1.z()))
        lTopVec = Geom.Vec2d(Geom.Pnt2d(leftArbIntPnt0.y(), leftArbIntPnt0.z()), Geom.Pnt2d(pnt5.y(), pnt5.z()))
        lBotVec.normalize()
        lTopVec.normalize()
        lProfVec = lBotVec.added(lTopVec)
        lProfVec.normalize()

        lProfPntArb = Geom.Pnt(p14 * 0.5, leftArbIntPnt0.y() + (-p31 * lProfVec.x()),
                               leftArbIntPnt0.z() + (-p31 * lProfVec.y()))
        lProfPntJamb = Geom.Pnt(p24 * 0.5, leftJambeIntPnt0.y() + (-p31 * lProfVec.x()),
                                leftJambeIntPnt0.z() + (-p31 * lProfVec.y()))

        self.addSubElement(
            self._createSubElement([lJambePnt0, lJambePnt1, leftJambeIntPnt0, lProfPntJamb, leftJambeIntPnt1], p24,
                                   Geom.Dir(-1.0, 0.0, 0.0)))
        self.addSubElement(
            self._createSubElement([pnt0, pnt1, leftArbIntPnt1, lProfPntArb, leftArbIntPnt0, pnt5, pnt6], p14,
                                   Geom.Dir(-1.0, 0.0, 0.0)))

        # Right jambe de force.
        rArbLine = Line2D.from2Points(
            Geom.Pnt2d(p1 + (math.cos(p6) * p7 / math.sin(p6)) - ((p15 + p10) / math.sin(p6)), p4),
            Geom.Pnt2d(p1 + (math.cos(p6) * p7 / math.sin(p6)) - ((p15 + p10) / math.sin(p6)) - math.cos(p6),
                       p4 + math.sin(p6)))

        rightDir = rArbLine.direction()
        rPnt1 = Geom.Pnt2d(p1 + (math.cos(p6) * p7 / math.sin(p6)) - ((p15 + p10) / math.sin(p6)), p4)

        a1 = rightDir.x() ** 2 + rightDir.y() ** 2
        b1 = 2 * (rightDir.x() * (rPnt1.x() - rJambePnt0.x()) + rightDir.y() * (rPnt1.y() - rJambePnt0.y()))
        c1 = (rPnt1.x() - rJambePnt0.x()) ** 2 + (rPnt1.y() - rJambePnt0.y()) ** 2 - p26 ** 2

        parameterList = solveSquare(a1, b1, c1)
        t1 = parameterList[0]
        x1 = rightDir.x() * t1 + rPnt1.x()
        y1 = rightDir.y() * t1 + rPnt1.y()

        rightArbIntPnt0 = Geom.Pnt(p14 * 0.5, x1, y1)
        rightJambeIntPnt0 = Geom.Pnt(p24 * 0.5, x1, y1)

        rightJambeLine = Line2D.from2Points(rJambePnt0, Geom.Pnt2d(x1, y1))
        offsetLine2 = rightJambeLine.normalOffset(-p25)  #/ math.sin(jambAngle))

        controlIntersection2 = Line2D.intersect(offsetLine2, rArbLine)

        rightArbIntPnt1 = Geom.Pnt(p14 * 0.5, controlIntersection2.x(), controlIntersection2.y())
        rightJambeIntPnt1 = Geom.Pnt(p24 * 0.5, controlIntersection2.x(), controlIntersection2.y())

        rJambePnt1 = Geom.Pnt(p24 * 0.5, rJambePnt1.x(), rJambePnt1.y())
        rJambePnt0 = Geom.Pnt(p24 * 0.5, rJambePnt0.x(), rJambePnt0.y())

        # profondeur
        rBotVec = Geom.Vec2d(Geom.Pnt2d(rightArbIntPnt0.y(), rightArbIntPnt0.z()),
                             Geom.Pnt2d(rJambePnt0.y(), rJambePnt0.z()))
        rTopVec = Geom.Vec2d(Geom.Pnt2d(rightArbIntPnt0.y(), rightArbIntPnt0.z()), Geom.Pnt2d(pnt9.y(), pnt9.z()))
        rBotVec.normalize()
        rTopVec.normalize()
        rProfVec = rBotVec.added(rTopVec)
        rProfVec.normalize()

        rProfPntArb = Geom.Pnt(p14 * 0.5, rightArbIntPnt0.y() + (-p31 * rProfVec.x()),
                               rightArbIntPnt0.z() + (-p31 * rProfVec.y()))
        rProfPntJamb = Geom.Pnt(p24 * 0.5, rightJambeIntPnt0.y() + (-p31 * rProfVec.x()),
                                rightJambeIntPnt0.z() + (-p31 * rProfVec.y()))

        self.addSubElement(
            self._createSubElement([rJambePnt0, rJambePnt1, rightJambeIntPnt1, rProfPntJamb, rightJambeIntPnt0], p24,
                                   Geom.Dir(-1.0, 0.0, 0.0)))
        self.addSubElement(
            self._createSubElement([pnt7, pnt8, pnt9, rightArbIntPnt0, rProfPntArb, rightArbIntPnt1, pnt13], p14,
                                   Geom.Dir(-1.0, 0.0, 0.0)))

        return [lJambePnt1, leftJambeIntPnt0, rJambePnt0,
                rightJambeIntPnt0]  # This method returns two lines for future calculations.

    def _createLeftBlochet(self, jambePnt, intersectionPnt):
        p3 = self._hauteurEncuvementGauche.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p7 = self._hauteurSabliere.getValue()
        p8 = self._largeurSabliere.getValue()
        p9 = self._hauteurDelardementSabliere.getValue()
        p14 = self._epaisseurArbaletrier.getValue()
        p21 = self._epaisseurBlochet.getValue()
        p22 = self._hauteurBlochet.getValue()
        p23 = self._depassementBlochetEtEntrait.getValue()
        p24 = self._epaisseurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()

        vecPnt2 = Geom.Pnt(p24 * 0.5, jambePnt.y() + 0.100, p27)
        jambeVec = Geom.Vec(jambePnt, intersectionPnt)
        horVec = Geom.Vec(jambePnt, vecPnt2)
        jambeAngle = jambeVec.angle(horVec)

        lineList = self._createBaseLines()

        firstLeftPnt = lineList[0]
        leftALine = lineList[2]

        secondLinPnt = Geom.Pnt2d(-(math.cos(p5) * p7) / math.sin(p5) + 1.000, p3)
        leftHorLine = Line2D.from2Points(firstLeftPnt, secondLinPnt)

        jambeLine = Line2D.from2Points(Geom.Pnt2d(jambePnt.y(), jambePnt.z()),
                                       Geom.Pnt2d(intersectionPnt.y(), intersectionPnt.z()))
        controlPnt = Line2D.intersect(jambeLine, leftHorLine)

        pnt0 = Geom.Pnt(p14 * 0.5, controlPnt.x() + p23, controlPnt.y())
        pnt1 = Geom.Pnt(p14 * 0.5, controlPnt.x() + p23 + (p22 / math.tan(jambeAngle)), controlPnt.y() + p22)
        pnt1a = Geom.Pnt(p14 * 0.5, controlPnt.x() + p23 + (p22 / math.tan(jambeAngle)) - 0.1, controlPnt.y() + p22)

        pnt1Line = Line2D.from2Points(Geom.Pnt2d(pnt1.y(), pnt1.z()), Geom.Pnt2d(pnt1a.y(), pnt1a.z()))
        topIntersect = Line2D.intersect(leftALine, pnt1Line)
        pnt2 = Geom.Pnt(p14 * 0.5, topIntersect.x(), topIntersect.y())

        ang = math.radians(90.0 - math.degrees(p5))

        a = (p22 - p7 + p9) * math.tan(ang)
        pnt3 = Geom.Pnt(p14 * 0.5, pnt2.y() - a, controlPnt.y() + p7 - p9)
        pnt4 = Geom.Pnt(p14 * 0.5, pnt3.y() + p8 + p9, pnt3.z())
        pnt5 = Geom.Pnt(p14 * 0.5, pnt4.y(), p3)

        blochetPntList = [pnt0, pnt1, pnt2, pnt3, pnt4, pnt5]

        self.addSubElement(self._createSubElement(blochetPntList, p21, Geom.Dir(1.0, 0.0, 0.0)))

        for i in range(len(blochetPntList)):
            blochetPntList[i].setX(-p14 * 0.5)
        list(reversed(blochetPntList))

        self.addSubElement(self._createSubElement(blochetPntList, p21, Geom.Dir(-1.0, 0.0, 0.0)))

    def _createRightBlochet(self, jambePnt, intersectionPnt):
        p1 = self._largeurExterieureMur.getValue()
        p4 = self._hauteurEncuvementDroit.getValue()
        p5 = math.radians(self._penteCouvertureGauche.getValue())
        p6 = math.radians(self._penteCouvertureDroite.getValue())
        p7 = self._hauteurSabliere.getValue()
        p8 = self._largeurSabliere.getValue()
        p9 = self._hauteurDelardementSabliere.getValue()
        p14 = self._epaisseurArbaletrier.getValue()
        p21 = self._epaisseurBlochet.getValue()
        p22 = self._hauteurBlochet.getValue()
        p23 = self._depassementBlochetEtEntrait.getValue()
        p24 = self._epaisseurJambeDeForce.getValue()
        p27 = self._hauteurSemelle.getValue()

        vecPnt2 = Geom.Pnt(p24 * 0.5, jambePnt.y() - 0.100, p27)
        jambeVec = Geom.Vec(jambePnt, intersectionPnt)
        horVec = Geom.Vec(jambePnt, vecPnt2)
        jambeAngle = jambeVec.angle(horVec)

        firstRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6), p4)
        secondRightPnt = Geom.Pnt2d(p1 + (math.cos(p6) * p7) / math.sin(p6) - math.cos(p6), p4 + math.sin(p6))

        rightALine = Line2D.from2Points(firstRightPnt, secondRightPnt)

        secondLinPnt = Geom.Pnt2d(p1 + (math.cos(p5) * p7) / math.sin(p5) + 1.000, p4)
        leftHorLine = Line2D.from2Points(firstRightPnt, secondLinPnt)

        jambeLine = Line2D.from2Points(Geom.Pnt2d(jambePnt.y(), jambePnt.z()),
                                       Geom.Pnt2d(intersectionPnt.y(), intersectionPnt.z()))
        controlPnt = Line2D.intersect(jambeLine, leftHorLine)

        pnt0 = Geom.Pnt(p14 * 0.5, controlPnt.x() - p23, controlPnt.y())
        pnt1 = Geom.Pnt(p14 * 0.5, controlPnt.x() - p23 - (p22 / math.tan(jambeAngle)), controlPnt.y() + p22)
        pnt1a = Geom.Pnt(p14 * 0.5, controlPnt.x() - p23 - (p22 / math.tan(jambeAngle)) + 0.1, controlPnt.y() + p22)

        pnt1Line = Line2D.from2Points(Geom.Pnt2d(pnt1.y(), pnt1.z()), Geom.Pnt2d(pnt1a.y(), pnt1a.z()))
        topIntersect = Line2D.intersect(rightALine, pnt1Line)
        pnt2 = Geom.Pnt(p14 * 0.5, topIntersect.x(), topIntersect.y())

        ang = math.radians(90.0 - math.degrees(p6))

        a = (p22 - p7 + p9) * math.tan(ang)
        pnt3 = Geom.Pnt(p14 * 0.5, pnt2.y() + a, controlPnt.y() + p7 - p9)
        pnt4 = Geom.Pnt(p14 * 0.5, pnt3.y() - p8, pnt3.z())
        pnt5 = Geom.Pnt(p14 * 0.5, pnt4.y(), p4)

        blochetPntList = [pnt5, pnt4, pnt3, pnt2, pnt1, pnt0]

        self.addSubElement(self._createSubElement(blochetPntList, p21, Geom.Dir(1.0, 0.0, 0.0)))

        for i in range(len(blochetPntList)):
            blochetPntList[i].setX(-p14 * 0.5)
        list(reversed(blochetPntList))

        self.addSubElement(self._createSubElement(blochetPntList, p21, Geom.Dir(-1.0, 0.0, 0.0)))

    def _createLeftSemelle(self):
        pointList = []
        epaisseurMur = self._epaisseurMur.getValue()
        semelleLength = self._largeurSemelle.getValue()
        semelleWidth = self._longueurSemelle.getValue()
        semelleSurWidth = self._surlongueurSemelle.getValue()
        semelleHeight = self._hauteurSemelle.getValue()

        pointList.append(Geom.Pnt(semelleLength * 0.5, epaisseurMur, 0.0))
        pointList.append(Geom.Pnt(semelleLength * 0.5, epaisseurMur + semelleWidth + semelleSurWidth, 0.0))
        pointList.append(
            Geom.Pnt(semelleLength * 0.5, epaisseurMur + semelleWidth + semelleSurWidth, semelleHeight - 0.02))
        pointList.append(
            Geom.Pnt(semelleLength * 0.5, epaisseurMur + semelleWidth + semelleSurWidth - 0.02, semelleHeight))
        pointList.append(Geom.Pnt(semelleLength * 0.5, epaisseurMur, semelleHeight))

        leftSemelleSubElem = self._createSubElement(pointList, semelleLength, Geom.Dir(-1.0, 0.0, 0.0))

        self.addSubElement(leftSemelleSubElem)

    def _createRightSemelle(self):
        pointList = []
        epaisseurMur = self._epaisseurMur.getValue()
        width = self._largeurExterieureMur.getValue()
        semelleLength = self._largeurSemelle.getValue()
        semelleWidth = self._longueurSemelle.getValue()
        semelleSurWidth = self._surlongueurSemelle.getValue()
        semelleHeight = self._hauteurSemelle.getValue()

        pointList.append(Geom.Pnt(semelleLength * 0.5, width - epaisseurMur - semelleWidth - semelleSurWidth, 0.0))
        pointList.append(Geom.Pnt(semelleLength * 0.5, width - epaisseurMur, 0.0))
        pointList.append(Geom.Pnt(semelleLength * 0.5, width - epaisseurMur, semelleHeight))
        pointList.append(
            Geom.Pnt(semelleLength * 0.5, width - epaisseurMur - semelleWidth - semelleSurWidth + 0.02, semelleHeight))
        pointList.append(
            Geom.Pnt(semelleLength * 0.5, width - epaisseurMur - semelleWidth - semelleSurWidth, semelleHeight - 0.02))

        rightSemelleSubElem = self._createSubElement(pointList, semelleLength, Geom.Dir(-1.0, 0.0, 0.0))
        self.addSubElement(rightSemelleSubElem)

    def _createGeometry(self):
        # doc = self.getDocument()
        self._createLeftSemelle()
        self._createRightSemelle()
        self._createEntrait()
        self._createPoincon()
        lineList = self._createArbaletriersEtJambeDeForce()
        self._createLeftBlochet(lineList[0], lineList[1])
        self._createRightBlochet(lineList[2], lineList[3])

    def _updateGeometry(self):
        doc = self.getDocument()

        with EditMode(doc):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == FermeBlochet._largeurExterieureMurPN:
            self.setLargeurExterieureMur(self._largeurExterieureMur.getValue())
        elif aPropertyName == FermeBlochet._epaisseurMurPN:
            self.setEpaisseurMur(self._epaisseurMur.getValue())
        elif aPropertyName == FermeBlochet._hauteurEncuvementGauchePN:
            self.setHauteurEncuvementGauche(self._hauteurEncuvementGauche.getValue())
        elif aPropertyName == FermeBlochet._hauteurEncuvementDroitPN:
            self.setHauteurEncuvementDroit(self._hauteurEncuvementDroit.getValue())
        elif aPropertyName == FermeBlochet._penteCouvertureGauchePN:
            self.setPenteCouvertureGauche(self._penteCouvertureGauche.getValue())
        elif aPropertyName == FermeBlochet._penteCouvertureDroitePN:
            self.setPenteCouvetureDroite(self._penteCouvertureDroite.getValue())
        elif aPropertyName == FermeBlochet._hauteurSablierePN:
            self.setHauteurSabliere(self._hauteurSabliere.getValue())
        elif aPropertyName == FermeBlochet._largeurSablierePN:
            self.setLargeurSabliere(self._largeurSabliere.getValue())
        elif aPropertyName == FermeBlochet._hauteurDelardementSablierePN:
            self.setHauteurDelardementSabliere(self._hauteurDelardementSabliere.getValue())
        elif aPropertyName == FermeBlochet._hauteurPannesIntermediairesPN:
            self.setHauteurPannesIntermediaires(self._hauteurPannesIntermediaires.getValue())
        elif aPropertyName == FermeBlochet._hauteurPanneFaitierePN:
            self.setHauteurPanneFaitiere(self._hauteurPanneFaitiere.getValue())
        elif aPropertyName == FermeBlochet._epaisseurPanneFaitierePN:
            self.setEpaisseurPanneFaitiere(self._epaisseurPanneFaitiere.getValue())
        elif aPropertyName == FermeBlochet._delardementFaitierePN:
            self.setDelardementFaitiere(self._delardementFaitiere.getValue())
        elif aPropertyName == FermeBlochet._epaisseurArbaletrierPN:
            self.setEpaisseurArbaletrier(self._epaisseurArbaletrier.getValue())
        elif aPropertyName == FermeBlochet._hauteurArbaletrierPN:
            self.setHauteurArbaletrier(self._hauteurArbaletrier.getValue())
        elif aPropertyName == FermeBlochet._sectionAuCarrePoinconPN:
            self.setSectionAuCarrePoincon(self._sectionAuCarrePoincon.getValue())
        elif aPropertyName == FermeBlochet._jeuPoinconPourPassageFaitierePN:
            self.setJeuPoinonPourPassageFaitiere(self._jeuPoinconPourPassageFaitiere.getValue())
        elif aPropertyName == FermeBlochet._epaisseurEntraitPN:
            self.setEpaisseurEntrait(self._epaisseurEntrait.getValue())
        elif aPropertyName == FermeBlochet._hauteurEntraitPN:
            self.setHauteurEntrait(self._hauteurEntrait.getValue())
        elif aPropertyName == FermeBlochet._hauteurSousEntraitPN:
            self.setHauteurSousEntrait(self._hauteurSousEntrait.getValue())
        elif aPropertyName == FermeBlochet._epaisseurBlochetPN:
            self.setEpaisseurBlochet(self._epaisseurBlochet.getValue())
        elif aPropertyName == FermeBlochet._hauteurBlochetPN:
            self.setHauteurBlochet(self._hauteurBlochet.getValue())
        elif aPropertyName == FermeBlochet._depassementBlochetEtEntraitPN:
            self.setDepassementBlochetEtEntrait(self._depassementBlochetEtEntrait.getValue())
        elif aPropertyName == FermeBlochet._epaisseurJambeDeForcePN:
            self.setEpaisseurJambeDeForce(self._epaisseurJambeDeForce.getValue())
        elif aPropertyName == FermeBlochet._hauteurJambeDeForcePN:
            self.setHauteurJambeDeForce(self._hauteurJambeDeForce.getValue())
        elif aPropertyName == FermeBlochet._longueurJambeDeForcePN:
            self.setLongueurJambeDeForce(self._longueurJambeDeForce.getValue())
        elif aPropertyName == FermeBlochet._hauteurSemellePN:
            self.setHauteurSemelle(self._hauteurSemelle.getValue())
        elif aPropertyName == FermeBlochet._largeurSemellePN:
            self.setLargeurSemelle(self._largeurSemelle.getValue())
        elif aPropertyName == FermeBlochet._longueurSemellePN:
            self.setLongueurSemelle(self._longueurSemelle.getValue())
        elif aPropertyName == FermeBlochet._surlongueurSemellePN:
            self.setSurlongueurSemelle(self._surlongueurSemelle.getValue())
        elif aPropertyName == FermeBlochet._profondeurEmbrevementPN:
            self.setProfondeurEmbrevement(self._profondeurEmbrevement.getValue())

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(doc):
            if not Geom.GeomTools.isEqual(x, 1.):
                old = self.length.getValue()
                self.length.setValue(old * x)
            if not Geom.GeomTools.isEqual(y, 1.):
                old = self.width.getValue()
                self.width.setValue(old * y)
            if not Geom.GeomTools.isEqual(z, 1.):
                old = self.height.getValue()
                self.height.setValue(old * z)

            self.translateAfterScaled(aVec, aScaleBasePnt)

if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{204DADAB-06AA-40C8-AF6B-BB7DE79D8D32}"))

    try:
        fBlochet = FermeBlochet(doc)
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
        else:
            pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))
        fBlochet.setLocalPlacement(pos)
    except Exception as e:
        # print(e.message)
        traceback.print_exc()
    finally:
        doc.recompute()
