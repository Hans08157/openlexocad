import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import traceback, math, time

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

def qstr(str):
    return Base.StringTool.toQString(lxstr(str))

# Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))

def getSkriptsFolder():
    pathString = cstr(lxstr(Core.Settings.getInstance().getCurrentScriptFilePath()))
    # print "path:", pathStr
    st = pathString.split("/")
    st_new = st[0] + "/"
    for i in range(1, len(st) - 1):
        st_new += st[i] + "/"
    st_new += "excavatorData/"
    return st_new

def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


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

class ExcavatorPart(lx.SubElement):
    partName = "Name"

    def getGlobalClassId(self):
        return Base.GlobalId("{1359ff94-490a-488b-805e-9212457a772e}")

    def __init__(self, doc):
        lx.SubElement.__init__(self, doc)
        self.registerPythonClass("TrackPart", "OpenLxApp.SubElement")

        self.type = self.registerPropertyString(self.partName, lxstr(""), lx.Property.NOT_VISIBLE, \
                                                lx.Property.NOT_EDITABLE, -1)  # NOT_VISIBLE

        self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())

    def setPartData(self, name):
        self.type.setValue(lxstr(name))

    def getPartData(self):
        return cstr(self.type.getValue())

class ExcavatorData:
    def __init__(self):
        self._bodyAngle = 0.0
        self._firstArrowAngle = 0.0
        self._secondArrowAngle = 0.0
        self._scoopAngle = 0.0

        self.xDirFrontPart = Geom.Dir(1, 0, 0)
        self.yDirFrontPart = Geom.Dir(0, 1, 0)

        self.trsfBase = None
        self.trsfHead = None
        self.trsfFirstArrow = None
        self.trsfSecondArrow = None
        self.trsfFirstCylinder = None
        self.trsfSecondCylinder = None
        self.trsfThreethCylinder = None
        self.trsfFirstPiston = None
        self.trsfSecondPiston = None
        self.trsfThreethPiston = None
        self.trsfLever = None
        self.trsfScoop = None

    def getTrsfBase(self):
        return self.trsfBase

    def getTrsfHead(self):
        return self.trsfHead

    def getTrsfFirstArrow(self):
        return self.trsfFirstArrow

    def getTrsfSecondArrow(self):
        return self.trsfSecondArrow

    def getTrsfFirstCylinder(self):
        return self.trsfFirstCylinder

    def getTrsfSecondCylinder(self):
        return self.trsfSecondCylinder

    def getTrsfThreethCylinder(self):
        return self.trsfThreethCylinder

    def getTrsfFirstPiston(self):
        return self.trsfFirstPiston

    def getTrsfSecondPiston(self):
        return self.trsfSecondPiston

    def getTrsfThreethPiston(self):
        return self.trsfThreethPiston

    def getTrsfLever(self):
        return self.trsfLever

    def getTrsfScoop(self):
        return self.trsfScoop

    def setBodyAngle(self, angleBody):
        self._angleBody = angleBody

    def setFirstArrowAngle(self, param):
        self._firstArrowAngle = param

    def setSecondArrowAngle(self, param):
        self._secondArrowAngle = param

    def setScoopAngle(self, param):
        self._scoopAngle = param

    @staticmethod
    def fiendCirclesIntersection(x0, y0, x1, y1, r0, r1, d):
        print("x1: ", x0)
        print("y1: ", y0)
        print("x2: ", x1)
        print("y2: ", y1)
        print("r1: ", r0)
        print("r2: ", r1)

        a = (math.pow(r0, 2) - math.pow(r1, 2) + math.pow(d, 2)) / (2*d)
        h = math.sqrt(math.fabs(math.pow(r0, 2) - math.pow(a, 2)))
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d

        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d
        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        return x3, y3, x4, y4

    def rotateBody(self):
        centerBody = Geom.Pnt(-0.00727,0.00158, 0.0)
        angle = math.radians(self._angleBody)
        zAxis = Geom.Ax1(centerBody, Geom.Dir(0, 0, 1))
        t_r = Geom.Trsf()
        t_r.setRotation(zAxis, angle)

        trsfFront = t_r

        self.trsfHead = trsfFront
        self.trsfFirstArrow = trsfFront
        self.trsfSecondArrow = trsfFront
        self.trsfFirstCylinder = trsfFront
        self.trsfSecondCylinder = trsfFront
        self.trsfThreethCylinder = trsfFront
        self.trsfFirstPiston = trsfFront
        self.trsfSecondPiston = trsfFront
        self.trsfThreethPiston = trsfFront
        self.trsfLever = trsfFront
        self.trsfScoop = trsfFront

    def firstArrowRotate(self):
        firstArrowWithBody = Geom.Pnt(0.0, -0.89377412, 0.91764954)
        xAxisForFirstArrow = Geom.Ax1(firstArrowWithBody, Geom.Dir(1.0, 0.0, 0.0))
        t_r = Geom.Trsf()
        t_r.setRotation(xAxisForFirstArrow, math.radians(-self._firstArrowAngle))
        trsfFirstArrow = t_r

        firstCylinderWithBody = Geom.Pnt(0.0, -1.05804825, 0.67702299)
        firstPistonWithFirstArrow = Geom.Pnt(0.0, -1.67243516, 1.53048170)
        firstPistonWithFirstArrowEnd = firstPistonWithFirstArrow.rotated(xAxisForFirstArrow, math.radians(-self._firstArrowAngle))

        middleFirstCylinderAndPiston = Geom.Pnt(0.0, -1.46626401, 1.24178720)

        firstCylinderVec = Geom.Vec(firstCylinderWithBody, firstPistonWithFirstArrow)
        firstCylinderVecEnd = Geom.Vec(firstCylinderWithBody, firstPistonWithFirstArrowEnd)

        print("First cylinder angle", firstCylinderVec.angle(firstCylinderVecEnd))

        xAxisForFirstCylinder = Geom.Ax1(firstCylinderWithBody, Geom.Dir(1.0, 0.0, 0.0))
        t_r_c = Geom.Trsf()
        if self._firstArrowAngle > 0.0:
            t_r_c.setRotation(xAxisForFirstCylinder, -firstCylinderVec.angle(firstCylinderVecEnd))
            middleFirstCylinderAndPistonEnd = middleFirstCylinderAndPiston.rotated(xAxisForFirstCylinder, -firstCylinderVec.angle(firstCylinderVecEnd))
            trsfForFirstCylinder = t_r_c
        else:
            t_r_c.setRotation(xAxisForFirstCylinder, firstCylinderVec.angle(firstCylinderVecEnd))
            middleFirstCylinderAndPistonEnd = middleFirstCylinderAndPiston.rotated(xAxisForFirstCylinder, firstCylinderVec.angle(firstCylinderVecEnd))

            trsfForFirstCylinder = t_r_c

        xAxisForFirstPiston = Geom.Ax1(firstPistonWithFirstArrowEnd, Geom.Dir(1.0, 0.0, 0.0))

        firstCylinderWithFirstPistonVec = Geom.Vec(firstPistonWithFirstArrow, middleFirstCylinderAndPiston)
        firstCylinderWithFirstPistonVecEnd = Geom.Vec(firstPistonWithFirstArrowEnd, middleFirstCylinderAndPistonEnd)

        t_r_p = Geom.Trsf()
        if self._firstArrowAngle > 0.0:
            t_r_p.setRotation(xAxisForFirstPiston, -firstCylinderWithFirstPistonVec.angle(firstCylinderWithFirstPistonVecEnd))
        else:
            t_r_p.setRotation(xAxisForFirstPiston, firstCylinderWithFirstPistonVec.angle(firstCylinderWithFirstPistonVecEnd))
        trsfForFirstPiston = t_r_p
        print("First piston angle: ", -firstCylinderWithFirstPistonVec.angle(firstCylinderWithFirstPistonVecEnd))

        translateFirstPiston = Geom.Trsf()
        translateFirstPiston.setTranslation(Geom.Vec(firstPistonWithFirstArrow, firstPistonWithFirstArrowEnd))

        self.trsfFirstArrow = self.trsfFirstArrow * trsfFirstArrow
        self.trsfSecondArrow = self.trsfSecondArrow * trsfFirstArrow
        self.trsfFirstCylinder = self.trsfFirstCylinder * trsfForFirstCylinder
        self.trsfSecondCylinder = self.trsfSecondCylinder * trsfFirstArrow
        self.trsfThreethCylinder = self.trsfThreethCylinder * trsfFirstArrow
        self.trsfFirstPiston = self.trsfFirstPiston * trsfForFirstPiston * translateFirstPiston
        self.trsfSecondPiston = self.trsfSecondPiston * trsfFirstArrow
        self.trsfThreethPiston = self.trsfThreethPiston * trsfFirstArrow
        self.trsfLever = self.trsfLever * trsfFirstArrow
        self.trsfScoop = self.trsfScoop * trsfFirstArrow

    def secondArrowRotate(self):

        firstArrowWithSecondArrow = Geom.Pnt(0.0, -2.81563616, 1.57771146)
        xAxisForSecondArrow = Geom.Ax1(firstArrowWithSecondArrow, Geom.Dir(1.0, 0.0, 0.0))
        t_r = Geom.Trsf()
        t_r.setRotation(xAxisForSecondArrow, math.radians(-self._secondArrowAngle))
        trsfSecondArrow = t_r

        secondCylinderWithFirstArrow = Geom.Pnt(0.0, -1.73984981, 1.89544249)
        secondPistonWithSecondArrow = Geom.Pnt(0.0, -3.00106621, 1.83174610)
        secondPistonWithSecondArrowEnd = secondPistonWithSecondArrow.rotated(xAxisForSecondArrow, math.radians(-self._secondArrowAngle))

        middleSecondCylinderAndPiston = Geom.Pnt(0.0, -2.45603466, 1.86038828)

        secondCylinderVec = Geom.Vec(secondCylinderWithFirstArrow, secondPistonWithSecondArrow)
        secondCylinderVecEnd = Geom.Vec(secondCylinderWithFirstArrow, secondPistonWithSecondArrowEnd)

        print("Second cylinder angle", secondCylinderVec.angle(secondCylinderVecEnd))

        xAxisForSecondCylinder = Geom.Ax1(secondCylinderWithFirstArrow, Geom.Dir(1.0, 0.0, 0.0))
        t_r_c = Geom.Trsf()
        if self._secondArrowAngle > 0.0:
            t_r_c.setRotation(xAxisForSecondCylinder, -secondCylinderVec.angle(secondCylinderVecEnd))
            middleFirstCylinderAndPistonEnd = middleSecondCylinderAndPiston.rotated(xAxisForSecondCylinder, -secondCylinderVec.angle(secondCylinderVecEnd))
        else:
            t_r_c.setRotation(xAxisForSecondCylinder, secondCylinderVec.angle(secondCylinderVecEnd))
            middleFirstCylinderAndPistonEnd = middleSecondCylinderAndPiston.rotated(xAxisForSecondCylinder, secondCylinderVec.angle(secondCylinderVecEnd))
        trsfForSecondCylinder = t_r_c

        xAxisForSecondPiston = Geom.Ax1(secondPistonWithSecondArrow, Geom.Dir(1.0, 0.0, 0.0))

        secondCylinderWithSecondPistonVec = Geom.Vec(secondPistonWithSecondArrow, middleSecondCylinderAndPiston)
        secondCylinderWithSecondPistonVecEnd = Geom.Vec(secondPistonWithSecondArrowEnd, middleFirstCylinderAndPistonEnd)

        t_r_p = Geom.Trsf()
        if self._secondArrowAngle > 0.0:
            t_r_p.setRotation(xAxisForSecondPiston, -secondCylinderWithSecondPistonVec.angle(secondCylinderWithSecondPistonVecEnd))
        else:
            t_r_p.setRotation(xAxisForSecondPiston, secondCylinderWithSecondPistonVec.angle(secondCylinderWithSecondPistonVecEnd))
        trsfForSecondPiston = t_r_p
        print("First piston angle: ", -secondCylinderWithSecondPistonVec.angle(secondCylinderWithSecondPistonVecEnd))

        translateFirstPiston = Geom.Trsf()
        translateFirstPiston.setTranslation(Geom.Vec(secondPistonWithSecondArrow, secondPistonWithSecondArrowEnd))

        self.trsfSecondArrow = self.trsfSecondArrow * trsfSecondArrow
        self.trsfSecondCylinder = self.trsfSecondCylinder * trsfForSecondCylinder
        self.trsfThreethCylinder = self.trsfThreethCylinder * trsfSecondArrow
        self.trsfSecondPiston = self.trsfSecondPiston * translateFirstPiston * trsfForSecondPiston
        self.trsfThreethPiston = self.trsfThreethPiston * trsfSecondArrow
        self.trsfLever = self.trsfLever * trsfSecondArrow
        self.trsfScoop = self.trsfScoop * trsfSecondArrow

    def rotateScoop(self):
        threeCylinderWithSecondArrow = Geom.Pnt(0.0, -2.93304777, 1.39739954)

        leverWithSecondArrow = Geom.Pnt(0.0, -2.43478429, 0.64846504)
        leverWithThreePiston = Geom.Pnt(0.0, -2.65496578, 0.55384642)
        leverWithScoop = Geom.Pnt(0.0, -2.52107334, 0.39257106)


        xAxisForLever = Geom.Ax1(leverWithSecondArrow, Geom.Dir(1.0, 0.0, 0.0))
        t_r = Geom.Trsf()
        t_r.setRotation(xAxisForLever, math.radians(-self._scoopAngle))
        trsfLever = t_r

        leverWithThreePistonEnd = leverWithThreePiston.rotated(xAxisForLever, math.radians(-self._scoopAngle))
        leverWithScoopEnd = leverWithScoop.rotated(xAxisForLever, -self._scoopAngle)

        threeCylinderWithThreePistonVecEnd = Geom.Vec(leverWithThreePistonEnd, threeCylinderWithSecondArrow)

        threeCylinderVec = Geom.Vec(threeCylinderWithSecondArrow, leverWithThreePiston)
        threeCylinderVecEnd = Geom.Vec(threeCylinderWithSecondArrow, leverWithThreePistonEnd)




        print("Three cylinder angle", threeCylinderVec.angle(threeCylinderVecEnd))

        xAxisForThreeCylinder = Geom.Ax1(threeCylinderWithSecondArrow, Geom.Dir(1.0, 0.0, 0.0))
        t_r_c = Geom.Trsf()
        if self._scoopAngle > 0.0:
            t_r_c.setRotation(xAxisForThreeCylinder, threeCylinderVec.angle(threeCylinderVecEnd))
        else:
            t_r_c.setRotation(xAxisForThreeCylinder, threeCylinderVec.angle(threeCylinderVecEnd))
        trsfForThreeCylinder = t_r_c



        translateFirstPiston = Geom.Trsf()
        translateFirstPiston.setTranslation(Geom.Vec(leverWithThreePiston, leverWithThreePistonEnd))



        threeCylinderWithThreePistonVec = Geom.Vec(leverWithThreePiston.translated(Geom.Vec(leverWithThreePiston, leverWithThreePistonEnd)), threeCylinderWithSecondArrow)

        xAxisForThreePiston = Geom.Ax1(leverWithThreePistonEnd, Geom.Dir(1.0, 0.0, 0.0))

        sideOfPiston = Geom.Pnt(0.0, -2.80345750, 1.03524411)
        sideOfPistonEnd = sideOfPiston.rotated(xAxisForLever, math.radians(self._scoopAngle))


        firstVecForPiston = Geom.Vec(leverWithThreePiston, sideOfPiston)
        secondVecForPiston = Geom.Vec(leverWithThreePistonEnd, threeCylinderWithSecondArrow)

        t_r_p = Geom.Trsf()
        if self._scoopAngle > 0.0:
            t_r_p.setRotation(xAxisForThreePiston, firstVecForPiston.angle(secondVecForPiston))
        else:
            t_r_p.setRotation(xAxisForThreePiston, firstVecForPiston.angle(secondVecForPiston))
        trsfForThreePiston = t_r_p
        print("Three piston angle: ", -threeCylinderWithThreePistonVec.angle(threeCylinderWithThreePistonVecEnd))




        self.trsfThreethCylinder = self.trsfThreethCylinder * trsfForThreeCylinder
        self.trsfThreethPiston = self.trsfThreethPiston * trsfForThreePiston * translateFirstPiston
        self.trsfLever = self.trsfLever * trsfLever
        self.trsfScoop = self.trsfScoop * trsfLever


