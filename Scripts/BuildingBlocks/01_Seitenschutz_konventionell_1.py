# coding=utf-8
# OpenLexocad libraries
"""
ifcRailing
attributes
    version 1.0
        - height
        - length
        - width
        - color
        - cwColor = 2100
    version 2.0 (27.01.2021)
        - width
        - height
        - line length(not editable)
        - representation(Axis, SolidModel)
    version 3.0 (03.02.2021)
        - width
        - height
        - line length
        - representation(Axis, SolidModel)
        - line position:
            - left
            - center
            - right
        - representation(Axis, SolidModel)


========================================
====  Supported by Roman Davydiuk   ====
====  Mail: davydjukroman@gmail.com ====
====  Skype: live:davydjukroman     ====
========================================

"""

import math

import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd
import Base, Core, Draw, Geom, Topo

import time, traceback

lxStr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

st = Topo.ShapeTool

# doc = lx.Application.getInstance().getActiveDocument()
# uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
# sel = uidoc.getSelection()

GUID_CLASS = Base.GlobalId("{84B7A068-2ACB-4A60-BBEF-A1A69DB6403E}")
GUID_SCRPT = Base.GlobalId("{5FE5853E-B33C-44F1-91F7-E1F15D2F110C}")
CW_COLOR = 3100
element_color = Base.Color(255, 51, 0)

epsilon = 0.0001
eps_DS = 0.001
pi2 = math.pi * 0.5


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
                raise RuntimeError("Unsupported edge type")

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


class DataStruct:
    def __init__(self, start_pnt, end_pnt, width, height, line_position, str_norm, end_norm, transform):
        self.start_pnt = start_pnt
        self.end_pnt = end_pnt
        self.width = width
        self.height = height
        self.line_position = line_position

        self.strNorm = str_norm
        self.endNorm = end_norm
        self.transform = transform

        self.length = Geom.Vec(self.start_pnt, self.end_pnt).magnitude()
        self.strNorm_LCS = str_norm.transformed(transform.inverted())
        self.endNorm_LCS = end_norm.transformed(transform.inverted())

    # def _invertToLCS(self):
    #     strPt = self.strPt
    #     endPt = self.endPt
    # equality v == u
    def __eq__(self, other):
        equality = True

        if abs(self.length - other.length) > eps_DS:
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


class SegmentBuilder:
    def __init__(self, doc):
        self._doc = doc

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
        beam_rez = lx.Element.createIn(self._doc)
        beam_rez.setGeometry(geom)
        beam_rez.setTransform(t)
        self._doc.removeObject(beam_vec[0])

        return beam_rez

    # def getCutBeam(self, beamType, startPt, endPt, radiusH, radiusV, startVec, endVec, beam_trsf):
    def getCutBeam(self, data):
        """
        data.start_pnt
        data.end_pnt
        data.width
        data.height
        data.line_position
        data.strNorm
        data.endNorm
        data.transform
        """

        startPt = data.start_pnt
        endPt = data.end_pnt
        width = data.width

        startNorm = data.strNorm
        endNorm = data.endNorm
        beam_transform = data.transform
        slope_angle = Geom.Vec(startPt, endPt).angle(Geom.Vec(startPt, Geom.Pnt(endPt.x(), endPt.y(), startPt.z())))
        print(f"Vector angle is {slope_angle}")
        height = data.height * math.cos(slope_angle) if slope_angle > 0.01 else data.height
        line_position = data.line_position
        if line_position == 0:  # left
            position_retreat = 0.0
        elif line_position == 1:  # right
            position_retreat = -width
        else:  # center
            position_retreat = -width * 0.5
        print("position_retreat:", position_retreat)
        length = data.length

        beamVec = Geom.Vec(startPt, endPt)
        dir = beamVec.normalized()
        beamLen = [2. * height, length, 2. * height]

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

        position = Geom.Ax2(Geom.Pnt(-beamLen[0], position_retreat, 0.0), Geom.Dir(0, 0, 1))

        beamGeom = lx.Block.createIn(self._doc)
        beamGeom.setLength(sum(beamLen))
        beamGeom.setWidth(width)
        beamGeom.setHeight(height)
        beamGeom.setPosition(position)

        element = lx.Element.createIn(self._doc)
        element.setGeometry(beamGeom)
        element.setTransform(beam_transform)

        if bool_endNorm:
            element = self._splitBeamByPlane(element, endPt, endNorm)
        if bool_startNorm:
            element = self._splitBeamByPlane(element, startPt, startNorm)

        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(element.getGeometry())
        beam.setTransform(element.getTransform())
        beam.setDiffuseColor(element_color)

        # clean elements

        # doc.removeObject(h_elements)
        self._doc.removeObject(element)
        return beam


