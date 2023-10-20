# coding=utf-8
# OpenLexocad libraries
# version 2.0   07.05.2020

# attributes
#   version 2.0
#   - innovations applied

# ========================================
# ====  Supported by Roman Davydiuk   ====
# ====  Mail: davydjukroman@gmail.com ====
# ====  Skype: live:davydjukroman     ====
# ========================================
import math

import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Draw, Geom, Topo

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

st = Topo.ShapeTool

doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()
CW_COLOR = 3027
epsilon = 0.0001
pi2 = math.pi * 0.5

listOfProfiles = [
    #   type    b      h      t      s      angle   btw_dist
    ['AU 14', 0.750, 0.408, 0.01, 0.0083, 47.8, 0.303],
    ['AU 16', 0.750, 0.411, 0.0115, 0.0093, 47.8, 0.303],
    ['AU 18', 0.750, 0.441, 0.0105, 0.0091, 54.7, 0.336],
    ['AU 20', 0.750, 0.444, 0.012, 0.01, 54.7, 0.336],
    ['AU 23', 0.750, 0.447, 0.013, 0.0095, 59.6, 0.374],
    ['AU 25', 0.750, 0.450, 0.0145, 0.0102, 59.6, 0.374],

    ['PU 12', 0.600, 0.360, 0.0098, 0.009, 50.4, 0.258],
    ['PU 12S', 0.600, 0.360, 0.010, 0.010, 50.4, 0.257],

    ['PU 18ˉ¹', 0.600, 0.430, 0.0102, 0.0084, 57.5, 0.269],
    ['PU 18', 0.600, 0.430, 0.0112, 0.009, 57.5, 0.269],
    ['PU 18⁺¹', 0.600, 0.430, 0.0122, 0.0095, 57.5, 0.269],

    ['PU 22ˉ¹', 0.600, 0.450, 0.0111, 0.009, 62.4, 0.297],
    ['PU 22', 0.600, 0.450, 0.0121, 0.0095, 62.4, 0.297],
    ['PU 22⁺¹', 0.600, 0.450, 0.0131, 0.010, 62.4, 0.297],

    ['PU 28ˉ¹', 0.600, 0.452, 0.0142, 0.0097, 68.0, 0.339],
    ['PU 28', 0.600, 0.454, 0.0152, 0.0101, 68.0, 0.339],
    ['PU 28⁺¹', 0.600, 0.456, 0.0162, 0.0105, 68.0, 0.339],

    ['PU 32ˉ¹', 0.600, 0.452, 0.0185, 0.0106, 68.1, 0.342],
    ['PU 32', 0.600, 0.452, 0.0195, 0.011, 68.1, 0.342],
    ['PU 32⁺¹', 0.600, 0.452, 0.0205, 0.0114, 68.1, 0.342],

    ['GU 6N', 0.600, 0.309, 0.006, 0.006, 42.5, 0.248],
    ['GU 7N', 0.600, 0.310, 0.0065, 0.0064, 42.5, 0.248],
    ['GU 7S', 0.600, 0.311, 0.0072, 0.0069, 42.5, 0.248],
    ['GU 7HWS', 0.600, 0.312, 0.0073, 0.0069, 42.5, 0.248],
    ['GU 8N', 0.600, 0.312, 0.0075, 0.0071, 42.5, 0.248],
    ['GU 8S', 0.600, 0.313, 0.008, 0.0075, 42.5, 0.248],

    ['GU 10N', 0.600, 0.316, 0.009, 0.0068, 52.0, 0.283],
    ['GU 11N', 0.600, 0.318, 0.010, 0.0074, 52.0, 0.283],
    ['GU 12N', 0.600, 0.320, 0.011, 0.008, 52.0, 0.283],

    ['GU 13N', 0.600, 0.418, 0.009, 0.0074, 54.3, 0.250],
    ['GU 14N', 0.600, 0.420, 0.010, 0.008, 54.3, 0.250],
    ['GU 15N', 0.600, 0.422, 0.011, 0.0086, 54.3, 0.250],

    ['GU 16N', 0.600, 0.430, 0.0102, 0.0084, 57.5, 0.269],
    ['GU 18N', 0.600, 0.430, 0.0112, 0.009, 57.5, 0.269],
    ['GU 20N', 0.600, 0.430, 0.0122, 0.0095, 57.5, 0.269],

    ['GU 21N', 0.600, 0.450, 0.0111, 0.009, 62.4, 0.297],
    ['GU 22N', 0.600, 0.450, 0.0121, 0.0095, 62.4, 0.297],
    ['GU 23N', 0.600, 0.450, 0.0131, 0.010, 62.4, 0.297],

    ['GU 27N', 0.600, 0.452, 0.0142, 0.0097, 68.0, 0.339],
    ['GU 28N', 0.600, 0.454, 0.0152, 0.0101, 68.0, 0.339],
    ['GU 30N', 0.600, 0.456, 0.0162, 0.0105, 68.0, 0.339],

    ['GU 31N', 0.600, 0.452, 0.0185, 0.0106, 68.1, 0.342],
    ['GU 32N', 0.600, 0.452, 0.0195, 0.011, 68.1, 0.342],
    ['GU 33N', 0.600, 0.452, 0.0205, 0.0114, 68.1, 0.342],

    ['GU 16-400', 0.400, 0.290, 0.0127, 0.0094, 82.1, 0.252],
    ['GU 18-400', 0.400, 0.292, 0.015, 0.0097, 82.1, 0.252]
]


def qstr(str):
    return Base.StringTool.toQString(lxstr(str))


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


def baseVecTranslate(pt, baseVec, dist):
    baseVec.normalize()
    return Geom.Pnt(
        pt.x() + (baseVec.x() * dist),
        pt.y() + (baseVec.y() * dist),
        pt.z() + (baseVec.z() * dist)
    )


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


def vecMagnitude2D(vec):
    return math.sqrt(vec.x() * vec.x() + vec.y() * vec.y())


