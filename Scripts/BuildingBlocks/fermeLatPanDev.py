 # coding=utf-8
# OpenLexocad libraries
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

class FermeLatPanDev(lx.Element):

    _p1ParamName = "Portée ferme"
    _p2ParamName = "Pente couverture"
    _p3ParamName = "Hauteur arbalètrier"
    _p4ParamName = "Epaisseur arbalètrier"
    _p5ParamName = "Embrèvement arbalètrier / poinçon"
    _p6ParamName = "Hauteur entrait"
    _p7ParamName = "Epaisseur entraits"
    _p8ParamName = "Section au carré du poinçon"
    _p9ParamName = "Hauteur contrefiche"
    _p10ParamName = "Epaisseur contrefiche"
    _p11ParamName = "Angle contrefiche / entrait"
    _p12ParamName = "Retrait contrefiche / entrait"
    _p13ParamName = "Hauteur panne"
    _p14ParamName = "Hauteur faîtière"
    _p15ParamName = "Epaisseur faîtière"
    _p16ParamName = "Hauteur ext. sablière"
    _p17ParamName = "Retrait entraits dans arbalétier"
    _p166ParamName = "Epaulement"
    _p168ParamName = "Hauteur lien"
    _p174ParamName = "Largeur lien"

    def getGlobalClassId(self):
        return Base.GlobalId("{37A49AA5-2E94-46F9-9EBD-53B92D9F1024}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("FermeLatPanDev", "OpenLxApp.Element")
        # Register properties 
        self.setPropertyHeader(lxstr("Ferme Lat Pan Dev"), -1)
        self.setPropertyGroupName(lxstr("Roof Parameter"), -1)

        self._p1 = self.registerPropertyDouble(self._p1ParamName, 8.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p2 = self.registerPropertyDouble(self._p2ParamName, 35.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p3 = self.registerPropertyDouble(self._p3ParamName, 0.250, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p4 = self.registerPropertyDouble(self._p4ParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p5 = self.registerPropertyDouble(self._p5ParamName, 0.03, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p6 = self.registerPropertyDouble(self._p6ParamName, 0.225, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p7 = self.registerPropertyDouble(self._p7ParamName, 0.075, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p8 = self.registerPropertyDouble(self._p8ParamName, 0.180, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p9 = self.registerPropertyDouble(self._p9ParamName, 0.175, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p10 = self.registerPropertyDouble(self._p10ParamName, 0.075, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p11 = self.registerPropertyDouble(self._p11ParamName, 45.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p12 = self.registerPropertyDouble(self._p12ParamName, 0.05, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p13 = self.registerPropertyDouble(self._p13ParamName, 0.225, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p14 = self.registerPropertyDouble(self._p14ParamName, 0.215, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p15 = self.registerPropertyDouble(self._p15ParamName, 0.075, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p16 = self.registerPropertyDouble(self._p16ParamName, 0.06, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p17 = self.registerPropertyDouble(self._p17ParamName, 0.01, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p166 = self.registerPropertyDouble(self._p166ParamName, 1.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p168 = self.registerPropertyDouble(self._p168ParamName, 0.175, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._p174 = self.registerPropertyDouble(self._p174ParamName, 0.063, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        
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

    def _entraitsBuild(self):
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p4 = self._p4.getValue()
        p6 = self._p6.getValue()
        p7 = self._p7.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()

        listFirstEntraitPoints = []
        listSecondEntraitPoints = []

        _retreat = ((math.cos(p2)) * (p6 - p16)) / math.sin(p2)

        first = float((p4 * 0.5) - p17 + p7)
        second = float(p17 - (p4 * 0.5))

        listFirstEntraitPoints.append(Geom.Pnt(first, 0.0, 0.0))
        listFirstEntraitPoints.append(Geom.Pnt(first, p1, 0.0))
        listFirstEntraitPoints.append(Geom.Pnt(first, p1, p16))
        listFirstEntraitPoints.append(Geom.Pnt(first, p1 - _retreat, p6))
        listFirstEntraitPoints.append(Geom.Pnt(first, _retreat, p6))
        listFirstEntraitPoints.append(Geom.Pnt(first, 0.0, p16))

        listSecondEntraitPoints.append(Geom.Pnt(second, 0.0, 0.0))
        listSecondEntraitPoints.append(Geom.Pnt(second, p1, 0.0))
        listSecondEntraitPoints.append(Geom.Pnt(second, p1, p16))
        listSecondEntraitPoints.append(Geom.Pnt(second, p1 - _retreat, p6))
        listSecondEntraitPoints.append(Geom.Pnt(second, _retreat, p6))
        listSecondEntraitPoints.append(Geom.Pnt(second, 0.0, p16))

        firstEntraits = self._createSubElement(listFirstEntraitPoints, p7, Geom.Dir(-1.0, 0.0, 0.0))
        secondEntrait = self._createSubElement(listSecondEntraitPoints, p7, Geom.Dir(-1.0, 0.0, 0.0))

        self.addSubElement(firstEntraits)
        self.addSubElement(secondEntrait)

    def _arbaletrierBuild(self):
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p3 = self._p3.getValue()
        p4 = self._p4.getValue()
        p5 = self._p5.getValue()
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p13 = self._p13.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()

        defAngle = 62.5 / (180.0 / math.pi)

        insXdim = (p4 * 0.5) - p17
        outXdim = p4 * 0.5

        clearanceY = (p1 - p8) * 0.5
        clearanceX = (p13 / math.sin(p2)) - ((p16 * math.cos(p2)) / math.sin(p2))
        coef = (p6 * (math.cos(p2))) / math.sin(p2)

        pnt0 = Geom.Pnt(insXdim, clearanceX, 0.0)
        pnt1 = Geom.Pnt(insXdim, clearanceX + (p3 / math.sin(p2)), 0.0)
        pnt2 = Geom.Pnt(insXdim, clearanceX + (p3 / math.sin(p2)) + coef, p6)
        pnt3 = Geom.Pnt(outXdim, clearanceX + (p3 / math.sin(p2)) + coef, p6)
        pnt4 = Geom.Pnt(outXdim, clearanceY, ((clearanceY - clearanceX - (p3 / math.sin(p2))) * math.sin(p2)) / (math.cos(p2)))
        pnt5 = Geom.Pnt(outXdim, clearanceY + p5, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)) - ((p5 * math.cos(defAngle)) / math.sin(defAngle)))
        pnt6 = Geom.Pnt(outXdim, clearanceY, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)))
        pnt7 = Geom.Pnt(outXdim, (clearanceX) + coef, p6)
        pnt8 = Geom.Pnt(insXdim, (clearanceX) + coef, p6)

        pnt9 = Geom.Pnt(-insXdim, clearanceX, 0.0)
        pnt10 = Geom.Pnt(-insXdim, clearanceX + (p3 / math.sin(p2)), 0.0)
        pnt11 = Geom.Pnt(-insXdim, clearanceX + (p3 / math.sin(p2)) + coef, p6)
        pnt12 = Geom.Pnt(-outXdim, clearanceX + (p3 / math.sin(p2)) + coef, p6)
        pnt13 = Geom.Pnt(-outXdim, clearanceY, ((clearanceY - clearanceX - (p3 / math.sin(p2))) * math.sin(p2)) / (math.cos(p2)))
        pnt14 = Geom.Pnt(-outXdim, clearanceY + p5, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)) - ((p5 * math.cos(defAngle)) / math.sin(defAngle)))
        pnt15 = Geom.Pnt(-outXdim, clearanceY, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)))
        pnt16 = Geom.Pnt(-outXdim, clearanceX + coef, p6)
        pnt17 = Geom.Pnt(-insXdim, clearanceX + coef, p6)

        mdl = FacetedModelAssembler(doc)
        mdl.beginModel()
        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt1, pnt2, pnt8])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt2, pnt3, pnt7, pnt8])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt7, pnt3, pnt4, pnt5, pnt6])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt6, pnt5, pnt14, pnt15])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt4, pnt13, pnt14, pnt5])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt6, pnt15, pnt16, pnt17, pnt9, pnt0, pnt8, pnt7])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt16, pnt15, pnt14, pnt13, pnt12])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt16, pnt12, pnt11, pnt17])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt9, pnt17, pnt11, pnt10])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt9, pnt10, pnt1])
        mdl.endFace()
        mdl.beginFace()
        mdl.addVertexList([pnt1, pnt10, pnt11, pnt12, pnt13, pnt4, pnt3, pnt2])
        mdl.endFace()
        geom = mdl.endModel()

        firstSubElement = lx.SubElement.createIn(doc)
        secondSubElement = lx.SubElement.createIn(doc)
        firstSubElement.setGeometry(geom)
        secondSubElement.setGeometry(geom)
        secondSubElement.translate(Geom.Vec(0.0, -p1, 0.0), Geom.CoordSpace_WCS)
        angleAxis = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0.0, 0.0, 1.0))
        secondSubElement.rotate(angleAxis, math.pi, Geom.CoordSpace_WCS)

        self.addSubElement(firstSubElement)
        self.addSubElement(secondSubElement)

    def _centerBeamBuild(self):
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p3 = self._p3.getValue()
        p4 = self._p4.getValue()
        p5 = self._p5.getValue()
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p13 = self._p13.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p17 = self._p17.getValue()
        clearanceX = (p13 / math.sin(p2)) - ((p16 * math.cos(p2)) / math.sin(p2))
        clearanceY = (p1 - p8) * 0.5

        l = (p16 * math.cos(p2) / math.sin(p2)) + clearanceY
        defAngle = 62.5 / (180.0 / math.pi)
        outXdim = p4 * 0.5
        bottomDim = 0.3
        coefX = p8 * 0.5
        coefZ = (p5 * math.cos(defAngle)) / math.sin(defAngle)
        clearanceZ = ((l + ((p8 - p15) * 0.5)) * math.sin(p2)) / math.cos(p2)

        pnt0 = Geom.Pnt(-coefX, (p1 - p8) * 0.5,  (l * math.sin(p2)) / math.cos(p2))
        pnt1 = Geom.Pnt(coefX, (p1 - p8) * 0.5,  (l * math.sin(p2)) / math.cos(p2))
        pnt2 = Geom.Pnt(coefX, (p1 - p15) * 0.5, clearanceZ)
        pnt3 = Geom.Pnt(-coefX, (p1 - p15) * 0.5, clearanceZ)
        pnt4 = Geom.Pnt(-coefX, (p1 + p15) * 0.5, clearanceZ)
        pnt5 = Geom.Pnt(coefX, (p1 + p15) * 0.5, clearanceZ)
        pnt6 = Geom.Pnt(coefX, (p1 + p8) * 0.5,  (l * math.sin(p2)) / math.cos(p2))
        pnt7 = Geom.Pnt(-coefX, (p1 + p8) * 0.5,  (l * math.sin(p2)) / math.cos(p2))

        pnt8 = Geom.Pnt(-coefX, (p1 - p15) * 0.5, clearanceZ - p14)
        pnt9 = Geom.Pnt(-coefX, (p1 + p15) * 0.5, clearanceZ - p14)
        pnt10 = Geom.Pnt(coefX, (p1 + p15) * 0.5, clearanceZ - p14)
        pnt11 = Geom.Pnt(coefX, (p1 - p15) * 0.5, clearanceZ - p14)

        pnt12 = Geom.Pnt(-outXdim, clearanceY, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)))
        pnt13 = Geom.Pnt(-outXdim, clearanceY + p5, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)) - coefZ)
        pnt14 = Geom.Pnt(outXdim, (p1 - p8) * 0.5, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)))
        pnt15 = Geom.Pnt(outXdim, clearanceY + p5, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)) - coefZ)
        pnt16 = Geom.Pnt(-outXdim, (p1 - p8) * 0.5, ((clearanceY - clearanceX - (p3 / math.sin(p2))) * math.sin(p2)) / math.cos(p2))
        pnt17 = Geom.Pnt(outXdim, (p1 - p8) * 0.5, ((clearanceY - clearanceX - (p3 / math.sin(p2))) * math.sin(p2)) / math.cos(p2))

        pnt18 = Geom.Pnt(-outXdim, (p1 + p8) * 0.5, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)))
        pnt19 = Geom.Pnt(-outXdim, (p1 * 0.5) + (p8 * 0.5) - p5, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)) - coefZ)
        pnt20 = Geom.Pnt(outXdim, (p1 + p8) * 0.5, (((p1 * 0.5) - (p8 * 0.5) - clearanceX) * math.sin(p2)) / (math.cos(p2)))
        pnt21 = Geom.Pnt(outXdim, (p1 * 0.5) + (p8 * 0.5) - p5, ((clearanceY - clearanceX) * math.sin(p2)) / (math.cos(p2)) - coefZ)
        pnt22 = Geom.Pnt(-outXdim, (p1 + p8) * 0.5, ((clearanceY - clearanceX - (p3 / math.sin(p2))) * math.sin(p2)) / (math.cos(p2)))
        pnt23 = Geom.Pnt(outXdim, (p1 + p8) * 0.5, ((clearanceY - clearanceX - (p3 / math.sin(p2))) * math.sin(p2)) / (math.cos(p2)))

        second = float(p17 - (p4 * 0.5))

        pnt24 = Geom.Pnt(-coefX, (p1 - p8) * 0.5, p6)
        pnt25 = Geom.Pnt(-coefX, (p1 + p8) * 0.5, p6)
        pnt26 = Geom.Pnt(second, (p1 + p8) * 0.5, p6)
        pnt27 = Geom.Pnt(second, (p1 - p8) * 0.5, p6)
        pnt28 = Geom.Pnt(-second, (p1 - p8) * 0.5, p6)
        pnt29 = Geom.Pnt(-second, (p1 + p8) * 0.5, p6)
        pnt30 = Geom.Pnt(coefX, (p1 + p8) * 0.5, p6)
        pnt31 = Geom.Pnt(coefX, (p1 - p8) * 0.5, p6)

        pnt32 = Geom.Pnt(-coefX, (p1 - p8) * 0.5, 0.0)
        pnt33 = Geom.Pnt(second, (p1 - p8) * 0.5, 0.0)
        pnt34 = Geom.Pnt(second, (p1 + p8) * 0.5, 0.0)
        pnt35 = Geom.Pnt(-coefX, (p1 + p8) * 0.5, 0.0)
        pnt36 = Geom.Pnt(-second, (p1 - p8) * 0.5, 0.0)
        pnt37 = Geom.Pnt(coefX, (p1 - p8) * 0.5, 0.0)
        pnt38 = Geom.Pnt(coefX, (p1 + p8) * 0.5, 0.0)
        pnt39 = Geom.Pnt(-second, (p1 + p8) * 0.5, 0.0)

        pnt40 = Geom.Pnt(coefX, (p1 - p8) * 0.5, -bottomDim + (p8 * 0.5))
        pnt41 = Geom.Pnt(coefX, (p1 + p8) * 0.5, -bottomDim + (p8 * 0.5))
        pnt42 = Geom.Pnt(-coefX, (p1 + p8) * 0.5, -bottomDim + (p8 * 0.5))
        pnt43 = Geom.Pnt(-coefX, (p1 - p8) * 0.5, -bottomDim + (p8 * 0.5))
        pnt44 = Geom.Pnt(0.0, p1 * 0.5, -bottomDim)

        mdl = FacetedModelAssembler(doc)
        mdl.beginModel()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt1, pnt2, pnt3])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt4, pnt5, pnt6, pnt7])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt2, pnt11, pnt8, pnt3])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt9, pnt10, pnt5, pnt4])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt8, pnt11, pnt10, pnt9])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt24, pnt27, pnt33, pnt32, pnt43, pnt40, pnt37, pnt36, pnt28, pnt31, pnt1])
        mdl.endLoop()
        mdl.addVertexList([pnt12, pnt14, pnt17, pnt16])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt6, pnt30, pnt29, pnt39, pnt38, pnt41, pnt42, pnt35, pnt34, pnt26, pnt25, pnt7])
        mdl.endLoop()
        mdl.addVertexList([pnt18, pnt22, pnt23, pnt20])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt3, pnt8, pnt9, pnt4, pnt7, pnt25, pnt24])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt24, pnt25, pnt26, pnt27])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt27, pnt26, pnt34, pnt33])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt32, pnt33, pnt34, pnt35])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt43, pnt32, pnt35, pnt42])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt1, pnt31, pnt30, pnt6, pnt5, pnt10, pnt11, pnt2])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt28, pnt29, pnt30, pnt31])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt28, pnt36, pnt39, pnt29])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt36, pnt37, pnt38, pnt39])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt37, pnt40, pnt41, pnt38])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt40, pnt44, pnt41])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt40, pnt43, pnt44])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt43, pnt42, pnt44])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt42, pnt41, pnt44])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt12, pnt13, pnt15, pnt14])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt12, pnt16, pnt13])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt14, pnt15, pnt17])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt16, pnt17, pnt15, pnt13])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt18, pnt20, pnt21, pnt19])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt19, pnt21, pnt23, pnt22])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt19, pnt22, pnt18])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt21, pnt20, pnt23])
        mdl.endFace()

        geom = mdl.endModel()

        subElement = lx.SubElement.createIn(doc)
        subElement.setGeometry(geom)

        self.addSubElement(subElement)

    def _strutBuild(self):
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p3 = self._p3.getValue()
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p9 = self._p9.getValue()
        p10 = self._p10.getValue()
        p11 = self._p11.getValue() / (180.0 / math.pi)
        p12 = self._p12.getValue()
        p13 = self._p13.getValue()
        p16 = self._p16.getValue()

        lenLine = 1000.0

        firstPntMainLine = Geom.Pnt2d((((p13 / math.sin(p2)) - ((p16 * math.cos(p2)) / math.sin(p2))) + ( p3 / math.sin(p2)) + ((p6 * (math.cos(p2))) / math.sin(p2))), p6)
        secondPntMainLine = Geom.Pnt2d((p1 * 0.5) - (p8 * 0.5), (((p1 * 0.5) - (p8 * 0.5) - ((p13 / math.sin(p2)) - ((p16 * math.cos(p2)) / math.sin(p2))) - (p3 / math.sin(p2))) * math.sin(p2)) / (math.cos(p2)))

        mainLine = Line2D.from2Points(firstPntMainLine, secondPntMainLine)
        lineTop = Line2D.from2Points(Geom.Pnt2d((p1 - p8) * 0.5, p6 + p12 + (p9 / math.cos(p11))), Geom.Pnt2d(((p1 - p8) * 0.5) - (lenLine * math.cos(p11)), (lenLine * math.sin(p11)) + p6 + p12 + (p9 / math.cos(p11))))
        lineBottom = Line2D.from2Points(Geom.Pnt2d((p1 - p8) * 0.5, p6 + p12), Geom.Pnt2d(((p1 - p8) * 0.5) - (lenLine * math.cos(p11)), (lenLine * math.sin(p11)) + p6 + p12))

        intPtTop = Line2D.intersect(mainLine, lineTop)
        intPtBottom = Line2D.intersect(mainLine, lineBottom)

        pnt0 = Geom.Pnt(-p10 * 0.5, (p1 - p8) * 0.5, p6 + p12 + (p9 / math.cos(p11)))
        pnt1 = Geom.Pnt(-p10 * 0.5, (p1 - p8) * 0.5, p6 + p12)
        pnt2 = Geom.Pnt(-p10 * 0.5, intPtBottom.x(), intPtBottom.y())
        pnt3 = Geom.Pnt(-p10 * 0.5, intPtTop.x(), intPtTop.y())

        pnt4 = Geom.Pnt(p10 * 0.5, (p1 - p8) * 0.5, p6 + p12 + (p9 / math.cos(p11)))
        pnt5 = Geom.Pnt(p10 * 0.5, (p1 - p8) * 0.5, p6 + p12)
        pnt6 = Geom.Pnt(p10 * 0.5, intPtBottom.x(), intPtBottom.y())
        pnt7 = Geom.Pnt(p10 * 0.5, intPtTop.x(), intPtTop.y())

        mdl = FacetedModelAssembler(doc)

        mdl.beginModel()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt1, pnt2, pnt3])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt7, pnt6, pnt5, pnt4])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt3, pnt2, pnt6, pnt7])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt4, pnt5, pnt1, pnt0])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt0, pnt3, pnt7, pnt4])
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertexList([pnt1, pnt5, pnt6, pnt2])
        mdl.endFace()

        geom = mdl.endModel()

        firstStrut = lx.SubElement.createIn(doc)
        secondStrut = lx.SubElement.createIn(doc)
        firstStrut.setGeometry(geom)
        secondStrut.setGeometry(geom)
        angleAxis = Geom.Ax1(Geom.Pnt(0.0, p1 * 0.5, 0.0), Geom.Dir(0.0, 0.0, 1.0))
        secondStrut.rotate(angleAxis, math.pi, Geom.CoordSpace_WCS)

        self.addSubElement(firstStrut)
        self.addSubElement(secondStrut)

    def _lienBeamsBuild(self):
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p8 = self._p8.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()

        p166 = self._p166.getValue()
        p168 = self._p168.getValue()
        p174 = self._p174.getValue()

        l = (p16 * math.cos(p2) / math.sin(p2)) + ((p1 - p8) * 0.5)
        defH = ((l + ((p8 - p15) * 0.5)) * math.sin(p2)) / math.cos(p2) - p14
        listLienPnt = []
        listLienPnt.append(Geom.Pnt(-p166 - (p8 * 0.5), (p1 - p174) * 0.5, defH))
        listLienPnt.append(Geom.Pnt(-(p8 * 0.5), (p1 - p174) * 0.5, defH - p166))
        listLienPnt.append(Geom.Pnt(-(p8 * 0.5), (p1 - p174) * 0.5, defH - p166 + (p168 / math.sin(math.pi * 0.25))))
        listLienPnt.append(Geom.Pnt(-p166 - (p8 * 0.5) + (p168 / math.sin(math.pi * 0.25)), (p1 - p174) * 0.5, defH))

        firstLien = self._createSubElement(listLienPnt, p174, Geom.Dir(0.0, 1.0, 0.0))
        secondLien = self._createSubElement(listLienPnt, p174, Geom.Dir(0.0, 1.0, 0.0))

        angleAxis = Geom.Ax1(Geom.Pnt(0.0, p1 * 0.5, 0.0), Geom.Dir(0.0, 0.0, 1.0))
        secondLien.rotate(angleAxis, math.pi, Geom.CoordSpace_WCS)

        self.addSubElement(firstLien)
        self.addSubElement(secondLien)

    def createCompound(self):
        self._entraitsBuild()
        self._arbaletrierBuild()
        self._centerBeamBuild()
        self._strutBuild()
        self._lienBeamsBuild()

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
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p3 = self._p3.getValue()
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p9 = self._p9.getValue()
        p11 = self._p11.getValue() / (180.0 / math.pi)
        p12 = self._p12.getValue()
        p13 = self._p13.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p166 = self._p166.getValue()

        valAngle = math.cos(p2) / math.sin(p2)
        firstMinVal = ((((p6 + p14 + p166 - p16) * valAngle) - ((p8 - p15) * 0.5)) * 2.0) + p8
        secondMinVal = ((p6 + p12 + (p9 / math.cos(p11))) * (math.cos(p2)) / math.sin(p2) + (p8 * 0.5) + ((p13 / math.sin(p2)) - ((p16 * math.cos(p2)) / math.sin(p2))) - (p3 / math.sin(p2))) * 2.0
        if firstMinVal > secondMinVal:
            return firstMinVal
        return secondMinVal

    def maxP1(self):
        return 10000.0

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
        p1 = self._p1.getValue()
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p166 = self._p166.getValue()

        n = (((p1 - p8) * 0.5) + ((p8 - p15) * 0.5)) / (p6 + p14 + p166 - p16)

        return math.atan(1.0 / n) * 180.0 / math.pi

    def maxP2(self):
        maxAngle = 89.0
        return maxAngle

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
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p9 = self._p9.getValue()
        p11 = self._p11.getValue() / (180.0 / math.pi)
        p12 = self._p12.getValue()
        p13 = self._p13.getValue()
        p16 = self._p16.getValue()
        maxValue = -((((p6 + p12 + (p9 / math.cos(p11))) * (math.cos(p2)) / math.sin(p2)) - (p1 * 0.5) + (p8 * 0.5) + ((p13 / math.sin(p2)) - ((p16 * math.cos(p2)) / math.sin(p2)))) * math.sin(p2))
        return maxValue

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
        return self._p17.getValue() * 2.0 + epsilon

    def maxP4(self):
        return self._p8.getValue() - 0.01

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
        return 0.01

    def maxP5(self):
        return self._p8.getValue() * 0.5 - epsilon

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
        return self._p16.getValue() + epsilon

    def maxP6(self):
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p8 = self._p8.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p166 = self._p166.getValue()
        valAngle = math.cos(p2) / math.sin(p2)
        maxValue = ((((p1 - p8) * 0.5) + ((p8 - p15) * 0.5)) / valAngle) - p14 - p166 + p16
        return maxValue

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
        return self._p17.getValue()

    def maxP7(self):
        p4 = self._p4.getValue()
        p8 = self._p8.getValue()
        p17 = self._p17.getValue()
        second = p17 - (p4 * 0.5)
        return (p8 * 0.5) + second

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
        p4 = self._p4.getValue()
        p5 = self._p5.getValue()
        p10 = self._p10.getValue()
        p15 = self._p15.getValue()
        variantList = [p5 * 2.0 + epsilon, p15 + epsilon, p4 + epsilon, p10 + epsilon]
        value = self.maxInList(variantList)
        return value

    def maxP8(self):
        maxWidth = 0.6
        return maxWidth - 0.01

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
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p3 = self._p3.getValue()
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p11 = self._p11.getValue() / (180.0 / math.pi)
        p12 = self._p12.getValue()
        p13 = self._p13.getValue()
        p16 = self._p16.getValue()

        maxValue = (((((p1 * 0.5) - (p8 * 0.5) - ((p13 / math.sin(p2)) - ((p16 * math.cos(p2)) / math.sin(p2))) - (p3 / math.sin(p2))) * math.sin(p2)) / (math.cos(p2))) - p6 - p12) * math.cos(p11)

        return maxValue - 0.0001

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
        return self._p8.getValue() - epsilon

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
        return 5.0

    def maxP11(self):
        return 80.0

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
        return 0.001

    def maxP12(self):
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p3 = self._p3.getValue()
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p9 = self._p9.getValue()
        p11 = self._p11.getValue() / (180.0 / math.pi)
        p13 = self._p13.getValue()
        p16 = self._p16.getValue()
        maxValue = (((-p3 / math.sin(p2)) + (p1 * 0.5) - (p8 * 0.5) - ((p13 / math.sin(p2)) + ((p16 * math.cos(p2)) / math.sin(p2)))) * math.sin(p2) / math.cos(p2)) - (p9 / math.cos(p11)) - p6
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
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p3 = self._p3.getValue()
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p9 = self._p9.getValue()
        p11 = self._p11.getValue() / (180.0 / math.pi)
        p12 = self._p12.getValue()
        p16 = self._p16.getValue()

        maxValue = ((p6 + p12 + (p9 / math.cos(p11)) * (math.cos(p2)) / math.sin(p2) - (p1 * 0.5) + (p8 * 0.5)) + (p3 / math.sin(p2)) - ((p16 * math.cos(p2)) / math.sin(p2))) * (-math.sin(p2))

        return maxValue - epsilon

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
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p3 = self._p3.getValue()
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p9 = self._p9.getValue()
        p11 = self._p11.getValue() / (180.0 / math.pi)
        p12 = self._p12.getValue()
        p16 = self._p16.getValue()
        p166 = self._p166.getValue()

        maxValue = ((p6 + p12 + (p9 / math.cos(p11))) * (math.cos(p2)) / math.sin(p2) + (p8 * 0.5) - ((p16 * math.cos(p2)) / math.sin(p2))) - (p3 / math.sin(p2)) - (p1 * 0.5) * (-math.sin(p2))
        return maxValue - epsilon - p166

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
        return 0.005

    def maxP15(self):
        return self._p8.getValue() - 0.01

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
        return 0.001

    def maxP16(self):
        return self._p6.getValue() - epsilon

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
        return 0.001

    def maxP17(self):
        return self._p4.getValue() * 0.5 - 0.01

    def setP166(self, p166):
        with EditMode(self.getDocument()):
            self._p166.setValue(clamp(p166, self.minP166(), self.maxP166()))
            self._updateGeometry()
        if p166 < self.minP166():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p166 > self.maxP166():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p166(self):
        return self._p166.getValue()

    def minP166(self):
        return self._p168.getValue() / math.sin(math.pi * 0.25) + 0.01

    def maxP166(self):
        p1 = self._p1.getValue()
        p2 = self._p2.getValue() / (180.0 / math.pi)
        p6 = self._p6.getValue()
        p8 = self._p8.getValue()
        p14 = self._p14.getValue()
        p15 = self._p15.getValue()
        p16 = self._p16.getValue()
        p166 = self._p166.getValue()
        p168 = self._p168.getValue()
        p174 = self._p174.getValue()
        l = (p16 * math.cos(p2) / math.sin(p2)) + ((p1 - p8) * 0.5)
        defH = ((l + ((p8 - p15) * 0.5)) * math.sin(p2)) / math.cos(p2) - p14
        listLienPnt = []
        listLienPnt.append(Geom.Pnt(-p166 - (p8 * 0.5), (p1 - p174) * 0.5, defH))
        listLienPnt.append(Geom.Pnt(-(p8 * 0.5), (p1 - p174) * 0.5, defH - p166))
        listLienPnt.append(Geom.Pnt(-(p8 * 0.5), (p1 - p174) * 0.5, defH - p166 + (p168 / math.sin(math.pi * 0.25))))
        listLienPnt.append(Geom.Pnt(-p166 - (p8 * 0.5) + (p168 / math.sin(math.pi * 0.25)), (p1 - p174) * 0.5, defH))
        return defH - p6

    def setP168(self, p168):
        with EditMode(self.getDocument()):
            self._p168.setValue(clamp(p168, self.minP168(), self.maxP168()))
            self._updateGeometry()
        if p168 < self.minP168():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p168 > self.maxP168():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p168(self):
        return self._p168.getValue()

    def minP168(self):
        return 0.0001

    def maxP168(self):
        return self._p166.getValue() * math.sin(0.25 * math.pi)

    def setP174(self, p174):
        with EditMode(self.getDocument()):
            self._p174.setValue(clamp(p174, self.minP174(), self.maxP174()))
            self._updateGeometry()
        if p174 < self.minP174():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        elif p174 > self.maxP174():
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def p174(self):
        return self._p174.getValue()

    def minP174(self):
        return 0.0001

    def maxP174(self):
        return self._p8.getValue()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == FermeLatPanDev._p1ParamName:
            self.setP1(self._p1.getValue())
        elif aPropertyName == FermeLatPanDev._p2ParamName:
            self.setP2(self._p2.getValue())
        elif aPropertyName == FermeLatPanDev._p3ParamName:
            self.setP3(self._p3.getValue())
        elif aPropertyName == FermeLatPanDev._p4ParamName:
            self.setP4(self._p4.getValue())
        elif aPropertyName == FermeLatPanDev._p5ParamName:
            self.setP5(self._p5.getValue())
        elif aPropertyName == FermeLatPanDev._p6ParamName:
            self.setP6(self._p6.getValue())
        elif aPropertyName == FermeLatPanDev._p7ParamName:
            self.setP7(self._p7.getValue())
        elif aPropertyName == FermeLatPanDev._p8ParamName:
            self.setP8(self._p8.getValue())
        elif aPropertyName == FermeLatPanDev._p9ParamName:
            self.setP9(self._p9.getValue())
        elif aPropertyName == FermeLatPanDev._p10ParamName:
            self.setP10(self._p10.getValue())
        elif aPropertyName == FermeLatPanDev._p10ParamName:
            self.setP10(self._p10.getValue())
        elif aPropertyName == FermeLatPanDev._p11ParamName:
            self.setP11(self._p11.getValue())
        elif aPropertyName == FermeLatPanDev._p12ParamName:
            self.setP12(self._p12.getValue())
        elif aPropertyName == FermeLatPanDev._p13ParamName:
            self.setP13(self._p13.getValue())
        elif aPropertyName == FermeLatPanDev._p14ParamName:
            self.setP14(self._p14.getValue())
        elif aPropertyName == FermeLatPanDev._p15ParamName:
            self.setP15(self._p15.getValue())
        elif aPropertyName == FermeLatPanDev._p16ParamName:
            self.setP16(self._p16.getValue())
        elif aPropertyName == FermeLatPanDev._p17ParamName:
            self.setP17(self._p17.getValue())
        elif aPropertyName == FermeLatPanDev._p166ParamName:
            self.setP166(self._p166.getValue())
        elif aPropertyName == FermeLatPanDev._p168ParamName:
            self.setP168(self._p168.getValue())
        elif aPropertyName == FermeLatPanDev._p174ParamName:
            self.setP174(self._p174.getValue())

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        doc.beginEditing()
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
        doc.endEditing()
        doc.recompute()
    
if __name__ == "__main__":   
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{91C50017-037F-43D3-AE7C-FB8D2A719395}"))

    comp = FermeLatPanDev(doc)

    # Begin editing of the Element
    doc.beginEditing()
    comp.createCompound()

    thisScript = lx.Application.getInstance().getActiveScript()
    if thisScript.isDragAndDropped():
        pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
    else:
        pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

    comp.setLocalPlacement(pos)

    # End editing of the Element
    doc.endEditing()
    doc.recompute()