# Author: Pavlo Leskovych
# Version: 1.2.8  13.10.2021
# Attributes:
    # Version 1.1:
        # Translations
    # Version 1.2:
        # Ankerkopf, Ankerplatte & other translations
    # Version 1.2.1:
        # Small fix with head plate & nail head intersection
        # Change plate and nail head colour
    # Version 1.2.2:
        # Change class to inherit from BuildingElementProxy
        # Component colour
        # Group Element's properties into PropertySets
    # Version 1.2.3
        # Set the PythonElement as parent
    # Version 1.2.4
        # Set the element colour
    # Version 1.2.5
        # Fixed a wrong rotating position of each part of anchor, some small fixes.
    # Version 1.2.6
        # Added a possibility to modify the distance between nails
    # Version 1.2.7
        # SB: Fixed an issue where the value "self._baseData" was not available after saving and reloading the file
    # Version 1.2.8
        # SB: Property names are case sensitive and MUST not change at all, otherwise the correspondence with the LXZ files used by the user is lost!
    # Version 1.2.9
        # SB: Use "Geom.Vec(self._baseData._startPt, self._baseData._endPt)" in various parts of the script since the value calculated with "startPt" and "endPt" returns an invalid direction when these values are identical.
    # Version 1.3.0
        # SB: Reworked PropertySets

import math
import copy
import traceback
# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI as ui
import OpenLxCmd as cmd
import Base
import Core
import Geom
import Topo
import Draw

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString
doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

# app = lx.Application.getInstance()
# doc = app.getActiveDocument()
# uiapp = ui.UIApplication.getInstance()
# uidoc = uiapp.getUIDocument(doc)

epsilon = 0.0001
maxValue = 10000
pi2 = math.pi * 0.5

property_set_name = "Nail / Injection Parameters"


def qstr(str):
    return Base.StringTool.toQString(lxstr(str))
# Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))


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

            print("Begin editing.")
        else:
            self._exitEditing = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._exitEditing:
            self._doc.endEditing()
            self._doc.recompute()

            print("End editing.")


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


class WireBuilder:
    def __init__(self, doc):
        self._doc = doc
        self._wireData = None

    def beginWire(self, startPt):
        if self._wireData is not None:
            raise RuntimeError("WireBuilder.beginWire() called twice")

        self._wireData = PolylineData.forAssembly(startPt)

    def endWire(self):
        if self._wireData is None:
            raise RuntimeError("WireBuilder.endWire() was called before WireBuilder.beginWire()")

        wireGeom = self._buildGeometry()
        self._wireData = None

        return wireGeom

    def addLineSegment(self, endPt):
        if self._wireData is None:
            raise RuntimeError("WireBuilder.addLineSegment() must be called between WireBuilder.beginWire() and WireBuilder.endWire()")

        self._wireData.appendLineSegment(endPt)

    def addArcSegment(self, middlePt, endPt):
        if self._wireData is None:
            raise RuntimeError("WireBuilder.addLineSegment() must be called between WireBuilder.beginWire() and WireBuilder.endWire()")

        self._wireData.appendArcSegment(middlePt, endPt)

    def _buildGeometry(self):
        if self._wireData is None:
            raise RuntimeError("Wire data is None")

        segmCount = self._wireData.segmentCount()
        if segmCount < 1:
            raise RuntimeError("Wire data has no segments")

        wireCurve = lx.CompositeCurve.createIn(self._doc)

        for segm in range(segmCount):
            segmType = self._wireData.segmentType(segm)
            if segmType == PolylineData.SegmType_Line:
                startPt = self._wireData.segmStartPt(segm)
                endPt = self._wireData.segmEndPt(segm)

                wireCurve.addSegment(lx.createLineSegment(self._doc, startPt, endPt))
            elif segmType == PolylineData.SegmType_Arc:
                startPt = self._wireData.segmStartPt(segm)
                middlePt = self._wireData.segmArc(segm).paramPt(0.5)
                endPt = self._wireData.segmEndPt(segm)

                wireCurve.addSegment(lx.createArc3PointsSegment(doc, startPt, middlePt, endPt))

        return wireCurve