class Seitenschutz01(lx.Railing):
    _propHeader = "_01SeitenschutzKonventionell"
    _propGroupName = "_01SeitenschutzKonventionellProperties"

    _widthPropName = "_width"
    _heightPropName = "_height"
    _lineLengthName = "_length"
    _linePositionPropName = "_linePosition"
    _representationPropName = "_representation"

    _polylineParamName = "Polyline"
    _polylineIDPropName = "PolylineID"

    def __init__(self, aArg):
        lx.Railing.__init__(self, aArg)
        self.registerPythonClass("Seitenschutz01", "OpenLxApp.Railing")

        self._insidePropUpdate = False

        self.setPropertyHeader(lxStr(Seitenschutz01._propHeader), 512)
        self.setPropertyGroupName(lxStr(Seitenschutz01._propGroupName), 513)

        self._width = self.registerPropertyDouble(Seitenschutz01._widthPropName,
                                                  0.2,
                                                  lx.Property.VISIBLE,
                                                  lx.Property.EDITABLE,
                                                  502)

        self._height = self.registerPropertyDouble(Seitenschutz01._heightPropName,
                                                   1.0,
                                                   lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE,
                                                   503)

        self._lineLength = self.registerPropertyDouble(self._lineLengthName, 3.0, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 505)

        self._linePosition = self.registerPropertyEnum(self._linePositionPropName, 0, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 566)
        self._linePosition.setEmpty()
        self._linePosition.addEntry(lxStr("Left"), 567)
        self._linePosition.addEntry(lxStr("Right"), 568)
        self._linePosition.addEntry(lxStr("Center"), 569)

        self._representation = self.registerPropertyEnum(self._representationPropName, 1, lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, 506)
        self._representation.setEmpty()
        self._representation.addEntry(lxStr("Axis"), 509)  # Index 0
        self._representation.addEntry(lxStr("SolidModel"), 508)  # Index 1

        self._polyline = self.registerPropertyString(self._polylineParamName, lxStr(""), lx.Property.NOT_VISIBLE,
                                                     lx.Property.NOT_EDITABLE, -1)  # NOT_VISIBLE
        self._polylineID = self.registerPropertyString(self._polylineIDPropName, lxStr(""), lx.Property.NOT_VISIBLE,
                                                       lx.Property.NOT_EDITABLE, -1)

        self.set_steps()
        self.setBoundingBoxEnabled(False)
        

    def set_steps(self):
        self._width.setSteps(0.1)
        self._height.setSteps(0.1)

    def _place_segment_on_line(self, start_pnt, end_pnt, start_vecs, end_vecs, builder):
        startVec1 = start_vecs[1]
        endVec1 = end_vecs[1]
        segmVec = Geom.Vec(start_pnt, end_pnt)
        segmBase = segmVec.normalized()
        # start making transform: Matrix and translationPart
        e_x = Geom.Vec(segmBase.x(), segmBase.y(), segmBase.z())
        e_y = Geom.Vec(-segmBase.y(), segmBase.x(), 0.0).normalized()
        e_z = e_x.crossed(e_y).normalized()

        e1 = Geom.XYZ(e_x.x(), e_x.y(), e_x.z())
        e2 = Geom.XYZ(e_y.x(), e_y.y(), e_y.z())
        e3 = Geom.XYZ(e_z.x(), e_z.y(), e_z.z())
        M = Geom.Mat(e1, e2, e3)
        loc = Geom.XYZ(start_pnt.x(), start_pnt.y(), start_pnt.z())
        scale_factor = 1.0
        transform = Geom.Trsf(M, loc, scale_factor)

        # finish making transform
        width = self._width.getValue()
        height = self._height.getValue()

        data_struct = DataStruct(start_pnt, end_pnt,
                                 width, height, self._linePosition.getValue(),
                                 startVec1, endVec1, transform)
        beam = builder.getCutBeam(data_struct)
        self.addSubElement(beam)

    def _getStartVector(self, polyLine, segmId):
        isFirst = bool(segmId == 0)
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
                curVec.setZ(0)
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            elif segmType == PolylineData.SegmType_Arc:
                arc = polyLine.segmArc(segmId)
                curVec = arc.startTangent()
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            preSegmType = polyLine.segmentType(segmId - 1)
            if preSegmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(segmId - 1)
                endPt = polyLine.segmEndPt(segmId - 1)
                preVec = Geom.Vec(startPt, endPt)
                preVec.setZ(0)
                preVec.normalize()
                preNor = Geom.Vec(-preVec.y(), preVec.x(), 0.0)
            elif preSegmType == PolylineData.SegmType_Arc:
                preArc = polyLine.segmArc(segmId - 1)
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
        # isFirst = bool(segmId == 0)
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
                curVec.setZ(0)
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)
            elif segmType == PolylineData.SegmType_Arc:
                arc = polyLine.segmArc(segmId)
                curVec = arc.endTangent()
                curVec.normalize()
                curNor = Geom.Vec(-curVec.y(), curVec.x(), 0.0)

            nexSegmType = polyLine.segmentType(segmId + 1)
            if nexSegmType == PolylineData.SegmType_Line:
                startPt = polyLine.segmStartPt(segmId + 1)
                endPt = polyLine.segmEndPt(segmId + 1)
                nexVec = Geom.Vec(startPt, endPt)
                nexVec.setZ(0)
                nexVec.normalize()
                nexNor = Geom.Vec(-nexVec.y(), nexVec.x(), 0.0)
            elif nexSegmType == PolylineData.SegmType_Arc:
                nexArc = polyLine.segmArc(segmId + 1)
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

    def _placeSegment(self, polyLine, segmId):
        builder = SegmentBuilder(self.getDocument())

        start_pnt = polyLine.segmStartPt(segmId)
        end_pnt = polyLine.segmEndPt(segmId)
        startVecs = self._getStartVector(polyLine, segmId)
        endVecs = self._getEndVector(polyLine, segmId)
        self._place_segment_on_line(start_pnt, end_pnt, startVecs, endVecs, builder)

    def _placeSegmentsAccLine(self, polyLine):
        segmCount = polyLine.segmentCount()
        if segmCount <= 0:
            return

        # print("segmCount = ", segmCount)
        for segmId in range(segmCount):
            self._placeSegment(polyLine, segmId)

    def createCompound(self):
        axisCurve = self.getAxisRepresentation()
        print(axisCurve)
        polyLine = PolylineData.fromElement(self.getPolylineData(axisCurve))
        self._placeSegmentsAccLine(polyLine)
        self.setLineLength(polyLine)

    def calculateLength(self, polyLine):
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

    def setLineLength(self, polyline):
        try:
            length = self.calculateLength(polyline)
            with EditMode(self.getDocument()):
                self._lineLength.setValue(length)
            # print(f"Line length = {length}")
        except Exception as err:
            print(f"{err.__class__.__name__}: {err}")

    def _updateGeometry(self):
        doc = self.getDocument()
        with EditMode(doc):
            # self.removeSubElements()
            self.removeSubElements_exceptLine()
            self.createCompound()

    def removeSubElements_exceptLine(self):
        sub_elems = self.getSubElements()
        lineGlobID = Base.GlobalId(self._polylineID.getValue())
        for i in range(len(sub_elems)):
            if sub_elems[i].getGlobalId() != lineGlobID:
                self.removeSubElement(sub_elems[i])

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

        return lineData

    def setWidth(self, width):
        with EditMode(self.getDocument()):
            self._width.setValue(width)
            self._updateGeometry()

    def setHeight(self, height):
        with EditMode(self.getDocument()):
            self._height.setValue(height)
            self._updateGeometry()

    def setElementLength(self, param):
        print("try to change len")
        with EditMode(self.getDocument()):
            self._lineLength.setValue(param)
        droppedOnElement = self.create_line(param)
        if droppedOnElement:
            geometry = droppedOnElement.getGeometry()
            if self._setAxisCurve(geometry):
                lx.Application.getInstance().getActiveDocument().removeObject(droppedOnElement)
        print("change len")
        with EditMode(self.getDocument()):
            self._updateGeometry()

    def setLinePosition(self, param):
        with EditMode(self.getDocument()):
            self._linePosition.setValue(param)
            self._updateGeometry()

    def setColor(self, color):
        self._subElemColor = color

    def getSubElementByGlobalId(self, globalId):
        sub_elems = self.getSubElements()
        for i in range(len(sub_elems)):
            if sub_elems[i].getGlobalId() == globalId:
                return sub_elems[i]

    def _switchRepresentations(self, index):
        with EditMode(self.getDocument()):
            if index == 0:  # Index 0
                self.showAxisRepresentation()
            else:
                self.showSolidModelRepresentation()

                """
                Recreate the "MultiGeo" based on the Axis
                """
                self._updateGeometry()

    def getGlobalClassId(self):
        return GUID_CLASS

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == self._width.getName():
            self.setWidth(self._width.getValue())
        elif aPropertyName == self._height.getName():
            self.setHeight(self._height.getValue())
        elif aPropertyName == self._lineLength.getName():
            self.setElementLength(self._lineLength.getValue())
        elif aPropertyName == self._linePosition.getName():
            self.setLinePosition(self._linePosition.getValue())
        elif aPropertyName == self._representation.getName():
            self._switchRepresentations(self._representation.getValue())
        self._insidePropUpdate = False

    def getPolylineData(self, lineSet):
        lineData = []
        edges = Topo.ShapeTool.getEdges(lineSet.getShape())

        print("edges len: ", len(edges))
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
            else:
                raise RuntimeError("Unsupported edge type")

        return lineData

    def create_line(self, param=None):
        start_pnt = Geom.Pnt(0.0, 0.0, 0.0)
        if param:
            end_pnt = Geom.Pnt(param, 0.0, 0.0)
        else:
            end_pnt = Geom.Pnt(self._lineLength.getValue(), 0.0, 0.0)

        comp_curve = lx.CompositeCurve.createIn(self.getDocument())
        comp_curve.addSegment(lx.createLineSegment(self.getDocument(), start_pnt, end_pnt))

        elem = lx.Element.createIn(self.getDocument())
        elem.setGeometry(comp_curve)
        self.getDocument().recompute()
        return elem

    def _setAxisCurve(self, axisCurve):
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
    doc = lx.Application.getInstance().getActiveDocument()

    if doc:
        print("Doc is not none")
        doc.registerPythonScript(GUID_SCRPT)
        element = Seitenschutz01(doc)
        lx.setNewComponentByColorAndName(CW_COLOR, Base.StringTool.toString("Seitenschutz konventionell"), element)

        geometry = None

        """
        If the script is dropped on an Element take the Geometry and delete Element
        """
        thisScript = lx.Application.getInstance().getActiveScript()
        location = Geom.Pnt(0., 0., 0.)
        if thisScript.isDragAndDropped():
            location = thisScript.getInsertionPoint()
            droppedOnElement = element.create_line()
            if droppedOnElement:
                geometry = droppedOnElement.getGeometry()
                if element._setAxisCurve(geometry):
                    doc.removeObject(droppedOnElement)

        pos = Geom.Ax2(location, Geom.Dir_ZDir())
        element.setLocalPlacement(pos)
        """
        Ask the user to pick a Line, take the Geometry and delete Element
        """
        if geometry is None:
            ui.showStatusBarMessage(5944)
            uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
            uidoc.highlightByShapeType(Topo.ShapeType_WIRE)
            ok = uidoc.pickPoint()
            uidoc.stopHighlightByShapeType()
            ui.showStatusBarMessage(lxStr(""))
            if ok:
                pickedElement = uidoc.getPickedElement()
                geometry = pickedElement.getGeometry()
                if element._setAxisCurve(geometry):
                    doc.removeObject(pickedElement)

        """
        Set IFC type and other additional properties
        """

        cmd.CmdSetPropertySetDefinition("Pset_RailingCommon", "reference", "01_Seitenschutz_konventionell", element).redo()

        pset_name = Base.StringTool.toStlString(Base.PTranslator.get(587))  # "Absturzsicherung_Suva"
        prop1_name = Base.StringTool.toStlString(Base.PTranslator.get(588))  # "Typ"
        prop1_value = Base.StringTool.toStlString(Base.PTranslator.get(512))  # "01_Seitenschutz_konventionell"

        prop2_name = Base.StringTool.toStlString(Base.PTranslator.get(590))    # "Vorgespanntes_Drahtseil"
        prop3_name = Base.StringTool.toStlString(Base.PTranslator.get(591))    # "Innengeländer"

        cmd.CmdSetPropertySetDefinition(pset_name, prop3_name, element).redo()
        cmd.CmdSetPropertySetDefinition(pset_name, prop1_name, prop1_value, element).redo()
        cmd.CmdSetPropertySetDefinition(pset_name, prop2_name, element).redo()


if __name__ == "__main__":
    main()
