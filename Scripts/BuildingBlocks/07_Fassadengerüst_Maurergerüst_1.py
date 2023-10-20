# OpenLexocad libraries
# version 1.0   27.10.2020

# attributes
#   version 1.0
#   - height
#   - length
#   - width
#   - color
#   - cwColor = 691

# ========================================
# ====  Supported by Roman Davydiuk   ====
# ====  Mail: davydjukroman@gmail.com ====
# ====  Skype: live:davydjukroman     ====
# ========================================


import math
import traceback

import Base
import Core
import Geom
import Topo
# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxCmd as cmd
import OpenLxUI  as ui

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

epsilon = 0.0001
pi2 = math.pi * 0.5


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


def baseVecTranslate(pt, baseVec, dist):
    return Geom.Pnt(
        pt.x() + (baseVec.x() * dist),
        pt.y() + (baseVec.y() * dist),
        pt.z() + (baseVec.z() * dist)
    )


def vecsAreSame(v1, v2, tolerance=epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)


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
        return [-b / (2.0 * a)]
    else:
        []


def printVal(name, val):
    print("{} = {}".format(name, val))


def printVec(name, val):
    print("{}: ({}, {}, {})".format(name, val.x(), val.y(), val.z()))


def printVec2D(name, val):
    print("{}: ({}, {})".format(name, val.x(), val.y()))


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


class Fassadengerust(lx.Wall):
    _classID = Base.GlobalId("{AC4AFD76-6747-41F1-8CFA-3794FB707D75}")

    _propHeader = "_07FassadengerüstMaurergerüst"
    _propGroupName = "_07FassadengerüstMaurergerüstParameter"

    _lengthPropName = "Length"
    _widthPropName = "Width"
    _heightPropName = "Height"
    _colorPropName = "Color"

    def getGlobalClassId(self):
        return Fassadengerust._classID

    def __init__(self, aArg):
        lx.Wall.__init__(self, aArg)
        self.registerPythonClass("Fassadengerust", "OpenLxApp.Wall")

        self._insidePropUpdate = False

        self.setPropertyHeader(lxstr(Fassadengerust._propHeader), 532)
        self.setPropertyGroupName(lxstr(Fassadengerust._propGroupName), 533)

        self._length = self.registerPropertyDouble(Fassadengerust._lengthPropName,
                                                   3.0,
                                                   lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE,
                                                   505)

        self._width = self.registerPropertyDouble(Fassadengerust._widthPropName,
                                                  0.9,
                                                  lx.Property.VISIBLE,
                                                  lx.Property.EDITABLE,
                                                  502)

        self._height = self.registerPropertyDouble(Fassadengerust._heightPropName,
                                                   2.0,
                                                   lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE,
                                                   503)

        # self._color = self.registerPropertyColor(Seitenschutz._colorPropName, Base.Color(180, 30, 30),
        #                                          lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._width.setSteps(0.01)
        self._length.setSteps(0.01)
        self._height.setSteps(0.01)
        self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())

        self._createGeometry()

    def _createGeometry(self):
        doc = self.getDocument()
        with EditMode(doc):
            self._profileDef = lx.RectangleProfileDef.createIn(doc)
            self._profileDef.setXDim(self._length.getValue())
            self._profileDef.setYDim(self._width.getValue())

            self._extrudedAreaSolid = lx.ExtrudedAreaSolid.createIn(doc)
            self._extrudedAreaSolid.setDepth(self._height.getValue())
            self._extrudedAreaSolid.setExtrudedDirection(Geom.Dir_ZDir())
            self._extrudedAreaSolid.setPosition(
                Geom.Ax2(Geom.Pnt(0., 0., 0.), Geom.Dir_XDir(), Geom.Dir_ZDir(), Geom.Dir_YDir()))
            self._extrudedAreaSolid.setSweptArea(self._profileDef)

            self.setGeometry(self._extrudedAreaSolid)

    def _updateGeometry(self):
        with EditMode(self.getDocument()):
            self._profileDef.setXDim(self._length.getValue())
            self._profileDef.setYDim(self._width.getValue())
            self._extrudedAreaSolid.setDepth(self._height.getValue())

    def setLength(self, length):
        with EditMode(self.getDocument()):
            self._length.setValue(clamp(length, 0.01, 100.0))
            self._updateGeometry()

    def setWidth(self, width):
        with EditMode(self.getDocument()):
            self._width.setValue(clamp(width, 0.01, 100.0))
            self._updateGeometry()

    def setHeight(self, height):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(height, 0.01, 100.0))
            self._updateGeometry()

    def setColor(self, color):
        with EditMode(self.getDocument()):
            self._color.setValue(color)
            self._updateGeometry()

    def onPropertyChanged(self, aPropertyName):
        if not self._insidePropUpdate:
            self._insidePropUpdate = True

            if aPropertyName == Fassadengerust._lengthPropName:
                self.setLength(self._length.getValue())
            elif aPropertyName == Fassadengerust._widthPropName:
                self.setWidth(self._width.getValue())
            elif aPropertyName == Fassadengerust._heightPropName:
                self.setHeight(self._height.getValue())
            # elif aPropertyName == Seitenschutz._colorPropName:
            #     self.setColor(self._color.getValue())

            self._insidePropUpdate = False

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(self.getDocument()):
            if not Geom.GeomTools.isEqual(x, 1.):
                print("Scale x by ", x)
                old = self._height.getValue()
                self.setHeight(old * x)
            if not Geom.GeomTools.isEqual(y, 1.):
                print("Scale y by ", y)
                old = self._length.getValue()
                self.setLength(old * y)
            if not Geom.GeomTools.isEqual(z, 1.):
                print("Scale z by ", z)
                old = self._width.getValue()
                self.setWidth(old * z)

            self.translateAfterScaled(aVec, aScaleBasePnt)


