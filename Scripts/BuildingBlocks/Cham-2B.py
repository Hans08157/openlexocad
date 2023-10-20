# coding=utf-8
# Author: Pavlo Leskovych
# Version 1.0.0  07.05.2020
# Attributes:
    # Version 1.0.0
        # Translations
        # A basic structure with the chamber and base SubElement and the chamber's tapes

# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import math, copy, traceback
from typing import Optional, List, Tuple, Union
from enum import Enum

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString
doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

# Exceptions
class BobCutException(Exception):
    # custom message
    def __init__(self, message: Optional[str] = "Bob cut error") -> None:
        super(BobCutException, self).__init__(message)


CW_COLOR = 3135

epsilon = 0.001
maxValue = 10000

CHAMBER_TYPES = {
    "2B": {
        "bottom_height": 0.10,
        "external_length": 1.24,
        "external_width": 1.20,
        "internal_length": 1.00,
        "internal_width": 0.96,
        "heights": {
            "2B AF06": 0.60,
            "2B AF09": 0.90,
            "2B AF12": 1.20,
            "2B SF06": 0.60,
            "2B SF09": 0.90,
            "2B SF12": 1.20,
        },
        "tapes": {
            "CHB E CDD 126 127": {
                "width": 1.27,
                "length": 1.26,
                "height": 0.24,
                "inner_width": 0.93,
                "inner_length": 0.95,
            },
            "CHB E CDB 124 120N": {
                "width": 1.24,
                "length": 1.20,
                "height": 0.20,
                "inner_width": 0.96,
                "inner_length": 1.00,
            },
            "CHB CON 124 120": {
                "width": 1.22,
                "length": 1.22,
                "height": 0.40,
                "inner_diameter": 0.60,
            },
            "CHB CV T10 120 030": {
                "width": 1.20,
                "length": 0.30,
                "height": 0.065,
            },
            "CHB CV T25 120 030": {
                "width": 1.20,
                "length": 0.30,
                "height": 0.10,
            },
            "CHB CV T60 120 030": {
                "width": 1.20,
                "length": 0.30,
                "height": 0.13,
            },
        }
    }
}


class ElemTypeEnum(Enum):
    LX_ELEMENT = "lx.Element"
    LX_SUB_ELEMENT = "lx.SubElement"


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
        x = -b / (2.0 * a)

        return [x]
    else:
        return []


def qstr(str):
    return Base.StringTool.toQString(lxstr(str))
# Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))


def printVal(name, val):
    print("{} = {}".format(name, val))


def printVec(name, val):
    print("{}: ({}, {}, {})".format(name, val.x(), val.y(), val.z()))


def printVec2D(name, val):
    print("{}: ({}, {})".format(name, val.x(), val.y()))


def printPnt(name, pnt):
    print("{}: [{}, {}, {}]".format(name, pnt.x(), pnt.y(), pnt.z()))


def printPnt2d(name, pnt):
    print("{}: [{}, {}]".format(name, pnt.x(), pnt.y()))


def vecsAreSame(v1, v2, tolerance=epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)


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


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


def baseVecTranslate(pt, baseVec, dist):
    return Geom.Pnt(
        pt.x() + (baseVec.x() * dist),
        pt.y() + (baseVec.y() * dist),
        pt.z() + (baseVec.z() * dist)
    )


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

