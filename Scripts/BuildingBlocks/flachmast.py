# OpenLexocad libraries
# version 5.1	27.04.2020


# attributes
# version 2.0
#   cable handling

# version 3.0
#   new features

# version 4.0
#   add parameters for base(l, w, h)

# ========================================
# ====  Supported by Roman Davydiuk   ====
# ====  Mail: davydjukroman@gmail.com ====
# ====  Skype: live:davydjukroman     ====
# ========================================

import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import traceback, math, time

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

epsilon = 0.001


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


class Flachmast(lx.PythonElement):
    def getGlobalClassId(self):
        return Base.GlobalId("{0A3DB1C7-B4CE-42E9-B0B2-4E5407A14615}")

    def __init__(self, aArg):
        lx.PythonElement.__init__(self, aArg)
        self.registerPythonClass("Flachmast", "OpenLxApp.PythonElement")

        # Register properties
        self.setPropertyHeader(lxstr("Flachmast"), -1)
        self.setPropertyGroupName(lxstr("Flachmast"), -1)

        self._height = self.registerPropertyDouble("Height", 10.0, lx.Property.VISIBLE, lx.Property.EDITABLE, 95)
        self._height.setSteps(0.05)

        self._hand = self.registerPropertyEnum("Cable hand", 0, lx.Property.VISIBLE,
                                               lx.Property.EDITABLE, 96)

        self._additionalArm = self.registerPropertyEnum("Additional arm", 1, lx.Property.VISIBLE,
                                                        lx.Property.EDITABLE, 97)

        self._hand.setEmpty()
        self._hand.addEntry(lxstr("Yes"), 161)
        self._hand.addEntry(lxstr("No"), 162)

        self._additionalArm.setEmpty()
        self._additionalArm.addEntry(lxstr("Yes"), 161)
        self._additionalArm.addEntry(lxstr("No"), 162)

        # ========================================

        self._base_width = self.registerPropertyDouble("Base width", 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, 158)
        self._base_length = self.registerPropertyDouble("Base length", 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, 159)
        self._base_height = self.registerPropertyDouble("Base height", 0.4, lx.Property.VISIBLE, lx.Property.EDITABLE, 160)

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

    def createSupportBase(self):
        w = self._base_width.getValue() * 0.5
        l = self._base_length.getValue() * 0.5
        h = self._base_height.getValue()

        pnt0 = Geom.Pnt(-w, -l, -h)
        pnt1 = Geom.Pnt(w, -l, -h)
        pnt2 = Geom.Pnt(w, l, -h)
        pnt3 = Geom.Pnt(-w, l, -h)
        pnt4 = Geom.Pnt(-w, -l, 0.0)
        pnt5 = Geom.Pnt(w, -l, 0.0)
        pnt6 = Geom.Pnt(w, l, 0.0)
        pnt7 = Geom.Pnt(-w, l, 0.0)

        base = FacetedModelAssembler(doc)
        base.beginModel()

        base.beginFace()
        base.addVertexList([pnt0, pnt3, pnt2, pnt1])
        base.endFace()

        base.beginFace()
        base.addVertexList([pnt4, pnt5, pnt6, pnt7])
        base.endFace()

        base.beginFace()
        base.addVertexList([pnt0, pnt1, pnt5, pnt4])
        base.endFace()

        base.beginFace()
        base.addVertexList([pnt0, pnt4, pnt7, pnt3])
        base.endFace()

        base.beginFace()
        base.addVertexList([pnt3, pnt7, pnt6, pnt2])
        base.endFace()

        base.beginFace()
        base.addVertexList([pnt5, pnt1, pnt2, pnt6])
        base.endFace()

        betonBase = lx.SubElement.createIn(doc)
        betonBase.setGeometry(base.endModel())
        betonBase.setDiffuseColor(Base.Color(108, 103, 96))

        self.addSubElement(betonBase)

    def createBindingParts(self):
        # right
        pntR0 = Geom.Pnt(-0.32, 0.25, 0.0)
        pntR1 = Geom.Pnt(-0.18, 0.25, 0.0)
        pntR2 = Geom.Pnt(-0.18, -0.25, 0.0)
        pntR3 = Geom.Pnt(-0.32, -0.25, 0.0)

        pntR4 = Geom.Pnt(-0.32, 0.25, 0.01)
        pntR5 = Geom.Pnt(-0.18, 0.25, 0.01)
        pntR6 = Geom.Pnt(-0.18, -0.25, 0.01)
        pntR7 = Geom.Pnt(-0.32, -0.25, 0.01)

        rightBinding = FacetedModelAssembler(doc)
        rightBinding.beginModel()

        # rightBinding.beginFace()
        # rightBinding.addVertexList([pntR1, pntR2, pntR3, pntR0])
        # rightBinding.endFace()

        rightBinding.beginFace()
        rightBinding.addVertexList([pntR7, pntR6, pntR5, pntR4])
        rightBinding.endFace()

        rightBinding.beginFace()
        rightBinding.addVertexList([pntR5, pntR6, pntR2, pntR1])
        rightBinding.endFace()

        rightBinding.beginFace()
        rightBinding.addVertexList([pntR4, pntR5, pntR1, pntR0])
        rightBinding.endFace()

        rightBinding.beginFace()
        rightBinding.addVertexList([pntR3, pntR7, pntR4, pntR0])
        rightBinding.endFace()

        rightBinding.beginFace()
        rightBinding.addVertexList([pntR6, pntR7, pntR3, pntR2])
        rightBinding.endFace()

        rightBindingElement = lx.SubElement.createIn(doc)
        rightBindingElement.setGeometry(rightBinding.endModel())
        rightBindingElement.setDiffuseColor(Base.Color(46, 139, 87))

        self.addSubElement(rightBindingElement)

        # left
        pntL0 = Geom.Pnt(0.18, 0.25, 0.0)
        pntL1 = Geom.Pnt(0.32, 0.25, 0.0)
        pntL2 = Geom.Pnt(0.32, -0.25, 0.0)
        pntL3 = Geom.Pnt(0.18, -0.25, 0.0)

        pntL4 = Geom.Pnt(0.18, 0.25, 0.01)
        pntL5 = Geom.Pnt(0.32, 0.25, 0.01)
        pntL6 = Geom.Pnt(0.32, -0.25, 0.01)
        pntL7 = Geom.Pnt(0.18, -0.25, 0.01)

        leftBinding = FacetedModelAssembler(doc)
        leftBinding.beginModel()

        # leftBinding.beginFace()
        # leftBinding.addVertexList([pntL1, pntL2, pntL3, pntL0])
        # leftBinding.endFace()

        leftBinding.beginFace()
        leftBinding.addVertexList([pntL7, pntL6, pntL5, pntL4])
        leftBinding.endFace()

        leftBinding.beginFace()
        leftBinding.addVertexList([pntL5, pntL6, pntL2, pntL1])
        leftBinding.endFace()

        leftBinding.beginFace()
        leftBinding.addVertexList([pntL4, pntL5, pntL1, pntL0])
        leftBinding.endFace()

        leftBinding.beginFace()
        leftBinding.addVertexList([pntL3, pntL7, pntL4, pntL0])
        leftBinding.endFace()

        leftBinding.beginFace()
        leftBinding.addVertexList([pntL6, pntL7, pntL3, pntL2])
        leftBinding.endFace()

        leftBindingElement = lx.SubElement.createIn(doc)
        leftBindingElement.setGeometry(leftBinding.endModel())
        leftBindingElement.setDiffuseColor(Base.Color(46, 139, 87))

        self.addSubElement(leftBindingElement)

    def addBoltInToPnt(self, pnt, radius, height, ax1=None, angle=None):
        direction = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))
        pntB0 = Geom.Pnt(radius, 0.0, 0.0)
        pntB1 = pntB0.rotated(direction, 60.0 * math.pi/180.0)
        pntB2 = pntB0.rotated(direction, 120.0 * math.pi/180.0)
        pntB3 = pntB0.rotated(direction, 180.0 * math.pi/180.0)
        pntB4 = pntB0.rotated(direction, 240.0 * math.pi/180.0)
        pntB5 = pntB0.rotated(direction, 300.0 * math.pi/180.0)

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

        bolt = lx.SubElement.createIn(doc)
        bolt.setGeometry(geom.endModel())
        bolt.setDiffuseColor(Base.Color(224, 223, 219))

        axis1 = Geom.Ax2(pnt, Geom.Dir(0, 0, 1))

        bolt.setLocalPlacement(axis1)

        if ax1:
            bolt.rotate(ax1, angle)

        self.addSubElement(bolt)

    def createMast(self):
        fromZeroPnt = 0.01
        h = self._height.getValue()
        width = 0.45
        length = 0.1

        pntB0 = Geom.Pnt(-width * 0.5, -length * 0.5, fromZeroPnt)
        pntB1 = Geom.Pnt(-width * 0.5, length * 0.5, fromZeroPnt)
        pntB2 = Geom.Pnt(width * 0.5, length * 0.5, fromZeroPnt)
        pntB3 = Geom.Pnt(width * 0.5, -length * 0.5, fromZeroPnt)

        self.createStrengthening(Geom.Pnt(-width * 0.5 + 0.005, -length * 0.5 + 0.005, fromZeroPnt), 58.0)
        self.createStrengthening(Geom.Pnt(-width * 0.5 + 0.005, -length * 0.5 + 0.005, fromZeroPnt), 98.0)

        self.createStrengthening(Geom.Pnt(-width * 0.5 + 0.005, length * 0.5 - 0.005, fromZeroPnt), 302.0)
        self.createStrengthening(Geom.Pnt(-width * 0.5 + 0.005, length * 0.5 - 0.005, fromZeroPnt), -98.0)

        self.createStrengthening(Geom.Pnt(width * 0.5 - 0.005, length * 0.5 - 0.005, fromZeroPnt), 238.0)
        self.createStrengthening(Geom.Pnt(width * 0.5 - 0.005, length * 0.5 - 0.005, fromZeroPnt), -82.0)

        self.createStrengthening(Geom.Pnt(width * 0.5 - 0.005, -length * 0.5 + 0.005, fromZeroPnt), 122.0)
        self.createStrengthening(Geom.Pnt(width * 0.5 - 0.005, -length * 0.5 + 0.005, fromZeroPnt), 82.0)

        pntT0 = Geom.Pnt(-0.1, -length * 0.5, h)
        pntT1 = Geom.Pnt(-0.1, length * 0.5, h)
        pntT2 = Geom.Pnt(0.1, length * 0.5, h)
        pntT3 = Geom.Pnt(0.1, -length * 0.5, h)

        mastGeom = FacetedModelAssembler(doc)
        mastGeom.beginModel()

        mastGeom.beginFace()
        mastGeom.addVertexList([pntB0, pntT0, pntT1, pntB1])
        mastGeom.endFace()

        mastGeom.beginFace()
        mastGeom.addVertexList([pntT3, pntT2, pntT1, pntT0])
        mastGeom.endFace()

        mastGeom.beginFace()
        mastGeom.addVertexList([pntB3, pntB2, pntT2, pntT3])
        mastGeom.endFace()

        n = (h + 0.25) // 0.5
        leftLine = Line2D.from2Points(Geom.Pnt2d(pntT0.x() + 0.06, pntT0.z()), Geom.Pnt2d(pntB0.x() + 0.06, pntB0.z()))
        rightLine = Line2D.from2Points(Geom.Pnt2d(pntT3.x() - 0.06, pntT3.z()), Geom.Pnt2d(pntB3.x() - 0.06, pntB3.z()))
        sells = []
        for i in range(int(n)):
            topDistance = (h - 0.1) - (i * 0.5) - 0.03
            bottomDistance = (h - 0.1) - ((i + 1) * 0.5) + 0.03
            if bottomDistance < 0.08:
                bottomDistance = 0.08
            topLine = Line2D.from2Points(Geom.Pnt2d(-width, topDistance), Geom.Pnt2d(width, topDistance))
            bottomLine = Line2D.from2Points(Geom.Pnt2d(-width, bottomDistance), Geom.Pnt2d(width, bottomDistance))
            pnt2d0 = Line2D.intersect(leftLine, bottomLine)
            pnt2d1 = Line2D.intersect(rightLine, bottomLine)
            pnt2d2 = Line2D.intersect(rightLine, topLine)
            pnt2d3 = Line2D.intersect(leftLine, topLine)
            sells.append([pnt2d0, pnt2d1, pnt2d2, pnt2d3])

        # create front face with sells
        mastGeom.beginFace()
        mastGeom.addVertexList([pntT0, pntB0, pntB3, pntT3])
        for i in sells:
            mastGeom.endLoop()
            pnt0 = Geom.Pnt(i[0].x(), -length * 0.5, i[0].y())
            pnt1 = Geom.Pnt(i[1].x(), -length * 0.5, i[1].y())
            pnt2 = Geom.Pnt(i[2].x(), -length * 0.5, i[2].y())
            pnt3 = Geom.Pnt(i[3].x(), -length * 0.5, i[3].y())
            mastGeom.addVertexList([pnt3, pnt2, pnt1, pnt0])
        mastGeom.endFace()

        # create bottom face with cells
        mastGeom.beginFace()
        mastGeom.addVertexList([pntT2, pntB2, pntB1, pntT1])
        for i in sells:
            mastGeom.endLoop()
            pnt0 = Geom.Pnt(i[0].x(), length * 0.5, i[0].y())
            pnt1 = Geom.Pnt(i[1].x(), length * 0.5, i[1].y())
            pnt2 = Geom.Pnt(i[2].x(), length * 0.5, i[2].y())
            pnt3 = Geom.Pnt(i[3].x(), length * 0.5, i[3].y())
            mastGeom.addVertexList([pnt0, pnt1, pnt2, pnt3])
        mastGeom.endFace()

        mast = lx.SubElement.createIn(doc)
        mast.setGeometry(mastGeom.endModel())
        mast.setDiffuseColor(Base.Color(46, 139, 87))

        self.addSubElement(mast)

    def createStrengthening(self, pnt, angle):
        width = 0.01
        length = 0.175
        height = 0.2

        pnt0 = Geom.Pnt(-length, -width * 0.5, 0.0)
        pnt1 = Geom.Pnt(0.0, -width * 0.5, 0.0)
        pnt2 = Geom.Pnt(0.0, width * 0.5, 0.0)
        pnt3 = Geom.Pnt(-length, width * 0.5, 0.0)
        pnt4 = Geom.Pnt(-0.02, -width * 0.5, height)
        pnt5 = Geom.Pnt(0.0, -width * 0.5, height)
        pnt6 = Geom.Pnt(0.0, width * 0.5, height)
        pnt7 = Geom.Pnt(-0.02, width * 0.5, height)
        pnt8 = Geom.Pnt(-length, -width * 0.5, 0.05)
        pnt9 = Geom.Pnt(-length, width * 0.5, 0.05)

        strengtheningGeom = FacetedModelAssembler(doc)
        strengtheningGeom.beginModel()

        strengtheningGeom.beginFace()
        strengtheningGeom.addVertexList([pnt3, pnt2, pnt1, pnt0])
        strengtheningGeom.endFace()

        strengtheningGeom.beginFace()
        strengtheningGeom.addVertexList([pnt1, pnt2, pnt6, pnt5])
        strengtheningGeom.endFace()

        strengtheningGeom.beginFace()
        strengtheningGeom.addVertexList([pnt4, pnt5, pnt6, pnt7])
        strengtheningGeom.endFace()

        strengtheningGeom.beginFace()
        strengtheningGeom.addVertexList([pnt4, pnt7, pnt9, pnt8])
        strengtheningGeom.endFace()

        strengtheningGeom.beginFace()
        strengtheningGeom.addVertexList([pnt0, pnt8, pnt9, pnt3])
        strengtheningGeom.endFace()

        strengtheningGeom.beginFace()
        strengtheningGeom.addVertexList([pnt0, pnt1, pnt5, pnt4, pnt8])
        strengtheningGeom.endFace()

        strengtheningGeom.beginFace()
        strengtheningGeom.addVertexList([pnt3, pnt9, pnt7, pnt6, pnt2])
        strengtheningGeom.endFace()


        strengthening = lx.SubElement.createIn(doc)
        strengthening.setGeometry(strengtheningGeom.endModel())
        strengthening.setDiffuseColor(Base.Color(46, 139, 87))

        axis1 = Geom.Ax2(pnt, Geom.Dir(0, 0, 1))

        strengthening.setLocalPlacement(axis1)
        strengthening.rotate(Geom.Ax1(pnt, Geom.Dir(0.0, 0.0, 1.0)), angle * (math.pi/180.0))

        self.addSubElement(strengthening)

    def createCableHand(self):
        h = self._height.getValue() - 0.01
        length = 0.1
        width = 0.2

        th = 0.08

        pnt0 = Geom.Pnt(-width * 0.5 - 0.01,      -length * 0.5 - 0.002,      h)
        pnt1 = Geom.Pnt(-width * 0.5 - 0.01,      -length * 0.5 - 0.002,      h - th)
        pnt2 = Geom.Pnt(width * 0.5 + 0.05,       -length * 0.5 - 0.002,      h - th)
        pnt3 = Geom.Pnt(width * 0.5 + 0.05,       -length * 0.5 - 0.002,      h)

        pnt4 = Geom.Pnt(width * 0.5 + 0.5,        -0.001,      h - th)
        pnt5 = Geom.Pnt(width * 0.5 + 0.5,        -0.001,      h)
        pnt6 = Geom.Pnt(1.1,                     -0.001,                      h - th)
        pnt7 = Geom.Pnt(1.1,                     -0.001,                      h)

        pnt8 = Geom.Pnt(-width * 0.5 - 0.01,      -length * 0.5 - 0.03,      h)
        pnt9 = Geom.Pnt(width * 0.5 + 0.05,       -length * 0.5 - 0.03,      h)
        pnt10 = Geom.Pnt(width * 0.5 + 0.5,       -0.001 - 0.03,             h)
        pnt11 = Geom.Pnt(1.1,                     -0.001 - 0.03,             h)

        pnt12 = Geom.Pnt(-width * 0.5 - 0.01,      -length * 0.5 - 0.03,      h - th)
        pnt13 = Geom.Pnt(width * 0.5 + 0.05,       -length * 0.5 - 0.03,      h - th)
        pnt14 = Geom.Pnt(width * 0.5 + 0.5,        -0.001 - 0.03,      h - th)
        pnt15 = Geom.Pnt(1.1,                      -0.001 - 0.03,                      h - th)

        hand = FacetedModelAssembler(doc)
        hand.beginModel()

        hand.beginFace()
        hand.addVertexList([pnt0, pnt1, pnt2, pnt3])
        hand.endFace()

        hand.beginFace()
        hand.addVertexList([pnt3, pnt2, pnt4, pnt5])
        hand.endFace()

        hand.beginFace()
        hand.addVertexList([pnt5, pnt4, pnt6, pnt7])
        hand.endFace()

        hand.beginFace()
        hand.addVertexList([pnt8, pnt0, pnt3, pnt9])
        hand.endFace()

        hand.beginFace()
        hand.addVertexList([pnt9, pnt3, pnt5, pnt10])
        hand.endFace()

        hand.beginFace()
        hand.addVertexList([pnt10, pnt5, pnt7, pnt11])
        hand.endFace()

        hand.beginFace()
        hand.addVertexList([pnt1, pnt12, pnt13, pnt2])
        hand.endFace()

        hand.beginFace()
        hand.addVertexList([pnt2, pnt13, pnt14, pnt4])
        hand.endFace()

        hand.beginFace()
        hand.addVertexList([pnt4, pnt14, pnt15, pnt6])
        hand.endFace()

        handGeom = hand.endModel()

        topHand = lx.SubElement.createIn(doc)
        topHand.setGeometry(handGeom)
        topHand.setDiffuseColor(Base.Color(46, 139, 87))

        topHand.setDiffuseColor(Base.Color(46, 139, 87))

        self.addSubElement(topHand)

        bottomHand = lx.SubElement.createIn(doc)
        bottomHand.setGeometry(handGeom)
        bottomHand.setDiffuseColor(Base.Color(46, 139, 87))

        bottomHand.rotate(Geom.Ax1(
            Geom.Pnt(-width * 0.5 - 0.01, 0.0, h - (th * 0.5)),
            Geom.Dir(1.0, 0.0, 0.0)), 180.0 * (math.pi/180.0))

        self.addSubElement(bottomHand)



        if self._additionalArm.getValue() is not 1:
            addTopHand = lx.SubElement.createIn(doc)
            addTopHand.setGeometry(handGeom)
            addTopHand.rotate(Geom.Ax1(
                Geom.Pnt(0.0, 0.0, 0.0),
                Geom.Dir(0.0, 0.0, 1.0)), 180.0 * (math.pi/180.0))
            addTopHand.setDiffuseColor(Base.Color(46, 139, 87))
            self.addSubElement(addTopHand)

            addBottomHand = lx.SubElement.createIn(doc)
            addBottomHand.setGeometry(handGeom)
            addBottomHand.rotate(Geom.Ax1(
                Geom.Pnt(-width * 0.5 - 0.01, 0.0, h - (th * 0.5)),
                Geom.Dir(1.0, 0.0, 0.0)), 180.0 * (math.pi/180.0))
            addBottomHand.rotate(Geom.Ax1(
                Geom.Pnt(0.0, 0.0, 0.0),
                Geom.Dir(0.0, 0.0, 1.0)), 180.0 * (math.pi/180.0))
            addBottomHand.setDiffuseColor(Base.Color(46, 139, 87))
            self.addSubElement(addBottomHand)

        # connections bolts to mast
        self.addBoltInToPnt(Geom.Pnt(0.05, -length * 0.5, h - (th * 0.5)), 0.02, 0.015,
                            Geom.Ax1(Geom.Pnt(0.5, -length * 0.5, h - (th * 0.5)), Geom.Dir(1.0, 0.0, 0.0)),
                            90.0 * (math.pi / 180.0))

        self.addBoltInToPnt(Geom.Pnt(-0.05, -length * 0.5, h - (th * 0.5)), 0.02, 0.015,
                            Geom.Ax1(Geom.Pnt(0.5, -length * 0.5, h - (th * 0.5)), Geom.Dir(1.0, 0.0, 0.0)),
                            90.0 * (math.pi / 180.0))

        self.addBoltInToPnt(Geom.Pnt(0.05, length * 0.5, h - (th * 0.5)), 0.02, 0.015,
                            Geom.Ax1(Geom.Pnt(0.5, length * 0.5, h - (th * 0.5)), Geom.Dir(1.0, 0.0, 0.0)),
                            -90.0 * (math.pi / 180.0))

        self.addBoltInToPnt(Geom.Pnt(-0.05, length * 0.5, h - (th * 0.5)), 0.02, 0.015,
                            Geom.Ax1(Geom.Pnt(0.5, length * 0.5, h - (th * 0.5)), Geom.Dir(1.0, 0.0, 0.0)),
                            -90.0 * (math.pi / 180.0))

        fuseDirRotation = Geom.Dir(0.0, 1.0, 0.0)
        self.createFuse(Geom.Pnt(1.1 - 0.035, 0.0, h - th), fuseDirRotation, 180.0 + 30)
        self.createFuse(Geom.Pnt(0.035 + width * 0.5 + 0.5, 0.0, h - th), fuseDirRotation, 180.0 - 30)

        self.cabbleHolder(
            Geom.Pnt(((1.1 - 0.035) + (0.035 + width * 0.5 + 0.5)) * 0.5, 0.0, self._height.getValue() - 0.37))

    def createFuse(self, pnt, dir, angle):
        r = 0.005
        R = 0.04
        L = 0.35
        l = 0.22

        pnt0 = [Geom.Pnt(r, 0.0, L)]
        pnt1 = [Geom.Pnt(R, 0.0, (L - l) * 0.5 + l)]
        pnt2 = [Geom.Pnt(R, 0.0, (L - l) * 0.5)]
        pnt3 = [Geom.Pnt(r, 0.0, 0.0)]

        for i in range(4):
            pnt0.append(pnt0[len(pnt0) - 1].rotated(Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0.0, 0.0, 1.0)), (360.0 / 5.0) * (math.pi / 180.0)))
            pnt1.append(pnt1[len(pnt1) - 1].rotated(Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0.0, 0.0, 1.0)), (360.0 / 5.0) * (math.pi / 180.0)))
            pnt2.append(pnt2[len(pnt2) - 1].rotated(Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0.0, 0.0, 1.0)), (360.0 / 5.0) * (math.pi / 180.0)))
            pnt3.append(pnt3[len(pnt3) - 1].rotated(Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0.0, 0.0, 1.0)), (360.0 / 5.0) * (math.pi / 180.0)))

        fuseGeom = FacetedModelAssembler(doc)
        fuseGeom.beginModel()

        for i in range(4):
            fuseGeom.beginFace()
            fuseGeom.addVertexList([pnt0[i], pnt1[i], pnt1[i+1], pnt0[i+1]])
            fuseGeom.endFace()

            fuseGeom.beginFace()
            fuseGeom.addVertexList([pnt1[i], pnt2[i], pnt2[i+1], pnt1[i+1]])
            fuseGeom.endFace()

            fuseGeom.beginFace()
            fuseGeom.addVertexList([pnt2[i], pnt3[i], pnt3[i+1], pnt2[i+1]])
            fuseGeom.endFace()

        fuseGeom.beginFace()
        fuseGeom.addVertexList([pnt1[0], pnt0[0], pnt0[4], pnt1[4]])
        fuseGeom.endFace()

        fuseGeom.beginFace()
        fuseGeom.addVertexList([pnt2[0], pnt1[0], pnt1[4], pnt2[4]])
        fuseGeom.endFace()

        fuseGeom.beginFace()
        fuseGeom.addVertexList([pnt2[0], pnt2[4], pnt3[4], pnt3[0]])
        fuseGeom.endFace()

        # top and bottom
        fuseGeom.beginFace()
        fuseGeom.addVertexList(pnt0)
        fuseGeom.endFace()

        fuseGeom.beginFace()
        fuseGeom.addVertexList(pnt3)
        fuseGeom.endFace()

        geom = fuseGeom.endModel()

        fuse = lx.SubElement.createIn(doc)
        fuse.setGeometry(geom)
        fuse.setDiffuseColor(Base.Color(60, 0, 0))

        axis1 = Geom.Ax2(pnt, Geom.Dir(0, 0, 1))

        fuse.setLocalPlacement(axis1)
        fuse.rotate(Geom.Ax1(pnt, dir), angle * (math.pi/180.0))

        self.addSubElement(fuse)

        if self._additionalArm.getValue() is not 1:
            addFuse = lx.SubElement.createIn(doc)
            addFuse.setGeometry(geom)
            addFuse.setLocalPlacement(axis1)
            addFuse.rotate(Geom.Ax1(pnt, dir), angle * (math.pi/180.0))
            addFuse.rotate(Geom.Ax1(
                Geom.Pnt(0.0, 0.0, 0.0),
                Geom.Dir(0.0, 0.0, 1.0)), 180.0 * (math.pi/180.0))
            addFuse.setDiffuseColor(Base.Color(60, 0, 0))
            self.addSubElement(addFuse)

    def cabbleHolder(self, pnt):
        pnt0 = Geom.Pnt(-0.06, -0.01, 0.0)
        pnt1 = Geom.Pnt(0.06, -0.01, 0.0)
        pnt2 = Geom.Pnt(0.06, 0.01, 0.0)
        pnt3 = Geom.Pnt(-0.06, 0.01, 0.0)
        pnt4 = Geom.Pnt(0.0, -0.01, -0.07)
        pnt5 = Geom.Pnt(0.0, 0.01, -0.07)

        holderGeom = FacetedModelAssembler(doc)
        holderGeom.beginModel()

        holderGeom.beginFace()
        holderGeom.addVertexList([pnt0, pnt1, pnt2, pnt3])
        holderGeom.endFace()

        holderGeom.beginFace()
        holderGeom.addVertexList([pnt4, pnt1, pnt0])
        holderGeom.endFace()

        holderGeom.beginFace()
        holderGeom.addVertexList([pnt5, pnt3, pnt2])
        holderGeom.endFace()

        holderGeom.beginFace()
        holderGeom.addVertexList([pnt0, pnt3, pnt5, pnt4])
        holderGeom.endFace()

        holderGeom.beginFace()
        holderGeom.addVertexList([pnt2, pnt1, pnt4, pnt5])
        holderGeom.endFace()

        geom = holderGeom.endModel()

        holder = lx.SubElement.createIn(doc)
        holder.setGeometry(geom)
        holder.setDiffuseColor(Base.Color(200, 200, 200))

        axis1 = Geom.Ax2(pnt, Geom.Dir(0, 0, 1))

        holder.setLocalPlacement(axis1)

        self.addSubElement(holder)

        if self._additionalArm.getValue() is not 1:
            addHolder = lx.SubElement.createIn(doc)
            addHolder.setGeometry(geom)

            addHolder.setLocalPlacement(axis1)
            addHolder.rotate(Geom.Ax1(
                Geom.Pnt(0.0, 0.0, 0.0),
                Geom.Dir(0.0, 0.0, 1.0)), 180.0 * (math.pi/180.0))
            addHolder.setDiffuseColor(Base.Color(200, 200, 200))
            self.addSubElement(addHolder)

    def _createGeometry(self):
        self.createSupportBase()
        self.createBindingParts()
        self.addBoltInToPnt(Geom.Pnt(0.25, 0.2, 0.01), 0.04, 0.025)
        self.addBoltInToPnt(Geom.Pnt(-0.25, 0.2, 0.01), 0.04, 0.025)
        self.addBoltInToPnt(Geom.Pnt(0.25, -0.2, 0.01), 0.04, 0.025)
        self.addBoltInToPnt(Geom.Pnt(-0.25, -0.2, 0.01), 0.04, 0.025)
        self.createMast()

        hand = self._hand.getValue()
        if hand is not 1:
            self.createCableHand()

    def setHeight(self, p):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(p, 6.0, 13.5))
            self._updateGeometry()

    def setHand(self, hand):
        with EditMode(self.getDocument()):
            self._hand.setValue(hand)
            self._updateGeometry()

    def setAdditionalArm(self, param):
        with EditMode(self.getDocument()):
            self._additionalArm.setValue(param)
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
        elif aPropertyName == "Cable hand":
            self.setHand(self._hand.getValue())
        elif aPropertyName == "Additional arm":
            self.setAdditionalArm(self._additionalArm.getValue())
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
    doc.registerPythonScript(Base.GlobalId("{768ECD68-6D17-4015-9C0A-B5BBD6ECB822}"))
    # doc.registerPythonScript(Base.GlobalId("{f0c4f2c7-7173-4d54-92f9-2ecb154261c8}")) # SubElement Class

    try:
        flachmast_pile = Flachmast(doc)
        flachmast_pile.setDiffuseColor(Base.Color_fromCdwkColor(20))
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
            flachmast_pile.setLocalPlacement(pos)
    except Exception as e:
        print("{}".format(e))
        traceback.print_exc()
    finally:
        doc.recompute()