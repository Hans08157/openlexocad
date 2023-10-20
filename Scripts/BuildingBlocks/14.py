# Version 1.1 - SB
#   Added the choice between 1, 2, or 3 horizontal Elements
#   Default values: 3 Elements, 1.150 Height
#   Cleanup, removed unused code
#
# Version 1.0 - Unknown


import math
import traceback

import Base
import Draw
import Geom
import OpenLxApp as lx
import OpenLxUI as ui
import Topo

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


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


def baseVecTranslate(pt, baseVec, dist):
    return Geom.Pnt(
        pt.x() + (baseVec.x() * dist),
        pt.y() + (baseVec.y() * dist),
        pt.z() + (baseVec.z() * dist)
    )


class PolylineData:
    SegmType_Line = 0

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
            if lineElem[edgeIndex][0] == PolylineData.SegmType_Line:
                p1Res = lineElem[edgeIndex][1]
                if firstEdge:
                    newPD._ptList.append(Geom.Pnt(p1Res))
                    firstEdge = False

                p2Res = lineElem[edgeIndex][2]
                newPD._ptList.append(Geom.Pnt(p2Res))

                segmData = PolylineData._LineSegmData(startIndex, False)
                newPD._segmList.append(PolylineData._Segment(
                    PolylineData.SegmType_Line, segmData))

                startIndex += 1
            else:
                raise RuntimeError("Unsupported edge type")

        i_n = len(lineElem[len(lineElem) - 1]) - 1
        newPD._closed = lineElem[len(lineElem) - 1][i_n]
        return newPD

    def pointCount(self):
        return len(self._ptList)

    def point(self, id):
        return self._ptList[id]


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
            return

        for segmId in range(self.segmCount):
            segmType = self.polyline.segmentType(segmId)

            if segmType == PolylineData.SegmType_Line:
                startPt = self.polyline.segmStartPt(segmId)
                endPt = self.polyline.segmEndPt(segmId)
                lineSegment = self.SegmLine(startPt, endPt)
                self.segmentsList.append(lineSegment)
            else:
                return

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


class ModelAssembler:
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

    wire = Topo.ShapeTool.isSingleWire(lineSet.getShape())

    if Topo.WireTool.isClosed(wire):
        edges = Topo.WireTool.getEdges(Topo.WireTool.reversed(wire))
    else:
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
            lineData.append([PolylineData.SegmType_Line,
                            Geom.Pnt(p1Res.p), Geom.Pnt(p2Res.p)])

        else:
            raise RuntimeError("Unsupported edge type")
    lineData[len(edges) - 1].append(Topo.WireTool.isClosed(wire))

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
    ui.showStatusBarMessage(8509)
    lineSet = selectPolyline(uidoc)
    ui.showStatusBarMessage(lxstr(""))

    if lineSet is not None:
        return getPolylineData(lineSet)
    else:
        return None


