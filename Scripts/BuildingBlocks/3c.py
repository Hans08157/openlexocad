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

GUID_CLASS = Base.GlobalId("{eae8322d-96b3-41cc-8c49-70569f595da1}")
GUID_SCRPT = Base.GlobalId("{b34513ac-ad8c-48ac-b3e4-c18a2d8079a2}")
CW_COLOR = 260

epsilon = 0.0001
eps_DS = 0.001
pi2 = math.pi * 0.5


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
        equality = True

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

        return equality


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
            self._addToPoool(new_dataStr, geom)
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

    def _addToPoool(self, new_dataStr, geom):
        self._dict_list.append({'data': new_dataStr, 'geom': geom})


class BeamFactory:
    # Beam types
    BT_Square = 0
    BT_Circle = 1

    # Beam type names
    _squareBTypeName = "square"
    _circleBTypeName = "circle"

    @staticmethod
    def correctBeamType(beamType):
        return bool(beamType == BeamFactory.BT_Square or beamType == BeamFactory.BT_Circle)

    @staticmethod
    def writeBeamType(bt):
        if bt == BeamFactory.BT_Square:
            return BeamFactory._squareBTypeName
        elif bt == BeamFactory.BT_Circle:
            return BeamFactory._circleBTypeName
        else:
            raise RuntimeError("Invalid beam type")

    @staticmethod
    def parseBeamType(bt):
        if bt == BeamFactory._squareBTypeName:
            return BeamFactory.BT_Square
        elif bt == BeamFactory._circleBTypeName:
            return BeamFactory.BT_Circle
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

    def _createBaseBeam(self, beamType, length, radiusH, radiusV):
        if not BeamFactory.correctBeamType(beamType):
            raise RuntimeError("Invalid beam type")

        if beamType == BeamFactory.BT_Square:
            return self._createBaseBeam_Square(length, radiusH, radiusV)
        else:
            if abs(radiusH - radiusV) > epsilon:
                raise RuntimeError("Radii must be equal")

            return self._createBaseBeam_Circle(length, radiusH)

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
        if len(beam_vec) > 1:
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
        beamLen = [2. * radiusV, length, 2. * radiusV]

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


