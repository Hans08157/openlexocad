# coding=utf-8
# OpenLexocad libraries
import math
import traceback
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Draw, Geom, Topo
# from PySide2 import QtWidgets, QtCore, QtGui

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

st = Topo.ShapeTool

doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

epsilon = 0.0001
maxValue = 10000

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

class PolylineReader:
    def __init__(self, polyLine):
        self.polyline = polyLine
        self.segmCount = polyLine.segmentCount()
        self.e = 0.0001
        self.pointListWithDistance = []
        self.segmentsList = []

        if self.segmCount <= 0:
            #print("There are anything segments")
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
                #print("Radius = ", arc.radius(), ", angle = ", arc.angle(), arc.angle() * 180.0 / math.pi)
                n = int(math.fabs(arc.angle() / (math.acos(((arc.radius() - self.e) / arc.radius())) * 2.0)))
                #print("N = ", n)
                for i in range(n):
                    pnt0 = arc.paramPt(float(i) / float(n))
                    pnt1 = arc.paramPt((float(float(i) + 1.0) / float(n)))
                    if ((float(float(i) + 1.0) / float(n))) <= 1.0:
                        lineSegment = self.SegmLine(pnt0, pnt1)
                        self.segmentsList.append(lineSegment)
                #print("ARC")
            else:
                #print("Unknown segment")
                return

    def getListPointWithDistanceOnPolyline(self, dist, radius, withLast):
        listPoint = []
        for segm in self.segmentsList:
            endPoint = self.segmentsList[len(self.segmentsList)-1].p1
            if segm == self.segmentsList[len(self.segmentsList)-1]:
                ifLast = True
            else:
                ifLast = False
            if len(listPoint) >= 1:
                distToPrev = segm.getDistanceToFirstPnt(listPoint[len(listPoint)-1], dist)
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
                #print("COEFICIENT T OUT OF RANGE!!!")
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
            c = (math.pow(qx,2))-(2.0*qx*p0x)+(math.pow(p0x,2))+(math.pow(qy,2))-(2.0*qy*p0y)+(math.pow(p0y,2))-len
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
                #print("D", D)
                #print("WRONG DISCRIMINANT")
                return None

        def getListPointWithDistance(self, distance, ifLast, rad, startDistance):
            pointList = []

            vecForAngle = Geom.Vec(Geom.Pnt(self.p0.x(), self.p0.y(), self.p0.z()), Geom.Pnt(self.p1.x(), self.p1.y(), self.p0.z()))
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
        beamGeom.setHeight(diameterV)

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
        beamGeom = lx.RightCircularCylinder .createIn(self._doc)
        beamGeom.setHeight(length)
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

        beam = self._createBaseBeam(beamType, beamLen+4.*radiusV, radiusH, radiusV, angle)

        rotAxisV = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 1, 0))
        beam.rotate(rotAxisV, beamAngleV, Geom.CoordSpace_WCS)

        rotAxisH = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 0, 1))
        beam.rotate(rotAxisH, beamAngleH, Geom.CoordSpace_WCS)

        beam.translate(Geom.Vec(startPt.x(), startPt.y(), startPt.z()), Geom.CoordSpace_WCS)
        trans = Geom.Vec(0.0 - 2.*radiusV*dir.x(), 0.0 - 2.*radiusV*dir.y(), 0.0 - 2.*radiusV*dir.z())
        #print()
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
        #doc.recompute()

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
        extrudeFace = Topo.FaceTool.extrudedFace(wire, Geom.Dir(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(0.0, 0.0, 1.0))), vRadius * 2.0)
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

# class LogoWindow(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.logo = QtWidgets.QLabel("Hello LexoCAD!")
#         self.hBox = QtWidgets.QHBoxLayout()
#         self.hBox.addWidget(self.logo)
#
#         self.setWindowTitle("lx.Window")
#         self.setLayout(self.hBox)


