# version 2.0   26.01.2021

# attributes
#   version 2.0
#   - height
#   - length
#   - width
#   - height
#   - handrail width
#   - handrail height
#   - handrail type
#   - column distance
#   - bottom distance
#   - intermediate thickness
#   - intermediate type
#   - intermediate direction 
#   - length

# ======================================
# ====  Supported by Taras Dalyak   ====
# ====  Mail: tdalyak@gmail.com     ====
# ====  Skype: live:tdalyak         ====
# ======================================

# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd
import Base, Core, Draw, Geom, Topo

import time, traceback
import math


lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

st = Topo.ShapeTool

# doc = lx.Application.getInstance().getActiveDocument()
# uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
# sel = uidoc.getSelection()
# from uuid import uuid4
GUID_CLASS = Base.GlobalId("{ddf83ba6-ef11-41fe-8f19-15c9d3972104}")
GUID_SCRPT = Base.GlobalId("{d9639c40-4cf7-42cd-8bd0-fe2beb679434}")
CW_COLOR = 3061

epsilon = 0.0001
eps_DS = 0.001
pi2 = math.pi * 0.5

# PROFILES = {
#     "G":   {# 301
#             'height'  :     1.1,  
#             'handrail':     {"size": (0.12, 0.06), 'ledge': 0.15},
#             'support':      {"size": (0.08, 0.05, 1.1-0.07-0.06),},
#             'spar':         None,
#             'bottom chord': {"size": (0.05, 0.025),
#                              "bottom distance": 0.095},
#             'pole':         {"size": (0.04, 0.02)},
#             'footplate':    {"size": (0.22, 0.04)},
#             'foundation':   {"size": (0.3, 0.07), 'ledge': 0.25},
#             },
#     "GS":  {# 302
#             'height'  :     1.1,  
#             'handrail':     {"size": (0.12, 0.06), 'ledge': 0.15},
#             'support':      {"size": (0.08, 0.05, 1.1-0.07-0.06),},
#             'spar':         {"size": (0.05, 0.03),
#                              "handrail distance": 0.27},
#             'bottom chord': {"size": (0.05, 0.025),
#                              "bottom distance": 0.095},
#             'pole':         {"size": (0.04, 0.02)},
#             'footplate':    {"size": (0.22, 0.04)},
#             'foundation':   {"size": (0.3, 0.07), 'ledge': 0.25},
#             },
#     "GSR": {# 303
#             'height'  :     1.3,  
#             'handrail':     {"size": (0.12, 0.06), 'ledge': 0.15},
#             'support':      {"size": (0.08, 0.05, 1.3-0.07-0.06)},
#             'spar':         {"size": (0.05, 0.03),
#                              "handrail distance": 0.27},
#             'bottom chord': {"size": (0.05, 0.025),
#                              "bottom distance": 0.095},
#             'pole':         {"size": (0.04, 0.02)},
#             'footplate':    {"size": (0.22, 0.04)},
#             'foundation':   {"size": (0.3, 0.07), 'ledge': 0.25},
#             },
#     "Ga":  {# 304
#             'height'  :     1.1,  
#             'handrail':     {"size": (0.08, 0.05), 'ledge': 0.15},
#             'support':      {"size": (0.06, 0.04, 1.1-0.07-0.05)},
#             'spar':         None,
#             'bottom chord': {"size": (0.04, 0.025),
#                              "bottom distance": 0.09},
#             'pole':         {"size": (0.03, 0.02)},
#             'footplate':    {"size": (0.16, 0.035)},
#             'foundation':   {"size": (0.25, 0.07), 'ledge': 0.25},
#             },
#     "GSa": {# 305
#             'height'  :     1.1,  
#             'handrail':     {"size": (0.08, 0.05), 'ledge': 0.15},
#             'support':      {"size": (0.05, 0.03)},
#             'spar':         {"size": (0.05, 0.03),
#                              "handrail distance": 0.27},
#             'bottom chord': {"size": (0.04, 0.025),
#                              "bottom distance": 0.09},
#             'pole':         {"size": (0.03, 0.02)},
#             'footplate':    {"size": (0.16, 0.035)},
#             'foundation':   {"size": (0.25, 0.07), 'ledge': 0.25},
#             },
#     "GSRa": {# 306
#             'height'  :     1.1,  
#             'handrail':     {"size": (0.08, 0.05), 'ledge': 0.15},
#             'support':      {"size": (0.05, 0.03)},
#             'spar':         {"size": (0.05, 0.03),
#                              "handrail distance": 0.27},
#             'bottom chord': {"size": (0.04, 0.025),
#                              "bottom distance": 0.09},
#             'pole':         {"size": (0.03, 0.02)},
#             'footplate':    {"size": (0.16, 0.035)},
#             'foundation':   {"size": (0.25, 0.07), 'ledge': 0.25},
#             },
# }


def qstr(str):
    return Base.StringTool.toQString(lxstr(str))


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


def baseVecTranslate(pt, baseVec, dist):
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


# decorator
def timer(f):
    def tmp(*args, **kwargs):
        
        t1_start = time.perf_counter()
        t2_start = time.process_time()

        res = f(*args, **kwargs)
        
        t1_stop = time.perf_counter()
        t2_stop = time.process_time()

        print("------------------------------------------------------------------------------")
        print("Elapsed time: %.5f [sec]" % (t1_stop-t1_start))
        print("CPU process time: %.5f [sec]" % (t2_stop-t2_start))
        print("------------------------------------------------------------------------------\n")

        return res

    return tmp


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
        def __init__(self, type_, data):
            self.type = type_
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
            ui.UIApplication.getInstance().getUIDocument(self._doc).getSelection().forceUpdate()
            self._doc.recompute()


class DataStruct:
    def __init__(self, bmType, strPt, endPt, weight, height, strNorm, endNorm, trsfrm):
        self.bmType = bmType
        self.strPt = strPt
        self.endPt = endPt
        self.weight = weight
        self.height = height
        self.strNorm = strNorm
        self.endNorm = endNorm
        self.trsfrm = trsfrm

        self.length = Geom.Vec(self.strPt, self.endPt).magnitude()
        self.strNorm_LCS = strNorm.transformed(trsfrm.inverted())
        self.endNorm_LCS = endNorm.transformed(trsfrm.inverted())

    # def _invertToLCS(self):
    #     strPt = self.strPt
    #     endPt = self.endPt
    # equality v == u
    def __eq__(self, other):

        if self.bmType != other.bmType:
            return False

        if abs(self.length - other.length) > eps_DS:
            return False

        if abs(self.weight - other.weight) > eps_DS:
            return False

        if abs(self.height - other.height) > eps_DS:
            return False

        enV_b = abs(self.endNorm_LCS.x() - other.endNorm_LCS.x()) > eps_DS or \
                abs(self.endNorm_LCS.y() - other.endNorm_LCS.y()) > eps_DS or \
                abs(self.endNorm_LCS.z() - other.endNorm_LCS.z()) > eps_DS
        if enV_b:
            return False

        stV_b = abs(self.strNorm_LCS.x() - other.strNorm_LCS.x()) > eps_DS or \
                abs(self.strNorm_LCS.y() - other.strNorm_LCS.y()) > eps_DS or \
                abs(self.strNorm_LCS.z() - other.strNorm_LCS.z()) > eps_DS
        if stV_b:
            return False

        return True


class BeamPool:
    def __init__(self, doc):  # , factory
        self._doc = doc
        self._dict_list = []
        # self._factory = factory

    def createBeam(self, new_dataStr):
        # print("Start of creating", len(self._dict_list))
        bmfc = BeamFactory(self._doc)
        beam = lx.SubElement.createIn(self._doc)
        geom = self._isInPool(new_dataStr)
        if geom is not None:
            # print("Existing geom")
            beam.setGeometry(geom)
            beam.setTransform(new_dataStr.trsfrm)
        else:
            # print("Creating geom")
            beam = bmfc.getCutBeam(new_dataStr)
            geom = beam.getGeometry()
            self._addToPool(new_dataStr, geom)
        # print("Finish of creating", len(self._dict_list))
        return beam

    def _isInPool(self, new_dataStr):
        """
        TODO:
        """
        for el in self._dict_list:
            if new_dataStr == el['data']:
                # print("equal")
                return el['geom']
        else:
            # print("not equal")
            return None

    def _addToPool(self, new_dataStr, geom):
        self._dict_list.append({'data': new_dataStr, 'geom': geom})


class BeamFactory:
    # Beam types
    BT_Square = 0
    BT_Circle = 1
    BT_Diamond = 2
    BT_IPE = 3
    # Beam type names
    _squareBTypeName = "square"
    _circleBTypeName = "circle"
    _diamondBTypeName = "diamond"
    _IPE_BTypeName = "IPE"

    @staticmethod
    def correctBeamType(beamType):
        return bool(beamType == BeamFactory.BT_Square or 
                    beamType == BeamFactory.BT_Circle or 
                    beamType == BeamFactory.BT_Diamond or 
                    beamType == BeamFactory.BT_IPE)

    @staticmethod
    def writeBeamType(bt):
        if bt == BeamFactory.BT_Square:
            return BeamFactory._squareBTypeName
        elif bt == BeamFactory.BT_Circle:
            return BeamFactory._circleBTypeName
        elif bt == BeamFactory.BT_Diamond:
            return BeamFactory._diamondBTypeName
        elif bt == BeamFactory.BT_IPE:
            return BeamFactory._IPE_BTypeName
        else:
            raise RuntimeError("Invalid beam type")

    @staticmethod
    def parseBeamType(bt):
        if bt == BeamFactory._squareBTypeName:
            return BeamFactory.BT_Square
        elif bt == BeamFactory._circleBTypeName:
            return BeamFactory.BT_Circle
        elif bt == BeamFactory._IPE_BTypeName:
            return BeamFactory.BT_IPE
        elif bt == BeamFactory._diamondBTypeName:
            return BeamFactory.BT_Diamond
        else:
            raise RuntimeError("Invalid beam type string")

    def __init__(self, doc):
        self._doc = doc
        # self._modelGr = None

    def _createBaseBeam_Square(self, length, radiusH, radiusV):
        diameterH = radiusH * 2.0
        diameterV = radiusV * 2.0
        position = Geom.Ax2(Geom.Pnt(-length[0], -radiusH, -radiusV), Geom.Dir(0, 0, 1))

        beamGeom = lx.Block.createIn(self._doc)
        beamGeom.setLength(sum(length))
        beamGeom.setWidth(diameterH)
        beamGeom.setHeight(diameterV)
        beamGeom.setPosition(position)

        # beamGeom.setYLength(diameterH)
        # beamGeom.setZLength(diameterV)
        # beamGeom.setXLength(length)

        beam_Sq = lx.SubElement.createIn(self._doc)
        beam_Sq.setGeometry(beamGeom)

        # beam.translate(Geom.Vec(0.0, -radiusH, -radiusV), Geom.CoordSpace_WCS)

        return beam_Sq

    def _createBaseBeam_Circle(self, length, radius):
        beamGeom = lx.RightCircularCylinder.createIn(self._doc)
        position = Geom.Ax2(Geom.Pnt(-length[0], 0, 0), Geom.Dir(1, 0, 0))
        beamGeom.setHeight(sum(length))
        beamGeom.setRadius(radius)
        beamGeom.setPosition(position)

        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(beamGeom)

        return beam
    
    def _createBaseBeam_IPE(self, height, extrudedDir=None, axis=None, depth=0.1, width=0.055, web_thickness=0.0041, 
                    flange_thickness=0.0057, fillet_radius=0.007):
        profile = lx.IShapeProfileDef.createIn(self._doc)
        profile.setOverallWidth(width)
        profile.setOverallDepth(depth)
        profile.setWebThickness(web_thickness)
        profile.setFlangeThickness(flange_thickness)
        profile.setFilletRadius(fillet_radius)
        eas = lx.ExtrudedAreaSolid.createIn(self._doc)
        eas.setSweptArea(profile)
        if not axis: 
            axis = Geom.Ax2(Geom.Pnt(-height[0], 0, 0), Geom.Dir(1, 0, 0))  # , Geom.Dir(1, 0, 0)
        eas.setPosition(axis)
        if not extrudedDir: 
            extrudedDir = Geom.Dir(0, 0, 1)
        eas.setExtrudedDirection(extrudedDir)  # Geom.Dir(0, 0, 1)
        # print('_createBaseBeam_IPE: height', height)
        eas.setDepth(sum(height))
        column_element = lx.SubElement.createIn(self._doc)
        column_element.setGeometry(eas)
        # column_element.setLocalPlacement(axis)
        
        return column_element
        # self.addSubElement(column_element)

    def _createBaseBeam_Diamond(self, length, radiusH, radiusV):
        diameterH = radiusH * 2.0
        # diameterV = radiusV * 2.0
        # position = Geom.Ax2(Geom.Pnt(-length[0], -radiusH, -radiusV), Geom.Dir(0, 0, 1))  # , Geom.Dir(1, 0, 0)
        position = Geom.Ax2(Geom.Pnt(-length[0], 0, -radiusH*math.sqrt(2)), 
                            Geom.Dir(0, -1./math.sqrt(2.), 1./math.sqrt(2.)), 
                            Geom.Dir(0, 1./math.sqrt(2.), 1./math.sqrt(2.)), 
                            Geom.Dir(1, 0, 0))

        beamGeom = lx.Block.createIn(self._doc)
        beamGeom.setLength(sum(length))
        beamGeom.setWidth(diameterH)
        beamGeom.setHeight(diameterH)
        beamGeom.setPosition(position)

        beam_ = lx.SubElement.createIn(self._doc)
        beam_.setGeometry(beamGeom)

        return beam_

    def _createBaseBeam(self, beamType, length, radiusH, radiusV, **profile_par):
        if not BeamFactory.correctBeamType(beamType):
            raise RuntimeError("Invalid beam type")

        if beamType == BeamFactory.BT_Square:
            return self._createBaseBeam_Square(length, radiusH, radiusV)
        elif beamType == BeamFactory.BT_Circle:
            if abs(radiusH - radiusV) > epsilon:
                raise RuntimeError("Radii must be equal")
            return self._createBaseBeam_Circle(length, radiusH)
        elif beamType == BeamFactory.BT_IPE:
            return self._createBaseBeam_IPE(length, **profile_par)
        elif beamType == BeamFactory.BT_Diamond:
            return self._createBaseBeam_Diamond(length, radiusH, radiusV)

    def _splitBeamByPlane(self, beam, plnPoint, plnNormal):
        pt = Geom.Pnt(plnPoint)
        norm = Geom.Dir(plnNormal)
        pln = Geom.Pln(pt, norm)
        beam_vec = lx.vector_Element()
        beam2 = lx.Element.createIn(self._doc)
        geom = beam.getGeometry()
        beam2.setGeometry(geom)
        t = beam.getTransform()
        beam2.setTransform(t)
        self._doc.removeObject(beam)

        if lx.bop_splitByPlane(beam2, pln, beam_vec) != 0:
            print("Error in cut")
        self._doc.removeObject(beam_vec[1])
        self._doc.removeObject(beam2)

        t = beam_vec[0].getTransform()
        geom = beam_vec[0].getGeometry()
        beam_rez = lx.SubElement.createIn(self._doc)
        beam_rez.setGeometry(geom)
        beam_rez.setTransform(t)
        self._doc.removeObject(beam_vec[0])

        return beam_rez

    # def getCutBeam(self, beamType, startPt, endPt, radiusH, radiusV, startVec, endVec, beam_trsf):
    def getCutBeam(self, data):
        """
        data.bmType
        data.strPt
        data.endPt
        data.weight
        data.height
        data.strNorm
        data.endNorm
        data.trsfrm
        """
        beamType = data.bmType
        startPt = data.strPt
        endPt = data.endPt
        length = data.length
        radiusH = data.weight
        radiusV = data.height
        startNorm = data.strNorm
        endNorm = data.endNorm
        beam_trsf = data.trsfrm

        beamVec = Geom.Vec(startPt, endPt)
        dir = beamVec.normalized()
        # beamLen = [2*radiusV, length, 2*radiusV]
        beamLen = [max(4*radiusV, 4*radiusH), length, max(4*radiusV, 4*radiusH)]

        bool_endNorm = True
        bool_startNorm = True
        # enV_b = (data.endNorm_LCS.y()) < eps_DS and (data.endNorm_LCS.z()) < eps_DS
        if abs(data.endNorm_LCS.y()) < eps_DS and abs(data.endNorm_LCS.z()) < eps_DS:
            bool_endNorm = False
            beamLen[2] = 0.0

        # stV_b = data.strNorm_LCS.y() < eps_DS and data.strNorm_LCS.z() < eps_DS
        if abs(data.strNorm_LCS.y()) < eps_DS and abs(data.strNorm_LCS.z()) < eps_DS:
            bool_startNorm = False
            beamLen[0] = 0.0
        print(beamLen)
        beam = self._createBaseBeam(beamType, beamLen, radiusH, radiusV)
        # trans = Geom.Vec(0.0 - 2.*radiusV*dir.x(), 0.0, 0.0)
        # print()
        # beam.translate(trans)

        # beam.translate(Geom.Vec(startPt.x(), startPt.y(), startPt.z()), Geom.CoordSpace_WCS)

        beam.setTransform(beam_trsf)

        # startNorm = Geom.Vec(startVec.x(), startVec.y(), startVec.z())
        # endNorm = Geom.Vec(endVec.x(), endVec.y(), endVec.z())
        # print("bool_endNorm = ", bool_endNorm, "; bool_startNorm = ", bool_startNorm)

        if bool_endNorm:
            beam = self._splitBeamByPlane(beam, endPt, endNorm)
        if bool_startNorm:
            beam = self._splitBeamByPlane(beam, startPt, startNorm)

        return beam