def vecHExpandXZ(unitVec, hLength):
    if math.fabs(unitVec.z()) > epsilon:
        z = (hLength * unitVec.z()) / unitVec.x()
        return Geom.Vec(hLength, 0.0, z)
    else:
        return Geom.Vec(hLength, 0.0, 0.0)


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
        # For the formulas, please look at https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_from_cross-_and_dot-products

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

        dt = 0.001

        dArc = None
        if (1.0 - t) < dt:
            pt1 = self.paramPt(t - dt)
            pt2 = self.paramPt(t)

            dArc = Geom.Vec(pt1, pt2)
        elif (t - 0.0) < dt:
            pt1 = self.paramPt(t)
            pt2 = self.paramPt(t + dt)

            dArc = Geom.Vec(pt1, pt2)
        else:
            pt1 = self.paramPt(t - dt)
            pt2 = self.paramPt(t + dt)

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

        firstEdge = True
        startIndex = 0
        for edgeIndex in range(len(lineElem)):
            # edge = edges[edgeIndex]
            #
            # edgeTypeRes = Topo.EdgeTool.getGeomCurveType(edge)
            # if not edgeTypeRes.ok:
            #     raise RuntimeError("Can't get edge type")

            if lineElem[edgeIndex][0] == PolylineData.SegmType_Line:
                p1Res = lineElem[edgeIndex][1]
                if firstEdge:
                    newPD._ptList.append(Geom.Pnt(p1Res))
                    firstEdge = False

                p2Res = lineElem[edgeIndex][2]
                newPD._ptList.append(Geom.Pnt(p2Res))

                segmData = PolylineData._LineSegmData(startIndex, False)
                newPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))

                startIndex += 1
            elif lineElem[edgeIndex][0] == PolylineData.SegmType_Arc:
                p1Res = lineElem[edgeIndex][1]
                if firstEdge:
                    newPD._ptList.append(Geom.Pnt(p1Res))
                    firstEdge = False

                p2Res = lineElem[edgeIndex][2]
                newPD._ptList.append(Geom.Pnt(p2Res))

                p3Res = lineElem[edgeIndex][3]
                newPD._ptList.append(Geom.Pnt(p3Res))

                segmData = PolylineData._ArcSegmData(newPD._ptList, startIndex, False)
                newPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))

                startIndex += 2
            else:
                raise RuntimeError("Unsupported edge type")

        i_n = len(lineElem[len(lineElem) - 1]) - 1
        newPD._closed = lineElem[len(lineElem) - 1][i_n]
        return newPD

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
            return -self._segmList[id].data.arc.endTangent()

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
        lastSegmId = segmCount

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
        self._color = None

    def beginModel(self, modelGr):
        if self._modelGr is not None:
            raise RuntimeError("beginModel() called twice")

        self._modelGr = modelGr
        if modelGr is None:
            raise RuntimeError("modelGr is NULL")

    def setColor(self, color):
        self._color = color

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
        beamGeom.set_height(diameterV)

        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(beamGeom)
        if self._color is not None:
            beam.setDiffuseColor(self._color)

        beam.translate(Geom.Vec(0.0, -radiusH, -radiusV), Geom.CoordSpace_WCS)

        if math.fabs(angle) > epsilon:
            angleAxis = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(1.0, 0.0, 0.0))
            beam.rotate(angleAxis, angle, Geom.CoordSpace_WCS)

        return beam

    def _createBaseBeam_Circle(self, length, radius):
        beamGeom = lx.RightCircularCylinder.createIn(self._doc)
        beamGeom.set_height(length)
        beamGeom.setRadius(radius)

        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(beamGeom)
        if self._color is not None:
            beam.setDiffuseColor(self._color)
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

    def addCutBeam(self, beamType, startPt, endPt, radiusH, radiusV, startVec, endVec, angle=0.0):
        beamVec = Geom.Vec(startPt, endPt)
        dir = beamVec.normalized()
        # print "beamVec = ({}, {}, {})".format(beamVec.x(), beamVec.y(), beamVec.z())
        beamLen = beamVec.magnitude()
        # myBeamLen = math.sqrt(beamVec.x() * beamVec.x() + beamVec.y() * beamVec.y() + beamVec.z() * beamVec.z())
        # print "beamLen = {}, myBeamLen = {}".format(beamLen, myBeamLen)
        beamAngleH, beamAngleV = angleVec(beamVec)
        # print "beamAngleH = {}, beamAngleV = {}".format(beamAngleH, beamAngleV)

        beam = self._createBaseBeam(beamType, beamLen + 4. * radiusV, radiusH, radiusV, angle)

        rotAxisV = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 1, 0))
        beam.rotate(rotAxisV, beamAngleV, Geom.CoordSpace_WCS)

        rotAxisH = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 0, 1))
        beam.rotate(rotAxisH, beamAngleH, Geom.CoordSpace_WCS)

        beam.translate(Geom.Vec(startPt.x(), startPt.y(), startPt.z()), Geom.CoordSpace_WCS)
        trans = Geom.Vec(0.0 - 2. * radiusV * dir.x(), 0.0 - 2. * radiusV * dir.y(), 0.0 - 2. * radiusV * dir.z())
        # print()
        beam.translate(trans, Geom.CoordSpace_WCS)

        startNorm = Geom.Vec(-startVec.y(), startVec.x(), startVec.z())
        endNorm = Geom.Vec(endVec.y(), -endVec.x(), endVec.z())
        startDir = Geom.Dir(startNorm.x(), startNorm.y(), 0.0)
        endDir = Geom.Dir(endNorm)
        startPln = Geom.Pln(Geom.Pnt(startPt.x(), startPt.y(), startPt.z()), startDir)
        endPln = Geom.Pln(endPt, endDir)
        beam2 = lx.Element.createIn(self._doc)
        # beam2 = beam.getElement()
        geom = beam.getGeometry()
        beam2.setGeometry(geom)
        t = beam.getTransform()
        beam2.setTransform(t)
        doc.removeObject(beam)

        beam_start = lx.vector_Element()
        beam_end = lx.vector_Element()

        if lx.bop_splitByPlane(beam2, startPln, beam_start) != 0:
            print("Error in cut")
        doc.removeObject(beam_start[1])
        doc.removeObject(beam2)

        if lx.bop_splitByPlane(beam_start[0], endPln, beam_end) != 0:
            print("Error in cut")
        doc.removeObject(beam_start[0])
        doc.removeObject(beam_end[1])

        t = beam_end[0].getTransform()
        geom = beam_end[0].getGeometry()
        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(geom)
        beam.setTransform(t)
        doc.removeObject(beam_end[0])
        # doc.recompute()

        self._modelGr.addSubElement(beam)

    def addHorCutBeam(self, firstPntA, secondPntA, vRadius, hRadius, firstVec, secondVec):
        firstPnt = Geom.Pnt(firstPntA.x(), firstPntA.y(), firstPntA.z() - vRadius)
        secondPnt = Geom.Pnt(secondPntA.x(), secondPntA.y(), secondPntA.z() - vRadius)
        mainVec = Geom.Vec(firstPnt, secondPnt)

        firstAngle = Geom.Vec.angle(firstVec, Geom.Vec(mainVec.x(), mainVec.y(), 0.0))
        secondAngle = Geom.Vec.angle(secondVec, Geom.Vec(mainVec.x(), mainVec.y(), 0.0))

        firstStep = hRadius / math.sin(firstAngle)
        secondStep = hRadius / math.sin(secondAngle)

        firVec = firstVec.normalized()
        secVec = secondVec.normalized()
        firVec.scale(firstStep)
        secVec.scale(secondStep)
        listPoint = []
        listPoint.append(firstPnt.translated(firVec))
        listPoint.append(firstPnt.translated(firVec.reversed()))
        listPoint.append(secondPnt.translated(secVec.reversed()))
        listPoint.append(secondPnt.translated(secVec))

        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire,
                                                 Geom.Dir(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(0.0, 0.0, 1.0))),
                                                 vRadius * 2.0)
        geom = lx.FacetedBrep.createIn(self._doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(self._doc)
        subElem.setGeometry(geom)
        self._modelGr.addSubElement(subElem)

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

    def addSubElem(self, subElem):
        self._modelGr.addSubElement(subElem)

    def addSubmodel(self, subMdl, transform=None):
        beamList = subMdl.getSubElements()
        for beam in beamList:
            if transform is not None:
                beamTr = beam.getTransform()
                newTr = transform * beamTr
                beam.setTransform(newTr)

            self._modelGr.addSubElement(beam)


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

        return Geom.Pnt(x, y, 0.0)

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
        # if Line2D.collinear(l1, l2):
        #    return None

        dx = l2._pt.x() - l1._pt.x()
        dy = l2._pt.y() - l1._pt.y()

        if math.fabs(l2._dir.y()) > epsilon:
            t = (dx * l2._dir.y() - dy * l2._dir.x()) / (l1._dir.x() * l2._dir.y() - l1._dir.y() * l2._dir.x())
            return l1.paramPoint(t)
        else:
            t = (dy * l1._dir.x() - dx * l1._dir.y()) / (l1._dir.y() * l2._dir.x())
            return l2.paramPoint(t)


def vecsAreSame(v1, v2, tolerance=epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)


class PolylineReader:
    def __init__(self, polyLine):
        self.polyline = polyLine
        self.segmCount = polyLine.segmentCount()
        self.e = 0.0001
        self.pointListWithDistance = []
        self.segmentsList = []

        if self.segmCount <= 0:
            # print("There are anything segments")
            return

        for segmId in range(self.segmCount):
            segmType = self.polyline.segmentType(segmId)

            if segmType == PolylineData.SegmType_Line:
                startPt = self.polyline.segmStartPt(segmId)
                endPt = self.polyline.segmEndPt(segmId)
                lineSegment = self.SegmLine(startPt, endPt)
                self.segmentsList.append(lineSegment)

            elif segmType == PolylineData.SegmType_Arc:
                arc = PolylineData.segmArc(self.polyline, segmId)
                # print("Radius = ", arc.radius(), ", angle = ", arc.angle(), arc.angle() * 180.0 / math.pi)
                n = int(math.fabs(arc.angle() / (math.acos(((arc.radius() - self.e) / arc.radius())) * 2.0)))
                # print("N = ", n)
                for i in range(n):
                    pnt0 = arc.paramPt(float(i) / float(n))
                    pnt1 = arc.paramPt((float(float(i) + 1.0) / float(n)))
                    if ((float(float(i) + 1.0) / float(n))) <= 1.0:
                        lineSegment = self.SegmLine(pnt0, pnt1)
                        self.segmentsList.append(lineSegment)
                # print("ARC")
            else:
                # print("Unknown segment")
                return

    def getListPointWithDistanceOnPolyline(self, dist, radius, withLast):
        listPoint = []
        for segm in self.segmentsList:
            endPoint = self.segmentsList[len(self.segmentsList) - 1].p1
            if segm == self.segmentsList[len(self.segmentsList) - 1]:
                ifLast = True
            else:
                ifLast = False
            if len(listPoint) >= 1:
                distToPrev = segm.getDistanceToFirstPnt(listPoint[len(listPoint) - 1], dist)
            else:
                distToPrev = segm.getDistanceToFirstPnt(self.segmentsList[0].p0, radius)
            listSegmentPoint = segm.getListPointWithDistance(dist, ifLast, radius, distToPrev)
            if listSegmentPoint is not None:
                for pnt in listSegmentPoint:
                    if withLast is False:
                        pntPro1 = Geom.Pnt(pnt.x(), pnt.y(), 0.0)
                        pntPro2 = Geom.Pnt(endPoint.x(), endPoint.y(), 0.0)
                        if pntPro1.distance(pntPro2) < radius:
                            pass
                        else:
                            listPoint.append(pnt)
                    else:
                        listPoint.append(pnt)
        return listPoint

    class SegmLine:
        def __init__(self, startPnt, endPnt):
            self.p0 = startPnt
            self.p1 = endPnt
            self.p0x = startPnt.x()
            self.p0y = startPnt.y()
            self.p1x = endPnt.x()
            self.p1y = endPnt.y()
            self.vecSegm = Geom.Vec(startPnt, endPnt)
            self.len = self.vecSegm.magnitude()

        def getNumberOfParts(self, dist):
            n = self.vecSegm.magnitude() / dist
            return n

        def getPntByCoef(self, t):
            if t == 0:
                return self.p0
            elif t == 1:
                return self.p1
            elif 0 < t < 1:
                return self.p0.translated(self.vecSegm.scaled(t))
            else:
                # print("COEFICIENT T OUT OF RANGE!!!")
                return None

        def getPntByDist(self, dist):
            if dist == 0:
                return self.p0
            elif dist == self.len:
                return self.p1
            else:
                normalVec = self.vecSegm.normalized()
                resPnt = self.p0.translated(normalVec.multiplied(dist))
                return resPnt

        def getDistanceToFirstPnt(self, q, dist):
            qx = q.x()
            qy = q.y()
            len = 4.0 * math.pow(dist * 0.5, 2)
            p0x = self.p0x
            p0y = self.p0y
            dirVec = self.vecSegm.normalized()
            dx = dirVec.x()
            dy = dirVec.y()
            a = math.pow(dx, 2.0) + math.pow(dy, 2.0)
            b = (-2. * dx * qx) + (p0x * dx) + (dx * p0x) - (2.0 * dy * qy) + (p0y * dy) + (dy * p0y)
            c = (math.pow(qx, 2)) - (2.0 * qx * p0x) + (math.pow(p0x, 2)) + (math.pow(qy, 2)) - (2.0 * qy * p0y) + (
                math.pow(p0y, 2)) - len
            D = math.pow(b, 2) - (4.0 * a * c)
            if D > 0.0:
                t1 = (-b + math.sqrt(D)) / (2.0 * a)
                t2 = (-b - math.sqrt(D)) / (2.0 * a)
                if t1 >= t2:
                    resPnt = self.getPntByDist(math.fabs(t1))
                    vecDist = Geom.Vec(self.p0, resPnt)
                    return vecDist.magnitude()
                elif t1 < t2:
                    resPnt = self.getPntByDist(math.fabs(t2))
                    vecDist = Geom.Vec(self.p0, resPnt)
                    return vecDist.magnitude()
            elif D == 0:
                t = - b / (2.0 * a)
                resPnt = self.getPntByDist(t)
                vecDist = Geom.Vec(self.p0, resPnt)
                return vecDist.magnitude()
            elif D < 0:
                # print("D", D)
                # print("WRONG DISCRIMINANT")
                return None

        def getListPointWithDistance(self, distance, ifLast, rad, startDistance):
            pointList = []

            vecForAngle = Geom.Vec(Geom.Pnt(self.p0.x(), self.p0.y(), self.p0.z()),
                                   Geom.Pnt(self.p1.x(), self.p1.y(), self.p0.z()))
            angle = self.vecSegm.angle(vecForAngle)
            len = self.len
            dist = distance
            radius = rad
            startDist = startDistance
            if angle == 0.5 * math.pi:
                return pointList
            elif angle < 0.00001:
                dist = distance / math.cos(angle)
            if ifLast:
                segmN = int(((len - startDist) / dist) + 1.0)
            elif startDist is not None:
                segmN = int(((len - startDist) / dist) + 1.0)
            else:
                segmN = int(((len - radius) / dist) + 1.0)

            for i in range(segmN):
                resPnt = self.getPntByDist(startDist + (dist * float(i)))
                pointList.append(resPnt)
            return pointList


class Segment:
    def __init__(self, _b, _h, _t, _s, _d, _angle, _height):
        self.b = _b
        self.h = _h
        self.t = _t
        self.s = _s * 0.5
        self.d = _d
        self.angle = _angle

        self.height = _height

    def getGeom(self):
        # firstconnection
        pntF00 = Geom.Pnt(0.045 + 0.012, 0.015, 0.0)
        pntF01 = Geom.Pnt(0.045 + 0.012, -0.02, 0.0)
        pntF02 = Geom.Pnt(0.039 + 0.012, -0.034, 0.0)
        pntF03 = Geom.Pnt(0.025 + 0.012, -0.04, 0.0)
        pntF04 = Geom.Pnt(-0.01, -0.04, 0.0)
        pntF05 = Geom.Pnt(-0.024, -0.034, 0.0)
        pntF06 = Geom.Pnt(-0.03, -0.02, 0.0)
        pntF07 = Geom.Pnt(-0.03, -0.01, 0.0)
        pntF08 = Geom.Pnt(-0.0255, 0.005, 0.0)
        pntF09 = Geom.Pnt(0.0, 0.02, 0.0)
        pntF10 = Geom.Pnt(0.005, 0.02, 0.0)
        pntF11 = Geom.Pnt(0.005 + 0.0025, 0.02 - 0.0035, 0.0)
        pntF12 = Geom.Pnt(0.005, 0.01, 0.0)
        pntF13 = Geom.Pnt(-0.015, -0.01, 0.0)
        pntF14 = Geom.Pnt(-0.015, -0.02, 0.0)
        pntF15 = Geom.Pnt(-0.0135, -0.0235, 0.0)
        pntF16 = Geom.Pnt(-0.01, -0.025, 0.0)
        pntF17 = Geom.Pnt(0.03 + 0.008, -0.025, 0.0)
        pntF18 = Geom.Pnt(0.0335 + 0.008, -0.0235, 0.0)
        pntF19 = Geom.Pnt(0.035 + 0.008, -0.02, 0.0)
        pntF20 = Geom.Pnt(0.035 + 0.008, 0.02, 0.0)

        # second connection
        pntS00 = Geom.Pnt(self.b - 0.045 - 0.012, 0.015, 0.0)
        pntS01 = Geom.Pnt(self.b - 0.045 - 0.012, -0.02, 0.0)
        pntS02 = Geom.Pnt(self.b - 0.039 - 0.012, -0.034, 0.0)
        pntS03 = Geom.Pnt(self.b - 0.025 - 0.012, -0.04, 0.0)
        pntS04 = Geom.Pnt(self.b - -0.01, -0.04, 0.0)
        pntS05 = Geom.Pnt(self.b - -0.024, -0.034, 0.0)
        pntS06 = Geom.Pnt(self.b - -0.03, -0.02, 0.0)
        pntS07 = Geom.Pnt(self.b - -0.03, -0.01, 0.0)
        pntS08 = Geom.Pnt(self.b - -0.0255, 0.005, 0.0)
        pntS09 = Geom.Pnt(self.b - 0.0, 0.02, 0.0)
        pntS10 = Geom.Pnt(self.b - 0.005, 0.02, 0.0)
        pntS11 = Geom.Pnt(self.b - 0.005 - 0.0025, 0.02 - 0.0035, 0.0)
        pntS12 = Geom.Pnt(self.b - 0.005, 0.01, 0.0)
        pntS13 = Geom.Pnt(self.b - -0.015, -0.01, 0.0)
        pntS14 = Geom.Pnt(self.b - -0.015, -0.02, 0.0)
        pntS15 = Geom.Pnt(self.b - -0.0135, -0.0235, 0.0)
        pntS16 = Geom.Pnt(self.b - -0.01, -0.025, 0.0)
        pntS17 = Geom.Pnt(self.b - 0.03 - 0.008, -0.025, 0.0)
        pntS18 = Geom.Pnt(self.b - 0.0335 - 0.008, -0.0235, 0.0)
        pntS19 = Geom.Pnt(self.b - 0.035 - 0.008, -0.02, 0.0)
        pntS20 = Geom.Pnt(self.b - 0.035 - 0.008, 0.02, 0.0)

        xSDir = self.s / math.sin(self.angle / (180.0 / math.pi))
        ySDir = self.s / math.sin((90.0 - self.angle) / (180.0 / math.pi))

        pnt1ForLine1 = Geom.Pnt((self.b * 0.5) - (self.d * 0.5), (self.h * 0.5) - self.t, 0.0)
        pnt2ForLine1 = Geom.Pnt((self.b * 0.5) - (self.d * 0.5) + xSDir, (self.h * 0.5) - self.t + ySDir, 0.0)

        pnt1ForLine4 = Geom.Pnt((self.b * 0.5) + (self.d * 0.5), (self.h * 0.5) - self.t, 0.0)
        pnt2ForLine4 = Geom.Pnt((self.b * 0.5) + (self.d * 0.5) - xSDir, (self.h * 0.5) - self.t + ySDir, 0.0)

        line0 = Line2D.from2Points(Geom.Pnt(pnt1ForLine1.x() - xSDir, pnt1ForLine1.y() + ySDir, 0.0),
                                   Geom.Pnt(pnt2ForLine1.x() - xSDir, pnt2ForLine1.y() + ySDir, 0.0))
        line1 = Line2D.from2Points(pnt1ForLine1, pnt2ForLine1)

        line2 = Line2D.from2Points(pntF19, pntF20)
        line3 = Line2D.from2Points(pntF01, pntF00)

        line4 = Line2D.from2Points(pnt1ForLine4, pnt2ForLine4)
        line5 = Line2D.from2Points(Geom.Pnt(pnt1ForLine4.x() + xSDir, pnt1ForLine4.y() + ySDir, 0.0),
                                   Geom.Pnt(pnt2ForLine4.x() + xSDir, pnt2ForLine4.y() + ySDir, 0.0))

        line6 = Line2D.from2Points(pntS01, pntS00)
        line7 = Line2D.from2Points(pntS19, pntS20)

        line8 = Line2D.from2Points(Geom.Pnt(0.0, self.h * 0.5, 0.0), Geom.Pnt(1.0, self.h * 0.5, 0.0))
        line9 = Line2D.from2Points(Geom.Pnt(0.0, (self.h * 0.5) - self.t, 0.0),
                                   Geom.Pnt(1.0, (self.h * 0.5) - self.t, 0.0))

        pnt0 = Line2D.intersect(line0, line8)
        pnt1 = Line2D.intersect(line5, line8)

        pnt2 = Line2D.intersect(line1, line9)
        pnt3 = Line2D.intersect(line9, line4)

        pntF00 = Line2D.intersect(line1, line3)
        pntS00 = Line2D.intersect(line4, line6)

        pntF20 = Line2D.intersect(line0, line2)
        pntS20 = Line2D.intersect(line5, line7)

        edgeList = Topo.vector_Edge(34)

        edgeList[0] = Topo.EdgeTool.makeEdge(pntF00, pntF01)
        edgeList[1] = Topo.EdgeTool.makeArcOfCircle(pntF01, pntF02, pntF03)
        edgeList[2] = Topo.EdgeTool.makeEdge(pntF03, pntF04)
        edgeList[3] = Topo.EdgeTool.makeArcOfCircle(pntF04, pntF05, pntF06)
        edgeList[4] = Topo.EdgeTool.makeEdge(pntF06, pntF07)
        edgeList[5] = Topo.EdgeTool.makeArcOfCircle(pntF07, pntF08, pntF09)
        edgeList[6] = Topo.EdgeTool.makeEdge(pntF09, pntF10)
        edgeList[7] = Topo.EdgeTool.makeArcOfCircle(pntF10, pntF11, pntF12)
        edgeList[8] = Topo.EdgeTool.makeEdge(pntF12, pntF13)
        edgeList[9] = Topo.EdgeTool.makeEdge(pntF13, pntF14)
        edgeList[10] = Topo.EdgeTool.makeArcOfCircle(pntF14, pntF15, pntF16)
        edgeList[11] = Topo.EdgeTool.makeEdge(pntF16, pntF17)
        edgeList[12] = Topo.EdgeTool.makeArcOfCircle(pntF17, pntF18, pntF19)
        edgeList[13] = Topo.EdgeTool.makeEdge(pntF19, pntF20)

        edgeList[14] = Topo.EdgeTool.makeEdge(pntF20, pnt0)
        edgeList[15] = Topo.EdgeTool.makeEdge(pnt0, pnt1)
        edgeList[16] = Topo.EdgeTool.makeEdge(pnt1, pntS20)

        edgeList[17] = Topo.EdgeTool.makeEdge(pntS20, pntS19)
        edgeList[18] = Topo.EdgeTool.makeArcOfCircle(pntS19, pntS18, pntS17)
        edgeList[19] = Topo.EdgeTool.makeEdge(pntS17, pntS16)
        edgeList[20] = Topo.EdgeTool.makeArcOfCircle(pntS16, pntS15, pntS14)
        edgeList[21] = Topo.EdgeTool.makeEdge(pntS14, pntS13)
        edgeList[22] = Topo.EdgeTool.makeEdge(pntS13, pntS12)
        edgeList[23] = Topo.EdgeTool.makeArcOfCircle(pntS12, pntS11, pntS10)
        edgeList[24] = Topo.EdgeTool.makeEdge(pntS10, pntS09)
        edgeList[25] = Topo.EdgeTool.makeArcOfCircle(pntS09, pntS08, pntS07)
        edgeList[26] = Topo.EdgeTool.makeEdge(pntS07, pntS06)
        edgeList[27] = Topo.EdgeTool.makeArcOfCircle(pntS06, pntS05, pntS04)
        edgeList[28] = Topo.EdgeTool.makeEdge(pntS04, pntS03)
        edgeList[29] = Topo.EdgeTool.makeArcOfCircle(pntS03, pntS02, pntS01)
        edgeList[30] = Topo.EdgeTool.makeEdge(pntS01, pntS00)
        edgeList[31] = Topo.EdgeTool.makeEdge(pntS00, pnt3)
        edgeList[32] = Topo.EdgeTool.makeEdge(pnt3, pnt2)
        edgeList[33] = Topo.EdgeTool.makeEdge(pnt2, pntF00)

        wire = Topo.WireTool.makeWire(edgeList, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())

        faceBottomBeam = Topo.FaceTool.extrudedFace(face, Geom.Dir(0.0, 0.0, 1.0), self.height)
        geomBottomBeam = lx.AdvancedBrep.createIn(doc)
        geomBottomBeam.setShape(faceBottomBeam)
        return geomBottomBeam


class Spundwand(lx.Wall):
    _profileParamName = "Profile"
    _heightParamName = "Height"

    _firstElemParamName = "Change first profile"
    _directionParamName = "Change direction"

    _bParamName = "b"
    _hParamName = "h"
    _tParamName = "t"
    _sParamName = "s"
    _angleParamName = "angle"
    _numberOfElementsParamName = "Number of elements"
    _totalLengthParamName = "Total length"

    _polylineParamName = "Polyline"

    def getGlobalClassId(self):
        return Base.GlobalId("{BCDF157E-9E9A-452A-9770-A7494847795A}")

    def __init__(self, aArg):
        lx.Wall.__init__(self, aArg)
        self.registerPythonClass("Spundwand", "OpenLxApp.Wall")
        # Register properties
        self.setPropertyHeader(lxstr("Spundwand U-Profile"), 253)
        self.setPropertyGroupName(lxstr("Spundwand U-Profile properties"), 254)

        self._profileType = self.registerPropertyEnum(self._profileParamName, 0, lx.Property.VISIBLE,
                                                      lx.Property.EDITABLE, 255)
        self._profileType.setEmpty()

        for i in range(len(listOfProfiles)):
            self._profileType.addEntry(lxstr(listOfProfiles[i][0]), -1)

        self._height = self.registerPropertyDouble(self._heightParamName, 10.0, lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE, 256)

        self._numberOfElements = self.registerPropertyInteger(self._numberOfElementsParamName, 1, lx.Property.VISIBLE,
                                                              lx.Property.NOT_EDITABLE, 257)

        self._totalLength = self.registerPropertyDouble(self._totalLengthParamName, 0.0, lx.Property.VISIBLE,
                                                        lx.Property.NOT_EDITABLE, 258)

        self._modules = self.registerPropertyDouble("Modules", 0.0, lx.Property.NOT_VISIBLE,
                                                    lx.Property.NOT_EDITABLE, -1)

        self._polyline = self.registerPropertyString(self._polylineParamName, lxstr(""), lx.Property.NOT_VISIBLE,
                                                     lx.Property.NOT_EDITABLE, -1)  # NOT_VISIBLE
        self._setAllSteps()
        self._baseData = None
        dataStr = cstr(self._polyline.getValue())
        if dataStr:
            self._baseData = self.readFromString(dataStr)

        self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())

    def _setAllSteps(self):
        self._height.setSteps(0.1)

    @staticmethod
    def _createSubElementFace(listPoint):
        edgeList = Topo.vector_Edge(4)

        edgeList[0] = Topo.EdgeTool.makeEdge(listPoint[0], listPoint[1])
        edgeList[1] = Topo.EdgeTool.makeEdge(listPoint[1], listPoint[2])
        edgeList[2] = Topo.EdgeTool.makeEdge(listPoint[2], listPoint[3])
        edgeList[3] = Topo.EdgeTool.makeEdge(listPoint[3], listPoint[0])

        wire = Topo.WireTool.makeWire(edgeList, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        # print(face)
        # print(wire)
        geom = lx.createCurveBoundedPlaneFromFace(doc, face)

        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(geom)
        return elem

    def _placeSegment(self, model, polyLine, segmId, distance, face, previousPoint):
        segmType = polyLine.segmentType(segmId)

        if segmType == PolylineData.SegmType_Line:
            previousPoint = self._buildWithLineSegment(model, polyLine, segmId, distance, face, previousPoint)

        elif segmType == PolylineData.SegmType_Arc:
            previousPoint = self._buildWithArcSegment(model, polyLine, segmId, distance, face, previousPoint)
        else:
            return None
        return previousPoint

    def _placeSegmentsAccLine(self, polyLine):
        height = self._height.getValue()
        indexOfType = self._profileType.getValue()
        b = listOfProfiles[indexOfType][1]
        h = listOfProfiles[indexOfType][2]
        t = listOfProfiles[indexOfType][3]
        s = listOfProfiles[indexOfType][4]
        angle = listOfProfiles[indexOfType][5]

        d = listOfProfiles[indexOfType][6]
        print("Parameters")
        print(listOfProfiles[indexOfType][0])
        print('b = ', b)
        print('h = ', h)
        print('t = ', t)
        print('s = ', s)
        print('angle = ', angle)

        polylyneElement = PolylineReader(polyLine)
        listPointsForColumn = polylyneElement.getListPointWithDistanceOnPolyline(b, 0.0, False)
        zDir1 = Geom.Dir(0, 0, 1)
        zDir2 = Geom.Dir(0, 0, -1)

        mainConstructor = Segment(b, h, t, s, d, angle, height)
        typeGeom = mainConstructor.getGeom()
        self._numberOfElements.setValue(len(listPointsForColumn) - 1)
        self._totalLength.setValue(float(len(listPointsForColumn) - 1) * b)
        for i in range(len(listPointsForColumn) - 1):
            if float(i) % 2 == 0:
                firstElem = lx.SubElement.createIn(doc)
                firstElem.setGeometry(typeGeom)
                dirVec = Geom.Vec(listPointsForColumn[i], listPointsForColumn[i + 1])
                axis = Geom.Ax2(listPointsForColumn[i], zDir1, Geom.Dir(dirVec))
                firstElem.setLocalPlacement(axis)
                self.addSubElement(firstElem)
            else:
                secondElem = lx.SubElement.createIn(doc)
                secondElem.setGeometry(typeGeom)
                dirVec = Geom.Vec(listPointsForColumn[i], listPointsForColumn[i + 1])
                axis = Geom.Ax2(listPointsForColumn[i], zDir2, Geom.Dir(dirVec))
                axis.translate(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(0.0, 0.0, height)))
                secondElem.setLocalPlacement(axis)
                self.addSubElement(secondElem)

    def printPolyline(self, name, ptList):
        print("{}:".format(name))

        for pt in ptList:
            print("    ({}, {}, {})".format(pt.x(), pt.y(), pt.z()))

    def fixPolyline(self, pntList):
        self._pntList = pntList
        self.printPolyline("pntList", pntList)
        self.printPolyline("self._pntList", self._pntList)

    def createCompound(self):
        polyLine = PolylineData.fromElement(self._baseData)
        self._placeSegmentsAccLine(polyLine)

    @staticmethod
    def maxInList(lst):
        assert lst
        m = lst[0]
        for i in lst:
            if i > m:
                m = i
        return m

    def _updateGeometry(self):
        with EditMode(self.getDocument()):
            self.removeSubElements()
            self.createCompound()

    def setProfileType(self, param):
        with EditMode(self.getDocument()):
            self._profileType.setValue(param)
            self._updateGeometry()

    def set_height(self, param):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(param, 0.01, 10000.0))
            self._updateGeometry()

    def reselectPolyline(self):
        pass

        doc.recompute()

    def printPolylineTest(self, strn):
        print(":{}".format(strn))

        # for pt in ptList:
        #     print "    ({}, {}, {})".format(pt.x(), pt.y(), pt.z())

    def setPolylineData(self, polylineData):
        if lxstr(self.writeToString(polylineData)) is self._modules.getValue():
            print("Select another polyline")
            return

        # if not self._insidePropUpdate:
        self._insidePropUpdate = True

        self._baseData = polylineData
        self._polyline.setValue(lxstr(self.writeToString(polylineData)))
        # self.printPolylineTest(cstr(self._polyline.getValue()))

        self._updateGeometry()

        # self._insidePropUpdate = False

        # with EditMode(self.getDocument()):
        #     self._polyline.setValue(polyline)
        #     self._updateGeometry()

    @staticmethod
    def writeToString(lineData):
        strn = ""
        strn += "{};".format(len(lineData))
        for i in range(len(lineData)):
            if lineData[i][0] == PolylineData.SegmType_Line:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};".format(lineData[i][0], \
                                                                                      lineData[i][1].x(),
                                                                                      lineData[i][1].y(),
                                                                                      lineData[i][1].z(), \
                                                                                      lineData[i][2].x(),
                                                                                      lineData[i][2].y(),
                                                                                      lineData[i][2].z())
            elif lineData[i][0] == PolylineData.SegmType_Arc:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};{7:.5f};{8:.5f};{9:.5f};".format(
                    lineData[i][0], \
                    lineData[i][1].x(), lineData[i][1].y(), lineData[i][1].z(), \
                    lineData[i][2].x(), lineData[i][2].y(), lineData[i][2].z(), \
                    lineData[i][3].x(), lineData[i][3].y(), lineData[i][3].z())
            # if i != len(lineData)-1:
            #     strn += ";"
        i_n = len(lineData[len(lineData) - 1]) - 1
        strn += "{}".format(lineData[len(lineData) - 1][i_n])
        return strn

    @staticmethod
    def readFromString(strn):
        lineData = []
        st = strn.split(";")
        # lenList = int(st[0])
        index = 0
        for i in range(int(st[0])):
            if int(st[index + 1]) == PolylineData.SegmType_Line:
                lineData.append(
                    [int(st[index + 1]), Geom.Pnt(float(st[index + 2]), float(st[index + 3]), float(st[index + 4])), \
                     Geom.Pnt(float(st[index + 5]), float(st[index + 6]), float(st[index + 7]))])
                index += 7
            elif int(st[index + 1]) == PolylineData.SegmType_Arc:
                lineData.append(
                    [int(st[index + 1]), Geom.Pnt(float(st[index + 2]), float(st[index + 3]), float(st[index + 4])), \
                     Geom.Pnt(float(st[index + 5]), float(st[index + 6]), float(st[index + 7])), \
                     Geom.Pnt(float(st[index + 8]), float(st[index + 9]), float(st[index + 10]))])
                index += 10

        i_n = len(lineData[int(st[0]) - 1])
        if st[len(st) - 1] == "True":
            bl = True
        else:
            bl = False
        lineData[int(st[0]) - 1].append(bl)
        # print "i_n={} , st[last]={}".format(i_n, lineData[int(st[0])-1][i_n])

        return lineData

    def polyline(self):
        return self._polyline.getValue()

    def onPropertyChanged(self, aPropertyName):

        if aPropertyName == Spundwand._profileParamName:
            self.setProfileType(self._profileType.getValue())
        elif aPropertyName == Spundwand._heightParamName:
            self.set_height(self._height.getValue())


