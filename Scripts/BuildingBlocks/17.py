
# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import math, copy, traceback

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString
doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

epsilon = 0.001
maxValue = 10000.0

pi2 = math.pi * 0.5

# Helper functions for easier model assembly
def vecHAngle(xCoord, yCoord):
    if yCoord > epsilon:
        if xCoord > epsilon:
            return math.atan(yCoord / xCoord)
        elif xCoord < -epsilon:
            return math.pi + math.atan(yCoord / xCoord)
        else:
            return pi2
    elif yCoord < -epsilon:
        if xCoord > epsilon:
            return math.atan(yCoord / xCoord)
        elif xCoord < -epsilon:
            return -math.pi + math.atan(yCoord / xCoord)
        else:
            return -pi2
    else:
        if xCoord > -epsilon:
            return 0.0
        else:
            return math.pi


def vecVAngle(length, zCoord):
    if length < epsilon:
        return 0.0

    return math.asin(zCoord / length)


def angleVec(vec):
    vecLen = vec.magnitude()

    angleH = vecHAngle(vec.x(), vec.y())
    angleV = vecVAngle(vecLen, vec.z())

    return angleH, -angleV

def qstr(str):
   return Base.StringTool.toQString(lxstr(str))
#Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))

def printVal(name, val):
    print("{} = {}".format(name, val))


def printVec(name, val):
    print("{}: ({}, {}, {})".format(name, val.x(), val.y(), val.z()))


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

def vecsAreSame(v1, v2, tolerance = epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)

def baseVecTranslate(pt, baseVec, dist):
    return Geom.Pnt(
        pt.x() + (baseVec.x() * dist),
        pt.y() + (baseVec.y() * dist),
        pt.z() + (baseVec.z() * dist)
    )

class CoordSystem2D:
    def __init__(self, origin, u, v):
        self._origin = Geom.Pnt(origin)

        self._u = Geom.Vec(u)
        self._v = Geom.Vec(v)

    def toGlobal(self, localX, localY):
        return Geom.Pnt(
            self._origin.x() + self._u.x() * localX + self._v.x() *localY,
            self._origin.y() + self._u.y() * localX + self._v.y() * localY,
            0.0
        )