class Excavator(lx.Element):
    _color = Base.Color(255, 214, 0)

    def getGlobalClassId(self):
        return Base.GlobalId("{FDF089F2-8F63-474A-9DAB-92D193EF80CD}")

    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Excavator", "OpenLxApp.Element")

        # Register properties
        self.setPropertyHeader(lxstr("Excavator"), -1)
        self.setPropertyGroupName(lxstr("Excavator"), -1)

        self._bodyAngle = self.registerPropertyDouble("Body angle", 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._firstArrowAngle = self.registerPropertyDouble("First arrow angle", 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._secondArrowAngle = self.registerPropertyDouble("Second arrow angle", 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._scoopAngle = self.registerPropertyDouble("Scoop angle", 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        #self._bodyAngle.setSteps(0.5)
        #self._firstArrowAngle.setSteps(0.5)
        #self._secondArrowAngle.setSteps(0.5)
        #self._scoopAngle.setSteps(0.5)
        self._dic = None

        self._initTrack()

        self.setStandardManipulatorPolicy(Core.StandardManipulatorPolicy())

        self._insidePropUpdate = False

    # check if subElements exist
    def _initTrack(self):
        subElems = self.getSubElements()
        if len(subElems) == 0:
            self._importingTrack()

    def _importTrackElem(self, fileName, elemName):
        doc = self.getDocument()
        se = ExcavatorPart(doc)
        se.setPartData(elemName)
        # strtr = se.getPartData()
        self.addSubElement(se)  # .addSubElement(se)
        imp = lx.IV_Importer.createIn(doc)
        imp.setCreateLayer(False)
        imp.importFile(lxstr(fileName))
        importedElem = imp.getImportedElems()
        geom = importedElem[0].getGeometry()
        t = importedElem[0].getTransform()
        se.setGeometry(geom)
        se.setTransform(t)
        doc.removeObject(importedElem[0])

    def _getSubElementName(self, elem):
        vel = elem.getPropertyString(ExcavatorPart.partName)
        if vel is not None:
            str = cstr(vel.getValue())
        else:
            str = ""
        # print(str)
        return str

    def _createSubElementsDictionary(self):
        # DONE: !!!
        subElems = self.getSubElements()  # getSubElements CranePart.partName
        self._dic = dict()
        for se in subElems:
            # print(self._getSubElementName(se))
            self._dic[self._getSubElementName(se)] = se

    def _updateSubElementsDictionary(self, name):
        subElems = self.getSubElements()
        # self._dic = dict()
        for se in subElems:
            if self._getSubElementName(se) == name:
                self._dic[name] = se
                # self._dic.update({name: se})
                break

    def _removeSubElementsDictionary(self, name):
        subElems = self.getSubElements()
        # self._dic = dict()
        for se in subElems:
            if self._getSubElementName(se) == name:
                # print(id(self._dic))
                # print(self._dic.keys())
                rem = self._dic.pop(name)
                # !!!!!!!
                self.removeSubElement(se)
                # !!!!!!!
                doc.removeObject(se)
                break

    def _clearSubElementsDictionary(self):
        if self._dic is not None:
            self._dic.clear()
            self._dic = None

    def _createCompound(self):
        pathStr = getSkriptsFolder()

        self._importTrackElem(pathStr + "base.iv", "base")
        self._importTrackElem(pathStr + "head.iv", "head")

        self._importTrackElem(pathStr + "firstArrow.iv", "firstArrow")
        self._importTrackElem(pathStr + "secondArrow.iv", "secondArrow")

        self._importTrackElem(pathStr + "firstCylinder.iv", "firstCylinder")
        self._importTrackElem(pathStr + "firstPiston.iv", "firstPiston")
        self._importTrackElem(pathStr + "secondCylinder.iv", "secondCylinder")
        self._importTrackElem(pathStr + "secondPiston.iv", "secondPiston")
        self._importTrackElem(pathStr + "threethCylinder.iv", "threethCylinder")
        self._importTrackElem(pathStr + "threethPiston.iv", "threethPiston")

        self._importTrackElem(pathStr + "lever.iv", "lever")
        self._importTrackElem(pathStr + "scoop.iv", "scoop")

    def printDict(self):
        for k, v in self._dic.items():
            print(" {}: {} ".format(k, v))

    def setBodyAngle(self, p):
        with EditMode(self.getDocument()):
            self._bodyAngle.setValue(clamp(p, -180.0, 180))
            self._updateGeometry()

    def setFirstArrowAngle(self, p):
        with EditMode(self.getDocument()):
            self._firstArrowAngle.setValue(clamp(p, -50, 50))
            self._updateGeometry()

    def setSecondArrowAngle(self, p):
        with EditMode(self.getDocument()):
            self._secondArrowAngle.setValue(clamp(p, -40, 65))
            self._updateGeometry()

    def setScoopAngle(self, p):
        with EditMode(self.getDocument()):
            self._scoopAngle.setValue(clamp(p, -50, 65))
            self._updateGeometry()

    def openDialogWindow(self):
        print("Button pressed")

    def _importingTrack(self):
        doc = self.getDocument()
        with EditMode(doc):
            self._createCompound()
            if self._dic is None:
                self._createSubElementsDictionary()
            # self.setDiffuseColor(Base.Color(255, 214, 0))

    def _updateGeometry(self):
        doc = self.getDocument()
        with EditMode(doc):
            if self._dic is None:
                self._createSubElementsDictionary()

            track = ExcavatorData()
            track.setBodyAngle(self._bodyAngle.getValue())
            track.setFirstArrowAngle(self._firstArrowAngle.getValue())
            track.setSecondArrowAngle(self._secondArrowAngle.getValue())
            track.setScoopAngle(self._scoopAngle.getValue())

            track.rotateBody()
            track.firstArrowRotate()
            track.secondArrowRotate()
            track.rotateScoop()


            trsfBase = track.getTrsfBase()
            trsfHead = track.getTrsfHead()
            trsfFirstArrow = track.getTrsfFirstArrow()
            trsfSecondArrow = track.getTrsfSecondArrow()
            trsfFirstCylinder = track.getTrsfFirstCylinder()
            trsfSecondCylinder = track.getTrsfSecondCylinder()
            trsfThreethCylinder = track.getTrsfThreethCylinder()
            trsfFirstPiston = track.getTrsfFirstPiston()
            trsfSecondPiston = track.getTrsfSecondPiston()
            trsfThreethPiston = track.getTrsfThreethPiston()
            trsfLever = track.getTrsfLever()
            trsfScoop = track.getTrsfScoop()

            #self._dic["base"].setTransform(trsfBase)
            self._dic["head"].setTransform(trsfHead)

            self._dic["firstArrow"].setTransform(trsfFirstArrow)
            self._dic["secondArrow"].setTransform(trsfSecondArrow)

            self._dic["firstCylinder"].setTransform(trsfFirstCylinder)
            self._dic["secondCylinder"].setTransform(trsfSecondCylinder)
            self._dic["threethCylinder"].setTransform(trsfThreethCylinder)

            self._dic["firstPiston"].setTransform(trsfFirstPiston)
            self._dic["secondPiston"].setTransform(trsfSecondPiston)
            self._dic["threethPiston"].setTransform(trsfThreethPiston)

            self._dic["lever"].setTransform(trsfLever)
            self._dic["scoop"].setTransform(trsfScoop)

    def onPropertyChanged(self, aPropertyName):
        if not self._insidePropUpdate:
            self._insidePropUpdate = True
            # print("onPropertyChanged({}) - ACTIVATED".format(aPropertyName))

            if aPropertyName == "Body angle":
                self.setBodyAngle(self._bodyAngle.getValue())
            elif aPropertyName == "First arrow angle":
                self.setFirstArrowAngle(self._firstArrowAngle.getValue())
            elif aPropertyName == "Second arrow angle":
                self.setSecondArrowAngle(self._secondArrowAngle.getValue())
            elif aPropertyName == "Scoop angle":
                self.setScoopAngle(self._scoopAngle.getValue())


            self._insidePropUpdate = False
            # print("onPropertyChanged({}) - DEACTIVATED".format(aPropertyName))
        else:
            pass
            # print("onPropertyChanged({}) - SKIPPED".format(aPropertyName))

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(self.getDocument()):
            if not Geom.GeomTools.isEqual(x, 1.):
                print("Scaling in X")
                old = self._width.getValue()
                self.setWidth(old * x)
            if not Geom.GeomTools.isEqual(y, 1.):
                print("Scaling in Y")
                old = self._length.getValue()
                self.setLength(old * y)
            if not Geom.GeomTools.isEqual(z, 1.):
                print("Scaling in Z")
                old = self._height.getValue()
                self.setHeight(old * z)

            self.translateAfterScaled(aVec, aScaleBasePnt)


if __name__ == "__main__":
    doc.registerPythonScript(Base.GlobalId("{F07345E5-136D-4AD6-99E1-2581BF07AF1F}"))
    # doc.registerPythonScript(Base.GlobalId("{f0c4f2c7-7173-4d54-92f9-2ecb154261c8}")) # SubElement Class

    try:
        turmCr = Excavator(doc)
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
            turmCr.setLocalPlacement(pos)
    except Exception as e:
        print("{}".format(e))
        traceback.print_exc()
    finally:
        doc.recompute()