class Barrier(lx.Element):
    _headerName = "Barrier"
    _groupName = "Barrier Parameters"
    _heightPropName = "Height"
    _colorPropName = "Color"
    _colorBoolPropName = "Use color"
    _polylinePropName = "Polyline"
    _tapeHeightPropName = "Tape Height"
    _tapeNumberPropName = "Tape number"

    def getGlobalClassId(self):
        return Base.GlobalId("{a43e2904-bd86-41ea-80b4-ca550bd555aa}")

    def getScriptVersion(self):
        return 110  # Version 1.1.0

    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Barrier", "OpenLxApp.Element")
        # Register properties
        self.setPropertyHeader(lxstr(Barrier._headerName), 585)
        self.setPropertyGroupName(lxstr(Barrier._groupName), 586)

        self._height = self.registerPropertyDouble(Barrier._heightPropName, 1.150,
                                                   lx.Property.VISIBLE, lx.Property.EDITABLE, 580)

        self._tapeHeight = self.registerPropertyDouble(Barrier._tapeHeightPropName, 0.15,
                                                       lx.Property.VISIBLE, lx.Property.EDITABLE, 581)

        self._colorBool = self.registerPropertyBool(Barrier._colorBoolPropName, False,
                                                    lx.Property.VISIBLE, lx.Property.EDITABLE, 582)

        self._color = self.registerPropertyColor(Barrier._colorPropName, Base.Color(5, 193, 74),
                                                 lx.Property.VISIBLE, lx.Property.EDITABLE, 583)

        self._tapeNumber = self.registerPropertyEnum(Barrier._tapeNumberPropName, 2,
                                                     lx.Property.VISIBLE, lx.Property.EDITABLE, 584)
        self._tapeNumber.setEmpty()
        self._tapeNumber.addEntry(lxstr("1"), -1)  # index 0
        self._tapeNumber.addEntry(lxstr("2"), -1)  # index 1
        self._tapeNumber.addEntry(lxstr("3"), -1)  # index 2

        # Not Visible
        self._polyline = self.registerPropertyString(Barrier._polylinePropName, lxstr(""),
                                                     lx.Property.NOT_VISIBLE, lx.Property.NOT_EDITABLE, -1)
        self._modules = self.registerPropertyDouble("Modules", 0.0,
                                                    lx.Property.NOT_VISIBLE, lx.Property.NOT_EDITABLE, -1)

        self._setAllSteps()
        self._setupColorBool()

        self._baseData = None
        dataStr = cstr(self._polyline.getValue())
        if dataStr:
            self._baseData = self.readFromString(dataStr)

    def _setupColorBool(self):
        mVal = self._colorBool.getValue()

        if mVal is 0:
            self._color.setVisible(False)
            print("Color property has set to False")
        elif mVal is 1:
            self._color.setVisible(True)
            print("Color property has set to True")

    @staticmethod
    def _createSubElement(listPoint, heightStep, dir):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)
        return subElem

    def setPolylineData(self, polylineData):
        if lxstr(self.writeToString(polylineData)) is self._modules.getValue():
            print("Select another polyline")
            return

        self._insidePropUpdate = True

        self._baseData = polylineData
        self._polyline.setValue(lxstr(self.writeToString(polylineData)))

        self._updateGeometry()

    def _setAllSteps(self):
        self._height.setSteps(0.1)
        self._tapeHeight.setSteps(0.05)

    @staticmethod
    def writeToString(lineData):
        strn = ""
        strn += "{};".format(len(lineData))
        for i in range(len(lineData)):
            if lineData[i][0] == PolylineData.SegmType_Line:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};".format(
                    lineData[i][0],
                    lineData[i][1].x(),
                    lineData[i][1].y(),
                    lineData[i][1].z(),
                    lineData[i][2].x(),
                    lineData[i][2].y(),
                    lineData[i][2].z()
                )

        i_n = len(lineData[len(lineData) - 1]) - 1
        strn += "{}".format(lineData[len(lineData) - 1][i_n])
        return strn

    @staticmethod
    def readFromString(strn):
        lineData = []
        st = strn.split(";")
        index = 0
        for i in range(int(st[0])):
            if int(st[index + 1]) == PolylineData.SegmType_Line:
                lineData.append([
                    int(st[index + 1]),
                    Geom.Pnt(float(st[index + 2]),
                             float(st[index + 3]),
                             float(st[index + 4])),
                    Geom.Pnt(float(st[index + 5]),
                             float(st[index + 6]),
                             float(st[index + 7]))
                ])
                index += 7

        i_n = len(lineData[int(st[0]) - 1])
        if st[len(st) - 1] == "True":
            bl = True
        else:
            bl = False
        lineData[int(st[0]) - 1].append(bl)

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

    def setTapeHeight(self, param):
        maxValue = self._height.getValue() * 0.33
        with EditMode(self.getDocument()):
            self._tapeHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setColor(self, param):
        with EditMode(self.getDocument()):
            self._color.setValue(param)
            self._updateGeometry()

    def setColorBool(self, param):
        with EditMode(self.getDocument()):
            self._colorBool.setValue(param)
            self._updateGeometry()

    def setNumber(self, param):
        with EditMode(self.getDocument()):
            self._tapeNumber.setValue(param)
            self._updateGeometry()

    def _createBases(self):
        mHeight = self._height.getValue()
        polyLine = PolylineData.fromElement(self._baseData)
        # Cylinders subelements
        for i in range(polyLine.pointCount()):
            # creating cylinders
            cylinder = lx.RightCircularCylinder.createIn(self.getDocument())
            cylinder.setHeight(mHeight)
            cylinder.setRadius(0.04)

            mCylinderSubElem = lx.SubElement.createIn(self.getDocument())
            mCylinderSubElem.setGeometry(cylinder)
            translateVector = Geom.Vec(
                Geom.Pnt(0.0, 0.0, 0.0), polyLine.point(i))
            mCylinderSubElem.translate(translateVector)
            self.addSubElement(mCylinderSubElem)

    def createTape(self, model, p):
        mHeight = self._height.getValue()
        mColor = self._color.getValue()
        mTapeHeight = self._tapeHeight.getValue()

        zMin = (mHeight - mTapeHeight) * p

        # polyline data
        polyLine = PolylineData.fromElement(self._baseData)

        texture = Draw.Texture2()
        texture.setTextureFileName(lxstr('textures/600/631.jpg'))

        for i in range(polyLine.pointCount()-1):
            floorPnt1 = polyLine.point(i)
            floorPnt2 = polyLine.point(i+1)

            firstVec = Geom.Vec(floorPnt1, floorPnt2)
            secondVec = Geom.Vec(floorPnt2, floorPnt1)

            firstVec.rotate(
                Geom.Ax1(floorPnt1, Geom.Dir(0, 0, 1)), -math.radians(90.0))
            secondVec.rotate(
                Geom.Ax1(floorPnt2, Geom.Dir(0, 0, 1)), math.radians(90.0))
            firstVec.normalize()
            secondVec.normalize()

            tapeVec1 = baseVecTranslate(floorPnt1, firstVec, 0.015)
            tapeVec2 = baseVecTranslate(floorPnt2, secondVec, 0.015)

            floorPnt1 = Geom.Pnt(tapeVec1.coord())
            floorPnt2 = Geom.Pnt(tapeVec2.coord())

            pnt1 = floorPnt1.translated(Geom.Vec(0.0, 0.0, zMin))
            pnt2 = floorPnt2.translated(Geom.Vec(0.0, 0.0, zMin))
            pnt3 = floorPnt2.translated(Geom.Vec(0.0, 0.0, zMin + mTapeHeight))
            pnt4 = floorPnt1.translated(Geom.Vec(0.0, 0.0, zMin + mTapeHeight))

            directionVec = Geom.Vec(floorPnt1, polyLine.point(i))

            subFace = self._createSubElement(
                [pnt1, pnt2, pnt3, pnt4], 0.03, Geom.Dir(directionVec))
            if self._colorBool.getValue():
                subFace.setDiffuseColor(mColor)
            else:
                subFace.setTexture(texture, -1)
            model.addSubElem(subFace)

    def _createGeometry(self):
        model = ModelAssembler(doc)
        model.beginModel(self)

        number = self._tapeNumber.getValue() + 1

        if number > 0:
            self._createBases()
            self.createTape(model, 1.0)
        if number > 1:
            self.createTape(model, 0.5)
        if number > 2:
            self.createTape(model, 0.0)

        model.endModel()

    def _updateGeometry(self):
        with EditMode(self.getDocument()):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == Barrier._heightPropName:
            self.setHeight(self._height.getValue())
        elif aPropertyName == Barrier._colorPropName:
            self.setColor(self._color.getValue())
        elif aPropertyName == Barrier._colorBoolPropName:
            self.setColorBool(self._colorBool.getValue())
        elif aPropertyName == Barrier._tapeHeightPropName:
            self.setTapeHeight(self._tapeHeight.getValue())
        elif aPropertyName == Barrier._tapeNumberPropName:
            self.setNumber(self._tapeNumber.getValue())


if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId(
        "{1a9a42f7-f8e5-495e-b6d4-81c0b80a5f83}"))
    # Begin creating the Element
    try:
        with EditMode(doc):
            polylineData = pickPolyline(uidoc)
            if polylineData is not None:
                elem = Barrier(doc)
                elem.setPolylineData(polylineData)
    except Exception as e:
        traceback.print_exc()
    finally:
        doc.recompute()
