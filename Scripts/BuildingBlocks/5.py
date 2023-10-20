# OpenLexocad libraries
# version 2.0	27.04.2020

# attributes
# version 1.0
#   cable handling(height)

# version 2.0
#   add parameters for base(width, length, height)

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


def vecsAreSame(v1, v2, tolerance = epsilon):
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
        return Geom.Vec2d(-self._dir.y(), self._dir.x())    # Direction is already normalized

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
        projVecLenSq *= projVecLenSq    # self._dir is already normalized, so we don't need to divide on ||self._dir||

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
    def getGlobalClassId(self):
        return Base.GlobalId("{1FDFDB39-54F7-43CB-B1A8-040277961737}")

    def __init__(self, aArg):
        lx.PythonElement.__init__(self, aArg)
        self.registerPythonClass("Breitflanschmast", "OpenLxApp.PythonElement")

        # Register properties
        self.setPropertyHeader(lxstr("Breitflanschmast"), 163)
        self.setPropertyGroupName(lxstr("Breitflanschmast parameters"), 164)

        self._height = self.registerPropertyDouble("Height", 10.0, lx.Property.VISIBLE, lx.Property.EDITABLE, 165)
        self._height.setSteps(0.5)

        self._heb = self.registerPropertyEnum("HEB sire", 0, lx.Property.VISIBLE,
                                                        lx.Property.EDITABLE, 166)

        self._heb.setEmpty()
        self._heb.addEntry(lxstr("160"), -1)
        self._heb.addEntry(lxstr("180"), -1)
        self._heb.addEntry(lxstr("200"), -1)
        self._heb.addEntry(lxstr("220"), -1)
        self._heb.addEntry(lxstr("240"), -1)
        self._heb.addEntry(lxstr("260"), -1)

        self._base_width = self.registerPropertyDouble("Base width", 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, 167)
        self._base_length = self.registerPropertyDouble("Base length", 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, 168)
        self._base_height = self.registerPropertyDouble("Base height", 0.4, lx.Property.VISIBLE, lx.Property.EDITABLE, 169)

        self._base_width.setSteps(0.01)
        self._base_length.setSteps(0.01)
        self._base_height.setSteps(0.01)

        

        self._updateGeometry()

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

    def addTrafficLightBase(self, scale, axis1, l, w, h):
        pnt0 = Geom.Pnt(-l * 0.5, -w * 0.5, 0.0)
        pnt1 = Geom.Pnt(-l * 0.5, w * 0.5, 0.0)
        pnt2 = Geom.Pnt(l * 0.5, w * 0.5, 0.0)
        pnt3 = Geom.Pnt(l * 0.5, -w * 0.5, 0.0)

        pnt4 = Geom.Pnt(-l * 0.5, -w * 0.5, -h)
        pnt5 = Geom.Pnt(-l * 0.5, w * 0.5, -h)
        pnt6 = Geom.Pnt(l * 0.5, w * 0.5, -h)
        pnt7 = Geom.Pnt(l * 0.5, -w * 0.5, -h)

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

        geom = base_geom.endModel()

        base = lx.SubElement.createIn(doc)
        base.setGeometry(geom)
        base.setDiffuseColor(Base.Color(108, 103, 96))

        base.setLocalPlacement(axis1)

        self.addSubElement(base)

    def addTrafficLightGlass(self, scale, axis1, color):
        r = 0.1
        l = 0.05

        start_pnt = Geom.Pnt(-r, 0.0, 0.0)

        dir = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, -1, 0))

        pnt0 = start_pnt.rotated(dir, 22.5 * (math.pi / 180.0))
        pnt1 = start_pnt.rotated(dir, -22.5 * (math.pi / 180.0))
        pnt2 = start_pnt.rotated(dir, -67.5 * (math.pi / 180.0))
        pnt3 = start_pnt.rotated(dir, -112.5 * (math.pi / 180.0))
        pnt4 = start_pnt.rotated(dir, -157.5 * (math.pi / 180.0))
        pnt5 = start_pnt.rotated(dir, -202.5 * (math.pi / 180.0))
        pnt6 = start_pnt.rotated(dir, -247.5 * (math.pi / 180.0))
        pnt7 = start_pnt.rotated(dir, -292.5 * (math.pi / 180.0))

        glass_geom = FacetedModelAssembler(doc)
        glass_geom.beginModel()

        glass_geom.beginFace()
        glass_geom.addVertexList([pnt0, pnt1, pnt2, pnt3, pnt4, pnt5, pnt6, pnt7])
        glass_geom.endFace()

        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(glass_geom.endModel())
        elem.setDiffuseColor(color)

        elem.setLocalPlacement(axis1)
        self.addSubElement(elem)

    def addTrafficLightSection(self, scale, axis1):
        r = 0.1
        l = 0.05

        start_pnt = Geom.Pnt(-r, 0.0, 0.0)

        dir = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, -1, 0))

        pnt0 = start_pnt.rotated(dir, 22.5 * (math.pi/180.0))
        pnt1 = start_pnt.rotated(dir, -22.5 * (math.pi/180.0))
        pnt2 = start_pnt.rotated(dir, -67.5 * (math.pi/180.0))
        pnt3 = start_pnt.rotated(dir, -112.5 * (math.pi/180.0))
        pnt4 = start_pnt.rotated(dir, -157.5 * (math.pi/180.0))
        pnt5 = start_pnt.rotated(dir, -202.5 * (math.pi/180.0))
        pnt6 = pnt4.translated(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(0.0, -l * 0.7, 0.0)))
        pnt7 = pnt3.translated(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(0.0, -l, 0.0)))
        pnt8 = pnt2.translated(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(0.0, -l, 0.0)))
        pnt9 = pnt1.translated(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(0.0, -l * 0.7, 0.0)))

        caver_geom = FacetedModelAssembler(doc)
        caver_geom.beginModel()

        caver_geom.beginFace()
        caver_geom.addVertexList([pnt0, pnt9, pnt1])
        caver_geom.endFace()

        caver_geom.beginFace()
        caver_geom.addVertexList([pnt1, pnt9, pnt8, pnt2])
        caver_geom.endFace()

        caver_geom.beginFace()
        caver_geom.addVertexList([pnt2, pnt8, pnt7, pnt3])
        caver_geom.endFace()

        caver_geom.beginFace()
        caver_geom.addVertexList([pnt3, pnt7, pnt6, pnt4])
        caver_geom.endFace()

        caver_geom.beginFace()
        caver_geom.addVertexList([pnt4, pnt6, pnt5])
        caver_geom.endFace()

        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(caver_geom.endModel())
        elem.setDiffuseColor(Base.Color(224, 223, 219))

        elem.setLocalPlacement(axis1)
        self.addSubElement(elem)

    def addTrafficLight(self, type, scale, pnt):
        # base
        base_geom = FacetedModelAssembler(doc)



        self.addTrafficLightSection(1.0, Geom.Ax2(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 0, 1)))
        self.addTrafficLightGlass(1.0, Geom.Ax2(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 0, 1)), Base.Color(224, 223, 219))

    def createBase(self):
        w = self._base_width.getValue() * 0.5
        l = self._base_length.getValue() * 0.5
        h = self._base_height.getValue()

        pnt0 = Geom.Pnt(-l * 0.5, -w * 0.5, 0.0)
        pnt1 = Geom.Pnt(-l * 0.5, w * 0.5, 0.0)
        pnt2 = Geom.Pnt(l * 0.5, w * 0.5, 0.0)
        pnt3 = Geom.Pnt(l * 0.5, -w * 0.5, 0.0)

        pnt4 = Geom.Pnt(-l * 0.5, -w * 0.5, -h)
        pnt5 = Geom.Pnt(-l * 0.5, w * 0.5, -h)
        pnt6 = Geom.Pnt(l * 0.5, w * 0.5, -h)
        pnt7 = Geom.Pnt(l * 0.5, -w * 0.5, -h)

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

        geom = base_geom.endModel()

        base = lx.SubElement.createIn(doc)
        base.setGeometry(geom)
        base.setDiffuseColor(Base.Color(108, 103, 96))

        self.addSubElement(base)

    def create_profile(self, profile_type, profile_size):
        print(profile_size)
        profile = lx.IShapeProfileDef.createIn(doc)
        profile.setValuesFromPredefinedSteelProfile(lxstr(profile_type + ' ' + profile_size))

        eas2 = lx.ExtrudedAreaSolid.createIn(doc)
        eas2.setSweptArea(profile)
        eas2.setExtrudedDirection(Geom.Dir(0, 0, 1))
        eas2.setDepth(Geom.Vec(Geom.Pnt(0, 0, 0), Geom.Pnt(0, 0, self._height.getValue())).magnitude())

        element = lx.SubElement.createIn(doc)
        element.setGeometry(eas2)

        self.addSubElement(element)

    def _createGeometry(self):
        self.createBase()

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

        self.create_profile('HEB', profile_size)

    def setHeight(self, p):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(p, 5.0, 16.0))
            self._updateGeometry()

    def setProfileSize(self, p):
        with EditMode(self.getDocument()):
            self._heb.setValue(p)
            self._updateGeometry()

    def set_base_width(self, param):
        with EditMode(self.getDocument()):
            self._base_width.setValue(param)
            self._updateGeometry()

    def set_base_length(self, param):
        with EditMode(self.getDocument()):
            self._base_length.setValue(param)
            self._updateGeometry()

    def set_base_height(self, param):
        with EditMode(self.getDocument()):
            self._base_height.setValue(param)
            self._updateGeometry()

    def _updateGeometry(self):
        doc = self.getDocument()

        with EditMode(doc):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == "Height":
            self.setHeight(self._height.getValue())
        elif aPropertyName == "HEB":
            self.setProfileSize(self._heb.getValue())

        elif aPropertyName == "Base width":
            self.set_base_width(self._base_width.getValue())
        elif aPropertyName == "Base length":
            self.set_base_length(self._base_length.getValue())
        elif aPropertyName == "Base height":
            self.set_base_height(self._base_height.getValue())

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
    doc.registerPythonScript(Base.GlobalId("{534840B0-B153-4324-BC9D-A5EFDD5D1E8C}"))
    # doc.registerPythonScript(Base.GlobalId("{f0c4f2c7-7173-4d54-92f9-2ecb154261c8}")) # SubElement Class

    try:
        support = Breitflanschmast(doc)
        support.setDiffuseColor(Base.Color_fromCdwkColor(5))
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
            support.setLocalPlacement(pos)
    except Exception as e:
        print("{}".format(e))
        traceback.print_exc()
    finally:
        doc.recompute()