class Arc3Pnt:
    def __init__(self, p1, p2, p3):
        self._startPt = Geom.Pnt(p1)
        self._endPt = Geom.Pnt(p3)

        self._centerPt = Arc3Pnt._calcCenterPt(p1, p2, p3)

        self._startVec = Geom.Vec(self._centerPt, self._startPt)
        middleVec = Geom.Vec(self._centerPt, p2)
        endVec = Geom.Vec(self._centerPt, self._endPt)

        self._normVec = self._startVec.crossed(endVec)
        if self._normVec.squareMagnitude() < epsilon:
            self._normVec = self._startVec.crossed(middleVec)
        self._normVec.normalize()

        self._angle = Arc3Pnt._calcAngle(self._startVec, middleVec, endVec, self._normVec)

        self._axis = Geom.Ax1(self._centerPt, Geom.Dir(self._normVec))

    def copy(self):
        return Arc3Pnt(self._startPt, self.paramPt(0.5), self._endPt)

    @staticmethod
    def _calcBaryCenter(w1, p1, w2, p2, w3, p3):
        x = w1 * p1.x() + w2 * p2.x() + w3 * p3.x()
        y = w1 * p1.y() + w2 * p2.y() + w3 * p3.y()
        z = w1 * p1.z() + w2 * p2.z() + w3 * p3.z()

        return Geom.Pnt(x, y, z)

    @staticmethod
    def _calcCenterPt(p1, p2, p3):
        # For the formulas, please look at
        # https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_from_cross-_and_dot-products

        v12 = Geom.Vec(p2, p1)
        v13 = Geom.Vec(p3, p1)
        v21 = Geom.Vec(p1, p2)
        v23 = Geom.Vec(p3, p2)
        v31 = Geom.Vec(p1, p3)
        v32 = Geom.Vec(p2, p3)

        v12Len = v12.magnitude()
        v13Len = v13.magnitude()
        v23Len = v23.magnitude()

        vCross = v12.crossed(v23)
        vCrossLen = vCross.magnitude()
        if vCrossLen < epsilon:
            raise RuntimeError("All three points are on the same line")

        invDen = 1.0 / (2.0 * vCrossLen * vCrossLen)  # Inverted denominator

        # Weights
        w1 = v23Len * v23Len * v12.dot(v13) * invDen
        w2 = v13Len * v13Len * v21.dot(v23) * invDen
        w3 = v12Len * v12Len * v31.dot(v32) * invDen

        return Arc3Pnt._calcBaryCenter(w1, p1, w2, p2, w3, p3)

    @staticmethod
    def _basisAngle(vec, u, v):
        # All 3 vectors must be normalized

        uAngle = math.acos(u.dot(vec))
        vAngleCos = v.dot(vec)

        if vAngleCos > 0.0:
            uAngle = (2.0 * math.pi) - uAngle

        return uAngle

    @staticmethod
    def _calcAngle(v1, v2, v3, vNorm):
        nv1 = v1.normalized()
        nv2 = v2.normalized()
        nv3 = v3.normalized()
        # vNorm must be already normalized

        pnv1 = vNorm.crossed(nv1)

        angle2 = Arc3Pnt._basisAngle(nv2, nv1, pnv1)
        angle3 = Arc3Pnt._basisAngle(nv3, nv1, pnv1)

        if (angle2 + epsilon) > angle3:
            return v1.angle(v3)
        else:
            return - ((2.0 * math.pi) - v1.angle(v3))

    def angle(self):
        return self._angle

    def radius(self):
        return self._centerPt.distance(self._startPt)

    def length(self):
        return math.fabs(self.radius() * self._angle)

    def paramRatio(self):
        return 1.0 / self.length()

    def partLength(self, dt):
        return self.radius() * self._angle * dt

    def startPt(self):
        return self._startPt

    def endPt(self):
        return self._endPt

    def centerPt(self):
        return self._centerPt

    def paramPt(self, t):
        if t < epsilon:
            return self._startPt
        if (t + epsilon) > 1.0:
            return self._endPt

        paramVec = self._startVec.rotated(self._axis, self._angle * t)
        return self._centerPt.translated(paramVec)

    def startTangent(self):
        return self.paramTangent(0.0)

    def endTangent(self):
        return self.paramTangent(1.0)

    def paramTangent(self, t):
        if t < epsilon:
            t = 0.0
        if (t + epsilon) > 1.0:
            t = 1.0

        dt = 0.02

        dArc = None
        if (1.0 - t) > dt:
            pt1 = self.paramPt(t)
            pt2 = self.paramPt(t + dt)

            dArc = Geom.Vec(pt1, pt2)
        else:
            pt1 = self.paramPt(t - dt)
            pt2 = self.paramPt(t)

            dArc = Geom.Vec(pt1, pt2)
        dArc.normalize()

        return dArc

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
        def __init__(self, startIndex, closeSegm = False):
            self.startIndex = startIndex

            if not closeSegm:
                self.endIndex = startIndex + 1
            else:
                self.endIndex = 0

    class _ArcSegmData:
        def __init__(self, ptList, p1Index, closeSegm = False):
            self.p1Index = p1Index
            self.p2Index = p1Index + 1
            if not closeSegm:
                self.p3Index = p1Index + 2
            else:
                self.p3Index = 0

            self.arc = Arc3Pnt(ptList[self.p1Index], ptList[self.p2Index],ptList[self.p3Index])

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
        for edgeIndex in range(len(edges)):
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

    def segmStartTangent(self, id, normalize = False):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
            endPtId = self._segmList[id].data.endIndex

            tangVec = Geom.Vec(self._ptList[startPtId], self._ptList[endPtId])
            if normalize:
                tangVec.normalize()

            return tangVec
        else:
            return self._segmList[id].data.arc.startTangent()

    def segmStartBisector(self, id, normalize = False):
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

    def segmEndTangent(self, id, normalize = False):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
            endPtId = self._segmList[id].data.endIndex

            tangVec = Geom.Vec(self._ptList[endPtId], self._ptList[startPtId])
            if normalize:
                tangVec.normalize()

            return tangVec
        else:
            return self._segmList[id].data.arc.endTangent()

    def segmEndBisector(self, id, normalize = False):
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
        for edge in range(lastSegmId):
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

