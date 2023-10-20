# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import os, traceback, math
import Base, Core, Geom, Topo, Draw

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()
epsilon = 0.0001

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


class Arc3Pnt:
    def __init__(self, p1, p2, p3):


        self._startPt = Geom.Pnt(p1)
        self._endPt = Geom.Pnt(p3)

        self._centerPt = Arc3Pnt._calcCenterPt(p1, p2, p3)

        self._startVec = Geom.Vec(self._centerPt, self._startPt)
        middleVec = Geom.Vec(self._centerPt, p2)
        endVec = Geom.Vec(self._centerPt, self._endPt)

        self._normVec = self._startVec.crossed(endVec)
        if self._normVec.squareMagnitude() < epsilon:
            self._normVec = self._startVec.crossed(middleVec)
        self._normVec.normalize()

        self._angle = Arc3Pnt._calcAngle(self._startVec, middleVec, endVec, self._normVec)

        self._axis = Geom.Ax1(self._centerPt, Geom.Dir(self._normVec))

    def copy(self):
        return Arc3Pnt(self._startPt, self.paramPt(0.5), self._endPt)

    @staticmethod
    def _calcBaryCenter(w1, p1, w2, p2, w3, p3):
        x = w1 * p1.x() + w2 * p2.x() + w3 * p3.x()
        y = w1 * p1.y() + w2 * p2.y() + w3 * p3.y()
        z = w1 * p1.z() + w2 * p2.z() + w3 * p3.z()

        return Geom.Pnt(x, y, z)

    @staticmethod
    def _calcCenterPt(p1, p2, p3):
        # For the formulas, please look at https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_from_cross-_and_dot-products

        v12 = Geom.Vec(p2, p1)
        v13 = Geom.Vec(p3, p1)
        v21 = Geom.Vec(p1, p2)
        v23 = Geom.Vec(p3, p2)
        v31 = Geom.Vec(p1, p3)
        v32 = Geom.Vec(p2, p3)

        v12Len = v12.magnitude()
        v13Len = v13.magnitude()
        v23Len = v23.magnitude()

        vCross = v12.crossed(v23)
        vCrossLen = vCross.magnitude()

        invDen = 1.0 / (2.0 * vCrossLen * vCrossLen)  # Inverted denominator

        # Weights
        w1 = v23Len * v23Len * v12.dot(v13) * invDen
        w2 = v13Len * v13Len * v21.dot(v23) * invDen
        w3 = v12Len * v12Len * v31.dot(v32) * invDen

        return Arc3Pnt._calcBaryCenter(w1, p1, w2, p2, w3, p3)

    @staticmethod
    def _basisAngle(vec, u, v):
        # All 3 vectors must be normalized

        uAngle = math.acos(u.dot(vec))
        vAngleCos = v.dot(vec)

        if vAngleCos > 0.0:
            uAngle = (2.0 * math.pi) - uAngle

        return uAngle

    @staticmethod
    def _calcAngle(v1, v2, v3, vNorm):
        nv1 = v1.normalized()
        nv2 = v2.normalized()
        nv3 = v3.normalized()
        # vNorm must be already normalized

        pnv1 = vNorm.crossed(nv1)

        angle2 = Arc3Pnt._basisAngle(nv2, nv1, pnv1)
        angle3 = Arc3Pnt._basisAngle(nv3, nv1, pnv1)

        if (angle2 + epsilon) > angle3:
            return v1.angle(v3)
        else:
            return - ((2.0 * math.pi) - v1.angle(v3))

    def angle(self):
        return self._angle

    def radius(self):
        return self._centerPt.distance(self._startPt)

    def length(self):
        return math.fabs(self.radius() * self._angle)

    def paramRatio(self):
        return 1.0 / self.length()

    def partLength(self, dt):
        return self.radius() * self._angle * dt

    def startPt(self):
        return self._startPt

    def endPt(self):
        return self._endPt

    def centerPt(self):
        return self._centerPt

    def paramPt(self, t):
        if t < epsilon:
            return self._startPt
        if (t + epsilon) > 1.0:
            return self._endPt

        paramVec = self._startVec.rotated(self._axis, self._angle * t)
        return self._centerPt.translated(paramVec)

    def startTangent(self):
        return self.paramTangent(0.0)

    def endTangent(self):
        return self.paramTangent(1.0)

    def paramTangent(self, t):
        if t < epsilon:
            t = 0.0
        if (t + epsilon) > 1.0:
            t = 1.0

        dt = 0.02

        dArc = None
        if (1.0 - t) > dt:
            pt1 = self.paramPt(t)
            pt2 = self.paramPt(t + dt)

            dArc = Geom.Vec(pt1, pt2)
        else:
            pt1 = self.paramPt(t - dt)
            pt2 = self.paramPt(t)

            dArc = Geom.Vec(pt1, pt2)
        dArc.normalize()

        return dArc