class BalustradeSegments(lx.Railing):
    _cwColor = CW_COLOR
    _heightParamName =                "_height"
    _handrailWidthParamName =         "_handrail_width"
    _handrailHeightParamName =        "_handrail_height"
    _handrailTypeParamName =          "_handrail_type"
    _columnDistanceParamName =        "_column_distance"
    _bottomDistanceParamName =        "_bottom_distance"
    _intermediateThicknessParamName = "_intermediate_thickness"
    _intermediateTypeParamName =      "_intermediate_type"
    _intermediateDirectionParamName = "_intermediate_direction"
    
    _lineLengthName = "_length"
    # _recalculateLenBtnName = "Redefine length"

    def getGlobalClassId(self):
        return GUID_CLASS

    def __init__(self, aArg):
        lx.Railing.__init__(self, aArg)
        self.registerPythonClass("BalustradeSegments", "OpenLxApp.Railing")
        # Register properties
        self.setPropertyHeader(lxstr("Balustrade"), 480)  # 480
        self.setPropertyGroupName(lxstr("Balustrade parameters"), 481)  # 481

        self._height = self.registerPropertyDouble(self._heightParamName, 1.0, lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE, 482)  # 482
        self._handrailWidth = self.registerPropertyDouble(self._handrailWidthParamName, 0.1, lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, 486)  # 486
        self._handrailHeight = self.registerPropertyDouble(self._handrailHeightParamName, 0.05, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 487)  # 487

        self._handrailType = self.registerPropertyEnum(self._handrailTypeParamName, 0, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 488)  # 488
        self._handrailType.setEmpty()
        self._handrailType.addEntry(lxstr("Square"), 489)  # 489
        self._handrailType.addEntry(lxstr("Circle"), 490)  # 490

        self._columnDistance = self.registerPropertyDouble(self._columnDistanceParamName, 1.0, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 491)  # 491
        self._bottomDistance = self.registerPropertyDouble(self._bottomDistanceParamName, 0.3, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 492)  # 492
        self._intermediateThickness = self.registerPropertyDouble(self._intermediateThicknessParamName, 0.02,
                                                                  lx.Property.VISIBLE, lx.Property.EDITABLE, 493)  # 493
        self._intermediateType = self.registerPropertyEnum(self._intermediateTypeParamName, 0, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 494)  # 494
        self._intermediateType.setEmpty()
        self._intermediateType.addEntry(lxstr("Square"), 495)  # 495
        self._intermediateType.addEntry(lxstr("Circle"), 496)  # 496

        self._intermediateDirection = self.registerPropertyEnum(self._intermediateDirectionParamName, 0, lx.Property.VISIBLE, 
                                                                lx.Property.EDITABLE, 497)  # 497
        self._intermediateDirection.setEmpty()
        self._intermediateDirection.addEntry(lxstr("Vertical"), 498)  # 498
        self._intermediateDirection.addEntry(lxstr("Horizontal"), 499)  # 499
        # self._recalcBtn = self.registerPropertyButton(self._recalculateBtnPropName, lx.Property.VISIBLE, 
        #                                               lx.Property.EDITABLE, -1)  # 500
        self._representation = self.registerPropertyEnum("_representation", 1, lx.Property.VISIBLE, lx.Property.EDITABLE, 500)   
        self._representation.setEmpty()
        self._representation.addEntry(lxstr("Axis"), 507)        # Index 0 507
        self._representation.addEntry(lxstr("SolidModel"), 508)  # Index 1 508

        self._lineLength = self.registerPropertyDouble(self._lineLengthName, 0.0, lx.Property.VISIBLE, 
                                                       lx.Property.NOT_EDITABLE, 501)  # 501
        # self._recalculateLenBtn = self.registerPropertyButton(self._recalculateLenBtnName, lx.Property.VISIBLE, 
        #                                                      lx.Property.EDITABLE, -1)
        self._setAllSteps()
        self._poolContainer = {}
        
        self.setBoundingBoxEnabled(False)
        

    def _setAllSteps(self):
        self._height.setSteps(0.1)
        self._handrailWidth.setSteps(0.01)
        self._handrailHeight.setSteps(0.01)
        self._columnDistance.setSteps(0.01)
        self._bottomDistance.setSteps(0.1)
        self._intermediateThickness.setSteps(0.01)

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

    def _placeSupportsAccLine(self, model, polyLine):
        # partHeight = self._height.getValue() - self._handrailHeight.getValue()
        supportRadius = self._intermediateThickness.getValue()
        # print("placeSupportsAccLine - enter")
        hType = 0

        segmCount = polyLine.segmentCount()
        for segm in range(1, segmCount):
            suppPos = polyLine.segmStartPt(segm)
            suppDirections = self._supportPositionVectors(polyLine, segm)
            # start making transform: Matrix and translationPart
            e_x = Geom.Vec(suppDirections[0])
            e_y = Geom.Vec(suppDirections[1])
            e_z = Geom.Vec(suppDirections[2])

            e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
            e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
            e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(suppPos.x(), suppPos.y(), suppPos.z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            lenSupp = self._height.getValue() - self._handrailHeight.getValue()
            strVec = Geom.Vec(0.0, 0.0, -1.0)
            endVec = Geom.Vec(0.0, 0.0, 1.0)
            suppEndPt = Geom.Pnt(suppPos.x(), suppPos.y(), suppPos.z()+lenSupp)
            dtStr = DataStruct(hType, suppPos, suppEndPt, supportRadius, supportRadius, strVec, endVec, Tr)
            beam_sup = self._poolContainer['supports'].createBeam(dtStr)
            self.addSubElement(beam_sup)

    def _calcColDist(self, divSpace):
        lengthBal = self._columnDistance.getValue()
        nSegInLine = int(divSpace // lengthBal)

        if divSpace % lengthBal > 0.5:
            nSegInLine += 1

        if nSegInLine <= 0:
            nSegInLine = 1

        colDistance = divSpace / float(nSegInLine)
        return nSegInLine, colDistance

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

    def _fillAperture_Vertical(self, model, apertureStartPt, apertureVec):
        dirVec = apertureVec.normalized()
        typeInt = self._intermediateType.getValue()
        bottomDist = self._bottomDistance.getValue()
        interThick = self._intermediateThickness.getValue()

        intermAngle = vecHAngle(apertureVec.x(), apertureVec.y())
        intermDist = (self._columnDistance.getValue() - (interThick * 2.0)) / 11.0
        intermRadius = interThick * 0.5
        intermNum = int(apertureVec.magnitude() // intermDist)
        colDist = (apertureVec.magnitude() - (intermNum-1)*interThick) / float(intermNum)
        intermDist = interThick + colDist  #apertureVec.magnitude() / float(intermNum)  # Compensate slope
        intFrStep = dirVec.scaled(colDist + 0.5*interThick)
        intermStep = dirVec.scaled(intermDist)

        intStartPt = Geom.Pnt(apertureStartPt)
        intStartPt.translate(intFrStep)
        partHeight = self._height.getValue() - self._handrailHeight.getValue()
        apertureHeight = partHeight - (bottomDist + (interThick*2.0))

        normApertVec = Geom.Vec(apertureVec.y(), -apertureVec.x(), 0.0).normalized()
        endVec = normApertVec.crossed(apertureVec).normalized()
        strVec = Geom.Vec(-endVec)

        # start making transform: Matrix and translationPart
        e1 = Geom.XYZ(0.0, 0.0, 1.0)
        e2 = Geom.XYZ(-normApertVec.x(), -normApertVec.y(), 0.0)
        e3 = Geom.XYZ(normApertVec.y(), -normApertVec.x(), 0.0)
        M = Geom.Mat(e1, e2, e3)
        loc = Geom.XYZ(intStartPt.x(), intStartPt.y(), intStartPt.z())
        scale_factor = 1.0
        Tr = Geom.Trsf(M, loc, scale_factor)
        # finish making transform

        intEndPt = Geom.Pnt(intStartPt.x(), intStartPt.y(), intStartPt.z()+apertureHeight)
        dtStr = DataStruct(typeInt, intStartPt, intEndPt, intermRadius, intermRadius, strVec, endVec, Tr)
        beam_p = self._poolContainer['apertures'].createBeam(dtStr)
        self.addSubElement(beam_p)
        geom_p = beam_p.getGeometry()
        t_p = beam_p.getTransform()
        #
        for el in range(1, intermNum-1):
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
        # start making transform: Matrix and translationPart
        e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
        e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
        e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
        M = Geom.Mat(e1, e2, e3)
        loc = Geom.XYZ(beamStartPt.x(), beamStartPt.y(), beamStartPt.z())
        scale_factor = 1.0
        Tr = Geom.Trsf(M, loc, scale_factor)
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

    def _placeLineStep(self, model, startPt, stepHLen, segmBase, segmHBase, segmRecCos, addSupport):
        interThick = self._intermediateThickness.getValue()
        bottomDist = self._bottomDistance.getValue()
        supportRadius = self._intermediateThickness.getValue()
        hrRadiusV = self._handrailHeight.getValue() * 0.5
        sqType = BeamFactory.BT_Square

        e_x = Geom.Vec(segmBase.x(), segmBase.y(), segmBase.z())
        e_y = Geom.Vec(-segmBase.y(), segmBase.x(), 0.0).normalized()
        e_z = e_x.crossed(e_y).normalized()

        # Place support if needed
        if addSupport:
            suppHOffs = stepHLen - interThick * segmRecCos
            suppOffs = suppHOffs

            suppStartPt = baseVecTranslate(startPt, segmBase, suppOffs)
            # self._placeSupport(model, suppStartPt, segmHBase)
            lenSupp = self._height.getValue() - hrRadiusV - 1.0 * hrRadiusV * segmRecCos
            normSuppTang = Geom.Vec(segmBase.y(), -segmBase.x(), 0.0).normalized()
            endVec = normSuppTang.crossed(segmBase).normalized()
            strVec = Geom.Vec(0.0, 0.0, -1.0)
            # start making transform: Matrix and translationPart
            e1 = Geom.XYZ(0.0, 0.0, 1.0)
            e2 = Geom.XYZ(-normSuppTang.x(), -normSuppTang.y(), 0.0)
            e3 = Geom.XYZ(normSuppTang.y(), -normSuppTang.x(), 0.0)
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(suppStartPt.x(), suppStartPt.y(), suppStartPt.z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            suppEndPt = Geom.Pnt(suppStartPt.x(), suppStartPt.y(), suppStartPt.z()+lenSupp)
            dtStr = DataStruct(sqType, suppStartPt, suppEndPt, supportRadius, supportRadius, strVec, endVec, Tr)
            beam_sup = self._poolContainer['supports'].createBeam(dtStr)
            self.addSubElement(beam_sup)



        # Place bottom beam
        bottomEndHOffs = stepHLen - interThick * 2.0 * segmRecCos # !!!
        bottomEndOffs = bottomEndHOffs #* segmRecCos

        bottomStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + bottomDist + interThick)
        bottomEndPt = baseVecTranslate(bottomStartPt, segmBase, bottomEndOffs)
        # start making transform: Matrix and translationPart
        e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
        e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
        e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
        M = Geom.Mat(e1, e2, e3)
        loc = Geom.XYZ(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z())
        scale_factor = 1.0
        Tr = Geom.Trsf(M, loc, scale_factor)
        # finish making transform
        dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, interThick, interThick, -segmHBase, segmHBase, Tr)
        beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
        self.addSubElement(beam_bot)

        # Fill aperture
        apertureStartPt = Geom.Pnt(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z() + interThick)
        apertureVec = segmBase * bottomEndOffs

        if self._intermediateDirection.getValue() == 0:
            self._fillAperture_Vertical(model, apertureStartPt, apertureVec)
        else:
            self._fillAperture_Horizontal(model, apertureStartPt, apertureVec)

    def _placeLineSegment(self, model, startPt, endPt, startVecs, endVecs, isFirst, isLast, isClosed):
        startVec = startVecs[0]
        endVec = endVecs[0]
        startVec1 = startVecs[1]
        endVec1 = endVecs[1]
        # Place handrails
        hrRadiusH = self._handrailWidth.getValue() * 0.5
        hrRadiusV = self._handrailHeight.getValue() * 0.5
        hrStartZDelta = self._height.getValue() - hrRadiusV
        hrStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + hrStartZDelta)
        hrEndPt = Geom.Pnt(endPt.x(), endPt.y(), endPt.z() + hrStartZDelta)
        supportRadius = self._intermediateThickness.getValue()
        sqType = BeamFactory.BT_Square
        segmVec = Geom.Vec(startPt, endPt)
        segmBase = segmVec.normalized()
        hType = self._handrailType.getValue()
        # start making transform: Matrix and translationPart
        e_x = Geom.Vec(segmBase.x(), segmBase.y(), segmBase.z())
        e_y = Geom.Vec(-segmBase.y(), segmBase.x(), 0.0).normalized()
        e_z = e_x.crossed(e_y).normalized()

        e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
        e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
        e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
        M = Geom.Mat(e1, e2, e3)
        loc = Geom.XYZ(hrStartPt.x(), hrStartPt.y(), hrStartPt.z())
        scale_factor = 1.0
        Tr = Geom.Trsf(M, loc, scale_factor)
        # finish making transform
        if hType == 0:
            dtStr = DataStruct(hType, hrStartPt, hrEndPt, hrRadiusH, hrRadiusV, startVec1, endVec1, Tr)
        else:
            dtStr = DataStruct(hType, hrStartPt, hrEndPt, hrRadiusH, hrRadiusH, startVec1, endVec1, Tr)
        beam = self._poolContainer['topbeams'].createBeam(dtStr)
        self.addSubElement(beam)

        interThick = self._intermediateThickness.getValue()
        bottomDist = self._bottomDistance.getValue()
        segmHorVec = Geom.Vec(segmVec.x(), segmVec.y(), 0.0) # corrected Vec
        segmHorBase = segmHorVec.normalized()
        
        segmHorLen = segmVec.magnitude()
        if segmHorLen < epsilon:
            return

        segmRecCos = 1.0 / segmBase.dot(segmHorBase)
        angle = Geom.Vec.angle(segmBase, startVec)
        segmStartCos = 1.0 / math.sin(angle)
        baseRecCos = 1.0 /segmBase.dot(segmHorBase)

        startSuppPt = Geom.Pnt(startPt)
        buildStartOffs = supportRadius * segmRecCos #* segmStartCos
        if isFirst and (not isClosed):
            startSuppOffs = buildStartOffs
            startSuppPt = baseVecTranslate(startPt, segmBase, startSuppOffs) # startSuppOffs

            lenSupp = self._height.getValue() - hrRadiusV - 1.0 * hrRadiusV * baseRecCos
            normSuppTang = Geom.Vec(segmBase.y(), -segmBase.x(), 0.0).normalized()
            endVec = normSuppTang.crossed(segmBase).normalized()
            strVec = Geom.Vec(0.0, 0.0, -1.0)
            # start making transform: Matrix and translationPart
            e1 = Geom.XYZ(0.0, 0.0, 1.0)
            e2 = Geom.XYZ(-normSuppTang.x(), -normSuppTang.y(), 0.0)
            e3 = Geom.XYZ(normSuppTang.y(), -normSuppTang.x(), 0.0)
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(startSuppPt.x(), startSuppPt.y(), startSuppPt.z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            endSuppPt = Geom.Pnt(startSuppPt.x(), startSuppPt.y(), startSuppPt.z()+lenSupp)
            dtStr = DataStruct(sqType, startSuppPt, endSuppPt, supportRadius, supportRadius, strVec, endVec, Tr)
            beam_sup = self._poolContainer['supports'].createBeam(dtStr)
            self.addSubElement(beam_sup)

            buildStartOffs = supportRadius * 2.0 * segmRecCos

        if isFirst and isClosed:
            angle2 = Geom.Vec.angle(segmBase, startVec)
            if angle2 >= math.pi:
                angle2 = angle2 - 0.5 * math.pi
                corDist = - interThick * (1.0 + math.tan(angle2) - 1.0 / math.cos(angle2))
            elif angle2 < math.pi:
                angle2 = 0.5 * math.pi - angle2
                corDist = interThick * (1.0 + math.tan(angle2) - 1.0 / math.cos(angle2))
            startSuppPt = baseVecTranslate(startPt, startVec, corDist)
            # TODO: !!!!!
            # self._placeSupport(model, startSuppPt, startVec)
            startSuppPt = Geom.Pnt(startPt)

            buildStartOffs = supportRadius * segmRecCos


        buildEndOffs = segmHorLen + supportRadius * segmRecCos
        endSuppPt = Geom.Pnt(endPt)
        if isLast and (not isClosed):
            buildEndOffs = segmHorLen

            endSuppOffs = supportRadius * segmRecCos
            endSuppStPt = baseVecTranslate(endPt, -segmBase, endSuppOffs)
            #print(endSuppPt.x(), endSuppPt.y())

            lenSupp = self._height.getValue() - hrRadiusV - 1.0 * hrRadiusV * baseRecCos
            normSuppTang = Geom.Vec(segmBase.y(), -segmBase.x(), 0.0).normalized()
            endVec = normSuppTang.crossed(segmBase).normalized()
            strVec = Geom.Vec(0.0, 0.0, -1.0)
            # start making transform: Matrix and translationPart
            e1 = Geom.XYZ(0.0, 0.0, 1.0)
            e2 = Geom.XYZ(-normSuppTang.x(), -normSuppTang.y(), 0.0)
            e3 = Geom.XYZ(normSuppTang.y(), -normSuppTang.x(), 0.0)
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(endSuppStPt.x(), endSuppStPt.y(), endSuppStPt.z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            endSuppEnPt = Geom.Pnt(endSuppStPt.x(), endSuppStPt.y(), endSuppStPt.z()+lenSupp)
            dtStr = DataStruct(sqType, endSuppStPt, endSuppEnPt, supportRadius, supportRadius, strVec, endVec, Tr)
            beam_sup = self._poolContainer['supports'].createBeam(dtStr)
            self.addSubElement(beam_sup)
            endSuppPt = Geom.Pnt(endSuppStPt)


        supportVec = Geom.Vec(startSuppPt, endSuppPt)
        supportLen = supportVec.magnitude()

        buildStartPt = baseVecTranslate(startPt, segmBase, buildStartOffs)
        buildEndPt = baseVecTranslate(startPt, segmBase, buildEndOffs)

        buildVec = Geom.Vec(buildStartPt, buildEndPt)
        buildLen = buildVec.magnitude()

        buildHorVec = Geom.Vec(buildVec.x(), buildVec.y(), buildVec.z())
        buildHorLen = buildHorVec.magnitude()

        #stepNum, colHorDist = self._calcColDist(buildHorLen)
        stepNum, colHorDist = self._calcColDist(supportLen)
        colDist = buildLen / float(stepNum)

        stepStartPt = buildStartPt
        lastStepId = stepNum - 1

        # Place bottom beam

        self._placeLineStep(model, stepStartPt, colHorDist, segmBase, segmHorBase, segmRecCos, (lastStepId >= 1))
        stepStartPt = baseVecTranslate(stepStartPt, segmBase, colDist)

        for step in range(1, lastStepId):
            self._placeLineStep(model, stepStartPt, colHorDist, segmBase, segmHorBase, segmRecCos, True)

            stepStartPt = baseVecTranslate(stepStartPt, segmBase, colDist)

        if stepNum > 1:
            self._placeLineStep(model, stepStartPt, colHorDist, segmBase, segmHorBase, segmRecCos, False)

    def _extendStepLastPt(self, startPt, endPt, dLen):
        stepVec = Geom.Vec(startPt, endPt)
        stepBase = stepVec.normalized()

        stepLen = stepVec.magnitude()

        return baseVecTranslate(startPt, stepBase, stepLen + dLen)

    def _setHorCutTopBeams(self, model, listPnt, listVec, vRadius, hRadius, isLoop=False):
        typeB = self._handrailType.getValue()
        if isLoop:
            if typeB == 0:
                model.addCutHorBeam(typeB, listPnt[0], listPnt[1], hRadius, vRadius, -listVec[len(listVec) - 1], listVec[1])
            else:
                model.addCutHorBeam(typeB, listPnt[0], listPnt[1], hRadius, hRadius, -listVec[len(listVec) - 1], listVec[1])
        else:
            baseVec = Geom.Vec(listPnt[0], listPnt[1]).normalized()
            # start making transform: Matrix and translationPart
            e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
            e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
            e_z = e_x.crossed(e_y).normalized()

            e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
            e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
            e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(listPnt[0].x(), listPnt[0].y(), listPnt[0].z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            if typeB == 0:
                dtStr = DataStruct(typeB, listPnt[0], listPnt[1], hRadius, vRadius, listVec[0], listVec[1], Tr)
            else:
                dtStr = DataStruct(typeB, listPnt[0], listPnt[1], hRadius, hRadius, listVec[0], listVec[1], Tr)
            beam_top = self._poolContainer['topbeams'].createBeam(dtStr)
            self.addSubElement(beam_top)


        for i in range(1, len(listPnt) - 2):
            baseVec = Geom.Vec(listPnt[i], listPnt[i+1]).normalized()
            # start making transform: Matrix and translationPart
            e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
            e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
            e_z = e_x.crossed(e_y).normalized()

            e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
            e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
            e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(listPnt[i].x(), listPnt[i].y(), listPnt[i].z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            if typeB == 0:
                dtStr = DataStruct(typeB, listPnt[i], listPnt[i+1], hRadius, vRadius, -listVec[i], listVec[i + 1], Tr)
                # model.addCutHorBeam(typeB, listPnt[i], listPnt[i + 1], hRadius, vRadius, -listVec[i], listVec[i + 1])
            else:
                dtStr = DataStruct(typeB, listPnt[i], listPnt[i+1], hRadius, hRadius, -listVec[i], listVec[i + 1], Tr)
                # model.addCutHorBeam(typeB, listPnt[i], listPnt[i + 1], hRadius, hRadius, -listVec[i], listVec[i + 1])
            beam_top = self._poolContainer['topbeams'].createBeam(dtStr)
            self.addSubElement(beam_top)

        if isLoop:
            pass
            # dmodel.addHorCutBeam(listPnt[len(listPnt)-2], listPnt[len(listPnt)-1], vRadius, hRadius, preBisec, nexBisec)
            # model.adHorCutBeam(listPnt[len(listPnt)-1], listPnt[0], vRadius, hRadius, nexBisec, zeroBisec)
        elif len(listPnt)>2:
            baseVec = Geom.Vec(listPnt[len(listPnt)-2], listPnt[len(listPnt)-1]).normalized()
            # start making transform: Matrix and translationPart
            e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
            e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
            e_z = e_x.crossed(e_y).normalized()

            e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
            e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
            e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(listPnt[len(listPnt)-2].x(), listPnt[len(listPnt)-2].y(), listPnt[len(listPnt)-2].z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            if typeB == 0:
                dtStr = DataStruct(typeB, listPnt[len(listPnt) - 2], listPnt[len(listPnt) - 1], hRadius, vRadius,
                                    -listVec[len(listVec)-2], listVec[len(listVec)-1], Tr)
            else:
                dtStr = DataStruct(typeB, listPnt[len(listPnt) - 2], listPnt[len(listPnt) - 1], hRadius, hRadius,
                                    -listVec[len(listVec)-2], listVec[len(listVec)-1], Tr)
            beam_top = self._poolContainer['topbeams'].createBeam(dtStr)
            self.addSubElement(beam_top)

    def _setArrSupports(self, model, arc, listParam, listVec, isLoop=False):
        sqType = BeamFactory.BT_Square

        for i in range(1, len(listParam) - 1):
            curSuppPt = arc.paramPt(listParam[i])
            partHeight = self._height.getValue() - self._handrailHeight.getValue()
            supportRadius = self._intermediateThickness.getValue()

            curSuppTang = arc.paramTangent(listParam[i])
            lenSupp = self._height.getValue() - self._handrailHeight.getValue()
            normSuppTang = Geom.Vec(curSuppTang.y(), -curSuppTang.x(), 0.0).normalized()
            endVec = normSuppTang.crossed(curSuppTang).normalized()
            strVec = Geom.Vec(0.0, 0.0, -1.0)
            # start making transform: Matrix and translationPart
            e1 = Geom.XYZ(0.0, 0.0, 1.0)
            e2 = Geom.XYZ(-normSuppTang.x(), -normSuppTang.y(), 0.0)
            e3 = Geom.XYZ(normSuppTang.y(), -normSuppTang.x(), 0.0)
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(curSuppPt.x(), curSuppPt.y(), curSuppPt.z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            suppEndPt = Geom.Pnt(curSuppPt.x(), curSuppPt.y(), curSuppPt.z()+lenSupp)
            dtStr = DataStruct(sqType, curSuppPt, suppEndPt, supportRadius, supportRadius, strVec, endVec, Tr)
            beam_sup = self._poolContainer['supports'].createBeam(dtStr)
            self.addSubElement(beam_sup)

    def _setHorCutBottomBeams(self, model, arc, listParam, listVec, vRadius, hRadius, isLoop=False):
        bottomDist = self._bottomDistance.getValue()
        interThick = self._intermediateThickness.getValue()

        sqType = BeamFactory.BT_Square

        paramRatio = arc.paramRatio()
        supportRadius = self._intermediateThickness.getValue()
        startTang = arc.paramTangent(listParam[0] + supportRadius*paramRatio)
        angle0 = Geom.Vec.angle(startTang, listVec[0])
        segmStartSin = 1.0 / math.sin(angle0)
        baseVec = Geom.Vec(arc.paramPt(listParam[0]), arc.paramPt(listParam[1])).normalized()
        baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
        baseRecCos = 1.0 / baseVec.dot(baseHorVec)
        prePnt = arc.paramPt(listParam[0] + supportRadius*paramRatio*baseRecCos)  # * segmStartSin
        curPnt = arc.paramPt(listParam[1] - supportRadius*paramRatio*baseRecCos)

        bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z() + bottomDist + interThick)
        bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z() + bottomDist + interThick)

        # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[0], listVec[1])
        strVec = Geom.Vec(listVec[0].x(), listVec[0].y(), 0.0)
        endVec = Geom.Vec(listVec[1].x(), listVec[1].y(), 0.0)
        # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, vRadius, interThick, strVec, endVec)
        # start making transform: Matrix and translationPart
        e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
        e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
        e_z = e_x.crossed(e_y).normalized()

        e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
        e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
        e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
        M = Geom.Mat(e1, e2, e3)
        loc = Geom.XYZ(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z())
        scale_factor = 1.0
        Tr = Geom.Trsf(M, loc, scale_factor)
        # finish making transform
        # suppEndPt = Geom.Pnt(suppStartPt.x(), suppStartPt.y(), suppStartPt.z()+lenSupp)
        dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec, Tr)
        beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
        self.addSubElement(beam_bot)
        

        for i in range(1, len(listParam) - 2):
            baseVec = Geom.Vec(arc.paramPt(listParam[i]), arc.paramPt(listParam[i+1])).normalized()
            baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
            baseRecCos = 1.0 / baseVec.dot(baseHorVec)
            prePnt = arc.paramPt(listParam[i] + supportRadius * paramRatio * baseRecCos)
            curPnt = arc.paramPt(listParam[i+1] - supportRadius * paramRatio * baseRecCos)
            bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z() + bottomDist + interThick)
            bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z() + bottomDist + interThick)
            # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[i], listVec[i+1])
            strVec = Geom.Vec(-listVec[i].x(), -listVec[i].y(), 0.0)
            endVec = Geom.Vec(listVec[i+1].x(), listVec[i+1].y(), 0.0)
            # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec)
            # start making transform: Matrix and translationPart
            e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
            e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
            e_z = e_x.crossed(e_y).normalized()

            e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
            e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
            e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            # suppEndPt = Geom.Pnt(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z()+lenSupp)
            dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec, Tr)
            beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
            self.addSubElement(beam_bot)

        if isLoop:
            #build prelast and last segment
            nexPnt = Geom.Pnt(listPnt[0].x(), listPnt[0].y(), 0.0)
            nexVec = Geom.Vec(nexPnt.x() - curPnt.x(), nexPnt.y() - curPnt.y(), 0.0)
            nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0) / nexVec.magnitude()
            nexBisec = (preNor + nexNor) / (preNor + nexNor).magnitude()
            # model.addHorCutBeam(listPnt[len(listParam)-2], listPnt[len(listPnt)-1], vRadius, hRadius, preBisec, nexBisec)
            # model.addHorCutBeam(listPnt[len(listParam)-1], listPnt[0], vRadius, hRadius, nexBisec, zeroBisec)
        elif len(listParam)>2:
            endTang = arc.paramTangent(listParam[len(listParam) - 1] - supportRadius)
            angle1 = Geom.Vec.angle(endTang, listVec[len(listVec)-1])
            segmEndSin = 1.0 / math.sin(angle1)
            baseVec = Geom.Vec(arc.paramPt(listParam[len(listParam) - 2]), arc.paramPt(listParam[len(listParam) - 1])).normalized()
            baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
            baseRecCos = 1.0 / baseVec.dot(baseHorVec)
            prePnt = arc.paramPt(listParam[len(listParam) - 2] + supportRadius*paramRatio*baseRecCos)
            curPnt = arc.paramPt(listParam[len(listParam) - 1] - supportRadius*paramRatio*baseRecCos)  # * segmEndSin
            bottomStartPt = Geom.Pnt(prePnt.x(), prePnt.y(), prePnt.z() + bottomDist + interThick)
            bottomEndPt = Geom.Pnt(curPnt.x(), curPnt.y(), curPnt.z() + bottomDist + interThick)
            # model.addHorCutBeam(bottomStartPt, bottomEndPt, vRadius, hRadius, listVec[len(listVec)-2], listVec[len(listVec)-1])
            strVec = Geom.Vec(-listVec[len(listVec)-2].x(), -listVec[len(listVec)-2].y(), 0.0)
            endVec = Geom.Vec(listVec[len(listVec)-1].x(), listVec[len(listVec)-1].y(), 0.0)
            # model.addCutHorBeam(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec)
            # start making transform: Matrix and translationPart
            e_x = Geom.Vec(baseVec.x(), baseVec.y(), baseVec.z())
            e_y = Geom.Vec(-baseVec.y(), baseVec.x(), 0.0).normalized()
            e_z = e_x.crossed(e_y).normalized()

            e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
            e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
            e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(bottomStartPt.x(), bottomStartPt.y(), bottomStartPt.z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            # suppEndPt = Geom.Pnt(bottomStartPt.x(), suppStartPt.y(), suppStartPt.z()+lenSupp)
            dtStr = DataStruct(sqType, bottomStartPt, bottomEndPt, interThick, interThick, strVec, endVec, Tr)
            beam_bot = self._poolContainer['botbeams'].createBeam(dtStr)
            self.addSubElement(beam_bot)

    def _placeArcStep(self, model, startPt, endPt, addSupport):
        # Place rest of the geometry
        bottomDist = self._bottomDistance.getValue()
        interThick = self._intermediateThickness.getValue()
        stepVec = Geom.Vec(startPt, endPt)
        stepBase = stepVec.normalized()

        stepHVec = Geom.Vec(stepVec.x(), stepVec.y(), 0.0)
        stepHBase = stepHVec.normalized()
        stepHLen = stepHVec.magnitude()

        stepRecCos = 1.0 / stepBase.dot(stepHBase)

        #self._placeStep(model, startPt, stepHLen, stepBase, stepHBase, stepRecCos, addSupport)
        apertureStartPt = Geom.Pnt(startPt.x(), startPt.y(), startPt.z() + bottomDist + 2.*interThick)
        apertureVec = stepVec  #segmBase * bottomEndOffs

        if self._intermediateDirection.getValue() == 0:
            self._fillAperture_Vertical(model, apertureStartPt, apertureVec)
        else:
            self._fillAperture_Horizontal(model, apertureStartPt, apertureVec)

    def _placeArcSegment(self, model, arc, startVecs, endVecs, isFirst, isLast, isClosed):
        startVec = startVecs[0]
        endVec = endVecs[0]
        startVec1 = startVecs[1]
        endVec1 = endVecs[1]

        arcLen = arc.length()
        paramRatio = arc.paramRatio()
        supportRadius = self._intermediateThickness.getValue()
        # supportSize = supportRadius * 2.0
        startParam = 0.0
        endParam = 1.0

        hrRadiusH = self._handrailWidth.getValue() * 0.5
        hrRadiusV = self._handrailHeight.getValue() * 0.5
        hrStartZDelta = self._height.getValue() - hrRadiusV
        sqType = BeamFactory.BT_Square

        if isFirst and (not isClosed):
            startSuppTang = arc.startTangent()
            startSuppTangHor = Geom.Vec(startSuppTang.x(), startSuppTang.y(), 0.0).normalized()
            # baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
            baseRecCos = 1.0 /startSuppTang.dot(startSuppTangHor)
            startParam = supportRadius * paramRatio * baseRecCos
            startSuppPt = arc.paramPt(startParam)
            lenSupp = self._height.getValue() - (1.0 + baseRecCos) * hrRadiusV
            # self._placeSupport(model, startSuppPt, startSuppTang)
            normSuppTang = Geom.Vec(startSuppTang.y(), -startSuppTang.x(), 0.0).normalized()
            endVec = normSuppTang.crossed(startSuppTang).normalized()
            strVec = Geom.Vec(0.0, 0.0, -1.0)
            # start making transform: Matrix and translationPart
            e1 = Geom.XYZ(0.0, 0.0, 1.0)
            e2 = Geom.XYZ(-normSuppTang.x(), -normSuppTang.y(), 0.0)
            e3 = Geom.XYZ(normSuppTang.y(), -normSuppTang.x(), 0.0)
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(startSuppPt.x(), startSuppPt.y(), startSuppPt.z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            endSuppPt = Geom.Pnt(startSuppPt.x(), startSuppPt.y(), startSuppPt.z()+lenSupp)
            dtStr = DataStruct(sqType, startSuppPt, endSuppPt, supportRadius, supportRadius, strVec, endVec, Tr)
            beam_sup = self._poolContainer['supports'].createBeam(dtStr)
            self.addSubElement(beam_sup)

        if isFirst and isClosed:
            #startParam = supportRadius * paramRatio
            startSuppPt = arc.paramPt(0.0)
            startSuppTang = arc.startTangent()
            angle2 = Geom.Vec.angle(startSuppTang, startVec)
            if angle2 >= math.pi:
                angle2 = angle2 - 0.5 * math.pi
                corDist = - supportRadius * (1.0 + math.tan(angle2) - 1.0 / math.cos(angle2))
            elif angle2 < math.pi:
                angle2 = 0.5 * math.pi - angle2
                corDist = supportRadius * (1.0 + math.tan(angle2) - 1.0 / math.cos(angle2))
            startSuppPt = baseVecTranslate(startSuppPt, startVec, corDist)

            # self._placeSupport(model, startSuppPt, startVec)

            startSuppPt = arc.paramPt(0.0)

        if isLast and (not isClosed):
            endSuppTang = arc.endTangent()
            endSuppTangHor = Geom.Vec(endSuppTang.x(), endSuppTang.y(), 0.0).normalized()
            # baseHorVec = Geom.Vec(baseVec.x(), baseVec.y(), 0.0).normalized()
            baseRecCos = 1.0 /endSuppTang.dot(endSuppTangHor)
            endParam = 1.0 - supportRadius * paramRatio * baseRecCos
            endSuppStPt = arc.paramPt(endParam)
            # self._placeSupport(model, endSuppPt, endSuppTang)
            lenSupp = self._height.getValue() - (1.0 + baseRecCos) * hrRadiusV
            normSuppTang = Geom.Vec(endSuppTang.y(), -endSuppTang.x(), 0.0).normalized()
            endVec = normSuppTang.crossed(endSuppTang).normalized()
            strVec = Geom.Vec(0.0, 0.0, -1.0)
            # start making transform: Matrix and translationPart
            e1 = Geom.XYZ(0.0, 0.0, 1.0)
            e2 = Geom.XYZ(-normSuppTang.x(), -normSuppTang.y(), 0.0)
            e3 = Geom.XYZ(normSuppTang.y(), -normSuppTang.x(), 0.0)
            M = Geom.Mat(e1, e2, e3)
            loc = Geom.XYZ(endSuppStPt.x(), endSuppStPt.y(), endSuppStPt.z())
            scale_factor = 1.0
            Tr = Geom.Trsf(M, loc, scale_factor)
            # finish making transform
            endSuppEnPt = Geom.Pnt(endSuppStPt.x(), endSuppStPt.y(), endSuppStPt.z()+lenSupp)
            dtStr = DataStruct(sqType, endSuppStPt, endSuppEnPt, supportRadius, supportRadius, strVec, endVec, Tr)
            beam_sup = self._poolContainer['supports'].createBeam(dtStr)
            self.addSubElement(beam_sup)

        buildParamLen = endParam - startParam
        buildLen = buildParamLen * arcLen
        # print startParam, endParam
        stepNum, colHorDist = self._calcColDist(buildLen)
        paramDist = buildParamLen / float(stepNum)

        listPnt = []
        listParam = []

        stepParam = startParam
        listParam.append(startParam)

        stepStartPt = arc.paramPt(stepParam + supportRadius*paramRatio) #*segmStartSin
        lastStepId = stepNum - 1
        hrStartPt = arc.paramPt(0.0)
        hrStartPt = Geom.Pnt(hrStartPt.x(), hrStartPt.y(), hrStartPt.z() + hrStartZDelta)
        listPnt.append(hrStartPt)
        for step in range(lastStepId):
            stepParam += paramDist
            stepEndPt = arc.paramPt(stepParam - supportRadius*paramRatio) #

            self._placeArcStep(model, stepStartPt, stepEndPt, True)
            #print(stepStartPt.x(), stepStartPt.y())

            stepEndPt = arc.paramPt(stepParam + supportRadius * paramRatio)
            listParam.append(stepParam)
            hrEndPt = arc.paramPt(stepParam)
            hrEndPt = Geom.Pnt(hrEndPt.x(), hrEndPt.y(), hrEndPt.z() + hrStartZDelta)
            listPnt.append(hrEndPt)

            stepStartPt = stepEndPt

        stepParam += paramDist
        listParam.append(stepParam)

        stepEndPt = arc.paramPt(stepParam - supportRadius * paramRatio) # *segmEndSin
        self._placeArcStep(model, stepStartPt, stepEndPt, False)

        hrEndPt = arc.paramPt(1.0)
        hrEndPt = Geom.Pnt(hrEndPt.x(), hrEndPt.y(), hrEndPt.z()+hrStartZDelta)
        listPnt.append(hrEndPt)

        listVec = self._setAllArcVectors(listPnt, startVecs, endVecs)

        self._setHorCutTopBeams(model, listPnt, listVec[1], hrRadiusV, hrRadiusH)

        self._setArrSupports(model, arc, listParam, listVec[0])

        self._setHorCutBottomBeams(model, arc, listParam, listVec[1], supportRadius, supportRadius)

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
            self._placeArcSegment(model, arc, startVec, endVec, isFirst, isLast, isClosed)
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

        self._placeSupportsAccLine(model, polyLine)
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

    def handrailHeight(self):
        return self._handrailHeight.getValue()

    def minHandrailHeight(self):
        return 0.001

    def maxHandrailHeight(self):
        return 10000.0

    def setHandrailType(self, handrailType):
        with EditMode(self.getDocument()):
            self._handrailType.setValue(handrailType)
            self.showSolidModelRepresentation()
            self._representation.setValue(1)
            self._updateGeometry()

    def setColumnDistance(self, columnDistance):
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

        if aPropertyName == self._height.getName():
            self.setHeight(self._height.getValue())
        elif aPropertyName == self._handrailWidth.getName():
            self.setHandrailWidth(self._handrailWidth.getValue())
        elif aPropertyName == self._handrailHeight.getName():
            self.setHandrailHeight(self._handrailHeight.getValue())
        elif aPropertyName == self._handrailType.getName():
            self.setHandrailType(self._handrailType.getValue())
        elif aPropertyName == self._columnDistance.getName():
            self.setColumnDistance(self._columnDistance.getValue())
        elif aPropertyName == self._bottomDistance.getName():
            self.setBottomDistance(self._bottomDistance.getValue())
        elif aPropertyName == self._intermediateThickness.getName():
            self.setIntermediateThickness(self._intermediateThickness.getValue())
        elif aPropertyName == self._intermediateType.getName():
            self.setIntermediateType(self._intermediateType.getValue())
        elif aPropertyName == self._intermediateDirection.getName():
            self.setIntermediateDirection(self._intermediateDirection.getValue())
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
        element = BalustradeSegments(doc)
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
                if element.setAxisCurve(geometry):
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
                geometry = pickedElement.getGeometry()
                if element.setAxisCurve(geometry):
                    doc.removeObject(pickedElement)

    
if __name__ == "__main__":
    main()
