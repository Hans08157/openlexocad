# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import math, copy, traceback

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString
doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

epsilon = 0.001
maxValue = 10000

def qstr(str):
    return Base.StringTool.toQString(lxstr(str))
# Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))

def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))

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
            raise RuntimeError("FacetedModelAssembler.endModel() must be called after FacetedModelAssembler.beginModel()")

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
            raise RuntimeError("FacetedModelAssembler.beginFace() must be called between FacetedModelAssembler.beginModel() and FacetedModelAssembler.endModel()")

        if self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.beginFace() is called twice")

        self._insideFaceCreation = True

    def addVertex(self, pos):
        if not self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.addVertex() must be called between FacetedModelAssembler.beginFace() and FacetedModelAssembler.endFace()")

        ptIndex = self._insertPoint(pos)
        self._indexList.append(ptIndex)

    def addVertexList(self, posList):
        if not self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.addVertexList() must be called between FacetedModelAssembler.beginFace() and FacetedModelAssembler.endFace()")

        for pos in posList:
            ptIndex = self._insertPoint(pos)
            self._indexList.append(ptIndex)

    def endLoop(self):
        self._indexList.append(-2)

    def endFace(self):
        if not self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.endFace() must be called after FacetedModelAssembler.beginFace()")

        self._indexList.append(-2)
        self._indexList.append(-1)

        self._insideFaceCreation = False

    def addExtrusionBridgeNeg(self, startEdge, endEdge, closed):
        if self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.addExtrusionBridgeNeg() must be called outside of face assembly process")

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

    @staticmethod
    def createExtrudedSubElement(listPoint, heightStep, dir):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)
        return subElem

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

