# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

epsilon = 0.001

def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))

class Dormer5aElem(lx.Element):
    def getGlobalClassId(self):
        return Base.GlobalId("{EF7BAAFC-42A4-42B0-B0E6-CBF0487E7967}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Dormer5aElem", "OpenLxApp.Element")
        # Register properties 
        self.setPropertyHeader(lxstr("Dormer5a"), -1)
        self.setPropertyGroupName(lxstr("Dormer parameter"), -1)
        self._length = self.registerPropertyDouble("Length",   \
                                                   10.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)  
        self._width = self.registerPropertyDouble("Width", \
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
                                                   3.0, \
                                                   lx.Property.VISIBLE, \
                                                   lx.Property.EDITABLE, \
                                                   -1)
        

        self._updateGeometry()

    def setLength(self, length):
        self._length.setValue(clamp(length, epsilon, 100000.0))
        self._updateGeometry()

    def length(self):
        return self._length.getValue()

    def setWidth(self, width):
        self._width.setValue(clamp(width, epsilon, 100000))
        self._updateGeometry()

    def width(self):
        return self._width.getValue()

    def setHeight(self, height):
        self._height.setValue(clamp(height, self._topHeight.getValue(), 10000.0))
        self._updateGeometry()

    def height(self):
        return self._height.getValue()

    def setTopHeight(self, topHeight):
        self._topHeight.setValue(clamp(topHeight, epsilon, self.maxTopHeight()))
        self._updateGeometry()

    def topHeight(self):
        return self._topHeight.getValue()

    def maxTopHeight(self):
        firstMin = self._height.getValue()
        secondMin = self._width.getValue() * 0.5
        if firstMin > secondMin:
            return secondMin
        return firstMin

    def _createGeometry(self):

        length = self._length.getValue()
        width = self._width.getValue()
        height = self._height.getValue()
        topHeight = self._topHeight.getValue()

        pointList = []

        pointList.append(Geom.Pnt(length * 0.5, -(width * 0.5), height - topHeight))
        pointList.append(Geom.Pnt(length * 0.5, 0.0, height))
        pointList.append(Geom.Pnt(length * 0.5, width * 0.5, height - topHeight))

        pointList.append(Geom.Pnt(length * 0.5, width * 0.5, 0.0))
        pointList.append(Geom.Pnt(length * 0.5, -(width * 0.5), 0.0))

        edgeList = Topo.vector_Edge(4)

        edgeList[0] = Topo.EdgeTool.makeArcOfCircle(pointList[0], pointList[1], pointList[2])
        edgeList[1] = Topo.EdgeTool.makeEdge(pointList[2], pointList[3])
        edgeList[2] = Topo.EdgeTool.makeEdge(pointList[3], pointList[4])
        edgeList[3] = Topo.EdgeTool.makeEdge(pointList[4], pointList[0])

        wire = Topo.WireTool.makeWire(edgeList, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())

        faceBeam = Topo.FaceTool.extrudedFace(face, Geom.Dir(-1.0, 0.0, 0.0), length)

        geom = lx.AdvancedBrep.createIn(doc)
        geom.setShape(faceBeam)

        return geom
    
    def modifyElem(self):
        block = self._createGeometry()
        if block:
            self.setGeometry(block)

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
    doc.registerPythonScript(Base.GlobalId("{C673F2F4-15AB-40BE-9B0D-7D890165184D}"))
    
    blockElem = Dormer5aElem(doc)
    
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
    