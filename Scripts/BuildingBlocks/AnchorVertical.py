# Author: Pavlo Leskovych
# Version: 1.2.4  24.04.2020
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

import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd
import Base, Core, Geom, Topo, Draw
import math, copy, traceback

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


def vecsAreSame(v1, v2, tolerance=epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


def baseVecTranslate(pt, baseVec, dist):
    return Geom.Pnt(
        pt.x() + (baseVec.x() * dist),
        pt.y() + (baseVec.y() * dist),
        pt.z() + (baseVec.z() * dist))


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


class RuehlWandVertical(lx.PythonElement):
    _classID = "{6B090AE9-6C9F-47B1-93BC-74EC574E041A}"
    _headerPropName = "Anker (Vertical)"
    _groupPropName = "Anker Parameter"

    # Parameters property names
    _nailLengthPropName = "Nail Length"
    _nailRadiusPropName = "Nail Radius"
    _bottomLengthPropName = "Injection Length"
    _bottomRadiusPropName = "Injection Radius"
    _anglePropName = "Angle"
    _nailColorName = "Nail Color"
    _injectionColorName = "Injection Color"
    _showNailHeadName = "Show nail head"
    _nailHeadRadiusName = "Nail head radius"
    _nailHeadLengthName = "Nail head length"
    _showHeadPlateName = "show Nail plate"
    _nailPlateWidthName = "Nail plate width"
    _nailPlateHeightName = "Nail plate height"
    _nailPlateThicknessName = "Nail plate thickness"

    def getGlobalClassId(self):
        return Base.GlobalId(RuehlWandVertical._classID)

    def __init__(self, aArg):
        lx.PythonElement.__init__(self, aArg)
        self.registerPythonClass("RuehlWandVertical", "OpenLxApp.PythonElement")

        # Register properties
        self.setPropertyHeader(lxstr(RuehlWandVertical._headerPropName), -1)
        self.setPropertyGroupName(lxstr(RuehlWandVertical._groupPropName), -1)

        self._nailLength = self.registerPropertyDouble(RuehlWandVertical._nailLengthPropName, 5.0,
                                                       lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 1)
        self._nailRadius = self.registerPropertyDouble(RuehlWandVertical._nailRadiusPropName, 0.075,
                                                       lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 2)
        self._showNailHead = self.registerPropertyEnum(self._showNailHeadName, 0,
                                                       lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 17)
        self._showNailHead.setEmpty()
        self._showNailHead.addEntry(lxstr("Yes"), -1)
        self._showNailHead.addEntry(lxstr("No"), -1)

        self._nailHeadRadius = self.registerPropertyDouble(RuehlWandVertical._nailHeadRadiusName, 0.10,
                                                           lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 20)
        self._nailHeadLength = self.registerPropertyDouble(RuehlWandVertical._nailHeadLengthName, 0.25,
                                                           lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 19)

        self._showHeadPlate = self.registerPropertyEnum(self._showHeadPlateName, 0,
                                                        lx.Property.VISIBLE,
                                                        lx.Property.EDITABLE, 18)
        self._showHeadPlate.setEmpty()
        self._showHeadPlate.addEntry(lxstr("Yes"), -1)
        self._showHeadPlate.addEntry(lxstr("No"), -1)
        self._nailPlateWidth = self.registerPropertyDouble(RuehlWandVertical._nailPlateWidthName, 0.40,
                                                           lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 23)
        self._nailPlateHeight = self.registerPropertyDouble(RuehlWandVertical._nailPlateHeightName, 0.40,
                                                            lx.Property.VISIBLE,
                                                            lx.Property.EDITABLE, 24)
        self._nailPlateThickness = self.registerPropertyDouble(RuehlWandVertical._nailPlateThicknessName, 0.05,
                                                               lx.Property.VISIBLE,
                                                               lx.Property.EDITABLE, 25)

        self._bottomLength = self.registerPropertyDouble(RuehlWandVertical._bottomLengthPropName, 1.0,
                                                         lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, 3)
        self._bottomRadius = self.registerPropertyDouble(RuehlWandVertical._bottomRadiusPropName, 0.12,
                                                         lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, 4)
        self._angle = self.registerPropertyDouble(RuehlWandVertical._anglePropName, 0.0, lx.Property.VISIBLE,
                                                  lx.Property.EDITABLE, 5)
        self._nailColor = self.registerPropertyColor(RuehlWandVertical._nailColorName, Base.Color_fromCdwkColor(34),
                                                     lx.Property.VISIBLE,
                                                     lx.Property.EDITABLE, 6)
        self._injectionColor = self.registerPropertyColor(RuehlWandVertical._injectionColorName,
                                                          Base.Color_fromCdwkColor(110),
                                                          lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, 7)

        self.setupHeadEnum()
        self.setupPlateEnum()
        self._setAllSteps()
        
        self._updateGeometry()

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

    @staticmethod
    def buildSubElemLine(aFromPnt, aToPnt):
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
            self._nailDiameter.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
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

    def _createNail(self):
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

        rotateAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(1, 0, 0))
        nailElem.rotate(rotateAxis, -angle, Geom.CoordSpace_WCS)
        self.addSubElement(nailElem)

    def _createHead(self):
        head_radius = self._nailHeadRadius.getValue()
        head_length = self._nailHeadLength.getValue()
        angle = math.radians(self._angle.getValue())
        rotateAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(1, 0, 0))

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
            headElem.rotate(rotateAxis, -angle, Geom.CoordSpace_WCS)
            self.addSubElement(headElem)
        else:
            return

    def _createPlate(self):
        plate_width = self._nailPlateWidth.getValue()
        plate_height = self._nailPlateHeight.getValue()
        plate_thickness = self._nailPlateThickness.getValue()
        angle = math.radians(self._angle.getValue())
        rotateAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(1, 0, 0))

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
            plateElem.rotate(rotateAxis, -angle, Geom.CoordSpace_WCS)
            self.addSubElement(plateElem)
        else:
            return

    def _createBottom(self):
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

        externCylinder = lx.RightCircularCylinder.createIn(doc)
        externCylinder.setHeight(bot_len)
        externCylinder.setRadius(bot_rad)
        extElement = lx.Element.createIn(doc)
        extElement.setGeometry(externCylinder)

        resultingCylinders = lx.vector_Element()
        if lx.bop_cut(extElement, intElement, resultingCylinders) != 0:
            print("error in cut!")
        doc.removeObject(intElement)
        doc.removeObject(extElement)

        transform = resultingCylinders[0].getTransform()
        geometry = resultingCylinders[0].getGeometry()

        botElem = lx.SubElement.createIn(doc)
        botElem.setTransform(transform)
        botElem.setGeometry(geometry)
        botElem.translate(Geom.Vec(0.0, 0.0, -nail_len), Geom.CoordSpace_WCS)
        botElem.setDiffuseColor(color)
        rotateAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(1, 0, 0))
        botElem.rotate(rotateAxis, -angle, Geom.CoordSpace_WCS)
        self.addSubElement(botElem)

    def _createGeometry(self):
        if self._bottomLength.getValue() > epsilon:
            self._createNail()
            self._createBottom()
            self._createHead()
            self._createPlate()
        else:
            self._createNail()
            self._createHead()
            self._createPlate()

    def _updateGeometry(self):
        doc = self.getDocument()

        with EditMode(doc):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == RuehlWandVertical._nailRadiusPropName:
            self.setNailRadius(self._nailRadius.getValue())
        elif aPropertyName == RuehlWandVertical._nailLengthPropName:
            self.setNailLength(self._nailLength.getValue())
        elif aPropertyName == RuehlWandVertical._bottomRadiusPropName:
            self.setBottomRadius(self._bottomRadius.getValue())
        elif aPropertyName == RuehlWandVertical._bottomLengthPropName:
            self.setBottomLength(self._bottomLength.getValue())
        elif aPropertyName == RuehlWandVertical._anglePropName:
            self.setAngle(self._angle.getValue())
        elif aPropertyName == RuehlWandVertical._nailColorName:
            self.setNailColor(self._nailColor.getValue())
        elif aPropertyName == RuehlWandVertical._injectionColorName:
            self.setInjectionColor(self._injectionColor.getValue())
        elif aPropertyName == RuehlWandVertical._nailHeadRadiusName:
            self.setNailHeadRadius(self._nailHeadRadius.getValue())
        elif aPropertyName == RuehlWandVertical._nailHeadLengthName:
            self.setNailHeadLength(self._nailHeadLength.getValue())
        elif aPropertyName == RuehlWandVertical._nailPlateWidthName:
            self.setNailPlateWidth(self._nailPlateWidth.getValue())
        elif aPropertyName == RuehlWandVertical._nailPlateHeightName:
            self.setNailPlateHeight(self._nailPlateHeight.getValue())
        elif aPropertyName == RuehlWandVertical._nailPlateThicknessName:
            self.setNailPlateThickness(self._nailPlateThickness.getValue())
        elif aPropertyName == RuehlWandVertical._showNailHeadName:
            self.setShowHead(self._showNailHead.getValue())
        elif aPropertyName == RuehlWandVertical._showHeadPlateName:
            self.setShowPlate(self._showHeadPlate.getValue())

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(doc):
            if not Geom.GeomTools.isEqual(x, 1.):
                old1 = self._nailRadius.getValue()
                old2 = self._bottomRadius.getValue()
                self.setNailRadius(old1 * x)
                self.setBottomRadius(old2 * x)
            if not Geom.GeomTools.isEqual(y, 1.):
                old1 = self._nailRadius.getValue()
                old2 = self._bottomRadius.getValue()
                self.setNailRadius(old1 * y)
                self.setBottomRadius(old2 * y)
            if not Geom.GeomTools.isEqual(z, 1.):
                old = self._nailLength.getValue()
                self.setNailLength(old * z)

            self.translateAfterScaled(aVec, aScaleBasePnt)


if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{D7983B18-383A-4771-97EA-C3F1BAC4F284}"))

    try:
        compound = RuehlWandVertical(doc)
        with EditMode(doc):
            compound.setDiffuseColor(Base.Color_fromCdwkColor(40))
        with EditMode(doc):
            cmd.CmdAddPropertySet(
                'Nail & Injection Parameters',
                [
                    compound._nailLengthPropName,
                    compound._nailRadiusPropName,
                    compound._anglePropName,
                    compound._bottomLengthPropName,
                    compound._bottomRadiusPropName,
                ],
                compound
            ).redo()
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
        else:
            pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

        compound.setLocalPlacement(pos)
    except Exception as e:
        # print(e.message)
        traceback.print_exc()
    finally:
        doc.recompute()
