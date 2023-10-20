 # coding=utf-8
# OpenLexocad libraries
import math

import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

epsilon = 0.001

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

def qstr(str):
   return Base.StringTool.toQString(lxstr(str))
#Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))

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

def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))

def vecsAreSame(v1, v2, tolerance = epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)

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
                return index

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
        print(geom)
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

class RoofCreator(lx.Element):

    _p1ParamName = "Roof slope"
    _p2ParamName = "Outside wall"
    _p3ParamName = "Wall height"
    _p4ParamName = "Purlin length"
    _p5ParamName = "Wall thickness"
    _p6ParamName = "Wall pocket depth"
    _p7ParamName = "Rafter overhang"
    _p8ParamName = "Rafter width"
    _p9ParamName = "Rafter height"
    _p10ParamName = "Purlin width"
    _p11ParamName = "Purlin height"
    _p12ParamName = "Number of purlins"
    _p13ParamName = "Ridge width"
    _p14ParamName = "Ridge height"
    _p15ParamName = "Wall plate width"
    _p16ParamName = "Wall plate height"
    _p17ParamName = "Wall plate overhang"
    _p18ParamName = "Chamfer height"
    _p19ParamName = "Main rafter width"
    _p20ParamName = "Main rafter height"
    _p21ParamName = "Depth of joint"
    _p22ParamName = "Collar tie width"
    _p23ParamName = "Collar tie height"
    _p24ParamName = "Distance below Collar tie // slab"
    _p25ParamName = "King post width"
    _p26ParamName = "King post height"
    _p27ParamName = "Tie width"
    _p28ParamName = "Tie height"
    _p29ParamName = "Distance Wall // top Tie"
    _p30ParamName = "Overhang Tie"
    _p31ParamName = "Strut width"
    _p32ParamName = "Strut height"
    _p33ParamName = "Distance Wall // Strut"
    _p34ParamName = "Strut angle"
    _p35ParamName = "Bolster width"
    _p36ParamName = "Bolster height"
    _p37ParamName = "Cleat width"
    #_p38ParamName = "Bolt diameter"
    _p39ParamName = "Lateral strut width"
    _p40ParamName = "Lateral strut height"
    _p41ParamName = "Distance Strut // top collar tie"
    _p42ParamName = "Lateral strut Angle"
    _p43ParamName = "Lap depth"
    _p44ParamName = "Top strut width"
    _p45ParamName = "Top strut height"
    _p46ParamName = "Distance Strut // bottom collar tie"
    _p47ParamName = "Top strut angle"
    _p48ParamName = "Struts?"
    _p60ParamName = "Chamfer to axis?"

    def getGlobalClassId(self):
        return Base.GlobalId("{83BFF676-CB93-4533-ADDC-CC924AB1052A}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("RoofCreator", "OpenLxApp.Element")
        # Register properties 
        self.setPropertyHeader(lxstr("RoofCreator"), -1)
        self.setPropertyGroupName(lxstr("Roof Parameter"), -1)

        self._p1 = self.registerPropertyDouble(self._p1ParamName, 30.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p2 = self.registerPropertyDouble(self._p2ParamName, 8.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p3 = self.registerPropertyDouble(self._p3ParamName, 1.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p4 = self.registerPropertyDouble(self._p4ParamName, 5.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p5 = self.registerPropertyDouble(self._p5ParamName, 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p6 = self.registerPropertyDouble(self._p6ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p7 = self.registerPropertyDouble(self._p7ParamName, 0.5, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p8 = self.registerPropertyDouble(self._p8ParamName, 0.06, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p9 = self.registerPropertyDouble(self._p9ParamName, 0.08, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p10 = self.registerPropertyDouble(self._p10ParamName, 0.12, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p11 = self.registerPropertyDouble(self._p11ParamName, 0.24, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p12 = self.registerPropertyInteger(self._p12ParamName, 2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p13 = self.registerPropertyDouble(self._p13ParamName, 0.12, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p14 = self.registerPropertyDouble(self._p14ParamName, 0.24, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p15 = self.registerPropertyDouble(self._p15ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p16 = self.registerPropertyDouble(self._p16ParamName, 0.08, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p17 = self.registerPropertyDouble(self._p17ParamName, 0.015, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p18 = self.registerPropertyDouble(self._p18ParamName, 0.015, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p19 = self.registerPropertyDouble(self._p19ParamName, 0.12, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p20 = self.registerPropertyDouble(self._p20ParamName, 0.24, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p21 = self.registerPropertyDouble(self._p21ParamName, 0.01, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p22 = self.registerPropertyDouble(self._p22ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p23 = self.registerPropertyDouble(self._p23ParamName, 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p24 = self.registerPropertyDouble(self._p24ParamName, 2.3, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p25 = self.registerPropertyDouble(self._p25ParamName, 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p26 = self.registerPropertyDouble(self._p26ParamName, 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p27 = self.registerPropertyDouble(self._p27ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p28 = self.registerPropertyDouble(self._p28ParamName, 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p29 = self.registerPropertyDouble(self._p29ParamName, 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p30 = self.registerPropertyDouble(self._p30ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p31 = self.registerPropertyDouble(self._p31ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p32 = self.registerPropertyDouble(self._p32ParamName, 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p33 = self.registerPropertyDouble(self._p33ParamName, 0.65, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p34 = self.registerPropertyDouble(self._p34ParamName, 65.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p35 = self.registerPropertyDouble(self._p35ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p36 = self.registerPropertyDouble(self._p36ParamName, 0.2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p37 = self.registerPropertyDouble(self._p37ParamName, 0.12, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        #self._p38 = self.registerPropertyDouble(self._p38ParamName, 0.016, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p39 = self.registerPropertyDouble(self._p39ParamName, 0.12, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p40 = self.registerPropertyDouble(self._p40ParamName, 0.12, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p41 = self.registerPropertyDouble(self._p41ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p42 = self.registerPropertyDouble(self._p42ParamName, 45, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p43 = self.registerPropertyDouble(self._p43ParamName, 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p44 = self.registerPropertyDouble(self._p44ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p45 = self.registerPropertyDouble(self._p45ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p46 = self.registerPropertyDouble(self._p46ParamName, 0.05, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p47 = self.registerPropertyDouble(self._p47ParamName, 45.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._p48 = self.registerPropertyEnum(self._p48ParamName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p48.setEmpty()
        self._p48.addEntry(lxstr("0"), -1)
        self._p48.addEntry(lxstr("1"), -1)

        self._p60 = self.registerPropertyEnum(self._p60ParamName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p60.setEmpty()
        self._p60.addEntry(lxstr("0"), -1)
        self._p60.addEntry(lxstr("1"), -1)

        self._p2.setSteps(0.01)
        self._p3.setSteps(0.01)
        self._p4.setSteps(0.01)
        self._p5.setSteps(0.01)
        self._p6.setSteps(0.01)
        self._p7.setSteps(0.01)
        self._p8.setSteps(0.01)
        self._p9.setSteps(0.01)
        self._p10.setSteps(0.01)
        self._p11.setSteps(0.01)
        self._p13.setSteps(0.01)
        self._p14.setSteps(0.01)
        self._p15.setSteps(0.01)
        self._p16.setSteps(0.01)
        self._p17.setSteps(0.01)
        self._p18.setSteps(0.01)
        self._p19.setSteps(0.01)
        self._p20.setSteps(0.01)
        self._p21.setSteps(0.01)
        self._p22.setSteps(0.01)
        self._p23.setSteps(0.01)
        self._p24.setSteps(0.01)
        self._p25.setSteps(0.01)
        self._p26.setSteps(0.01)
        self._p27.setSteps(0.01)
        self._p28.setSteps(0.01)
        self._p29.setSteps(0.01)
        self._p30.setSteps(0.01)
        self._p31.setSteps(0.01)
        self._p32.setSteps(0.01)
        self._p33.setSteps(0.01)
        self._p35.setSteps(0.01)
        self._p36.setSteps(0.01)
        self._p37.setSteps(0.01)
        self._p39.setSteps(0.01)
        self._p40.setSteps(0.01)
        self._p41.setSteps(0.01)
        self._p43.setSteps(0.01)
        self._p44.setSteps(0.01)
        self._p45.setSteps(0.01)
        self._p46.setSteps(0.01)

        
        self._updateGeometry()

    @staticmethod
    def buildSubElemLine(aDoc, aFromPnt, aToPnt):
        res = Geom.Vec(aToPnt.xyz() - aFromPnt.xyz())
        dir = Geom.Dir(res.normalized())
        line = lx.Line.createIn(aDoc)
        line.setPoint(aFromPnt)
        line.setDirection(dir)
        tc = lx.TrimmedCurve.createIn(aDoc)
        tc.setBasisCurve(line)
        tc.setTrim1(0)
        tc.setTrim2(res.magnitude())
        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(tc)
        return elem

    @staticmethod
    def _createSubElement(listPoint, heightStep, dir):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)
        return subElem

    @staticmethod
    def _createExtrudedGeom(listPoint, heightStep, dir):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        return geom

    def _createPurlins(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p4 = self._p4.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p12 = self._p12.getValue()
        p13 = self._p13.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p37 = self._p37.getValue()
        p60 = self._p60.getValue()

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)

        topMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ),
                                         Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ))

        leftInsideY = (p2 - p13) * 0.5

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)

        insideLinePnt0 = Geom.Pnt2d(leftInsideY, 0.0)
        insideLinePnt1 = Geom.Pnt2d(leftInsideY, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)
        insidePnt = Line2D.intersect(mainLine, insideLine)

        mainVec = Geom.Vec(Geom.Pnt(0.0, -p17, p16 - p18), Geom.Pnt(0.0, leftInsideY, insidePnt.y()))

        stepVec = mainVec.divided(p12 + 1)

        pnt0 = Geom.Pnt(p4 * 0.5, -p17, p16 - p11)
        pnt1 = Geom.Pnt(p4 * 0.5, p10 - p17, p16 - p11)
        pnt2 = Geom.Pnt(p4 * 0.5, p10 - p17, p16)
        pnt3 = Geom.Pnt(p4 * 0.5, ((math.cos(p1) * p18) / math.sin(p1)) - p17, p16)
        pnt4 = Geom.Pnt(p4 * 0.5, -p17, p16 - p18)

        angle = ((math.pi * 0.5) - p1) * 0.5

        lineSup = Line2D.from2Points(Geom.Pnt2d(-p17, p16 - p18), Geom.Pnt2d(-p17 - math.sin(angle), p16 - p18 - math.cos(angle)))
        supPnt2d = Line2D.intersect(topMainLine, lineSup)

        firstSupPnt0 = Geom.Pnt(p37 * 0.5, supPnt2d.x(), supPnt2d.y())
        firstSupPnt1 = Geom.Pnt(p37 * 0.5, p10 - p17, p16 - p11)
        firstSupPnt2 = Geom.Pnt(p37 * 0.5, -p17, p16 - p11)
        firstSupPnt3 = Geom.Pnt(p37 * 0.5, -p17, p16 - p18)

        for i in range(1, p12+1):
            distVec = stepVec.multiplied(i)
            tPnt0 = pnt0.translated(distVec)
            tPnt1 = pnt1.translated(distVec)
            tPnt2 = pnt2.translated(distVec)
            tPnt3 = pnt3.translated(distVec)
            tPnt4 = pnt4.translated(distVec)

            supPnt0 = firstSupPnt0.translated(distVec)
            supPnt1 = firstSupPnt1.translated(distVec)
            supPnt2 = firstSupPnt2.translated(distVec)
            supPnt3 = firstSupPnt3.translated(distVec)

            geom = self._createExtrudedGeom([tPnt0, tPnt1, tPnt2, tPnt3, tPnt4], p4, Geom.Dir(-1.0, 0.0, 0.0))
            geomSup = self._createExtrudedGeom([supPnt0, supPnt1, supPnt2, supPnt3], p37, Geom.Dir(-1.0, 0.0, 0.0))
            firstSubElem = lx.SubElement.createIn(doc)
            secondSubElem = lx.SubElement.createIn(doc)
            supFirstSubElem = lx.SubElement.createIn(doc)
            supSecondSubElem = lx.SubElement.createIn(doc)

            firstSubElem.setGeometry(geom)
            secondSubElem.setGeometry(geom)
            self.addSubElement(firstSubElem)
            secondSubElem.rotate(Geom.Ax1(Geom.Pnt(0.0, p2 * 0.5, 0.0), Geom.Dir(0.0, 0.0, 1.0)), math.pi)
            self.addSubElement(secondSubElem)

            supFirstSubElem.setGeometry(geomSup)
            supSecondSubElem.setGeometry(geomSup)
            self.addSubElement(supFirstSubElem)
            supSecondSubElem.rotate(Geom.Ax1(Geom.Pnt(0.0, p2 * 0.5, 0.0), Geom.Dir(0.0, 0.0, 1.0)), math.pi)
            self.addSubElement(supSecondSubElem)

    def _createWallPlates(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p4 = self._p4.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60

        pnt0First = Geom.Pnt(p4 * 0.5, -p17, 0.0)
        pnt1First = Geom.Pnt(p4 * 0.5, p15 - p17, 0.0)
        pnt2First = Geom.Pnt(p4 * 0.5, p15 - p17, p16)
        pnt3First = Geom.Pnt(p4 * 0.5, ((math.cos(p1) * p18) / math.sin(p1)) - p17, p16)
        pnt4First = Geom.Pnt(p4 * 0.5, -p17, p16 - p18)

        geom = self._createExtrudedGeom([pnt0First, pnt1First, pnt2First, pnt3First, pnt4First], p4, Geom.Dir(-1.0, 0.0, 0.0))
        firstSubElem = lx.SubElement.createIn(doc)
        secondSubElem = lx.SubElement.createIn(doc)
        firstSubElem.setGeometry(geom)
        secondSubElem.setGeometry(geom)
        self.addSubElement(firstSubElem)
        secondSubElem.rotate(Geom.Ax1(Geom.Pnt(0.0, p2 * 0.5, 0.0), Geom.Dir(0.0, 0.0, 1.0)), math.pi)
        self.addSubElement(secondSubElem)

    def _createBolster(self):
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p5 = self._p5.getValue()
        p30 = self._p30.getValue()
        p32 = self._p32.getValue()
        p33 = self._p33.getValue()
        p34 = self._p34.getValue() / (180.0 / math.pi)
        p35 = self._p35.getValue()
        p36 = self._p36.getValue()

        pnt0First = Geom.Pnt(p36 * 0.5, (p35 * 0.5) + (p32 / math.sin(p34)) + (p30 / math.sin(p34)) + p33 + p5, -p3)
        pnt1First = Geom.Pnt(p36 * 0.5, p5, -p3)
        pnt2First = Geom.Pnt(p36 * 0.5, p5, p35 - p3)
        pnt3First = Geom.Pnt(p36 * 0.5, (p32 / math.sin(p34)) + (p30 / math.sin(p34)) + p33 + p5, p35 - p3)
        pnt4First = Geom.Pnt(p36 * 0.5, (p35 * 0.5) + (p32 / math.sin(p34)) + (p30 / math.sin(p34)) + p33 + p5, p35 - p3 - (p35 * 0.5))

        firstBolsterElem = self._createSubElement([pnt0First, pnt1First, pnt2First, pnt3First, pnt4First], p36, Geom.Dir(-1.0, 0.0, 0.0))
        self.addSubElement(firstBolsterElem)

        pnt0Second = Geom.Pnt(p36 * 0.5, p2 - ((p35 * 0.5) + (p32 / math.sin(p34)) + (p30 / math.sin(p34)) + p33 + p5), - p3)
        pnt1Second = Geom.Pnt(p36 * 0.5, p2 - p5, - p3)
        pnt2Second = Geom.Pnt(p36 * 0.5, p2 - p5, p35 - p3)
        pnt3Second = Geom.Pnt(p36 * 0.5, p2 - ((p32 / math.sin(p34)) + (p30 / math.sin(p34)) + p33 + p5), p35 - p3)
        pnt4Second = Geom.Pnt(p36 * 0.5, p2 - ((p35 * 0.5) + (p32 / math.sin(p34)) + (p30 / math.sin(p34)) + p33 + p5), p35 - p3 - (p35 * 0.5))

        secondBolsterElem = self._createSubElement([pnt0Second, pnt1Second, pnt2Second, pnt3Second, pnt4Second], p36, Geom.Dir(-1.0, 0.0, 0.0))
        self.addSubElement(secondBolsterElem)

    def _createTie(self):
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p5 = self._p5.getValue()
        p6 = self._p6.getValue()
        p27 = self._p27.getValue()
        p28 = self._p28.getValue()
        p29 = self._p29.getValue()
        p30 = self._p30.getValue()
        p31 = self._p31.getValue()
        p32 = self._p32.getValue()
        p33 = self._p33.getValue()
        p34 = self._p34.getValue() / (180.0 / math.pi)
        p35 = self._p35.getValue()
        p43 = self._p43.getValue()

        dim = (p32 / math.sin(p34)) + (p30 / math.sin(p34)) + p33 + p5

        #left
        pnt0FirstLeft = Geom.Pnt((p31 * 0.5) + p27 - p43, dim + (((p3 + p29 - p28 - p35) * math.cos(p34)) / math.sin(p34)), p29 - p28)
        pnt1FirstLeft = Geom.Pnt((p31 * 0.5) + p27 - p43, p5 - p6, p29 - p28)
        pnt2FirstLeft = Geom.Pnt((p31 * 0.5) + p27 - p43, p5 - p6, p29)
        pnt3FirstLeft = Geom.Pnt((p31 * 0.5) + p27 - p43, dim + (((p3 + p29 - p35) * math.cos(p34)) / math.sin(p34)), p29)

        firstTieElem = self._createSubElement([pnt0FirstLeft, pnt1FirstLeft, pnt2FirstLeft, pnt3FirstLeft], p27, Geom.Dir(-1.0, 0.0, 0.0))
        self.addSubElement(firstTieElem)

        pnt0SecondLeft = Geom.Pnt(-p31 * 0.5 + p43, dim + (((p3 + p29 - p28 - p35) * math.cos(p34)) / math.sin(p34)), p29 - p28)
        pnt1SecondLeft = Geom.Pnt(-p31 * 0.5 + p43, p5 - p6, p29 - p28)
        pnt2SecondLeft = Geom.Pnt(-p31 * 0.5 + p43, p5 - p6, p29)
        pnt3SecondLeft = Geom.Pnt(-p31 * 0.5 + p43, dim + (((p3 + p29 - p35) * math.cos(p34)) / math.sin(p34)), p29)

        firstTieElem = self._createSubElement([pnt0SecondLeft, pnt1SecondLeft, pnt2SecondLeft, pnt3SecondLeft], p27, Geom.Dir(-1.0, 0.0, 0.0))
        self.addSubElement(firstTieElem)

        #right
        pnt0FirstRight = Geom.Pnt((p31 * 0.5) + p27 - p43, p2 - (dim + (((p3 + p29 - p28 - p35) * math.cos(p34)) / math.sin(p34))), p29 - p28)
        pnt1FirstRight = Geom.Pnt((p31 * 0.5) + p27 - p43, p2 - (p5 - p6), p29 - p28)
        pnt2FirstRight = Geom.Pnt((p31 * 0.5) + p27 - p43, p2 - (p5 - p6), p29)
        pnt3FirstRight = Geom.Pnt((p31 * 0.5) + p27 - p43, p2 - (dim + (((p3 + p29 - p35) * math.cos(p34)) / math.sin(p34))), p29)

        firstTieElem = self._createSubElement([pnt0FirstRight, pnt1FirstRight, pnt2FirstRight, pnt3FirstRight], p27, Geom.Dir(-1.0, 0.0, 0.0))
        self.addSubElement(firstTieElem)

        pnt0SecondRight = Geom.Pnt(-p31 * 0.5 + p43, p2 - (dim + (((p3 + p29 - p28 - p35) * math.cos(p34)) / math.sin(p34))), p29 - p28)
        pnt1SecondRight = Geom.Pnt(-p31 * 0.5 + p43, p2 - (p5 - p6), p29 - p28)
        pnt2SecondRight = Geom.Pnt(-p31 * 0.5 + p43, p2 - (p5 - p6), p29)
        pnt3SecondRight = Geom.Pnt(-p31 * 0.5 + p43, p2 - (dim + (((p3 + p29 - p35) * math.cos(p34)) / math.sin(p34))), p29)

        firstTieElem = self._createSubElement([pnt0SecondRight, pnt1SecondRight, pnt2SecondRight, pnt3SecondRight], p27, Geom.Dir(-1.0, 0.0, 0.0))
        self.addSubElement(firstTieElem)

    def _createRafter(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p5 = self._p5.getValue()
        p6 = self._p6.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p19 = self._p19.getValue()
        p20 = self._p20.getValue()
        p21 = self._p21.getValue()
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p25 = self._p25.getValue()
        p28 = self._p28.getValue()
        p29 = self._p29.getValue()
        p43 = self._p43.getValue()
        p60 = float(self._p60.getValue())

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)
        insideY = (p2 - p25) * 0.5
        outsideY = p5 - p6

        topMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ), Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ))
        bottomMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))), Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))

        insideLine = Line2D.from2Points(Geom.Pnt2d(insideY, 0.0), Geom.Pnt2d(insideY, 1.0))
        outsideLine = Line2D.from2Points(Geom.Pnt2d(outsideY, 0.0), Geom.Pnt2d(outsideY, 1.0))

        topCollarTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p24 + p23 - p3), Geom.Pnt2d(1.0, p24 + p23 - p3))
        bottomCollarTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p24 - p3), Geom.Pnt2d(1.0, p24 - p3))

        topTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p29), Geom.Pnt2d(1.0, p29))
        bottomTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p29 - p28), Geom.Pnt2d(1.0, p29 - p28))

        outBottomPnt = Line2D.intersect(outsideLine, bottomMainLine)
        insideBottomPnt = Line2D.intersect(insideLine, bottomMainLine)
        insideTopPnt = Line2D.intersect(insideLine, topMainLine)
        outTopPnt = Line2D.intersect(outsideLine, topMainLine)
        outMiddlePnt = Line2D.intersect(bottomTieLine, outsideLine)
        bottomTiePnt = Line2D.intersect(bottomTieLine, bottomMainLine)
        topTieMainPnt = Line2D.intersect(topTieLine, bottomMainLine)
        topTieOutLine = Line2D.intersect(topMainLine, topTieLine)

        bottomRightPntCollarTie = Line2D.intersect(bottomCollarTieLine, bottomMainLine)
        topRightPntCollarTie = Line2D.intersect(topCollarTieLine, bottomMainLine)
        topLeftPntCollarTie = Line2D.intersect(topCollarTieLine, topMainLine)
        bottomLeftPntCollarTie = Line2D.intersect(bottomCollarTieLine, topMainLine)

        pnt0 = Geom.Pnt(p19 * 0.5, outBottomPnt.x(), outBottomPnt.y())
        pnt1 = Geom.Pnt(p19 * 0.5, insideBottomPnt.x(), insideBottomPnt.y())
        pnt2 = Geom.Pnt(p19 * 0.5, insideTopPnt.x(), insideTopPnt.y())
        pnt3 = Geom.Pnt((p19 * 0.5) - p21 - p43, outTopPnt.x(), outTopPnt.y())
        pnt4 = Geom.Pnt(p19 * 0.5, outMiddlePnt.x(), outMiddlePnt.y())
        pnt5 = Geom.Pnt(p19 * 0.5, bottomTiePnt.x(), bottomTiePnt.y())
        pnt6 = Geom.Pnt(p19 * 0.5, topTieMainPnt.x(), topTieMainPnt.y())
        pnt7 = Geom.Pnt(p19 * 0.5, topTieOutLine.x(), topTieOutLine.y())
        pnt8 = Geom.Pnt(p19 * 0.5, bottomRightPntCollarTie.x(), bottomRightPntCollarTie.y())
        pnt9 = Geom.Pnt(p19 * 0.5, topRightPntCollarTie.x(), topRightPntCollarTie.y())
        pnt10 = Geom.Pnt(p19 * 0.5, topLeftPntCollarTie.x(), topLeftPntCollarTie.y())
        pnt11 = Geom.Pnt(p19 * 0.5, bottomLeftPntCollarTie.x(), bottomLeftPntCollarTie.y())
        pnt12 = Geom.Pnt((p19 * 0.5) - p21 - p43, bottomTiePnt.x(), bottomTiePnt.y())
        pnt13 = Geom.Pnt((p19 * 0.5) - p21 - p43, outMiddlePnt.x(), outMiddlePnt.y())
        pnt14 = Geom.Pnt((p19 * 0.5) - p21 - p43, topTieOutLine.x(), topTieOutLine.y())
        pnt15 = Geom.Pnt((p19 * 0.5) - p21 - p43, topTieMainPnt.x(), topTieMainPnt.y())
        pnt16 = Geom.Pnt((p19 * 0.5) - p21 - p43, bottomRightPntCollarTie.x(), bottomRightPntCollarTie.y())
        pnt17 = Geom.Pnt((p19 * 0.5) - p21 - p43, topRightPntCollarTie.x(), topRightPntCollarTie.y())
        pnt18 = Geom.Pnt((p19 * 0.5) - p21 - p43, topLeftPntCollarTie.x(), topLeftPntCollarTie.y())
        pnt19 = Geom.Pnt((p19 * 0.5) - p21 - p43, bottomLeftPntCollarTie.x(), bottomLeftPntCollarTie.y())

        pnt20 = Geom.Pnt(-p19 * 0.5, outBottomPnt.x(), outBottomPnt.y())
        pnt21 = Geom.Pnt(-p19 * 0.5, insideBottomPnt.x(), insideBottomPnt.y())
        pnt22 = Geom.Pnt(-p19 * 0.5, insideTopPnt.x(), insideTopPnt.y())
        pnt23 = Geom.Pnt(-(p19 * 0.5) + p21 + p43, outTopPnt.x(), outTopPnt.y())
        pnt24 = Geom.Pnt(-p19 * 0.5, outMiddlePnt.x(), outMiddlePnt.y())
        pnt25 = Geom.Pnt(-p19 * 0.5, bottomTiePnt.x(), bottomTiePnt.y())
        pnt26 = Geom.Pnt(-p19 * 0.5, topTieMainPnt.x(), topTieMainPnt.y())
        pnt27 = Geom.Pnt(-p19 * 0.5, topTieOutLine.x(), topTieOutLine.y())
        pnt28 = Geom.Pnt(-p19 * 0.5, bottomRightPntCollarTie.x(), bottomRightPntCollarTie.y())
        pnt29 = Geom.Pnt(-p19 * 0.5, topRightPntCollarTie.x(), topRightPntCollarTie.y())
        pnt30 = Geom.Pnt(-p19 * 0.5, topLeftPntCollarTie.x(), topLeftPntCollarTie.y())
        pnt31 = Geom.Pnt(-p19 * 0.5, bottomLeftPntCollarTie.x(), bottomLeftPntCollarTie.y())
        pnt32 = Geom.Pnt(-(p19 * 0.5) + p21 + p43, bottomTiePnt.x(), bottomTiePnt.y())
        pnt33 = Geom.Pnt(-(p19 * 0.5) + p21 + p43, outMiddlePnt.x(), outMiddlePnt.y())
        pnt34 = Geom.Pnt(-(p19 * 0.5) + p21 + p43, topTieOutLine.x(), topTieOutLine.y())
        pnt35 = Geom.Pnt(-(p19 * 0.5) + p21 + p43, topTieMainPnt.x(), topTieMainPnt.y())
        pnt36 = Geom.Pnt(-(p19 * 0.5) + p21 + p43, bottomRightPntCollarTie.x(), bottomRightPntCollarTie.y())
        pnt37 = Geom.Pnt(-(p19 * 0.5) + p21 + p43, topRightPntCollarTie.x(), topRightPntCollarTie.y())
        pnt38 = Geom.Pnt(-(p19 * 0.5) + p21 + p43, topLeftPntCollarTie.x(), topLeftPntCollarTie.y())
        pnt39 = Geom.Pnt(-(p19 * 0.5) + p21 + p43, bottomLeftPntCollarTie.x(), bottomLeftPntCollarTie.y())

        mdl = FacetedModelAssembler(doc)
        mdl.beginModel()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt5, pnt4])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt4, pnt5, pnt12, pnt13])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt13, pnt12, pnt15, pnt14, pnt3])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt7, pnt14, pnt15, pnt6])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt7, pnt6, pnt8, pnt11])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt8, pnt16, pnt19, pnt11])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt19, pnt16, pnt17, pnt18])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt10, pnt18, pnt17, pnt9])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt10, pnt9, pnt1, pnt2])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt24, pnt25, pnt20])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt33, pnt32, pnt25, pnt24])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt23, pnt34, pnt35, pnt32, pnt33])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt26, pnt35, pnt34, pnt27])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt31, pnt28, pnt26, pnt27])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt31, pnt39, pnt36, pnt28])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt38, pnt37, pnt36, pnt39])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt29, pnt37, pnt38, pnt30])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt22, pnt21, pnt29, pnt30])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt4, pnt13, pnt3, pnt23, pnt33, pnt24, pnt20])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt2, pnt1, pnt21, pnt22])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt3, pnt14, pnt7, pnt11, pnt19, pnt18, pnt10, pnt2, pnt22, pnt30, pnt38, pnt39, pnt31, pnt27, pnt34, pnt23])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt1, pnt9, pnt17, pnt16, pnt8, pnt6, pnt15, pnt12, pnt5, pnt0, pnt20, pnt25, pnt32, pnt35, pnt26, pnt28, pnt36, pnt37, pnt29, pnt21])
        mdl.endFace()

        geom = mdl.endModel()

        firstSubElement = lx.SubElement.createIn(doc)
        secondSubElement = lx.SubElement.createIn(doc)
        firstSubElement.setGeometry(geom)
        secondSubElement.setGeometry(geom)
        angleAxis = Geom.Ax1(Geom.Pnt(0.0, p2 * 0.5, 0.0), Geom.Dir(0.0, 0.0, 1.0))
        secondSubElement.rotate(angleAxis, math.pi, Geom.CoordSpace_WCS)

        self.addSubElement(firstSubElement)
        self.addSubElement(secondSubElement)

    def _createKingPost(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p13 = self._p13.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p19 = self._p19.getValue()
        p21 = self._p21.getValue()
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p25 = self._p25.getValue()
        p26 = self._p26.getValue()
        p60 = float(self._p60.getValue())

        frontOutsideX = p26 * 0.5
        backOutsideX = -p26 * 0.5

        frontInsideX = (p19 * 0.5) - p21
        backInsideX = (- p19 * 0.5) + p21

        leftOutsideY = (p2 - p25) * 0.5
        rightOutsideY = (p2 + p25) * 0.5

        leftInsideY = (p2 - p13) * 0.5
        rightInsideY = (p2 + p13) * 0.5

        bottomHeight = p24 - p3

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)

        outsideLinePnt0 = Geom.Pnt2d(leftOutsideY, 0.0)
        outsideLinePnt1 = Geom.Pnt2d(leftOutsideY, 1.0)
        outsideLine = Line2D.from2Points(outsideLinePnt0, outsideLinePnt1)

        insideLinePnt0 = Geom.Pnt2d(leftInsideY, 0.0)
        insideLinePnt1 = Geom.Pnt2d(leftInsideY, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)

        outsidePnt = Line2D.intersect(mainLine, outsideLine)
        insidePnt = Line2D.intersect(mainLine, insideLine)

        plaseForPurlinZ = insidePnt.y() - p14 + (p18 * (1.0 - p60) + p13 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60)

        pnt0 = Geom.Pnt(backOutsideX, leftOutsideY, outsidePnt.y())
        pnt1 = Geom.Pnt(frontOutsideX, leftOutsideY, outsidePnt.y())
        pnt2 = Geom.Pnt(frontOutsideX, leftInsideY, insidePnt.y())
        pnt3 = Geom.Pnt(backOutsideX, leftInsideY, insidePnt.y())
        pnt4 = Geom.Pnt(backOutsideX, rightInsideY, insidePnt.y())
        pnt5 = Geom.Pnt(frontOutsideX, rightInsideY, insidePnt.y())
        pnt6 = Geom.Pnt(frontOutsideX, rightOutsideY, outsidePnt.y())
        pnt7 = Geom.Pnt(backOutsideX, rightOutsideY, outsidePnt.y())
        pnt8 = Geom.Pnt(backOutsideX, leftInsideY, plaseForPurlinZ)
        pnt9 = Geom.Pnt(frontOutsideX, leftInsideY, plaseForPurlinZ)
        pnt10 = Geom.Pnt(frontOutsideX, rightInsideY, plaseForPurlinZ)
        pnt11 = Geom.Pnt(backOutsideX, rightInsideY, plaseForPurlinZ)
        pnt12 = Geom.Pnt(backOutsideX, leftOutsideY, bottomHeight + p23)
        pnt13 = Geom.Pnt(frontOutsideX, leftOutsideY, bottomHeight + p23)
        pnt14 = Geom.Pnt(frontOutsideX, rightOutsideY, bottomHeight + p23)
        pnt15 = Geom.Pnt(backOutsideX, rightOutsideY, bottomHeight + p23)

        pnt16 = Geom.Pnt(frontInsideX, leftOutsideY, bottomHeight + p23)
        pnt17 = Geom.Pnt(backInsideX, leftOutsideY, bottomHeight + p23)
        pnt18 = Geom.Pnt(backInsideX, rightOutsideY, bottomHeight + p23)
        pnt19 = Geom.Pnt(frontInsideX, rightOutsideY, bottomHeight + p23)
        pnt20 = Geom.Pnt(frontInsideX, rightOutsideY, bottomHeight)
        pnt21 = Geom.Pnt(backInsideX, rightOutsideY, bottomHeight)
        pnt22 = Geom.Pnt(backInsideX, leftOutsideY, bottomHeight)
        pnt23 = Geom.Pnt(frontInsideX, leftOutsideY, bottomHeight)

        mdl = FacetedModelAssembler(doc)
        mdl.beginModel()

        mdl.beginFace()
        mdl.addVertexList([pnt3, pnt2, pnt9, pnt8])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt8, pnt9, pnt10, pnt11])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt4, pnt11, pnt10, pnt5])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt1, pnt13, pnt14, pnt6, pnt5, pnt10, pnt9, pnt2])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt12, pnt0, pnt3, pnt8, pnt11, pnt4, pnt7, pnt15])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt4, pnt5, pnt6, pnt7])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt1, pnt2, pnt3])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt20, pnt21, pnt18, pnt15, pnt7, pnt6, pnt14, pnt19])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt23, pnt16, pnt13, pnt1, pnt0, pnt12, pnt17, pnt22])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt20, pnt23, pnt22, pnt21])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt20, pnt19, pnt16, pnt23])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt17, pnt18, pnt21, pnt22])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt18, pnt17, pnt12, pnt15])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt13, pnt16, pnt19, pnt14])
        mdl.endFace()

        subElement = lx.SubElement.createIn(doc)
        subElement.setGeometry(mdl.endModel())

        self.addSubElement(subElement)

    def _createChevron(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p7 = self._p7.getValue()
        p8 = self._p8.getValue()
        p9 = self._p9.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)

        outsideLinePnt0 = Geom.Pnt2d(-p7, 0.0)
        outsideLinePnt1 = Geom.Pnt2d(-p7, 1.0)
        outsideLine = Line2D.from2Points(outsideLinePnt0, outsideLinePnt1)

        insideLinePnt0 = Geom.Pnt2d(p2 * 0.5, 0.0)
        insideLinePnt1 = Geom.Pnt2d(p2 * 0.5, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)

        outsidePnt = Line2D.intersect(mainLine, outsideLine)
        insidePnt = Line2D.intersect(mainLine, insideLine)

        pnt0 = Geom.Pnt(p8 * 0.5, -p7, outsidePnt.y() + (p9 / math.cos(p1)))
        pnt1 = Geom.Pnt(p8 * 0.5, -p7, outsidePnt.y())
        pnt2 = Geom.Pnt(p8 * 0.5, p2 * 0.5, insidePnt.y() + (p9 / math.cos(p1)))
        pnt3 = Geom.Pnt(p8 * 0.5, p2 * 0.5, insidePnt.y())
        pnt4 = Geom.Pnt(p8 * 0.5, p2 + p7, outsidePnt.y() + (p9 / math.cos(p1)))
        pnt5 = Geom.Pnt(p8 * 0.5, p2 + p7, outsidePnt.y())

        leftChevronElem = self._createSubElement([pnt0, pnt1, pnt3, pnt2], p8, Geom.Dir(-1.0, 0.0, 0.0))
        rightChevronElem = self._createSubElement([pnt2, pnt3, pnt5, pnt4], p8, Geom.Dir(-1.0, 0.0, 0.0))
        self.addSubElement(leftChevronElem)
        self.addSubElement(rightChevronElem)

    def _createRidge(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p4 = self._p4.getValue()
        p13 = self._p13.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p60 = float(self._p60.getValue())

        catet = (p18 * (1.0 - p60) + p13 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60)

        leftInsideY = (p2 - p13) * 0.5
        rightInsideY = (p2 + p13) * 0.5

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)
        insideLinePnt0 = Geom.Pnt2d(leftInsideY, 0.0)
        insideLinePnt1 = Geom.Pnt2d(leftInsideY, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)

        insidePnt = Line2D.intersect(mainLine, insideLine)

        plaseForPurlinZ = insidePnt.y() - p14 + (p18 * (1.0 - p60) + p13 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60)

        pnt0 = Geom.Pnt(p4 * 0.5, leftInsideY, plaseForPurlinZ)
        pnt1 = Geom.Pnt(p4 * 0.5, rightInsideY, plaseForPurlinZ)
        pnt2 = Geom.Pnt(p4 * 0.5, rightInsideY, insidePnt.y())
        pnt3 = Geom.Pnt(p4 * 0.5, leftInsideY, insidePnt.y())

        if p60 == 0.0:
            pnt4 = Geom.Pnt(p4 * 0.5, rightInsideY - ((catet * math.cos(p1)) / math.sin(p1)), insidePnt.y() + catet)
            pnt5 = Geom.Pnt(p4 * 0.5, leftInsideY + ((catet * math.cos(p1)) / math.sin(p1)), insidePnt.y() + catet)

            ridgeElem = self._createSubElement([pnt0, pnt3, pnt5, pnt4, pnt2, pnt1], p4, Geom.Dir(-1.0, 0.0, 0.0))
            self.addSubElement(ridgeElem)

        elif p60 == 1.0:
            pnt4 = Geom.Pnt(p4 * 0.5, p2 * 0.5, plaseForPurlinZ + p14)
            ridgeElem = self._createSubElement([pnt0, pnt3, pnt4, pnt2, pnt1], p4, Geom.Dir(-1.0, 0.0, 0.0))
            self.addSubElement(ridgeElem)

    def _createCollarTie(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p19 = self._p19.getValue()
        p21 = self._p21.getValue()
        p22 = self._p22.getValue()
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p60 = self._p60.getValue()

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)

        topMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ), Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ))

        topCollarTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p24 + p23 - p3), Geom.Pnt2d(1.0, p24 + p23 - p3))
        bottomCollarTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p24 - p3), Geom.Pnt2d(1.0, p24 - p3))
        topLeftPntCollarTie = Line2D.intersect(topCollarTieLine, topMainLine)
        bottomLeftPntCollarTie = Line2D.intersect(bottomCollarTieLine, topMainLine)

        pnt0First = Geom.Pnt((p19 * 0.5) - p21, topLeftPntCollarTie.x(), topLeftPntCollarTie.y())
        pnt1First = Geom.Pnt((p19 * 0.5) - p21, bottomLeftPntCollarTie.x(), bottomLeftPntCollarTie.y())
        pnt2First = Geom.Pnt((p19 * 0.5) - p21, p2 - bottomLeftPntCollarTie.x(), bottomLeftPntCollarTie.y())
        pnt3First = Geom.Pnt((p19 * 0.5) - p21, p2 - topLeftPntCollarTie.x(), topLeftPntCollarTie.y())

        pnt0Second = Geom.Pnt(-(p19 * 0.5) + p21, topLeftPntCollarTie.x(), topLeftPntCollarTie.y())
        pnt1Second = Geom.Pnt(-(p19 * 0.5) + p21, bottomLeftPntCollarTie.x(), bottomLeftPntCollarTie.y())
        pnt2Second = Geom.Pnt(-(p19 * 0.5) + p21, p2 - bottomLeftPntCollarTie.x(), bottomLeftPntCollarTie.y())
        pnt3Second = Geom.Pnt(-(p19 * 0.5) + p21, p2 - topLeftPntCollarTie.x(), topLeftPntCollarTie.y())

        firstElem = self._createSubElement([pnt0First, pnt1First, pnt2First, pnt3First], p22, Geom.Dir(1.0, 0.0, 0.0))
        secondElem = self._createSubElement([pnt0Second, pnt1Second, pnt2Second, pnt3Second], p22, Geom.Dir(-1.0, 0.0, 0.0))
        self.addSubElement(firstElem)
        self.addSubElement(secondElem)

    def _createStruts(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p20 = self._p20.getValue()
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p25 = self._p25.getValue()
        p44 = self._p44.getValue()
        p45 = self._p45.getValue()
        p46 = self._p46.getValue()
        p47 = self._p47.getValue() / (180.0 / math.pi)
        p60 = self._p60.getValue()

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)

        leftOutsideY = (p2 - p25) * 0.5

        bottomHeight = p24 - p3

        bottomMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))), Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))
        topStrutsLine = Line2D.from2Points(Geom.Pnt2d(leftOutsideY, bottomHeight + p23 + (p45 / math.cos(p47)) + p46), Geom.Pnt(leftOutsideY - math.cos(p47), bottomHeight + p23 + (p45 / math.cos(p47)) + p46 + math.sin(p47)))
        bottomStrutsLine = Line2D.from2Points(Geom.Pnt2d(leftOutsideY, bottomHeight + p23 + p46), Geom.Pnt2d(leftOutsideY - math.cos(p47), bottomHeight + p23 + p46 + math.sin(p47)))

        pnt02d = Line2D.intersect(bottomMainLine, bottomStrutsLine)
        pnt12d = Line2D.intersect(bottomMainLine, topStrutsLine)

        pnt0 = Geom.Pnt(p44 * 0.5, pnt02d.x(), pnt02d.y())
        pnt1 = Geom.Pnt(p44 * 0.5, pnt12d.x(), pnt12d.y())
        pnt2 = Geom.Pnt(p44 * 0.5, leftOutsideY, bottomHeight + p23 + (p45 / math.cos(p47)) + p46)
        pnt3 = Geom.Pnt(p44 * 0.5, leftOutsideY, bottomHeight + p23 + p46)

        geom = self._createExtrudedGeom([pnt0, pnt1, pnt2, pnt3], p44, Geom.Dir(-1.0, 0.0, 0.0))
        firstSubElem = lx.SubElement.createIn(doc)
        secondSubElem = lx.SubElement.createIn(doc)
        firstSubElem.setGeometry(geom)
        secondSubElem.setGeometry(geom)
        self.addSubElement(firstSubElem)
        secondSubElem.rotate(Geom.Ax1(Geom.Pnt(0.0, p2 * 0.5, 0.0), Geom.Dir(0.0, 0.0, 1.0)), math.pi)
        self.addSubElement(secondSubElem)

    def _createBottomStruts(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p5 = self._p5.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p20 = self._p20.getValue()
        p28 = self._p28.getValue()
        p29 = self._p29.getValue()
        p31 = self._p31.getValue()
        p32 = self._p32.getValue()
        p33 = self._p33.getValue()
        p34 = self._p34.getValue() / (180.0 / math.pi)
        p35 = self._p35.getValue()
        p43 = self._p43.getValue()
        p60 = self._p60.getValue()

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)

        bottomMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))), Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))

        outsideLine = Line2D.from2Points(Geom.Pnt2d(p33 + p5, p35 - p3), Geom.Pnt(p33 + p5 + math.cos(p34), p35 - p3 + math.sin(p34)))
        insideLine = Line2D.from2Points(Geom.Pnt2d((p32 / math.sin(p34)) + p33 + p5, p35 - p3), Geom.Pnt((p32 / math.sin(p34)) + p33 + p5 + math.cos(p34), p35 - p3 + math.sin(p34)))

        outsidePnt = Line2D.intersect(bottomMainLine, outsideLine)
        insidePnt = Line2D.intersect(bottomMainLine, insideLine)


        topTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p29), Geom.Pnt2d(1.0, p29))
        bottomTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p29 - p28), Geom.Pnt2d(1.0, p29 - p28))

        topLeftPnt = Line2D.intersect(outsideLine, topTieLine)
        topRightPnt = Line2D.intersect(topTieLine, insideLine)
        bottomLeftPnt = Line2D.intersect(outsideLine, bottomTieLine)
        bottomRightPnt = Line2D.intersect(insideLine, bottomTieLine)



        pnt0 = Geom.Pnt(p31 * 0.5, (p32 / math.sin(p34)) + p33 + p5, p35 - p3)
        pnt1 = Geom.Pnt(p31 * 0.5, p33 + p5, p35 - p3)
        pnt2 = Geom.Pnt(p31 * 0.5, outsidePnt.x(), outsidePnt.y())
        pnt3 = Geom.Pnt(p31 * 0.5, insidePnt.x(), insidePnt.y())

        pnt4 = Geom.Pnt(p31 * 0.5, bottomRightPnt.x(), bottomRightPnt.y())
        pnt5 = Geom.Pnt(p31 * 0.5, bottomLeftPnt.x(), bottomLeftPnt.y())
        pnt6 = Geom.Pnt(p31 * 0.5, topLeftPnt.x(), topLeftPnt.y())
        pnt7 = Geom.Pnt(p31 * 0.5, topRightPnt.x(), topRightPnt.y())

        pnt8 = Geom.Pnt(p31 * 0.5 - p43, bottomRightPnt.x(), bottomRightPnt.y())
        pnt9 = Geom.Pnt(p31 * 0.5 - p43, bottomLeftPnt.x(), bottomLeftPnt.y())
        pnt10 = Geom.Pnt(p31 * 0.5 - p43, topLeftPnt.x(), topLeftPnt.y())
        pnt11 = Geom.Pnt(p31 * 0.5 - p43, topRightPnt.x(), topRightPnt.y())

        pnt12 = Geom.Pnt(-p31 * 0.5, (p32 / math.sin(p34)) + p33 + p5, p35 - p3)
        pnt13 = Geom.Pnt(-p31 * 0.5, p33 + p5, p35 - p3)
        pnt14 = Geom.Pnt(-p31 * 0.5, outsidePnt.x(), outsidePnt.y())
        pnt15 = Geom.Pnt(-p31 * 0.5, insidePnt.x(), insidePnt.y())

        pnt16 = Geom.Pnt(-p31 * 0.5, bottomRightPnt.x(), bottomRightPnt.y())
        pnt17 = Geom.Pnt(-p31 * 0.5, bottomLeftPnt.x(), bottomLeftPnt.y())
        pnt18 = Geom.Pnt(-p31 * 0.5, topLeftPnt.x(), topLeftPnt.y())
        pnt19 = Geom.Pnt(-p31 * 0.5, topRightPnt.x(), topRightPnt.y())

        pnt20 = Geom.Pnt(-p31 * 0.5 + p43, bottomRightPnt.x(), bottomRightPnt.y())
        pnt21 = Geom.Pnt(-p31 * 0.5 + p43, bottomLeftPnt.x(), bottomLeftPnt.y())
        pnt22 = Geom.Pnt(-p31 * 0.5 + p43, topLeftPnt.x(), topLeftPnt.y())
        pnt23 = Geom.Pnt(-p31 * 0.5 + p43, topRightPnt.x(), topRightPnt.y())

        mdl = FacetedModelAssembler(doc)
        mdl.beginModel()

        mdl.beginFace()
        mdl.addVertexList([pnt1, pnt5, pnt9, pnt10, pnt6, pnt2, pnt14, pnt18, pnt22, pnt21, pnt17, pnt13])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt1, pnt13, pnt12])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt3, pnt7, pnt11, pnt8, pnt4, pnt0, pnt12, pnt16, pnt20, pnt23, pnt19, pnt15])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt2, pnt3, pnt15, pnt14])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt4, pnt5, pnt1])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt5, pnt4, pnt8, pnt9])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt9, pnt8, pnt11, pnt10])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt6, pnt10, pnt11, pnt7])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt6, pnt7, pnt3, pnt2])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt15, pnt19, pnt18, pnt14])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt19, pnt23, pnt22, pnt18])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt23, pnt20, pnt21, pnt22])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt16, pnt17, pnt21, pnt20])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt16, pnt12, pnt13, pnt17])
        mdl.endFace()

        geom = mdl.endModel()
        firstSubElem = lx.SubElement.createIn(doc)
        secondSubElem = lx.SubElement.createIn(doc)
        firstSubElem.setGeometry(geom)
        secondSubElem.setGeometry(geom)
        self.addSubElement(firstSubElem)
        secondSubElem.rotate(Geom.Ax1(Geom.Pnt(0.0, p2 * 0.5, 0.0), Geom.Dir(0.0, 0.0, 1.0)), math.pi)
        self.addSubElement(secondSubElem)

    def _createLateralStruts(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p13 = self._p13.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p25 = self._p25.getValue()
        p39 = self._p39.getValue()
        p40 = self._p40.getValue()
        p41 = self._p41.getValue()
        p42 = self._p42.getValue() / (180.0 / math.pi)
        p60 = self._p60.getValue()

        leftInsideY = (p2 - p13) * 0.5

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)

        insideLinePnt0 = Geom.Pnt2d(leftInsideY, 0.0)
        insideLinePnt1 = Geom.Pnt2d(leftInsideY, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)

        insidePnt = Line2D.intersect(mainLine, insideLine)

        plaseForPurlinZ = insidePnt.y() - p14 + (p18 * (1.0 - p60) + p13 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60)
        heightStruts = plaseForPurlinZ - (p24 - p3 + p23 + p41)
        lengthStruts = (heightStruts * math.cos(p42)) / math.sin(p42)

        pnt0 = Geom.Pnt((p25 * 0.5), (p2 - p39) * 0.5, p24 - p3 + p23 + p41 + (p40 / math.cos(p42)))
        pnt1 = Geom.Pnt((p25 * 0.5), (p2 - p39) * 0.5, p24 - p3 + p23 + p41)
        pnt2 = Geom.Pnt((p25 * 0.5) + lengthStruts, (p2 - p39) * 0.5, plaseForPurlinZ)
        pnt3 = Geom.Pnt((p25 * 0.5) + lengthStruts - (p40 / math.sin(p42)), (p2 - p39) * 0.5, plaseForPurlinZ)

        geom = self._createExtrudedGeom([pnt0, pnt1, pnt2, pnt3], p39, Geom.Dir(0.0, 1.0, 0.0))
        firstSubElem = lx.SubElement.createIn(doc)
        secondSubElem = lx.SubElement.createIn(doc)
        firstSubElem.setGeometry(geom)
        secondSubElem.setGeometry(geom)
        self.addSubElement(firstSubElem)
        secondSubElem.rotate(Geom.Ax1(Geom.Pnt(0.0, p2 * 0.5, 0.0), Geom.Dir(0.0, 0.0, 1.0)), math.pi)
        self.addSubElement(secondSubElem)

    def createCompound(self):
        p48 = self._p48.getValue()
        self._createWallPlates()
        self._createBolster()
        self._createTie()
        self._createRafter()
        self._createKingPost()
        self._createChevron()
        self._createRidge()
        self._createCollarTie()
        if p48 == 1:
            self._createStruts()
        self._createBottomStruts()
        self._createLateralStruts()
        if self._p12.getValue() >= 1:
            self._createPurlins()


    @staticmethod
    def maxInList(lst):
        assert lst
        m = lst[0]
        for i in lst:
            if i > m:
                m = i
        return m

    def _updateGeometry(self):
        doc = self.getDocument()
        with EditMode(doc):
            self.removeSubElements()
            self.createCompound()

    def setP1(self, p1):
        with EditMode(self.getDocument()):
            self._p1.setValue(clamp(p1, self.minP1(), self.maxP1()))
            self._updateGeometry()
        if p1 < self.minP1():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p1 > self.maxP1():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p1(self):
        return self._p1.getValue()

    def minP1(self):
        return 10.0

    def maxP1(self):
        return 80.0

    def setP2(self, p2):
        with EditMode(self.getDocument()):
            self._p2.setValue(clamp(p2, self.minP2(), self.maxP2()))

            self._updateGeometry()
        if p2 < self.minP2():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p2 > self.maxP2():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p2(self):
        return self._p2.getValue()

    def minP2(self):
        return 0.1

    def maxP2(self):
        return 100000.0

    def setP3(self, p3):
        with EditMode(self.getDocument()):
            self._p3.setValue(clamp(p3, self.minP3(), self.maxP3()))
            self._updateGeometry()
        if p3 < self.minP3():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p3 > self.maxP3():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p3(self):
        return self._p3.getValue()

    def minP3(self):
        return 0.001

    def maxP3(self):
        return 10000.0

    def setP4(self, p4):
        with EditMode(self.getDocument()):
            self._p4.setValue(clamp(p4, self.minP4(), self.maxP4()))
            self._updateGeometry()
        if p4 < self.minP4():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p4 > self.maxP4():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p4(self):
        return self._p4.getValue()

    def minP4(self):
        return 0.001

    def maxP4(self):
        return 10000.0

    def setP5(self, p5):
        with EditMode(self.getDocument()):
            self._p5.setValue(clamp(p5, self.minP5(), self.maxP5()))
            self._updateGeometry()
        if p5 < self.minP5():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p5 > self.maxP5():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p5(self):
        return self._p5.getValue()

    def minP5(self):
        return self._p6.getValue() + epsilon

    def maxP5(self):
        return 1000.0

    def setP6(self, p6):
        with EditMode(self.getDocument()):
            self._p6.setValue(clamp(p6, self.minP6(), self.maxP6()))
            self._updateGeometry()
        if p6 < self.minP6():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p6 > self.maxP6():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p6(self):
        return self._p6.getValue()

    def minP6(self):
        return 0.001

    def maxP6(self):
        return self._p5.getValue() - epsilon

    def setP7(self, p7):
        with EditMode(self.getDocument()):
            self._p7.setValue(clamp(p7, self.minP7(), self.maxP7()))
            self._updateGeometry()
        if p7 < self.minP7():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p7 > self.maxP7():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p7(self):
        return self._p7.getValue()

    def minP7(self):
        return 0.001

    def maxP7(self):
        return 10000.0

    def setP8(self, p8):
        with EditMode(self.getDocument()):
            self._p8.setValue(clamp(p8, self.minP8(), self.maxP8()))
            self._updateGeometry()
        if p8 < self.minP8():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p8 > self.maxP8():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p8(self):
        return self._p8.getValue()

    def minP8(self):
        return 0.001

    def maxP8(self):
        return 10000.0

    def setP9(self, p9):
        with EditMode(self.getDocument()):
            self._p9.setValue(clamp(p9, self.minP9(), self.maxP9()))
            self._updateGeometry()
        if p9 < self.minP9():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p9 > self.maxP9():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p9(self):
        return self._p9.getValue()

    def minP9(self):
        return 0.001

    def maxP9(self):
        return 10000.0

    def setP10(self, p10):
        with EditMode(self.getDocument()):
            self._p10.setValue(clamp(p10, self.minP10(), self.maxP10()))
            self._updateGeometry()
        if p10 < self.minP10():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p10 > self.maxP10():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p10(self):
        return self._p10.getValue()

    def minP10(self):
        return 0.001

    def maxP10(self):
        return 100000.0

    def setP11(self, p11):
        with EditMode(self.getDocument()):
            self._p11.setValue(clamp(p11, self.minP11(), self.maxP11()))
            self._updateGeometry()
        if p11 < self.minP11():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p11 > self.maxP11():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p11(self):
        return self._p11.getValue()

    def minP11(self):
        return 0.001

    def maxP11(self):
        return 10000.0

    def setP12(self, p12):
        with EditMode(self.getDocument()):
            self._p12.setValue(clamp(p12, self.minP12(), self.maxP12()))
            self._updateGeometry()
        if p12 < self.minP12():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p12 > self.maxP12():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p12(self):
        return self._p12.getValue()

    def minP12(self):
        return 0

    def maxP12(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p13 = self._p13.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p60 = self._p60.getValue()

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)

        topMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ),
                                         Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ))

        leftInsideY = (p2 - p13) * 0.5

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)

        insideLinePnt0 = Geom.Pnt2d(leftInsideY, 0.0)
        insideLinePnt1 = Geom.Pnt2d(leftInsideY, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)
        insidePnt = Line2D.intersect(mainLine, insideLine)

        mainVec = Geom.Vec(Geom.Pnt(0.0, -p17, p16 - p18), Geom.Pnt(0.0, leftInsideY, insidePnt.y()))

        angle = ((math.pi * 0.5) - p1) * 0.5

        lineSup = Line2D.from2Points(Geom.Pnt2d(-p17, p16 - p18),
                                     Geom.Pnt2d(-p17 - math.sin(angle), p16 - p18 - math.cos(angle)))
        supPnt2d = Line2D.intersect(topMainLine, lineSup)

        step = Geom.Vec(Geom.Pnt(0.0, supPnt2d.x(), supPnt2d.y()), Geom.Pnt(0.0, -p17, p16 - p18))
        maxValue = int(mainVec.magnitude() / step.magnitude())
        return maxValue

    def setP13(self, p13):
        with EditMode(self.getDocument()):
            self._p13.setValue(clamp(p13, self.minP13(), self.maxP13()))
            self._updateGeometry()
        if p13 < self.minP13():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p13 > self.maxP13():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p13(self):
        return self._p13.getValue()

    def minP13(self):
        return 0.0001

    def maxP13(self):
        return self._p25.getValue() - epsilon

    def setP14(self, p14):
        with EditMode(self.getDocument()):
            self._p14.setValue(clamp(p14, self.minP14(), self.maxP14()))
            self._updateGeometry()
        if p14 < self.minP14():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p14 > self.maxP14():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p14(self):
        return self._p14.getValue()

    def minP14(self):
        return 0.0001

    def maxP14(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p13 = self._p13.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p40 = self._p40.getValue()
        p41 = self._p41.getValue()
        p42 = self._p42.getValue() / (180.0 / math.pi)
        p60 = self._p60.getValue()

        leftInsideY = (p2 - p13) * 0.5

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)

        insideLinePnt0 = Geom.Pnt2d(leftInsideY, 0.0)
        insideLinePnt1 = Geom.Pnt2d(leftInsideY, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)

        insidePnt = Line2D.intersect(mainLine, insideLine)

        maxValue = insidePnt.y() + (p18 * (1.0 - p60) + p13 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60) - (p24 - p3 + p23 + p41 + (p40 / math.cos(p42)))

        return maxValue - epsilon

    def setP15(self, p15):
        with EditMode(self.getDocument()):
            self._p15.setValue(clamp(p15, self.minP15(), self.maxP15()))
            self._updateGeometry()
        if p15 < self.minP15():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p15 > self.maxP15():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p15(self):
        return self._p15.getValue()

    def minP15(self):
        return 0.1

    def maxP15(self):
        return 10000.0

    def setP16(self, p16):
        with EditMode(self.getDocument()):
            self._p16.setValue(clamp(p16, self.minP16(), self.maxP16()))
            self._updateGeometry()
        if p16 < self.minP16():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p16 > self.maxP16():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p16(self):
        return self._p16.getValue()

    def minP16(self):
        return self._p18.getValue() + epsilon

    def maxP16(self):
        return 10000.0

    def setP17(self, p17):
        with EditMode(self.getDocument()):
            self._p17.setValue(clamp(p17, self.minP17(), self.maxP17()))
            self._updateGeometry()
        if p17 < self.minP17():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p17 > self.maxP17():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p17(self):
        return self._p17.getValue()

    def minP17(self):
        return 0.0001

    def maxP17(self):
        return self._p15.getValue() - epsilon

    def setP18(self, p18):
        with EditMode(self.getDocument()):
            self._p18.setValue(clamp(p18, self.minP18(), self.maxP18()))
            self._updateGeometry()
        if p18 < self.minP18():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p18 > self.maxP18():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p18(self):
        return self._p18.getValue()

    def maxP18(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p13 = self._p13.getValue()
        return ((p13 * 0.5) * math.sin(p1)) / math.cos(p1) - epsilon

    def minP18(self):
        return 0.001

    def setP19(self, p19):
        with EditMode(self.getDocument()):
            self._p19.setValue(clamp(p19, self.minP19(), self.maxP19()))
            self._updateGeometry()
        if p19 < self.minP19():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p19 > self.maxP19():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p19(self):
        return self._p19.getValue()

    def maxP19(self):
        return self._p26.getValue()

    def minP19(self):
        return self._p21.getValue() * 2.0 + epsilon

    def setP20(self, p20):
        with EditMode(self.getDocument()):
            self._p20.setValue(clamp(p20, self.minP20(), self.maxP20()))
            self._updateGeometry()
        if p20 < self.minP20():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p20 > self.maxP20():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p20(self):
        return self._p18.getValue()

    def maxP20(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p25 = self._p25.getValue()
        p60 = float(self._p60.getValue())

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)
        insideY = (p2 - p25) * 0.5
        topMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ), Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ))
        insideLine = Line2D.from2Points(Geom.Pnt2d(insideY, 0.0), Geom.Pnt2d(insideY, 1.0))
        topCollarTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p24 + p23 - p3), Geom.Pnt2d(1.0, p24 + p23 - p3))
        insideTopPnt = Line2D.intersect(insideLine, topMainLine)
        topLeftPntCollarTie = Line2D.intersect(topCollarTieLine, topMainLine)

        h = insideTopPnt.y() - topLeftPntCollarTie.y()

        return math.cos(p1) * h - epsilon
    def minP20(self):
        return 0.001

    def setP21(self, p21):
        with EditMode(self.getDocument()):
            self._p21.setValue(clamp(p21, self.minP21(), self.maxP21()))
            self._updateGeometry()
        if p21 < self.minP21():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p21 > self.maxP21():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p21(self):
        return self._p18.getValue()

    def maxP21(self):
        return self._p19.getValue() * 0.5 + epsilon

    def minP21(self):
        return 0.001

    def setP22(self, p22):
        with EditMode(self.getDocument()):
            self._p22.setValue(clamp(p22, self.minP22(), self.maxP22()))
            self._updateGeometry()
        if p22 < self.minP22():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p22 > self.maxP22():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p22(self):
        return self._p18.getValue()

    def maxP22(self):
        return 10000.0

    def minP22(self):
        return (self._p26.getValue() - self._p19.getValue()) * 0.5 + self._p21.getValue()

    def setP23(self, p23):
        with EditMode(self.getDocument()):
            self._p23.setValue(clamp(p23, self.minP23(), self.maxP23()))
            self._updateGeometry()
        if p23 < self.minP23():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p23 > self.maxP23():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p23(self):
        return self._p18.getValue()

    def maxP23(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p20 = self._p20.getValue()
        p24 = self._p24.getValue()
        p25 = self._p25.getValue()
        p60 = float(self._p60.getValue())

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)
        insideY = (p2 - p25) * 0.5
        bottomMainLine = Line2D.from2Points(
            Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))),
            Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))

        insideLine = Line2D.from2Points(Geom.Pnt2d(insideY, 0.0), Geom.Pnt2d(insideY, 1.0))
        bottomCollarTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p24 - p3), Geom.Pnt2d(1.0, p24 - p3))
        insideBottomPnt = Line2D.intersect(insideLine, bottomMainLine)
        bottomRightPntCollarTie = Line2D.intersect(bottomCollarTieLine, bottomMainLine)

        return insideBottomPnt.y() - bottomRightPntCollarTie.y() - epsilon

    def minP23(self):
        return 0.001

    def setP24(self, p24):
        with EditMode(self.getDocument()):
            self._p24.setValue(clamp(p24, self.minP24(), self.maxP24()))
            self._updateGeometry()
        if p24 < self.minP24():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p24 > self.maxP24():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p24(self):
        return self._p18.getValue()

    def maxP24(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p20 = self._p20.getValue()
        p23 = self._p23.getValue()
        p25 = self._p25.getValue()
        p60 = float(self._p60.getValue())

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)
        insideY = (p2 - p25) * 0.5

        bottomMainLine = Line2D.from2Points(
            Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))),
            Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))

        insideLine = Line2D.from2Points(Geom.Pnt2d(insideY, 0.0), Geom.Pnt2d(insideY, 1.0))

        insideBottomPnt = Line2D.intersect(insideLine, bottomMainLine)
        return insideBottomPnt.y() + p3 - epsilon - p23

    def minP24(self):
        return self._p3.getValue() + epsilon

    def setP25(self, p25):
        with EditMode(self.getDocument()):
            self._p25.setValue(clamp(p25, self.minP25(), self.maxP25()))
            self._updateGeometry()
        if p25 < self.minP25():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p25 > self.maxP25():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p25(self):
        return self._p18.getValue()

    def maxP25(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p20 = self._p20.getValue()
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p60 = float(self._p60.getValue())

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)
        bottomMainLine = Line2D.from2Points(
            Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))),
            Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))
        topCollarTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p24 + p23 - p3), Geom.Pnt2d(1.0, p24 + p23 - p3))
        topRightPntCollarTie = Line2D.intersect(topCollarTieLine, bottomMainLine)
        return ((p2 * 0.5) - topRightPntCollarTie.x()) * 2.0 - epsilon

    def minP25(self):
        return 0.001

    def setP26(self, p26):
        with EditMode(self.getDocument()):
            self._p26.setValue(clamp(p26, self.minP26(), self.maxP26()))
            self._updateGeometry()
        if p26 < self.minP26():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p26 > self.maxP26():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p26(self):
        return self._p26.getValue()

    def maxP26(self):
        return 10000.0

    def minP26(self):
        return self._p19.getValue()

    def setP27(self, p27):
        with EditMode(self.getDocument()):
            self._p27.setValue(clamp(p27, self.minP27(), self.maxP27()))
            self._updateGeometry()
        if p27 < self.minP27():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p27 > self.maxP27():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p27(self):
        return self._p27.getValue()

    def maxP27(self):
        return 10000.0

    def minP27(self):
        return self._p43.getValue() + epsilon

    def setP28(self, p28):
        with EditMode(self.getDocument()):
            self._p28.setValue(clamp(p28, self.minP28(), self.maxP28()))
            self._updateGeometry()
        if p28 < self.minP28():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p28 > self.maxP28():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p28(self):
        return self._p28.getValue()

    def maxP28(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p5 = self._p5.getValue()
        p6 = self._p6.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p20 = self._p20.getValue()
        p29 = self._p29.getValue()
        p60 = float(self._p60.getValue())

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)
        outsideY = p5 - p6
        bottomMainLine = Line2D.from2Points(
            Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))),
            Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))

        outsideLine = Line2D.from2Points(Geom.Pnt2d(outsideY, 0.0), Geom.Pnt2d(outsideY, 1.0))
        outBottomPnt = Line2D.intersect(outsideLine, bottomMainLine)
        return -outBottomPnt.y() + p29

    def minP28(self):
        return 0.001

    def setP29(self, p29):
        with EditMode(self.getDocument()):
            self._p29.setValue(clamp(p29, self.minP29(), self.maxP29()))
            self._updateGeometry()
        if p29 < self.minP29():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p29 > self.maxP29():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p29(self):
        return self._p29.getValue()

    def maxP29(self):
        return self._p28.getValue()

    def minP29(self):
        return 0.0

    def setP30(self, p30):
        with EditMode(self.getDocument()):
            self._p30.setValue(clamp(p30, self.minP30(), self.maxP30()))
            self._updateGeometry()
        if p30 < self.minP30():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p30 > self.maxP30():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p30(self):
        return self._p30.getValue()

    def maxP30(self):
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p5 = self._p5.getValue()
        p29 = self._p29.getValue()
        p32 = self._p32.getValue()
        p33 = self._p33.getValue()
        p34 = self._p34.getValue() / (180.0 / math.pi)
        p35 = self._p35.getValue()
        maxVal = ((p2 * 0.5) - (p32 / math.sin(p34)) - p5 - (((p3 + p29 - p35) * math.cos(p34)) / math.sin(p34)) - p33) * math.sin(p34)
        return maxVal - epsilon

    def minP30(self):
        return 0.001

    def setP31(self, p31):
        with EditMode(self.getDocument()):
            self._p31.setValue(clamp(p31, self.minP31(), self.maxP31()))
            self._updateGeometry()
        if p31 < self.minP31():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p31 > self.maxP31():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p31(self):
        return self._p31.getValue()

    def maxP31(self):
        return self._p19.getValue() - (self._p21.getValue() * 2.0)

    def minP31(self):
        return 0.0

    def setP32(self, p32):
        with EditMode(self.getDocument()):
            self._p32.setValue(clamp(p32, self.minP32(), self.maxP32()))
            self._updateGeometry()
        if p32 < self.minP32():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p32 > self.maxP32():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p32(self):
        return self._p32.getValue()

    def maxP32(self):
        return 10000.0

    def minP32(self):
        return 0.001

    def setP33(self, p33):
        with EditMode(self.getDocument()):
            self._p33.setValue(clamp(p33, self.minP33(), self.maxP33()))
            self._updateGeometry()
        if p33 < self.minP33():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p33 > self.maxP33():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p33(self):
        return self._p18.getValue()

    def maxP33(self):
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p5 = self._p5.getValue()
        p29 = self._p29.getValue()
        p30 = self._p30.getValue()
        p32 = self._p32.getValue()
        p34 = self._p34.getValue() / (180.0 / math.pi)
        p35 = self._p35.getValue()
        maxVal = (p2 * 0.5) - (p32 / math.sin(p34)) - (p30 / math.sin(p34)) - p5 - (((p3 + p29 - p35) * math.cos(p34)) / math.sin(p34))
        return maxVal

    def minP33(self):
        return 0.001

    def setP34(self, p34):
        with EditMode(self.getDocument()):
            self._p34.setValue(clamp(p34, self.minP34(), self.maxP34()))
            self._updateGeometry()
        if p34 < self.minP34():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p34 > self.maxP34():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p34(self):
        return self._p34.getValue()

    def maxP34(self):
        return 89.0

    def minP34(self):
        return 30.0

    def setP35(self, p35):
        with EditMode(self.getDocument()):
            self._p35.setValue(clamp(p35, self.minP35(), self.maxP35()))
            self._updateGeometry()
        if p35 < self.minP35():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p35 > self.maxP35():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p35(self):
        return self._p35.getValue()

    def maxP35(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p3 = self._p3.getValue()
        p5 = self._p5.getValue()
        p6 = self._p6.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p20 = self._p20.getValue()
        p60 = float(self._p60.getValue())

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)
        outsideY = p5 - p6
        bottomMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))), Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))

        outsideLine = Line2D.from2Points(Geom.Pnt2d(outsideY, 0.0), Geom.Pnt2d(outsideY, 1.0))
        outBottomPnt = Line2D.intersect(outsideLine, bottomMainLine)
        return p3 + outBottomPnt.y()

    def minP35(self):
        return 0.001

    def setP36(self, p36):
        with EditMode(self.getDocument()):
            self._p36.setValue(clamp(p36, self.minP36(), self.maxP36()))
            self._updateGeometry()
        if p36 < self.minP36():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p36 > self.maxP36():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p36(self):
        return self._p18.getValue()

    def maxP36(self):
        return 10000.0

    def minP36(self):
        return self._p31.getValue()

    def setP37(self, p37):
        with EditMode(self.getDocument()):
            self._p37.setValue(clamp(p37, self.minP37(), self.maxP37()))
            self._updateGeometry()
        if p37 < self.minP37():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p37 > self.maxP37():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p37(self):
        return self._p37.getValue()

    def maxP37(self):
        return self._p19.getValue()

    def minP37(self):
        return 0.001

    #def setP38(self, p38):
    #    with EditMode(self.getDocument()):
    #        self._p38.setValue(clamp(p38, self.minP38(), self.maxP38()))
    #        self._updateGeometry()
    #    if p38 < self.minP38():
    #        Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
    #    elif p38 > self.maxP38():
    #        Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    #def p38(self):
    #    return self._p38.getValue()

    #def maxP38(self):
    #    return 10000.0

    #def minP38(self):
    #    return 0.001

    def setP39(self, p39):
        with EditMode(self.getDocument()):
            self._p39.setValue(clamp(p39, self.minP39(), self.maxP39()))
            self._updateGeometry()
        if p39 < self.minP39():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p39 > self.maxP39():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p39(self):
        return self._p39.getValue()

    def maxP39(self):
        return self._p13.getValue()

    def minP39(self):
        return 0.001

    def setP40(self, p40):
        with EditMode(self.getDocument()):
            self._p40.setValue(clamp(p40, self.minP40(), self.maxP40()))
            self._updateGeometry()
        if p40 < self.minP40():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p40 > self.maxP40():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p40(self):
        return self._p40.getValue()

    def maxP40(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p13 = self._p13.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p41 = self._p41.getValue()
        p42 = self._p42.getValue() / (180.0 / math.pi)
        p60 = self._p60.getValue()

        leftInsideY = (p2 - p13) * 0.5

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)

        insideLinePnt0 = Geom.Pnt2d(leftInsideY, 0.0)
        insideLinePnt1 = Geom.Pnt2d(leftInsideY, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)

        insidePnt = Line2D.intersect(mainLine, insideLine)

        plaseForPurlinZ = insidePnt.y() - p14 + (p18 * (1.0 - p60) + p13 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60)

        h = plaseForPurlinZ - (p24 - p3 + p23 + p41)
        return h * math.cos(p42) - epsilon

    def minP40(self):
        return 0.001

    def setP41(self, p41):
        with EditMode(self.getDocument()):
            self._p41.setValue(clamp(p41, self.minP41(), self.maxP41()))
            self._updateGeometry()
        if p41 < self.minP41():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p41 > self.maxP41():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p41(self):
        return self._p37.getValue()

    def maxP41(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p13 = self._p13.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p40 = self._p40.getValue()
        p41 = self._p41.getValue()
        p42 = self._p42.getValue() / (180.0 / math.pi)
        p60 = self._p60.getValue()

        leftInsideY = (p2 - p13) * 0.5

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)

        insideLinePnt0 = Geom.Pnt2d(leftInsideY, 0.0)
        insideLinePnt1 = Geom.Pnt2d(leftInsideY, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)

        insidePnt = Line2D.intersect(mainLine, insideLine)

        plaseForPurlinZ = insidePnt.y() - p14 + (p18 * (1.0 - p60) + p13 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60)
        return plaseForPurlinZ - p24 + p3 - p23 - (p40 / math.cos(p42)) - epsilon

    def minP41(self):
        return 0.0

    def setP42(self, p42):
        with EditMode(self.getDocument()):
            self._p42.setValue(clamp(p42, self.minP42(), self.maxP42()))
            self._updateGeometry()
        if p42 < self.minP42():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p42 > self.maxP42():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p42(self):
        return self._p42.getValue()

    def maxP42(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p13 = self._p13.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p40 = self._p40.getValue()
        p41 = self._p41.getValue()
        p60 = self._p60.getValue()

        leftInsideY = (p2 - p13) * 0.5

        linePnt0 = Geom.Pnt2d(-p17, p16 - p18)
        linePnt1 = Geom.Pnt2d(-p17 + math.cos(p1), p16 - p18 + math.sin(p1))
        mainLine = Line2D.from2Points(linePnt0, linePnt1)

        insideLinePnt0 = Geom.Pnt2d(leftInsideY, 0.0)
        insideLinePnt1 = Geom.Pnt2d(leftInsideY, 1.0)
        insideLine = Line2D.from2Points(insideLinePnt0, insideLinePnt1)

        insidePnt = Line2D.intersect(mainLine, insideLine)

        plaseForPurlinZ = insidePnt.y() - p14 + (p18 * (1.0 - p60) + p13 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60)
        return math.acos(p40 / (plaseForPurlinZ - p24 + p3 - p23 - p41)) * (180.0 / math.pi) - epsilon

    def minP42(self):
        return 5.0

    def setP43(self, p43):
        with EditMode(self.getDocument()):
            self._p43.setValue(clamp(p43, self.minP43(), self.maxP43()))
            self._updateGeometry()
        if p43 < self.minP43():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p43 > self.maxP43():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p43(self):
        return self._p43.getValue()

    def maxP43(self):
        return self._p31.getValue() * 0.5 - epsilon

    def minP43(self):
        return 0.0

    def setP44(self, p44):
        with EditMode(self.getDocument()):
            self._p44.setValue(clamp(p44, self.minP44(), self.maxP44()))
            self._updateGeometry()
        if p44 < self.minP44():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p44 > self.maxP44():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p44(self):
        return self._p44.getValue()

    def maxP44(self):
        return self._p8.getValue()

    def minP44(self):
        return 0.001

    def setP45(self, p45):
        with EditMode(self.getDocument()):
            self._p45.setValue(clamp(p45, self.minP45(), self.maxP45()))
            self._updateGeometry()
        if p45 < self.minP45():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p45 > self.maxP45():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p45(self):
        return self._p45.getValue()

    def maxP45(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p20 = self._p20.getValue()
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p25 = self._p25.getValue()
        p46 = self._p46.getValue()
        p47 = self._p47.getValue() / (180.0 / math.pi)
        p60 = float(self._p60.getValue())

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)
        insideY = (p2 - p25) * 0.5

        bottomMainLine = Line2D.from2Points(
            Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))),
            Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))

        insideLine = Line2D.from2Points(Geom.Pnt2d(insideY, 0.0), Geom.Pnt2d(insideY, 1.0))

        insideBottomPnt = Line2D.intersect(insideLine, bottomMainLine)

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)

        topMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ),
                                         Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ))

        topCollarTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p24 + p23 - p3), Geom.Pnt2d(1.0, p24 + p23 - p3))
        topLeftPntCollarTie = Line2D.intersect(topCollarTieLine, topMainLine)
        return math.cos(p47) * (insideBottomPnt.y() - topLeftPntCollarTie.y() - p46) - epsilon

    def minP45(self):
        return 0.001

    def setP46(self, p46):
        with EditMode(self.getDocument()):
            self._p46.setValue(clamp(p46, self.minP46(), self.maxP46()))
            self._updateGeometry()
        if p46 < self.minP46():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p46 > self.maxP46():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p46(self):
        return self._p46.getValue()

    def maxP46(self):
        p1 = self._p1.getValue() / (180.0 / math.pi)
        p2 = self._p2.getValue()
        p3 = self._p3.getValue()

        p10 = self._p10.getValue()
        p11 = self._p11.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        p60 = float(self._p60.getValue())
        p18 = self._p18.getValue() * (1.0 - p60) + p15 * 0.5 * (math.sin(p1) / math.cos(p1)) * p60
        p20 = self._p20.getValue()
        p23 = self._p23.getValue()
        p24 = self._p24.getValue()
        p25 = self._p25.getValue()
        p45 = self._p45.getValue()
        p47 = self._p47.getValue() / (180.0 / math.pi)
        p60 = float(self._p60.getValue())

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)
        insideY = (p2 - p25) * 0.5

        bottomMainLine = Line2D.from2Points(
            Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ - (p20 / math.cos(p1))),
            Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ - (p20 / math.cos(p1))))

        insideLine = Line2D.from2Points(Geom.Pnt2d(insideY, 0.0), Geom.Pnt2d(insideY, 1.0))

        insideBottomPnt = Line2D.intersect(insideLine, bottomMainLine)

        cathetus = (p18 / 2.0 * (1.0 - p60) + p10 / 4.0 * (math.sin(p1) / math.cos(p1)) * p60) * 2.0
        gipot = p10 - ((cathetus * math.cos(p1)) / math.sin(p1))
        valueZ = (gipot * math.sin(p1)) / math.cos(p1)

        topMainLine = Line2D.from2Points(Geom.Pnt2d(((math.cos(p1) * p18) / math.sin(p1)) - p17, p16 - p11 - valueZ),
                                         Geom.Pnt2d(-p17, p16 - p18 - p11 - valueZ))

        topCollarTieLine = Line2D.from2Points(Geom.Pnt2d(0.0, p24 + p23 - p3), Geom.Pnt2d(1.0, p24 + p23 - p3))
        topLeftPntCollarTie = Line2D.intersect(topCollarTieLine, topMainLine)

        return insideBottomPnt.y() - topLeftPntCollarTie.y() - (p45 / math.cos(p47))

    def minP46(self):
        return 0.0

    def setP47(self, p47):
        with EditMode(self.getDocument()):
            self._p47.setValue(clamp(p47, self.minP47(), self.maxP47()))
            self._updateGeometry()
        if p47 < self.minP47():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p47 > self.maxP47():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p47(self):
        return self._p47.getValue()

    def maxP47(self):
        return 75.0

    def minP47(self):
        return 1.0

    def setP48(self, p48):
        with EditMode(self.getDocument()):
            self._p48.setValue(p48)
            self._updateGeometry()

    def p48(self):
        return self._p48.getValue()

    def setP60(self, p60):
        with EditMode(self.getDocument()):
            self._p60.setValue(p60)
            self._updateGeometry()

    def p60(self):
        return self._p60.getValue()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == RoofCreator._p1ParamName:
            self.setP1(self._p1.getValue())
        elif aPropertyName == RoofCreator._p2ParamName:
            self.setP2(self._p2.getValue())
        elif aPropertyName == RoofCreator._p3ParamName:
            self.setP3(self._p3.getValue())
        elif aPropertyName == RoofCreator._p4ParamName:
            self.setP4(self._p4.getValue())
        elif aPropertyName == RoofCreator._p5ParamName:
            self.setP5(self._p5.getValue())
        elif aPropertyName == RoofCreator._p6ParamName:
            self.setP6(self._p6.getValue())
        elif aPropertyName == RoofCreator._p7ParamName:
            self.setP7(self._p7.getValue())
        elif aPropertyName == RoofCreator._p8ParamName:
            self.setP8(self._p8.getValue())
        elif aPropertyName == RoofCreator._p9ParamName:
            self.setP9(self._p9.getValue())
        elif aPropertyName == RoofCreator._p10ParamName:
            self.setP10(self._p10.getValue())
        elif aPropertyName == RoofCreator._p10ParamName:
            self.setP10(self._p10.getValue())
        elif aPropertyName == RoofCreator._p11ParamName:
            self.setP11(self._p11.getValue())
        elif aPropertyName == RoofCreator._p12ParamName:
            self.setP12(self._p12.getValue())
        elif aPropertyName == RoofCreator._p13ParamName:
            self.setP13(self._p13.getValue())
        elif aPropertyName == RoofCreator._p14ParamName:
            self.setP14(self._p14.getValue())
        elif aPropertyName == RoofCreator._p15ParamName:
            self.setP15(self._p15.getValue())
        elif aPropertyName == RoofCreator._p16ParamName:
            self.setP16(self._p16.getValue())
        elif aPropertyName == RoofCreator._p17ParamName:
            self.setP17(self._p17.getValue())
        elif aPropertyName == RoofCreator._p18ParamName:
            self.setP18(self._p18.getValue())
        elif aPropertyName == RoofCreator._p19ParamName:
            self.setP19(self._p19.getValue())
        elif aPropertyName == RoofCreator._p20ParamName:
            self.setP20(self._p20.getValue())
        elif aPropertyName == RoofCreator._p21ParamName:
            self.setP21(self._p21.getValue())
        elif aPropertyName == RoofCreator._p22ParamName:
            self.setP22(self._p22.getValue())
        elif aPropertyName == RoofCreator._p23ParamName:
            self.setP23(self._p23.getValue())
        elif aPropertyName == RoofCreator._p24ParamName:
            self.setP24(self._p24.getValue())
        elif aPropertyName == RoofCreator._p25ParamName:
            self.setP25(self._p25.getValue())
        elif aPropertyName == RoofCreator._p26ParamName:
            self.setP26(self._p26.getValue())
        elif aPropertyName == RoofCreator._p27ParamName:
            self.setP27(self._p27.getValue())
        elif aPropertyName == RoofCreator._p28ParamName:
            self.setP28(self._p28.getValue())
        elif aPropertyName == RoofCreator._p29ParamName:
            self.setP29(self._p29.getValue())
        elif aPropertyName == RoofCreator._p30ParamName:
            self.setP30(self._p30.getValue())
        elif aPropertyName == RoofCreator._p31ParamName:
            self.setP31(self._p31.getValue())
        elif aPropertyName == RoofCreator._p32ParamName:
            self.setP32(self._p32.getValue())
        elif aPropertyName == RoofCreator._p33ParamName:
            self.setP33(self._p33.getValue())
        elif aPropertyName == RoofCreator._p34ParamName:
            self.setP34(self._p34.getValue())
        elif aPropertyName == RoofCreator._p35ParamName:
            self.setP35(self._p35.getValue())
        elif aPropertyName == RoofCreator._p36ParamName:
            self.setP36(self._p36.getValue())
        elif aPropertyName == RoofCreator._p37ParamName:
            self.setP37(self._p37.getValue())
        #elif aPropertyName == RoofCreator._p38ParamName:
        #    self.setP38(self._p38.getValue())
        elif aPropertyName == RoofCreator._p39ParamName:
            self.setP39(self._p39.getValue())
        elif aPropertyName == RoofCreator._p40ParamName:
            self.setP40(self._p40.getValue())
        elif aPropertyName == RoofCreator._p41ParamName:
            self.setP41(self._p41.getValue())
        elif aPropertyName == RoofCreator._p42ParamName:
            self.setP42(self._p42.getValue())
        elif aPropertyName == RoofCreator._p43ParamName:
            self.setP43(self._p43.getValue())
        elif aPropertyName == RoofCreator._p44ParamName:
            self.setP44(self._p44.getValue())
        elif aPropertyName == RoofCreator._p45ParamName:
            self.setP45(self._p45.getValue())
        elif aPropertyName == RoofCreator._p46ParamName:
            self.setP46(self._p46.getValue())
        elif aPropertyName == RoofCreator._p47ParamName:
            self.setP47(self._p47.getValue())
        elif aPropertyName == RoofCreator._p48ParamName:
            self.setP48(self._p48.getValue())
        elif aPropertyName == RoofCreator._p60ParamName:
            self.setP60(self._p60.getValue())

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(doc):
            if not Geom.GeomTools.isEqual(x, 1.):
                old = self.width.getValue()
                self.width.setValue(old * x)
                self.modifyElem()
            if not Geom.GeomTools.isEqual(y, 1.):
                old = self.width.getValue()
                self.width.setValue(old * y)
                self.modifyElem()
            if not Geom.GeomTools.isEqual(z, 1.):
                old = self.height.getValue()
                self.height.setValue(old * z)
                self.modifyElem()

            self.translateAfterScaled(aVec, aScaleBasePnt)
    
if __name__ == "__main__":   
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{60A0EC36-4E7C-4BBE-B177-9365A068FAB4}"))

    comp = RoofCreator(doc)

    with EditMode(doc):
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
        else:
            pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

        comp.setLocalPlacement(pos)