class AnchorOnHorLine(lx.PythonElement):
    _classID = "{5CBAA741-DEA2-4331-9A03-58481C678F5B}"
    _headerPropName = "Anchors on a line"
    _groupPropName = "Anchors on a line properties"

    # Parameters property names
    _nailCountPropName = "_nails_count"
    _distanceBetweenNailsName = "_nails_distance"
    _nailLengthPropName = "_nails_length"
    _nailRadiusPropName = "_nails_radius"
    _bottomLengthPropName = "_nails_injections_length"
    _bottomRadiusPropName = "_nails_injections_radius"
    _anglePropName = "_nails_angle"
    _nailColorName = "_nails_color"
    _injectionColorName = "_nails_injections_color"
    _lineDataPropName = "_lineData"
    _recalculateBtnPropName = "Recalculate"
    _showNailHeadName = "_nails_show_head"
    _nailHeadRadiusName = "_nails_head_radius"
    _nailHeadLengthName = "_nails_head_length"

    _showHeadPlateName = "_nails_show_plate"
    _nailPlateWidthName = "_nails_plate_width"
    _nailPlateHeightName = "_nails_plate_height"
    _nailPlateThicknessName = "_nails_plate_thickness"

    class BaseData:
        def __init__(self, startPt, endPt):
            self._startPt = startPt
            self._endPt = endPt
            if (startPt is None) or (endPt is None):
                raise RuntimeError("Start point or end point is NULL.")

            self._uVec = None
            self._vVec = None
            self._updateBasisVecs()

        def _updateBasisVecs(self):
            self._uVec = Geom.Vec(self._startPt, self._endPt)
            self._uVec.normalize()

            self._vVec = Geom.Vec(-self._uVec.y(), self._uVec.x(), 0.0)

        def baseLength(self):
            return self._startPt.distance(self._endPt)

        def localCS(self):
            return CoordSystem2D(self._startPt, self._uVec, self._vVec)

        def writeString(self):
            outStr = "{};{};{};{};{};{}".format(
                self._startPt.x(), self._startPt.y(), self._startPt.z(),
                self._endPt.x(), self._endPt.y(), self._endPt.z()
            )

            return outStr

        @staticmethod
        def readString(dataStr):
            splitStr = dataStr.split(";")
            if len(splitStr) != 6:  # There should be two 3D points
                return None

            try:
                parsedData = [float(s) for s in splitStr]

                startPt = Geom.Pnt(parsedData[0], parsedData[1], parsedData[2])
                endPt = Geom.Pnt(parsedData[3], parsedData[4], parsedData[5])

                return AnchorOnHorLine.BaseData(startPt, endPt)
            except ValueError:
                return None

        @property
        def endPt(self):
            return self._endPt

    def getGlobalClassId(self):
        return Base.GlobalId(AnchorOnHorLine._classID)

    def getScriptVersion(self):
        return 130  # Version 1.3.0

    def __init__(self, aArg):
        lx.PythonElement.__init__(self, aArg)
        self.registerPythonClass("AnchorOnHorLine", "OpenLxApp.PythonElement")

        # Register properties
        self.setPropertyHeader(lxstr(AnchorOnHorLine._headerPropName), -1)
        self.setPropertyGroupName(lxstr(AnchorOnHorLine._groupPropName), -1)

        self._distanceBetweenNails = self.registerPropertyDouble(AnchorOnHorLine._distanceBetweenNailsName,
                                                                 0.5, lx.Property.VISIBLE,
                                                                 lx.Property.EDITABLE, 570)
        self._nailCount = self.registerPropertyInteger(AnchorOnHorLine._nailCountPropName, 3, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 26)
        self._nailLength = self.registerPropertyDouble(AnchorOnHorLine._nailLengthPropName, 5.0, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 27)
        self._nailRadius = self.registerPropertyDouble(AnchorOnHorLine._nailRadiusPropName, 0.075, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 28)
        self._showNailHead = self.registerPropertyEnum(self._showNailHeadName, 0,
                                                       lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 17)
        self._showNailHead.setEmpty()
        self._showNailHead.addEntry(lxstr("Yes"), -1)
        self._showNailHead.addEntry(lxstr("No"), -1)

        self._nailHeadRadius = self.registerPropertyDouble(AnchorOnHorLine._nailHeadRadiusName, 0.10,
                                                           lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 20)
        self._nailHeadLength = self.registerPropertyDouble(AnchorOnHorLine._nailHeadLengthName, 0.25,
                                                           lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 19)

        self._showHeadPlate = self.registerPropertyEnum(self._showHeadPlateName, 0,
                                                        lx.Property.VISIBLE,
                                                        lx.Property.EDITABLE, 18)
        self._showHeadPlate.setEmpty()
        self._showHeadPlate.addEntry(lxstr("Yes"), -1)
        self._showHeadPlate.addEntry(lxstr("No"), -1)
        self._nailPlateWidth = self.registerPropertyDouble(AnchorOnHorLine._nailPlateWidthName, 0.40,
                                                           lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 23)
        self._nailPlateHeight = self.registerPropertyDouble(AnchorOnHorLine._nailPlateHeightName, 0.40,
                                                            lx.Property.VISIBLE,
                                                            lx.Property.EDITABLE, 24)
        self._nailPlateThickness = self.registerPropertyDouble(AnchorOnHorLine._nailPlateThicknessName, 0.05,
                                                               lx.Property.VISIBLE,
                                                               lx.Property.EDITABLE, 25)
        self._bottomLength = self.registerPropertyDouble(AnchorOnHorLine._bottomLengthPropName, 1.0, lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, 29)
        self._bottomRadius = self.registerPropertyDouble(AnchorOnHorLine._bottomRadiusPropName, 0.12, lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, 30)
        self._angle = self.registerPropertyDouble(AnchorOnHorLine._anglePropName, 0.0, lx.Property.VISIBLE,
                                                  lx.Property.EDITABLE, 31)
        self._nailColor = self.registerPropertyColor(AnchorOnHorLine._nailColorName, Base.Color_fromCdwkColor(34),
                                                     lx.Property.VISIBLE,
                                                     lx.Property.EDITABLE, 32)
        self._injectionColor = self.registerPropertyColor(AnchorOnHorLine._injectionColorName,
                                                          Base.Color_fromCdwkColor(110),
                                                          lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, 33)
        self._recalcBtn = self.registerPropertyButton(AnchorOnHorLine._recalculateBtnPropName, lx.Property.VISIBLE,
                                                      lx.Property.EDITABLE, 34)
        self._lineData = self.registerPropertyString(AnchorOnHorLine._lineDataPropName, lxstr(""),
                                                     lx.Property.NOT_VISIBLE,
                                                     lx.Property.NOT_EDITABLE,
                                                     -1)

        self._baseData = None
        baseDataStr = cstr(self._lineData.getValue())
        self._baseData = AnchorOnHorLine.BaseData.readString(baseDataStr)

        self.setupHeadEnum()
        self.setupPlateEnum()
        self._setAllSteps()
        
        self._insidePropUpdate = False

    def _setAllSteps(self):
        self._nailRadius.setSteps(0.05)
        self._nailLength.setSteps(0.1)
        self._bottomLength.setSteps(0.1)
        self._bottomRadius.setSteps(0.1)
        self._angle.setSteps(5.0)
        self._nailHeadLength.setSteps(0.1)
        self._nailHeadRadius.setSteps(0.1)
        self._nailPlateThickness.setSteps(0.1)
        self._nailPlateHeight.setSteps(0.1)
        self._nailPlateWidth.setSteps(0.1)

    def setupHeadEnum(self):
        if self._showNailHead.getValue() == 0:
            self._nailHeadLength.setVisible(True)
            self._nailHeadRadius.setVisible(True)
        elif self._showNailHead.getValue() is 1:
            self._nailHeadLength.setVisible(False)
            self._nailHeadRadius.setVisible(False)

    def setupPlateEnum(self):
        if self._showHeadPlate.getValue() == 0:
            self._nailPlateWidth.setVisible(True)
            self._nailPlateHeight.setVisible(True)
            self._nailPlateThickness.setVisible(True)
        elif self._showHeadPlate.getValue() is 1:
            self._nailPlateWidth.setVisible(False)
            self._nailPlateHeight.setVisible(False)
            self._nailPlateThickness.setVisible(False)

    # Recalculation button
    def _on_Recalculate_Button_clicked(self):
        try:
            print("Recalculate button pressed...")
            with EditMode(doc):
                line = pickLine(uidoc)
                if line is not None:
                    printVec("line[0]", line[0])
                    printVec("line[1]", line[1])

                self.setBaseLine(line[0], line[1])
        except Exception as e:
            traceback.print_exc()
        finally:
            doc.recompute()

    @staticmethod
    def buildSubElemLine(aFromPnt, aToPnt, startPt, endPt):
        res = Geom.Vec(aToPnt.xyz() - aFromPnt.xyz())
        dir = Geom.Dir(res.normalized())
        line = lx.Line.createIn(doc)
        line.setPoint(aFromPnt)
        line.setDirection(dir)
        tc = lx.TrimmedCurve.createIn(doc)
        tc.setBasisCurve(line)
        tc.setTrim1(0)
        tc.setTrim2(res.magnitude())
        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(tc)
        elem.setDiffuseColor(Base.Color(0, 0, 0))
        # Creating Ax2 for local placement...
        vec = Geom.Vec(self._baseData._startPt, self._baseData._endPt)
        locAxis = Geom.Ax2(startPt, Geom.Dir(vec))

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

    def setNailCount(self, param):
        # width = self._calcWidthBetweenNails()
        startPnt = self._baseData._startPt
        endPnt = self._baseData._endPt

        nailCount = self._nailCount.getValue()
        cursor = Geom.Vec(startPnt, endPnt)
        magnitude = cursor.magnitude()

        epsilon = 0
        maxValue = self._nailCount.getValue()

        with EditMode(self.getDocument()):
            self._nailCount.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setShowHead(self, param):
        with EditMode(self.getDocument()):
            self._showNailHead.setValue(param)
            self._updateGeometry()
            self.setupHeadEnum()

    def setShowPlate(self, param):
        with EditMode(self.getDocument()):
            self._showHeadPlate.setValue(param)
            self._updateGeometry()
            self.setupPlateEnum()

    def setDistanceBetweenNails(self, param):
        epsilon = self._nailRadius.getValue() * 2
        with EditMode(self.getDocument()):
            self._distanceBetweenNails.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setNailHeadRadius(self, param):
        epsilon = self._nailRadius.getValue()
        with EditMode(self.getDocument()):
            self._nailHeadRadius.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setNailHeadLength(self, param):
        with EditMode(self.getDocument()):
            self._nailHeadLength.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setNailPlateWidth(self, param):
        epsilon = self._nailHeadRadius.getValue()
        with EditMode(self.getDocument()):
            self._nailPlateWidth.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setNailPlateHeight(self, param):
        # epsilon = self._nailPlateHeight.getValue()
        with EditMode(self.getDocument()):
            self._nailPlateHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setNailPlateThickness(self, param):
        with EditMode(self.getDocument()):
            self._nailPlateThickness.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setNailRadius(self, param):
        maxValue = self._bottomRadius.getValue() - epsilon
        with EditMode(self.getDocument()):
            self._nailRadius.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        cmd.CmdSetPropertySetDefinition(property_set_name, "Nail Radius", self._nailRadius.getValue(), self).redo()  # Update PropertySet
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big, try to change the "
                                                      "\"Bottom Radius\" parameter"))

    def setNailLength(self, param):
        epsilon = self._bottomLength.getValue()
        with EditMode(self.getDocument()):
            self._nailLength.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        cmd.CmdSetPropertySetDefinition(property_set_name, "Nail Length", self._nailLength.getValue(), self).redo()  # Update PropertySet
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setBottomLength(self, param):
        epsilon = 0.000
        maxValue = self._nailLength.getValue()
        with EditMode(self.getDocument()):
            self._bottomLength.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        cmd.CmdSetPropertySetDefinition(property_set_name, "Injection Length", self._bottomLength.getValue(), self).redo()  # Update PropertySet
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setBottomRadius(self, param):
        with EditMode(self.getDocument()):
            self._bottomRadius.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        cmd.CmdSetPropertySetDefinition(property_set_name, "Injection Radius", self._bottomRadius.getValue(), self).redo()  # Update PropertySet
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setAngle(self, param):
        epsilon = -359.999
        maxValue = 359.999
        with EditMode(self.getDocument()):
            self._angle.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        cmd.CmdSetPropertySetDefinition(property_set_name, "Angle", self._angle.getValue(), self).redo()  # Update PropertySet
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setNailColor(self, param):
        with EditMode(self.getDocument()):
            self._nailColor.setValue(param)
            self._updateGeometry()

    def setInjectionColor(self, param):
        with EditMode(self.getDocument()):
            self._injectionColor.setValue(param)
            self._updateGeometry()

    def _calcWidthBetweenNails(self):
        nailCount = self._nailCount.getValue()
        line = pickLine(uidoc)
        vec = Geom.Vec2d(line[0], line[1])
        magn = vec.magnitude()
        width = magn / nailCount
        return width

    def _createNail(self, startPt, endPt, last):
        nail_rad = self._nailRadius.getValue()
        nail_len = self._nailLength.getValue()
        angle = math.radians(self._angle.getValue())
        color = self._nailColor.getValue()

        profile = lx.CircleProfileDef.createIn(doc)
        profile.setRadius(nail_rad)
        eas = lx.ExtrudedAreaSolid.createIn(doc)
        eas.setSweptArea(profile)
        eas.setExtrudedDirection(Geom.Dir(0, 0, -1))
        eas.setDepth(nail_len)

        nailElem = lx.SubElement.createIn(doc)
        nailElem.setGeometry(eas)
        nailElem.setDiffuseColor(color)

        rotVec = Geom.Vec(self._baseData._startPt, self._baseData._endPt)
        rotateAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(rotVec))

        positionAngle = math.radians(90.0)
        nailElem.rotate(rotateAxis, -(angle + positionAngle), Geom.CoordSpace_WCS)

        dirVec = Geom.Vec(self._baseData._startPt, self._baseData._endPt)
        rotatedZVec = Geom.Vec(Geom.Pnt(0, 0, 0), Geom.Pnt(0, 0, 1))
        rotatedZVec.rotate(rotateAxis, -(angle + positionAngle))
        zDir = Geom.Dir(rotatedZVec)
        if last:
            localAxis = Geom.Ax2(endPt, zDir, Geom.Dir(dirVec))
        else:
            localAxis = Geom.Ax2(startPt, zDir, Geom.Dir(dirVec))

        nailElem.setLocalPlacement(localAxis)

        self.addSubElement(nailElem)

    def _createHead(self, startPt, endPt, last):
        head_radius = self._nailHeadRadius.getValue()
        head_length = self._nailHeadLength.getValue()
        angle = math.radians(self._angle.getValue())

        if self._showNailHead.getValue() == 0:
            #  Head profile creation
            head_profile = lx.CircleProfileDef.createIn(doc)
            head_profile.setRadius(head_radius)
            eas2 = lx.ExtrudedAreaSolid.createIn(doc)
            eas2.setSweptArea(head_profile)
            eas2.setExtrudedDirection(Geom.Dir(0, 0, 1))
            eas2.setDepth(head_length)
            headElem = lx.SubElement.createIn(doc)
            headElem.setGeometry(eas2)
            headElem.setDiffuseColor(Base.Color_fromCdwkColor(123))
            rotVec = Geom.Vec(self._baseData._startPt, self._baseData._endPt)
            rotateAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(rotVec))

            positionAngle = math.radians(90.0)
            headElem.rotate(rotateAxis, -(angle + positionAngle), Geom.CoordSpace_WCS)

            dirVec = Geom.Vec(self._baseData._startPt, self._baseData._endPt)
            rotatedZVec = Geom.Vec(Geom.Pnt(0, 0, 0), Geom.Pnt(0, 0, 1))
            rotatedZVec.rotate(rotateAxis, -(angle + positionAngle))
            zDir = Geom.Dir(rotatedZVec)
            if last:
                localAxis = Geom.Ax2(endPt, zDir, Geom.Dir(dirVec))
            else:
                localAxis = Geom.Ax2(startPt, zDir, Geom.Dir(dirVec))

            headElem.setLocalPlacement(localAxis)

            self.addSubElement(headElem)
        else:
            return

    def _createPlate(self, startPt, endPt, last):
        plate_width = self._nailPlateWidth.getValue()
        plate_height = self._nailPlateHeight.getValue()
        plate_thickness = self._nailPlateThickness.getValue()
        angle = math.radians(self._angle.getValue())

        if self._showHeadPlate.getValue() == 0:
            #  Head plate creation
            plate_profile = lx.RectangleProfileDef.createIn(doc)
            plate_profile.setXDim(plate_width)
            plate_profile.setYDim(plate_height)
            eas3 = lx.ExtrudedAreaSolid.createIn(doc)
            eas3.setSweptArea(plate_profile)
            eas3.setExtrudedDirection(Geom.Dir(0, 0, -1))
            eas3.setDepth(plate_thickness)
            plateElem = lx.SubElement.createIn(doc)
            plateElem.setGeometry(eas3)
            plateElem.setDiffuseColor(Base.Color_fromCdwkColor(126))
            rotVec = Geom.Vec(self._baseData._startPt, self._baseData._endPt)
            rotateAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(rotVec))

            positionAngle = math.radians(90.0)
            plateElem.rotate(rotateAxis, -(angle + positionAngle), Geom.CoordSpace_WCS)

            dirVec = Geom.Vec(self._baseData._startPt, self._baseData._endPt)
            rotatedZVec = Geom.Vec(Geom.Pnt(0, 0, 0), Geom.Pnt(0, 0, 1))
            rotatedZVec.rotate(rotateAxis, -(angle + positionAngle))
            zDir = Geom.Dir(rotatedZVec)
            if last:
                localAxis = Geom.Ax2(endPt, zDir, Geom.Dir(dirVec))
            else:
                localAxis = Geom.Ax2(startPt, zDir, Geom.Dir(dirVec))

            plateElem.setLocalPlacement(localAxis)

            self.addSubElement(plateElem)
        else:
            return

    def _createBottom(self, startPt, endPt, last):
        nail_rad = self._nailRadius.getValue()
        nail_len = self._nailLength.getValue()
        bot_rad = self._bottomRadius.getValue()
        bot_len = self._bottomLength.getValue()
        angle = math.radians(self._angle.getValue())
        color = self._injectionColor.getValue()

        internCylinder = lx.RightCircularCylinder.createIn(doc)
        internCylinder.setHeight(bot_len)
        internCylinder.setRadius(nail_rad)
        intElement = lx.Element.createIn(doc)
        intElement.setGeometry(internCylinder)
        print("Created intern Cylinder...")

        externCylinder = lx.RightCircularCylinder.createIn(doc)
        externCylinder.setHeight(bot_len)
        externCylinder.setRadius(bot_rad)
        extElement = lx.Element.createIn(doc)
        extElement.setGeometry(externCylinder)

        resultingCylinders = lx.vector_Element()
        if lx.bop_cut(extElement, intElement, resultingCylinders) != 0:
            print("Error in cut")

        transform = resultingCylinders[0].getTransform()
        geometry = resultingCylinders[0].getGeometry()
        # doc.removeObject(resultingCylinders)

        doc.removeObject(intElement)
        doc.removeObject(extElement)

        botElem = lx.SubElement.createIn(doc)
        botElem.setTransform(transform)
        botElem.setGeometry(geometry)
        botElem.setDiffuseColor(color)

        rotVec = Geom.Vec(self._baseData._startPt, self._baseData._endPt)
        rotateAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(rotVec))
        positionAngle = math.radians(90.0)

        dirVec = Geom.Vec(self._baseData._startPt, self._baseData._endPt)
        rotatedZVec = Geom.Vec(Geom.Pnt(0, 0, 0), Geom.Pnt(0, 0, 1))
        rotatedZVec.rotate(rotateAxis, -(angle + positionAngle))
        zDir = Geom.Dir(rotatedZVec)
        if last:
            localAxis = Geom.Ax2(endPt, zDir, Geom.Dir(dirVec))
        else:
            localAxis = Geom.Ax2(startPt, zDir, Geom.Dir(dirVec))

        botElem.setLocalPlacement(localAxis)
        botElem.translate(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(0.0, 0.0, -nail_len)), Geom.CoordSpace_LCS)
        self.addSubElement(botElem)

    def _generateAnchor(self, startPt, endPt, last):
        # width = self._calcWidthBetweenNails()

        if self._bottomLength.getValue() > epsilon:
            self._createNail(startPt, endPt, last)
            self._createBottom(startPt, endPt, last)
            self._createHead(startPt, endPt, last)
            self._createPlate(startPt, endPt, last)
        else:
            self._createNail(startPt, endPt, last)
            self._createHead(startPt, endPt, last)
            self._createPlate(startPt, endPt, last)

    def _updateGeometry(self):
        print(__name__)
        # width = self._calcWidthBetweenNails()
        startPnt = self._baseData._startPt
        endPnt = self._baseData._endPt

        nailCount = self._nailCount.getValue()
        cursor = Geom.Vec(startPnt, endPnt)
        magnitude = cursor.magnitude()
        scaleRatio = self._distanceBetweenNails.getValue()
        scaleStep = self._distanceBetweenNails.getValue()

        with EditMode(doc):
            self.removeSubElements()

            if self._baseData is not None:

                if nailCount > 1:
                    print("Nail Count: {}".format(nailCount))
                    for place in range(nailCount):
                        if place is 0:
                            self._generateAnchor(startPnt, endPnt, False)

                        elif place >= 1:
                            cursor.normalize()
                            cursor.scale(scaleRatio)
                            scaleRatio += scaleStep
                            pnt = startPnt.translated(cursor)
                            self._generateAnchor(pnt, endPnt, False)
            else:
                raise RuntimeError('_BaseData is None.')

    def onPropertyChanged(self, aPropertyName):
        print(aPropertyName)
        if aPropertyName == AnchorOnHorLine._nailRadiusPropName:
            self.setNailRadius(self._nailRadius.getValue())
        elif aPropertyName == AnchorOnHorLine._nailLengthPropName:
            self.setNailLength(self._nailLength.getValue())
        elif aPropertyName == AnchorOnHorLine._bottomRadiusPropName:
            self.setBottomRadius(self._bottomRadius.getValue())
        elif aPropertyName == AnchorOnHorLine._bottomLengthPropName:
            self.setBottomLength(self._bottomLength.getValue())
        elif aPropertyName == AnchorOnHorLine._anglePropName:
            self.setAngle(self._angle.getValue())
        elif aPropertyName == AnchorOnHorLine._nailCountPropName:
            self.setNailCount(self._nailCount.getValue())
        elif aPropertyName == AnchorOnHorLine._recalculateBtnPropName:
            self._on_Recalculate_Button_clicked()
        elif aPropertyName == AnchorOnHorLine._nailColorName:
            self.setNailColor(self._nailColor.getValue())
        elif aPropertyName == AnchorOnHorLine._injectionColorName:
            self.setInjectionColor(self._injectionColor.getValue())
        elif aPropertyName == AnchorOnHorLine._nailHeadRadiusName:
            self.setNailHeadRadius(self._nailHeadRadius.getValue())
        elif aPropertyName == AnchorOnHorLine._nailHeadLengthName:
            self.setNailHeadLength(self._nailHeadLength.getValue())
        elif aPropertyName == AnchorOnHorLine._nailPlateWidthName:
            self.setNailPlateWidth(self._nailPlateWidth.getValue())
        elif aPropertyName == AnchorOnHorLine._nailPlateHeightName:
            self.setNailPlateHeight(self._nailPlateHeight.getValue())
        elif aPropertyName == AnchorOnHorLine._nailPlateThicknessName:
            self.setNailPlateThickness(self._nailPlateThickness.getValue())
        elif aPropertyName == AnchorOnHorLine._showNailHeadName:
            self.setShowHead(self._showNailHead.getValue())
        elif aPropertyName == AnchorOnHorLine._showHeadPlateName:
            self.setShowPlate(self._showHeadPlate.getValue())
        elif aPropertyName == AnchorOnHorLine._distanceBetweenNailsName:
            self.setDistanceBetweenNails(self._distanceBetweenNails.getValue())

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(doc):
            if not Geom.GeomTools.isEqual(x, 1.):
                pass
            if not Geom.GeomTools.isEqual(y, 1.):
                pass
            if not Geom.GeomTools.isEqual(z, 1.):
                pass

            self.translateAfterScaled(aVec, aScaleBasePnt)

    def setBaseLine(self, startPt, endPt):
        if not self._insidePropUpdate:
            self._insidePropUpdate = True

            self._baseData = AnchorOnHorLine.BaseData(startPt, endPt)
            self._lineData.setValue(lxstr(self._baseData.writeString()))
            self._updateGeometry()

            self._insidePropUpdate = False