class ModelAssembler:
    # Beam types
    BT_Square = 0
    BT_Circle = 1

    # Beam type names
    _squareBTypeName = "square"
    _circleBTypeName = "circle"

    @staticmethod
    def correctBeamType(beamType):
        return bool(beamType == ModelAssembler.BT_Square or beamType == ModelAssembler.BT_Circle)

    @staticmethod
    def writeBeamType(bt):
        if bt == ModelAssembler.BT_Square:
            return ModelAssembler._squareBTypeName
        elif bt == ModelAssembler.BT_Circle:
            return ModelAssembler._circleBTypeName
        else:
            raise RuntimeError("Invalid beam type")

    @staticmethod
    def parseBeamType(bt):
        if bt == ModelAssembler._squareBTypeName:
            return ModelAssembler.BT_Square
        elif bt == ModelAssembler._circleBTypeName:
            return ModelAssembler.BT_Circle
        else:
            raise RuntimeError("Invalid beam type string")

    def __init__(self, doc):
        self._doc = doc
        self._modelGr = None

    def beginModel(self, modelGr):
        if self._modelGr is not None:
            raise RuntimeError("beginModel() called twice")

        self._modelGr = modelGr
        if modelGr is None:
            raise RuntimeError("modelGr is NULL")

    def endModel(self):
        if self._modelGr is None:
            raise RuntimeError("Called endModel() before beginModel()")

        finishedModel = self._modelGr
        self._modelGr = None

        return finishedModel

    def _createBaseBeam_Square(self, length, radiusH, radiusV, angle):
        diameterH = radiusH * 2.0
        diameterV = radiusV * 2.0

        beamGeom = lx.Block.createIn(self._doc)
        beamGeom.setLength(length)
        beamGeom.setWidth(diameterH)
        beamGeom.setHeight(diameterV)

        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(beamGeom)

        beam.translate(Geom.Vec(0.0, -radiusH, -radiusV), Geom.CoordSpace_WCS)

        if math.fabs(angle) > epsilon:
            angleAxis = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(1.0, 0.0, 0.0))
            beam.rotate(angleAxis, angle, Geom.CoordSpace_WCS)

        return beam

    def _createBaseBeam_Circle(self, length, radius):
        beamGeom = lx.RightCircularCylinder .createIn(self._doc)
        beamGeom.setHeight(length)
        beamGeom.setRadius(radius)

        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(beamGeom)

        rotAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 1, 0))
        beam.rotate(rotAxis, math.radians(90), Geom.CoordSpace_WCS)

        return beam

    def _createBaseBeam(self, beamType, length, radiusH, radiusV, angle):
        if not ModelAssembler.correctBeamType(beamType):
            raise RuntimeError("Invalid beam type")

        if beamType == ModelAssembler.BT_Square:
            return self._createBaseBeam_Square(length, radiusH, radiusV, angle)
        else:
            if abs(radiusH - radiusV) > epsilon:
                raise RuntimeError("Radii must be equal")

            return self._createBaseBeam_Circle(length, radiusH)

    def addXBeam(self, beamType, startPt, length, radiusH, radiusV, angle=0.0):
        if self._modelGr is None:
            raise RuntimeError("Called addXBeam() before beginModel()")

        beam = self._createBaseBeam(beamType, length, radiusH, radiusV, angle)
        beam.translate(Geom.Vec(startPt.x(),
                                          startPt.y(),
                                          startPt.z()),
                                 Geom.CoordSpace_WCS)

        self._modelGr.addSubElement(beam)

    def addXBeamUniform(self, beamType, startPt, length, radius, angle=0.0):
        self.addXBeam(beamType, startPt, length, radius, radius, angle)

    def addYBeam(self, beamType, startPt, length, radiusH, radiusV, angle):
        if self._modelGr is None:
            raise RuntimeError("Called addYBeam() before beginModel()")

        beam = self._createBaseBeam(beamType, length, radiusH, radiusV, angle)

        rotAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))
        beam.rotate(rotAxis, math.radians(90), Geom.CoordSpace_WCS)

        beam.translate(Geom.Vec(startPt.x(),
                                          startPt.y(),
                                          startPt.z()),
                                 Geom.CoordSpace_WCS)

        self._modelGr.addSubElement(beam)

    def addYBeamUniform(self, beamType, startPt, length, radius, angle=0.0):
        self.addYBeam(beamType, startPt, length, radius, radius, angle)

    def addZBeam(self, beamType, startPt, length, radiusH, radiusV, angle=0.0):
        if self._modelGr is None:
            raise RuntimeError("Called addZBeam() before beginModel()")

        beam = self._createBaseBeam(beamType, length, radiusH, radiusV, angle)

        rotAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 1, 0))
        beam.rotate(rotAxis, math.radians(-90), Geom.CoordSpace_WCS)

        beam.translate(Geom.Vec(startPt.x(),
                                          startPt.y(),
                                          startPt.z()),
                                 Geom.CoordSpace_WCS)

        self._modelGr.addSubElement(beam)

    def addZBeamUniform(self, beamType, startPt, length, radius, angle=0.0):
        self.addZBeam(beamType, startPt, length, radius, radius, angle)

    def addBeam(self, beamType, startPt, endPt, radiusH, radiusV, angle=0.0):
        beamVec = Geom.Vec(startPt, endPt)
        # print "beamVec = ({}, {}, {})".format(beamVec.x(), beamVec.y(), beamVec.z())
        beamLen = beamVec.magnitude()
        # myBeamLen = math.sqrt(beamVec.x() * beamVec.x() + beamVec.y() * beamVec.y() + beamVec.z() * beamVec.z())
        # print "beamLen = {}, myBeamLen = {}".format(beamLen, myBeamLen)
        beamAngleH, beamAngleV = angleVec(beamVec)
        # print "beamAngleH = {}, beamAngleV = {}".format(beamAngleH, beamAngleV)

        beam = self._createBaseBeam(beamType, beamLen, radiusH, radiusV, angle)

        rotAxisV = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 1, 0))
        beam.rotate(rotAxisV, beamAngleV, Geom.CoordSpace_WCS)

        rotAxisH = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 0, 1))
        beam.rotate(rotAxisH, beamAngleH, Geom.CoordSpace_WCS)

        beam.translate(Geom.Vec(startPt.x(),
                                          startPt.y(),
                                          startPt.z()),
                                 Geom.CoordSpace_WCS)

        self._modelGr.addSubElement(beam)

    def addBeamUniform(self, beamType, startPt, endPt, radius, angle=0.0):
        self.addBeam(beamType, startPt, endPt, radius, radius, angle)

    @staticmethod
    def _preapareRotTransf(angle):
        angleAxis = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(1.0, 0.0, 0.0))

        rotTr = Geom.Trsf()
        if math.fabs(angle) > epsilon:
            rotTr.setRotation(angleAxis, angle)

        return rotTr

    @staticmethod
    def _addProfilePoints_Square(radiusH, radiusV, angle, vtxList):
        rotTr = ModelAssembler._preapareRotTransf(angle)

        vtx = Geom.Pnt(0.0, radiusH, radiusV)
        vtx.transform(rotTr)
        vtxList.append(vtx)

        vtx = Geom.Pnt(0.0, radiusH, -radiusV)
        vtx.transform(rotTr)
        vtxList.append(vtx)

        vtx = Geom.Pnt(0.0, -radiusH, -radiusV)
        vtx.transform(rotTr)
        vtxList.append(vtx)

        vtx = Geom.Pnt(0.0, -radiusH, radiusV)
        vtx.transform(rotTr)
        vtxList.append(vtx)

    @staticmethod
    def _findCircleDivAngle(radius, perfAngle, minEdgeLen, minVtxCount):
        twoPi = 2.0 * math.pi

        perfDivAngle = math.pi - perfAngle
        perfDivCount = math.ceil(twoPi / perfDivAngle)

        divAngle = twoPi / perfDivCount

        radiusSq = radius * radius
        minEdgeLenSq = minEdgeLen * minEdgeLen
        edgeLenSq = radiusSq + radiusSq + 2.0 * radiusSq * math.cos(divAngle)
        if (edgeLenSq + epsilon) < minEdgeLenSq:
            twoRadiusSq = radiusSq + radiusSq
            edgeDivAngleCos = (twoRadiusSq - edgeLenSq) / twoRadiusSq
            edgeDivAngle = math.acos(edgeDivAngleCos)

            edgeDivCount = math.floor(twoPi / edgeDivAngle)
            divAngle = twoPi / edgeDivCount

        divCount = int(twoPi / divAngle)
        if divCount < minVtxCount:
            divAngle = twoPi / minVtxCount

        return divAngle

    @staticmethod
    def _addProfilePoints_Circle(radius, vtxList):
        perfAngle = 0.94 * math.pi
        minEdgeLen = min(0.1, radius / 8)
        divAngle = ModelAssembler._findCircleDivAngle(radius, perfAngle, minEdgeLen, 8)

        srcVtx = Geom.Pnt(0.0, 0.0, radius)
        twoPi = 2.0 * math.pi
        angleAxis = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(1.0, 0.0, 0.0))
        currAngle = twoPi
        while currAngle > epsilon:
            vtxList.append(srcVtx.rotated(angleAxis, currAngle))
            currAngle -= divAngle

    @staticmethod
    def _addProfilePoints(beamType, radiusH, radiusV, angle, vtxList):
        if beamType == ModelAssembler.BT_Square:
            ModelAssembler._addProfilePoints_Square(radiusH, radiusV, angle, vtxList)
        else:
            if abs(radiusH - radiusV) > epsilon:
                raise RuntimeError("Radii must be equal")

            ModelAssembler._addProfilePoints_Circle(radiusH, vtxList)

    @staticmethod
    def _appenExtrusionSegm(extrPos, extrTangent, vtxList, indexList, profVtxList):
        profVtxCount = len(profVtxList)
        extrStartId = len(vtxList) - profVtxCount

        # Generate new vertices
        extrTrsf = ModelAssembler._calcTransfByTangent(extrTangent)
        extrTrVec = Geom.Vec(extrPos.x(), extrPos.y(), extrPos.z())
        for profVtx in profVtxList:
            trProfVtx = profVtx.transformed(extrTrsf)
            trProfVtx.translate(extrTrVec)

            vtxList.append(trProfVtx)

        # Generate bridge faces
        for profVtxId in range(profVtxCount):
            startVtxId = extrStartId + profVtxId
            endVtxId = extrStartId + ((profVtxId + 1) % profVtxCount)

            indexList.append(endVtxId)
            indexList.append(startVtxId)
            indexList.append(startVtxId + profVtxCount)
            indexList.append(-2)
            indexList.append(-1)

            indexList.append(endVtxId)
            indexList.append(startVtxId + profVtxCount)
            indexList.append(endVtxId + profVtxCount)
            indexList.append(-2)
            indexList.append(-1)

    @staticmethod
    def _calcTransfByTangent(tangent):
        angleH, angleV = angleVec(tangent)

        rotAxisV = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 1, 0))
        trsfV = Geom.Trsf()
        trsfV.setRotation(rotAxisV, angleV)

        rotAxisH = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 0, 1))
        trsfH = Geom.Trsf()
        trsfH.setRotation(rotAxisH, angleH)

        return trsfH * trsfV

    @staticmethod
    def _calcExtrusionStep(arc):
        arcRadius = arc.radius()

        perfAngle = 0.96 * math.pi
        minEdgeLen = min(0.1, arcRadius / 8)
        divAngle = ModelAssembler._findCircleDivAngle(arcRadius, perfAngle, minEdgeLen, 8)

        arcAngle = math.fabs(arc.angle())
        divNum = int(arcAngle // divAngle)
        if (math.fabs(arcAngle % divAngle) > epsilon) or (divNum == 0):
            divNum += 1

        return 1.0 / float(divNum)

    def addSubmodel(self, subMdl, transform=None):
        beamList = subMdl.getSubElements()
        for beam in beamList:
            if transform is not None:
                beamTr = beam.getTransform()
                newTr = transform * beamTr
                beam.setTransform(newTr)

            self._modelGr.addSubElement(beam)

class Beispiel(lx.Element):
    _classID = "{9FA12082-EE3E-4A93-942A-0E5D8E2C83BA}"
    _headerPropName = "Beispiel"
    _groupPropName = "Beispiel parameters"

    #Parameters
    _lengthStateParamName = "Length stage"
    _widthStateParamName = "Width stage"
    _heightStageParamName = "Height stage"
    _numberElementInHeightParamName = "Ne in height "
    _numberElementInLengthParamName = "Ne in length"
    _totalLengthParamName = "Total length"
    _totalHeightParamName = "Total height"

    def getGlobalClassId(self):
        return Base.GlobalId(Beispiel._classID)

    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Beispiel", "OpenLxApp.Element")
        # Register properties

        self.setPropertyHeader(lxstr(Beispiel._headerPropName), -1)
        self.setPropertyGroupName(lxstr(Beispiel._groupPropName), -1)

        self._lengthState = self.registerPropertyDouble(Beispiel._lengthStateParamName, \
                                                        2.5, \
                                                        lx.Property.VISIBLE, \
                                                        lx.Property.EDITABLE, \
                                                        -1)

        self._widthState = self.registerPropertyDouble(Beispiel._widthStateParamName, \
                                                         0.75, \
                                                         lx.Property.VISIBLE, \
                                                         lx.Property.EDITABLE, \
                                                         -1)

        self._heightStage = self.registerPropertyDouble(Beispiel._heightStageParamName, \
                                                            1.97, \
                                                            lx.Property.VISIBLE, \
                                                            lx.Property.EDITABLE, \
                                                            -1)

        self._numberElementInHeight = self.registerPropertyInteger(Beispiel._numberElementInHeightParamName, \
                                                             4, \
                                                             lx.Property.VISIBLE, \
                                                             lx.Property.EDITABLE, \
                                                             -1)

        self._numberElementInLength = self.registerPropertyInteger(Beispiel._numberElementInLengthParamName, \
                                                                   6, \
                                                                   lx.Property.VISIBLE, \
                                                                   lx.Property.EDITABLE, \
                                                                   -1)

        self._totalLength = self.registerPropertyDouble(Beispiel._totalLengthParamName, \
                                                        self._lengthState.getValue() *
                                                             self._numberElementInLength.getValue(),
                                                             lx.Property.VISIBLE, \
                                                        lx.Property.EDITABLE, \
                                                        -1)

        self._totalHeight = self.registerPropertyDouble(Beispiel._totalHeightParamName, \
                                                        self._heightStage.getValue() *
                                                             self._numberElementInHeight.getValue(),
                                                             lx.Property.VISIBLE, \
                                                        lx.Property.EDITABLE, \
                                                        -1)

        self._lengthState.setSteps(0.1)
        self._widthState.setSteps(0.01)
        self._heightStage.setSteps(0.1)

        
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

    def setLengthState(self, param):
        with EditMode(self.getDocument()):
            self._lengthState.setValue(clamp(param, epsilon, maxValue))
            self._totalLength.setValue(self._lengthState.getValue() * float(self._numberElementInLength.getValue()))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))

    def setWidthState(self, param):
        with EditMode(self.getDocument()):
            self._widthState.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))

    def setHeightState(self, param):
        with EditMode(self.getDocument()):
            self._heightStage.setValue(clamp(param, epsilon, maxValue))
            self._totalHeight.setValue(self._heightStage.getValue() * float(self._numberElementInHeight.getValue()))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))

    def setNumberElementsInHeight(self, param):
        with EditMode(self.getDocument()):
            self._numberElementInHeight.setValue(clamp(param, 1, 10000))
            self._totalHeight.setValue(self._heightStage.getValue() * float(self._numberElementInHeight.getValue()))
            self._updateGeometry()
        if param < 1:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too small"))
        elif param >= 10000:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))

    def setNumberElementsInLength(self, param):
        with EditMode(self.getDocument()):
            self._numberElementInLength.setValue(clamp(param, 1, 10000))
            self._totalLength.setValue(self._lengthState.getValue() * float(self._numberElementInLength.getValue()))
            self._updateGeometry()
        if param < 1:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too small"))
        elif param >= 10000:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))

    def setTotalLength(self, param):
        with EditMode(self.getDocument()):
            self._totalLength.setValue(clamp(param, epsilon, maxValue))
            self._numberElementInLength.setValue(int((self._totalLength.getValue() / self._lengthState.getValue()) + 0.5))
            self._lengthState.setValue(self._totalLength.getValue() / float(self._numberElementInLength.getValue()))
            self._updateGeometry()
        if param <= epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too small"))
        elif param >= maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))

    def setTotalHeight(self, param):
        with EditMode(self.getDocument()):
            self._totalHeight.setValue(clamp(param, epsilon, maxValue))
            self._numberElementInHeight.setValue(int((self._totalHeight.getValue() / self._heightStage.getValue()) + 0.5))
            self._heightStage.setValue(self._totalHeight.getValue() / float(self._numberElementInHeight.getValue()))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("Value is too big"))


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
    def _createSubElementFace(listPoint):
        edgeList = Topo.vector_Edge(4)

        edgeList[0] = Topo.EdgeTool.makeEdge(listPoint[0], listPoint[1])
        edgeList[1] = Topo.EdgeTool.makeEdge(listPoint[1], listPoint[2])
        edgeList[2] = Topo.EdgeTool.makeEdge(listPoint[2], listPoint[3])
        edgeList[3] = Topo.EdgeTool.makeEdge(listPoint[3], listPoint[0])

        wire = Topo.WireTool.makeWire(edgeList, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())

        geom = lx.createCurveBoundedPlaneFromFace(doc, face)

        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(geom)
        return elem

    def createSegment(self, model, pos, ifFirst, ifLeft, ifRight, ifBase):
        height = self._heightStage.getValue()
        length = self._lengthState.getValue()
        width = self._widthState.getValue()
        x = pos.x()
        y = pos.y()
        z = pos.z()
        widthBetween = width - 0.07
        lengthBetween = length - 0.014
        heightConnection = 0.175
        radiusConnection = 0.025

        radiusSupport = 0.01

        heightMainBeam = height - heightConnection
        radiusMainBeam = 0.035

        pntTopLeftMainBeam = Geom.Pnt(x, y, z)
        pntBottomLeftMainBeam = Geom.Pnt(-widthBetween + x, y, z)
        pntTopRightMainBeam = Geom.Pnt(x, lengthBetween + y, z)
        pntBottomRightMainBeam = Geom.Pnt(-widthBetween + x, lengthBetween + y, z)

        pntTopLeftMainConnectionBeam = Geom.Pnt(x, y, z + heightMainBeam)
        pntBottomLeftConnectionBeam = Geom.Pnt(-widthBetween + x, y, z + heightMainBeam)
        pntTopRightConnectionBeam = Geom.Pnt(x, y + lengthBetween, z + heightMainBeam)
        pntBottomRightConnectionBeam = Geom.Pnt(-widthBetween + x, y + lengthBetween, z + heightMainBeam)

        model.addZBeamUniform(ModelAssembler.BT_Circle, pntTopRightMainBeam, heightMainBeam, radiusMainBeam, 0.0)
        model.addZBeamUniform(ModelAssembler.BT_Circle, pntBottomRightMainBeam, heightMainBeam, radiusMainBeam, 0.0)

        model.addZBeamUniform(ModelAssembler.BT_Circle, pntTopRightConnectionBeam, heightConnection, radiusConnection, 0.0)
        model.addZBeamUniform(ModelAssembler.BT_Circle, pntBottomRightConnectionBeam, heightConnection, radiusConnection, 0.0)

        #x beam
        pntTopLeftXSupport = Geom.Pnt(x, y, 0.11 + z)
        pntTopRightXSupport = Geom.Pnt(x, y + lengthBetween, z + heightMainBeam)
        model.addBeamUniform(ModelAssembler.BT_Circle, pntTopLeftXSupport, pntTopRightXSupport, radiusSupport, 0.0)


        #add middle supports
        pntTopLeftMiddleSupport = Geom.Pnt(x, y, z + heightMainBeam * 0.5)
        pntBottomLeftMiddleSupport = Geom.Pnt(-widthBetween + x, y, z + (heightMainBeam * 0.5))
        pntTopRightMiddleSupport = Geom.Pnt(x, y + lengthBetween, z + (heightMainBeam * 0.5))
        pntBottomRightMiddleSupport = Geom.Pnt(-widthBetween + x, y + lengthBetween, z + (heightMainBeam * 0.5))

        model.addBeamUniform(ModelAssembler.BT_Circle, pntTopLeftMiddleSupport, pntTopRightMiddleSupport, radiusSupport, 0.0)

        if ifRight:
            model.addBeamUniform(ModelAssembler.BT_Circle, pntBottomRightMiddleSupport, pntTopRightMiddleSupport, radiusSupport, 0.0)
        if ifLeft:
            model.addBeamUniform(ModelAssembler.BT_Circle, pntTopLeftMiddleSupport, pntBottomLeftMiddleSupport, radiusSupport, 0.0)

        if ifFirst:
            model.addZBeamUniform(ModelAssembler.BT_Circle, pntTopLeftMainBeam, heightMainBeam, radiusMainBeam, 0.0)
            model.addZBeamUniform(ModelAssembler.BT_Circle, pntBottomLeftMainBeam, heightMainBeam, radiusMainBeam, 0.0)
            model.addZBeamUniform(ModelAssembler.BT_Circle, pntTopLeftMainConnectionBeam, heightConnection, radiusConnection, 0.0)
            model.addZBeamUniform(ModelAssembler.BT_Circle, pntBottomLeftConnectionBeam, heightConnection, radiusConnection, 0.0)

        if ifBase:
            pntTopLeftBottomSupport = Geom.Pnt(x, y, z + 0.11)
            pntBottomLeftBottomSupport = Geom.Pnt(-widthBetween + x, y, 0.11 + z)
            pntTopRightBottomSupport = Geom.Pnt(x, lengthBetween + y, z + 0.11)
            pntBottomRightBottomSupport = Geom.Pnt(-widthBetween + x, y + lengthBetween, z + 0.11)


            model.addBeamUniform(ModelAssembler.BT_Circle, pntTopLeftBottomSupport, pntTopRightBottomSupport, radiusSupport, 0.0)
            model.addBeamUniform(ModelAssembler.BT_Circle, pntBottomLeftBottomSupport, pntTopLeftBottomSupport, radiusSupport, 0.0)
            model.addBeamUniform(ModelAssembler.BT_Circle, pntBottomRightBottomSupport, pntTopRightBottomSupport, radiusSupport, 0.0)

        #create podium
        defColor = Base.Color(168, 81, 0)

        pnt0 = Geom.Pnt(x, lengthBetween + y, z + heightMainBeam)
        pnt1 = Geom.Pnt(-widthBetween + x, y + lengthBetween, z + heightMainBeam)
        pnt2 = Geom.Pnt(-widthBetween + x, y + lengthBetween, z + heightMainBeam + 0.045)
        pnt3 = Geom.Pnt(x, y + lengthBetween, z + heightMainBeam + 0.045)
        pnt4 = Geom.Pnt(x, y, z + heightMainBeam + 0.045)
        pnt5 = Geom.Pnt(-widthBetween + x, y, z + heightMainBeam + 0.045)
        pnt6 = Geom.Pnt(-widthBetween + x, y, z + heightMainBeam)
        pnt7 = Geom.Pnt(x, y, z + heightMainBeam)
        pnt8 = Geom.Pnt(x, y + lengthBetween, z + heightMainBeam + 0.17)
        pnt9 = Geom.Pnt(x, y, z + heightMainBeam + 0.17)
        pnt10 = Geom.Pnt(-widthBetween + x, y, z + heightMainBeam + 0.17)
        pnt11 = Geom.Pnt(-widthBetween + x, y + lengthBetween, z + heightMainBeam + 0.17)

        mainPlateElem = self._createSubElementFace([pnt3, pnt2, pnt5, pnt4])
        mainPlateElem.setDiffuseColor(defColor)
        self.addSubElement(mainPlateElem)
        self.addSubElement(self._createSubElementFace([pnt1, pnt2, pnt5, pnt6]))
        bottomPlateElem = self._createSubElementFace([pnt8, pnt9, pnt4, pnt3])
        bottomPlateElem.setDiffuseColor(defColor)
        self.addSubElement(bottomPlateElem)
        self.addSubElement(self._createSubElementFace([pnt0, pnt3, pnt4, pnt7]))

        if ifLeft:
            self.addSubElement(self._createSubElementFace([pnt4, pnt7, pnt6, pnt5]))
            elemLeft = self._createSubElementFace([pnt9, pnt10, pnt5, pnt4])
            elemLeft.setDiffuseColor(defColor)
            self.addSubElement(elemLeft)
        if ifRight:
            self.addSubElement(self._createSubElementFace([pnt0, pnt1, pnt2, pnt3]))
            elemRight = self._createSubElementFace([pnt2, pnt3, pnt8, pnt11])
            elemRight.setDiffuseColor(defColor)
            self.addSubElement(elemRight)

    def _createGeometry(self):
        numberVertical = self._numberElementInHeight.getValue()
        numberHorizontal = self._numberElementInLength.getValue()
        height = self._heightStage.getValue()
        length = self._lengthState.getValue() - 0.014

        model = ModelAssembler(doc)
        model.beginModel(self)



        #createSegment(self, model, pos, ifFirst, ifLeft, ifRight):
        for l in range(numberHorizontal):
            for h in range(numberVertical):
                ifFirst = False
                ifLeft = False
                ifRight = False
                ifBase = False
                if h is 0:
                    ifBase = True
                if l is 0:
                    ifLeft = True
                    ifFirst = True
                if l is numberHorizontal - 1:
                    ifRight = True
                self.createSegment(model, Geom.Pnt(0.0, length * l, height * h), ifFirst, ifLeft, ifRight, ifBase)
        #model.endModel()




    def _updateGeometry(self):
        doc = self.getDocument()

        with EditMode(doc):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == Beispiel._lengthStateParamName:
            self.setLengthState(self._lengthState.getValue())
        elif aPropertyName == Beispiel._widthStateParamName:
            self.setWidthState(self._widthState.getValue())
        elif aPropertyName == Beispiel._heightStageParamName:
            self.setHeightState(self._heightStage.getValue())
        elif aPropertyName == Beispiel._numberElementInHeightParamName:
            self.setNumberElementsInHeight(self._numberElementInHeight.getValue())
        elif aPropertyName == Beispiel._numberElementInLengthParamName:
            self.setNumberElementsInLength(self._numberElementInLength.getValue())
        elif aPropertyName == Beispiel._totalLengthParamName:
            self.setTotalLength(self._totalLength.getValue())
        elif aPropertyName == Beispiel._totalHeightParamName:
            self.setTotalHeight(self._totalHeight.getValue())

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
    doc.registerPythonScript(Base.GlobalId("{CE873EBA-C7DE-4D06-ADF8-130FB2CA5D8C}"))

    try:
        beispeils = Beispiel(doc)
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
        else:
            pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

        beispeils.setLocalPlacement(pos)
    except Exception as e:
        print(e.message)
        traceback.print_exc()
    finally:
        doc.recompute()