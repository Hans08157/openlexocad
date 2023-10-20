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


class SchachtKonusElemSimplified(lx.Element):
    _classID = "{18620B25-6B37-4C3A-A19C-1EEF8D226A07}"
    _headerPropName = "Schacht Konus"
    _groupPropName = "Schacht Konus Parameter"

    _diameterUpperPropName = "Diameter upper part"
    _diameterLowerPropName = "Diameter lower part"
    _topHeightPropName = "Height top part"
    _middleHeightPropName = "Height middle part"
    _lowerHeightPropName = "Height lower part"

    def getGlobalClassId(self):
        return Base.GlobalId(SchachtKonusElemSimplified._classID)

    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("SchachtKonusElemSimplified", "OpenLxApp.Element")
        # Register properties
        self.setPropertyHeader(lxstr(SchachtKonusElemSimplified._headerPropName), -1)
        self.setPropertyGroupName(lxstr(SchachtKonusElemSimplified._groupPropName), -1)

        self._diameterUpper = self.registerPropertyDouble(SchachtKonusElemSimplified._diameterUpperPropName,
                                                          0.625,
                                                          lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)
        self._diameterLower = self.registerPropertyDouble(SchachtKonusElemSimplified._diameterLowerPropName,
                                                          1.0,
                                                          lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, -1)
        self._topHeight = self.registerPropertyDouble(SchachtKonusElemSimplified._topHeightPropName,
                                                      0.3,
                                                      lx.Property.VISIBLE,
                                                      lx.Property.EDITABLE, -1)
        self._middleHeight = self.registerPropertyDouble(SchachtKonusElemSimplified._middleHeightPropName,
                                                         0.6,
                                                         lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, -1)
        self._lowerHeight = self.registerPropertyDouble(SchachtKonusElemSimplified._lowerHeightPropName,
                                                        1.0,
                                                        lx.Property.VISIBLE,
                                                        lx.Property.EDITABLE, -1)

        self._setAllSteps()
        
        self._updateGeometry()

    def _setAllSteps(self):
        self._diameterUpper.setSteps(0.1)
        self._diameterLower.setSteps(0.1)
        self._topHeight.setSteps(0.1)
        self._middleHeight.setSteps(0.1)
        self._lowerHeight.setSteps(0.1)

    def setUpperDiameter(self, param):
        with EditMode(self.getDocument()):
            self._diameterUpper.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setLowerDiameter(self, param):
        with EditMode(self.getDocument()):
            self._diameterLower.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setTopHeight(self, param):
        epsilon = 0.00
        with EditMode(self.getDocument()):
            self._topHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setMiddleHeight(self, param):
        with EditMode(self.getDocument()):
            self._middleHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def setLowerHeight(self, param):
        epsilon = 0.00
        with EditMode(self.getDocument()):
            self._lowerHeight.setValue(clamp(param, epsilon, maxValue))
            self._updateGeometry()
        if param < epsilon:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too small"))
        elif param > maxValue:
            Base.Message().showMessageBoxWarning(qstr("Wrong Parameter"),
                                                 qstr("The value is too big"))

    def _createUpperPart(self):

        bottomRadius = self._diameterLower.getValue() * 0.5
        topRadius = self._diameterUpper.getValue() * 0.5
        xOffset = bottomRadius - topRadius

        height = self._topHeight.getValue()
        zOffset = self._middleHeight.getValue()

        if height <= 0:
            return
        else:
            cylinder = lx.RightCircularCylinder.createIn(doc)
            cylinder.setHeight(height)
            cylinder.setRadius(topRadius)

            elem = lx.SubElement.createIn(doc)
            elem.setGeometry(cylinder)
            translateVector = Geom.Vec(xOffset, 0.0, zOffset)
            elem.translate(translateVector, Geom.CoordSpace_WCS)

            self.addSubElement(elem)

    def _createLowerPart(self):

        bottomRadius = self._diameterLower.getValue() * 0.5
        topRadius = self._diameterUpper.getValue() * 0.5
        xOffset = bottomRadius - topRadius

        height = self._lowerHeight.getValue()
        if height <= 0:
            return
        else:
            cylinder = lx.RightCircularCylinder.createIn(doc)
            cylinder.setHeight(height)
            cylinder.setRadius(bottomRadius)

            elem = lx.SubElement.createIn(doc)
            elem.setGeometry(cylinder)
            translateVector = Geom.Vec(0.0, 0.0, -height)
            elem.translate(translateVector, Geom.CoordSpace_WCS)

            self.addSubElement(elem)

    def _createCone(self):

        bottomRadius = self._diameterLower.getValue() * 0.5
        topRadius = self._diameterUpper.getValue() * 0.5
        xOffset = bottomRadius - topRadius
        height = self._middleHeight.getValue()

        pnt1 = Geom.Pnt(0.0, -bottomRadius, 0.0)
        pnt2 = Geom.Pnt(bottomRadius, 0.0, 0.0)
        pnt3 = Geom.Pnt(0.0, bottomRadius, 0.0)
        pnt4 = Geom.Pnt(-bottomRadius, 0.0, 0.0)

        pnt5 = Geom.Pnt(xOffset, -topRadius, height)
        pnt6 = Geom.Pnt(xOffset + topRadius, 0.0, height)
        pnt7 = Geom.Pnt(xOffset, topRadius, height)
        pnt8 = Geom.Pnt(xOffset - topRadius, 0.0, height)

        faceList = Topo.vector_Face(4)

        topEdgeList = Topo.vector_Edge(2)
        topEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
        topEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt8, pnt5)
        topWire = Topo.WireTool.makeWire(topEdgeList, Geom.Precision.linear_Resolution())
        topFace = Topo.FaceTool.makeFace(topWire, Geom.Precision.linear_Resolution())
        faceList[0] = topFace

        bottomEdgeList = Topo.vector_Edge(2)
        bottomEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
        bottomEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt3, pnt4, pnt1)
        bottomWire = Topo.WireTool.makeWire(bottomEdgeList, Geom.Precision.linear_Resolution())
        bottomFace = Topo.FaceTool.makeFace(bottomWire, Geom.Precision.linear_Resolution())
        faceList[1] = bottomFace

        leftEdgeList = Topo.vector_Edge(4)
        leftEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt3, pnt4, pnt1)
        leftEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt8, pnt5)
        leftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
        leftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
        leftWire = Topo.WireTool.makeWire(leftEdgeList, Geom.Precision.linear_Resolution())
        leftFace = Topo.FaceTool.makeFace(leftWire, Geom.Precision.linear_Resolution())
        faceList[2] = leftFace

        rightEdgeList = Topo.vector_Edge(4)
        rightEdgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
        rightEdgeList[1] = Topo.EdgeTool.makeArcOfCircle(pnt5, pnt6, pnt7)
        rightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
        rightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
        rightWire = Topo.WireTool.makeWire(rightEdgeList, Geom.Precision.linear_Resolution())
        rightFace = Topo.FaceTool.makeFace(rightWire, Geom.Precision.linear_Resolution())
        faceList[3] = rightFace

        advancedBrep = lx.AdvancedBrep.createIn(doc)
        shapeList = Topo.ShapeTool.makeShape(faceList)
        advancedBrep.setShape(shapeList)

        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(advancedBrep)
        self.addSubElement(elem)

    def _createElement(self):
        # launching three methods to create a whole model.
        self._createLowerPart()
        self._createUpperPart()
        self._createCone()

    def _updateGeometry(self):
        doc = self.getDocument()

        print("in _updateGeometry()...")
        with EditMode(doc):
            self.removeSubElements()  # Removing all subElements.
            print("removed all subelements")
            self._createElement()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == SchachtKonusElemSimplified._diameterLowerPropName:
            self.setLowerDiameter(self._diameterLower.getValue())
        elif aPropertyName == SchachtKonusElemSimplified._diameterUpperPropName:
            self.setUpperDiameter(self._diameterUpper.getValue())
        elif aPropertyName == SchachtKonusElemSimplified._topHeightPropName:
            self.setTopHeight(self._topHeight.getValue())
        elif aPropertyName == SchachtKonusElemSimplified._middleHeightPropName:
            self.setMiddleHeight(self._middleHeight.getValue())
        elif aPropertyName == SchachtKonusElemSimplified._lowerHeightPropName:
            self.setLowerHeight(self._lowerHeight.getValue())


if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{DC0EF4CA-B819-42F7-85F1-ADCC49C4D8D2}"))

    try:
        compound = SchachtKonusElemSimplified(doc)
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