def pickLineElement(uidoc):
    uidoc.highlightByShapeType(Topo.ShapeType_WIRE)
    ok = uidoc.pickPoint()
    uidoc.stopHighlightByShapeType()

    if ok:
        return uidoc.getPickedElement()
    else:
        return None


def extractBasePoints(lineElem):
    linePtsList = Geom.vector_Pnt()
    Topo.ShapeTool.getVerticesAsPoints(lineElem.getShape(), linePtsList)

    if len(linePtsList) >= 2:
        return [Geom.Pnt(linePtsList[0]), Geom.Pnt(linePtsList[1])]
    return None


def pickLine(uidoc):
    ui.showStatusBarMessage(lxstr("[L] Select base line [Esc] Cancel"))
    lineElem = pickLineElement(uidoc)
    ui.showStatusBarMessage(lxstr(""))

    if lineElem is not None:
        return extractBasePoints(lineElem)
        # lineElem
    else:
        return None


if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{4408120F-CC52-4B4F-ACDB-3CBC3FD5AA3A}"))

    try:
        with EditMode(doc):
            line = pickLine(uidoc)
            if line is not None:
                printVec("line[0]", line[0])
                printVec("line[1]", line[1])

                anchorsOnLineElement = AnchorOnHorLine(doc)
                anchorsOnLineElement.setBaseLine(line[0], line[1])
        with EditMode(doc):
            anchorsOnLineElement.setDiffuseColor(Base.Color_fromCdwkColor(41))

        # Creating PropertySets
        cmd.CmdSetPropertySetDefinition(property_set_name, "Angle", anchorsOnLineElement._angle.getValue(), anchorsOnLineElement).redo()
        cmd.CmdSetPropertySetDefinition(property_set_name, "Nail Length", anchorsOnLineElement._nailLength.getValue(), anchorsOnLineElement).redo()
        cmd.CmdSetPropertySetDefinition(property_set_name, "Nail Radius", anchorsOnLineElement._nailRadius.getValue(), anchorsOnLineElement).redo()
        cmd.CmdSetPropertySetDefinition(property_set_name, "Injection Length", anchorsOnLineElement._bottomLength.getValue(), anchorsOnLineElement).redo()
        cmd.CmdSetPropertySetDefinition(property_set_name, "Injection Radius", anchorsOnLineElement._bottomRadius.getValue(), anchorsOnLineElement).redo()
    except Exception as e:
        traceback.print_exc()
    finally:
        doc.recompute()