class SchachtKonusElem(lx.Element):
    _classID = "{835e2bdc-067f-4f6b-85af-35b4558bf2e6}"
    _headerPropName = "Schacht Konus"
    _groupPropName = "Schacht Parameter"

    _topDiameterPropName = "Top Diameter"
    _bottomDiameterPropName = "Bottom Diameter"
    _heightPropName = "Height"
    _thicknessPropName = "Thickness"
    _topHeightPropName = "Top Height"
    _circlesCountPropName = "Circles Count"
    _circlesHeightPropName = "Circles Height"
    _bottomBendingPropName = "Bottom Bending"
    _baseDiameterPropName = "Base Diameter"
    _baseHeightPropName = "Base Height"
    _baseTypePropName = "Base Type"
    _baseLengthPropName = "Base Length"
    _tapeTypePropName = "Tape Type"

    def getGlobalClassId(self):
        return Base.GlobalId(SchachtKonusElem._classID)

    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("SchachtKonusElem", "OpenLxApp.Element")
        # Register properties
        self.setPropertyHeader(lxstr(SchachtKonusElem._headerPropName), -1)
        self.setPropertyGroupName(lxstr(SchachtKonusElem._groupPropName), -1)

        self._topConeDiameter = self.registerPropertyDouble(SchachtKonusElem._topDiameterPropName,
                                                            0.625,
                                                            lx.Property.VISIBLE,
                                                            lx.Property.EDITABLE, -1)
        self._bottomConeDiameter = self.registerPropertyDouble(SchachtKonusElem._bottomDiameterPropName,
                                                               1.0,
                                                               lx.Property.VISIBLE,
                                                               lx.Property.EDITABLE, -1)
        self._ConeHeight = self.registerPropertyDouble(SchachtKonusElem._heightPropName,
                                                       0.6,
                                                       lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, -1)
        self._ConeThickness = self.registerPropertyDouble(SchachtKonusElem._thicknessPropName,
                                                          0.120,
                                                          lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)
        self._topHeight = self.registerPropertyDouble(SchachtKonusElem._topHeightPropName,
                                                          0.30,
                                                          lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)
        self._circlesCount = self.registerPropertyInteger(SchachtKonusElem._circlesCountPropName,
                                                      2,
                                                      lx.Property.VISIBLE,
                                                      lx.Property.EDITABLE, -1)
        self._circlesHeight = self.registerPropertyDouble(SchachtKonusElem._circlesHeightPropName,
                                                         0.5,
                                                         lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, -1)
        self._bottomBending = self.registerPropertyDouble(SchachtKonusElem._bottomBendingPropName,
                                                          0.250,
                                                          lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)

        self._baseType = self.registerPropertyEnum(self._baseTypePropName, 0, lx.Property.VISIBLE,
                                               lx.Property.EDITABLE, -1)
        self._baseType.setEmpty()
        self._baseType.addEntry(lxstr("Round"), -1)
        self._baseType.addEntry(lxstr("Square"), -1)

        self._baseDiameter = self.registerPropertyDouble(SchachtKonusElem._baseDiameterPropName,
                                                          1.640,
                                                          lx.Property.NOT_VISIBLE,
                                                          lx.Property.EDITABLE, -1)
        self._baseLength = self.registerPropertyDouble(SchachtKonusElem._baseLengthPropName,
                                                         1.640,
                                                         lx.Property.NOT_VISIBLE,
                                                         lx.Property.EDITABLE, -1)
        print(self._baseLength.getValue())
        self._baseHeight = self.registerPropertyDouble(SchachtKonusElem._baseHeightPropName,
                                                          0.250,
                                                          lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)

        self._tapeType = self.registerPropertyEnum(self._tapeTypePropName, 0, lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE, -1)
        self._tapeType.setEmpty()
        self._tapeType.addEntry(lxstr("Closed"), -1)
        self._tapeType.addEntry(lxstr("With holes"), -1)
        self._tapeType.addEntry(lxstr("With slots"), -1)

        self._setupTypeCombobox()
        self._setAllSteps()
        
        self._updateGeometry()

    def _setupTypeCombobox(self):
        if self._baseType.getValue() is 0:
            self._baseDiameter.setVisible(True)
            self._baseLength.setVisible(False)
        elif self._baseType.getValue() is 1:
            self._baseDiameter.setVisible(False)
            self._baseLength.setVisible(True)

    def _setAllSteps(self):
        self._topConeDiameter.setSteps(0.1)
        self._bottomConeDiameter.setSteps(0.1)
        self._ConeHeight.setSteps(0.2)
        self._ConeThickness.setSteps(0.05)
        self._topHeight.setSteps(0.05)
        self._circlesHeight.setSteps(0.1)
        self._baseHeight.setSteps(0.05)
        self._baseDiameter.setSteps(0.1)
        self._bottomBending.setSteps(0.1)
        self._baseLength.setSteps(0.1)

    def setBottomBending(self, param):
        epsilon = self._ConeThickness.getValue()
        maxValue = self._circlesHeight.getValue()

        with EditMode(self.getDocument()):
            self._bottomBending.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setBaseDiameter(self, param):
        epsilon = self._bottomConeDiameter.getValue()
        with EditMode(self.getDocument()):
            self._baseDiameter.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setBaseHeight(self, param):
        with EditMode(self.getDocument()):
            self._baseHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setBaseLength(self, param):
        with EditMode(self.getDocument()):
            self._baseLength.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setBaseType(self, param):
        with EditMode(self.getDocument()):
            self._baseType.setValue(param)
            self._updateGeometry()

    def setTapeType(self, param):
        with EditMode(self.getDocument()):
            self._tapeType.setValue(param)
            self._updateGeometry()

    def setTopHeight(self, param):
        epsilon = self._ConeThickness.getValue() + 0.001

        with EditMode(self.getDocument()):
            self._topHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setTopConeDiameter(self, param):
        maxValue = self._bottomConeDiameter.getValue()

        with EditMode(self.getDocument()):
            self._topConeDiameter.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setBottomConeDiameter(self, param):
        if self._baseType is 0:
            maxValue = self._baseDiameter.getValue() +  2 * self._ConeThickness.getValue()
        else:
            maxValue = self._baseLength.getValue() +  2 * self._ConeThickness.getValue()

        epsilon = self._topConeDiameter.getValue()

        with EditMode(self.getDocument()):
            self._bottomConeDiameter.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setConeHeight(self, param):
        with EditMode(self.getDocument()):
            self._ConeHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setConeThickness(self, param):
        maxValue = self._topHeight.getValue() - epsilon
        with EditMode(self.getDocument()):
            self._ConeThickness.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setCirclesCount(self, param):
        with EditMode(self.getDocument()):
            self._circlesCount.setValue(clamp(param, -0.001, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setCirclesHeight(self, param):
        with EditMode(self.getDocument()):
            self._circlesHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def _createCircle(self, zCoordinate, last):

        doc = self.getDocument()

        # topRadius = self._topConeDiameter.getValue() * 0.5
        bottomRadius = self._bottomConeDiameter.getValue() * 0.5
        coneHeight = self._ConeHeight.getValue()
        circlesHeight = self._circlesHeight.getValue()
        thickness = self._ConeThickness.getValue()
        # xOffset = bottomRadius - topRadius

        if self._circlesCount.getValue() > 0:
            if last:
                # Points
                bendingZ = self._bottomBending.getValue()
                middleBendingZ = (bendingZ - thickness) * 0.5
                # middleBendingZ = bendingZ / 2

                pnt1 = Geom.Pnt(0.0, -bottomRadius - thickness, zCoordinate)
                pnt2 = Geom.Pnt(bottomRadius + thickness, 0.0, zCoordinate)
                pnt3 = Geom.Pnt(0.0, bottomRadius + thickness, zCoordinate)
                pnt4 = Geom.Pnt(-bottomRadius - thickness, 0.0, zCoordinate)

                pnt5 = Geom.Pnt(0.0, -bottomRadius, zCoordinate + middleBendingZ + thickness)
                pnt6 = Geom.Pnt(bottomRadius, 0.0, zCoordinate + thickness)
                pnt7 = Geom.Pnt(0.0, bottomRadius, zCoordinate + middleBendingZ + thickness)
                pnt8 = Geom.Pnt(-bottomRadius, 0.0, zCoordinate + bendingZ)

                # pnt5 = Geom.Pnt(0.0, -bottomRadius, zCoordinate + thickness)
                # pnt6 = Geom.Pnt(bottomRadius, 0.0, zCoordinate + thickness)
                # pnt7 = Geom.Pnt(0.0, bottomRadius, zCoordinate + thickness)
                # pnt8 = Geom.Pnt(-bottomRadius, 0.0, zCoordinate + thickness)

                pnt17 = Geom.Pnt(0.0, -bottomRadius - thickness, zCoordinate + circlesHeight)
                pnt18 = Geom.Pnt(bottomRadius + thickness, 0.0, zCoordinate + circlesHeight)
                pnt19 = Geom.Pnt(0.0, bottomRadius + thickness, zCoordinate + circlesHeight)
                pnt20 = Geom.Pnt(-bottomRadius - thickness, 0.0, zCoordinate + circlesHeight)

                pnt21 = Geom.Pnt(0.0, -bottomRadius - thickness * 0.5, zCoordinate + circlesHeight)
                pnt22 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, zCoordinate + circlesHeight)
                pnt23 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, zCoordinate + circlesHeight)
                pnt24 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, zCoordinate + circlesHeight)

                pnt25 = Geom.Pnt(0.0, -bottomRadius - thickness * 0.5, zCoordinate + circlesHeight + thickness * 0.5)
                pnt26 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, zCoordinate + circlesHeight + thickness * 0.5)
                pnt27 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, zCoordinate + circlesHeight + thickness * 0.5)
                pnt28 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, zCoordinate + circlesHeight + thickness * 0.5)

                pnt29 = Geom.Pnt(0.0, -bottomRadius, zCoordinate + circlesHeight + thickness * 0.5)
                pnt30 = Geom.Pnt(bottomRadius, 0.0, zCoordinate + circlesHeight + thickness * 0.5)
                pnt31 = Geom.Pnt(0.0, bottomRadius, zCoordinate + circlesHeight + thickness * 0.5)
                pnt32 = Geom.Pnt(-bottomRadius, 0.0, zCoordinate + circlesHeight + thickness * 0.5)

                faceList = Topo.vector_Face(12)

                #  Bottom face
                bottomEdgeList = Topo.vector_Edge(2)
                bottomEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
                bottomEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt3, pnt4, pnt1)
                # bottomRightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt3)
                # bottomRightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt1)
                bottomWire = Topo.WireTool.makeWire(bottomEdgeList, Geom.Precision.linear_Resolution())
                bottomFace = Topo.FaceTool.makeFace(bottomWire, Geom.Precision.linear_Resolution())
                faceList[0] = bottomFace

                #  Bending face
                bendingEdgeList = Topo.vector_Edge(2)
                bendingEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
                bendingEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt8, pnt7)
                # bendingEdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt7)
                # bendingEdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt5)
                bendingWire = Topo.WireTool.makeWire(bendingEdgeList, Geom.Precision.linear_Resolution())
                bendingFace = Topo.FaceTool.makeFace(bendingWire, Geom.Precision.linear_Resolution())
                faceList[1] = bendingFace

                #  External faces
                extRightEdgeList = Topo.vector_Edge(4)
                extRightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
                extRightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt18, pnt19)
                extRightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt17)
                extRightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt19)
                extRightWire = Topo.WireTool.makeWire(extRightEdgeList, Geom.Precision.linear_Resolution())
                extRightFace = Topo.FaceTool.makeFace(extRightWire, Geom.Precision.linear_Resolution())
                faceList[2] = extRightFace

                extLeftEdgeList = Topo.vector_Edge(4)
                extLeftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt4, pnt3)
                extLeftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt20, pnt19)
                extLeftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt17)
                extLeftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt19)
                extLeftWire = Topo.WireTool.makeWire(extLeftEdgeList, Geom.Precision.linear_Resolution())
                extLeftFace = Topo.FaceTool.makeFace(extLeftWire, Geom.Precision.linear_Resolution())
                faceList[3] = extLeftFace

                #  internal faces
                internRightEdgeList = Topo.vector_Edge(4)
                internRightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
                internRightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt30, pnt31)
                internRightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt29)
                internRightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt31)
                internRightWire = Topo.WireTool.makeWire(internRightEdgeList, Geom.Precision.linear_Resolution())
                internRightFace = Topo.FaceTool.makeFace(internRightWire, Geom.Precision.linear_Resolution())
                faceList[4] = internRightFace

                internLeftEdgeList = Topo.vector_Edge(4)
                internLeftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt8, pnt7)
                internLeftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt32, pnt31)
                internLeftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt29)
                internLeftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt31)
                internLeftWire = Topo.WireTool.makeWire(internLeftEdgeList, Geom.Precision.linear_Resolution())
                internLeftFace = Topo.FaceTool.makeFace(internLeftWire, Geom.Precision.linear_Resolution())
                faceList[5] = internLeftFace

                #  Upper six faces
                upper1EdgeList = Topo.vector_Edge(4)
                upper1EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt18, pnt19)
                upper1EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt22, pnt23)
                upper1EdgeList[2] = Topo.EdgeTool.makeEdge(pnt17, pnt21)
                upper1EdgeList[3] = Topo.EdgeTool.makeEdge(pnt19, pnt23)
                upper1Wire = Topo.WireTool.makeWire(upper1EdgeList, Geom.Precision.linear_Resolution())
                upper1Face = Topo.FaceTool.makeFace(upper1Wire, Geom.Precision.linear_Resolution())
                faceList[6] = upper1Face

                upper2EdgeList = Topo.vector_Edge(4)
                upper2EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt20, pnt19)
                upper2EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt24, pnt23)
                upper2EdgeList[2] = Topo.EdgeTool.makeEdge(pnt17, pnt21)
                upper2EdgeList[3] = Topo.EdgeTool.makeEdge(pnt19, pnt23)
                upper2Wire = Topo.WireTool.makeWire(upper2EdgeList, Geom.Precision.linear_Resolution())
                upper2Face = Topo.FaceTool.makeFace(upper2Wire, Geom.Precision.linear_Resolution())
                faceList[7] = upper2Face

                upper3EdgeList = Topo.vector_Edge(4)
                upper3EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt22, pnt23)
                upper3EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt26, pnt27)
                upper3EdgeList[2] = Topo.EdgeTool.makeEdge(pnt21, pnt25)
                upper3EdgeList[3] = Topo.EdgeTool.makeEdge(pnt23, pnt27)
                upper3Wire = Topo.WireTool.makeWire(upper3EdgeList, Geom.Precision.linear_Resolution())
                upper3Face = Topo.FaceTool.makeFace(upper3Wire, Geom.Precision.linear_Resolution())
                faceList[8] = upper3Face

                upper4EdgeList = Topo.vector_Edge(4)
                upper4EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt24, pnt23)
                upper4EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt28, pnt27)
                upper4EdgeList[2] = Topo.EdgeTool.makeEdge(pnt21, pnt25)
                upper4EdgeList[3] = Topo.EdgeTool.makeEdge(pnt23, pnt27)
                upper4Wire = Topo.WireTool.makeWire(upper4EdgeList, Geom.Precision.linear_Resolution())
                upper4Face = Topo.FaceTool.makeFace(upper4Wire, Geom.Precision.linear_Resolution())
                faceList[9] = upper4Face

                upper5EdgeList = Topo.vector_Edge(4)
                upper5EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt26, pnt27)
                upper5EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt30, pnt31)
                upper5EdgeList[2] = Topo.EdgeTool.makeEdge(pnt25, pnt29)
                upper5EdgeList[3] = Topo.EdgeTool.makeEdge(pnt27, pnt31)
                upper5Wire = Topo.WireTool.makeWire(upper5EdgeList, Geom.Precision.linear_Resolution())
                upper5Face = Topo.FaceTool.makeFace(upper5Wire, Geom.Precision.linear_Resolution())
                faceList[10] = upper5Face

                upper6EdgeList = Topo.vector_Edge(4)
                upper6EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt28, pnt27)
                upper6EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt32, pnt31)
                upper6EdgeList[2] = Topo.EdgeTool.makeEdge(pnt25, pnt29)
                upper6EdgeList[3] = Topo.EdgeTool.makeEdge(pnt27, pnt31)
                upper6Wire = Topo.WireTool.makeWire(upper6EdgeList, Geom.Precision.linear_Resolution())
                upper6Face = Topo.FaceTool.makeFace(upper6Wire, Geom.Precision.linear_Resolution())
                faceList[11] = upper6Face

            else:
                #  Points
                pnt1 = Geom.Pnt(0.0, -bottomRadius - thickness, zCoordinate)
                pnt2 = Geom.Pnt(bottomRadius + thickness, 0.0, zCoordinate)
                pnt3 = Geom.Pnt(0.0, bottomRadius + thickness, zCoordinate)
                pnt4 = Geom.Pnt(-bottomRadius - thickness, 0.0, zCoordinate)

                pnt5 = Geom.Pnt(0.0, -bottomRadius - thickness * 0.5, zCoordinate)
                pnt6 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, zCoordinate)
                pnt7 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, zCoordinate)
                pnt8 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, zCoordinate)

                pnt9 = Geom.Pnt(0.0, -bottomRadius - thickness * 0.5, zCoordinate + thickness * 0.5)
                pnt10 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, zCoordinate + thickness * 0.5)
                pnt11 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, zCoordinate + thickness * 0.5)
                pnt12 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, zCoordinate + thickness * 0.5)

                pnt13 = Geom.Pnt(0.0, -bottomRadius, zCoordinate + thickness * 0.5)
                pnt14 = Geom.Pnt(bottomRadius, 0.0, zCoordinate + thickness * 0.5)
                pnt15 = Geom.Pnt(0.0, bottomRadius,  zCoordinate + thickness * 0.5)
                pnt16 = Geom.Pnt(-bottomRadius, 0.0, zCoordinate + thickness * 0.5)

                # xOffset = bottomRadius - topRadius

                pnt17 = Geom.Pnt(0.0, -bottomRadius - thickness, zCoordinate + circlesHeight)
                pnt18 = Geom.Pnt(bottomRadius + thickness, 0.0, zCoordinate + circlesHeight)
                pnt19 = Geom.Pnt(0.0, bottomRadius + thickness, zCoordinate + circlesHeight)
                pnt20 = Geom.Pnt(-bottomRadius - thickness, 0.0, zCoordinate + circlesHeight)

                pnt21 = Geom.Pnt(0.0, -bottomRadius - thickness * 0.5, zCoordinate + circlesHeight)
                pnt22 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, zCoordinate + circlesHeight)
                pnt23 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, zCoordinate + circlesHeight)
                pnt24 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, zCoordinate + circlesHeight)

                pnt25 = Geom.Pnt(0.0, -bottomRadius - thickness * 0.5, zCoordinate + circlesHeight + thickness * 0.5)
                pnt26 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, zCoordinate + circlesHeight + thickness * 0.5)
                pnt27 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, zCoordinate + circlesHeight + thickness * 0.5)
                pnt28 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, zCoordinate + circlesHeight + thickness * 0.5)

                pnt29 = Geom.Pnt(0.0, -bottomRadius, zCoordinate + circlesHeight + thickness * 0.5)
                pnt30 = Geom.Pnt(bottomRadius, 0.0, zCoordinate + circlesHeight + thickness * 0.5)
                pnt31 = Geom.Pnt(0.0, bottomRadius, zCoordinate + circlesHeight + thickness * 0.5)
                pnt32 = Geom.Pnt(-bottomRadius, 0.0, zCoordinate + circlesHeight + thickness * 0.5)

                faceList = Topo.vector_Face(16)

                #  Bottom six planes
                bottom1EdgeList = Topo.vector_Edge(4)
                bottom1EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
                bottom1EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
                bottom1EdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
                bottom1EdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
                bottom1Wire = Topo.WireTool.makeWire(bottom1EdgeList, Geom.Precision.linear_Resolution())
                bottom1Face = Topo.FaceTool.makeFace(bottom1Wire, Geom.Precision.linear_Resolution())
                faceList[0] = bottom1Face

                bottom2EdgeList = Topo.vector_Edge(4)
                bottom2EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt4, pnt3)
                bottom2EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt8, pnt7)
                bottom2EdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
                bottom2EdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
                bottom2Wire = Topo.WireTool.makeWire(bottom2EdgeList, Geom.Precision.linear_Resolution())
                bottom2Face = Topo.FaceTool.makeFace(bottom2Wire, Geom.Precision.linear_Resolution())
                faceList[1] = bottom2Face

                bottom3EdgeList = Topo.vector_Edge(4)
                bottom3EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
                bottom3EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt10, pnt11)
                bottom3EdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt9)
                bottom3EdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt11)
                bottom3Wire = Topo.WireTool.makeWire(bottom3EdgeList, Geom.Precision.linear_Resolution())
                bottom3Face = Topo.FaceTool.makeFace(bottom3Wire, Geom.Precision.linear_Resolution())
                faceList[2] = bottom3Face

                bottom4EdgeList = Topo.vector_Edge(4)
                bottom4EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt8, pnt7)
                bottom4EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt12, pnt11)
                bottom4EdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt9)
                bottom4EdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt11)
                bottom4Wire = Topo.WireTool.makeWire(bottom4EdgeList, Geom.Precision.linear_Resolution())
                bottom4Face = Topo.FaceTool.makeFace(bottom4Wire, Geom.Precision.linear_Resolution())
                faceList[3] = bottom4Face

                bottom5EdgeList = Topo.vector_Edge(4)
                bottom5EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt10, pnt11)
                bottom5EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt14, pnt15)
                bottom5EdgeList[2] = Topo.EdgeTool.makeEdge(pnt9, pnt13)
                bottom5EdgeList[3] = Topo.EdgeTool.makeEdge(pnt11, pnt15)
                bottom5Wire = Topo.WireTool.makeWire(bottom5EdgeList, Geom.Precision.linear_Resolution())
                bottom5Face = Topo.FaceTool.makeFace(bottom5Wire, Geom.Precision.linear_Resolution())
                faceList[4] = bottom5Face

                bottom6EdgeList = Topo.vector_Edge(4)
                bottom6EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt12, pnt11)
                bottom6EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt16, pnt15)
                bottom6EdgeList[2] = Topo.EdgeTool.makeEdge(pnt9, pnt13)
                bottom6EdgeList[3] = Topo.EdgeTool.makeEdge(pnt11, pnt15)
                bottom6Wire = Topo.WireTool.makeWire(bottom6EdgeList, Geom.Precision.linear_Resolution())
                bottom6Face = Topo.FaceTool.makeFace(bottom6Wire, Geom.Precision.linear_Resolution())
                faceList[5] = bottom6Face

                #  External planes
                externalLeftEdgeList = Topo.vector_Edge(4)
                externalLeftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt4, pnt3)
                externalLeftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt20, pnt19)
                externalLeftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt17)
                externalLeftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt19)
                externalLeftWire = Topo.WireTool.makeWire(externalLeftEdgeList, Geom.Precision.linear_Resolution())
                externalLeftFace = Topo.FaceTool.makeFace(externalLeftWire, Geom.Precision.linear_Resolution())
                faceList[6] = externalLeftFace

                externalRightEdgeList = Topo.vector_Edge(4)
                externalRightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
                externalRightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt18, pnt19)
                externalRightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt17)
                externalRightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt19)
                externalRightWire = Topo.WireTool.makeWire(externalRightEdgeList, Geom.Precision.linear_Resolution())
                externalRightFace = Topo.FaceTool.makeFace(externalRightWire, Geom.Precision.linear_Resolution())
                faceList[7] = externalRightFace

                #  Internal planes
                internalRightEdgeList = Topo.vector_Edge(4)
                internalRightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt14, pnt15)
                internalRightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt30, pnt31)
                internalRightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt13, pnt29)
                internalRightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt15, pnt31)
                internalRightWire = Topo.WireTool.makeWire(internalRightEdgeList, Geom.Precision.linear_Resolution())
                internalRightFace = Topo.FaceTool.makeFace(internalRightWire, Geom.Precision.linear_Resolution())
                faceList[8] = internalRightFace

                internalLeftEdgeList = Topo.vector_Edge(4)
                internalLeftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt16, pnt15)
                internalLeftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt32, pnt31)
                internalLeftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt13, pnt29)
                internalLeftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt15, pnt31)
                internalLeftWire = Topo.WireTool.makeWire(internalLeftEdgeList, Geom.Precision.linear_Resolution())
                internalLeftFace = Topo.FaceTool.makeFace(internalLeftWire, Geom.Precision.linear_Resolution())
                faceList[9] = internalLeftFace

                #  Upper six faces
                upper1EdgeList = Topo.vector_Edge(4)
                upper1EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt18, pnt19)
                upper1EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt22, pnt23)
                upper1EdgeList[2] = Topo.EdgeTool.makeEdge(pnt17, pnt21)
                upper1EdgeList[3] = Topo.EdgeTool.makeEdge(pnt19, pnt23)
                upper1Wire = Topo.WireTool.makeWire(upper1EdgeList, Geom.Precision.linear_Resolution())
                upper1Face = Topo.FaceTool.makeFace(upper1Wire, Geom.Precision.linear_Resolution())
                faceList[10] = upper1Face

                upper2EdgeList = Topo.vector_Edge(4)
                upper2EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt20, pnt19)
                upper2EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt24, pnt23)
                upper2EdgeList[2] = Topo.EdgeTool.makeEdge(pnt17, pnt21)
                upper2EdgeList[3] = Topo.EdgeTool.makeEdge(pnt19, pnt23)
                upper2Wire = Topo.WireTool.makeWire(upper2EdgeList, Geom.Precision.linear_Resolution())
                upper2Face = Topo.FaceTool.makeFace(upper2Wire, Geom.Precision.linear_Resolution())
                faceList[11] = upper2Face

                upper3EdgeList = Topo.vector_Edge(4)
                upper3EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt22, pnt23)
                upper3EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt26, pnt27)
                upper3EdgeList[2] = Topo.EdgeTool.makeEdge(pnt21, pnt25)
                upper3EdgeList[3] = Topo.EdgeTool.makeEdge(pnt23, pnt27)
                upper3Wire = Topo.WireTool.makeWire(upper3EdgeList, Geom.Precision.linear_Resolution())
                upper3Face = Topo.FaceTool.makeFace(upper3Wire, Geom.Precision.linear_Resolution())
                faceList[12] = upper3Face

                upper4EdgeList = Topo.vector_Edge(4)
                upper4EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt24, pnt23)
                upper4EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt28, pnt27)
                upper4EdgeList[2] = Topo.EdgeTool.makeEdge(pnt21, pnt25)
                upper4EdgeList[3] = Topo.EdgeTool.makeEdge(pnt23, pnt27)
                upper4Wire = Topo.WireTool.makeWire(upper4EdgeList, Geom.Precision.linear_Resolution())
                upper4Face = Topo.FaceTool.makeFace(upper4Wire, Geom.Precision.linear_Resolution())
                faceList[13] = upper4Face

                upper5EdgeList = Topo.vector_Edge(4)
                upper5EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt26, pnt27)
                upper5EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt30, pnt31)
                upper5EdgeList[2] = Topo.EdgeTool.makeEdge(pnt25, pnt29)
                upper5EdgeList[3] = Topo.EdgeTool.makeEdge(pnt27, pnt31)
                upper5Wire = Topo.WireTool.makeWire(upper5EdgeList, Geom.Precision.linear_Resolution())
                upper5Face = Topo.FaceTool.makeFace(upper5Wire, Geom.Precision.linear_Resolution())
                faceList[14] = upper5Face

                upper6EdgeList = Topo.vector_Edge(4)
                upper6EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt28, pnt27)
                upper6EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt32, pnt31)
                upper6EdgeList[2] = Topo.EdgeTool.makeEdge(pnt25, pnt29)
                upper6EdgeList[3] = Topo.EdgeTool.makeEdge(pnt27, pnt31)
                upper6Wire = Topo.WireTool.makeWire(upper6EdgeList, Geom.Precision.linear_Resolution())
                upper6Face = Topo.FaceTool.makeFace(upper6Wire, Geom.Precision.linear_Resolution())
                faceList[15] = upper6Face

            advancedBrep = lx.AdvancedBrep.createIn(doc)

            shapeList = Topo.ShapeTool.makeShape(faceList)
            advancedBrep.setShape(shapeList)

            elem = lx.SubElement.createIn(doc)
            elem.setGeometry(advancedBrep)
            self.addSubElement(elem)
            print("added circle subelement")
        else:
            return

    def _createTape(self, tapeType):
        doc = self.getDocument()

        topRadius = self._topConeDiameter.getValue() * 0.5
        bottomRadius = self._bottomConeDiameter.getValue() * 0.5
        tapeRadius = 0.35
        coneHeight = self._ConeHeight.getValue()
        thickness = self._ConeThickness.getValue()
        topHeight = self._topHeight.getValue()
        xOffset = bottomRadius - topRadius

        if tapeType is 0:
            # hardElements = lx.vector_Element()
            # pnt1 = Geom.Pnt(0.025, 0.05, 0.0)
            # pnt2 = Geom.Pnt(0.0, 0.0705, 0.0)
            # pnt3 = Geom.Pnt(-0.025, 0.05, 0.0)
            # pnt4 = Geom.Pnt(-0.025, -0.05, 0.0)
            # pnt5 = Geom.Pnt(0.0, -0.0705, 0.0)
            # pnt6 = Geom.Pnt(0.025, -0.05, 0.0)
            #
            # pnt7 = Geom.Pnt(0.025, 0.05, 0.1)
            # pnt8 = Geom.Pnt(0.0, 0.0705, 0.1)
            # pnt9 = Geom.Pnt(-0.025, 0.05, 0.1)
            # pnt10 = Geom.Pnt(-0.025, -0.05, 0.1)
            # pnt11 = Geom.Pnt(0.0, -0.0705, 0.1)
            # pnt12 = Geom.Pnt(0.025, -0.05, 0.1)
            #
            # faceList = Topo.vector_Face(6)
            #
            # bottomEdgeList = Topo.vector_Edge(4)
            # bottomEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
            # bottomEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt4, pnt5, pnt6)
            # bottomEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt6)
            # bottomEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt4)
            # bottomWire = Topo.WireTool.makeWire(bottomEdgeList, Geom.Precision.linear_Resolution())
            # bottomFace = Topo.FaceTool.makeFace(bottomWire, Geom.Precision.linear_Resolution())
            # faceList[0] = bottomFace
            #
            # upperEdgeList = Topo.vector_Edge(4)
            # upperEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt8, pnt9)
            # upperEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt10, pnt11, pnt12)
            # upperEdgeList[2] = Topo.EdgeTool.makeEdge(pnt9, pnt10)
            # upperEdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt12)
            # upperWire = Topo.WireTool.makeWire(upperEdgeList, Geom.Precision.linear_Resolution())
            # upperFace = Topo.FaceTool.makeFace(upperWire, Geom.Precision.linear_Resolution())
            # faceList[1] = upperFace
            #
            # rightEdgeList = Topo.vector_Edge(4)
            # rightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
            # rightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt8, pnt9)
            # rightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt7)
            # rightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt9)
            # rightWire = Topo.WireTool.makeWire(rightEdgeList, Geom.Precision.linear_Resolution())
            # rightFace = Topo.FaceTool.makeFace(rightWire, Geom.Precision.linear_Resolution())
            # faceList[2] = rightFace
            #
            # leftEdgeList = Topo.vector_Edge(4)
            # leftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt4, pnt5, pnt6)
            # leftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt10, pnt11, pnt12)
            # leftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt4, pnt10)
            # leftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt6, pnt12)
            # leftWire = Topo.WireTool.makeWire(leftEdgeList, Geom.Precision.linear_Resolution())
            # leftFace = Topo.FaceTool.makeFace(leftWire, Geom.Precision.linear_Resolution())
            # faceList[3] = leftFace
            #
            # frontEdgeList = Topo.vector_Edge(4)
            # frontEdgeList[1] = Topo.EdgeTool.makeEdge(pnt6, pnt1)
            # frontEdgeList[0] = Topo.EdgeTool.makeEdge(pnt1, pnt7)
            # frontEdgeList[2] = Topo.EdgeTool.makeEdge(pnt7, pnt12)
            # frontEdgeList[3] = Topo.EdgeTool.makeEdge(pnt12, pnt6)
            # frontWire = Topo.WireTool.makeWire(frontEdgeList, Geom.Precision.linear_Resolution())
            # frontFace = Topo.FaceTool.makeFace(frontWire, Geom.Precision.linear_Resolution())
            # faceList[4] = frontFace
            #
            # backEdgeList = Topo.vector_Edge(4)
            # backEdgeList[1] = Topo.EdgeTool.makeEdge(pnt3, pnt9)
            # backEdgeList[0] = Topo.EdgeTool.makeEdge(pnt9, pnt10)
            # backEdgeList[2] = Topo.EdgeTool.makeEdge(pnt10, pnt4)
            # backEdgeList[3] = Topo.EdgeTool.makeEdge(pnt4, pnt3)
            # backWire = Topo.WireTool.makeWire(backEdgeList, Geom.Precision.linear_Resolution())
            # backFace = Topo.FaceTool.makeFace(backWire, Geom.Precision.linear_Resolution())
            # faceList[5] = backFace
            # advancedBrep = lx.AdvancedBrep.createIn(doc)
            # shapeList = Topo.ShapeTool.makeShape(faceList)
            # advancedBrep.setShape(shapeList)
            #
            # hardElem = lx.Element.createIn(doc)
            # hardElem.setGeometry(advancedBrep)
            # # hardElements.push_back(hardElem)
            #
            # profile = lx.CircleProfileDef.createIn(doc)
            # profile.setRadius(tapeRadius)
            # eas = lx.ExtrudedAreaSolid.createIn(doc)
            # eas.setSweptArea(profile)
            # eas.setExtrudedDirection(Geom.Dir(0, 0, 1))
            # eas.setDepth(0.03)
            #
            # tapeElement = lx.Element.createIn(doc)
            # tapeElement.setGeometry(eas)

            holeCylinder = lx.RightCircularCylinder.createIn(doc)
            holeCylinder.setHeight(0.1)
            holeCylinder.setRadius(0.02)
            hardElement = lx.Element.createIn(doc)
            hardElement.setGeometry(holeCylinder)

            tapeCylinder = lx.RightCircularCylinder.createIn(doc)
            tapeCylinder.setHeight(0.03)
            tapeCylinder.setRadius(0.35)
            tapeElement = lx.Element.createIn(doc)
            tapeElement.setGeometry(tapeCylinder)

            print("Preparing to CUT...")
            resultingCylinders = lx.vector_Element()
            if lx.bop_cut(tapeElement, hardElement, resultingCylinders) != 0:
                print("Error in cut")

            transform = resultingCylinders[0].getTransform()
            geometry = resultingCylinders[0].getGeometry()
            print("Getting transf and geom of resulting elem...")

            doc.removeObject(tapeElement)
            doc.removeObject(hardElement)

            finishedTape = lx.SubElement.createIn(doc)
            finishedTape.setTransform(transform)
            finishedTape.setGeometry(geometry)

            translateVector = Geom.Vec(0.0, 0.0, coneHeight + topHeight - 0.05)
            finishedTape.translate(translateVector, Geom.CoordSpace_WCS)
            self.addSubElement(finishedTape)

        elif tapeType is 1:
            hardElements = lx.vector_Element()

            # ---------------------------------------------------------------
            holeCylinder = lx.RightCircularCylinder.createIn(doc)
            holeCylinder.setHeight(0.1)
            holeCylinder.setRadius(0.02)
            hElement1 = lx.Element.createIn(doc)
            hElement1.setGeometry(holeCylinder)
            hardElements.push_back(hElement1)
            print("Greated geometry and pushed first element")

            hElement2 = lx.Element.createIn(doc)
            hElement2.setGeometry(holeCylinder)
            hElement2.translate(Geom.Vec(0.2, 0.0, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement2)

            # hElement22 = lx.Element.createIn(doc)
            # hElement22.setGeometry(holeCylinder)
            # hElement22.translate(Geom.Vec(0.1, 0.0, 0.0), Geom.CoordSpace_WCS)
            # hardElements.push_back(hElement22)
            print("Greated geometry and pushed 2nd element")

            hElement3 = lx.Element.createIn(doc)
            hElement3.setGeometry(holeCylinder)
            hElement3.translate(Geom.Vec(0.2, 0.2, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement3)

            hElement33 = lx.Element.createIn(doc)
            hElement33.setGeometry(holeCylinder)
            hElement33.translate(Geom.Vec(0.1, 0.1, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement33)
            print("Greated geometry and pushed 3rd element")

            hElement4 = lx.Element.createIn(doc)
            hElement4.setGeometry(holeCylinder)
            hElement4.translate(Geom.Vec(0.0, 0.2, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement4)

            # hElement44 = lx.Element.createIn(doc)
            # hElement44.setGeometry(holeCylinder)
            # hElement44.translate(Geom.Vec(0.0, 0.1, 0.0), Geom.CoordSpace_WCS)
            # hardElements.push_back(hElement44)
            print("Greated geometry and pushed 4th element")

            hElement5 = lx.Element.createIn(doc)
            hElement5.setGeometry(holeCylinder)
            hElement5.translate(Geom.Vec(-0.2, 0.2, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement5)

            hElement55 = lx.Element.createIn(doc)
            hElement55.setGeometry(holeCylinder)
            hElement55.translate(Geom.Vec(-0.1, 0.1, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement55)
            print("Greated geometry and pushed 5th element")

            hElement6 = lx.Element.createIn(doc)
            hElement6.setGeometry(holeCylinder)
            hElement6.translate(Geom.Vec(-0.2, 0.0, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement6)
            print("Greated geometry and pushed 6th element")

            hElement7 = lx.Element.createIn(doc)
            hElement7.setGeometry(holeCylinder)
            hElement7.translate(Geom.Vec(-0.2, -0.2, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement7)

            hElement77 = lx.Element.createIn(doc)
            hElement77.setGeometry(holeCylinder)
            hElement77.translate(Geom.Vec(-0.1, -0.1, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement77)
            print("Greated geometry and pushed 7th element")

            hElement8 = lx.Element.createIn(doc)
            hElement8.setGeometry(holeCylinder)
            hElement8.translate(Geom.Vec(0.0, -0.2, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement8)
            print("Greated geometry and pushed 8th element")

            hElement9 = lx.Element.createIn(doc)
            hElement9.setGeometry(holeCylinder)
            hElement9.translate(Geom.Vec(0.2, -0.2, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement9)

            hElement99 = lx.Element.createIn(doc)
            hElement99.setGeometry(holeCylinder)
            hElement99.translate(Geom.Vec(0.1, -0.1, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(hElement99)
            print("Greated geometry and pushed 9th element")
            # ----------------------------------------------------------------

            tapeCylinder = lx.RightCircularCylinder.createIn(doc)
            tapeCylinder.setHeight(0.03)
            tapeCylinder.setRadius(0.35)
            tapeElement = lx.Element.createIn(doc)
            tapeElement.setGeometry(tapeCylinder)
            print("Created tapeElement")
            print("Creating resultingCylinders vector")
            resultingCylinders = lx.vector_Element()

            print("Preparing to cut the tapeElement")
            if lx.bop_cut(tapeElement, hardElements, resultingCylinders) != 0:
                print("Error in cut")
            print("Starting to remove used elements")
            doc.removeObject(hElement1)
            doc.removeObject(hElement2)
            doc.removeObject(hElement3)
            doc.removeObject(hElement33)
            doc.removeObject(hElement4)
            doc.removeObject(hElement5)
            doc.removeObject(hElement55)
            doc.removeObject(hElement6)
            doc.removeObject(hElement7)
            doc.removeObject(hElement77)
            doc.removeObject(hElement8)
            doc.removeObject(hElement9)
            doc.removeObject(hElement99)
            doc.removeObject(tapeElement)
            print("Removed used elements...")
            transform = resultingCylinders[0].getTransform()
            geometry = resultingCylinders[0].getGeometry()

            tapeElem = lx.SubElement.createIn(doc)
            tapeElem.setTransform(transform)
            tapeElem.setGeometry(geometry)
            print("Set geometry and transform to subElement...")
            translateVector = Geom.Vec(0.0, 0.0, coneHeight + topHeight - 0.05)
            tapeElem.translate(translateVector, Geom.CoordSpace_WCS)
            print("the \"tapeElem\" has been translated...")
            print("Adding a subelement to main Element...")
            self.addSubElement(tapeElem)
            print("DONE...")

        elif tapeType is 2:
            # Larger hElem
            print("In create type function() -> elif tapeType is 2:")
            pnt1 = Geom.Pnt(0.025, 0.17, 0.0)
            pnt2 = Geom.Pnt(0.0, 0.2, 0.0)
            pnt3 = Geom.Pnt(-0.025, 0.17, 0.0)
            pnt4 = Geom.Pnt(-0.025, -0.17, 0.0)
            pnt5 = Geom.Pnt(0.0, -0.2, 0.0)
            pnt6 = Geom.Pnt(0.025, -0.17, 0.0)

            pnt7  = Geom.Pnt(0.025, 0.17, 0.1)
            pnt8  = Geom.Pnt(0.0, 0.2, 0.1)
            pnt9  = Geom.Pnt(-0.025, 0.17, 0.1)
            pnt10 = Geom.Pnt(-0.025, -0.17, 0.1)
            pnt11 = Geom.Pnt(0.0, -0.2, 0.1)
            pnt12 = Geom.Pnt(0.025, -0.17, 0.1)

            faceList = Topo.vector_Face(6)

            bottomEdgeList = Topo.vector_Edge(4)
            bottomEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
            bottomEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt4, pnt5, pnt6)
            bottomEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt6)
            bottomEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt4)
            bottomWire = Topo.WireTool.makeWire(bottomEdgeList, Geom.Precision.linear_Resolution())
            bottomFace = Topo.FaceTool.makeFace(bottomWire, Geom.Precision.linear_Resolution())
            faceList[0] = bottomFace

            upperEdgeList = Topo.vector_Edge(4)
            upperEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt8, pnt9)
            upperEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt10, pnt11, pnt12)
            upperEdgeList[2] = Topo.EdgeTool.makeEdge(pnt9, pnt10)
            upperEdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt12)
            upperWire = Topo.WireTool.makeWire(upperEdgeList, Geom.Precision.linear_Resolution())
            upperFace = Topo.FaceTool.makeFace(upperWire, Geom.Precision.linear_Resolution())
            faceList[1] = upperFace

            rightEdgeList = Topo.vector_Edge(4)
            rightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
            rightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt8, pnt9)
            rightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt7)
            rightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt9)
            rightWire = Topo.WireTool.makeWire(rightEdgeList, Geom.Precision.linear_Resolution())
            rightFace = Topo.FaceTool.makeFace(rightWire, Geom.Precision.linear_Resolution())
            faceList[2] = rightFace

            leftEdgeList = Topo.vector_Edge(4)
            leftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt4, pnt5, pnt6)
            leftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt10, pnt11, pnt12)
            leftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt4, pnt10)
            leftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt6, pnt12)
            leftWire = Topo.WireTool.makeWire(leftEdgeList, Geom.Precision.linear_Resolution())
            leftFace = Topo.FaceTool.makeFace(leftWire, Geom.Precision.linear_Resolution())
            faceList[3] = leftFace

            frontEdgeList = Topo.vector_Edge(4)
            frontEdgeList[1] = Topo.EdgeTool.makeEdge(pnt6, pnt1)
            frontEdgeList[0] = Topo.EdgeTool.makeEdge(pnt1, pnt7)
            frontEdgeList[2] = Topo.EdgeTool.makeEdge(pnt7, pnt12)
            frontEdgeList[3] = Topo.EdgeTool.makeEdge(pnt12, pnt6)
            frontWire = Topo.WireTool.makeWire(frontEdgeList, Geom.Precision.linear_Resolution())
            frontFace = Topo.FaceTool.makeFace(frontWire, Geom.Precision.linear_Resolution())
            faceList[4] = frontFace

            backEdgeList = Topo.vector_Edge(4)
            backEdgeList[1] = Topo.EdgeTool.makeEdge(pnt3, pnt9)
            backEdgeList[0] = Topo.EdgeTool.makeEdge(pnt9, pnt10)
            backEdgeList[2] = Topo.EdgeTool.makeEdge(pnt10, pnt4)
            backEdgeList[3] = Topo.EdgeTool.makeEdge(pnt4, pnt3)
            backWire = Topo.WireTool.makeWire(backEdgeList, Geom.Precision.linear_Resolution())
            backFace = Topo.FaceTool.makeFace(backWire, Geom.Precision.linear_Resolution())
            faceList[5] = backFace

            hardElements = lx.vector_Element()

            advancedBrep = lx.AdvancedBrep.createIn(doc)
            shapeList = Topo.ShapeTool.makeShape(faceList)
            advancedBrep.setShape(shapeList)

            hardElem = lx.Element.createIn(doc)
            hardElem.setGeometry(advancedBrep)
            hardElements.push_back(hardElem)
            print("Created center hard element...")

            leftHardElement = lx.Element.createIn(doc)
            leftHardElement.setGeometry(advancedBrep)
            leftHardElement.translate(Geom.Vec(0.1, 0.0, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(leftHardElement)
            print("Created left Hard element...")

            leftEndHardElement = lx.Element.createIn(doc)
            leftEndHardElement.setGeometry(advancedBrep)
            leftEndHardElement.translate(Geom.Vec(0.2, 0.0, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(leftEndHardElement)

            rightHardElement = lx.Element.createIn(doc)
            rightHardElement.setGeometry(advancedBrep)
            rightHardElement.translate(Geom.Vec(-0.1, 0.0, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(rightHardElement)
            print("Created right hard element...")

            rightEndHardElement = lx.Element.createIn(doc)
            rightEndHardElement.setGeometry(advancedBrep)
            rightEndHardElement.translate(Geom.Vec(-0.2, 0.0, 0.0), Geom.CoordSpace_WCS)
            hardElements.push_back(rightEndHardElement)

            #  Soft element
            tapeCylinder = lx.RightCircularCylinder.createIn(doc)
            tapeCylinder.setHeight(0.03)
            tapeCylinder.setRadius(0.35)
            tapeElement = lx.Element.createIn(doc)
            tapeElement.setGeometry(tapeCylinder)
            print("Created tapeElement")
            print("Creating resultingCylinders vector")

            print("Preparing to CUT...")
            resultingCylinders = lx.vector_Element()
            if lx.bop_cut(tapeElement, hardElements, resultingCylinders) != 0:
                print("Error in cut")

            transform = resultingCylinders[0].getTransform()
            geometry = resultingCylinders[0].getGeometry()
            print("Getting transf and geom of resulting elem...")

            doc.removeObject(leftHardElement)
            doc.removeObject(rightHardElement)
            doc.removeObject(tapeElement)
            doc.removeObject(hardElem)
            doc.removeObject(rightEndHardElement)
            doc.removeObject(leftEndHardElement)

            finishedTape = lx.SubElement.createIn(doc)
            finishedTape.setTransform(transform)
            finishedTape.setGeometry(geometry)

            print("Set geometry and transform to subElement...")
            translateVector = Geom.Vec(0.0, 0.0, coneHeight + topHeight - 0.05)
            finishedTape.translate(translateVector, Geom.CoordSpace_WCS)
            print("the \"tapeElem\" has been translated...")
            print("Adding a subelement to main Element...")
            self.addSubElement(finishedTape)
            print("DONE...")

    def _createOverConePart(self):
        doc = self.getDocument()

        topRadius = self._topConeDiameter.getValue() * 0.5
        bottomRadius = self._bottomConeDiameter.getValue() * 0.5
        coneHeight = self._ConeHeight.getValue()
        thickness = self._ConeThickness.getValue()
        topHeight = self._topHeight.getValue()
        # xOffset = bottomRadius - topRadius

        # pnt1 = Geom.Pnt(xOffset, -topRadius, coneHeight)
        # pnt2 = Geom.Pnt(xOffset + topRadius, 0.0, coneHeight)
        # pnt3 = Geom.Pnt(xOffset, topRadius, coneHeight)
        # pnt4 = Geom.Pnt(xOffset - topRadius, 0.0, coneHeight)
        #
        # pnt5 = Geom.Pnt(xOffset, -topRadius - thickness, coneHeight)
        # pnt6 = Geom.Pnt(xOffset + topRadius + thickness, 0.0, coneHeight)
        # pnt7 = Geom.Pnt(xOffset, topRadius + thickness, coneHeight)
        # pnt8 = Geom.Pnt(xOffset - topRadius - thickness, 0.0, coneHeight)
        #
        # pnt9 = Geom.Pnt(xOffset, -topRadius, coneHeight + topHeight)
        # pnt10 = Geom.Pnt(xOffset + topRadius, 0.0, coneHeight + topHeight)
        # pnt11 = Geom.Pnt(xOffset, topRadius, coneHeight + topHeight)
        # pnt12 = Geom.Pnt(xOffset - topRadius, 0.0, coneHeight + topHeight)
        #
        # pnt13 = Geom.Pnt(xOffset, -topRadius - thickness, coneHeight + topHeight)
        # pnt14 = Geom.Pnt(xOffset + topRadius + thickness, 0.0, coneHeight + topHeight)
        # pnt15 = Geom.Pnt(xOffset, topRadius + thickness, coneHeight + topHeight)
        # pnt16 = Geom.Pnt(xOffset - topRadius - thickness, 0.0, coneHeight + topHeight)
        #  _______________
        pnt1 = Geom.Pnt(0.0, - bottomRadius - thickness, coneHeight)
        pnt2 = Geom.Pnt(bottomRadius + thickness, 0.0, coneHeight)
        pnt3 = Geom.Pnt(0.0, bottomRadius + thickness, coneHeight)
        pnt4 = Geom.Pnt(-bottomRadius - thickness, 0.0, coneHeight)

        pnt5 = Geom.Pnt(0.0, - bottomRadius - thickness * 0.5, coneHeight)
        pnt6 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, coneHeight)
        pnt7 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, coneHeight)
        pnt8 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, coneHeight)

        pnt9 = Geom.Pnt(0.0, - bottomRadius - thickness * 0.5, coneHeight + thickness * 0.5)
        pnt10 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, coneHeight + thickness * 0.5)
        pnt11 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, coneHeight + thickness * 0.5)
        pnt12 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, coneHeight + thickness * 0.5)

        pnt13 = Geom.Pnt(0.0, - bottomRadius, coneHeight + thickness * 0.5)
        pnt14 = Geom.Pnt(bottomRadius, 0.0, coneHeight + thickness * 0.5)
        pnt15 = Geom.Pnt(0.0, bottomRadius, coneHeight + thickness * 0.5)
        pnt16 = Geom.Pnt(-bottomRadius, 0.0, coneHeight + thickness * 0.5)

        # xOffset = bottomRadius - topRadius

        pnt17 = Geom.Pnt(0.0, - topRadius - thickness, coneHeight + topHeight)
        pnt18 = Geom.Pnt(topRadius + thickness, 0.0, coneHeight + topHeight)
        pnt19 = Geom.Pnt(0.0, topRadius + thickness, coneHeight + topHeight)
        pnt20 = Geom.Pnt(-topRadius - thickness, 0.0, coneHeight + topHeight)

        # pnt21 = Geom.Pnt(0.0, - topRadius - thickness * 0.5, coneHeight + topHeight)
        # pnt22 = Geom.Pnt(topRadius + thickness * 0.5, 0.0, coneHeight + topHeight)
        # pnt23 = Geom.Pnt(0.0, topRadius + thickness * 0.5, coneHeight + topHeight)
        # pnt24 = Geom.Pnt(-topRadius - thickness * 0.5, 0.0, coneHeight + topHeight)
        #
        # pnt25 = Geom.Pnt(0.0, - topRadius - thickness * 0.5, coneHeight + topHeight - 0.05)
        # pnt26 = Geom.Pnt(topRadius + thickness * 0.5, 0.0, coneHeight + topHeight - 0.05)
        # pnt27 = Geom.Pnt(0.0, topRadius + thickness * 0.5, coneHeight + topHeight - 0.05)
        # pnt28 = Geom.Pnt(-topRadius - thickness * 0.5, 0.0, coneHeight + topHeight - 0.05)
        #
        # pnt29 = Geom.Pnt(0.0, - topRadius, coneHeight + topHeight - 0.05)
        # pnt30 = Geom.Pnt(topRadius, 0.0, coneHeight + topHeight - 0.05)
        # pnt31 = Geom.Pnt(0.0, topRadius, coneHeight + topHeight - 0.05)
        # pnt32 = Geom.Pnt(-topRadius, 0.0, coneHeight + topHeight - 0.05)

        pnt21 = Geom.Pnt(0.0, - 0.35, coneHeight + topHeight)
        pnt22 = Geom.Pnt(0.35, 0.0, coneHeight + topHeight)
        pnt23 = Geom.Pnt(0.0, 0.35, coneHeight + topHeight)
        pnt24 = Geom.Pnt(-0.35, 0.0, coneHeight + topHeight)

        pnt25 = Geom.Pnt(0.0, - 0.35, coneHeight + topHeight - 0.05)
        pnt26 = Geom.Pnt(0.35, 0.0, coneHeight + topHeight - 0.05)
        pnt27 = Geom.Pnt(0.0, 0.35, coneHeight + topHeight - 0.05)
        pnt28 = Geom.Pnt(-0.35, 0.0, coneHeight + topHeight - 0.05)

        pnt29 = Geom.Pnt(0.0, - topRadius, coneHeight + topHeight - 0.05)
        pnt30 = Geom.Pnt(topRadius, 0.0, coneHeight + topHeight - 0.05)
        pnt31 = Geom.Pnt(0.0, topRadius, coneHeight + topHeight - 0.05)
        pnt32 = Geom.Pnt(-topRadius, 0.0, coneHeight + topHeight - 0.05)

        faceList = Topo.vector_Face(16)

        #  Bottom six planes
        bottom1EdgeList = Topo.vector_Edge(4)
        bottom1EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
        bottom1EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
        bottom1EdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
        bottom1EdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
        bottom1Wire = Topo.WireTool.makeWire(bottom1EdgeList, Geom.Precision.linear_Resolution())
        bottom1Face = Topo.FaceTool.makeFace(bottom1Wire, Geom.Precision.linear_Resolution())
        faceList[0] = bottom1Face

        bottom2EdgeList = Topo.vector_Edge(4)
        bottom2EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt4, pnt3)
        bottom2EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt8, pnt7)
        bottom2EdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
        bottom2EdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
        bottom2Wire = Topo.WireTool.makeWire(bottom2EdgeList, Geom.Precision.linear_Resolution())
        bottom2Face = Topo.FaceTool.makeFace(bottom2Wire, Geom.Precision.linear_Resolution())
        faceList[1] = bottom2Face

        bottom3EdgeList = Topo.vector_Edge(4)
        bottom3EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
        bottom3EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt10, pnt11)
        bottom3EdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt9)
        bottom3EdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt11)
        bottom3Wire = Topo.WireTool.makeWire(bottom3EdgeList, Geom.Precision.linear_Resolution())
        bottom3Face = Topo.FaceTool.makeFace(bottom3Wire, Geom.Precision.linear_Resolution())
        faceList[2] = bottom3Face

        bottom4EdgeList = Topo.vector_Edge(4)
        bottom4EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt8, pnt7)
        bottom4EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt12, pnt11)
        bottom4EdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt9)
        bottom4EdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt11)
        bottom4Wire = Topo.WireTool.makeWire(bottom4EdgeList, Geom.Precision.linear_Resolution())
        bottom4Face = Topo.FaceTool.makeFace(bottom4Wire, Geom.Precision.linear_Resolution())
        faceList[3] = bottom4Face

        bottom5EdgeList = Topo.vector_Edge(4)
        bottom5EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt10, pnt11)
        bottom5EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt14, pnt15)
        bottom5EdgeList[2] = Topo.EdgeTool.makeEdge(pnt9, pnt13)
        bottom5EdgeList[3] = Topo.EdgeTool.makeEdge(pnt11, pnt15)
        bottom5Wire = Topo.WireTool.makeWire(bottom5EdgeList, Geom.Precision.linear_Resolution())
        bottom5Face = Topo.FaceTool.makeFace(bottom5Wire, Geom.Precision.linear_Resolution())
        faceList[4] = bottom5Face

        bottom6EdgeList = Topo.vector_Edge(4)
        bottom6EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt12, pnt11)
        bottom6EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt16, pnt15)
        bottom6EdgeList[2] = Topo.EdgeTool.makeEdge(pnt9, pnt13)
        bottom6EdgeList[3] = Topo.EdgeTool.makeEdge(pnt11, pnt15)
        bottom6Wire = Topo.WireTool.makeWire(bottom6EdgeList, Geom.Precision.linear_Resolution())
        bottom6Face = Topo.FaceTool.makeFace(bottom6Wire, Geom.Precision.linear_Resolution())
        faceList[5] = bottom6Face

        #  External planes
        externalLeftEdgeList = Topo.vector_Edge(4)
        externalLeftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt4, pnt3)
        externalLeftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt20, pnt19)
        externalLeftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt17)
        externalLeftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt19)
        externalLeftWire = Topo.WireTool.makeWire(externalLeftEdgeList, Geom.Precision.linear_Resolution())
        externalLeftFace = Topo.FaceTool.makeFace(externalLeftWire, Geom.Precision.linear_Resolution())
        faceList[6] = externalLeftFace

        externalRightEdgeList = Topo.vector_Edge(4)
        externalRightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
        externalRightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt18, pnt19)
        externalRightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt17)
        externalRightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt19)
        externalRightWire = Topo.WireTool.makeWire(externalRightEdgeList, Geom.Precision.linear_Resolution())
        externalRightFace = Topo.FaceTool.makeFace(externalRightWire, Geom.Precision.linear_Resolution())
        faceList[7] = externalRightFace

        #  Internal planes
        internalRightEdgeList = Topo.vector_Edge(4)
        internalRightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt14, pnt15)
        internalRightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt30, pnt31)
        internalRightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt13, pnt29)
        internalRightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt15, pnt31)
        internalRightWire = Topo.WireTool.makeWire(internalRightEdgeList, Geom.Precision.linear_Resolution())
        internalRightFace = Topo.FaceTool.makeFace(internalRightWire, Geom.Precision.linear_Resolution())
        faceList[8] = internalRightFace

        internalLeftEdgeList = Topo.vector_Edge(4)
        internalLeftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt16, pnt15)
        internalLeftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt32, pnt31)
        internalLeftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt13, pnt29)
        internalLeftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt15, pnt31)
        internalLeftWire = Topo.WireTool.makeWire(internalLeftEdgeList, Geom.Precision.linear_Resolution())
        internalLeftFace = Topo.FaceTool.makeFace(internalLeftWire, Geom.Precision.linear_Resolution())
        faceList[9] = internalLeftFace

        #  Upper six faces
        upper1EdgeList = Topo.vector_Edge(4)
        upper1EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt18, pnt19)
        upper1EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt22, pnt23)
        upper1EdgeList[2] = Topo.EdgeTool.makeEdge(pnt17, pnt21)
        upper1EdgeList[3] = Topo.EdgeTool.makeEdge(pnt19, pnt23)
        upper1Wire = Topo.WireTool.makeWire(upper1EdgeList, Geom.Precision.linear_Resolution())
        upper1Face = Topo.FaceTool.makeFace(upper1Wire, Geom.Precision.linear_Resolution())
        faceList[10] = upper1Face

        upper2EdgeList = Topo.vector_Edge(4)
        upper2EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt20, pnt19)
        upper2EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt24, pnt23)
        upper2EdgeList[2] = Topo.EdgeTool.makeEdge(pnt17, pnt21)
        upper2EdgeList[3] = Topo.EdgeTool.makeEdge(pnt19, pnt23)
        upper2Wire = Topo.WireTool.makeWire(upper2EdgeList, Geom.Precision.linear_Resolution())
        upper2Face = Topo.FaceTool.makeFace(upper2Wire, Geom.Precision.linear_Resolution())
        faceList[11] = upper2Face

        upper3EdgeList = Topo.vector_Edge(4)
        upper3EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt22, pnt23)
        upper3EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt26, pnt27)
        upper3EdgeList[2] = Topo.EdgeTool.makeEdge(pnt21, pnt25)
        upper3EdgeList[3] = Topo.EdgeTool.makeEdge(pnt23, pnt27)
        upper3Wire = Topo.WireTool.makeWire(upper3EdgeList, Geom.Precision.linear_Resolution())
        upper3Face = Topo.FaceTool.makeFace(upper3Wire, Geom.Precision.linear_Resolution())
        faceList[12] = upper3Face

        upper4EdgeList = Topo.vector_Edge(4)
        upper4EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt24, pnt23)
        upper4EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt28, pnt27)
        upper4EdgeList[2] = Topo.EdgeTool.makeEdge(pnt21, pnt25)
        upper4EdgeList[3] = Topo.EdgeTool.makeEdge(pnt23, pnt27)
        upper4Wire = Topo.WireTool.makeWire(upper4EdgeList, Geom.Precision.linear_Resolution())
        upper4Face = Topo.FaceTool.makeFace(upper4Wire, Geom.Precision.linear_Resolution())
        faceList[13] = upper4Face

        upper5EdgeList = Topo.vector_Edge(4)
        upper5EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt26, pnt27)
        upper5EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt30, pnt31)
        upper5EdgeList[2] = Topo.EdgeTool.makeEdge(pnt25, pnt29)
        upper5EdgeList[3] = Topo.EdgeTool.makeEdge(pnt27, pnt31)
        upper5Wire = Topo.WireTool.makeWire(upper5EdgeList, Geom.Precision.linear_Resolution())
        upper5Face = Topo.FaceTool.makeFace(upper5Wire, Geom.Precision.linear_Resolution())
        faceList[14] = upper5Face

        upper6EdgeList = Topo.vector_Edge(4)
        upper6EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt28, pnt27)
        upper6EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt32, pnt31)
        upper6EdgeList[2] = Topo.EdgeTool.makeEdge(pnt25, pnt29)
        upper6EdgeList[3] = Topo.EdgeTool.makeEdge(pnt27, pnt31)
        upper6Wire = Topo.WireTool.makeWire(upper6EdgeList, Geom.Precision.linear_Resolution())
        upper6Face = Topo.FaceTool.makeFace(upper6Wire, Geom.Precision.linear_Resolution())
        faceList[15] = upper6Face

        advancedBrep = lx.AdvancedBrep.createIn(doc)
        shapeList = Topo.ShapeTool.makeShape(faceList)
        advancedBrep.setShape(shapeList)

        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(advancedBrep)
        self.addSubElement(elem)

    def _createBase(self, zCoordinate, baseType):
        print(" in _createBase() method...")
        doc = self.getDocument()

        baseHeight = self._baseHeight.getValue()
        baseRadius = self._baseDiameter.getValue() * 0.5
        # thickness = self._ConeThickness.getValue()
        halfBaseLength = self._baseLength.getValue() * 0.5
        print("half base length is: ", halfBaseLength)

        if baseType is 0:
            pnt1 = Geom.Pnt(0.0, -baseRadius, zCoordinate - baseHeight)
            pnt2 = Geom.Pnt(baseRadius, 0.0, zCoordinate - baseHeight)
            pnt3 = Geom.Pnt(0.0, baseRadius, zCoordinate - baseHeight)
            pnt4 = Geom.Pnt(-baseRadius, 0.0, zCoordinate - baseHeight)

            pnt5 = Geom.Pnt(0.0, -baseRadius, zCoordinate)
            pnt6 = Geom.Pnt(baseRadius, 0.0, zCoordinate)
            pnt7 = Geom.Pnt(0.0, baseRadius, zCoordinate)
            pnt8 = Geom.Pnt(-baseRadius, 0.0, zCoordinate)

            faceList = Topo.vector_Face(4)

            # bottomLeft
            topEdgeList = Topo.vector_Edge(2)
            topEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
            topEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt8, pnt5)
            # topEdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt7)
            # topEdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt5)
            topWire = Topo.WireTool.makeWire(topEdgeList, Geom.Precision.linear_Resolution())
            topFace = Topo.FaceTool.makeFace(topWire, Geom.Precision.linear_Resolution())
            faceList[0] = topFace

            bottomEdgeList = Topo.vector_Edge(2)
            bottomEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
            bottomEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt3, pnt4, pnt1)
            # bottomEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt3)
            # bottomEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt1)
            bottomWire = Topo.WireTool.makeWire(bottomEdgeList, Geom.Precision.linear_Resolution())
            bottomFace = Topo.FaceTool.makeFace(bottomWire, Geom.Precision.linear_Resolution())
            faceList[1] = bottomFace

            leftEdgeList = Topo.vector_Edge(4)
            leftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt4, pnt3)
            leftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt8, pnt5)
            leftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
            leftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt5, pnt1)
            leftWire = Topo.WireTool.makeWire(leftEdgeList, Geom.Precision.linear_Resolution())
            leftFace = Topo.FaceTool.makeFace(leftWire, Geom.Precision.linear_Resolution())
            faceList[2] = leftFace

            rightEdgeList = Topo.vector_Edge(4)
            rightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
            rightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt6, pnt5)
            rightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
            rightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt5, pnt1)
            rightWire = Topo.WireTool.makeWire(rightEdgeList, Geom.Precision.linear_Resolution())
            rightFace = Topo.FaceTool.makeFace(rightWire, Geom.Precision.linear_Resolution())
            faceList[3] = rightFace

            advancedBrep = lx.AdvancedBrep.createIn(doc)

            shapeList = Topo.ShapeTool.makeShape(faceList)
            print("circle shape list - ", shapeList)
            print("making face of the circle base")
            advancedBrep.setShape(shapeList)
            print("setting the shape of the circle base")

            elem = lx.SubElement.createIn(doc)
            print("created subelement of circle base")
            elem.setGeometry(advancedBrep)
            print("created geom of circle base")
            self.addSubElement(elem)
            print("added a circle base sub element")
            print(" ")

        elif baseType is 1:
            pnt1 = Geom.Pnt(halfBaseLength, -halfBaseLength, zCoordinate - baseHeight)
            pnt2 = Geom.Pnt(halfBaseLength, halfBaseLength, zCoordinate - baseHeight)
            pnt3 = Geom.Pnt(-halfBaseLength, halfBaseLength, zCoordinate - baseHeight)
            pnt4 = Geom.Pnt(-halfBaseLength, -halfBaseLength, zCoordinate - baseHeight)

            # pnt5 = Geom.Pnt(halfBaseLength, -halfBaseLength, zCoordinate)
            # pnt6 = Geom.Pnt(halfBaseLength, halfBaseLength, zCoordinate)
            # pnt7 = Geom.Pnt(-halfBaseLength, halfBaseLength, zCoordinate)
            # pnt8 = Geom.Pnt(-halfBaseLength, -halfBaseLength, zCoordinate)
            #
            # model = FacetedModelAssembler(doc)

            self.addSubElement(FacetedModelAssembler.createExtrudedSubElement([pnt1, pnt2, pnt3, pnt4], baseHeight,
                                                           Geom.Dir(0.0, 0.0, 1.0)))
            # faceList = Topo.vector_Face(6)
            #
            # #  Bottom
            # bottomEdgeList = Topo.vector_Edge(4)
            # bottomEdgeList[0] = Topo.EdgeTool.makeEdge(pnt1, pnt4)
            # bottomEdgeList[1] = Topo.EdgeTool.makeEdge(pnt4, pnt3)
            # bottomEdgeList[2] = Topo.EdgeTool.makeEdge(pnt3, pnt2)
            # bottomEdgeList[3] = Topo.EdgeTool.makeEdge(pnt2, pnt1)
            # bottomWire = Topo.WireTool.makeWire(bottomEdgeList, Geom.Precision.linear_Resolution())
            # bottomFace = Topo.FaceTool.makeFace(bottomWire, Geom.Precision.linear_Resolution())
            # faceList[0] = bottomFace
            #
            # #  Upper
            # topEdgeList = Topo.vector_Edge(4)
            # topEdgeList[0] = Topo.EdgeTool.makeEdge(pnt5, pnt6)
            # topEdgeList[1] = Topo.EdgeTool.makeEdge(pnt6, pnt7)
            # topEdgeList[2] = Topo.EdgeTool.makeEdge(pnt7, pnt8)
            # topEdgeList[3] = Topo.EdgeTool.makeEdge(pnt8, pnt5)
            # topWire = Topo.WireTool.makeWire(topEdgeList, Geom.Precision.linear_Resolution())
            # topFace = Topo.FaceTool.makeFace(topWire, Geom.Precision.linear_Resolution())
            # faceList[1] = topFace
            #
            # # right
            # rightEdgeList = Topo.vector_Edge(4)
            # rightEdgeList[0] = Topo.EdgeTool.makeEdge(pnt1, pnt2)
            # rightEdgeList[1] = Topo.EdgeTool.makeEdge(pnt2, pnt6)
            # rightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt6, pnt5)
            # rightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt5, pnt1)
            # rightWire = Topo.WireTool.makeWire(rightEdgeList, Geom.Precision.linear_Resolution())
            # rightFace = Topo.FaceTool.makeFace(rightWire, Geom.Precision.linear_Resolution())
            # faceList[2] = rightFace
            #
            # leftEdgeList = Topo.vector_Edge(4)
            # leftEdgeList[0] = Topo.EdgeTool.makeEdge(pnt3, pnt4)
            # leftEdgeList[1] = Topo.EdgeTool.makeEdge(pnt4, pnt8)
            # leftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt8, pnt7)
            # leftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt3)
            # leftWire = Topo.WireTool.makeWire(leftEdgeList, Geom.Precision.linear_Resolution())
            # leftFace = Topo.FaceTool.makeFace(leftWire, Geom.Precision.linear_Resolution())
            # faceList[3] = leftFace
            #
            # frontEdgeList = Topo.vector_Edge(4)
            # frontEdgeList[0] = Topo.EdgeTool.makeEdge(pnt4, pnt1)
            # frontEdgeList[1] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
            # frontEdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt8)
            # frontEdgeList[3] = Topo.EdgeTool.makeEdge(pnt8, pnt4)
            # frontWire = Topo.WireTool.makeWire(frontEdgeList, Geom.Precision.linear_Resolution())
            # frontFace = Topo.FaceTool.makeFace(frontWire, Geom.Precision.linear_Resolution())
            # faceList[4] = frontFace
            #
            # backEdgeList = Topo.vector_Edge(4)
            # backEdgeList[0] = Topo.EdgeTool.makeEdge(pnt2, pnt3)
            # backEdgeList[1] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
            # backEdgeList[2] = Topo.EdgeTool.makeEdge(pnt7, pnt6)
            # backEdgeList[3] = Topo.EdgeTool.makeEdge(pnt6, pnt2)
            # backWire = Topo.WireTool.makeWire(backEdgeList, Geom.Precision.linear_Resolution())
            # backFace = Topo.FaceTool.makeFace(backWire, Geom.Precision.linear_Resolution())
            # faceList[5] = backFace
            #
            # advancedBrep = lx.AdvancedBrep.createIn(doc)
            #
            # shapeList = Topo.ShapeTool.makeShape(faceList)
            # print("shape list - ", shapeList)
            # print("making face of the square base")
            # advancedBrep.setShape(shapeList)
            # print("setting the shape of the square base")
            #
            # elem = lx.SubElement.createIn(doc)
            # print("created subelement of square base")
            # elem.setGeometry(advancedBrep)
            # print("created geom of square base")
            # self.addSubElement(elem)
            # print("added a square base sub element")
            # print(" ")

    def _createCone(self):
        doc = self.getDocument()

        #  Points
        topRadius = self._bottomConeDiameter.getValue() * 0.5
        bottomRadius = self._bottomConeDiameter.getValue() * 0.5
        height = self._ConeHeight.getValue()
        thickness = self._ConeThickness.getValue()

        pnt1 = Geom.Pnt(0.0, -bottomRadius - thickness, 0.0)
        pnt2 = Geom.Pnt(bottomRadius + thickness, 0.0, 0.0)
        pnt3 = Geom.Pnt(0.0, bottomRadius + thickness, 0.0)
        pnt4 = Geom.Pnt(-bottomRadius - thickness, 0.0, 0.0)

        pnt5 = Geom.Pnt(0.0, -bottomRadius - thickness * 0.5, 0.0)
        pnt6 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, 0.0)
        pnt7 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, 0.0)
        pnt8 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, 0.0)

        pnt9 = Geom.Pnt(0.0, -bottomRadius - thickness * 0.5, thickness * 0.5)
        pnt10 = Geom.Pnt(bottomRadius + thickness * 0.5, 0.0, thickness * 0.5)
        pnt11 = Geom.Pnt(0.0, bottomRadius + thickness * 0.5, thickness * 0.5)
        pnt12 = Geom.Pnt(-bottomRadius - thickness * 0.5, 0.0, thickness * 0.5)

        pnt13 = Geom.Pnt(0.0, -bottomRadius, thickness * 0.5)
        pnt14 = Geom.Pnt(bottomRadius, 0.0, thickness * 0.5)
        pnt15 = Geom.Pnt(0.0, bottomRadius, thickness * 0.5)
        pnt16 = Geom.Pnt(-bottomRadius, 0.0, thickness * 0.5)

        xOffset = bottomRadius - topRadius

        pnt17 = Geom.Pnt(0.0, -topRadius - thickness, height)
        pnt18 = Geom.Pnt(topRadius + thickness, 0.0, height)
        pnt19 = Geom.Pnt(0.0, topRadius + thickness, height)
        pnt20 = Geom.Pnt(-topRadius - thickness, 0.0, height)

        pnt21 = Geom.Pnt(0.0, -topRadius - thickness * 0.5, height)
        pnt22 = Geom.Pnt(topRadius + thickness * 0.5, 0.0, height)
        pnt23 = Geom.Pnt(0.0, topRadius + thickness * 0.5, height)
        pnt24 = Geom.Pnt(-topRadius - thickness * 0.5, 0.0, height)

        pnt25 = Geom.Pnt(0.0, -topRadius - thickness * 0.5, height + thickness * 0.5)
        pnt26 = Geom.Pnt(topRadius + thickness * 0.5, 0.0, height + thickness * 0.5)
        pnt27 = Geom.Pnt(0.0, topRadius + thickness * 0.5, height + thickness * 0.5)
        pnt28 = Geom.Pnt(-topRadius - thickness * 0.5, 0.0, height + thickness * 0.5)

        pnt29 = Geom.Pnt(0.0, -topRadius, height + thickness * 0.5)
        pnt30 = Geom.Pnt(topRadius, 0.0, height + thickness * 0.5)
        pnt31 = Geom.Pnt(0.0, topRadius, height + thickness * 0.5)
        pnt32 = Geom.Pnt(-topRadius, 0.0, height + thickness * 0.5)

        faceList = Topo.vector_Face(16)

        #  Bottom six planes
        bottom1EdgeList = Topo.vector_Edge(4)
        bottom1EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
        bottom1EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
        bottom1EdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
        bottom1EdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
        bottom1Wire = Topo.WireTool.makeWire(bottom1EdgeList, Geom.Precision.linear_Resolution())
        bottom1Face = Topo.FaceTool.makeFace(bottom1Wire, Geom.Precision.linear_Resolution())
        faceList[0] = bottom1Face

        bottom2EdgeList = Topo.vector_Edge(4)
        bottom2EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt4, pnt3)
        bottom2EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt8, pnt7)
        bottom2EdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
        bottom2EdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
        bottom2Wire = Topo.WireTool.makeWire(bottom2EdgeList, Geom.Precision.linear_Resolution())
        bottom2Face = Topo.FaceTool.makeFace(bottom2Wire, Geom.Precision.linear_Resolution())
        faceList[1] = bottom2Face

        bottom3EdgeList = Topo.vector_Edge(4)
        bottom3EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
        bottom3EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt10, pnt11)
        bottom3EdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt9)
        bottom3EdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt11)
        bottom3Wire = Topo.WireTool.makeWire(bottom3EdgeList, Geom.Precision.linear_Resolution())
        bottom3Face = Topo.FaceTool.makeFace(bottom3Wire, Geom.Precision.linear_Resolution())
        faceList[2] = bottom3Face

        bottom4EdgeList = Topo.vector_Edge(4)
        bottom4EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt8, pnt7)
        bottom4EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt12, pnt11)
        bottom4EdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt9)
        bottom4EdgeList[3] = Topo.EdgeTool.makeEdge(pnt7, pnt11)
        bottom4Wire = Topo.WireTool.makeWire(bottom4EdgeList, Geom.Precision.linear_Resolution())
        bottom4Face = Topo.FaceTool.makeFace(bottom4Wire, Geom.Precision.linear_Resolution())
        faceList[3] = bottom4Face

        bottom5EdgeList = Topo.vector_Edge(4)
        bottom5EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt10, pnt11)
        bottom5EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt14, pnt15)
        bottom5EdgeList[2] = Topo.EdgeTool.makeEdge(pnt9, pnt13)
        bottom5EdgeList[3] = Topo.EdgeTool.makeEdge(pnt11, pnt15)
        bottom5Wire = Topo.WireTool.makeWire(bottom5EdgeList, Geom.Precision.linear_Resolution())
        bottom5Face = Topo.FaceTool.makeFace(bottom5Wire, Geom.Precision.linear_Resolution())
        faceList[4] = bottom5Face

        bottom6EdgeList = Topo.vector_Edge(4)
        bottom6EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt9, pnt12, pnt11)
        bottom6EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt16, pnt15)
        bottom6EdgeList[2] = Topo.EdgeTool.makeEdge(pnt9, pnt13)
        bottom6EdgeList[3] = Topo.EdgeTool.makeEdge(pnt11, pnt15)
        bottom6Wire = Topo.WireTool.makeWire(bottom6EdgeList, Geom.Precision.linear_Resolution())
        bottom6Face = Topo.FaceTool.makeFace(bottom6Wire, Geom.Precision.linear_Resolution())
        faceList[5] = bottom6Face

        #  External planes
        externalLeftEdgeList = Topo.vector_Edge(4)
        externalLeftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt4, pnt3)
        externalLeftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt20, pnt19)
        externalLeftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt17)
        externalLeftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt19)
        externalLeftWire = Topo.WireTool.makeWire(externalLeftEdgeList, Geom.Precision.linear_Resolution())
        externalLeftFace = Topo.FaceTool.makeFace(externalLeftWire, Geom.Precision.linear_Resolution())
        faceList[6] = externalLeftFace

        externalRightEdgeList = Topo.vector_Edge(4)
        externalRightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
        externalRightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt18, pnt19)
        externalRightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt17)
        externalRightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt19)
        externalRightWire = Topo.WireTool.makeWire(externalRightEdgeList, Geom.Precision.linear_Resolution())
        externalRightFace = Topo.FaceTool.makeFace(externalRightWire, Geom.Precision.linear_Resolution())
        faceList[7] = externalRightFace

        #  Internal planes
        internalRightEdgeList = Topo.vector_Edge(4)
        internalRightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt14, pnt15)
        internalRightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt30, pnt31)
        internalRightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt13, pnt29)
        internalRightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt15, pnt31)
        internalRightWire = Topo.WireTool.makeWire(internalRightEdgeList, Geom.Precision.linear_Resolution())
        internalRightFace = Topo.FaceTool.makeFace(internalRightWire, Geom.Precision.linear_Resolution())
        faceList[8] = internalRightFace

        internalLeftEdgeList = Topo.vector_Edge(4)
        internalLeftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt13, pnt16, pnt15)
        internalLeftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt32, pnt31)
        internalLeftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt13, pnt29)
        internalLeftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt15, pnt31)
        internalLeftWire = Topo.WireTool.makeWire(internalLeftEdgeList, Geom.Precision.linear_Resolution())
        internalLeftFace = Topo.FaceTool.makeFace(internalLeftWire, Geom.Precision.linear_Resolution())
        faceList[9] = internalLeftFace

        #  Upper six faces
        upper1EdgeList = Topo.vector_Edge(4)
        upper1EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt18, pnt19)
        upper1EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt22, pnt23)
        upper1EdgeList[2] = Topo.EdgeTool.makeEdge(pnt17, pnt21)
        upper1EdgeList[3] = Topo.EdgeTool.makeEdge(pnt19, pnt23)
        upper1Wire = Topo.WireTool.makeWire(upper1EdgeList, Geom.Precision.linear_Resolution())
        upper1Face = Topo.FaceTool.makeFace(upper1Wire, Geom.Precision.linear_Resolution())
        faceList[10] = upper1Face

        upper2EdgeList = Topo.vector_Edge(4)
        upper2EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt17, pnt20, pnt19)
        upper2EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt24, pnt23)
        upper2EdgeList[2] = Topo.EdgeTool.makeEdge(pnt17, pnt21)
        upper2EdgeList[3] = Topo.EdgeTool.makeEdge(pnt19, pnt23)
        upper2Wire = Topo.WireTool.makeWire(upper2EdgeList, Geom.Precision.linear_Resolution())
        upper2Face = Topo.FaceTool.makeFace(upper2Wire, Geom.Precision.linear_Resolution())
        faceList[11] = upper2Face

        upper3EdgeList = Topo.vector_Edge(4)
        upper3EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt22, pnt23)
        upper3EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt26, pnt27)
        upper3EdgeList[2] = Topo.EdgeTool.makeEdge(pnt21, pnt25)
        upper3EdgeList[3] = Topo.EdgeTool.makeEdge(pnt23, pnt27)
        upper3Wire = Topo.WireTool.makeWire(upper3EdgeList, Geom.Precision.linear_Resolution())
        upper3Face = Topo.FaceTool.makeFace(upper3Wire, Geom.Precision.linear_Resolution())
        faceList[12] = upper3Face

        upper4EdgeList = Topo.vector_Edge(4)
        upper4EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt21, pnt24, pnt23)
        upper4EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt28, pnt27)
        upper4EdgeList[2] = Topo.EdgeTool.makeEdge(pnt21, pnt25)
        upper4EdgeList[3] = Topo.EdgeTool.makeEdge(pnt23, pnt27)
        upper4Wire = Topo.WireTool.makeWire(upper4EdgeList, Geom.Precision.linear_Resolution())
        upper4Face = Topo.FaceTool.makeFace(upper4Wire, Geom.Precision.linear_Resolution())
        faceList[13] = upper4Face

        upper5EdgeList = Topo.vector_Edge(4)
        upper5EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt26, pnt27)
        upper5EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt30, pnt31)
        upper5EdgeList[2] = Topo.EdgeTool.makeEdge(pnt25, pnt29)
        upper5EdgeList[3] = Topo.EdgeTool.makeEdge(pnt27, pnt31)
        upper5Wire = Topo.WireTool.makeWire(upper5EdgeList, Geom.Precision.linear_Resolution())
        upper5Face = Topo.FaceTool.makeFace(upper5Wire, Geom.Precision.linear_Resolution())
        faceList[14] = upper5Face

        upper6EdgeList = Topo.vector_Edge(4)
        upper6EdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt25, pnt28, pnt27)
        upper6EdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt29, pnt32, pnt31)
        upper6EdgeList[2] = Topo.EdgeTool.makeEdge(pnt25, pnt29)
        upper6EdgeList[3] = Topo.EdgeTool.makeEdge(pnt27, pnt31)
        upper6Wire = Topo.WireTool.makeWire(upper6EdgeList, Geom.Precision.linear_Resolution())
        upper6Face = Topo.FaceTool.makeFace(upper6Wire, Geom.Precision.linear_Resolution())
        faceList[15] = upper6Face

        advancedBrep = lx.AdvancedBrep.createIn(doc)

        shapeList = Topo.ShapeTool.makeShape(faceList)
        advancedBrep.setShape(shapeList)

        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(advancedBrep)
        self.addSubElement(elem)

    def _updateGeometry(self):
        doc = self.getDocument()

        circlesCount = self._circlesCount.getValue()
        circlesHeight = self._circlesHeight.getValue()
        zCoord = -self._circlesHeight.getValue()
        baseType = self._baseType.getValue()
        tapeType = self._tapeType.getValue()

        print("in _updateGeometry()...")
        with EditMode(doc):
            self.removeSubElements()  # Removing all subElements.
            print("removed all subelements")
            self._createOverConePart()
            self._createCone()
            self._createTape(tapeType=tapeType)
            if circlesCount > 1:
                for i in range(circlesCount-1):
                    self._createCircle(zCoord, last=False)
                    zCoord -= circlesHeight
                    if i == circlesCount-2:
                        self._createCircle(zCoord, last=True)

                # zCoord -= circlesHeight
                # self._createBase(zCoord + circlesHeight, baseType=baseType)
                self._createBase(zCoord, baseType=baseType)

            elif circlesCount == 1:
                self._createCircle(zCoord, last=True)
                zCoord -= circlesHeight
                self._createBase(zCoord + circlesHeight, baseType=baseType)

            # if self._topHeight.getValue() == 0.0 and self._circlesCount.getValue() == 0.0:
            #     self._createCone()
            #     print("int 1 condition")
            # elif self._topHeight.getValue() == 0:
            #     print("in 2 condition")
            #     self._createCone()
            #     for i in range(circlesCount - 1):
            #         self._createCircle(zCoord)
            #         zCoord -= circlesHeight
            # elif self._circlesCount.getValue() == 0:
            #     print("in 3 condition")
            #     self._createOverConePart()
            #     self._createCone()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == SchachtKonusElem._topDiameterPropName:
            self.setTopConeDiameter(self._topConeDiameter.getValue())
        if aPropertyName == SchachtKonusElem._bottomDiameterPropName:
            self.setBottomConeDiameter(self._bottomConeDiameter.getValue())
        elif aPropertyName == SchachtKonusElem._heightPropName:
            self.setConeHeight(self._ConeHeight.getValue())
        elif aPropertyName == SchachtKonusElem._thicknessPropName:
            self.setConeThickness(self._ConeThickness.getValue())
        elif aPropertyName == SchachtKonusElem._topHeightPropName:
            self.setTopHeight(self._topHeight.getValue())
        elif aPropertyName == SchachtKonusElem._circlesCountPropName:
            self.setCirclesCount(self._circlesCount.getValue())
        elif aPropertyName == SchachtKonusElem._circlesHeightPropName:
            self.setCirclesHeight(self._circlesHeight.getValue())
        elif aPropertyName == SchachtKonusElem._bottomBendingPropName:
            self.setBottomBending(self._bottomBending.getValue())
        elif aPropertyName == SchachtKonusElem._baseDiameterPropName:
            self.setBaseDiameter(self._baseDiameter.getValue())
        elif aPropertyName == SchachtKonusElem._baseHeightPropName:
            self.setBaseHeight(self._baseHeight.getValue())
        elif aPropertyName == SchachtKonusElem._baseLengthPropName:
            self.setBaseLength(self._baseLength.getValue())
        elif aPropertyName == SchachtKonusElem._baseTypePropName:
            self.setBaseType(self._baseType.getValue())
        elif aPropertyName == SchachtKonusElem._tapeTypePropName:
            self.setTapeType(self._tapeType.getValue())

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(doc):
            if not Geom.GeomTools.isEqual(x, 1.):
                old = self._length.getValue()
                self._length.setValue(old * x)
                self.modifyElem()
            if not Geom.GeomTools.isEqual(y, 1.):
                old = self._width.getValue()
                self._width.setValue(old * y)
                self.modifyElem()
            if not Geom.GeomTools.isEqual(z, 1.):
                old = self._height.getValue()
                self._height.setValue(old * z)
                self.modifyElem()

            self.translateAfterScaled(aVec, aScaleBasePnt)


if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{dc651a20-2271-49ab-bea8-c21cb5821f94}"))

    try:
        compound = SchachtKonusElem(doc)
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