def getPolylineData(lineSet):
    lineData = []
    # edges = Topo.ShapeTool.getEdges(lineSet.getShape())
    wire = Topo.ShapeTool.isSingleWire(lineSet.getShape())
    # print("Is Wire Closed?", Topo.WireTool.isClosed(wire))
    # print("Is Wire SelfIntersecting?", Topo.WireTool.isSelfIntersecting(wire))
    # print("Fix Reorder in Wire !", Topo.WireTool.fixReorder(wire))
    if Topo.WireTool.isClosed(wire):
        edges = Topo.WireTool.getEdges(Topo.WireTool.reversed(wire))
    else:
        edges = Topo.WireTool.getEdges(wire)
    # edges = Topo.WireTool.getEdges(wire)

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
            p2Res = Topo.EdgeTool.d0(edge, lineParamRes.endParam)
            if (not p1Res.ok) or (not p2Res.ok):
                raise RuntimeError("Can't get line start or end point")
            lineData.append([PolylineData.SegmType_Line, Geom.Pnt(p1Res.p), Geom.Pnt(p2Res.p)])

            # print "LineNumb[{}] has type {}: startPt ({}, {}, {}), " \
            #       "\n endPt ({}, {}, {})".format(edgeIndex, lineData[edgeIndex][0],
            #                                      lineData[edgeIndex][1].x(), lineData[edgeIndex][1].y(), lineData[edgeIndex][1].z(),
            #                                      lineData[edgeIndex][2].x(), lineData[edgeIndex][2].y(), lineData[edgeIndex][2].z())

        elif edgeTypeRes.type == Geom.CurveType_CIRCLE:
            arcParamsRes = Topo.EdgeTool.getArcParameters(edge)
            if not arcParamsRes.ok:
                raise RuntimeError("Can't get arc parameters")
            p1Res = Topo.EdgeTool.d0(edge, arcParamsRes.startParam)
            middleParam = (arcParamsRes.startParam + arcParamsRes.endParam) * 0.5
            p2Res = Topo.EdgeTool.d0(edge, middleParam)
            p3Res = Topo.EdgeTool.d0(edge, arcParamsRes.endParam)
            if (not p1Res.ok) or (not p2Res.ok) or (not p3Res.ok):
                raise RuntimeError("Can't get arc start or middle or end point")
            lineData.append([PolylineData.SegmType_Arc, Geom.Pnt(p1Res.p), Geom.Pnt(p2Res.p), Geom.Pnt(p3Res.p)])

            # print "LineNumb[{}] has type {}: startPt ({}, {}, {}), " \
            #       "\n endPt ({}, {}, {})".format(edgeIndex, lineData[edgeIndex][0],
            #                                      lineData[edgeIndex][1].x(), lineData[edgeIndex][1].y(), lineData[edgeIndex][1].z(),
            #                                      lineData[edgeIndex][2].x(), lineData[edgeIndex][2].y(), lineData[edgeIndex][2].z(),
            #                                      lineData[edgeIndex][3].x(), lineData[edgeIndex][3].y(), lineData[edgeIndex][3].z())
        else:
            raise RuntimeError("Unsupported edge type")
    lineData[len(edges) - 1].append(Topo.WireTool.isClosed(wire))
    # print(lineData[len(edges)-1])
    return lineData


def selectPolyline(uidoc):
    uidoc.highlightByShapeType(Topo.ShapeType_WIRE)
    ok = uidoc.pickPoint()
    uidoc.stopHighlightByShapeType()
    if ok:
        return uidoc.getPickedElement()
    else:
        return None


def pickPolyline(uidoc):
    ui.showStatusBarMessage(lxstr("[L] Select base line [Esc] Cancel"))
    lineSet = selectPolyline(uidoc)
    ui.showStatusBarMessage(lxstr(""))

    if lineSet is not None:
        return getPolylineData(lineSet)
    else:
        return None


if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{A5F5C073-DAD3-485B-AE51-81C8FF1DAC14}"))

    # Begin creating the Element
    with EditMode(doc):
        polylineData = pickPolyline(uidoc)
        if polylineData is not None:
            comp = Spundwand(doc)
            lx.setNewComponentByColorAndName(CW_COLOR, Base.StringTool.toString("Spundwand_u"), comp)
            comp.setPolylineData(polylineData)  # !!!!!!!!!!!!!

    doc.recompute()