class FenceElem(lx.Element):
    _headerName = "Fence"
    _groupName = "Fence Parameters"
    _heightPropName = "Height"
    _colorPropName = "Color"
    _colorBoolPropName = "Use color"
    _polylinePropName = "Polyline"
    # _buttonPropName = "Logo"
    # _logoHeightPropName = "Logo Height"
    # _logoWidthPropName = "Logo Width"


    def getGlobalClassId(self):
        return Base.GlobalId("{7D520272-FBE3-4984-980C-3EFE5786B987}")

    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("FenceElem", "OpenLxApp.Element")
        # Register properties
        self.setPropertyHeader(lxstr(FenceElem._headerName), -1)
        self.setPropertyGroupName(lxstr(FenceElem._groupName), -1)

        self._height = self.registerPropertyDouble(FenceElem._heightPropName, 2.0, lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE, -1)
        self._colorBool = self.registerPropertyBool(FenceElem._colorBoolPropName, True, lx.Property.VISIBLE,
                                                    lx.Property.EDITABLE, -1)
        self._color = self.registerPropertyColor(FenceElem._colorPropName, Base.Color(5, 193, 74),
                                                 lx.Property.VISIBLE,
                                                 lx.Property.EDITABLE, -1)

        self._polyline = self.registerPropertyString(FenceElem._polylinePropName, lxstr(""), lx.Property.NOT_VISIBLE,
                                                     lx.Property.NOT_EDITABLE, -1)  # NOT_VISIBLE
        self._modules = self.registerPropertyDouble("Modules", 0.0, lx.Property.NOT_VISIBLE,
                                                    lx.Property.NOT_EDITABLE, -1)
        # self._logo = self.registerPropertyButton(FenceElem._buttonPropName, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        # self._logoWidth = self.registerPropertyDouble(FenceElem._logoWidthPropName, 2.30, lx.Property.VISIBLE,
        #                                               lx.Property.EDITABLE, -1)
        # self._logoHeight = self.registerPropertyDouble(FenceElem._logoHeightPropName, 1.10, lx.Property.VISIBLE,
        #                                                lx.Property.EDITABLE, -1)

        self._setAllSteps()
        self._setupColorBool()

        self._baseData = None
        dataStr = cstr(self._polyline.getValue())
        if dataStr:
            self._baseData = self.readFromString(dataStr)

        
        # self._updateGeometry()

    # def _onSelectButtonClicked(self):
    #     import sys
    #     app = QtWidgets.QApplication(sys.argv)
    #     window = LogoWindow()
    #     window.resize(200, 300)
    #     window.show()
    #
    #     sys.exit(app.exec_())

    def _setupColorBool(self):
        mVal = self._colorBool.getValue()

        if mVal is 0:
            self._color.setVisible(False)
            print("Color property has set to False")
        elif mVal is 1:
            self._color.setVisible(True)
            print("Color property has set to True")


        # if mVal is 0:
        #     self._color.setVisible(False)
        #     print("Color property has set to False")
        # elif mVal is 1:
        #     self._color.setVisible(True)
        #     print("Color property has set to True")

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

    def setPolylineData(self, polylineData):
        if lxstr(self.writeToString(polylineData)) is self._modules.getValue():
            print("Select another polyline")
            return

        #if not self._insidePropUpdate:
        self._insidePropUpdate = True

        self._baseData = polylineData
        self._polyline.setValue(lxstr(self.writeToString(polylineData)))
        #self.printPolylineTest(cstr(self._polyline.getValue()))

        self._updateGeometry()

    def _setAllSteps(self):
        self._height.setSteps(0.1)
        # self._logoWidth.setSteps(0.05)
        # self._logoHeight.setSteps(0.05)

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

    def getPolyline(self):
        return self._polyline.getValue()

    def setHeight(self, param):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    # def setLogoHeight(self, param):
    #     maxValue = self._height.getValue()
    #     with EditMode(self.getDocument()):
    #         self._logoHeight.setValue(clamp(param, epsilon, maxValue))
    #         self._updateGeometry()
    #     if param < epsilon:
    #         Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
    #                                              qstr("The value is too small"))
    #     elif param > maxValue:
    #         Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
    #                                              qstr("The value is too big"))

    # def setLogoWidth(self, param):
    #     with EditMode(self.getDocument()):
    #         self._logoWidth.setValue(clamp(param, epsilon, maxValue))
    #         self._updateGeometry()
    #     if param < epsilon:
    #         Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
    #                                              qstr("The value is too small"))
    #     elif param > maxValue:
    #         Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
    #                                              qstr("The value is too big"))

    def setColor(self, param):
        with EditMode(self.getDocument()):
            self._color.setValue(param)
            self._updateGeometry()

    def setColorBool(self, param):
        with EditMode(self.getDocument()):
            self._colorBool.setValue(param)
            self._updateGeometry()

    # def _calcPointsForLogo(self, polyLine):
        # return [logoPnt1, logoPnt2, logoPnt3, logoPnt4]

    def _createLogos(self, model):
        # Logo faces
        mHeight = self._height.getValue()

        logoWidth = self._logoWidth.getValue()
        logoHeight = self._logoHeight.getValue()

        lowerPntsHeight = 0.5 * (mHeight - logoHeight)
        upperPntsHeight = 0.5 * (mHeight + logoHeight)
        # polyline data
        polyLine = PolylineData.fromElement(self._baseData)

        logoTexture = Draw.Texture2()
        logoTexture.setTextureFileName(lxstr('textures/630.jpg'))  # While PySide2 not working.

        for i in range(polyLine.pointCount() - 1):
            vec = Geom.Vec(polyLine.point(i), polyLine.point(i + 1))
            magn = vec.magnitude()
            normVec = vec.normalized()

            halfVec = baseVecTranslate(polyLine.point(i), normVec, magn * 0.50000)
            # print("HalfVec -> ", halfVec.x(), halfVec.y(), halfVec.z())

            pntVec = Geom.Vec(Geom.Pnt(halfVec.x(), halfVec.y(), halfVec.z()), polyLine.point(i + 1))
            pntVec.normalize()
            pnt2Vec = baseVecTranslate(Geom.Pnt(halfVec.x(), halfVec.y(), halfVec.z()), pntVec, logoWidth * 0.5000)
            pnt1Vec = pnt2Vec.mirrored(Geom.Pnt(halfVec.x(), halfVec.y(), halfVec.z()))

            # Calculating points
            floorpnt2 = Geom.Pnt(pnt2Vec.coord())
            floorpnt1 = Geom.Pnt(pnt1Vec.coord())

            # Offsetting two floor points to avoid flickering

            offsetVec2 = Geom.Vec(floorpnt2, polyLine.point(i))
            offsetVec1 = Geom.Vec(floorpnt1, polyLine.point(i + 1))
            # offsetVec1.normalize(); offsetVec2.normalize()

            offsetVec2.rotate(Geom.Ax1(floorpnt2, Geom.Dir(0, 0, 1)), -math.radians(90.0))
            offsetVec1.rotate(Geom.Ax1(floorpnt1, Geom.Dir(0, 0, 1)), math.radians(90.0))
            offsetVec1.normalize()
            offsetVec2.normalize()

            logoVec2 = baseVecTranslate(floorpnt2, offsetVec2, 0.005)
            logoVec1 = baseVecTranslate(floorpnt1, offsetVec1, 0.005)

            logoVec3 = logoVec2.mirrored(floorpnt2)
            logoVec4 = logoVec1.mirrored(floorpnt1)

            floorpnt2 = Geom.Pnt(logoVec2.coord())
            floorpnt1 = Geom.Pnt(logoVec1.coord())

            floorpnt5 = Geom.Pnt(logoVec3.coord())
            floorpnt6 = Geom.Pnt(logoVec4.coord())

            # Translating points for plane creation
            logoPnt1 = floorpnt1.translated(Geom.Vec(Geom.Pnt(floorpnt1.coord()),Geom.Pnt(floorpnt1.x(), floorpnt1.y(),
                                                              floorpnt1.z() + lowerPntsHeight)))
            logoPnt2 = floorpnt2.translated(Geom.Vec(Geom.Pnt(floorpnt2.coord()),Geom.Pnt(floorpnt2.x(), floorpnt2.y(),
                                                              floorpnt2.z() + lowerPntsHeight)))
            logoPnt4 = floorpnt1.translated(Geom.Vec(Geom.Pnt(floorpnt1.coord()),Geom.Pnt(floorpnt1.x(), floorpnt1.y(),
                                                              floorpnt1.z() + upperPntsHeight)))
            logoPnt3 = floorpnt2.translated(Geom.Vec(Geom.Pnt(floorpnt2.coord()),Geom.Pnt(floorpnt2.x(), floorpnt2.y(),
                                                              floorpnt2.z() + upperPntsHeight)))

            logoPnt5 = floorpnt1.translated(Geom.Vec(Geom.Pnt(floorpnt1.coord()), Geom.Pnt(floorpnt5.x(), floorpnt5.y(),
                                                                                        floorpnt5.z() + lowerPntsHeight)))
            logoPnt6 = floorpnt2.translated(Geom.Vec(Geom.Pnt(floorpnt2.coord()), Geom.Pnt(floorpnt6.x(), floorpnt6.y(),
                                                                                        floorpnt6.z() + lowerPntsHeight)))
            logoPnt8 = floorpnt1.translated(Geom.Vec(Geom.Pnt(floorpnt1.coord()), Geom.Pnt(floorpnt5.x(), floorpnt5.y(),
                                                                                        floorpnt5.z() + upperPntsHeight)))
            logoPnt7 = floorpnt2.translated(Geom.Vec(Geom.Pnt(floorpnt2.coord()), Geom.Pnt(floorpnt6.x(), floorpnt6.y(),
                                                                                        floorpnt6.z() + upperPntsHeight)))

            pointList = [logoPnt1, logoPnt2, logoPnt3, logoPnt4]
            logoFace = self._createSubElementFace(pointList)
            pointList = [logoPnt5, logoPnt6, logoPnt7, logoPnt8]
            logoFace2 = self._createSubElementFace(pointList)

            # pointList = self._calcPointsForLogo(polyLine)

            # Setting the texture
            logoFace.setTexture(logoTexture)
            logoFace2.setTexture(logoTexture)
            # Adding subelement
            model.addSubElem(logoFace)
            model.addSubElem(logoFace2)

    def _createBases(self):
        mHeight = self._height.getValue()
        polyLine = PolylineData.fromElement(self._baseData)
        # Cylinders subelements
        for i in range(polyLine.pointCount()):
            # creating cylinders
            cylinder = lx.RightCircularCylinder.createIn(self.getDocument())
            cylinder.setHeight(mHeight)
            cylinder.setRadius(0.07)

            mCylinderSubElem = lx.SubElement.createIn(self.getDocument())
            mCylinderSubElem.setGeometry(cylinder)
            translateVector = Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), polyLine.point(i))
            mCylinderSubElem.translate(translateVector)
            self.addSubElement(mCylinderSubElem)

    def createFence(self, model):
        mHeight = self._height.getValue()
        mColor = self._color.getValue()
        # polyline data
        polyLine = PolylineData.fromElement(self._baseData)

        texture = Draw.Texture2()
        texture.setTextureFileName(lxstr('textures/600/629.png'))

        for i in range(polyLine.pointCount()-1):
            pnt1 = polyLine.point(i)
            pnt2 = polyLine.point(i+1)
            pnt3 = pnt2.translated(Geom.Vec(0.0, 0.0, mHeight))
            pnt4 = pnt1.translated(Geom.Vec(0.0, 0.0, mHeight))

            subFace = self._createSubElementFace([pnt1, pnt2, pnt3, pnt4])
            if self._colorBool.getValue():
                subFace.setDiffuseColor(mColor)
            else:
                subFace.setTexture(texture)
            model.addSubElem(subFace)

            #Adding logo
            # self._createLogos(model)

    def _createGeometry(self):
        # print(">>in _createGeometry()")
        model = ModelAssembler(doc)
        model.beginModel(self)

        self.createFence(model)
        self._createBases()

        model.endModel()

    def _updateGeometry(self):
        # print(">>in _updateGeometry()")
        with EditMode(self.getDocument()):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == FenceElem._heightPropName:
            self.setHeight(self._height.getValue())
        elif aPropertyName == FenceElem._colorPropName:
            self.setColor(self._color.getValue())
        elif aPropertyName == FenceElem._colorBoolPropName:
            self.setColorBool(self._colorBool.getValue())
        elif aPropertyName == FenceElem._logoHeightPropName:
            self.setLogoHeight(self._logoHeight.getValue())
        elif aPropertyName == FenceElem._logoWidthPropName:
            self.setLogoWidth(self._logoWidth.getValue())
        # elif aPropertyName == FenceElem._buttonPropName:
        #     self._onSelectButtonClicked()

if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{86F2B6F6-0803-4A86-B1E4-62F228E900CC}"))
    # Begin creating the Element
    try:
        with EditMode(doc):
            polylineData = pickPolyline(uidoc)
            if polylineData is not None:
                elem = FenceElem(doc)
                elem.setPolylineData(polylineData)
    except Exception as e:
        traceback.print_exc()
    finally:
        doc.recompute()