class DistributionChamber2B(lx.DistributionChamberElement):
    _classID = "{16B4EF7C-928F-425F-A158-6A2F00AEF476}"
    _headerPropName = "Distribution Chamber 2B"
    _groupPropName = "Distribution Chamber Parameter"

    # Parameters property names
    _heightsPropName: str = "Heights"
    _tapeTypePropName: str = "Tape type"
    _showBottomPropName: str = "Show bottom"
    
    def getGlobalClassId(self) -> Base.GlobalId:
        return Base.GlobalId(DistributionChamber2B._classID)

    def __init__(self, aArg) -> None:
        lx.DistributionChamberElement.__init__(self, aArg)
        self.registerPythonClass("DistributionChamber2B", "OpenLxApp.DistributionChamberElement")
        # Register properties
        self.setPropertyHeader(lxstr(DistributionChamber2B._headerPropName), -1)
        self.setPropertyGroupName(lxstr(DistributionChamber2B._groupPropName), -1)

        self._tapeType = self.registerPropertyEnum(DistributionChamber2B._tapeTypePropName, 0,
                                                        lx.Property.VISIBLE,
                                                        lx.Property.EDITABLE, -1)
        self._tapeType.setEmpty()
        for key in list(CHAMBER_TYPES["2B"]["tapes"].keys()):
            self._tapeType.addEntry(lxstr(key), -1)

        self._heights = self.registerPropertyEnum(DistributionChamber2B._heightsPropName, 0,
                                                       lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, -1)
        self._heights.setEmpty()
        for key in list(CHAMBER_TYPES["2B"]["heights"].keys()):
            self._heights.addEntry(lxstr(key), -1)

        self._showBottom = self.registerPropertyBool(
            DistributionChamber2B._showBottomPropName,
            False,
            lx.Property.VISIBLE,
            lx.Property.EDITABLE,
            -1
        )
        
        self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())
        self._updateGeometry()

    def getScriptVersion(self) -> int:
        return 100  # Version 1.0.0

    def setTapeType(self, param) -> None:
        with EditMode(self.getDocument()):
            self._tapeType.setValue(param)
            self._updateGeometry()

    def setHeights(self, param) -> None:
        with EditMode(self.getDocument()):
            self._heights.setValue(param)
            self._updateGeometry()

    def setShowBottom(self, param) -> None:
        with EditMode(self.getDocument()):
            self._showBottom.setValue(param)
            self._updateGeometry()
    
    def buildSubElemLine(aDoc, aFromPnt, aToPnt) -> lx.SubElement:
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
    def _createExtrudedSubElement(listPoint, heightStep, dir) -> lx.SubElement:
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)
        return subElem

    def create_block(self, width: float, height: float, length: float) -> lx.Element:
        doc = self.getDocument()
        half_length = length * 0.5
        half_width = width * 0.5

        # bottom points
        pnt1 = Geom.Pnt(-half_length, -half_width, 0.0)
        pnt2 = Geom.Pnt(-half_length, width, 0.0)
        pnt3 = Geom.Pnt(half_length, half_width, 0.0)
        pnt4 = Geom.Pnt(half_length, -half_width, 0.0)

        # top points
        pnt5 = Geom.Pnt(-half_length, -half_width, height)
        pnt6 = Geom.Pnt(-half_length, width, height)
        pnt7 = Geom.Pnt(half_length, half_width, height)
        pnt8 = Geom.Pnt(half_length, -half_width, height)

        # creating the
        advancedBrep = lx.AdvancedBrep.createIn(doc)
        faceList = Topo.vector_Face(6)
        
        # build bottom edges and face
        bottomEdgeList = Topo.vector_Edge(4)
        bottomEdgeList[0] = Topo.EdgeTool.makeEdge(pnt1, pnt2)
        bottomEdgeList[1] = Topo.EdgeTool.makeEdge(pnt2, pnt3)
        bottomEdgeList[2] = Topo.EdgeTool.makeEdge(pnt3, pnt4)
        bottomEdgeList[3] = Topo.EdgeTool.makeEdge(pnt4, pnt1)
        bottomWire = Topo.WireTool.makeWire(bottomEdgeList, Geom.Precision.linear_Resolution())
        bottomFace = Topo.FaceTool.makeFace(bottomWire, Geom.Precision.linear_Resolution())
        faceList[0] = bottomFace
        
        # build top edges and face
        topEdgeList = Topo.vector_Edge(4)
        topEdgeList[0] = Topo.EdgeTool.makeEdge(pnt8, pnt7)
        topEdgeList[1] = Topo.EdgeTool.makeEdge(pnt7, pnt6)
        topEdgeList[2] = Topo.EdgeTool.makeEdge(pnt6, pnt5)
        topEdgeList[3] = Topo.EdgeTool.makeEdge(pnt5, pnt8)
        topWire = Topo.WireTool.makeWire(topEdgeList, Geom.Precision.linear_Resolution())
        topFace = Topo.FaceTool.makeFace(topWire, Geom.Precision.linear_Resolution())
        faceList[1] = topFace
        
        # build back edges and face
        backEdgeList = Topo.vector_Edge(4)
        backEdgeList[0] = Topo.EdgeTool.makeEdge(pnt4, pnt8)
        backEdgeList[1] = Topo.EdgeTool.makeEdge(pnt8, pnt5)
        backEdgeList[2] = Topo.EdgeTool.makeEdge(pnt5, pnt1)
        backEdgeList[3] = Topo.EdgeTool.makeEdge(pnt1, pnt4)
        backWire = Topo.WireTool.makeWire(backEdgeList, Geom.Precision.linear_Resolution())
        backFace = Topo.FaceTool.makeFace(backWire, Geom.Precision.linear_Resolution())
        faceList[2] = backFace
        
        # build right edges and face
        rightEdgeList = Topo.vector_Edge(4)
        rightEdgeList[0] = Topo.EdgeTool.makeEdge(pnt1, pnt5)
        rightEdgeList[1] = Topo.EdgeTool.makeEdge(pnt5, pnt6)
        rightEdgeList[2] = Topo.EdgeTool.makeEdge(pnt6, pnt2)
        rightEdgeList[3] = Topo.EdgeTool.makeEdge(pnt2, pnt1)
        rightWire = Topo.WireTool.makeWire(rightEdgeList, Geom.Precision.linear_Resolution())
        rightFace = Topo.FaceTool.makeFace(rightWire, Geom.Precision.linear_Resolution())
        faceList[3] = rightFace
        
        # build front edges and face
        frontEdgeList = Topo.vector_Edge(4)
        frontEdgeList[0] = Topo.EdgeTool.makeEdge(pnt6, pnt7)
        frontEdgeList[1] = Topo.EdgeTool.makeEdge(pnt7, pnt3)
        frontEdgeList[2] = Topo.EdgeTool.makeEdge(pnt3, pnt2)
        frontEdgeList[3] = Topo.EdgeTool.makeEdge(pnt2, pnt6)
        frontWire = Topo.WireTool.makeWire(frontEdgeList, Geom.Precision.linear_Resolution())
        frontFace = Topo.FaceTool.makeFace(frontWire, Geom.Precision.linear_Resolution())
        faceList[4] = frontFace

        # build left edges and face
        leftEdgeList = Topo.vector_Edge(4)
        leftEdgeList[0] = Topo.EdgeTool.makeEdge(pnt3, pnt7)
        leftEdgeList[1] = Topo.EdgeTool.makeEdge(pnt7, pnt8)
        leftEdgeList[2] = Topo.EdgeTool.makeEdge(pnt8, pnt4)
        leftEdgeList[3] = Topo.EdgeTool.makeEdge(pnt4, pnt3)
        leftWire = Topo.WireTool.makeWire(leftEdgeList, Geom.Precision.linear_Resolution())
        leftFace = Topo.FaceTool.makeFace(leftWire, Geom.Precision.linear_Resolution())
        faceList[5] = leftFace

        shapeList = Topo.ShapeTool.makeShape(faceList)
        advancedBrep.setShape(shapeList)

        elem = lx.Element.createIn(doc)
        elem.setGeometry(advancedBrep)
        return elem
    
    def create_simplified_block(
        self, width: float, height: float,
        length: float, return_elem_type: ElemTypeEnum = ElemTypeEnum.LX_ELEMENT
    ) -> Union[lx.Element, lx.SubElement]:
        doc = self.getDocument()
        
        internBlock = lx.Block.createIn(doc)
        internBlock.setXLength(length)
        internBlock.setYLength(width)
        internBlock.setZLength(height)
        
        if return_elem_type == ElemTypeEnum.LX_ELEMENT:
            internalElement = lx.Element.createIn(doc)
        elif return_elem_type == ElemTypeEnum.LX_SUB_ELEMENT:
            internalElement = lx.SubElement.createIn(doc)
        else:
            raise ValueError("Unknown return_elem_type")

        internalElement.setGeometry(internBlock)
        return internalElement
    
    def createHandleForNarrowTape(self) -> None:
        head_radius = self._nailHeadRadius.getValue()
        head_length = self._nailHeadLength.getValue()
        angle = math.radians(self._angle.getValue())
        rotateAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(1, 0, 0))
        positionAngle = math.radians(90.0)

        if self._showNailHead.getValue() == 0:
            #  Head profile creation
            head_profile = lx.CircleProfileDef.createIn(doc)
            head_profile.setRadius(head_radius)
            eas2 = lx.ExtrudedAreaSolid.createIn(doc)
            eas2.setSweptArea(head_profile)
            eas2.setExtrudedDirection(Geom.Dir(0, 0, 1))
            eas2.setDepth(head_length)
            headElem = lx.SubElement.createIn(doc)
            headElem.setGeometry(eas2)
            headElem.setDiffuseColor(Base.Color_fromCdwkColor(18))
            headElem.rotate(rotateAxis, -(angle + positionAngle), Geom.CoordSpace_WCS)
            self.addSubElement(headElem)
        else:
            return
    
    def prepare_chamber(
        self, hardElement: lx.Element, softElement: lx.Element,
        return_elem_type: ElemTypeEnum = ElemTypeEnum.LX_ELEMENT
        ) -> Union[lx.Element, lx.SubElement]:
        # cutting two objects
        resultingBlocks = lx.vector_Element()
        if lx.bop_cut(softElement, hardElement, resultingBlocks) != 0:
            print("Error: bop_cut failed")
        
        doc.removeObject(hardElement)
        doc.removeObject(softElement)

        transform = resultingBlocks[0].getTransform()
        geometry = resultingBlocks[0].getGeometry()
        
        if return_elem_type == ElemTypeEnum.LX_ELEMENT:
            baseElement = lx.Element.createIn(doc)
        elif return_elem_type == ElemTypeEnum.LX_SUB_ELEMENT:
            baseElement = lx.SubElement.createIn(doc)
        else:
            raise ValueError("Unknown return_elem_type")
        
        baseElement.setTransform(transform)
        baseElement.setGeometry(geometry)
        return baseElement
    
    def createBottom(self, width: float, height: float, length: float) -> lx.SubElement:
        doc = self.getDocument()
        
        bottomBlock = lx.Block.createIn(doc)
        bottomBlock.setXLength(length)
        bottomBlock.setYLength(width)
        bottomBlock.setZLength(height)
        bottomElement = lx.SubElement.createIn(doc)
        bottomElement.setGeometry(bottomBlock)
        bottomElement.setDiffuseColor(Base.Color_fromCdwkColor(18))
        return bottomElement
    
    def carveTheNichesInChamber(self, chamber_element: lx.Element) -> lx.SubElement:
        # Create 4 blocks and translate them to the 4 sides of the chamber
        doc = self.getDocument()
        niche_height = 0.30
        external_length: float = CHAMBER_TYPES["2B"]["external_length"]
        internal_length: float = CHAMBER_TYPES["2B"]["internal_length"]
        external_width: float = CHAMBER_TYPES["2B"]["external_width"]
        internal_width: float = CHAMBER_TYPES["2B"]["internal_width"]
        niche_width: float = external_width * 0.5
        niche_length: float = external_length * 0.5
        cutting_depth: float = (external_length - internal_length) * 0.25
        
        # create four blocks
        firstBlock = lx.Block.createIn(doc)
        firstBlock.setXLength(niche_length)
        firstBlock.setYLength(niche_width)
        firstBlock.setZLength(niche_height)
        firstBlockElement = lx.Element.createIn(doc)
        firstBlockElement.setGeometry(firstBlock)
        firstBlockElement.translate(Geom.Vec(niche_length * 0.5, -niche_width + cutting_depth, 0.0), Geom.CoordSpace_WCS)
        
        secondBlock = lx.Block.createIn(doc)
        secondBlock.setXLength(niche_length)
        secondBlock.setYLength(niche_width)
        secondBlock.setZLength(niche_height)
        secondBlockElement = lx.Element.createIn(doc)
        secondBlockElement.setGeometry(secondBlock)
        secondBlockElement.translate(Geom.Vec(niche_length * 0.5, 2 * niche_width - cutting_depth, 0.0), Geom.CoordSpace_WCS)
        
        thirdBlock = lx.Block.createIn(doc)
        thirdBlock.setXLength(niche_length)
        thirdBlock.setYLength(niche_width)
        thirdBlock.setZLength(niche_height)
        thirdBlockElement = lx.Element.createIn(doc)
        thirdBlockElement.setGeometry(thirdBlock)
        thirdBlockElement.translate(Geom.Vec(2 * niche_length - cutting_depth, niche_width * 0.5, 0.0), Geom.CoordSpace_WCS)
        
        fourthBlock = lx.Block.createIn(doc)
        fourthBlock.setXLength(niche_length)
        fourthBlock.setYLength(niche_width)
        fourthBlock.setZLength(niche_height)
        fourthBlockElement = lx.Element.createIn(doc)
        fourthBlockElement.setGeometry(fourthBlock)
        fourthBlockElement.translate(Geom.Vec(-niche_length + cutting_depth, niche_width * 0.5, 0.0), Geom.CoordSpace_WCS)
        
        # carve the niches in chamber
        resultingBlocks1 = lx.vector_Element()
        resultingBlocks2 = lx.vector_Element()
        resultingBlocks3 = lx.vector_Element()
        resultingBlocks4 = lx.vector_Element()
        
        if lx.bop_cut(chamber_element, firstBlockElement, resultingBlocks1) != 0:
            print("Error: first bop_cut failed")

        if lx.bop_cut(resultingBlocks1[0], secondBlockElement, resultingBlocks2) != 0:
            print("Error: bop_cut failed")
        
        if lx.bop_cut(resultingBlocks2[0], thirdBlockElement, resultingBlocks3) != 0:
            print("Error: bop_cut failed")
        
        if lx.bop_cut(resultingBlocks3[0], fourthBlockElement, resultingBlocks4) != 0:
            print("Error: bop_cut failed")
        
        doc.removeObject(firstBlockElement)
        doc.removeObject(secondBlockElement)
        doc.removeObject(thirdBlockElement)
        doc.removeObject(fourthBlockElement)
        doc.removeObject(chamber_element)

        transform = resultingBlocks4[0].getTransform()
        geometry = resultingBlocks4[0].getGeometry()
        
        chamberElement = lx.SubElement.createIn(doc)
        chamberElement.setTransform(transform)
        chamberElement.setGeometry(geometry)
        chamberElement.setDiffuseColor(Base.Color_fromCdwkColor(18))
        return chamberElement
    
    def _get_tape_type_string(self) -> str:
        tape_type_index: int = self._tapeType.getValue()
        tape_type = list(CHAMBER_TYPES["2B"]["tapes"].keys())
        tape_type: str = tape_type[tape_type_index]
        return tape_type
    
    def _calculate_height_offset_for_tape(self, tape_type: str) -> float:
        def get_height_type_string() -> str:
            height_type_index: int = self._heights.getValue()
            height_type = list(CHAMBER_TYPES["2B"]["heights"].keys())
            height_type: str = height_type[height_type_index]
            return height_type
    
        base_height: float = CHAMBER_TYPES["2B"]["bottom_height"]
        current_chamber_height: float = CHAMBER_TYPES["2B"]["heights"][get_height_type_string()]
        starting_height: float = current_chamber_height
        if self._showBottom.getValue() == True:
            starting_height += base_height
        
        return starting_height
    
    def create_tape_B400(self) -> lx.SubElement:  # "CHB E CDD 126 127"
        '''Build CHB.CHB.E.CDD.126/127 tape SubElement'''
        chamber_tapes_dict = CHAMBER_TYPES["2B"]["tapes"]["CHB E CDD 126 127"]
        width: float = chamber_tapes_dict["width"]
        height: float = chamber_tapes_dict["height"]
        length: float = chamber_tapes_dict["length"]
        inner_width = chamber_tapes_dict["inner_width"]
        inner_length = chamber_tapes_dict["inner_length"]
        doc = self.getDocument()
        
        starting_height: float = self._calculate_height_offset_for_tape("CHB E CDD 126 127")
        
        soft_block = self.create_simplified_block(width=width, length=length, height=height)
        hard_block = self.create_simplified_block(width=inner_width, length=inner_length, height=height)
        xWallThickness = (length - inner_length) * 0.5
        yWallThickness = (width - inner_width) * 0.5
        hard_block.translate(Geom.Vec(xWallThickness, yWallThickness, .0), Geom.CoordSpace_WCS)
        
        tape_base_with_hole: lx.SubElement = self.prepare_chamber(hardElement=hard_block, softElement=soft_block, return_elem_type=ElemTypeEnum.LX_SUB_ELEMENT)
        tape_base_with_hole.translate(
            Geom.Vec(
                -(length - CHAMBER_TYPES["2B"]["external_length"]) * 0.5,
                -(width - CHAMBER_TYPES["2B"]["external_width"]) * 0.5,
                starting_height
            ),
            Geom.CoordSpace_WCS
        )
        tape_base_with_hole.setDiffuseColor(Base.Color_fromCdwkColor(18))
        
        tape_1: lx.SubElement = self.create_simplified_block(
            width=inner_width + 0.08,
            length=inner_length * 0.5 + 0.04,
            height=0.02,
            return_elem_type=ElemTypeEnum.LX_SUB_ELEMENT
        )
        tape_2: lx.SubElement = self.create_simplified_block(
            width=inner_width + 0.08,
            length=inner_length * 0.5 + 0.04,
            height=0.02,
            return_elem_type=ElemTypeEnum.LX_SUB_ELEMENT
        )
        tape_1.translate(Geom.Vec(0.08, 0.08, starting_height + height), Geom.CoordSpace_WCS)
        tape_1.setDiffuseColor(Base.Color_fromCdwkColor(15))
        tape_2.translate(Geom.Vec(inner_length * 0.5 + 0.04 + 0.08, 0.08, starting_height + height), Geom.CoordSpace_WCS)
        tape_2.setDiffuseColor(Base.Color_fromCdwkColor(15))
        self.addSubElement(tape_1)
        self.addSubElement(tape_2)
        
        return tape_base_with_hole
  
    def create_tape_B125(self) -> lx.SubElement:  # "CHB E CDB 124 120N"
        '''Build CHB.E.CDB.124/120N tape SubElement'''
        chamber_tapes_dict = CHAMBER_TYPES["2B"]["tapes"]["CHB E CDB 124 120N"]
        chamber_length: float = CHAMBER_TYPES["2B"]["external_length"]
        width: float = chamber_tapes_dict["width"]
        height: float = chamber_tapes_dict["height"]
        length: float = chamber_tapes_dict["length"]
        inner_width = chamber_tapes_dict["inner_width"]
        inner_length = chamber_tapes_dict["inner_length"]
        doc = self.getDocument()
        
        starting_height: float = self._calculate_height_offset_for_tape("CHB E CDD 126 127")
        
        soft_block = self.create_simplified_block(width=width, length=length, height=height)
        hard_block = self.create_simplified_block(width=inner_width, length=inner_length, height=height)
        xWallThickness = (length - inner_length) * 0.5
        yWallThickness = (width - inner_width) * 0.5
        hard_block.translate(Geom.Vec(xWallThickness, yWallThickness, .0), Geom.CoordSpace_WCS)
        
        tape_base_with_hole: lx.SubElement = self.prepare_chamber(hardElement=hard_block, softElement=soft_block, return_elem_type=ElemTypeEnum.LX_SUB_ELEMENT)
        tape_base_with_hole.translate(Geom.Vec((chamber_length - length) * 0.5, -(width - CHAMBER_TYPES["2B"]["external_width"]) * 0.5, starting_height), Geom.CoordSpace_WCS)
        tape_base_with_hole.setDiffuseColor(Base.Color_fromCdwkColor(18))
        
        tape_1: lx.SubElement = self.create_simplified_block(
            width=inner_width + 0.08,
            length=inner_length * 0.5 + 0.04,
            height=0.02,
            return_elem_type=ElemTypeEnum.LX_SUB_ELEMENT
        )
        tape_2: lx.SubElement = self.create_simplified_block(
            width=inner_width + 0.08,
            length=inner_length * 0.5 + 0.04,
            height=0.02,
            return_elem_type=ElemTypeEnum.LX_SUB_ELEMENT
        )
        tape_1.translate(Geom.Vec(0.08, 0.08, starting_height + height), Geom.CoordSpace_WCS)
        tape_1.setDiffuseColor(Base.Color_fromCdwkColor(15))
        tape_2.translate(Geom.Vec(inner_length * 0.5 + 0.04 + 0.08, 0.08, starting_height + height), Geom.CoordSpace_WCS)
        tape_2.setDiffuseColor(Base.Color_fromCdwkColor(15))
        self.addSubElement(tape_1)
        self.addSubElement(tape_2)
        
        return tape_base_with_hole
    
    def create_tape_con_124_120(self) -> lx.SubElement:  # "CHB CON 124 120"
        '''Build CHB.CON.124/120 tape SubElement'''
        chamber_types_dict = CHAMBER_TYPES["2B"]["tapes"]["CHB CON 124 120"]
        width: float = chamber_types_dict["width"]
        height: float = chamber_types_dict["height"]
        length: float = chamber_types_dict["length"]
        inner_radius: float = chamber_types_dict["inner_diameter"] * 0.5
        
        chamber_length: float = CHAMBER_TYPES["2B"]["external_length"]
        chamber_width: float = CHAMBER_TYPES["2B"]["external_width"]
        
        anchor_height: float = self._calculate_height_offset_for_tape("CHB CON 124 120")
        
        # For creating such type of a tape we would need to create the pyramid element with straight base segment
        # and then cut it to flatten the top
        
        # Define the points of the pyramid
        pnt1 = Geom.Pnt(length * 0.5, - width * 0.5, .0)
        pnt2 = Geom.Pnt(-length * 0.5, - width * 0.5, .0)
        pnt3 = Geom.Pnt(-length * 0.5, width * 0.5, .0)
        pnt4 = Geom.Pnt(length * 0.5, width * 0.5, .0)
        
        pnt5 = Geom.Pnt(length * 0.5, - width * 0.5, 0.05)
        pnt6 = Geom.Pnt(-length * 0.5, - width * 0.5, 0.05)
        pnt7 = Geom.Pnt(-length * 0.5, width * 0.5, 0.05)
        pnt8 = Geom.Pnt(length * 0.5, width * 0.5, 0.05)
        
        # the pyramid top point
        pnt9 = Geom.Pnt(.0, .0, 0.74)
        
        model_assembler = FacetedModelAssembler(doc)
        model_assembler.beginModel()
        
        # bottom face
        model_assembler.beginFace()
        model_assembler.addVertexList([pnt1, pnt2, pnt3, pnt4])
        model_assembler.endFace()
        
        # front base face
        model_assembler.beginFace()
        model_assembler.addVertexList([pnt1, pnt4, pnt8, pnt5])
        model_assembler.endFace()
        
        # back base face
        model_assembler.beginFace()
        model_assembler.addVertexList([pnt7, pnt3, pnt2, pnt6])
        model_assembler.endFace()
        
        # left base face
        model_assembler.beginFace()
        model_assembler.addVertexList([pnt1, pnt5, pnt6, pnt2])
        model_assembler.endFace()
        
        # right base face
        model_assembler.beginFace()
        model_assembler.addVertexList([pnt4, pnt3, pnt7, pnt8])
        model_assembler.endFace()
        
        # front triangular face
        model_assembler.beginFace()
        model_assembler.addVertexList([pnt5, pnt8, pnt9])
        model_assembler.endFace()
        
        # left triangular face
        model_assembler.beginFace()
        model_assembler.addVertexList([pnt6, pnt5, pnt9])
        model_assembler.endFace()
        
        # back triangular face
        model_assembler.beginFace()
        model_assembler.addVertexList([pnt7, pnt6, pnt9])
        model_assembler.endFace()
        
        # right triangular face
        model_assembler.beginFace()
        model_assembler.addVertexList([pnt8, pnt7, pnt9])
        model_assembler.endFace()
        
        geometry = model_assembler.endModel()
        pyramid_element = lx.Element.createIn(doc)
        pyramid_element.setGeometry(geometry)
        
        hard_block: lx.Element = self.create_simplified_block(
            width=width,
            length=length,
            height=width,
            return_elem_type=ElemTypeEnum.LX_ELEMENT
        )
        hard_block.translate(Geom.Vec(-length * 0.5, -width * 0.5, height), Geom.CoordSpace_WCS)
        
        # cutting two objects
        resultingBlocks = lx.vector_Element()
        if lx.bop_cut(pyramid_element, hard_block, resultingBlocks) != 0:
            print("Error: bop_cut failed")
        
        doc.removeObject(pyramid_element)
        doc.removeObject(hard_block)

        transform = resultingBlocks[0].getTransform()
        geometry = resultingBlocks[0].getGeometry()
        pyramid_element1 = lx.Element.createIn(doc)
        pyramid_element1.setTransform(transform)
        pyramid_element1.setGeometry(geometry)
        
        # Create cylinder element to cut through the pyramid
        internCylinder = lx.RightCircularCylinder.createIn(doc)
        internCylinder.setHeight(.50)
        internCylinder.setRadius(inner_radius)
        intElement = lx.Element.createIn(doc)
        intElement.setGeometry(internCylinder)
        
        # cutting two objects
        resultingBlocks = lx.vector_Element()
        if lx.bop_cut(pyramid_element1, intElement, resultingBlocks) != 0:
            print("Error: bop_cut failed")
        
        doc.removeObject(pyramid_element1)
        doc.removeObject(intElement)

        transform = resultingBlocks[0].getTransform()
        geometry = resultingBlocks[0].getGeometry()
        final_element = lx.SubElement.createIn(doc)
        final_element.setTransform(transform)
        final_element.setGeometry(geometry)
        
        final_element.translate(Geom.Vec(chamber_length * 0.5, chamber_width * 0.5, anchor_height), Geom.CoordSpace_WCS)
        final_element.setDiffuseColor(Base.Color_fromCdwkColor(18))
        
        return final_element

    def create_tape_chb_cvt_10(self) -> lx.SubElement: # CHB.CV.T10.120/030
        def prepare_single_cvt10_tape_sub_element() -> lx.SubElement:
            '''Build CHB.CV.T10.120/030 tape SubElement'''
            chamber_tapes_dict = CHAMBER_TYPES["2B"]["tapes"]["CHB CV T10 120 030"]
            width: float = chamber_tapes_dict["width"]
            height: float = chamber_tapes_dict["height"]
            length: float = chamber_tapes_dict["length"]
            doc = self.getDocument()
            
            # Create the base soft block using the parameters
            soft_block = self.create_simplified_block(width=width, length=length, height=height)
            # Next we would need two hard blocks to cut the handles
            hard_block1 = self.create_simplified_block(width=0.10, length=0.10, height=0.05)
            hard_block2 = self.create_simplified_block(width=0.10, length=0.10, height=0.05)
            hard_block1.translate(Geom.Vec(0.10, 0.0, 0.0), Geom.CoordSpace_WCS)
            hard_block2.translate(Geom.Vec(0.10, width - 0.10, 0.0), Geom.CoordSpace_WCS)
            
            # cutting two objects
            resulting_elements1 = lx.vector_Element()
            resulting_elements2 = lx.vector_Element()
            if lx.bop_cut(soft_block, hard_block1, resulting_elements1) != 0:
                print("Error: bop_cut failed")
            
            if lx.bop_cut(resulting_elements1[0], hard_block2, resulting_elements2) != 0:
                print("Error: bop_cut failed")
            
            doc.removeObject(hard_block1)
            doc.removeObject(hard_block2)
            doc.removeObject(soft_block)

            transform = resulting_elements2[0].getTransform()
            geometry = resulting_elements2[0].getGeometry()
            
            cvt10_tape_element = lx.SubElement.createIn(doc)
            cvt10_tape_element.setTransform(transform)
            cvt10_tape_element.setGeometry(geometry)
            
            return cvt10_tape_element
        
        doc = self.getDocument()
        starting_height: float = self._calculate_height_offset_for_tape("CHB CV T10 120 030")
        centering_offset: float = 0.02
        length_offset: float = 0.0
        for elem in range(0, 4):
            tape_element = prepare_single_cvt10_tape_sub_element()
            tape_element.translate(Geom.Vec(length_offset + centering_offset, 0.0, starting_height), Geom.CoordSpace_WCS)
            length_offset += 0.30
            self.addSubElement(tape_element)
      
    def create_tape_chb_cvt_25(self) -> lx.SubElement: # CHB.CV.T25.120/030
        def prepare_single_cvt25_tape_sub_element() -> lx.SubElement:
            '''Build CHB.CV.T25.120/030 tape SubElement'''
            chamber_tapes_dict = CHAMBER_TYPES["2B"]["tapes"]["CHB CV T25 120 030"]
            width: float = chamber_tapes_dict["width"]
            height: float = chamber_tapes_dict["height"]
            length: float = chamber_tapes_dict["length"]
            doc = self.getDocument()
            
            # Create the base soft block using the parameters
            soft_block = self.create_simplified_block(width=width, length=length, height=height)
            # Next we would need two hard blocks to cut the handles
            hard_block1 = self.create_simplified_block(width=0.10, length=0.10, height=0.075)
            hard_block2 = self.create_simplified_block(width=0.10, length=0.10, height=0.075)
            hard_block1.translate(Geom.Vec(0.10, 0.0, 0.025), Geom.CoordSpace_WCS)
            hard_block2.translate(Geom.Vec(0.10, width - 0.10, 0.025), Geom.CoordSpace_WCS)
            
            # cutting two objects
            resulting_elements1 = lx.vector_Element()
            resulting_elements2 = lx.vector_Element()
            if lx.bop_cut(soft_block, hard_block1, resulting_elements1) != 0:
                print("Error: bop_cut failed")
            
            if lx.bop_cut(resulting_elements1[0], hard_block2, resulting_elements2) != 0:
                print("Error: bop_cut failed")

            # For creating such type of a tape we would need to create the pyramid element with straight base segment
            # and then cut it to flatten the top
            
            # Define the points of the pyramid
            pnt1 = Geom.Pnt(length / 2, -width / 4, 0.0)
            pnt2 = Geom.Pnt(length / 2, width / 4, 0.0)
            pnt3 = Geom.Pnt(-length / 2, width / 4, 0.0)
            pnt4 = Geom.Pnt(-length / 2, -width / 4, 0.0)
            
            pnt5 = Geom.Pnt(length / 2, -width / 4, -0.03)
            pnt6 = Geom.Pnt(-length / 2, -width / 4, -0.03)
            
            # the cheese-like top object        
            model_assembler = FacetedModelAssembler(doc)
            model_assembler.beginModel()
            
            # top face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt1, pnt2, pnt3, pnt4])
            model_assembler.endFace()
            
            # back face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt1, pnt4, pnt6, pnt5])
            model_assembler.endFace()
            
            # left face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt1, pnt5, pnt2])
            model_assembler.endFace()
            
            # right face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt3, pnt4, pnt6])
            model_assembler.endFace()
            
            # bottom face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt2, pnt5, pnt6, pnt3])
            model_assembler.endFace()
            
            geometry = model_assembler.endModel()
            bend_cut_element1 = lx.Element.createIn(doc)
            bend_cut_element2 = lx.Element.createIn(doc)
            bend_cut_element1.setGeometry(geometry)
            bend_cut_element2.setGeometry(geometry)
            
            bend_cut_element1.translate(Geom.Vec(length / 2, width / 4, height), Geom.CoordSpace_WCS)
            bend_cut_element2.translate(Geom.Vec(-length / 2, -width / 2 -width / 4, height), Geom.CoordSpace_WCS)
            rotate_axis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))
            bend_cut_element2.rotate(rotate_axis, math.radians(180), Geom.CoordSpace_WCS)
            
            resulting_elements3 = lx.vector_Element()
            resulting_elements4 = lx.vector_Element()
            if lx.bop_cut(resulting_elements2[0], bend_cut_element1, resulting_elements3) != 0:
                print("Error: bop_cut failed")
            
            if lx.bop_cut(resulting_elements3[0], bend_cut_element2, resulting_elements4) != 0:
                print("Error: bop_cut failed")
            
            doc.removeObject(hard_block1)
            doc.removeObject(hard_block2)
            doc.removeObject(soft_block)
            doc.removeObject(bend_cut_element1)
            doc.removeObject(bend_cut_element2)

            final_transform = resulting_elements4[0].getTransform()
            final_geometry = resulting_elements4[0].getGeometry()
            
            cvt25_tape_element = lx.SubElement.createIn(doc)
            cvt25_tape_element.setTransform(final_transform)
            cvt25_tape_element.setGeometry(final_geometry)
            
            return cvt25_tape_element

        doc = self.getDocument()
        starting_height: float = self._calculate_height_offset_for_tape("CHB CV T25 120 030")
        centering_offset: float = 0.02
        length_offset: float = 0.0
        for elem in range(0, 4):
            tape_element = prepare_single_cvt25_tape_sub_element()
            tape_element.translate(Geom.Vec(length_offset + centering_offset, 0.0, starting_height), Geom.CoordSpace_WCS)
            length_offset += 0.30
            self.addSubElement(tape_element)
    
    def create_tape_chb_cvt_60(self) -> lx.SubElement: # CHB.CV.T60.120/030
        def prepare_single_cvt60_tape_sub_element() -> lx.SubElement:
            '''Build CHB.CV.T60.120/030 tape SubElement'''
            chamber_tapes_dict = CHAMBER_TYPES["2B"]["tapes"]["CHB CV T60 120 030"]
            width: float = chamber_tapes_dict["width"]
            height: float = chamber_tapes_dict["height"]
            length: float = chamber_tapes_dict["length"]
            doc = self.getDocument()
            
            # Create the base soft block using the parameters
            soft_block = self.create_simplified_block(width=width, length=length, height=height)
            # Next we would need two hard blocks to cut the handles
            hard_block1 = self.create_simplified_block(width=0.10, length=0.10, height=0.075)
            hard_block2 = self.create_simplified_block(width=0.10, length=0.10, height=0.075)
            hard_block1.translate(Geom.Vec(0.10, 0.0, 0.025), Geom.CoordSpace_WCS)
            hard_block2.translate(Geom.Vec(0.10, width - 0.10, 0.025), Geom.CoordSpace_WCS)
            
            # cutting two objects
            resulting_elements1 = lx.vector_Element()
            resulting_elements2 = lx.vector_Element()
            if lx.bop_cut(soft_block, hard_block1, resulting_elements1) != 0:
                print("Error: bop_cut failed")
            
            if lx.bop_cut(resulting_elements1[0], hard_block2, resulting_elements2) != 0:
                print("Error: bop_cut failed")

            # For creating such type of a tape we would need to create the pyramid element with straight base segment
            # and then cut it to flatten the top
            
            # Define the points of the pyramid
            pnt1 = Geom.Pnt(length / 2, -width / 4, 0.0)
            pnt2 = Geom.Pnt(length / 2, width / 4 - 0.1, 0.0)
            pnt3 = Geom.Pnt(-length / 2, width / 4 - 0.1, 0.0)
            pnt4 = Geom.Pnt(-length / 2, -width / 4, 0.0)
            
            pnt5 = Geom.Pnt(length / 2, -width / 4, -0.045)
            pnt6 = Geom.Pnt(-length / 2, -width / 4, -0.045)
            
            # the cheese-like top object        
            model_assembler = FacetedModelAssembler(doc)
            model_assembler.beginModel()
            
            # top face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt1, pnt2, pnt3, pnt4])
            model_assembler.endFace()
            
            # back face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt1, pnt4, pnt6, pnt5])
            model_assembler.endFace()
            
            # left face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt1, pnt5, pnt2])
            model_assembler.endFace()
            
            # right face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt3, pnt4, pnt6])
            model_assembler.endFace()
            
            # bottom face
            model_assembler.beginFace()
            model_assembler.addVertexList([pnt2, pnt5, pnt6, pnt3])
            model_assembler.endFace()
            
            geometry = model_assembler.endModel()
            bend_cut_element1 = lx.Element.createIn(doc)
            bend_cut_element2 = lx.Element.createIn(doc)
            bend_cut_element1.setGeometry(geometry)
            bend_cut_element2.setGeometry(geometry)
            
            bend_cut_element1.translate(Geom.Vec(length / 2, width / 4, height), Geom.CoordSpace_WCS)
            bend_cut_element2.translate(Geom.Vec(-length / 2, -width / 2 -width / 4, height), Geom.CoordSpace_WCS)
            rotate_axis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))
            bend_cut_element2.rotate(rotate_axis, math.radians(180), Geom.CoordSpace_WCS)
            
            resulting_elements3 = lx.vector_Element()
            resulting_elements4 = lx.vector_Element()
            if lx.bop_cut(resulting_elements2[0], bend_cut_element1, resulting_elements3) != 0:
                print("Error: bop_cut failed")
            
            if lx.bop_cut(resulting_elements3[0], bend_cut_element2, resulting_elements4) != 0:
                print("Error: bop_cut failed")
            
            doc.removeObject(hard_block1)
            doc.removeObject(hard_block2)
            doc.removeObject(soft_block)
            doc.removeObject(bend_cut_element1)
            doc.removeObject(bend_cut_element2)

            final_transform = resulting_elements4[0].getTransform()
            final_geometry = resulting_elements4[0].getGeometry()
            
            cvt25_tape_element = lx.SubElement.createIn(doc)
            cvt25_tape_element.setTransform(final_transform)
            cvt25_tape_element.setGeometry(final_geometry)
            
            return cvt25_tape_element

        def prepare_two_handles_for_cvt60_tapes() -> Tuple[lx.SubElement]:
            '''Build CHB.CV.T60.120/030 tape SubElement'''
            chamber_tapes_dict = CHAMBER_TYPES["2B"]["tapes"]["CHB CV T60 120 030"]
            width: float = chamber_tapes_dict["width"]
            height: float = chamber_tapes_dict["height"]
            length: float = chamber_tapes_dict["length"]
            doc = self.getDocument()
            
            rotation_axis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 1, 0))
            
            cylinder1 = lx.RightCircularCylinder.createIn(doc)
            cylinder1.setHeight(0.10)
            cylinder1.setRadius(0.01)
            cylinder_sub_element1 = lx.SubElement.createIn(doc)
            cylinder_sub_element1.setGeometry(cylinder1)
            cylinder_sub_element1.rotate(rotation_axis, math.radians(90), Geom.CoordSpace_WCS)
            cylinder_sub_element1.translate(Geom.Vec(0.10, 0.05, 0.06), Geom.CoordSpace_WCS)
            cylinder_sub_element1.setDiffuseColor(Base.Color_fromCdwkColor(110))
            
            cylinder2 = lx.RightCircularCylinder.createIn(doc)
            cylinder2.setHeight(0.10)
            cylinder2.setRadius(0.01)
            cylinder_sub_element2 = lx.SubElement.createIn(doc)
            cylinder_sub_element2.setGeometry(cylinder2)
            cylinder_sub_element2.rotate(rotation_axis, math.radians(90), Geom.CoordSpace_WCS)
            cylinder_sub_element2.translate(Geom.Vec(0.10, width - 0.05, 0.06), Geom.CoordSpace_WCS)
            cylinder_sub_element2.setDiffuseColor(Base.Color_fromCdwkColor(110))
            
            return cylinder_sub_element1, cylinder_sub_element2
        
        doc = self.getDocument()
        starting_height: float = self._calculate_height_offset_for_tape("CHB CV T60 120 030")
        centering_offset: float = 0.02
        length_offset: float = 0.0
        for elem in range(0, 4):
            tape_element = prepare_single_cvt60_tape_sub_element()
            handle1, handle2 = prepare_two_handles_for_cvt60_tapes()
            translation_vec = Geom.Vec(length_offset + centering_offset, 0.0, starting_height)
            tape_element.translate(translation_vec, Geom.CoordSpace_WCS)
            handle1.translate(translation_vec, Geom.CoordSpace_WCS)
            handle2.translate(translation_vec, Geom.CoordSpace_WCS)
            length_offset += 0.30
            self.addSubElement(tape_element)
            self.addSubElement(handle1)
            self.addSubElement(handle2)
    
    def _createGeometry(self)  -> None:
        doc = self.getDocument()
        external_length: float = CHAMBER_TYPES["2B"]["external_length"]
        internal_length: float = CHAMBER_TYPES["2B"]["internal_length"]
        external_width: float = CHAMBER_TYPES["2B"]["external_width"]
        internal_width: float = CHAMBER_TYPES["2B"]["internal_width"]
        bottom_height: float = CHAMBER_TYPES["2B"]["bottom_height"]
        show_bottom: bool = self._showBottom.getValue()
        
        current_height_param: float = self._heights.getValue()
        # convert dict keys to list
        height_param_height_type = list(CHAMBER_TYPES["2B"]["heights"].keys())[current_height_param]
        height = CHAMBER_TYPES["2B"]["heights"][height_param_height_type]
        
        # check if all variables have value and are not None
        if all([external_length, internal_length, external_width, internal_width, height]):
            soft_block = self.create_simplified_block(width=external_width, length=external_length, height=height)
            hard_block = self.create_simplified_block(width=internal_width, length=internal_length, height=height)
            xWallThickness = (external_length - internal_length) * 0.5
            yWallThickness = (external_width - internal_width) * 0.5
            hard_block.translate(Geom.Vec(xWallThickness, yWallThickness, .0), Geom.CoordSpace_WCS)
            cut_chamber: lx.Element = self.prepare_chamber(hardElement=hard_block, softElement=soft_block)
            cut_chamber_with_niches: lx.SubElement = self.carveTheNichesInChamber(cut_chamber)
            # if success in the niches carving - remove object
            doc.removeObject(cut_chamber)
            
            if show_bottom:
                cut_chamber_with_niches.translate(Geom.Vec(0, 0, bottom_height), Geom.CoordSpace_WCS)
                bottom = self.createBottom(width=external_width, length=external_length, height=bottom_height)
                self.addSubElement(bottom)
            
            tape_type: str = self._get_tape_type_string()
            
            if tape_type == "CHB E CDB 124 120N":
                tape = self.create_tape_B125()
                self.addSubElement(tape)
            elif tape_type == "CHB E CDD 126 127":
                tape = self.create_tape_B400()
                self.addSubElement(tape)
            elif tape_type == "CHB CON 124 120":
                tape = self.create_tape_con_124_120()
                self.addSubElement(tape)
            elif tape_type == "CHB CV T10 120 030":
                self.create_tape_chb_cvt_10()
            elif tape_type == "CHB CV T25 120 030":
                self.create_tape_chb_cvt_25()
            elif tape_type == "CHB CV T60 120 030":
                self.create_tape_chb_cvt_60()
            else:
                return NotImplementedError()

            self.addSubElement(cut_chamber_with_niches)
        else:
            raise Exception("Some of the parameter variables are None")

    def _updateGeometry(self):
        doc = self.getDocument()

        with EditMode(doc):
            self.removeSubElements()
            self._createGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == DistributionChamber2B._tapeTypePropName:
            self.setTapeType(self._tapeType.getValue())
        elif aPropertyName == DistributionChamber2B._heightsPropName:
            self.setHeights(self._heights.getValue())
        elif aPropertyName == DistributionChamber2B._showBottomPropName:
            self.setShowBottom(self._showBottom.getValue())

    def onScaling(self, aVec, aScaleBasePnt):
        doc.beginEditing()
        self.translateAfterScaled(aVec, aScaleBasePnt)
        doc.endEditing()
        doc.recompute()


if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{501BD7DB-9424-40A3-B4EC-61A82219E955}"))

    try:
        compound = DistributionChamber2B(doc)
        # lx.setNewComponentByColorAndName(CW_COLOR, Base.StringTool.toString("distribution_chamber2B"), compound)
        compound.setDiffuseColor(Base.Color_fromCdwkColor(CW_COLOR))
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
        else:
            pos = Geom.Ax2(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))

        compound.setLocalPlacement(pos)
    except Exception as e:
        traceback.print_exc()
    finally:
        doc.recompute()