class DormerRElem(lx.Element):
    def getGlobalClassId(self):
        return Base.GlobalId("{673F4134-78A9-4B6E-9DC0-DA73E2603285}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("DormerRElem", "OpenLxApp.Element")
        # Register properties 
        self.setPropertyHeader(lxstr("DormerR"), -1)
        self.setPropertyGroupName(lxstr("Dormer parameter"), -1)

        self._length = self.registerPropertyDouble("Length", \
                                                   4.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self._width  = self.registerPropertyDouble("Width", \
                                                   4.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self._height = self.registerPropertyDouble("Height", \
                                                   4.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self.top = self.registerPropertyDouble("Top", \
                                               1.0, \
                                               lx.Property.VISIBLE, \
                                               lx.Property.EDITABLE, \
                                               -1)
        self._side = self.registerPropertyDouble("Side", \
                                                 1.0, \
                                                 lx.Property.VISIBLE, \
                                                 lx.Property.EDITABLE, \
                                                 -1)
        self._front = self.registerPropertyDouble("Front", \
                                                    1.0, \
                                                    lx.Property.VISIBLE, \
                                                    lx.Property.EDITABLE, \
                                                    -1)
        

        self._updateGeometry()

    def setLength(self, length):
        self._length.setValue(clamp(length, self._front.getValue() + epsilon, 10000.0))
        self._updateGeometry()

    def length(self):
        return self._length.getValue()

    def setWidth(self, width):
        self._width.setValue(clamp(width, self._side.getValue() * 2 + epsilon, 10000.0))
        self._updateGeometry()

    def width(self):
        return self._width.getValue()

    def setHeight(self, height):
        self._height.setValue(clamp(height, self.top.getValue(), 10000.0))
        self._updateGeometry()

    def height(self):
        return self._height.getValue()

    def setTop(self, top):
        self.top.setValue(clamp(top, self.minTop(), self._width.getValue() * 0.5))
        self._updateGeometry()

    def top(self):
        return self.top.getValue()

    def minTop(self):
        height = self._height.getValue()
        width = self._width.getValue()
        bAngle = 0.5 * width / height
        minValue = height - (height * math.cos(bAngle))
        return minValue


    def setSide(self, side):
        self._side.setValue(clamp(side, 0.1, self._width.getValue() * 0.5 - 0.1))
        self._updateGeometry()

    def side(self):
        return self._side.getValue()

    def setFront(self, front):
        self._front.setValue(clamp(front, epsilon, self.maxFront()))
        self._updateGeometry()

    def front(self):
        return self._front.getValue()

    def maxFront(self):
        return self._width.getValue() - 0.1

    def _createGeometry(self):

        length = self._length.getValue()
        width = self._width.getValue()
        height = self._height.getValue()
        top = self.top.getValue()
        off1 = self._side.getValue()
        off2 = self._front.getValue()

        x = -length * 0.5
        X = length * 0.5
        y = -width * 0.5
        Y = width * 0.5

        arcOut = Arc3Pnt(Geom.Pnt(X, Y, height - top), Geom.Pnt(X, 0.0, height), Geom.Pnt(X, y, height - top))
        centerPnt = arcOut.centerPt()
        angle = arcOut.angle() * 0.5

        if off1 > epsilon:
            if math.sin(angle) != 0:
                r = off1 / math.sin(angle)
            else:
                r = 0.0
            cathetus = math.sqrt((r * r) - (off1 * off1))
        else:
            cathetus = 0.0

        vecOutsideArc = Geom.Vec(Geom.Pnt(0.0, centerPnt.y(), centerPnt.z()), Geom.Pnt(0.0, Y - off1, height - cathetus - top))
        dist = Geom.Vec.magnitude(vecOutsideArc)

        n = int(angle*180.0/math.pi)
        if n < 5:
            n = 5

        firstTopList = []
        secondTopList = []
        frontList = []

        firstTopArc = Arc3Pnt(Geom.Pnt(X, Y, height - top), Geom.Pnt(X, 0.0, height), Geom.Pnt(X, y, height - top))
        secondTopArc = Arc3Pnt(Geom.Pnt(x, Y, height - top), Geom.Pnt(x, 0.0, height), Geom.Pnt(x, y, height - top))
        frontArc = Arc3Pnt(Geom.Pnt(X - off2, Y - off1, height - cathetus - top), Geom.Pnt(X - off2, 0.0, centerPnt.z() + dist), Geom.Pnt(X - off2, y + off1, height - cathetus - top))

        for i in range(n+1):
            firstTopList.append(firstTopArc.paramPt(1.0 - (float(i) * (1.0 / float(n)))))

        for i in range(n+1):
            secondTopList.append(secondTopArc.paramPt(1.0 - (float(i) * (1.0 / float(n)))))

        for i in range(n+1):
            frontList.append(frontArc.paramPt(1.0 - (float(i) * (1.0 / float(n)))))


        mdl = FacetedModelAssembler(doc)
        mdl.beginModel()

        mdl.addExtrusionBridgePos(firstTopList, secondTopList, False)
        mdl.addExtrusionBridgePos(firstTopList, frontList, False)

        mdl.beginFace()
        mdl.addVertexList(frontList)
        mdl.addVertex(Geom.Pnt(X - off2, Y - off1, 0.0))
        mdl.addVertex(Geom.Pnt(X - off2, y + off1, 0.0))
        mdl.endFace()

        #R
        mdl.beginFace()
        mdl.addVertex(Geom.Pnt(X, Y, height - top))
        mdl.addVertex(Geom.Pnt(X - off2, Y - off1, height - cathetus - top))
        mdl.addVertex(Geom.Pnt(x, Y - off1, height - cathetus - top))
        mdl.addVertex(Geom.Pnt(x, Y, height - top))
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertex(Geom.Pnt(x, Y - off1, height - cathetus - top))
        mdl.addVertex(Geom.Pnt(X - off2, Y - off1, height - cathetus - top))
        mdl.addVertex(Geom.Pnt(X - off2, Y - off1, 0.0))
        mdl.endFace()

        #L
        mdl.beginFace()
        mdl.addVertex(Geom.Pnt(x, y, height - top))
        mdl.addVertex(Geom.Pnt(x, y + off1, height - cathetus - top))
        mdl.addVertex(Geom.Pnt(X - off2, y + off1, height - cathetus - top))
        mdl.addVertex(Geom.Pnt(X, y, height - top))
        mdl.endFace()

        mdl.beginFace()
        mdl.addVertex(Geom.Pnt(X - off2, y + off1, 0.0))
        mdl.addVertex(Geom.Pnt(X - off2, y + off1, height - cathetus - top))
        mdl.addVertex(Geom.Pnt(x, y + off1, height - cathetus - top))
        mdl.endFace()

        return mdl.endModel()

    def modifyElem(self):
        geom = self._createGeometry()
        if geom:
            self.setGeometry(geom)

    def _updateGeometry(self):

        geom = self._createGeometry()
        self.setGeometry(geom)

        doc.endEditing()
        doc.recompute()

    def onPropertyChanged(self, aPropertyName):

        doc = self.getDocument()
        doc.beginEditing()

        if aPropertyName == "Length":
            self.setLength(self._length.getValue())
        elif aPropertyName == "Width":
            self.setWidth(self._width.getValue())
        elif aPropertyName == "Height":
            self.setHeight(self._height.getValue())
        elif aPropertyName == "Top":
            self.setTop(self.top.getValue())
        elif aPropertyName == "Side":
            self.setSide(self._side.getValue())
        elif aPropertyName == "Front":
            self.setFront(self._front.getValue())
        
    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        doc.beginEditing()
        if not Geom.GeomTools.isEqual(x,1.):
            old = self._length.getValue()
            self._length.setValue(old * x)
            self.modifyElem()      
        if not Geom.GeomTools.isEqual(y,1.):
            old = self._width.getValue()
            self._width.setValue(old * y)
            self.modifyElem() 
        if not Geom.GeomTools.isEqual(z,1.):
            old = self._height.getValue()
            self._height.setValue(old * z)
            self.modifyElem()
            
        self.translateAfterScaled(aVec, aScaleBasePnt)
        doc.endEditing()
        doc.recompute()
    
if __name__ == "__main__":   
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{86FAE956-A45E-479C-B93A-E46FBFE4EE17}"))
    
    blockElem = DormerRElem(doc)
    
    # Begin editing of the Element
    doc.beginEditing()
    b = blockElem._createGeometry()
    blockElem.setGeometry(b)

    thisScript = lx.Application.getInstance().getActiveScript()
    if thisScript.isDragAndDropped():
        pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
    else:
        pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

    blockElem.setLocalPlacement(pos)

    # End editing of the Element
    doc.endEditing()
    doc.recompute()   
    