if __name__ == "__main__":
    app = lx.Application.getInstance()
    doc = app.getActiveDocument()
    uiapp = ui.UIApplication.getInstance()
    uidoc = uiapp.getUIDocument(doc)

    doc.registerPythonScript(Base.GlobalId("{9A6BA560-E126-4A30-9CD3-C1A877143C1F}"))

    try:
        cwColor = 3111
        element = Fassadengerust(doc)
        lx.setNewComponentByColorAndName(cwColor, Base.StringTool.toString("Fassadengerust Maurergerust"), element)
        element.setDiffuseColor(Base.Color_fromCdwkColor(cwColor))
        element.setPredefinedType(lx.Wall.WallTypeEnum_USERDEFINED)

        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            location = thisScript.getInsertionPoint()
        else:
            location = Geom.Pnt(0., 0., 0.)

        pos = Geom.Ax2(location, -Geom.Dir_YDir(), Geom.Dir_ZDir())
        element.setLocalPlacement(pos)

        pset_name = Base.StringTool.toStlString(Base.PTranslator.get(587))  # "Absturzsicherung_Suva"
        prop1_name = Base.StringTool.toStlString(Base.PTranslator.get(588))  # "Typ"
        prop1_value = Base.StringTool.toStlString(Base.PTranslator.get(532))  # "07_Fassadengerüst_Maurergerüst"
        prop2_name = Base.StringTool.toStlString(Base.PTranslator.get(590))    # "Vorgespanntes_Drahtseil"
        prop3_name = Base.StringTool.toStlString(Base.PTranslator.get(591))    # "Innengeländer"

        cmd.CmdSetPropertySetDefinition("Pset_WallCommon", "reference", "07_Fassadengerüst_Maurergerüst", element).redo()

        cmd.CmdSetPropertySetDefinition(pset_name, prop3_name, False, element).redo()
        cmd.CmdSetPropertySetDefinition(pset_name, prop1_name, prop1_value, element).redo()
        cmd.CmdSetPropertySetDefinition(pset_name, prop2_name, element).redo()  # Empty

    except Exception as e:
        traceback.print_exc()
    finally:
        doc.recompute()
