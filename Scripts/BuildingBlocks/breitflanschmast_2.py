# OpenLexocad libraries
# version 2.0	27.04.2020

# attributes
# version 1.0
#   cable handling(height)

# version 2.0
#   add parameters for base(width, length, height)

# version 3.0
#   add footplate

# version 4.0
#   add second foundation and arm

# ========================================
# ====  Supported by Roman Davydiuk   ====
# ====  Mail: davydjukroman@gmail.com ====
# ====  Skype: live:davydjukroman     ====
# ========================================

import collections
import OpenLxApp as lx
import OpenLxUI as ui
import Base, Core, Geom, Topo, Draw
import traceback, math, time

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

epsilon = 0.001

# Python dictionary of all profiles listed in Lexocad...
profiles = collections.OrderedDict()

profiles.update({'HEA 160': {'h': 152E-03, 'b': 160E-03, 's': 6.0E-03, 't': 9.0E-03, 'r': 15.0E-03}})
profiles.update({'HEA 180': {'h': 171E-03, 'b': 180E-03, 's': 6.0E-03, 't': 9.5E-03, 'r': 15.0E-03}})
profiles.update({'HEA 200': {'h': 190E-03, 'b': 200E-03, 's': 6.5E-03, 't': 10.0E-03, 'r': 18.0E-03}})
profiles.update({'HEA 220': {'h': 210E-03, 'b': 220E-03, 's': 7.0E-03, 't': 11.0E-03, 'r': 18.0E-03}})
profiles.update({'HEA 240': {'h': 230E-03, 'b': 240E-03, 's': 7.5E-03, 't': 12.0E-03, 'r': 21.0E-03}})
profiles.update({'HEA 260': {'h': 250E-03, 'b': 260E-03, 's': 7.5E-03, 't': 12.5E-03, 'r': 24.0E-03}})


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


def vecsAreSame(v1, v2, tolerance=epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)


class Line2D:
    def __init__(self, pt, dir):
        self._pt = Geom.Pnt2d(pt.x(), pt.y())
        self._dir = dir.normalized()

    @staticmethod
    def from2Points(pt1, pt2):
        dir = Geom.Vec2d(pt2.x() - pt1.x(), pt2.y() - pt1.y())
        return Line2D(pt1, dir)

    def point(self):
        return self._pt

    def paramPoint(self, t):
        x = self._pt.x() + t * self._dir.x()
        y = self._pt.y() + t * self._dir.y()

        return Geom.Pnt2d(x, y)

    def direction(self):
        return self._dir

    def normal(self):
        return Geom.Vec2d(-self._dir.y(), self._dir.x())  # Direction is already normalized

    def offset(self, dVec):
        return Line2D(self._pt.translated(dVec), self._dir)

    def normalOffset(self, offs):
        normVec = self.normal()
        normVec.scale(offs)

        return self.offset(normVec)

    def findX(self, y):

        yDir = self._dir.y()
        if math.fabs(yDir) < epsilon:
            raise ZeroDivisionError("Line is parallel to Y axis.")

        t = (y - self._pt.y()) / yDir
        return self._pt.x() + t * self._dir.x()

    def findY(self, x):
        xDir = self._dir.x()
        if math.fabs(xDir) < epsilon:
            raise ZeroDivisionError("Line is parallel to X axis.")

        t = (x - self._pt.x()) / xDir
        return self._pt.y() + t * self._dir.y()

    def distanceToPointSq(self, pt):
        ptVec = Geom.Vec2d(self._pt, pt)
        ptVecLenSq = ptVec.squareMagnitude()

        projVecLenSq = ptVec * self._dir
        projVecLenSq *= projVecLenSq  # self._dir is already normalized, so we don't need to divide on ||self._dir||

        return ptVecLenSq - projVecLenSq

    def distanceToPoint(self, pt):
        return math.sqrt(self.distanceToPointSq(pt))

    def classifyPoint(self, pt):
        normVec = self.normal()
        ptDir = Geom.Vec2d(self._pt, pt)

        return math.copysign(1.0, normVec * ptDir)

    def signedDistToPoint(self, pt):
        return self.distanceToPoint(pt) * self.classifyPoint(pt)

    @staticmethod
    def collinear(l1, l2):
        if math.fabs(l2._dir.x()) < epsilon:
            return bool(math.fabs(l1._dir.x()) < epsilon)
        if math.fabs(l2._dir.y()) < epsilon:
            return bool(math.fabs(l1._dir.y()) < epsilon)

        return bool(math.fabs((l1._dir.x() / l2._dir.x()) - (l1._dir.y() / l2._dir.y())) < epsilon)

    @staticmethod
    def intersect(l1, l2):
        if Line2D.collinear(l1, l2):
            return None

        dx = l2._pt.x() - l1._pt.x()
        dy = l2._pt.y() - l1._pt.y()

        if math.fabs(l2._dir.y()) > epsilon:
            t = (dx * l2._dir.y() - dy * l2._dir.x()) / (l1._dir.x() * l2._dir.y() - l1._dir.y() * l2._dir.x())
            return l1.paramPoint(t)
        else:
            t = (dy * l1._dir.x() - dx * l1._dir.y()) / (l1._dir.y() * l2._dir.x())
            return l2.paramPoint(t)


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