class RailingSegments(lx.Railing):
    _cwColor = CW_COLOR
    _isFoundationParamName =          "_with_foundation"
    _isSparParamName =                "_with_spar"
    _heightParamName =                "_height"
    _handrailWidthParamName =         "_handrail_width"
    _handrailHeightParamName =        "_handrail_height"
    _handrailLedgeParamName =         "_handrail_ledge"
    _sparTypeParamName =              "_spar_type"
    _handrailSparGapParamName =       "_handrailSparGap"
    _sparWidthParamName =             "_spar_width"
    _sparHeightParamName =            "_spar_height"
    _chordWidthParamName =            "_bottom_chord_width"
    _chordHeightParamName =           "_bottom_chord_height"
    _supportWidthParamName =          "_support_width"
    _supportThicknessParamName =      "_support_Thickness"
    _railingTypeParamName =           "_railing_type"
    _columnDistanceParamName =        "_column_distance"
    _bottomDistanceParamName =        "_bottom_distance"
    _intermediateWidthParamName =     "_intermediate_width"
    _intermediateThicknessParamName = "_intermediate_thickness"
    _intermediateTypeParamName =      "_intermediate_type"
    _intermediateDirectionParamName = "_intermediate_direction"
    _footPlateWidthParamName =        "_foot_plate_width"
    _footPlateThicknessParamName =    "_foot_plate_thickness"
    _foundationHeightParamName =      "_foundation_height"
    _foundationWidthParamName =       "_foundation_width"
    _foundationLedgeParamName =       "_foundation_ledge"
    
    # _handrailSize = 0.12, 0.06
    # _supportSize = 0.05, 0.08
    # _topBeamSize = 0.05, 0.03
    # _apertureSize = 0.02, 0.04, 0.55
    # _botBeamSize = 0.05, 0.025
    # _footplateSize = 0.22, 0.04
    # _foundationSize = 0.3, 0.07
    
    _lineLengthName = "_length"
    _recalculateLenBtnName = "Redefine length"

    def getGlobalClassId(self):
        return GUID_CLASS
    
    def getScriptVersion(self):
        return 100

    def __init__(self, aArg):
        lx.Railing.__init__(self, aArg)
        self.registerPythonClass("RailingSegments", "OpenLxApp.Railing")
        # Register properties
        self.setPropertyHeader(lxstr("Railing"), -1)  # 480
        self.setPropertyGroupName(lxstr("Railing parameters"), 481)  # 481
        self._isFoundation = self.registerPropertyBool(self._isFoundationParamName, True, lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE, -1)  # 482
        self._height = self.registerPropertyDouble(self._heightParamName, 1.1+0.075, lx.Property.NOT_VISIBLE,
                                                   lx.Property.NOT_EDITABLE, -1)  # 482
        self._handrailWidth = self.registerPropertyDouble(self._handrailWidthParamName, 0.12, lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)  # 486
        self._handrailHeight = self.registerPropertyDouble(self._handrailHeightParamName, 0.06, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 487
        self._handrailLedge = self.registerPropertyDouble(self._handrailLedgeParamName, 0.15, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 487
        self._isSpar = self.registerPropertyBool(self._isSparParamName, True, lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE, -1)
        self._handrailSparGap = self.registerPropertyDouble(self._handrailSparGapParamName, 0.27, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 492
        self._sparWidth = self.registerPropertyDouble(self._sparWidthParamName, 0.05, lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)  # 486
        self._sparHeight = self.registerPropertyDouble(self._sparHeightParamName, 0.03, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 487

        self._supportWidth = self.registerPropertyDouble(self._supportWidthParamName, 0.08, lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)  # 486
        self._supportThickness = self.registerPropertyDouble(self._supportThicknessParamName, 0.05, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 487
        self._sparType = self.registerPropertyEnum(self._sparTypeParamName, 0, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 488)  # 488
        self._sparType.setEmpty()
        self._sparType.addEntry(lxstr("Square"), -1)  # 489
        self._sparType.addEntry(lxstr("Circle"), -1)  # 489
        self._sparType.addEntry(lxstr("Diamond"), -1)  # 490
        self._chordWidth = self.registerPropertyDouble(self._chordWidthParamName, 0.05, lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)  # 486
        self._chordHeight = self.registerPropertyDouble(self._chordHeightParamName, 0.025, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 487

        self._columnDistance = self.registerPropertyDouble(self._columnDistanceParamName, 1.95, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 491
        self._bottomDistance = self.registerPropertyDouble(self._bottomDistanceParamName, 0.09, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 492
        self._intermediateWidth = self.registerPropertyDouble(self._intermediateWidthParamName, 0.04,
                                                                  lx.Property.VISIBLE, lx.Property.EDITABLE, -1)  # 493
        self._intermediateThickness = self.registerPropertyDouble(self._intermediateThicknessParamName, 0.02,
                                                                  lx.Property.VISIBLE, lx.Property.EDITABLE, -1)  # 493
        self._intermediateType = self.registerPropertyEnum(self._intermediateTypeParamName, 0, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 494
        self._intermediateType.setEmpty()
        self._intermediateType.addEntry(lxstr("Square"), -1)  # 495
        self._intermediateType.addEntry(lxstr("Circle"), -1)  # 496

        self._intermediateDirection = self.registerPropertyEnum(self._intermediateDirectionParamName, 0, lx.Property.VISIBLE, 
                                                                lx.Property.EDITABLE, -1)  # 497
        self._intermediateDirection.setEmpty()
        self._intermediateDirection.addEntry(lxstr("Vertical"), -1)  # 498
        self._intermediateDirection.addEntry(lxstr("Horizontal"), -1)  # 499
        # self._recalcBtn = self.registerPropertyButton(self._recalculateBtnPropName, lx.Property.VISIBLE, 
        #                                               lx.Property.EDITABLE, -1)  # 500
        self._footPlateWidth = self.registerPropertyDouble(self._footPlateWidthParamName, 0.22, lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)  # 486
        self._footPlateThickness = self.registerPropertyDouble(self._footPlateThicknessParamName, 0.04, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 487

        self._foundationWidth = self.registerPropertyDouble(self._foundationWidthParamName, 0.3, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 491
        self._foundationHeight = self.registerPropertyDouble(self._foundationHeightParamName, 0.07, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)  # 491
        self._foundationLedge = self.registerPropertyDouble(self._foundationLedgeParamName, 0.25, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, -1)
        
        self._railingType = self.registerPropertyEnum(self._railingTypeParamName, 1, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 488)  # 488
        self._railingType.setEmpty()
        # for name in PROFILES:
        #     self._railingType.addEntry(lxstr(name), -1)

        #             lx.Property.EDITABLE, -1)
        
        self._representation = self.registerPropertyEnum("_representation", 1, lx.Property.VISIBLE, lx.Property.EDITABLE, 500)   
        self._representation.setEmpty()
        self._representation.addEntry(lxstr("Axis"), 507)        # Index 0 507
        self._representation.addEntry(lxstr("SolidModel"), 508)  # Index 1 508

        self._lineLength = self.registerPropertyDouble(self._lineLengthName, 0.0, lx.Property.VISIBLE, 
                                                       lx.Property.NOT_EDITABLE, 501)  # 501
        self._recalculateLenBtn = self.registerPropertyButton(self._recalculateLenBtnName, lx.Property.VISIBLE, 
                                                             lx.Property.EDITABLE, -1)
        # self._height.setVisible(False)
        self._handrailWidth.setVisible(False)
        self._handrailHeight.setVisible(False)
        self._handrailLedge.setVisible(False)
        self._isSpar.setVisible(False)
        self._handrailSparGap.setVisible(False)
        self._sparWidth.setVisible(False)
        self._sparHeight.setVisible(False)
        self._supportWidth.setVisible(False)
        self._supportThickness.setVisible(False)
        self._chordWidth.setVisible(False)
        self._chordHeight.setVisible(False)
        self._columnDistance.setVisible(False)
        self._bottomDistance.setVisible(False)
        self._intermediateWidth.setVisible(False)
        self._intermediateThickness.setVisible(False)
        self._intermediateType.setVisible(False)
        self._intermediateDirection.setVisible(False)
        self._railingType.setVisible(False)
        # self._handrailType.
        # self._bottomDistance
        self._intermediateType.setVisible(False)
        # self._sparType.setVisible(False)
        self._intermediateDirection.setVisible(False)
        self._setAllSteps()
        self._poolContainer = {}
        
        self.setBoundingBoxEnabled(False)
        #self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())

    def _setAllSteps(self):
        self._height.setSteps(0.1)
        self._handrailWidth.setSteps(0.001)
        self._handrailHeight.setSteps(0.001)
        self._handrailLedge.setSteps(0.01)
        self._supportWidth.setSteps(0.001)
        self._supportThickness.setSteps(0.001)
        self._columnDistance.setSteps(0.1)
        self._bottomDistance.setSteps(0.01)
        self._sparWidth.setSteps(0.001)
        self._sparHeight.setSteps(0.001)
        self._chordWidth.setSteps(0.001)
        self._chordHeight.setSteps(0.001)
        self._handrailSparGap.setSteps(0.01)
        self._intermediateWidth.setSteps(0.001)
        self._intermediateThickness.setSteps(0.001)
        self._footPlateWidth.setSteps(0.001)
        self._footPlateThickness.setSteps(0.001)
        self._foundationWidth.setSteps(0.01)
        self._foundationHeight.setSteps(0.01)
        self._foundationLedge.setSteps(0.01)


    def _supportPositionVectors(self, polyLine, segmId):
        prevLineTan = polyLine.segmEndTangent(segmId-1)
        nextLineTan = polyLine.segmStartTangent(segmId)
        prevHorTan = Geom.Vec(prevLineTan.x(), prevLineTan.y(), 0.0).normalized()
        nextHorTan = Geom.Vec(nextLineTan.x(), nextLineTan.y(), 0.0).normalized()
        prevNorm = Geom.Vec(prevHorTan.y(), -prevHorTan.x(), 0.0)
        nextNorm = Geom.Vec(-nextHorTan.y(), nextHorTan.x(), 0.0)
        bisec = (prevNorm+nextNorm).normalized()
        suppTang = Geom.Vec(bisec.y(), -bisec.x(), 0.0).normalized()
        e_x = Geom.Vec(0.0, 0.0, 1.0)
        return [e_x, bisec, suppTang]
    
    @staticmethod
    def _getTransform(e_x, e_y, e_z, locPt, scale_factor=1.0):
        e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
        e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
        e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
        M = Geom.Mat(e1, e2, e3)
        loc = Geom.XYZ(locPt.x(), locPt.y(), locPt.z())
        Tr = Geom.Trsf(M, loc, scale_factor)
        return Tr

    def _placeSupportsAccLine(self, model, polyLine):
        # partHeight = self._height.getValue() - self._handrailHeight.getValue()
        # supportRadius = self._intermediateThickness.getValue()
        foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0
        # print("placeSupportsAccLine - enter")
        hType = 0

        segmCount = polyLine.segmentCount()
        for segm in range(1, segmCount):
            suppPos = polyLine.segmStartPt(segm)
            suppDirections = self._supportPositionVectors(polyLine, segm)
            # start making transform: Matrix and translationPart
            # e_x = Geom.Vec(suppDirections[0])
            # e_y = Geom.Vec(suppDirections[1])
            # e_z = Geom.Vec(suppDirections[2])

            # Tr = self._getTransform(e_x, e_y, e_z, suppPos, scale_factor=1.0)
            # finish making transform
            lenSupp = self._height.getValue() - self._handrailHeight.getValue() + foundationHeight
            # strVec = Geom.Vec(0.0, 0.0, -1.0)
            # endVec = Geom.Vec(0.0, 0.0, 1.0)
            # suppEndPt = Geom.Pnt(suppPos.x(), suppPos.y(), suppPos.z()+lenSupp)
            # dtStr = DataStruct(hType, suppPos, suppEndPt, supportRadius, supportRadius, strVec, endVec, Tr)
            # beam_sup = self._poolContainer['supports'].createBeam(dtStr)
            # self.addSubElement(beam_sup)

            self._drawSupport(suppPos, suppDirections[2], lenSupp, e_basis=())

    def _calcColDist(self, divSpace):
        # lengthBal = self._columnDistance.getValue()
        lengthBal = 2.0
        nSegInLine = int(divSpace // lengthBal)

        if divSpace % lengthBal > (0.5*lengthBal):
            nSegInLine += 1

        if nSegInLine <= 0:
            nSegInLine = 1

        colDistance = divSpace / float(nSegInLine)
        # nSegInLine // 3, nSegInLine % 3
        return nSegInLine // 3, nSegInLine % 3, colDistance

    def _calcSpanParams(self, length, supportSize):
        colDist = self._colDistance.getValue()

        availLength = length - supportSize
        if colDist > (availLength + epsilon):
            return 1, availLength - supportSize

        spanCount = availLength // colDist
        spanTail = availLength - (colDist * spanCount)
        if spanTail > (colDist * 0.75):
            spanCount += 1
        spanLength = (availLength / spanCount) - supportSize

        return int(spanCount), spanLength

    def _fillAperture_Vertical(self, startPt, apertureVec, baseDist, repeat=14):
        dirVec = apertureVec.normalized()
        # typeInt = self._intermediateType.getValue()
        # bottomDist = self._bottomDistance.getValue()  # + self._footplateSize[1]
        # botBeamH, botBeamV = self._botBeamSize
        botBeamV = self._chordHeight.getValue()
        interWidth = self._intermediateWidth.getValue()
        interThick = self._intermediateThickness.getValue()
        # apertureHeight = self._apertureSize[2]
        apertureHeight = 0.6
        # if self._isSpar.getValue():
        #     apertureHeight -= (self._sparHeight.getValue() + self._handrailSparGap.getValue())

        # intermAngle = vecHAngle(apertureVec.x(), apertureVec.y())
        intermDist = (self._columnDistance.getValue() - (interThick * 2.0)) / 16.0
        intermRadius = interThick * 0.5
        intermNum = int(apertureVec.magnitude() // intermDist)
        # colDist = (apertureVec.magnitude() - (intermNum-1)*interThick) / float(intermNum)
        normApertVec = Geom.Vec(apertureVec.y(), -apertureVec.x(), 0.0).normalized()
        endVec = normApertVec.crossed(apertureVec).normalized()
        strVec = Geom.Vec(-endVec)
        e_x = Geom.Vec(0.0, 0.0, 1.0)
        e_y = Geom.Vec(-normApertVec.x(), -normApertVec.y(), 0.0)
        e_z = Geom.Vec(normApertVec.y(), -normApertVec.x(), 0.0)
        startPt_Z = 0.07 + 0.035 + 0.075

        intermDist = 0.0638 * baseDist  # 115/1830
        intFrDist = 0.0836 * baseDist        
        if repeat > 1:
            intermStep = dirVec.scaled(intFrDist)
        else:
            intermStep = dirVec.scaled(intermDist)

        intStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z()+startPt_Z)
        intStartPt.translate(intermStep)
        Tr = self._getTransform(e_x, e_y, e_z, intStartPt)
        intEndPt = Geom.Pnt(intStartPt.x(), intStartPt.y(), intStartPt.z()+apertureHeight)
        dtStr = DataStruct(1, intStartPt, intEndPt, 0.012, 0.012, strVec, endVec, Tr)
        beam_p = self._poolContainer['apertures'].createBeam(dtStr)
        self.addSubElement(beam_p)
        geom_p = beam_p.getGeometry()
        t_p = beam_p.getTransform()
        #
        for el in range(1, repeat):
            beam_nt = lx.SubElement.createIn(self.getDocument())
            beam_nt.setGeometry(geom_p)
            beam_nt.setTransform(t_p)
            beam_nt.translate(dirVec.scaled(el*intermDist), Geom.CoordSpace_WCS)
            self.addSubElement(beam_nt)

    def _findHorBeamCount(self, height):
        horBeamCount = 5  # Start width default count
        intThickness = self._intermediateThickness.getValue()

        while True:
            beamSpace = intThickness * float(horBeamCount)  # Find out what space beams take together
            if beamSpace <= (height + epsilon):
                return horBeamCount  # It is possible to fit this number of beams into available aperture
            else:
                # This number of beams doesn't fit available aperture
                horBeamCount -= 1
                if horBeamCount <= 0:
                    return 0

    def _fillAperture_Horizontal(self, model, apertureStartPt, apertureVec):
        apertureHeight = (self._height.getValue() - self._handrailHeight.getValue()) - (self._bottomDistance.getValue() + (self._intermediateThickness.getValue() * 2.0))
        beamCount = self._findHorBeamCount(apertureHeight)
        bottomSize = self._intermediateThickness.getValue() * 2.0
        apertureHeight = (self._height.getValue() - self._handrailHeight.getValue()) - (self._bottomDistance.getValue() + bottomSize)
        beamType = self._intermediateType.getValue()
        beamDPos = Geom.Vec(0.0, 0.0, apertureHeight / float(beamCount + 1))
        beamRadius = self._intermediateThickness.getValue() * 0.5
        beamStartPt = Geom.Pnt(apertureStartPt)
        beamStartPt.translate(beamDPos)
        beamEndPt = beamStartPt.translated(apertureVec)
        apertHorVec = Geom.Vec(apertureVec.x(), apertureVec.y(), 0.0).normalized()
        segmBase = apertureVec.normalized()
        endVec = Geom.Vec(apertHorVec) 
        strVec = Geom.Vec(-endVec)

        e_x = Geom.Vec(segmBase.x(), segmBase.y(), segmBase.z())
        e_y = Geom.Vec(-segmBase.y(), segmBase.x(), 0.0).normalized()
        e_z = e_x.crossed(e_y).normalized()
        Tr = self._getTransform(e_x, e_y, e_z, beamStartPt)
        # finish making transform
        dtStr = DataStruct(beamType, beamStartPt, beamEndPt, beamRadius, beamRadius, strVec, endVec, Tr)
        beam_p = self._poolContainer['apertures'].createBeam(dtStr)
        self.addSubElement(beam_p)
        geom_p = beam_p.getGeometry()
        t_p = beam_p.getTransform()
        # print(beamCount)

        for el in range(1, beamCount):
            # beamStartPt.translate(beamDPos)
            # beamEndPt = beamStartPt.translated(apertureVec)
            beamDPos = Geom.Vec(0.0, 0.0, el*apertureHeight / float(beamCount + 1))
            beam_nt = lx.SubElement.createIn(self.getDocument())
            beam_nt.setGeometry(geom_p)
            beam_nt.setTransform(t_p)
            beam_nt.translate(beamDPos, Geom.CoordSpace_WCS)
            self.addSubElement(beam_nt)

    
    def _drawSpar(self, sqType, stPt, endPt, radAx1, radAx2, startVec, endVec, Tr):
        dtStr = DataStruct(sqType, stPt, endPt, radAx1, radAx2, 
                           startVec, endVec, Tr)
        beam_top = self._poolContainer['topbeams'].createBeam(dtStr)
        self.addSubElement(beam_top)

    def _placeLineSpars(self, startPt, stepHLen, segmBase, segmHBase, segmRecCos, addSupport, parts=3):
        sqType = BeamFactory.BT_Circle
        e_x = Geom.Vec(segmBase.x(), segmBase.y(), segmBase.z())
        e_y = Geom.Vec(-segmBase.y(), segmBase.x(), 0.0).normalized()
        e_z = e_x.crossed(e_y).normalized()

        # Place top spar beam
        zShift = self._height.getValue() - 0.075
        topEndHOffs = parts*stepHLen - 0.05  # !!!- interThick * 2.0 * segmRecCos # !!!
        topEndOffs = topEndHOffs #* segmRecCos
        topStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + zShift)
        topStartPt = baseVecTranslate(topStartPt, segmBase, 0.05)
        topEndPt = baseVecTranslate(Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + zShift), segmBase, topEndOffs)
        # print('topStartPt', topStartPt.x(), 'topEndPt', topEndPt.x())
        # start making transform: Matrix and translationPart
        rR = 0.02415
        rot_dir = Geom.Dir(segmHBase.crossed(Geom.Vec(0, 0, 1)))

        Tr = self._getTransform(e_x, e_y, e_z, topStartPt)
        self._drawSpar(sqType, topStartPt, topEndPt, rR, rR, 
                        (-segmHBase).rotated(Geom.Ax1(topStartPt, rot_dir), math.pi/4.), 
                        segmHBase.rotated(Geom.Ax1(topEndPt, rot_dir), -math.pi/4.), Tr)
        # Place middle spar beam
        rR = 0.01615
        zShift = zShift - 0.32
        middleEndHOffs = parts*stepHLen - 0.05  # !!!- interThick * 2.0 * segmRecCos # !!!
        middleEndOffs = middleEndHOffs #* segmRecCos
        middleStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + zShift)
        middleStartPt = baseVecTranslate(middleStartPt, segmBase, 0.05)
        middleEndPt = baseVecTranslate(Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + zShift), segmBase, middleEndOffs)
        # print('midleStartPt', midleStartPt.x(), 'midleEndPt', midleEndPt.x())
        Tr = self._getTransform(e_x, e_y, e_z, middleStartPt)
        self._drawSpar(sqType, middleStartPt, middleEndPt, rR, rR, 
                        -segmHBase, segmHBase, Tr)
        # Place bottom spar beam
        rR = 0.02415
        zShift = zShift - 0.6  # self._height.getValue() - self._handrailHeight.getValue() - self._handrailSparGap.getValue() - topBeamV + foundationHeight
        bottomEndHOffs = parts*stepHLen - 0.05  # interThick * 2.0 * segmRecCos # !!!
        bottomEndOffs = bottomEndHOffs #* segmRecCos
        bottomStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + zShift)
        bottomStartPt = baseVecTranslate(bottomStartPt, segmBase, 0.05)
        bottomEndPt = baseVecTranslate(Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + zShift), segmBase, bottomEndOffs)
        # print('bottomStartPt', bottomStartPt.x(), 'bottomEndPt', bottomEndPt.x())
        Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
        self._drawSpar(sqType, bottomStartPt, bottomEndPt, rR, rR, 
                        (-segmHBase).rotated(Geom.Ax1(topStartPt, rot_dir), -math.pi/4.), 
                        segmHBase.rotated(Geom.Ax1(topEndPt, rot_dir), math.pi/4.), Tr)
        
        normSuppTang = Geom.Vec(segmBase.y(), -segmBase.x(), 0.0).normalized()
        e_x = Geom.Vec(0.0, 0.0, 1.0)
        e_y = Geom.Vec(-normSuppTang.x(), -normSuppTang.y(), 0.0)
        e_z = Geom.Vec(normSuppTang.y(), -normSuppTang.x(), 0.0)
        strVec = Geom.Vec(0.0, 0.0, -1.0)
        endVec = Geom.Vec(0.0, 0.0, 1.0)

        Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
        self._drawSpar(sqType, bottomStartPt, topStartPt, rR, rR, 
                        strVec.rotated(Geom.Ax1(bottomStartPt, rot_dir), math.pi/4.), 
                        endVec.rotated(Geom.Ax1(topStartPt, rot_dir), -math.pi/4.), Tr)

        Tr = self._getTransform(e_x, e_y, e_z, bottomEndPt)
        self._drawSpar(sqType, bottomEndPt, topEndPt, rR, rR, 
                        strVec.rotated(Geom.Ax1(bottomEndPt, rot_dir), -math.pi/4.), 
                        endVec.rotated(Geom.Ax1(topEndPt, rot_dir), math.pi/4.), Tr)

    
    def _placeLineStep(self, model, startPt, stepHLen, segmBase, segmHBase, segmRecCos, addSupport, parts=3):  # 
        # foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0
        # sqType = BeamFactory.BT_Diamond
        # sqType = BeamFactory.BT_Circle
       
        if parts:
            lenSupp = self._height.getValue()  # + foundationHeight
            suppStartPt = baseVecTranslate(startPt, segmBase, 3*0.05*stepHLen)
            self._fillAperture_Vertical(suppStartPt, -segmBase, 3*0.3*stepHLen, repeat=1)
            self._drawSupport(suppStartPt, segmBase, lenSupp)
            self._fillAperture_Vertical(suppStartPt, segmBase, 3*0.3*stepHLen, repeat=14)
            for i in range(parts-1):
                suppStartPt = baseVecTranslate(suppStartPt, segmBase, 3*0.3*stepHLen)
                self._drawSupport(suppStartPt, segmBase, lenSupp)
                self._fillAperture_Vertical(suppStartPt, segmBase, 3*0.3*stepHLen, repeat=14)
            suppStartPt = baseVecTranslate(startPt, segmBase, stepHLen*(parts-0.15))
            self._drawSupport(suppStartPt, segmBase, lenSupp)
            self._fillAperture_Vertical(suppStartPt, segmBase, 3*0.3*stepHLen, repeat=1)

        self._placeLineSpars(startPt, stepHLen, segmBase, segmHBase, segmRecCos, addSupport, parts=parts)
        # Fill aperture
        # apertureStartPt = Geom.Pnt(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z()+0.5*botBeamV)
        # apertureVec = segmBase * bottomEndOffs
        # self._fillAperture_Vertical(apertureStartPt, apertureVec)
        # if self._intermediateDirection.getValue() == 0:
        #     self._fillAperture_Vertical(model, apertureStartPt, apertureVec)
        # else:
        #     self._fillAperture_Horizontal(model, apertureStartPt, apertureVec)

    def _drawSupport(self, startSuppPt, segmBase, lenSupp, e_basis=None):
        foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0
        fdRadiusV = 0.5*foundationHeight
        sqType = BeamFactory.BT_IPE
        # supportRadius = self._intermediateThickness.getValue()
        supportWidth, supportLength = self._supportWidth.getValue(), self._supportThickness.getValue()
        normSuppTang = Geom.Vec(segmBase.y(), -segmBase.x(), 0.0).normalized()
        if e_basis:
            e_x, e_y, e_z = e_basis 
        else:    
            e_x = Geom.Vec(0.0, 0.0, 1.0)
            e_y = Geom.Vec(-normSuppTang.x(), -normSuppTang.y(), 0.0)
            e_z = Geom.Vec(normSuppTang.y(), -normSuppTang.x(), 0.0) 
        # e_x = Geom.Vec(0.0, 0.0, 1.0)
        # e_y = Geom.Vec(-normSuppTang.x(), -normSuppTang.y(), 0.0)
        # e_z = Geom.Vec(normSuppTang.y(), -normSuppTang.x(), 0.0)
        Tr = self._getTransform(e_x, e_y, e_z, startSuppPt)
        # finish making transform
        strVec = Geom.Vec(0.0, 0.0, -1.0)
        endVec = Geom.Vec(0.0, 0.0, 1.0)
        # endVec = normSuppTang.crossed(segmBase).normalized()
        endSuppPt = Geom.Pnt(startSuppPt.x(), startSuppPt.y(), startSuppPt.z()+lenSupp)
        dtStr = DataStruct(sqType, startSuppPt, endSuppPt, 0.5*supportLength, 0.5*supportLength, strVec, endVec, Tr)
        beam_sup = self._poolContainer['supports'].createBeam(dtStr)
        self.addSubElement(beam_sup)
        # Footplate is added
        footPlateV, footPlateRadiusH = self._footPlateThickness.getValue(), 0.5*self._footPlateWidth.getValue()
        startFootPt = Geom.Pnt(startSuppPt.x(), startSuppPt.y(), startSuppPt.z()+2*fdRadiusV)
        endFootPt = Geom.Pnt(startSuppPt.x(), startSuppPt.y(), startSuppPt.z()+2*fdRadiusV+footPlateV)
        e_x = Geom.Vec(0.0, 0.0, 1.0)
        e_y = Geom.Vec(-normSuppTang.x(), -normSuppTang.y(), 0.0)
        e_z = Geom.Vec(normSuppTang.y(), -normSuppTang.x(), 0.0) 
        Tr = self._getTransform(e_x, e_y, e_z, startFootPt)
        strVec = Geom.Vec(0.0, 0.0, -1.0)
        endVec = Geom.Vec(0.0, 0.0, 1.0)
        sqType = BeamFactory.BT_Square
        dtStr = DataStruct(sqType, startFootPt, endFootPt, footPlateRadiusH, footPlateRadiusH, strVec, endVec, Tr)
        beam_sup = self._poolContainer['supports'].createBeam(dtStr)
        self.addSubElement(beam_sup)

    def _placeLineSegment(self, model, startPt, endPt, startVecs, endVecs, isFirst, isLast, isClosed):
        # print("_placeLineSegment", self._railingType.getValue())
        startVec = startVecs[0]
        # endVec = endVecs[0]
        startVec1 = startVecs[1]
        endVec1 = endVecs[1]
        # Place handrails
        foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0
        fdRadiusV = 0.5*foundationHeight
        hrRadiusH = self._handrailWidth.getValue() * 0.5
        hrRadiusV = self._handrailHeight.getValue() * 0.5
        hrStartZDelta = self._height.getValue() - hrRadiusV + foundationHeight
        supportRadius = self._intermediateThickness.getValue()
        supportWidth, supportThickness = self._supportWidth.getValue(), self._supportThickness.getValue()
        # sqType = BeamFactory.BT_Square
        segmVec = Geom.Vec(startPt, endPt)
        segmBase = segmVec.normalized()
        hType = self._sparType.getValue()
        # start making transform: Matrix and translationPart
        e_x = Geom.Vec(segmBase.x(), segmBase.y(), segmBase.z())
        e_y = Geom.Vec(-segmBase.y(), segmBase.x(), 0.0).normalized()
        e_z = e_x.crossed(e_y).normalized()

        # build foundation
        if self._isFoundation.getValue():
            fdRadiusH = 0.5*self._foundationWidth.getValue()
            foundationLedge = self._foundationLedge.getValue()
            if isFirst:
                fdStartPt = baseVecTranslate(Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + fdRadiusV), startVec1, foundationLedge)
            else:
                fdStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + fdRadiusV)
            if isLast:
                fdEndPt = baseVecTranslate(Geom.Pnt(endPt.x(), endPt.y(), endPt.z() + fdRadiusV),  endVec1, foundationLedge)
            else:
                fdEndPt = Geom.Pnt(endPt.x(), endPt.y(), endPt.z() + fdRadiusV)
            Tr = self._getTransform(e_x, e_y, e_z, fdStartPt)
            dtStr = DataStruct(hType, fdStartPt, fdEndPt, fdRadiusH, fdRadiusV, startVec1, endVec1, Tr)
            beam = self._poolContainer['foundbeams'].createBeam(dtStr)
            self.addSubElement(beam)

        segmHorVec = Geom.Vec(segmVec.x(), segmVec.y(), 0.0) # corrected Vec
        segmHorBase = segmHorVec.normalized()
        
        segmHorLen = segmVec.magnitude()
        if segmHorLen < epsilon:
            return

        segmRecCos = 1.0 / segmBase.dot(segmHorBase)
        angle = Geom.Vec.angle(segmBase, startVec)
        # segmStartCos = 1.0 / math.sin(angle)
        # baseRecCos = 1.0 /segmBase.dot(segmHorBase)

        startSuppPt = Geom.Pnt(startPt)
        # buildStartOffs = 0.5*supportThickness * segmRecCos #* segmStartCos

        # buildEndOffs = segmHorLen + 0.5*supportThickness * segmRecCos
        endSuppPt = Geom.Pnt(endPt)
        if isLast and (not isClosed):
            # buildEndOffs = segmHorLen

            endSuppOffs = supportRadius * segmRecCos
            endSuppStPt = baseVecTranslate(endPt, -segmBase, endSuppOffs)

            # self._drawSupport(endSuppStPt, segmBase, lenSupp)
            endSuppPt = Geom.Pnt(endSuppStPt)

        sectionVec = Geom.Vec(startSuppPt, endSuppPt)
        sectionLen = sectionVec.magnitude()

        #stepNum, colHorDist = self._calcColDist(buildHorLen)
        sectionNum, remainder, colHorDist = self._calcColDist(divSpace=sectionLen)
        # colDist = buildLen / float(stepNum)
        # print('_placeLineSegment', supportLen, sectionNum, remainder, colHorDist)

        # stepStartPt = buildStartPt
        # print(f'_placeLineSegment: stepStartPt = ({stepStartPt.x()}, {stepStartPt.y()}, )')
        if sectionNum > 0:
            # Place bottom beam
            self._placeLineStep(model, startPt, colHorDist, segmBase, segmHorBase, segmRecCos, None, parts=3)  # , segmRecCos
            stepStartPt = baseVecTranslate(startPt, segmBase, 3*colHorDist)
            print(f'_placeLineSegment: stepStartPt = ({stepStartPt.x()}, {stepStartPt.y()}, )')
            for step in range(1, sectionNum):
                self._placeLineStep(model, stepStartPt, colHorDist, segmBase, segmHorBase, segmRecCos, None, parts=3)  # , segmRecCos
                stepStartPt = baseVecTranslate(stepStartPt, segmBase, 3*colHorDist)  # , segmBase, segmHorBase

        if remainder:
            self._placeLineStep(model, stepStartPt, colHorDist, segmBase, segmHorBase, segmRecCos, None, parts=remainder)  # , segmRecCos

    # def _extendStepLastPt(self, startPt, endPt, dLen):
    #     stepVec = Geom.Vec(startPt, endPt)
    #     stepBase = stepVec.normalized()

    #     stepLen = stepVec.magnitude()

    #     return baseVecTranslate(startPt, stepBase, stepLen + dLen)

    # def _setHorCutHandrailBeams(self, model, listPnt, listVec, vRadius, hRadius, isFirst, isLast, isLoop=False):
    #     typeB = self._handrailType.getValue()
    #     handrailLedge = self._handrailLedge.getValue()
    #     if isLoop:
    #         if typeB == 0:
    #             model.addCutHorBeam(typeB, listPnt[0], listPnt[1], hRadius, vRadius, -listVec[len(listVec) - 1], listVec[1])
    #         else:
    #             model.addCutHorBeam(typeB, listPnt[0], listPnt[1], hRadius, hRadius, -listVec[len(listVec) - 1], listVec[1])
    #     else:
    #         baseVec = Geom.Vec(listPnt[0], listPnt[1]).normalized()
    #         # start making transform: Matrix and translationPart
    #         e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #         e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #         e_z = e_x.crossed(e_y).normalized()

    #         Tr = self._getTransform(e_x, e_y, e_z, listPnt[0])
    #         # finish making transform
    #         stPt = Geom.Pnt(listPnt[0].x(), listPnt[0].y(), listPnt[0].z())
    #         enPt = Geom.Pnt(listPnt[1].x(), listPnt[1].y(), listPnt[1].z())
    #         if isFirst:
    #             stPt = baseVecTranslate(Geom.Pnt(stPt.x(), stPt.y(), stPt.z()), -baseVec, handrailLedge)
    #         # if isLast and len(listPnt) == 2:
    #         #     enPt = baseVecTranslate(Geom.Pnt(enPt.x(), enPt.y(), enPt.z()), baseVec, handrailLedge)
    #         if typeB == 0:
    #             dtStr = DataStruct(typeB, stPt, enPt, hRadius, vRadius, listVec[0], listVec[1], Tr)
    #         else:
    #             dtStr = DataStruct(typeB, stPt, enPt, hRadius, hRadius, listVec[0], listVec[1], Tr)
    #         beam_top = self._poolContainer['handrailbeams'].createBeam(dtStr)
    #         self.addSubElement(beam_top)


    #     for i in range(1, len(listPnt) - 2):
    #         baseVec = Geom.Vec(listPnt[i], listPnt[i+1]).normalized()
    #         # start making transform: Matrix and translationPart
    #         e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #         e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #         e_z = e_x.crossed(e_y).normalized()

    #         Tr = self._getTransform(e_x, e_y, e_z, listPnt[i])
    #         # finish making transform
    #         if typeB == 0:
    #             dtStr = DataStruct(typeB, listPnt[i], listPnt[i+1], hRadius, vRadius, -listVec[i], listVec[i + 1], Tr)
    #             # model.addCutHorBeam(typeB, listPnt[i], listPnt[i + 1], hRadius, vRadius, -listVec[i], listVec[i + 1])
    #         else:
    #             dtStr = DataStruct(typeB, listPnt[i], listPnt[i+1], hRadius, hRadius, -listVec[i], listVec[i + 1], Tr)
    #             # model.addCutHorBeam(typeB, listPnt[i], listPnt[i + 1], hRadius, hRadius, -listVec[i], listVec[i + 1])
    #         beam_top = self._poolContainer['topbeams'].createBeam(dtStr)
    #         self.addSubElement(beam_top)

    #     if isLoop:
    #         pass
    #         # dmodel.addHorCutBeam(listPnt[len(listPnt)-2], listPnt[len(listPnt)-1], vRadius, hRadius, preBisec, nexBisec)
    #         # model.adHorCutBeam(listPnt[len(listPnt)-1], listPnt[0], vRadius, hRadius, nexBisec, zeroBisec)
    #     elif len(listPnt)>2:
    #         baseVec = Geom.Vec(listPnt[len(listPnt)-2], listPnt[len(listPnt)-1]).normalized()
    #         # start making transform: Matrix and translationPart
    #         e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #         e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #         e_z = e_x.crossed(e_y).normalized()

    #         Tr = self._getTransform(e_x, e_y, e_z, listPnt[len(listPnt)-2])
    #         # finish making transform
    #         enPt = Geom.Pnt(listPnt[-1].x(), listPnt[-1].y(), listPnt[-1].z())
    #         if isLast:
    #             enPt = baseVecTranslate(Geom.Pnt(enPt.x(), enPt.y(), enPt.z()), baseVec, handrailLedge)
    #         if typeB == 0:
    #             dtStr = DataStruct(typeB, listPnt[len(listPnt) - 2], enPt, hRadius, vRadius,
    #                                 -listVec[len(listVec)-2], listVec[len(listVec)-1], Tr)
    #         else:
    #             dtStr = DataStruct(typeB, listPnt[len(listPnt) - 2], enPt, hRadius, hRadius,
    #                                 -listVec[len(listVec)-2], listVec[len(listVec)-1], Tr)
    #         beam_top = self._poolContainer['handrailbeams'].createBeam(dtStr)
    #         self.addSubElement(beam_top)

    # def _setArrSupports(self, model, arc, listParam, listVec, isLoop=False):
    #     sqType = BeamFactory.BT_Square
    #     foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0

    #     for i in range(1, len(listParam) - 1):
    #         curSuppPt = arc.paramPt(listParam[i])
    #         # partHeight = self._height.getValue() - self._handrailHeight.getValue()
    #         # supportRadius = self._intermediateThickness.getValue()

    #         curSuppTang = arc.paramTangent(listParam[i])
    #         lenSupp = self._height.getValue() - self._handrailHeight.getValue() + foundationHeight
            
    #         self._drawSupport(curSuppPt, curSuppTang, lenSupp)

    # def _setHorCutTopBeams(self, arc, listParam, listVec, isLoop=False):
    #     # if self._isFoundation.getValue():
    #     bottomDist = self._bottomDistance.getValue()
    #     interThick = self._intermediateThickness.getValue()
    #     # apertureHeight = self._apertureSize[2]
    #     apertureHeight = self._height.getValue() - self._handrailHeight.getValue() - self._bottomDistance.getValue() - self._chordHeight.getValue()

    #     sqType = BeamFactory.BT_Square
    #     # apertureHeight = self._apertureSize[2]
    #     botBeamH, botBeamV = self._sparWidth.getValue(), self._sparHeight.getValue()
    #     foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0

    #     paramRatio = arc.paramRatio()
    #     supportThickness = self._supportThickness.getValue()
    #     supportRadius = 0.5*supportThickness
    #     zShift = apertureHeight + 0.5*botBeamV + bottomDist + foundationHeight
    #     zShift = self._height.getValue() - self._handrailSparGap.getValue() - botBeamV - self._handrailHeight.getValue() + foundationHeight
        
    #     startTang = arc.paramTangent(listParam[0] + supportRadius*paramRatio)
    #     angle0 = Geom.Vec.angle(startTang, listVec[0])
    #     # segmStartSin = 1.0 / math.sin(angle0)

    #     baseVec = Geom.Vec(arc.paramPt(listParam[0]), arc.paramPt(listParam[1])).normalized()
    #     baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
    #     baseRecCos = 1.0 / baseVec.dot(baseHorVec)
    #     prePnt = arc.paramPt(listParam[0] + supportRadius*paramRatio*baseRecCos)  # * segmStartSin
    #     curPnt = arc.paramPt(listParam[1] - supportRadius*paramRatio*baseRecCos)
    #     bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z() + zShift)
    #     bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z() + zShift)
    #     # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[0], listVec[1])
    #     strVec = Geom.Vec(listVec[0].x(), listVec[0].y(), 0.0)
    #     endVec = Geom.Vec(listVec[1].x(), listVec[1].y(), 0.0)
    #     # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, vRadius, interThick, strVec, endVec)
    #     # start making transform: Matrix and translationPart
    #     e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #     e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #     e_z = e_x.crossed(e_y).normalized()

    #     Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
    #     # finish making transform
    #     # suppEndPt = Geom.Pnt(suppStartPt.x(), suppStartPt.y(), suppStartPt.z()+lenSupp)
    #     dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, 0.5*botBeamH, 0.5*botBeamV, strVec, endVec, Tr)
    #     beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
    #     self.addSubElement(beam_bot)

    #     for i in range(1, len(listParam) - 2):
    #         baseVec = Geom.Vec(arc.paramPt(listParam[i]), arc.paramPt(listParam[i+1])).normalized()
    #         baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
    #         baseRecCos = 1.0 / baseVec.dot(baseHorVec)
    #         prePnt = arc.paramPt(listParam[i] + supportRadius * paramRatio * baseRecCos)
    #         curPnt = arc.paramPt(listParam[i+1] - supportRadius * paramRatio * baseRecCos)
    #         bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z() + zShift)
    #         bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z() + zShift)
    #         # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[i], listVec[i+1])
    #         strVec = Geom.Vec(-listVec[i].x(), -listVec[i].y(), 0.0)
    #         endVec = Geom.Vec(listVec[i+1].x(), listVec[i+1].y(), 0.0)
    #         # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec)
    #         # start making transform: Matrix and translationPart
    #         e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #         e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #         e_z = e_x.crossed(e_y).normalized()

    #         Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
    #         # finish making transform
    #         # suppEndPt = Geom.Pnt(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z()+lenSupp)
    #         dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, 0.5*botBeamH, 0.5*botBeamV, strVec, endVec, Tr)
    #         beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
    #         self.addSubElement(beam_bot)

    #     if isLoop:
    #         pass
    #         #build prelast and last segment
    #         # nexPnt = Geom.Pnt(listPnt[0].x(), listPnt[0].y(), 0.0)
    #         # nexVec = Geom.Vec(nexPnt.x() - curPnt.x(), nexPnt.y() - curPnt.y(), 0.0)
    #         # nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0) / nexVec.magnitude()
    #         # nexBisec = (preNor + nexNor) / (preNor + nexNor).magnitude()
    #         # model.addHorCutBeam(listPnt[len(listParam)-2], listPnt[len(listPnt)-1], vRadius, hRadius, preBisec, nexBisec)
    #         # model.addHorCutBeam(listPnt[len(listParam)-1], listPnt[0], vRadius, hRadius, nexBisec, zeroBisec)
    #     elif len(listParam)>2:
    #         endTang = arc.paramTangent(listParam[len(listParam) - 1] - supportRadius)
    #         angle1 = Geom.Vec.angle(endTang, listVec[len(listVec)-1])
    #         segmEndSin = 1.0 / math.sin(angle1)
    #         baseVec = Geom.Vec(arc.paramPt(listParam[len(listParam) - 2]), arc.paramPt(listParam[len(listParam) - 1])).normalized()
    #         baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
    #         baseRecCos = 1.0 / baseVec.dot(baseHorVec)
    #         prePnt = arc.paramPt(listParam[len(listParam) - 2] + supportRadius*paramRatio*baseRecCos)
    #         curPnt = arc.paramPt(listParam[len(listParam) - 1] - supportRadius*paramRatio*baseRecCos)  # * segmEndSin
    #         bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z() + zShift)
    #         bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z() + zShift)
    #         # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[len(listVec)-2], listVec[len(listVec)-1])
    #         strVec = Geom.Vec(-listVec[len(listVec)-2].x(), -listVec[len(listVec)-2].y(), 0.0)
    #         endVec = Geom.Vec(listVec[len(listVec)-1].x(), listVec[len(listVec)-1].y(), 0.0)
    #         # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec)
    #         # start making transform: Matrix and translationPart
    #         e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #         e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #         e_z = e_x.crossed(e_y).normalized()

    #         Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
    #         # finish making transform
    #         # suppEndPt = Geom.Pnt(bottomStartPt.x(), suppStartPt.y(), suppStartPt.z()+lenSupp)
    #         dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec, Tr)
    #         beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
    #         self.addSubElement(beam_bot)

    # def _setHorCutBottomBeams(self, model, arc, listParam, listVec, isLoop=False):
    #     # vRadius, hRadius = 0.5*supportWidth, 0.5*supportLength
    #     bottomDist = self._bottomDistance.getValue()
    #     interThick = self._intermediateThickness.getValue()

    #     sqType = BeamFactory.BT_Square
    #     # apertureHeight = self._apertureSize[2]
    #     botBeamH, botBeamV = self._chordWidth.getValue(), self._sparHeight.getValue()
    #     foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0

    #     paramRatio = arc.paramRatio()
    #     supportRadius = self._intermediateThickness.getValue()
    #     startTang = arc.paramTangent(listParam[0] + supportRadius*paramRatio)
    #     angle0 = Geom.Vec.angle(startTang, listVec[0])
    #     # segmStartSin = 1.0 / math.sin(angle0)
    #     zShift = 0.5*botBeamV + bottomDist + foundationHeight

    #     baseVec = Geom.Vec(arc.paramPt(listParam[0]), arc.paramPt(listParam[1])).normalized()
    #     baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
    #     baseRecCos = 1.0 / baseVec.dot(baseHorVec)
    #     prePnt = arc.paramPt(listParam[0] + supportRadius*paramRatio*baseRecCos)  # * segmStartSin
    #     curPnt = arc.paramPt(listParam[1] - supportRadius*paramRatio*baseRecCos)
    #     bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z() + zShift)
    #     bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z() + zShift)
    #     # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[0], listVec[1])
    #     strVec = Geom.Vec(listVec[0].x(), listVec[0].y(), 0.0)
    #     endVec = Geom.Vec(listVec[1].x(), listVec[1].y(), 0.0)
    #     # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, vRadius, interThick, strVec, endVec)
    #     # start making transform: Matrix and translationPart
    #     e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #     e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #     e_z = e_x.crossed(e_y).normalized()

    #     Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
    #     # finish making transform
    #     # suppEndPt = Geom.Pnt(suppStartPt.x(), suppStartPt.y(), suppStartPt.z()+lenSupp)
    #     dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, 0.5*botBeamH, 0.5*botBeamV, strVec, endVec, Tr)
    #     beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
    #     self.addSubElement(beam_bot)
        

    #     for i in range(1, len(listParam) - 2):
    #         baseVec = Geom.Vec(arc.paramPt(listParam[i]), arc.paramPt(listParam[i+1])).normalized()
    #         baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
    #         baseRecCos = 1.0 / baseVec.dot(baseHorVec)
    #         prePnt = arc.paramPt(listParam[i] + supportRadius * paramRatio * baseRecCos)
    #         curPnt = arc.paramPt(listParam[i+1] - supportRadius * paramRatio * baseRecCos)
    #         bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z() + zShift)
    #         bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z() + zShift)
    #         # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[i], listVec[i+1])
    #         strVec = Geom.Vec(-listVec[i].x(), -listVec[i].y(), 0.0)
    #         endVec = Geom.Vec(listVec[i+1].x(), listVec[i+1].y(), 0.0)
    #         # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec)
    #         # start making transform: Matrix and translationPart
    #         e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #         e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #         e_z = e_x.crossed(e_y).normalized()

    #         Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
    #         # finish making transform
    #         # suppEndPt = Geom.Pnt(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z()+lenSupp)
    #         dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, 0.5*botBeamH, 0.5*botBeamV, strVec, endVec, Tr)
    #         beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
    #         self.addSubElement(beam_bot)

    #     if isLoop:
    #         #build prelast and last segment
    #         nexPnt = Geom.Pnt(listPnt[0].x(), listPnt[0].y(), 0.0)
    #         nexVec = Geom.Vec(nexPnt.x() - curPnt.x(), nexPnt.y() - curPnt.y(), 0.0)
    #         nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0) / nexVec.magnitude()
    #         nexBisec = (preNor + nexNor) / (preNor + nexNor).magnitude()
    #         # model.addHorCutBeam(listPnt[len(listParam)-2], listPnt[len(listPnt)-1], vRadius, hRadius, preBisec, nexBisec)
    #         # model.addHorCutBeam(listPnt[len(listParam)-1], listPnt[0], vRadius, hRadius, nexBisec, zeroBisec)
    #     elif len(listParam)>2:
    #         endTang = arc.paramTangent(listParam[len(listParam) - 1] - supportRadius)
    #         angle1 = Geom.Vec.angle(endTang, listVec[len(listVec)-1])
    #         segmEndSin = 1.0 / math.sin(angle1)
    #         baseVec = Geom.Vec(arc.paramPt(listParam[len(listParam) - 2]), arc.paramPt(listParam[len(listParam) - 1])).normalized()
    #         baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
    #         baseRecCos = 1.0 / baseVec.dot(baseHorVec)
    #         prePnt = arc.paramPt(listParam[len(listParam) - 2] + supportRadius*paramRatio*baseRecCos)
    #         curPnt = arc.paramPt(listParam[len(listParam) - 1] - supportRadius*paramRatio*baseRecCos)  # * segmEndSin
    #         bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z() + zShift)
    #         bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z() + zShift)
    #         # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[len(listVec)-2], listVec[len(listVec)-1])
    #         strVec = Geom.Vec(-listVec[len(listVec)-2].x(), -listVec[len(listVec)-2].y(), 0.0)
    #         endVec = Geom.Vec(listVec[len(listVec)-1].x(), listVec[len(listVec)-1].y(), 0.0)
    #         # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec)
    #         # start making transform: Matrix and translationPart
    #         e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #         e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #         e_z = e_x.crossed(e_y).normalized()

    #         Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
    #         # finish making transform
    #         # suppEndPt = Geom.Pnt(bottomStartPt.x(), suppStartPt.y(), suppStartPt.z()+lenSupp)
    #         dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec, Tr)
    #         beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
    #         self.addSubElement(beam_bot)

    # def _setHorCutFoundation(self, arc, listParam, listVec, isFirst, isLast, isLoop=False):
    #     if self._isFoundation.getValue():
    #         # typeB = self._handrailType.getValue()
    #         wRadius = 0.5 * self._foundationWidth.getValue()
    #         hRadius = 0.5 * self._foundationHeight.getValue()
    #         # vRadius, hRadius = 0.5*supportWidth, 0.5*supportLength
    #         # bottomDist = self._bottomDistance.getValue()
    #         # interThick = self._intermediateThickness.getValue()

    #         sqType = BeamFactory.BT_Square
    #         paramRatio = arc.paramRatio()
    #         supportRadius = self._intermediateThickness.getValue()
    #         startTang = arc.paramTangent(listParam[0] + supportRadius*paramRatio)
    #         angle0 = Geom.Vec.angle(startTang, listVec[0])
    #         # segmStartSin = 1.0 / math.sin(angle0)
    #         zShift = hRadius

    #         baseVec = Geom.Vec(arc.paramPt(listParam[0]), arc.paramPt(listParam[1])).normalized()
    #         baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
    #         baseRecCos = 1.0 / baseVec.dot(baseHorVec)
    #         prePnt = arc.paramPt(listParam[0])  # * segmStartSin
    #         curPnt = arc.paramPt(listParam[1])
    #         foundationLedge = self._foundationLedge.getValue()
    #         if isFirst:
    #             bottomStartPt = baseVecTranslate(Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z()+zShift), -baseVec, foundationLedge)
    #         else:
    #             bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z()+zShift)
    #         # if isLast:
    #         #     bottomEndPt = baseVecTranslate(Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z()+zShift), baseVec, foundationLedge)
    #         # else:
    #         bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z()+zShift)
    #         # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[0], listVec[1])
    #         strVec = Geom.Vec(listVec[0].x(), listVec[0].y(), 0.0)
    #         endVec = Geom.Vec(listVec[1].x(), listVec[1].y(), 0.0)
    #         # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, vRadius, interThick, strVec, endVec)
    #         # start making transform: Matrix and translationPart
    #         e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #         e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #         e_z = e_x.crossed(e_y).normalized()

    #         Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
    #         # finish making transform
    #         # suppEndPt = Geom.Pnt(suppStartPt.x(), suppStartPt.y(), suppStartPt.z()+lenSupp)
    #         dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, wRadius, hRadius, strVec, endVec, Tr)
    #         beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
    #         self.addSubElement(beam_bot)
            

    #         for i in range(1, len(listParam) - 2):
    #             baseVec = Geom.Vec(arc.paramPt(listParam[i]), arc.paramPt(listParam[i+1])).normalized()
    #             baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
    #             baseRecCos = 1.0 / baseVec.dot(baseHorVec)
    #             prePnt = arc.paramPt(listParam[i])
    #             curPnt = arc.paramPt(listParam[i+1])
    #             bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z()+zShift)
    #             bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z()+zShift)
    #             # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[i], listVec[i+1])
    #             strVec = Geom.Vec(-listVec[i].x(), -listVec[i].y(), 0.0)
    #             endVec = Geom.Vec(listVec[i+1].x(), listVec[i+1].y(), 0.0)
    #             # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec)
    #             # start making transform: Matrix and translationPart
    #             e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #             e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #             e_z = e_x.crossed(e_y).normalized()

    #             Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
    #             # finish making transform
    #             # suppEndPt = Geom.Pnt(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z()+lenSupp)
    #             dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, wRadius, hRadius, strVec, endVec, Tr)
    #             beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
    #             self.addSubElement(beam_bot)

    #         if isLoop:
    #             #build prelast and last segment
    #             nexPnt = Geom.Pnt(listPnt[0].x(), listPnt[0].y(), 0.0)
    #             nexVec = Geom.Vec(nexPnt.x() - curPnt.x(), nexPnt.y() - curPnt.y(), 0.0)
    #             nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0) / nexVec.magnitude()
    #             nexBisec = (preNor + nexNor) / (preNor + nexNor).magnitude()
    #             # model.addHorCutBeam(listPnt[len(listParam)-2], listPnt[len(listPnt)-1], vRadius, hRadius, preBisec, nexBisec)
    #             # model.addHorCutBeam(listPnt[len(listParam)-1], listPnt[0], vRadius, hRadius, nexBisec, zeroBisec)
    #         elif len(listParam)>2:
    #             endTang = arc.paramTangent(listParam[len(listParam) - 1] - supportRadius)
    #             angle1 = Geom.Vec.angle(endTang, listVec[len(listVec)-1])
    #             segmEndSin = 1.0 / math.sin(angle1)
    #             baseVec = Geom.Vec(arc.paramPt(listParam[len(listParam) - 2]), arc.paramPt(listParam[len(listParam) - 1])).normalized()
    #             baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
    #             baseRecCos = 1.0 / baseVec.dot(baseHorVec)
    #             prePnt = arc.paramPt(listParam[len(listParam) - 2] )
    #             curPnt = arc.paramPt(listParam[len(listParam) - 1] )  # * segmEndSin
    #             # if isFirst:
    #             #     bottomStartPt = baseVecTranslate(Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z()+zShift), -baseVec, foundationLedge)
    #             # else:
    #             bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z()+zShift)
    #             if isLast:
    #                 bottomEndPt = baseVecTranslate(Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z()+zShift), baseVec, foundationLedge)
    #             else:
    #                 bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z()+zShift)
    #             strVec = Geom.Vec(-listVec[len(listVec)-2].x(), -listVec[len(listVec)-2].y(), 0.0)
    #             endVec = Geom.Vec(listVec[len(listVec)-1].x(), listVec[len(listVec)-1].y(), 0.0)
    #             # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec)
    #             # start making transform: Matrix and translationPart
    #             e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
    #             e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
    #             e_z = e_x.crossed(e_y).normalized()

    #             Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
    #             # finish making transform
    #             # suppEndPt = Geom.Pnt(bottomStartPt.x(), suppStartPt.y(), suppStartPt.z()+lenSupp)
    #             dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, wRadius, hRadius, strVec, endVec, Tr)
    #             beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
    #             self.addSubElement(beam_bot)
    
    def _placeArcFonfation(self, arc, stepStartParam, stepEndParam, isFirst, isLast):  # , stepHLen, parts=3
        print("_placeArcFonfation: ", self._isFoundation.getValue())
        if self._isFoundation.getValue():
            foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0
            fdRadiusH, fdRadiusV = 0.5*self._foundationWidth.getValue(), 0.5*foundationHeight
            foundationLedge = self._foundationLedge.getValue()
            fdStartPt = arc.paramPt(stepStartParam)
            fdEndPt = arc.paramPt(stepEndParam)
            bStartVec = arc.paramTangent(stepStartParam)
            bEndVec = arc.paramTangent(stepEndParam)       
            # startVec = Geom.Vec(0, 0, 1)
            if isFirst:
                fdStartPt = baseVecTranslate(Geom.Pnt(fdStartPt.x(), fdStartPt.y(), fdStartPt.z() + fdRadiusV), -bStartVec, foundationLedge)
            else:
                fdStartPt = Geom.Pnt(fdStartPt.x(), fdStartPt.y(), fdStartPt.z() + fdRadiusV)
            if isLast:
                fdEndPt = baseVecTranslate(Geom.Pnt(fdEndPt.x(), fdEndPt.y(), fdEndPt.z() + fdRadiusV),  bEndVec, foundationLedge)
            else:
                fdEndPt = Geom.Pnt(fdEndPt.x(), fdEndPt.y(), fdEndPt.z() + fdRadiusV)
            segmBase = Geom.Vec(fdStartPt, fdEndPt).normalized()
            e_x = Geom.Vec(segmBase.x(), segmBase.y(), segmBase.z())
            e_y = Geom.Vec(-segmBase.y(), segmBase.x(), 0.0).normalized()
            e_z = e_x.crossed(e_y).normalized()
            Tr = self._getTransform(e_x, e_y, e_z, fdStartPt)
            hType = BeamFactory.BT_Square
            dtStr = DataStruct(hType, fdStartPt, fdEndPt, fdRadiusH, fdRadiusV, -bStartVec, bEndVec, Tr)
            beam = self._poolContainer['foundbeams'].createBeam(dtStr)
            self.addSubElement(beam)
    
    def _placeArcSpars(self, arc, startParam, endParam, stepHLen, parts=3, 
                      start=False, middle=False, end=False):
        
        # sqType = BeamFactory.BT_Square
        sqType = BeamFactory.BT_Circle
        # sqType = BeamFactory.BT_Diamond

        if middle:
            startPt = arc.paramPt(startParam)
            startBase = arc.paramTangent(startParam)
            endPt = arc.paramPt(endParam)
            endBase = arc.paramTangent(endParam)
            segmBase = Geom.Vec(startPt, endPt).normalized()

        e_x = Geom.Vec(segmBase.x(), segmBase.y(), segmBase.z())
        e_y = Geom.Vec(-segmBase.y(), segmBase.x(), 0.0).normalized()
        e_z = e_x.crossed(e_y).normalized()

        rR = 0.02415
        zShift = self._height.getValue() - 0.075
        topStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + zShift)
        topEndPt = Geom.Pnt(endPt.x(), endPt.y(), endPt.z() + zShift)
        Tr = self._getTransform(e_x, e_y, e_z, topStartPt)
        self._drawSpar(sqType, topStartPt, topEndPt, rR, rR, 
                        -startBase, endBase, Tr)

        rR = 0.01615
        zShift = zShift - 0.32
        middleStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + zShift)
        middleEndPt = Geom.Pnt(endPt.x(), endPt.y(), endPt.z() + zShift)
        Tr = self._getTransform(e_x, e_y, e_z, middleStartPt)
        self._drawSpar(sqType, middleStartPt, middleEndPt, rR, rR, 
                        -startBase, endBase, Tr)
        
        rR = 0.02415
        zShift = zShift - 0.6
        bottomStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + zShift)
        bottomEndPt = Geom.Pnt(endPt.x(), endPt.y(), endPt.z() + zShift)
        # self._fillAperture_Vertical(suppStartPt, -segmBase, 3*0.3*stepHLen, repeat=1)
        Tr = self._getTransform(e_x, e_y, e_z, bottomStartPt)
        self._drawSpar(sqType, bottomStartPt, bottomEndPt, rR, rR, 
                        -startBase, endBase, Tr)
        
        self._fillAperture_Vertical(startPt, segmBase, 3*0.3*stepHLen, repeat=14)
        
        if start:
            e_x = Geom.Vec(startBase.x(), startBase.y(), startBase.z())
            e_y = Geom.Vec(-startBase.y(), startBase.x(), 0.0).normalized()
            e_z = e_x.crossed(e_y).normalized()
            rot_dir = Geom.Dir(startBase.crossed(Geom.Vec(0, 0, 1)))

            rR = 0.02415          
            startTopEdgePt = baseVecTranslate(topStartPt, -startBase, stepHLen*3*0.05 - 0.05)
            Tr = self._getTransform(e_x, e_y, e_z, startTopEdgePt)
            self._drawSpar(sqType, startTopEdgePt, topStartPt, rR, rR, 
                        (-startBase).rotated(Geom.Ax1(startTopEdgePt, rot_dir), math.pi/4.), 
                        startBase, Tr)
            rR = 0.01615
            startEdgePt = baseVecTranslate(middleStartPt, -startBase, stepHLen*3*0.05 - 0.05)
            Tr = self._getTransform(e_x, e_y, e_z, startEdgePt)
            self._drawSpar(sqType, startEdgePt, middleStartPt, rR, rR, 
                        -startBase, startBase, Tr)
            rR = 0.02415
            startBotEdgePt = baseVecTranslate(bottomStartPt, -startBase, stepHLen*3*0.05 - 0.05)
            Tr = self._getTransform(e_x, e_y, e_z, startBotEdgePt)
            self._drawSpar(sqType, startBotEdgePt, bottomStartPt, rR, rR, 
                        (-startBase).rotated(Geom.Ax1(startBotEdgePt, rot_dir), -math.pi/4.), 
                        startBase, Tr)
            
            normSuppTang = Geom.Vec(startBase.y(), -startBase.x(), 0.0).normalized()
            e_x = Geom.Vec(0.0, 0.0, 1.0)
            e_y = Geom.Vec(-normSuppTang.x(), -normSuppTang.y(), 0.0)
            e_z = Geom.Vec(normSuppTang.y(), -normSuppTang.x(), 0.0)
            strVec = Geom.Vec(0.0, 0.0, -1.0)
            endVec = Geom.Vec(0.0, 0.0, 1.0)
            Tr = self._getTransform(e_x, e_y, e_z, startBotEdgePt)
            self._drawSpar(sqType, startBotEdgePt, startTopEdgePt, rR, rR, 
                        strVec.rotated(Geom.Ax1(startBotEdgePt, rot_dir), math.pi/4.), 
                        endVec.rotated(Geom.Ax1(startTopEdgePt, rot_dir), -math.pi/4.), Tr)

            self._fillAperture_Vertical(startPt, -startBase, 3*0.3*stepHLen, repeat=1)

        if end:
            e_x = Geom.Vec(endBase.x(), endBase.y(), endBase.z())
            e_y = Geom.Vec(-endBase.y(), endBase.x(), 0.0).normalized()
            e_z = e_x.crossed(e_y).normalized()
            rot_dir = Geom.Dir(endBase.crossed(Geom.Vec(0, 0, 1)))
            endTopEdgePt = baseVecTranslate(topEndPt, endBase, stepHLen*3*0.05 - 0.05)
            Tr = self._getTransform(e_x, e_y, e_z, topEndPt)
            self._drawSpar(sqType, topEndPt, endTopEdgePt, rR, rR, 
                        -endBase, 
                        endBase.rotated(Geom.Ax1(endTopEdgePt, rot_dir), -math.pi/4.), Tr)
            
            endEdgePt = baseVecTranslate(middleEndPt, endBase, stepHLen*3*0.05 - 0.05)
            Tr = self._getTransform(e_x, e_y, e_z, middleEndPt)
            self._drawSpar(sqType, middleEndPt, endEdgePt, rR, rR, 
                        -endBase, endBase, Tr)
            
            endBotEdgePt = baseVecTranslate(bottomEndPt, endBase, stepHLen*3*0.05 - 0.05)
            Tr = self._getTransform(e_x, e_y, e_z, bottomEndPt)
            self._drawSpar(sqType, bottomEndPt, endBotEdgePt, rR, rR, 
                        -endBase, 
                        endBase.rotated(Geom.Ax1(endBotEdgePt, rot_dir), math.pi/4.), Tr)
            
            normSuppTang = Geom.Vec(endBase.y(), -endBase.x(), 0.0).normalized()
            e_x = Geom.Vec(0.0, 0.0, 1.0)
            e_y = Geom.Vec(-normSuppTang.x(), -normSuppTang.y(), 0.0)
            e_z = Geom.Vec(normSuppTang.y(), -normSuppTang.x(), 0.0)
            strVec = Geom.Vec(0.0, 0.0, -1.0)
            endVec = Geom.Vec(0.0, 0.0, 1.0)
            Tr = self._getTransform(e_x, e_y, e_z, endBotEdgePt)
            self._drawSpar(sqType, endBotEdgePt, endTopEdgePt, rR, rR, 
                        strVec.rotated(Geom.Ax1(endBotEdgePt, rot_dir), -math.pi/4.), 
                        endVec.rotated(Geom.Ax1(endTopEdgePt, rot_dir), math.pi/4.), Tr)
            
            self._fillAperture_Vertical(endPt, endBase, 3*0.3*stepHLen, repeat=1)
    
    def _placeArcStep(self, arc, stepStartParam, stepEndParam, stepHLen, isFirst, isLast, parts=3):
        # Place rest of the geometry
        paramRatio = arc.paramRatio()
        lenSupp = self._height.getValue()
        rR = 0.02415
        # bottomDist = self._bottomDistance.getValue()
        # interThick = self._intermediateThickness.getValue()
        # foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0
        # botBeamV = self._chordHeight.getValue()
        
        previousParam = stepParam = stepStartParam + stepHLen*3*0.05 * paramRatio
        suppStartPt = arc.paramPt(stepParam)
        supportBase = arc.paramTangent(stepParam)
        self._drawSupport(suppStartPt, supportBase, lenSupp)
        if self._isFoundation.getValue():
            self._placeArcFonfation(arc, stepStartParam, stepParam, isFirst, False)

        # self._placeArcSpars(arc, startParam, endParam, stepHLen, parts=3, 
        #               start=False, middle=False, end=False)

        supportPt = suppStartPt
        for _ in range(1, parts):
            
            # previousSupportBase = supportBase
            stepParam += stepHLen*3*0.3 * paramRatio
            supportPt = arc.paramPt(stepParam)
            supportBase = arc.paramTangent(stepParam)
            self._drawSupport(supportPt, supportBase, lenSupp)

            self._placeArcSpars(arc, previousParam, stepParam, stepHLen, parts=3, 
                                start=(_==1), middle=True)
            if self._isFoundation.getValue():
                self._placeArcFonfation(arc, previousParam, stepParam, False, False)
            previousParam = stepParam

        stepParam = stepStartParam + stepHLen*(parts-0.15) * paramRatio
        suppEndPt = arc.paramPt(stepParam)
        suppEndBase = arc.paramTangent(stepParam)
        self._drawSupport(suppEndPt, suppEndBase, lenSupp)

        self._placeArcFonfation(arc, previousParam, stepParam, False, False)

        self._placeArcSpars(arc, previousParam, stepParam, 
                            stepHLen, parts=parts, start=(parts==1), middle=True, end=True)
        print("stepParams: ", stepParam, stepEndParam)
        self._placeArcFonfation(arc, stepParam, stepEndParam, False, isLast)
        # if self._intermediateDirection.getValue() == 0:
        #     self._fillAperture_Vertical(model, apertureStartPt, apertureVec)
        # else:
        #     self._fillAperture_Horizontal(model, apertureStartPt, apertureVec)

    def _placeArcSegment(self, arc, startVecs, endVecs, isFirst, isLast, isClosed):
        startVec = startVecs[0]
        # endVec = endVecs[0]
        # startVec1 = startVecs[1]
        # endVec1 = endVecs[1]

        arcLen = arc.length()
        paramRatio = arc.paramRatio()
        foundationHeight = self._foundationHeight.getValue() if self._isFoundation.getValue() else 0.0
        supportRadius = self._intermediateThickness.getValue()
        # supportWidth, supportLength = 0.08, 0.05
        # supportSize = supportRadius * 2.0
        startParam = 0.0
        endParam = 1.0

        hrRadiusH = self._handrailWidth.getValue() * 0.5
        hrRadiusV = self._handrailHeight.getValue() * 0.5
        hrStartZDelta = self._height.getValue() - hrRadiusV + foundationHeight
        # sqType = BeamFactory.BT_Square
        # lenSupp = self._height.getValue() - self._handrailHeight.getValue() + foundationHeight


        buildParamLen = endParam - startParam
        sectionLen = buildParamLen * arcLen
        # print startParam, endParam

        # stepNum, colHorDist = self._calcColDist(buildLen)
        sectionNum, remainder, colHorDist = self._calcColDist(divSpace=sectionLen)

        stepParam = startParam
        # stepStartPt = arc.paramPt(stepParam) #*segmStartSin
        lastStepId = sectionNum

        paramDist = 3*colHorDist
        stepStartParam = stepParam
        for _ in range(lastStepId):
            stepEndParam = stepStartParam + paramDist * paramRatio

            self._placeArcStep(arc, stepStartParam, stepEndParam, colHorDist, 
                               isFirst and (_==0), False)

            stepStartParam = stepEndParam

        if remainder:
            paramDist = remainder*colHorDist
            stepEndParam += paramDist
            stepEndPt = arc.paramPt(stepParam) # *segmEndSin
            self._placeArcStep(arc, stepStartParam, stepEndParam, colHorDist, False, isLast, parts=remainder)

    def _setAllArcVectors(self, listPnt, startVec, endVec, isLoop=False):
        listVectors = [[], []]
        if isLoop:
            prePnt = Geom.Pnt(listPnt[len(listPnt) - 1].x(), listPnt[len(listPnt) - 1].y(), 0.0)
            curPnt = Geom.Pnt(listPnt[0].x(), listPnt[0].y(), 0.0)
            nexPnt = Geom.Pnt(listPnt[1].x(), listPnt[1].y(), 0.0)
            preVec = Geom.Vec(curPnt.x() - prePnt.x(), curPnt.y() - prePnt.y(), 0.0)
            nexVec = Geom.Vec(nexPnt.x() - curPnt.x(), nexPnt.y() - curPnt.y(), 0.0)
            preNor = Geom.Vec(-preVec.y(), preVec.x(), 0.0) / preVec.magnitude()
            nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0) / nexVec.magnitude()
            preBisec = (preNor + nexNor) / (preNor + nexNor).magnitude()
            zeroBisec = preBisec
            curPnt = nexPnt
            preNor = nexNor
        else:
            prePnt = Geom.Pnt(listPnt[0].x(), listPnt[0].y(), listPnt[0].z())
            curPnt = Geom.Pnt(listPnt[1].x(), listPnt[1].y(), listPnt[1].z())
            preVec = Geom.Vec(curPnt.x() - prePnt.x(), curPnt.y() - prePnt.y(), curPnt.z() - prePnt.z())
            preVec.normalize()
            preNor = Geom.Vec(-preVec.y(), preVec.x(), 0.0) / preVec.magnitude()
            # preBisec = Geom.Vec(startVec)
            # listVectors.append(preBisec)
            listVectors[0] += [startVec[0]]
            listVectors[1] += [startVec[1]]
            #printVec("Bisec start", preBisec)                                                                                    

        for i in range(1, len(listPnt) - 1):
            nexPnt = Geom.Pnt(listPnt[i+1].x(), listPnt[i+1].y(), listPnt[i+1].z())
            nexVec = Geom.Vec(nexPnt.x() - curPnt.x(), nexPnt.y() - curPnt.y(), nexPnt.z() - curPnt.z())
            nexVec.normalize()
            nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0) / nexVec.magnitude()
            nexBisec = (preNor + nexNor) / (preNor + nexNor).magnitude()
            bis = (nexVec - preVec).normalized()
            norm = ((-preVec).crossed(nexVec)).normalized()
            norVec = (norm.crossed(bis)).normalized()
            # listVectors.append(nexBisec)
            listVectors[0] += [bis]
            listVectors[1] += [norVec]
            #printVec("Bisec", nexBisec)
            curPnt = nexPnt
            preNor = nexNor
            # !!!
            preVec = nexVec
            preBisec = nexBisec

        if isLoop:
            #build prelast and last segment
            nexPnt = Geom.Pnt(listPnt[0].x(), listPnt[0].y(), 0.0)
            nexVec = Geom.Vec(nexPnt.x() - curPnt.x(), nexPnt.y() - curPnt.y(), 0.0)
            nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0) / nexVec.magnitude()
            nexBisec = (preNor + nexNor) / (preNor + nexNor).magnitude()
        else:
            nexBisec = endVec
            # listVectors.append(nexBisec)
            listVectors[0] += [endVec[0]]
            listVectors[1] += [endVec[1]]
            #printVec("Bisec end", nexBisec)
            #print(" _allvecs_ ", len(listVectors))

        return listVectors

    def _getStartVector(self, polyLine, segmId):
        isFirst = bool(segmId == 0)
        # isLast = bool(segmId == (polyLine.segmentCount() - 1))
        isClosed = polyLine._closed
        startVector = []

        segmType = polyLine.segmentType(segmId)
        if isFirst and (not isClosed):
            if segmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(segmId)
                endPt = polyLine.segmEndPt(segmId)
                vec = Geom.Vec(startPt, endPt)
                vec.normalize()
                startVector += [Geom.Vec(-vec.y(), vec.x(), 0.0)]
                startVector += [Geom.Vec(-vec.x(), -vec.y(), 0.0)]
            elif segmType == PolylineData.SegmType_Arc:
                arc = polyLine.segmArc(segmId)
                vec = arc.startTangent()
                vec.normalize()
                startVector += [Geom.Vec(-vec.y(), vec.x(), 0.0)]
                startVector += [Geom.Vec(-vec.x(), -vec.y(), 0.0)]
        elif isFirst and isClosed:
            if segmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(0)
                endPt = polyLine.segmEndPt(0)
                curVec = Geom.Vec(startPt, endPt)
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            elif segmType == PolylineData.SegmType_Arc:
                arc = polyLine.segmArc(0)
                curVec = arc.startTangent()
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            preSegmType = polyLine.segmentType(polyLine.segmentCount() - 1)
            if preSegmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(polyLine.segmentCount() - 1)
                endPt = polyLine.segmEndPt(polyLine.segmentCount() - 1)
                preVec = Geom.Vec(startPt, endPt)
                preVec.normalize()
                preNor = Geom.Vec(-preVec.y(), preVec.x(), 0.0)
            elif preSegmType == PolylineData.SegmType_Arc:
                preArc = polyLine.segmArc(polyLine.segmentCount() - 1)
                preVec = preArc.endTangent()
                preVec.normalize()
                preNor = Geom.Vec(-preVec.y(), preVec.x(), 0.0)
            startVector = (preNor + curNor) / (preNor + curNor).magnitude()
        else:
            if segmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(segmId)
                endPt = polyLine.segmEndPt(segmId)
                curVec = Geom.Vec(startPt, endPt)
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            elif segmType == PolylineData.SegmType_Arc:
                arc = polyLine.segmArc(segmId)
                curVec = arc.startTangent()
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            preSegmType = polyLine.segmentType(segmId-1)
            if preSegmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(segmId-1)
                endPt = polyLine.segmEndPt(segmId-1)
                preVec = Geom.Vec(startPt, endPt)
                preVec.normalize()
                preNor = Geom.Vec(-preVec.y(), preVec.x(), 0.0)
            elif preSegmType == PolylineData.SegmType_Arc:
                preArc = polyLine.segmArc(segmId-1)
                preVec = preArc.endTangent()
                preVec.normalize()
                preNor = Geom.Vec(-preVec.y(), preVec.x(), 0.0)
            # ang1 = Geom.Vec.angle(prevVec, curVec)
            # ang2 = Geom.Vec.angle(curVec, prevVec)
            # bis = (curVec - preVec).normalized()
            if ((curVec - preVec).magnitude()) < 0.000001:
                bis = (Geom.Vec(-curVec.y(), curVec.x(), 0.0)).normalized()
                norm = (bis.crossed(curVec)).normalized()
            else:
                bis = (curVec - preVec).normalized()
                norm = ((-preVec).crossed(curVec)).normalized()

            norVec = (bis.crossed(norm)).normalized()
            startVector += [bis]
            startVector += [norVec]

        return startVector

    def _getEndVector(self, polyLine, segmId):
        #isFirst = bool(segmId == 0)
        isLast = bool(segmId == (polyLine.segmentCount() - 1))
        isClosed = polyLine._closed
        endVector = []

        segmType = polyLine.segmentType(segmId)
        if isLast and (not isClosed):
            if segmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(segmId)
                endPt = polyLine.segmEndPt(segmId)
                vec = Geom.Vec(startPt, endPt)
                vec.normalize()
                endVector += [Geom.Vec(-vec.y(), vec.x(), 0.0)]
                endVector += [Geom.Vec(vec.x(), vec.y(), 0.0)]
            elif segmType == PolylineData.SegmType_Arc:
                arc = polyLine.segmArc(segmId)
                vec = arc.endTangent()
                vec.normalize()
                endVector += [Geom.Vec(-vec.y(), vec.x(), 0.0)]
                endVector += [Geom.Vec(vec.x(), vec.y(), 0.0)]
        elif isLast and isClosed:
            if segmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(polyLine.segmentCount() - 1)
                endPt = polyLine.segmEndPt(polyLine.segmentCount() - 1)
                curVec = Geom.Vec(startPt, endPt)
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            elif segmType == PolylineData.SegmType_Arc:
                arc = polyLine.segmArc(polyLine.segmentCount() - 1)
                curVec = arc.endTangent()
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            nexSegmType = polyLine.segmentType(0)
            if nexSegmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(0)
                endPt = polyLine.segmEndPt(0)
                nexVec = Geom.Vec(startPt, endPt)
                nexVec.normalize()
                nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0)
            elif nexSegmType == PolylineData.SegmType_Arc:
                nexArc = polyLine.segmArc(0)
                nexVec = nexArc.startTangent()
                nexVec.normalize()
                nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0)

            endVector = (nexNor + curNor) / (nexNor + curNor).magnitude()
        else:
            if segmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(segmId)
                endPt = polyLine.segmEndPt(segmId)
                curVec = Geom.Vec(startPt, endPt)
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            elif segmType == PolylineData.SegmType_Arc:
                arc = polyLine.segmArc(segmId)
                curVec = arc.endTangent()
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)

            nexSegmType = polyLine.segmentType(segmId+1)
            if nexSegmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(segmId+1)
                endPt = polyLine.segmEndPt(segmId+1)
                nexVec = Geom.Vec(startPt, endPt)
                nexVec.normalize()
                nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0)
            elif nexSegmType == PolylineData.SegmType_Arc:
                nexArc = polyLine.segmArc(segmId+1)
                nexVec = nexArc.startTangent()
                nexVec.normalize()
                nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0)

            if ((nexVec - curVec).magnitude()) < 0.000001:
                bis = (Geom.Vec(-curVec.y(), curVec.x(), 0.0)).normalized()
                norm = ((bis).crossed(nexVec)).normalized()
            else:
                bis = (nexVec - curVec).normalized()
                norm = ((-curVec).crossed(nexVec)).normalized()
            norVec = (norm.crossed(bis)).normalized()
            # endVector = (nextNor + curNor) / (nextNor + curNor).magnitude()
            endVector += [bis]
            endVector += [norVec]

        return endVector

    def _placeSegment(self, model, polyLine, segmId):
        # TODO: Add support for closed polylines
        #

        isFirst = bool(segmId == 0)
        isLast = bool(segmId == (polyLine.segmentCount() - 1))
        isClosed = polyLine._closed
        # print("place {} Segment - enter \n".format(segmId))

        segmType = polyLine.segmentType(segmId)
        if segmType == PolylineData.SegmType_Line:
            startPt = polyLine.segmStartPt(segmId)
            endPt = polyLine.segmEndPt(segmId)
            startVecs = self._getStartVector(polyLine, segmId)
            endVecs = self._getEndVector(polyLine, segmId)
            # print("marker {}th segment".format(segmId))
            self._placeLineSegment(model, startPt, endPt, startVecs, endVecs, isFirst, isLast, isClosed)
        elif segmType == PolylineData.SegmType_Arc:
            arc = polyLine.segmArc(segmId)
            startVec = self._getStartVector(polyLine, segmId)
            endVec = self._getEndVector(polyLine, segmId)
            # print("marker {}th segment".format(segmId))
            self._placeArcSegment(arc, startVec, endVec, isFirst, isLast, isClosed)
        # print("place {} Segment - exit \n".format(segmId))

    def _placeSegmentsAccLine(self, model, polyLine):
        segmCount = polyLine.segmentCount()
        if segmCount <= 0:
            return

        # print("segmCount = ", segmCount)
        for segmId in range(segmCount):
            self._placeSegment(model, polyLine, segmId)

    def printPolyline(self, name, ptList):
        print("{}:".format(name))

        for pt in ptList:
            print("    ({}, {}, {})".format(pt.x(), pt.y(), pt.z()))

    def fixPolyline(self, pntList):
        self._pntList = pntList
        self.printPolyline("pntList", pntList)
        self.printPolyline("self._pntList", self._pntList)

    def createCompound(self):
        # polyLine = PolylineData.fromElement(self._baseData)
        axisCurve = self.getAxisRepresentation()
        polyLine = PolylineData.fromElement(self.getPolylineData(axisCurve))
        # print("createCompound")
        # ui.showStatusBarMessage(lxstr("[C] Creating of balustrade"))

        model = "Hi!"
        # model = ModelAssembler(doc)
        # model.beginModel(self)

        bmpl_ap = BeamPool(self.getDocument())
        self._poolContainer['apertures'] = bmpl_ap
        bmpl_sup = BeamPool(self.getDocument())
        self._poolContainer['supports'] = bmpl_sup
        bmpl_bot = BeamPool(self.getDocument())
        self._poolContainer['botbeams'] = bmpl_bot
        bmpl_top = BeamPool(self.getDocument())
        self._poolContainer['topbeams'] = bmpl_top
        bmpl_hand = BeamPool(self.getDocument())
        self._poolContainer['handrailbeams'] = bmpl_hand
        bmpl_found = BeamPool(self.getDocument())
        self._poolContainer['foundbeams'] = bmpl_found

        # self._placeSupportsAccLine(model, polyLine)
        self._placeSegmentsAccLine(model, polyLine)

        self.setLineLength(polyLine)

        self.colorSubElements()

        # ui.showStatusBarMessage(lxstr(""))

    @staticmethod
    def maxInList(lst):
        assert lst
        m = lst[0]
        for i in lst:
            if i > m:
                m = i
        return m

    @timer
    def _updateGeometry(self):
        # print("_updateGeometry")
        doc = self.getDocument()
        with EditMode(doc):
            self.removeSubElements()
            self.createCompound()
    
    def setHeight(self, height):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(height, self.minHeight(), self.maxHeight()))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if height < self.minHeight():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif height > self.maxHeight():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def height(self):
        return self._height.getValue()

    def minHeight(self):
        return self._bottomDistance.getValue() + self._handrailHeight.getValue() + 3.*self._intermediateThickness.getValue()

    def maxHeight(self):
        return 10000.0
    
    def setHandrailWidth(self, handrailWidth):
        with EditMode(self.getDocument()):
            self._handrailWidth.setValue(clamp(handrailWidth, self.minHandrailWidth(), self.maxHandrailWidth()))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if handrailWidth < self.minHandrailWidth():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif handrailWidth > self.maxHandrailWidth():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def handrailWidth(self):
        return self._breite.getValue()

    def minHandrailWidth(self):
        return 0.001

    def maxHandrailWidth(self):
        return 10000.0

    def setHandrailHeight(self, handrailHeight):
        with EditMode(self.getDocument()):
            self._handrailHeight.setValue(clamp(handrailHeight, self.minHandrailHeight(), self.maxHandrailHeight()))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if handrailHeight < self.minHandrailHeight():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif handrailHeight > self.maxHandrailHeight():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setHandrailLedge(self, handrailLedge):
        if handrailLedge >= 0.0: 
            with EditMode(self.getDocument()):
                self._handrailLedge.setValue(handrailLedge)
                self.showSolidModelRepresentation()
                self._representation.setValue(1)
                self._updateGeometry()
        else:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def handrailHeight(self):
        return self._handrailHeight.getValue()

    def minHandrailHeight(self):
        return 0.001

    def maxHandrailHeight(self):
        return 10000.0

    def setSupportWidth(self, supportWidth):
        with EditMode(self.getDocument()):
            self._supportWidth.setValue(clamp(supportWidth, 0.001, 1e4))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if supportWidth < 0.001:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif supportWidth > 1e4:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setSupportThickness(self, supportThickness):
        with EditMode(self.getDocument()):
            self._supportThickness.setValue(clamp(supportThickness, 0.001, 1e4))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if supportThickness < 0.001:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif supportThickness > 1e4:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setSparType(self, handrailType):
        with EditMode(self.getDocument()):
            self._sparType.setValue(handrailType)
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()

    def _updateValues(self, railingType):
        # print(railingType, PROFILES.keys(), list(PROFILES.keys())[railingType])  #list(PROFILES.keys())[railingType]
        # print(railingType, PROFILES.get(list(PROFILES.keys())[railingType]))
        profile = PROFILES.get(list(PROFILES.keys())[railingType])
        self._height.setValue(profile['height']-profile['foundation']['size'][1])
        self._handrailWidth.setValue(profile['handrail']['size'][0])
        self._handrailHeight.setValue(profile['handrail']['size'][1])
        self._handrailLedge.setValue(profile['handrail']['ledge'])
        self._supportWidth.setValue(profile['support']['size'][0])
        self._supportThickness.setValue(profile['support']['size'][1])
        if profile['spar']:
            print(self._isSpar.getValue())
            self._isSpar.setValue(True)
            self._handrailSparGap.setValue(profile['spar']['handrail distance'])
            self._sparWidth.setValue(profile['spar']['size'][0])
            self._sparHeight.setValue(profile['spar']['size'][1])
        else:
            self._isSpar.setValue(False)
        self._intermediateWidth.setValue(profile['pole']['size'][0])
        self._intermediateThickness.setValue(profile['pole']['size'][1])
        self._chordWidth.setValue(profile['bottom chord']['size'][0])
        self._chordHeight.setValue(profile['bottom chord']['size'][1])
        self._bottomDistance.setValue(profile['bottom chord']['bottom distance'])
        self._footPlateWidth.setValue(profile['footplate']['size'][0])
        self._footPlateThickness.setValue(profile['footplate']['size'][1])
        self._isFoundation.setValue(True)
        self._foundationWidth.setValue(profile['foundation']['size'][0])
        self._foundationHeight.setValue(profile['foundation']['size'][1])
        self._foundationLedge.setValue(profile['foundation']['ledge'])

    def setRailingType(self, railingType):
        with EditMode(self.getDocument()):
            self._railingType.setValue(railingType)
            self._updateValues(railingType)
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()

    def setColumnDistance(self, columnDistance):
        print("setFoundationState", columnDistance)
        with EditMode(self.getDocument()):
            self._columnDistance.setValue(clamp(columnDistance, self.minColumnDistance(), self.maxColumnDistance()))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if columnDistance < self.minColumnDistance():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif columnDistance > self.maxColumnDistance():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def columnDistance(self):
        return self._columnDistance.getValue()

    def minColumnDistance(self):
        return 12.*self._intermediateThickness.getValue()

    def maxColumnDistance(self):
        return 10000.0

    def setSparState(self, SparState):
        #print("setFoundationState", foundationState)
        if SparState:
            self._handrailSparGap.setEditable(True)
        else:
            self._handrailSparGap.setEditable(False)
        with EditMode(self.getDocument()):
            self._isSpar.setValue(SparState)
            self._updateGeometry()

    def setHandrailSparGap(self, handrailSparGap):
        with EditMode(self.getDocument()):
            self._handrailSparGap.setValue(clamp(handrailSparGap, self.minBottomDistance(), self.maxBottomDistance()))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if handrailSparGap < 0.1:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif handrailSparGap > 0.7*self._height.getValue():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setSparWidth(self, sparWidth):
        with EditMode(self.getDocument()):
            self._sparWidth.setValue(clamp(sparWidth, 0.001, 1e4))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if sparWidth < 0.001:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif sparWidth > 1e4:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setSparHeight(self, sparHeight):
        with EditMode(self.getDocument()):
            self._sparHeight.setValue(clamp(sparHeight, 0.001, 1e4))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if sparHeight < 0.001:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif sparHeight > 1e4:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setChordWidth(self, chordWidth):
        with EditMode(self.getDocument()):
            self._chordWidth.setValue(clamp(chordWidth, 0.001, 1e4))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if chordWidth < 0.001:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif chordWidth > 1e4:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setChordHeight(self, chordHeight):
        with EditMode(self.getDocument()):
            self._sparHeight.setValue(clamp(chordHeight, 0.001, 1e4))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if chordHeight < 0.001:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif chordHeight > 1e4:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setBottomDistance(self, bottomDistance):
        with EditMode(self.getDocument()):
            self._bottomDistance.setValue(clamp(bottomDistance, self.minBottomDistance(), self.maxBottomDistance()))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if bottomDistance < self.minBottomDistance():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif bottomDistance > self.maxBottomDistance():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def bottomDistance(self):
        return self._bottomDistance.getValue()

    def minBottomDistance(self):
        return 0.001

    def maxBottomDistance(self):
        return self._height.getValue() - self._handrailHeight.getValue() - 3.*self._intermediateThickness.getValue()

    def setIntermediateWidth(self, intermediateWidth):
        with EditMode(self.getDocument()):
            self._intermediateWidth.setValue(
                clamp(intermediateWidth, self.minIntermediateThickness(), self.maxIntermediateThickness()))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if intermediateWidth < self.minIntermediateThickness():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif intermediateWidth > self.maxIntermediateThickness():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setIntermediateThickness(self, intermediateThickness):
        with EditMode(self.getDocument()):
            self._intermediateThickness.setValue(
                clamp(intermediateThickness, self.minIntermediateThickness(), self.maxIntermediateThickness()))
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
        if intermediateThickness < self.minIntermediateThickness():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif intermediateThickness > self.maxIntermediateThickness():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def intermediateThickness(self):
        return self._intermediateThickness.getValue()

    def minIntermediateThickness(self):
        return 0.001

    def maxIntermediateThickness(self):
        return 10000.0

    def setIntermediateDirection(self, intermediateDirection):
        with EditMode(self.getDocument()):
            self._intermediateDirection.setValue(intermediateDirection)
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()

    def setIntermediateType(self, intermediateType):
        with EditMode(self.getDocument()):
            self._intermediateType.setValue(intermediateType)
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()
    
    def setFootPlateWidth(self, footPlateWidth):
        if footPlateWidth >= 0.0: 
            with EditMode(self.getDocument()):
                self._footPlateWidth.setValue(footPlateWidth)
                self.showSolidModelRepresentation()
                self._representation.setValue(1)
                self._updateGeometry()

    def setFootPlateThickness(self, footPlateThickness):
        if (footPlateThickness >= 0.0): 
            with EditMode(self.getDocument()):
                self._footPlateThickness.setValue(footPlateThickness)
                self.showSolidModelRepresentation()
                self._representation.setValue(1)
                self._updateGeometry()

    def setFoundationState(self, foundationState):
        #print("setFoundationState", foundationState)
        if foundationState:
            self._foundationLedge.setEditable(True)
        else:
            self._foundationLedge.setEditable(False)
        with EditMode(self.getDocument()):
            self._isFoundation.setValue(foundationState)
            self._updateGeometry()

    def setFoundationWidth(self, foundationWidth):
        if self._isFoundation.getValue() and (foundationWidth >= 0.0): 
            with EditMode(self.getDocument()):
                self._foundationWidth.setValue(foundationWidth)
                self.showSolidModelRepresentation()
                self._representation.setValue(1)
                self._updateGeometry()

    def setFoundationHeight(self, foundationHeight):
        if self._isFoundation.getValue() and (foundationHeight >= 0.0): 
            with EditMode(self.getDocument()):
                self._foundationHeight.setValue(foundationHeight)
                self.showSolidModelRepresentation()
                self._representation.setValue(1)
                self._updateGeometry()

    def setFoundationLedge(self, foundationLedge):
        if self._isFoundation.getValue() and (foundationLedge >= 0.0): 
            with EditMode(self.getDocument()):
                self._foundationLedge.setValue(foundationLedge)
                self.showSolidModelRepresentation()
                self._representation.setValue(1)
                self._updateGeometry()
        else:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def getSubElementByGlobalId(self, globalId):
        sub_elems = self.getSubElements()
        for i in range(len(sub_elems)):
            if sub_elems[i].getGlobalId() == globalId:
                return sub_elems[i]

    def _switchRepresentations(self, index):
        with EditMode(self.getDocument()):
            if index == 0:                                  # Index 0
                self.showAxisRepresentation()
            else:
                self.showSolidModelRepresentation()

                """
                Recreate the "MultiGeo" based on the Axis
                """
                self._updateGeometry()
    
    def calculateLength(self, polyLine):
        # polyLine = PolylineData.fromElement(self._baseData)
        segmCount = polyLine.segmentCount()
        if segmCount <= 0:
            return 0

        lineLength = 0.0
        # print("segmCount = ", segmCount)
        for segmId in range(segmCount):
            segmType = polyLine.segmentType(segmId)
            if segmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(segmId)
                endPt = polyLine.segmEndPt(segmId)
                segmDistance = Geom.Vec(endPt, startPt).magnitude()
                lineLength += segmDistance
                # print(f"current = {segmDistance}, total = {lineLength}")
                
            elif segmType == PolylineData.SegmType_Arc:
                arc = polyLine.segmArc(segmId)
                arcLen = arc.length()
                paramRatio = arc.paramRatio()
                supportRadius = self._intermediateThickness.getValue()
                # supportSize = supportRadius * 2.0
                startParam = 0.0
                endParam = 1.0

                buildParamLen = endParam - startParam
                buildLen = buildParamLen * arcLen
                # print startParam, endParam
                stepNum, colHorDist = self._calcColDist(buildLen)
                paramDist = buildParamLen / float(stepNum)

                listPnt = []
                
                stepParam = startParam
                
                lastStepId = stepNum - 1
                hrStartPt = arc.paramPt(0.0)
                hrStartPt = Geom.Pnt(hrStartPt.x(), hrStartPt.y(), hrStartPt.z())
                listPnt.append(hrStartPt)
                stepStartPt = hrStartPt
                for step in range(lastStepId):
                    stepParam += paramDist
                    # listParam.append(stepParam)
                    hrEndPt = arc.paramPt(stepParam)
                    hrEndPt = Geom.Pnt(hrEndPt.x(), hrEndPt.y(), hrEndPt.z())
                    listPnt.append(hrEndPt)
                    stepEndPt = hrEndPt
                    segmDistance = Geom.Vec(stepEndPt, stepStartPt).magnitude()
                    lineLength += segmDistance
                    stepStartPt = stepEndPt

                stepParam += paramDist
                # listParam.append(stepParam)

                hrEndPt = arc.paramPt(1.0)
                hrEndPt = Geom.Pnt(hrEndPt.x(), hrEndPt.y(), hrEndPt.z())
                listPnt.append(hrEndPt)
                stepEndPt = hrEndPt
                segmDistance = Geom.Vec(stepEndPt, stepStartPt).magnitude()
                lineLength += segmDistance
                # print(f"current = {segmDistance}, total = {lineLength}")
        return lineLength               

    def printPolylineTest(self, strn):
        print(":{}".format(strn))

        # for pt in ptList:
        #     print "    ({}, {}, {})".format(pt.x(), pt.y(), pt.z())

    def setLineLength(self, polyline):
        try:
            length = self.calculateLength(polyline)
            with EditMode(self.getDocument()):
                self._lineLength.setValue(length)
            # print(f"Line length = {length}")
        except Exception as err:
            print(f"{err.__class__.__name__}: {err}")
    
    def setColor(self, color):
        self._subElemColor = color 

    def colorSubElements(self):
        sub_elems = self.getSubElements()
        for i in range(len(sub_elems)):
            sub_elems[i].setDiffuseColor(Base.Color_fromCdwkColor(self._cwColor))

    @staticmethod
    def writeToString(lineData):
        strn = ""
        strn += "{};".format(len(lineData))
        for i in range(len(lineData)):
            if lineData[i][0] == PolylineData.SegmType_Line:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};".format(lineData[i][0],\
                                                             lineData[i][1].x(), lineData[i][1].y(), lineData[i][1].z(),\
                                                             lineData[i][2].x(), lineData[i][2].y(), lineData[i][2].z())
            elif lineData[i][0] == PolylineData.SegmType_Arc:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};{7:.5f};{8:.5f};{9:.5f};".format(lineData[i][0],\
                                                             lineData[i][1].x(), lineData[i][1].y(), lineData[i][1].z(),\
                                                             lineData[i][2].x(), lineData[i][2].y(), lineData[i][2].z(),\
                                                             lineData[i][3].x(), lineData[i][3].y(), lineData[i][3].z())
            # if i != len(lineData)-1:
            #     strn += ";"
        i_n = len(lineData[len(lineData)-1])-1
        strn += "{}".format(lineData[len(lineData)-1][i_n])
        return strn

    @staticmethod
    def readFromString(strn):
        lineData = []
        st = strn.split(";")
        #lenList = int(st[0])
        index = 0
        for i in range(int(st[0])):
            if int(st[index+1]) == PolylineData.SegmType_Line:
                lineData.append([int(st[index+1]), Geom.Pnt(float(st[index+2]), float(st[index+3]), float(st[index+4])),\
                                Geom.Pnt(float(st[index+5]), float(st[index+6]), float(st[index+7]))])
                index += 7
            elif int(st[index+1]) == PolylineData.SegmType_Arc:
                lineData.append([int(st[index + 1]), Geom.Pnt(float(st[index + 2]), float(st[index + 3]), float(st[index + 4])), \
                                Geom.Pnt(float(st[index + 5]), float(st[index + 6]), float(st[index + 7])), \
                                Geom.Pnt(float(st[index + 8]), float(st[index + 9]), float(st[index + 10]))])
                index += 10

        i_n = len(lineData[int(st[0])-1])
        if st[len(st)-1] == "True":
            bl = True
        else:
            bl = False
        lineData[int(st[0])-1].append(bl)
        #print "i_n={} , st[last]={}".format(i_n, lineData[int(st[0])-1][i_n])

        return lineData

    def polyline(self):
        return self._polyline.getValue()

    def onPropertyChanged(self, aPropertyName):
        #print("onPropertyChanged", aPropertyName)
        # self._railingType
        # if aPropertyName == self._railingType.getName():
        #     self.setRailingType(self._railingType.getValue())
        if aPropertyName == self._height.getName():
            self.setHeight(self._height.getValue())
        elif aPropertyName == self._handrailWidth.getName():
            self.setHandrailWidth(self._handrailWidth.getValue())
        elif aPropertyName == self._handrailHeight.getName():
            self.setHandrailHeight(self._handrailHeight.getValue())
        elif aPropertyName == self._handrailLedge.getName():
            self.setHandrailLedge(self._handrailLedge.getValue())
        elif aPropertyName == self._sparType.getName():
            self.setSparType(self._sparType.getValue())
        elif aPropertyName == self._supportWidth.getName():
            self.setSupportWidth(self._supportWidth.getValue())
        elif aPropertyName == self._supportThickness.getName():
            self.setSupportThickness(self._supportThickness.getValue())
        elif aPropertyName == self._columnDistance.getName():
            self.setColumnDistance(self._columnDistance.getValue())

        elif aPropertyName == self._isSpar.getName():
            self.setSparState(self._isSpar.getValue())
        elif aPropertyName == self._handrailSparGap.getName():
            self.setHandrailSparGap(self._handrailSparGap.getValue())
        elif aPropertyName == self._sparWidth.getName():
            self.setSparWidth(self._sparWidth.getValue())
        elif aPropertyName == self._sparHeight.getName():
            self.setSparHeight(self._sparHeight.getValue())
        elif aPropertyName == self._chordWidth.getName():
            self.setChordWidth(self._chordWidth.getValue())
        elif aPropertyName == self._chordHeight.getName():
            self.setChordHeight(self._chordHeight.getValue())

        elif aPropertyName == self._bottomDistance.getName():
            self.setBottomDistance(self._bottomDistance.getValue())
        elif aPropertyName == self._intermediateWidth.getName():
            self.setIntermediateWidth(self._intermediateWidth.getValue())
        elif aPropertyName == self._intermediateThickness.getName():
            self.setIntermediateThickness(self._intermediateThickness.getValue())
        elif aPropertyName == self._intermediateType.getName():
            self.setIntermediateType(self._intermediateType.getValue())
        # elif aPropertyName == self._intermediateDirection.getName():
        #     self.setIntermediateDirection(self._intermediateDirection.getValue())
        elif aPropertyName == self._footPlateWidth.getName():
            self.setFootPlateWidth(self._footPlateWidth.getValue())
        elif aPropertyName == self._footPlateThickness.getName():
            self.setFootPlateThickness(self._footPlateThickness.getValue())
        elif aPropertyName == self._isFoundation.getName():
            self.setFoundationState(self._isFoundation.getValue())
        elif aPropertyName == self._foundationWidth.getName():
            self.setFoundationWidth(self._foundationWidth.getValue())
        elif aPropertyName == self._foundationHeight.getName():
            self.setFoundationHeight(self._foundationHeight.getValue())
        elif aPropertyName == self._foundationLedge.getName():
            self.setFoundationLedge(self._foundationLedge.getValue())
        elif aPropertyName == self._railingType.getName():
            self.setRailingType(self._railingType.getValue())
        elif aPropertyName == self._representation.getName():
            self._switchRepresentations(self._representation.getValue())
            # self._onRecalculateButtonClicked()
        # elif aPropertyName == BalustradeSegments._recalculateLenBtnName:
        #     self._onRedefineLineButtonClicked()

    def getPolylineData(self, lineSet):
        lineData = []
        #edges = Topo.ShapeTool.getEdges(lineSet.getShape())
        wire = Topo.ShapeTool.isSingleWire(lineSet.computeShape(False))
        # if Topo.WireTool.isClosed(wire):
        #     edges = Topo.WireTool.getEdges(Topo.WireTool.reversed(wire))
        # else:
        #     edges = Topo.WireTool.getEdges(wire)
        edges = Topo.WireTool.getEdges(wire)

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
                
                # p_0_d2 = Topo.EdgeTool.d2(edge, arcParamsRes.startParam)
                # print('Params: ', arcParamsRes.startParam, middleParam, arcParamsRes.endParam)
                # printVec('p_0_d2: v1', p_0_d2.v1)
                # printVec('p_0_d2: v2', p_0_d2.v2)
                # p_m_d2 = Topo.EdgeTool.d2(edge, middleParam)
                # printVec('p_m_d2: v1', p_m_d2.v1)
                # printVec('p_m_d2: v2', p_m_d2.v2)
                # p_1_d2 = Topo.EdgeTool.d2(edge, arcParamsRes.endParam)
                # printVec('p_1_d2: v1', p_1_d2.v1)
                # printVec('p_1_d2: v2', p_1_d2.v2)

            else:
                raise RuntimeError("Unsupported edge type")
        lineData[len(edges)-1].append(Topo.WireTool.isClosed(wire))
        #print(lineData[len(edges)-1])
        return lineData
    
    def setAxisCurve(self, axisCurve):
        with EditMode(self.getDocument()):
            """
            Here we set the Axis
            """
            ok = self.setAxisRepresentation(axisCurve)

            """
            Recreate the "MultiGeo" based on the Axis
            """
            self._updateGeometry()
            return ok


