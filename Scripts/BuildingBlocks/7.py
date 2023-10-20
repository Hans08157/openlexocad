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

class Dormer5Elem(lx.Element):
    def getGlobalClassId(self):
        return Base.GlobalId("{C82753C5-4CFE-429D-A9A7-0F46B9F556BB}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Dormer5Elem", "OpenLxApp.Element")
        # Register properties 
        self.setPropertyHeader(lxstr("Dormer5"), -1)
        self.setPropertyGroupName(lxstr("Dormer parameter"), -1)

        self._length = self.registerPropertyDouble("Length", \
                                                   10.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self._width  = self.registerPropertyDouble("Width", \
                                                   10.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self._height = self.registerPropertyDouble("Height", \
                                                   10.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        self._topHeight = self.registerPropertyDouble("Top height", \
                                                      4.0, \
                                                      lx.Property.VISIBLE, \
                                                      lx.Property.EDITABLE, \
                                                      -1)
        self._offset1 = self.registerPropertyDouble("Offset 1", \
                                                    2.0, \
                                                    lx.Property.VISIBLE, \
                                                    lx.Property.EDITABLE, \
                                                    -1)
        self._offset2 = self.registerPropertyDouble("Offset 2", \
                                                    2.0, \
                                                    lx.Property.VISIBLE, \
                                                    lx.Property.EDITABLE, \
                                                    -1)
        

        self._updateGeometry()

    def setLength(self, length):
        self._length.setValue(clamp(length, self._offset2.getValue() + epsilon, 10000.0))
        self._updateGeometry()

    def length(self):
        return self._length.getValue()

    def setWidth(self, width):
        self._width.setValue(clamp(width, self._offset1.getValue() * 2 + epsilon, 10000.0))
        self._updateGeometry()

    def width(self):
        return self._width.getValue()

    def setHeight(self, height):
        self._height.setValue(clamp(height, self._topHeight.getValue(), 10000.0))
        self._updateGeometry()

    def height(self):
        return self._height.getValue()

    def setTopHeight(self, topHeight):
        self._topHeight.setValue(clamp(topHeight, 0.01, self._width.getValue() * 0.5))
        self._updateGeometry()

    def topHeight(self):
        return self._topHeight.getValue()

    def setOffset1(self, offset1):
        self._offset1.setValue(clamp(offset1, epsilon, self._width.getValue() * 0.5))
        self._updateGeometry()

    def offset1(self):
        return self._offset1.getValue()

    def setOffset2(self, offset2):
        self._offset2.setValue(clamp(offset2, epsilon, self._length.getValue() - epsilon))
        self._updateGeometry()

    def offset2(self):
        return self._offset2.getValue()
      
    def _createGeometry(self):

        if self._length.getValue() < epsilon:
            self._length.setValue(epsilon)
        if self._height.getValue() < epsilon:
            self._height.setValue(epsilon)
        if self._width.getValue() < epsilon:
            self._width.setValue(epsilon)
        if self._topHeight.getValue() * 2 > self._height.getValue():
            self._topHeight.setValue(self._height.getValue() * 0.5)
        if self._topHeight.getValue() * 2 > self._width.getValue():
            self._topHeight.setValue(self._width.getValue() * 0.5)
        if self._offset1.getValue() * 2.0 > self._width.getValue() - epsilon:
            self._offset1.setValue(self._width.getValue() / 2 + epsilon)
        if self._offset2.getValue() > self._length.getValue() - epsilon:
            self._offset2.setValue(self._length.getValue() - epsilon)

        length = self._length.getValue()
        width = self._width.getValue()
        height = self._height.getValue()
        topHeight = self._topHeight.getValue()
        off1 = self._offset1.getValue()
        off2 = self._offset2.getValue()

        pointList = []
        listFace = Topo.vector_Face(9)

        x = -length * 0.5
        X = length * 0.5
        y = -width * 0.5
        Y = width * 0.5

        #bottom
        pointList.append(Geom.Pnt(x, y + off1, 0.0))
        pointList.append(Geom.Pnt(x, Y - off1, 0.0))
        pointList.append(Geom.Pnt(X - off2, Y - off1, 0.0))
        pointList.append(Geom.Pnt(X - off2, y + off1, 0.0))

        #top
        pointList.append(Geom.Pnt(x, y, height - topHeight))
        pointList.append(Geom.Pnt(x, Y, height - topHeight))
        pointList.append(Geom.Pnt(X, Y, height - topHeight))
        pointList.append(Geom.Pnt(X, y, height - topHeight))

        #middle points arc
        pointList.append(Geom.Pnt(X, 0.0, height))
        pointList.append(Geom.Pnt(x, 0.0, height))

        arcOut = Arc3Pnt(pointList[6], pointList[8], pointList[7])
        centrPnt = arcOut.centerPt()
        angle = arcOut.angle() * 0.5

        if off1 > epsilon:
            if math.sin(angle) != 0:
                r = off1 / math.sin(angle)
            else:
                r = 0.0
            katet = math.sqrt((r * r) - (off1 * off1))
        else:
            katet = 0.0

        pointList.append(Geom.Pnt(x, y + off1, height - katet - topHeight))
        pointList.append(Geom.Pnt(x, Y - off1, height - katet - topHeight))
        pointList.append(Geom.Pnt(X - off2, Y - off1, height - katet - topHeight))
        pointList.append(Geom.Pnt(X - off2, y + off1, height - katet - topHeight))

        vecOutsideArc = Geom.Vec(Geom.Pnt(0.0, centrPnt.y(), centrPnt.z()), Geom.Pnt(0.0, pointList[12].y(), pointList[12].z()))
        dist = Geom.Vec.magnitude(vecOutsideArc)

        pointList.append(Geom.Pnt(X - off2, 0.0, centrPnt.z() + dist))  #14

        edgeList = Topo.vector_Edge(4)
        edgeList[0] = Topo.EdgeTool.makeEdge(pointList[7], pointList[4])
        edgeList[1] = Topo.EdgeTool.makeArcOfCircle(pointList[4], pointList[9], pointList[5])
        edgeList[2] = Topo.EdgeTool.makeEdge(pointList[5], pointList[6])
        edgeList[3] = Topo.EdgeTool.makeArcOfCircle(pointList[6], pointList[8], pointList[7])
        wire = Topo.WireTool.makeWire(edgeList, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        listFace[0] = face

        edgeListBack = Topo.vector_Edge(6)
        edgeListBack[0] = Topo.EdgeTool.makeEdge(pointList[0], pointList[1])
        edgeListBack[1] = Topo.EdgeTool.makeEdge(pointList[1], pointList[11])
        edgeListBack[2] = Topo.EdgeTool.makeEdge(pointList[11], pointList[5])
        edgeListBack[3] = Topo.EdgeTool.makeArcOfCircle(pointList[5], pointList[9], pointList[4])
        edgeListBack[4] = Topo.EdgeTool.makeEdge(pointList[4], pointList[10])
        edgeListBack[5] = Topo.EdgeTool.makeEdge(pointList[10], pointList[0])
        wire = Topo.WireTool.makeWire(edgeListBack, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        listFace[1] = face

        edgeList1 = Topo.vector_Edge(4)
        edgeList1[0] = Topo.EdgeTool.makeEdge(pointList[10], pointList[13])
        edgeList1[1] = Topo.EdgeTool.makeEdge(pointList[13], pointList[7])
        edgeList1[2] = Topo.EdgeTool.makeEdge(pointList[7], pointList[4])
        edgeList1[3] = Topo.EdgeTool.makeEdge(pointList[4], pointList[10])
        wire = Topo.WireTool.makeWire(edgeList1, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        listFace[2] = face

        edgeList2 = Topo.vector_Edge(4)
        edgeList2[0] = Topo.EdgeTool.makeEdge(pointList[11], pointList[12])
        edgeList2[1] = Topo.EdgeTool.makeEdge(pointList[12], pointList[6])
        edgeList2[2] = Topo.EdgeTool.makeEdge(pointList[6], pointList[5])
        edgeList2[3] = Topo.EdgeTool.makeEdge(pointList[5], pointList[11])
        wire = Topo.WireTool.makeWire(edgeList2, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        listFace[3] = face

        edgeListBot = Topo.vector_Edge(4)
        edgeListBot[0] = Topo.EdgeTool.makeEdge(pointList[0], pointList[10])
        edgeListBot[1] = Topo.EdgeTool.makeEdge(pointList[10], pointList[13])
        edgeListBot[2] = Topo.EdgeTool.makeEdge(pointList[13], pointList[3])
        edgeListBot[3] = Topo.EdgeTool.makeEdge(pointList[3], pointList[0])
        wire = Topo.WireTool.makeWire(edgeListBot, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        listFace[4] = face

        edgeListTop = Topo.vector_Edge(4)
        edgeListTop[0] = Topo.EdgeTool.makeEdge(pointList[1], pointList[2])
        edgeListTop[1] = Topo.EdgeTool.makeEdge(pointList[2], pointList[12])
        edgeListTop[2] = Topo.EdgeTool.makeEdge(pointList[12], pointList[11])
        edgeListTop[3] = Topo.EdgeTool.makeEdge(pointList[11], pointList[1])
        wire = Topo.WireTool.makeWire(edgeListTop, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        listFace[5] = face

        edgeListTop1 = Topo.vector_Edge(4)
        edgeListTop1[0] = Topo.EdgeTool.makeEdge(pointList[13], pointList[7])
        edgeListTop1[1] = Topo.EdgeTool.makeArcOfCircle(pointList[7], pointList[8], pointList[6])
        edgeListTop1[2] = Topo.EdgeTool.makeEdge(pointList[6], pointList[12])
        edgeListTop1[3] = Topo.EdgeTool.makeArcOfCircle(pointList[12], pointList[14], pointList[13])
        wire = Topo.WireTool.makeWire(edgeListTop1, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        listFace[6] = face

        edgeListTop2 = Topo.vector_Edge(4)
        edgeListTop2[0] = Topo.EdgeTool.makeArcOfCircle(pointList[13], pointList[14], pointList[12])
        edgeListTop2[1] = Topo.EdgeTool.makeEdge(pointList[12], pointList[2])
        edgeListTop2[2] = Topo.EdgeTool.makeEdge(pointList[2], pointList[3])
        edgeListTop2[3] = Topo.EdgeTool.makeEdge(pointList[3], pointList[13])
        wire = Topo.WireTool.makeWire(edgeListTop2, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        listFace[7] = face

        edgeListB = Topo.vector_Edge(4)
        edgeListB[0] = Topo.EdgeTool.makeEdge(pointList[3], pointList[2])
        edgeListB[1] = Topo.EdgeTool.makeEdge(pointList[2], pointList[1])
        edgeListB[2] = Topo.EdgeTool.makeEdge(pointList[1], pointList[0])
        edgeListB[3] = Topo.EdgeTool.makeEdge(pointList[0], pointList[3])
        wire = Topo.WireTool.makeWire(edgeListB, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        listFace[8] = face

        listShape = Topo.ShapeTool.makeShape(listFace)

        geom = lx.AdvancedBrep.createIn(doc)
        geom.setShape(listShape)

        return geom
    
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
        elif aPropertyName == "Top height":
            self.setTopHeight(self._topHeight.getValue())
        elif aPropertyName == "Offset 1":
            self.setOffset1(self._offset1.getValue())
        elif aPropertyName == "Offset 2":
            self.setOffset2(self._offset2.getValue())
        
    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())
        print("SCALING")

        doc.beginEditing()
        if not Geom.GeomTools.isEqual(x,1.):
            print("Scaling in X")
            old = self._length.getValue()
            self._length.setValue(old * x)
            self.modifyElem()      
        if not Geom.GeomTools.isEqual(y,1.):
            print("Scaling in Y")
            old = self._width.getValue()
            self._width.setValue(old * y)
            self.modifyElem() 
        if not Geom.GeomTools.isEqual(z,1.):
            print("Scaling in Z")
            old = self._height.getValue()
            self._height.setValue(old * z)
            self.modifyElem()
            
        self.translateAfterScaled(aVec, aScaleBasePnt)
        doc.endEditing()
        doc.recompute()
    
if __name__ == "__main__":   
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{7185DAAB-4558-47E4-AB26-796BA3AB4216}"))
    
    blockElem = Dormer5Elem(doc)
    
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
    