class Breitflanschmast(lx.PythonElement):
    _height_param_name = "Height"
    _type_of_foundation_param_name = "Type of foundation"
    _x_retreat_param_name = "X retreat for foundation"
    _y_retreat_param_name = "Y retreat for foundation"
    _lower_base_depth_param_name = "Lower base depth"
    _upper_base_height_param_name = "Upper base height"
    _footplate_param_name = "With footplate"
    _footplate_distance_param_name = "Footplate distance"
    _if_anchor_foundation_param_name = "Anchor foundation"
    _distance_to_anchor_param_name = "Distance to anchor"
    _type_of_anchor_foundation_param_name = "Type of anchor foundation"
    _if_arm_param_name = "With arm"
    _arm_height_param_name = "Arm height"

    def getGlobalClassId(self):
        return Base.GlobalId("{1099DF7C-1F2A-46AA-A5F5-532DB5CE4D43}")

    def __init__(self, aArg):
        lx.PythonElement.__init__(self, aArg)
        self.registerPythonClass("Breitflanschmast", "OpenLxApp.PythonElement")

        # Register properties
        self.setPropertyHeader(lxstr("Breitflanschmast"), -1)
        self.setPropertyGroupName(lxstr("Breitflanschmast parameters"), -1)

        self._height = self.registerPropertyDouble(self._height_param_name, 10.0, lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE, -1)
        self._height.setSteps(0.5)

        self._heb = self.registerPropertyEnum("HEB sire", 0, lx.Property.VISIBLE,
                                              lx.Property.EDITABLE, -1)
        self._heb.setEmpty()
        self._heb.addEntry(lxstr("160"), -1)
        self._heb.addEntry(lxstr("180"), -1)
        self._heb.addEntry(lxstr("200"), -1)
        self._heb.addEntry(lxstr("220"), -1)
        self._heb.addEntry(lxstr("240"), -1)
        self._heb.addEntry(lxstr("260"), -1)

        self._type_of_foundation = self.registerPropertyEnum(self._type_of_foundation_param_name, 0,
                                                             lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._type_of_foundation.setEmpty()
        self._type_of_foundation.addEntry(lxstr("Foundation with centered head"), -1)
        self._type_of_foundation.addEntry(lxstr("Foundation with offset head"), -1)

        self._x_retreat = self.registerPropertyDouble(self._x_retreat_param_name, 0.0, lx.Property.VISIBLE,
                                                      lx.Property.EDITABLE, -1)
        self._y_retreat = self.registerPropertyDouble(self._y_retreat_param_name, 0.0, lx.Property.VISIBLE,
                                                      lx.Property.EDITABLE, -1)

        # self._lower_base_width = self.registerPropertyDouble("Lower base width", 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, 167)
        # self._lower_base_length = self.registerPropertyDouble("Lower base length", 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, 168)
        self._lower_base_depth = self.registerPropertyDouble(self._lower_base_depth_param_name, 2.0,
                                                             lx.Property.VISIBLE,
                                                             lx.Property.EDITABLE, -1)

        # self._upper_base_width = self.registerPropertyDouble("Lower base width", 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        # self._upper_base_length = self.registerPropertyDouble("Lower base length", 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._upper_base_height = self.registerPropertyDouble(self._upper_base_height_param_name, 0.6,
                                                              lx.Property.VISIBLE,
                                                              lx.Property.EDITABLE, -1)

        self._footplate = self.registerPropertyEnum(self._footplate_param_name, 0, lx.Property.VISIBLE,
                                                    lx.Property.EDITABLE, -1)
        self._footplate.setEmpty()
        self._footplate.addEntry(lxstr("Yes"), -1)
        self._footplate.addEntry(lxstr("No"), -1)

        self._footplate_distance = self.registerPropertyDouble(self._footplate_distance_param_name, 0.25,
                                                               lx.Property.VISIBLE,
                                                               lx.Property.EDITABLE, -1)
        #  Anchor foundation

        self._if_anchor_foundation = self.registerPropertyEnum(self._if_anchor_foundation_param_name, 0,
                                                               lx.Property.VISIBLE,
                                                               lx.Property.EDITABLE, -1)
        self._if_anchor_foundation.setEmpty()
        self._if_anchor_foundation.addEntry(lxstr("Yes"), -1)
        self._if_anchor_foundation.addEntry(lxstr("No"), -1)

        self._distance_to_anchor_foundation = self.registerPropertyDouble(self._distance_to_anchor_param_name, 3.0,
                                                                          lx.Property.VISIBLE,
                                                                          lx.Property.EDITABLE, -1)

        self._type_of_anchor_foundation = self.registerPropertyEnum(self._type_of_anchor_foundation_param_name, 0,
                                                                    lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._type_of_anchor_foundation.setEmpty()
        self._type_of_anchor_foundation.addEntry(lxstr("Centric foundation"), -1)
        self._type_of_anchor_foundation.addEntry(lxstr("Eccentric foundation (right)"), -1)
        self._type_of_anchor_foundation.addEntry(lxstr("Eccentric foundation (left)"), -1)

        #  Arm
        self._if_arm = self.registerPropertyEnum(self._if_arm_param_name, 0, lx.Property.VISIBLE, lx.Property.EDITABLE,
                                                 -1)
        self._if_arm.setEmpty()
        self._if_arm.addEntry(lxstr("Yes"), -1)
        self._if_arm.addEntry(lxstr("No"), -1)

        self._arm_height = self.registerPropertyDouble(self._arm_height_param_name, 5,
                                                               lx.Property.VISIBLE,
                                                               lx.Property.EDITABLE, -1)

        self._distance_to_anchor_foundation.setSteps(0.1)
        self._arm_height.setSteps(0.1)
        self._height.setSteps(0.05)

        self._x_retreat.setSteps(0.005)
        self._y_retreat.setSteps(0.005)
        # self._lower_base_width.setSteps(0.01)
        # self._lower_base_length.setSteps(0.01)
        self._lower_base_depth.setSteps(0.01)

        # self._upper_base_width.setSteps(0.01)
        # self._upper_base_length.setSteps(0.01)
        self._upper_base_height.setSteps(0.01)

        self._footplate_distance.setSteps(0.005)

        

        self._updateGeometry()

    def create_line(self, aFromPnt, aToPnt):
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
        self.addSubElement(elem)

    @staticmethod
    def intersect(l1, l2):
        if Line2D.collinear(l1, l2):
            return None

        dx = l2._pt.x() - l1._pt.x()
        dy = l2._pt.y() - l1._pt.y()

        if math.fabs(l2._dir.y()) > epsilon:
            t = (dx * l2._dir.y() - dy * l2._dir.x()) / (l1._dir.x() * l2._dir.y() - l1._dir.y() * l2._dir.x())
            return l1.paramPoint(t)
        else:
            t = (dy * l1._dir.x() - dx * l1._dir.y()) / (l1._dir.y() * l2._dir.x())
            return l2.paramPoint(t)

    def addBoltInToPnt(self, pnt, radius, height, ax1=None, angle=None):
        direction = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))
        pntB0 = Geom.Pnt(radius, 0.0, 0.0)
        pntB1 = pntB0.rotated(direction, 60.0 * math.pi / 180.0)
        pntB2 = pntB0.rotated(direction, 120.0 * math.pi / 180.0)
        pntB3 = pntB0.rotated(direction, 180.0 * math.pi / 180.0)
        pntB4 = pntB0.rotated(direction, 240.0 * math.pi / 180.0)
        pntB5 = pntB0.rotated(direction, 300.0 * math.pi / 180.0)

        heightVec = Geom.Vec(Geom.Pnt(0, 0, 0), Geom.Pnt(0.0, 0.0, height))

        pntT0 = pntB0.translated(heightVec)
        pntT1 = pntB1.translated(heightVec)
        pntT2 = pntB2.translated(heightVec)
        pntT3 = pntB3.translated(heightVec)
        pntT4 = pntB4.translated(heightVec)
        pntT5 = pntB5.translated(heightVec)

        geom = FacetedModelAssembler(doc)
        geom.beginModel()

        geom.beginFace()
        geom.addVertexList([pntT0, pntT1, pntT2, pntT3, pntT4, pntT5])
        geom.endFace()

        geom.beginFace()
        geom.addVertexList([pntT1, pntT0, pntB0, pntB1])
        geom.endFace()

        geom.beginFace()
        geom.addVertexList([pntT2, pntT1, pntB1, pntB2])
        geom.endFace()

        geom.beginFace()
        geom.addVertexList([pntT3, pntT2, pntB2, pntB3])
        geom.endFace()

        geom.beginFace()
        geom.addVertexList([pntT4, pntT3, pntB3, pntB4])
        geom.endFace()

        geom.beginFace()
        geom.addVertexList([pntT5, pntT4, pntB4, pntB5])
        geom.endFace()

        geom.beginFace()
        geom.addVertexList([pntT0, pntT5, pntB5, pntB0])
        geom.endFace()

        geom.beginFace()
        geom.addVertexList([pntB5, pntB4, pntB3, pntB2, pntB1, pntB0])
        geom.endFace()

        bolt = lx.SubElement.createIn(doc)
        bolt.setGeometry(geom.endModel())
        bolt.setDiffuseColor(Base.Color(224, 223, 219))

        axis1 = Geom.Ax2(pnt, Geom.Dir(0, 0, 1))

        bolt.setLocalPlacement(axis1)

        if ax1:
            bolt.rotate(ax1, angle)

        self.addSubElement(bolt)

    def create_lower_base(self):
        y = None
        x = None
        x_retreat = None
        y_retreat = None
        if self._type_of_foundation.getValue() == 0:
            x = 1.0
            y = 1.0
            x_retreat = 0.0
            y_retreat = 0.0
        elif self._type_of_foundation.getValue() == 1:
            x = 1.0
            y = 1.0
            x_retreat = -0.2
            y_retreat = 0.0

        x_retreat = x_retreat + self._x_retreat.getValue()
        y_retreat = y_retreat + self._y_retreat.getValue()

        h = self._lower_base_depth.getValue()

        pnt0 = Geom.Pnt(-x * 0.5, -y * 0.5, 0.0)
        pnt1 = Geom.Pnt(x * 0.5, -y * 0.5, 0.0)
        pnt2 = Geom.Pnt(x * 0.5, y * 0.5, 0.0)
        pnt3 = Geom.Pnt(-x * 0.5, y * 0.5, 0.0)

        pnt4 = Geom.Pnt(-x * 0.5, -y * 0.5, -h)
        pnt5 = Geom.Pnt(x * 0.5, -y * 0.5, -h)
        pnt6 = Geom.Pnt(x * 0.5, y * 0.5, -h)
        pnt7 = Geom.Pnt(-x * 0.5, y * 0.5, -h)

        base_geom = FacetedModelAssembler(doc)
        base_geom.beginModel()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt1, pnt2, pnt3])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt7, pnt6, pnt5, pnt4])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt3, pnt7, pnt4])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt4, pnt5, pnt1, pnt0])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt5, pnt6, pnt2, pnt1])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt6, pnt7, pnt3, pnt2])
        base_geom.endFace()

        geom = base_geom.endModel()

        base = lx.SubElement.createIn(doc)
        base.setGeometry(geom)
        base.translate(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(x_retreat, y_retreat, 0.0)))
        base.setDiffuseColor(Base.Color(108, 103, 96))

        self.addSubElement(base)

    def create_upper_base(self):
        w = 0.6
        l = 0.6
        h = self._upper_base_height.getValue()

        pnt0t = Geom.Pnt(-l * 0.5 + 0.05, -w * 0.5 + 0.05, h)
        pnt1t = Geom.Pnt(-l * 0.5 + 0.05, w * 0.5 - 0.05, h)
        pnt2t = Geom.Pnt(l * 0.5 - 0.05, w * 0.5 - 0.05, h)
        pnt3t = Geom.Pnt(l * 0.5 - 0.05, -w * 0.5 + 0.05, h)

        pnt0 = Geom.Pnt(-l * 0.5, -w * 0.5, h - 0.075)
        pnt1 = Geom.Pnt(-l * 0.5, w * 0.5, h - 0.075)
        pnt2 = Geom.Pnt(l * 0.5, w * 0.5, h - 0.075)
        pnt3 = Geom.Pnt(l * 0.5, -w * 0.5, h - 0.075)

        pnt4 = Geom.Pnt(-l * 0.5, -w * 0.5, 0.0)
        pnt5 = Geom.Pnt(-l * 0.5, w * 0.5, 0.0)
        pnt6 = Geom.Pnt(l * 0.5, w * 0.5, 0.0)
        pnt7 = Geom.Pnt(l * 0.5, -w * 0.5, 0.0)

        base_geom = FacetedModelAssembler(doc)
        base_geom.beginModel()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt0t, pnt1t, pnt1])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt1, pnt1t, pnt2t, pnt2])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt3, pnt2, pnt2t, pnt3t])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt3, pnt3t, pnt0t])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt3t, pnt2t, pnt1t, pnt0t])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt4, pnt5, pnt6, pnt7])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt4, pnt7, pnt3, pnt0])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt1, pnt5, pnt4])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt1, pnt2, pnt6, pnt5])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt2, pnt3, pnt7, pnt6])
        base_geom.endFace()

        geom = base_geom.endModel()

        base = lx.SubElement.createIn(doc)
        base.setGeometry(geom)
        base.setDiffuseColor(Base.Color(108, 103, 96))

        self.addSubElement(base)

    def create_footplate(self, profile_size):
        l = 0.45
        w = 0.45
        z_retreat = self._upper_base_height.getValue() + self._footplate_distance.getValue()
        if profile_size == "260" or profile_size == "240":
            h = 0.04
        else:
            h = 0.035

        pnt0 = Geom.Pnt(-l * 0.5, -w * 0.5, h + z_retreat)
        pnt1 = Geom.Pnt(-l * 0.5, w * 0.5, h + z_retreat)
        pnt2 = Geom.Pnt(l * 0.5, w * 0.5, h + z_retreat)
        pnt3 = Geom.Pnt(l * 0.5, -w * 0.5, h + z_retreat)

        pnt4 = Geom.Pnt(-l * 0.5, -w * 0.5, z_retreat)
        pnt5 = Geom.Pnt(-l * 0.5, w * 0.5, z_retreat)
        pnt6 = Geom.Pnt(l * 0.5, w * 0.5, z_retreat)
        pnt7 = Geom.Pnt(l * 0.5, -w * 0.5, z_retreat)

        base_geom = FacetedModelAssembler(doc)
        base_geom.beginModel()

        base_geom.beginFace()
        base_geom.addVertexList([pnt3, pnt2, pnt1, pnt0])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt4, pnt5, pnt6, pnt7])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt4, pnt7, pnt3, pnt0])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt1, pnt5, pnt4])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt1, pnt2, pnt6, pnt5])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt2, pnt3, pnt7, pnt6])
        base_geom.endFace()

        base = lx.Element.createIn(doc)
        base.setGeometry(base_geom.endModel())

        hElements = lx.Element.createIn(doc)
        hElements.setGeometry(self.cutting_part())

        # Create a vector to hold the result of the cutting operation
        resulting_elements = lx.vector_Element()

        # Cut base (soft) with tool (hard) elements
        if lx.bop_cut(base, hElements, resulting_elements) != 0:
            print("Error in cut")

        transform = resulting_elements[0].getTransform()
        geometry = resulting_elements[0].getGeometry()

        doc.removeObject(base)
        doc.removeObject(hElements)

        footplate = lx.SubElement.createIn(doc)
        footplate.setTransform(transform)
        footplate.setGeometry(geometry)

        self.addSubElement(footplate)

        distance_between_connectors = 0.34
        connector_radius = 0.02

        self.addBoltInToPnt(
            Geom.Pnt((distance_between_connectors * 0.5), (distance_between_connectors * 0.5), z_retreat - 0.035),
            0.035, 0.07 + h)
        self.addBoltInToPnt(
            Geom.Pnt((distance_between_connectors * 0.5), -(distance_between_connectors * 0.5), z_retreat - 0.035),
            0.035, 0.07 + h)
        self.addBoltInToPnt(
            Geom.Pnt(-(distance_between_connectors * 0.5), (distance_between_connectors * 0.5), z_retreat - 0.035),
            0.035, 0.07 + h)
        self.addBoltInToPnt(
            Geom.Pnt(-(distance_between_connectors * 0.5), -(distance_between_connectors * 0.5), z_retreat - 0.035),
            0.035, 0.07 + h)

        self.create_cylinder(Geom.Pnt((distance_between_connectors * 0.5), (distance_between_connectors * 0.5),
                                      z_retreat - 0.015 - self._footplate_distance.getValue()),
                             self._footplate_distance.getValue() + h + 0.06, connector_radius)
        self.create_cylinder(Geom.Pnt((distance_between_connectors * 0.5), -(distance_between_connectors * 0.5),
                                      z_retreat - 0.015 - self._footplate_distance.getValue()),
                             self._footplate_distance.getValue() + h + 0.06, connector_radius)
        self.create_cylinder(Geom.Pnt(-(distance_between_connectors * 0.5), (distance_between_connectors * 0.5),
                                      z_retreat - 0.015 - self._footplate_distance.getValue()),
                             self._footplate_distance.getValue() + h + 0.06, connector_radius)
        self.create_cylinder(Geom.Pnt(-(distance_between_connectors * 0.5), -(distance_between_connectors * 0.5),
                                      z_retreat - 0.015 - self._footplate_distance.getValue()),
                             self._footplate_distance.getValue() + h + 0.06, connector_radius)

    def cutting_part(self):
        l = 0.15
        w = 0.11
        h = 4
        r = 0.03

        pnt0 = Geom.Pnt(-(l * 0.5) + r, -w * 0.5, 0.0)
        pnt1 = Geom.Pnt((l * 0.5) - r, -w * 0.5, 0.0)
        pnt2 = pnt1.rotated(Geom.Ax1(Geom.Pnt((l * 0.5) - r, -(w * 0.5) + r, 0.0), Geom.Dir(0, 0, 1)), math.radians(45))
        pnt3 = Geom.Pnt(l * 0.5, -(w * 0.5) + r, 0.0)
        pnt4 = Geom.Pnt(l * 0.5, (w * 0.5) - r, 0.0)
        pnt5 = pnt4.rotated(Geom.Ax1(Geom.Pnt((l * 0.5) - r, (w * 0.5) - r, 0.0), Geom.Dir(0, 0, 1)), math.radians(45))
        pnt6 = Geom.Pnt((l * 0.5) - r, w * 0.5, 0.0)
        pnt7 = Geom.Pnt(-(l * 0.5) + r, w * 0.5, 0.0)
        pnt8 = pnt7.rotated(Geom.Ax1(Geom.Pnt(-(l * 0.5) + r, (w * 0.5) - r, 0.0), Geom.Dir(0, 0, 1)), math.radians(45))
        pnt9 = Geom.Pnt(-l * 0.5, (w * 0.5) - r, 0.0)
        pnt10 = Geom.Pnt(-l * 0.5, -(w * 0.5) + r, 0.0)
        pnt11 = pnt10.rotated(Geom.Ax1(Geom.Pnt(-(l * 0.5) + r, -(w * 0.5) + r, 0.0), Geom.Dir(0, 0, 1)),
                              math.radians(45))

        edgeList = Topo.vector_Edge(8)

        edgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
        edgeList[1] = Topo.EdgeTool.makeEdge(pnt3, pnt4)
        edgeList[2] = Topo.EdgeTool.makeArcOfCircle(pnt4, pnt5, pnt6)
        edgeList[3] = Topo.EdgeTool.makeEdge(pnt6, pnt7)
        edgeList[4] = Topo.EdgeTool.makeArcOfCircle(pnt7, pnt8, pnt9)
        edgeList[5] = Topo.EdgeTool.makeEdge(pnt9, pnt10)
        edgeList[6] = Topo.EdgeTool.makeArcOfCircle(pnt10, pnt11, pnt0)
        edgeList[7] = Topo.EdgeTool.makeEdge(pnt0, pnt1)

        wire = Topo.WireTool.makeWire(edgeList, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())

        faceBeam = Topo.FaceTool.extrudedFace(face, Geom.Dir(0.0, 0.0, 1.0), h)

        geom = lx.AdvancedBrep.createIn(doc)
        geom.setShape(faceBeam)

        return geom

    def create_cylinder(self, pnt, h, r, axis=None, color=None):
        beamGeom = lx.RightCircularCylinder.createIn(doc)
        beamGeom.setHeight(h)
        beamGeom.setRadius(r)

        beam = lx.SubElement.createIn(doc)
        beam.setGeometry(beamGeom)

        if axis:
            beam.setLocalPlacement(axis)
        else:
            trVec = Geom.Vec(Geom.Pnt(0, 0, 0), pnt)
            beam.translate(trVec, Geom.CoordSpace_WCS)
        beam.setDiffuseColor(Base.Color(224, 223, 219))
        if color:
            beam.setDiffuseColor(color)
        else:
            beam.setDiffuseColor(Base.Color(224, 223, 219))
        self.addSubElement(beam)

    def create_profile(self, profile_type, profile_size, z_retreat, angle=None):
        print(profile_size)
        profile = lx.IShapeProfileDef.createIn(doc)
        profile.setValuesFromPredefinedSteelProfile(lxstr(profile_type + ' ' + profile_size))

        eas2 = lx.ExtrudedAreaSolid.createIn(doc)
        eas2.setSweptArea(profile)
        eas2.setExtrudedDirection(Geom.Dir(0, 0, 1))
        eas2.setDepth(Geom.Vec(Geom.Pnt(0, 0, 0), Geom.Pnt(0, 0, self._height.getValue())).magnitude() - z_retreat)

        element = lx.SubElement.createIn(doc)
        element.setGeometry(eas2)
        element.translate(Geom.Vec(Geom.Pnt(0, 0, 0), Geom.Pnt(0, 0, -self._lower_base_depth.getValue() + z_retreat)))
        if angle:
            direction = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))
            element.rotate(direction, math.radians(angle))
        self.addSubElement(element)

    def create_anchor_foundation(self):
        y = 1.6
        x = 0.9
        x_retreat = 0.0
        y_retreat = 0.0
        x_foundation_retreat = 0.0
        y_foundation_retreat = 0.0
        if self._type_of_anchor_foundation.getValue() == 0:  # Centric
            x = 1.6
            y = 0.9
            x_foundation_retreat = -0.3
            y_foundation_retreat = 0.0
        elif self._type_of_anchor_foundation.getValue() == 1:  # Eccentric
            x = 1.6
            y = 0.9
            x_foundation_retreat = -0.3
            y_foundation_retreat = -0.25
        elif self._type_of_anchor_foundation.getValue() == 2:
            x = 1.6
            y = 0.9
            x_foundation_retreat = -0.3
            y_foundation_retreat = 0.25

        x_retreat = x_retreat - self._distance_to_anchor_foundation.getValue()

        h = 1.8

        pnt0 = Geom.Pnt(-x * 0.5, -y * 0.5, 0.0)
        pnt1 = Geom.Pnt(x * 0.5, -y * 0.5, 0.0)
        pnt2 = Geom.Pnt(x * 0.5, y * 0.5, 0.0)
        pnt3 = Geom.Pnt(-x * 0.5, y * 0.5, 0.0)

        pnt4 = Geom.Pnt(-x * 0.5, -y * 0.5, -h)
        pnt5 = Geom.Pnt(x * 0.5, -y * 0.5, -h)
        pnt6 = Geom.Pnt(x * 0.5, y * 0.5, -h)
        pnt7 = Geom.Pnt(-x * 0.5, y * 0.5, -h)

        base_geom = FacetedModelAssembler(doc)
        base_geom.beginModel()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt1, pnt2, pnt3])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt7, pnt6, pnt5, pnt4])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt3, pnt7, pnt4])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt4, pnt5, pnt1, pnt0])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt5, pnt6, pnt2, pnt1])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt6, pnt7, pnt3, pnt2])
        base_geom.endFace()

        geom = base_geom.endModel()

        base = lx.SubElement.createIn(doc)
        base.setGeometry(geom)
        base.translate(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(x_retreat + x_foundation_retreat,
                                                                  y_retreat + y_foundation_retreat, 0.0)))
        base.setDiffuseColor(Base.Color(108, 103, 96))

        self.addSubElement(base)

        l = 0.6
        w = 0.4

        h = self._upper_base_height.getValue()

        pnt0t = Geom.Pnt(-l * 0.5 + 0.05, -w * 0.5 + 0.05, h)
        pnt1t = Geom.Pnt(-l * 0.5 + 0.05, w * 0.5 - 0.05, h)
        pnt2t = Geom.Pnt(l * 0.5 - 0.05, w * 0.5 - 0.05, h)
        pnt3t = Geom.Pnt(l * 0.5 - 0.05, -w * 0.5 + 0.05, h)

        pnt0 = Geom.Pnt(-l * 0.5, -w * 0.5, h - 0.075)
        pnt1 = Geom.Pnt(-l * 0.5, w * 0.5, h - 0.075)
        pnt2 = Geom.Pnt(l * 0.5, w * 0.5, h - 0.075)
        pnt3 = Geom.Pnt(l * 0.5, -w * 0.5, h - 0.075)

        pnt4 = Geom.Pnt(-l * 0.5, -w * 0.5, 0.0)
        pnt5 = Geom.Pnt(-l * 0.5, w * 0.5, 0.0)
        pnt6 = Geom.Pnt(l * 0.5, w * 0.5, 0.0)
        pnt7 = Geom.Pnt(l * 0.5, -w * 0.5, 0.0)

        base_geom = FacetedModelAssembler(doc)
        base_geom.beginModel()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt0t, pnt1t, pnt1])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt1, pnt1t, pnt2t, pnt2])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt3, pnt2, pnt2t, pnt3t])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt3, pnt3t, pnt0t])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt3t, pnt2t, pnt1t, pnt0t])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt4, pnt5, pnt6, pnt7])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt4, pnt7, pnt3, pnt0])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt0, pnt1, pnt5, pnt4])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt1, pnt2, pnt6, pnt5])
        base_geom.endFace()

        base_geom.beginFace()
        base_geom.addVertexList([pnt2, pnt3, pnt7, pnt6])
        base_geom.endFace()

        geom = base_geom.endModel()

        base = lx.SubElement.createIn(doc)
        base.setGeometry(geom)
        base.translate(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(x_retreat, y_retreat, 0.0)))
        base.setDiffuseColor(Base.Color(108, 103, 96))

        self.addSubElement(base)

        out_radius = 0.2
        width = 0.03

        pnt0 = Geom.Pnt(l * 0.5 - 0.13, width * 0.5, h)
        pnt1 = Geom.Pnt(l * 0.5 - 0.13 - width, width * 0.5, h)

        pnt2 = Geom.Pnt(l * 0.5 - 0.13 - (out_radius * 0.5), width * 0.5, h + (out_radius * 0.5) - width)

        pnt3 = Geom.Pnt(l * 0.5 - 0.13 - out_radius + width, width * 0.5, h)
        pnt4 = Geom.Pnt(l * 0.5 - 0.13 - out_radius, width * 0.5, h)

        pnt5 = Geom.Pnt(l * 0.5 - 0.13 - (out_radius * 0.5), width * 0.5, h + (out_radius * 0.5))

        edgeList = Topo.vector_Edge(4)

        edgeList[0] = Topo.EdgeTool.makeArcOfCircle(pnt1, pnt2, pnt3)
        edgeList[1] = Topo.EdgeTool.makeEdge(pnt3, pnt4)
        edgeList[2] = Topo.EdgeTool.makeArcOfCircle(pnt4, pnt5, pnt0)
        edgeList[3] = Topo.EdgeTool.makeEdge(pnt0, pnt1)

        wire = Topo.WireTool.makeWire(edgeList, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())

        faceBeam = Topo.FaceTool.extrudedFace(face, Geom.Dir(0.0, -1.0, 0.0), width)

        geom = lx.AdvancedBrep.createIn(doc)
        geom.setShape(faceBeam)

        base = lx.SubElement.createIn(doc)
        base.setGeometry(geom)
        base.translate(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(x_retreat, y_retreat, 0.0)))

        self.addSubElement(base)

        self.create_line(Geom.Pnt(l * 0.5 - 0.13 - (width * 2) - self._distance_to_anchor_foundation.getValue(), 0.0, h + out_radius * 0.5 - width), Geom.Pnt(0.0, 0.0, self._height.getValue() - self._lower_base_depth.getValue() - 0.25))

    def create_stand_off_bracket(self, axis):
        l = 1.5
        w = 0.05

        first_h = 0.1
        second_h = 0.05

        pnt0 = Geom.Pnt(0.0, -w * 0.5, 0.0)
        pnt1 = Geom.Pnt(l, -w * 0.5, 0.0)
        pnt2 = Geom.Pnt(l, w * 0.5, 0.0)
        pnt3 = Geom.Pnt(0.0, w * 0.5, 0.0)

        pnt4 = Geom.Pnt(0.0, -w * 0.5, -first_h)
        pnt5 = Geom.Pnt(0.0, w * 0.5, -first_h)

        pnt6 = Geom.Pnt(l - 0.05, w * 0.5, -second_h)
        pnt7 = Geom.Pnt(l - 0.05, -w * 0.5, -second_h)

        model = FacetedModelAssembler(doc)
        model.beginModel()

        model.beginFace()
        model.addVertexList([pnt0, pnt1, pnt2, pnt3])
        model.endFace()

        model.beginFace()
        model.addVertexList([pnt0, pnt4, pnt7, pnt1])
        model.endFace()

        model.beginFace()
        model.addVertexList([pnt5, pnt3, pnt2, pnt6])
        model.endFace()

        geom = model.endModel()
        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(geom)
        elem.setLocalPlacement(axis)

        self.addSubElement(elem)

    def _createGeometry(self):
        self.create_lower_base()
        self.create_upper_base()

        heb_type = self._heb.getValue()

        profile_size = None

        if heb_type == 0:
            profile_size = '160'
        elif heb_type == 1:
            profile_size = '180'
        elif heb_type == 2:
            profile_size = '200'
        elif heb_type == 3:
            profile_size = '220'
        elif heb_type == 4:
            profile_size = '240'
        elif heb_type == 5:
            profile_size = '260'

        z_retreat = 0.0
        if self._footplate.getValue() == 0:
            if profile_size == "260" or profile_size == "240":
                h = 0.04
            else:
                h = 0.035
            self.create_footplate(profile_size)
            z_retreat = self._upper_base_height.getValue() + self._footplate_distance.getValue() + self._lower_base_depth.getValue() + h

        self.create_profile('HEB', profile_size, z_retreat, 90.0)

        if self._if_anchor_foundation.getValue() == 0:
            self.create_anchor_foundation()

        #  create arm
        if self._if_arm.getValue() == 0:
            arm_height = self._arm_height.getValue() + self._upper_base_height.getValue() + 2.650
            self.create_stand_off_bracket(Geom.Ax2(Geom.Pnt(float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 2.55), Geom.Dir(0, 0, 1)))
            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 4.416, 0.04, Geom.Ax2(Geom.Pnt(float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 0.54), Geom.Dir(1, 0, 0)))
            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 3.73, 0.04, Geom.Ax2( Geom.Pnt(float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 2), Geom.Dir(1, 0, 0.425)))

            # add lover part with fuse
            r = 0.006
            R = 0.0225
            L = 0.620
            l = 0.35
            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 3.15, r, Geom.Ax2( Geom.Pnt(1.525 + float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 2.575), Geom.Dir(1, 0, 0)))

            #  add fuse
            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), l, R, Geom.Ax2( Geom.Pnt(1.525 + 0.08 + float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 2.575), Geom.Dir(1, 0, 0)), Base.Color(80, 25, 25))

            # add lover connections
            lover_connection_geom = FacetedModelAssembler(doc)
            lover_connection_geom.beginModel()
            c_w = 0.08
            c_h = 0.06
            c_l = 0.07
            lover_connection_geom.beginFace()
            lover_connection_geom.addVertexList([Geom.Pnt(0.0, -(c_w * 0.5), -(c_h * 0.5)),
                                                 Geom.Pnt(0.0, c_w * 0.5, -(c_h * 0.5)),
                                                 Geom.Pnt(0.0, c_w * 0.5, c_h * 0.5),
                                                 Geom.Pnt(0.0, -(c_w * 0.5), c_h * 0.5)])
            lover_connection_geom.endFace()

            lover_connection_geom.beginFace()
            lover_connection_geom.addVertexList([Geom.Pnt(0.0, -(c_w * 0.5), c_h * 0.5),
                                                 Geom.Pnt(0.0, c_w * 0.5, c_h * 0.5),
                                                 Geom.Pnt(-c_l, c_w * 0.5, c_h * 0.5),
                                                 Geom.Pnt(-c_l, -(c_w * 0.5), c_h * 0.5)])
            lover_connection_geom.endFace()

            lover_connection = lx.SubElement.createIn(doc)
            lover_connection.setGeometry(lover_connection_geom.endModel())
            lover_connection.setDiffuseColor(Base.Color(224, 223, 219))
            lover_connection.translate(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(1.525 + float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 2.575)))
            self.addSubElement(lover_connection)

            self.create_cylinder(Geom.Pnt(3.063 + 1.525 + float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 2.575), -0.2, r)

            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 0.115, r, Geom.Ax2(Geom.Pnt(3.063 + 1.525 + float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 2.575 - 0.194), Geom.Dir(-1, 0.0, 0.8)))

            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 1.133, r, Geom.Ax2(Geom.Pnt(3.063 - 0.09 + 1.53 + float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 2.575 - 0.2 + 0.0768), Geom.Dir(-1, 0.0, -0.17)))

            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 0.09, r, Geom.Ax2(Geom.Pnt(3.063 - 1.105 - 0.09 + 1.525 + float(profile_size) * 0.5 * 0.001, 0.0, arm_height - 2.575 - 0.2 + 0.085 - 0.196), Geom.Dir(0.17, 0.0, -1)))

            # add upper connections
            self.create_cylinder(Geom.Pnt(float(profile_size) * 0.5 * 0.001 + 3.735, 0.0, arm_height - 0.54), -0.084, r)
            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 0.515, r, Geom.Ax2(Geom.Pnt(float(profile_size) * 0.5 * 0.001 + 3.735, 0.0, arm_height - 0.54 - 0.08), Geom.Dir(-0.4, 0.0, -0.5)))
            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 0.08, r, Geom.Ax2(
                Geom.Pnt(float(profile_size) * 0.5 * 0.001 + 3.735 - 0.355, 0.0, arm_height - 0.62 - 0.38), Geom.Dir(0.5, 0.0, -0.4)))

            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 0.06, r, Geom.Ax2(Geom.Pnt(float(profile_size) * 0.5 * 0.001 + 3.385, 0.0, arm_height - 1.0035), Geom.Dir(-0.4, 0.0, -0.5)))

            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), 0.06, r, Geom.Ax2(Geom.Pnt(float(profile_size) * 0.5 * 0.001 + 3.735 - 0.297, 0.0, arm_height - 0.54 - 0.08 - 0.426), Geom.Dir(-0.4, 0.0, -0.5)))

            #  add fuse
            self.create_cylinder(Geom.Pnt(0.0, 0.0, 0.0), l, R, Geom.Ax2(Geom.Pnt(float(profile_size) * 0.5 * 0.001 + 3.735 - 0.071, 0.0, arm_height - 0.54 - 0.08 - 0.088), Geom.Dir(-0.4, 0.0, -0.5)), Base.Color(80, 25, 25))

    def setHeight(self, p):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(p, 5.0, 16.0))
            self._updateGeometry()

    def setProfileSize(self, p):
        with EditMode(self.getDocument()):
            self._heb.setValue(p)
            self._updateGeometry()

    def set_foundation_type(self, param):
        with EditMode(self.getDocument()):
            self._type_of_foundation.setValue(param)
            self._updateGeometry()

    # def set_lower_base_width(self, param):
    #     with EditMode(self.getDocument()):
    #         self._lower_base_width.setValue(param)
    #         self._updateGeometry()
    #
    # def set_lower_base_length(self, param):
    #     with EditMode(self.getDocument()):
    #         self._lower_base_length.setValue(param)
    #         self._updateGeometry()

    def set_x_retreat(self, param):
        with EditMode(self.getDocument()):
            self._x_retreat.setValue(clamp(param, -1.0, 1.0))
            self._updateGeometry()

    def set_y_retreat(self, param):
        with EditMode(self.getDocument()):
            self._y_retreat.setValue(clamp(param, -1.0, 1.0))
            self._updateGeometry()

    def set_lower_base_depth(self, param):
        with EditMode(self.getDocument()):
            self._lower_base_depth.setValue(clamp(param, 1.8, 3.0))
            self._updateGeometry()

    # def set_upper_base_width(self, param):
    #     with EditMode(self.getDocument()):
    #         self._upper_base_width.setValue(param)
    #         self._updateGeometry()
    #
    # def set_upper_base_length(self, param):
    #     with EditMode(self.getDocument()):
    #         self._upper_base_length.setValue(param)
    #         self._updateGeometry()

    def set_upper_base_height(self, param):
        with EditMode(self.getDocument()):
            self._upper_base_height.setValue(param)
            self._updateGeometry()

    def set_footplate(self, param):
        with EditMode(self.getDocument()):
            self._footplate.setValue(param)
            self._updateGeometry()

    def set_footplate_distance(self, param):
        with EditMode(self.getDocument()):
            self._footplate_distance.setValue(clamp(param, 0.0, 0.5))
            self._updateGeometry()

    def set_if_anchor_foundation(self, param):
        with EditMode(self.getDocument()):
            self._if_anchor_foundation.setValue(param)
            self._updateGeometry()

    def set_distance_to_anchor(self, param):
        with EditMode(self.getDocument()):
            self._distance_to_anchor_foundation.setValue(param)
            self._updateGeometry()

    def set_anchor_foundation_type(self, param):
        with EditMode(self.getDocument()):
            self._type_of_anchor_foundation.setValue(param)
            self._updateGeometry()

    def set_if_arm(self, param):
        with EditMode(self.getDocument()):
            self._if_arm.setValue(param)
            if self._if_arm.getValue() == 0:
                self._arm_height.setVisible(True)
            else:
                self._arm_height.setVisible(False)
            self._updateGeometry()

    def set_arm_height(self, param):
        with EditMode(self.getDocument()):
            self._arm_height.setValue(clamp(param, 0.0, 100.0))
            self._updateGeometry()

    def _updateGeometry(self):
        doc = self.getDocument()

        with EditMode(doc):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == self._height_param_name:
            self.setHeight(self._height.getValue())
        elif aPropertyName == "HEB sire":
            self.setProfileSize(self._heb.getValue())
        elif aPropertyName == self._type_of_foundation_param_name:
            self.set_foundation_type(self._type_of_foundation.getValue())

        elif aPropertyName == self._x_retreat_param_name:
            self.set_x_retreat(self._x_retreat.getValue())
        elif aPropertyName == self._y_retreat_param_name:
            self.set_y_retreat(self._y_retreat.getValue())
        # elif aPropertyName == "Lower base width":
        #     self.set_lower_base_width(self._lower_base_width.getValue())
        # elif aPropertyName == "Lower base length":
        #     self.set_lower_base_length(self._lower_base_length.getValue())
        elif aPropertyName == self._lower_base_depth_param_name:
            self.set_lower_base_depth(self._lower_base_depth.getValue())

        # elif aPropertyName == "Upper base width":
        #     self.set_upper_base_width(self._upper_base_width.getValue())
        # elif aPropertyName == "Upper base length":
        #     self.set_upper_base_length(self._upper_base_length.getValue())
        elif aPropertyName == self._upper_base_height_param_name:
            self.set_upper_base_height(self._upper_base_height.getValue())
        elif aPropertyName == self._footplate_distance_param_name:
            self.set_footplate_distance(self._footplate_distance.getValue())

        elif aPropertyName == self._footplate_param_name:
            self.set_footplate(self._footplate.getValue())
        #  Anchor foundation
        elif aPropertyName == self._if_anchor_foundation_param_name:
            self.set_if_anchor_foundation(self._if_anchor_foundation.getValue())
        elif aPropertyName == self._distance_to_anchor_param_name:
            self.set_distance_to_anchor(self._distance_to_anchor_foundation.getValue())
        elif aPropertyName == self._type_of_anchor_foundation_param_name:
            self.set_anchor_foundation_type(self._type_of_anchor_foundation.getValue())
        elif aPropertyName == self._if_arm_param_name:
            self.set_if_arm(self._if_arm.getValue())
        elif aPropertyName == self._arm_height_param_name:
            self.set_arm_height(self._arm_height.getValue())

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(self.getDocument()):
            if not Geom.GeomTools.isEqual(x, 1.):
                print("Scaling in X")
                old = self._height.getValue()
                self.setHeight(old * x)
            if not Geom.GeomTools.isEqual(y, 1.):
                print("Scaling in Y")
            if not Geom.GeomTools.isEqual(z, 1.):
                print("Scaling in Z")

            self.translateAfterScaled(aVec, aScaleBasePnt)


if __name__ == "__main__":
    doc.registerPythonScript(Base.GlobalId("{CEBB074B-FC3A-4F08-B23E-697A7EC31A39}"))
    # doc.registerPythonScript(Base.GlobalId("{f0c4f2c7-7173-4d54-92f9-2ecb154261c8}")) # SubElement Class

    try:
        support = Breitflanschmast(doc)
        support.setDiffuseColor(Base.Color_fromCdwkColor(60))
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
            support.setLocalPlacement(pos)
    except Exception as e:
        print("{}".format(e))
        traceback.print_exc()
    finally:
        doc.recompute()