def main():
    # Register this Python Script
    doc = lx.Application.getInstance().getActiveDocument()

    if doc:
        doc.registerPythonScript(GUID_SCRPT)
        cwColor = CW_COLOR
        element = RailingSegments(doc)
        lx.setNewComponentByColorAndName(cwColor, Base.StringTool.toString("Balustrade"), element)

        geometry = None

        """
        If the script is dropped on an Element take the Geometry and delete Element
        """
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            droppedOnElement = thisScript.getDroppedOnElement()
            if droppedOnElement:
                geometry = droppedOnElement.getGeometry()
                trfs = droppedOnElement.getTransform()
                element.setTransform(trfs)
                if element.setAxisCurve(geometry):
                    pass
                    doc.removeObject(droppedOnElement)

        """
        Ask the user to pick a Line, take the Geometry and delete Element
        """
        if geometry is None:
            ui.showStatusBarMessage(5944)
            uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
            uidoc.highlightByShapeType(Topo.ShapeType_WIRE)
            ok = uidoc.pickPoint()
            uidoc.stopHighlightByShapeType()
            ui.showStatusBarMessage(lxstr(""))
            if ok:
                pickedElement = uidoc.getPickedElement()
                if pickedElement:
                    geometry = pickedElement.getGeometry()
                    trfs = pickedElement.getTransform()
                    element.setTransform(trfs)
                    if element.setAxisCurve(geometry):
                        pass
                        # doc.removeObject(pickedElement)

    
if __name__ == "__main__":
    main()
