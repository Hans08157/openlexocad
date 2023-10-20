# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import traceback, math, collections

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

#=====================================================================================================================

# Python dictionary of all profiles listed in Lexocad...

#=====================================================================================================================


def qstr(str):
   return Base.StringTool.toQString(lxstr(str))
#Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))

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

class Pumpenkran(lx.Element):

    # _lengthName = "Gesamtlänge"  # "Length"
    # _widthName = "Gesamtbreite"  # "Width"
    _seatHeightName = "Fundamenthöhe"  # "Seat Height"
    _heightName = "Tower Height" # First Level
    _angleName = "Tower Angle"  # "First Arm Angle"
    _arm1AngleName = "First Arm Angle"  # "First Arm Angle"
    _arm2AngleName = "Second Arm Angle"  # "Second Arm Angle"
    _arm3AngleName = "Third Arm Angle"  # "Third Arm Angle"
    _arm4AngleName = "Fourth Arm Angle"  # "Fourth Arm Angle"
    _seatSizeName = "Fundamentbreite"  # "Seat Size"
    _topPlateWidthName = "Ballastbreite"  # "Upper Beam Size"
    _topPlateSizeName = "Ballaststärke"  # "Upper Beam Thickness"
    _metallprofileTypeName1 = "Metallprofil Typ St1"  # "Metallprofile type"
    _metallprofileName1 = "Metallprofil Stand 1"  # "Metallprofile"
    _metallprofileTypeName2 = "Ober Metallprofil Typ"  # "Metallprofile type"
    _metallprofileName2 = "Ober Metallprofil"  # "Metallprofile"
    _metallprofileTypeName0 = "Unter Metallprofil Typ"  # "Metallprofile type"
    _metallprofileName0 = "Unter Metallprofil"  # "Metallprofile"
    _topPlateNumberName = "Anzahl Ballast"  # "Number of Upper Beams"
    _ankerAngleName = "Halterungwinkel"  # "Angle of anker"
    _railsLengthName = "Gleislänge"  # "Length of rails"

    _color_I_beam = Base.Color(255, 170, 0)
    _color_I_base_beam = Base.Color(204, 204, 204)
    _color_Seat_beam = Base.Color(153, 153, 153)
    _color_Tower = Base.Color(233, 233, 233)
    _color_Arm = Base.Color(255, 168, 0)

    def getGlobalClassId(self):
        return Base.GlobalId("{b7cc7eff-60bc-46de-8924-01ef206cd558}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Pumpenkran", "OpenLxApp.Element")
        
        # Register properties 
        self.setPropertyHeader(lxstr("Pumpenkran"), -1)
        self.setPropertyGroupName(lxstr("Pumpenkran Parameter"), -1)
        self.setUserName(lxstr("Pumpenkran"))
        # self._length = self.registerPropertyDouble(self._lengthName, 14.0, lx.Property.NOT_VISIBLE, lx.Property.EDITABLE, -1)
        # self._width = self.registerPropertyDouble(self._widthName, 6.2, lx.Property.NOT_VISIBLE, lx.Property.EDITABLE, -1)
        self._height = self.registerPropertyDouble(self._heightName, 15.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        # self._seatHeight = self.registerPropertyDouble(self._seatHeightName, 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._seatSize = self.registerPropertyDouble(self._seatSizeName, 0.6, lx.Property.NOT_VISIBLE, lx.Property.EDITABLE, -1)
        self._angle = self.registerPropertyInteger(self._angleName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._arm1Angle = self.registerPropertyInteger(self._arm1AngleName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._arm2Angle = self.registerPropertyInteger(self._arm2AngleName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._arm3Angle = self.registerPropertyInteger(self._arm3AngleName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._arm4Angle = self.registerPropertyInteger(self._arm4AngleName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        
        # self._topPlateSize = self.registerPropertyDouble(self._topPlateSizeName, 0.25, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        # self._topPlateWidth = self.registerPropertyDouble(self._topPlateWidthName, 1.8, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        # self._ankerAngle = self.registerPropertyDouble(self._ankerAngleName, 45., lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._railsLength = self.registerPropertyDouble(self._railsLengthName, 25., lx.Property.NOT_VISIBLE, lx.Property.EDITABLE, -1)


        # self._topPlateNumber = self.registerPropertyInteger(self._topPlateNumberName, 6, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._setAllSteps()

        self._updateGeometry()

        self._insidePropUpdate = False

        
        
    def _setAllSteps(self):
        # self._length.setSteps(0.1)
        # self._width.setSteps(0.1)
        self._height.setSteps(1.0)
        # self._seatHeight.setSteps(0.1)
        self._seatSize.setSteps(0.1)
        self._arm1Angle.setSteps(1)
        self._arm2Angle.setSteps(1)
        # self._topPlateSize.setSteps(0.01)
        # self._topPlateWidth.setSteps(0.1)
        # self._railsLength.setSteps(0.1)


    @staticmethod
    def _createFacetedBrepSubElement(listPoint, heightStep, dir):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        # subElem = lx.SubElement.createIn(doc)
        # subElem.setGeometry(geom)
        return geom


    def _createSeat(self):
        """ Creating seat beams """
        zDir = Geom.Dir(0, 0, 1)
        # xDir = Geom.Dir(1, 0, 0)
        # yDir = Geom.Dir(0, 1, 0)

        # Square beam
        baseSize = 3.0
        thick = 0.8
        pointList = []
        pointList.append(Geom.Pnt(baseSize, baseSize, 0.0))
        pointList.append(Geom.Pnt(-baseSize, baseSize, 0.0))
        pointList.append(Geom.Pnt(-baseSize, -baseSize, 0.0))
        pointList.append(Geom.Pnt(baseSize, -baseSize, 0.0))


        base_plate = Pumpenkran._createFacetedBrepSubElement(pointList, thick, zDir)

        element = lx.SubElement.createIn(doc)
        element.setGeometry(base_plate)
        # axis1 = Geom.Ax2(Geom.Pnt(0, 0, 0), zDir, yDir) # width/2., 0
        # element.setLocalPlacement(axis1)
        element.setDiffuseColor(self._color_Seat_beam)

        self.addSubElement(element)

    def _createTower(self):
        
        # length = self._length.getValue()
        # width  = self._width.getValue()
        # seatSize = self._seatSize.getValue()
        # !!!
        height = self._height.getValue()
        
        # connecting beam sizes
        # h_beam = 0.2
        # b_beam = 0.05

        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)

        # Square beam
        beamSize = 0.4
        pointList = []
        pointList.append(Geom.Pnt(beamSize, beamSize, 0.0))
        pointList.append(Geom.Pnt(-beamSize, beamSize, 0.0))
        pointList.append(Geom.Pnt(-beamSize, -beamSize, 0.0))
        pointList.append(Geom.Pnt(beamSize, -beamSize, 0.0))


        base_plate = Pumpenkran._createFacetedBrepSubElement(pointList, height, zDir)

        element = lx.SubElement.createIn(doc)
        element.setGeometry(base_plate)
        # axis1 = Geom.Ax2(Geom.Pnt(0, 0, 0), zDir, yDir) # width/2., 0
        # element.setLocalPlacement(axis1)
        element.setDiffuseColor(self._color_Tower)
        self.addSubElement(element)

        cyl_pos = Geom.Ax2(Geom.Pnt(0, 0, height), Geom.Dir(0, 0, 1))
        cylinder = lx.RightCircularCylinder.createIn(doc)
        cylinder.setHeight(0.1)
        cylinder.setRadius(0.2)
        cylinder.setPosition(cyl_pos)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cylinder)
        elem_cyl.setDiffuseColor(self._color_Tower)

        self.addSubElement(elem_cyl)

        # platform 

        platformSize = 1.28
        platformThick = 0.1
        pointList = []
        pointList.append(Geom.Pnt( platformSize,  platformSize, 0.0))
        pointList.append(Geom.Pnt(-platformSize,  platformSize, 0.0))
        pointList.append(Geom.Pnt(-platformSize, -platformSize, 0.0))
        pointList.append(Geom.Pnt( platformSize, -platformSize, 0.0))

        platform_plate = Pumpenkran._createFacetedBrepSubElement(pointList, platformThick, zDir)

        plat_pos = Geom.Ax2(Geom.Pnt(0, 0, height-2.5), Geom.Dir(0, 0, 1))
        # platform_plate.setPosition(plat_pos)

        elem_plat = lx.SubElement.createIn(doc)
        elem_plat.setGeometry(platform_plate)
        elem_plat.setLocalPlacement(plat_pos)
        elem_plat.setDiffuseColor(self._color_Tower)

        self.addSubElement(elem_plat)

        cyl_ver_pos = Geom.Ax2(Geom.Pnt(0, 0, height-2.5), Geom.Dir(0, 0, 1))
        cyl_ver = lx.RightCircularCylinder.createIn(doc)
        cyl_ver.setHeight(1.2)
        cyl_ver.setRadius(0.04)
        cyl_ver.setPosition(cyl_ver_pos)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(1.2, 1.2, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(1.2, -1.2, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(-1.2, -1.2, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(-1.2, 1.2, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(1.2, 0.4, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(1.2, -0.4, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(-1.2, 0.4, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(-1.2, -0.4, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(0.4, 1.2, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(-0.4, 1.2, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(0.4, -1.2, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_ver)
        axis_poz = Geom.Ax2(Geom.Pnt(-0.4, -1.2, 0), zDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        cyl_hor_pos = Geom.Ax2(Geom.Pnt(0, 0, height-2.5), Geom.Dir(1, 0, 0))
        cyl_hor = lx.RightCircularCylinder.createIn(doc)
        cyl_hor.setHeight(2.4)
        cyl_hor.setRadius(0.04)
        cyl_hor.setPosition(cyl_hor_pos)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_hor)
        axis_poz = Geom.Ax2(Geom.Pnt(1.2, -2.4/2., 1.2), zDir, yDir) # width/2., 
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_hor)
        axis_poz = Geom.Ax2(Geom.Pnt(-1.2, -2.4/2., 1.2), zDir, yDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_hor)
        axis_poz = Geom.Ax2(Geom.Pnt(1.2, -2.4/2., 0.7), zDir, yDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_hor)
        axis_poz = Geom.Ax2(Geom.Pnt(-1.2, -2.4/2., 0.7), zDir, yDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_hor)
        axis_poz = Geom.Ax2(Geom.Pnt(-2.4/2., 1.2, 1.2), zDir, xDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_hor)
        axis_poz = Geom.Ax2(Geom.Pnt(-2.4/2., -1.2, 1.2), zDir, xDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_hor)
        axis_poz = Geom.Ax2(Geom.Pnt(-2.4/2., 1.2, 0.7), zDir, xDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)

        elem_cyl = lx.SubElement.createIn(doc)
        elem_cyl.setGeometry(cyl_hor)
        axis_poz = Geom.Ax2(Geom.Pnt(-2.4/2., -1.2, 0.7), zDir, xDir) # width/2., 0
        elem_cyl.setLocalPlacement(axis_poz)
        elem_cyl.setDiffuseColor(self._color_Tower)
        self.addSubElement(elem_cyl)


    def _createArmHolder(self):
        angle = self._angle.getValue()
        
        # length = self._length.getValue()
        # width  = self._width.getValue()
        # seatSize = self._seatSize.getValue()
        height = self._height.getValue()
        armWidth = 0.22
        z_c = 0.85

        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)

        ax_rot01 = Geom.Ax1(Geom.Pnt(0.6, 0, -0.6), yDir)
        ax_rot1 = Geom.Ax1(Geom.Pnt(0.0, 0, 0.), yDir)
        ang_rot = -30 * math.pi/180.
        

        pointList = []
        pointList.append(Geom.Pnt(-0.3, armWidth, -0.8))
        pointList.append(Geom.Pnt(0.3, armWidth, -0.8))
        pointList.append(Geom.Pnt(0.45, armWidth, -0.75))
        pointList.append(Geom.Pnt(0.6, armWidth, -0.75))
        # pointList.append(Geom.Pnt(9.25, armWidth, -0.1))
        # pointList.append(Geom.Pnt(9.35, armWidth, -0.15))

        pointList.append(Geom.Pnt(0.6, armWidth, -0.75).rotated(ax_rot01, 1*ang_rot))
        pointList.append(Geom.Pnt(0.6, armWidth, -0.75).rotated(ax_rot01, 2*ang_rot))
        pointList.append(Geom.Pnt(0.6, armWidth, -0.75).rotated(ax_rot01, 3*ang_rot))
        pointList.append(Geom.Pnt(0.6, armWidth, -0.75).rotated(ax_rot01, 4*ang_rot))
        pointList.append(Geom.Pnt(0.6, armWidth, -0.75).rotated(ax_rot01, 5*ang_rot))

        pointList.append(Geom.Pnt(0.4, armWidth, -0.35))
        pointList.append(Geom.Pnt(0.25, armWidth, -0.2))
        pointList.append(Geom.Pnt(0.25, armWidth, -0.0))

        pointList.append(Geom.Pnt(0.25, armWidth, -0.0).rotated(ax_rot1, 1*ang_rot))
        pointList.append(Geom.Pnt(0.25, armWidth, -0.0).rotated(ax_rot1, 2*ang_rot))
        pointList.append(Geom.Pnt(0.25, armWidth, -0.0).rotated(ax_rot1, 3*ang_rot))
        pointList.append(Geom.Pnt(0.25, armWidth, -0.0).rotated(ax_rot1, 4*ang_rot))

        pointList.append(Geom.Pnt(-0.45, armWidth, 0.05))
        pointList.append(Geom.Pnt(-0.45, armWidth, -0.2))
        pointList.append(Geom.Pnt(-4.0, armWidth, -0.2))
        pointList.append(Geom.Pnt(-4.0, armWidth, -0.6))
        pointList.append(Geom.Pnt(-0.4, armWidth, -0.6))
        pointList.append(Geom.Pnt(-0.35, armWidth, -0.75))

        # axes for setLocalPlacement  
        axis = Geom.Ax2(Geom.Pnt(0, 0, height + z_c), zDir) # width/2., 0
   
        base_plate = Pumpenkran._createFacetedBrepSubElement(pointList, 2*armWidth, -yDir)

        element = lx.SubElement.createIn(doc)
        element.setGeometry(base_plate)
        element.setLocalPlacement(axis)
        element.setDiffuseColor(self._color_Arm)
        
        ang = -math.pi*angle/180.0
        ax_rot = Geom.Ax1(Geom.Pnt(0, 0, height + z_c), zDir) 
        element.rotate(ax_rot, ang)
        self.addSubElement(element)

        pointList2 = []
        pointList2.append(Geom.Pnt(-4, -0.25, -0.2))
        pointList2.append(Geom.Pnt(-4, -0.25, -1.2))
        pointList2.append(Geom.Pnt(-4, -0.75, -1.2))
        pointList2.append(Geom.Pnt(-4, -0.75,  0.3))
        pointList2.append(Geom.Pnt(-4,  0.75,  0.2))
        pointList2.append(Geom.Pnt(-4,  0.75, -1.2))
        pointList2.append(Geom.Pnt(-4,  0.25, -1.2))
        pointList2.append(Geom.Pnt(-4,  0.25, -0.2))

        balast_plate = Pumpenkran._createFacetedBrepSubElement(pointList2, 0.5, xDir)

        axis1 = Geom.Ax2(Geom.Pnt(0, 0, height + z_c), zDir)
        elem_b1 = lx.SubElement.createIn(doc)
        elem_b1.setGeometry(balast_plate)
        elem_b1.setLocalPlacement(axis1)
        elem_b1.setDiffuseColor(self._color_Tower)
        elem_b1.rotate(ax_rot, ang)

        axis2 = Geom.Ax2(Geom.Pnt(0.5, 0, height + z_c), zDir)
        elem_b2 = lx.SubElement.createIn(doc)
        elem_b2.setGeometry(balast_plate)
        elem_b2.setLocalPlacement(axis2)
        elem_b2.setDiffuseColor(self._color_Tower)
        elem_b2.rotate(ax_rot, ang)

        axis3 = Geom.Ax2(Geom.Pnt(1.0, 0, height + z_c), zDir)
        elem_b3 = lx.SubElement.createIn(doc)
        elem_b3.setGeometry(balast_plate)
        elem_b3.setLocalPlacement(axis3)
        elem_b3.setDiffuseColor(self._color_Tower)
        elem_b3.rotate(ax_rot, ang)

        self.addSubElement(elem_b1)
        self.addSubElement(elem_b2)
        self.addSubElement(elem_b3)


    def _createArm1(self):
        angle = self._angle.getValue()
        arm1Angle = self._arm1Angle.getValue()
        
        # length = self._length.getValue()
        # width  = self._width.getValue()
        # seatSize = self._seatSize.getValue()
        height = self._height.getValue()
        armWidth = 0.3
        z_c = 0.85

        pointList = []
        pointList.append(Geom.Pnt(-0.25, armWidth, 0.3))
        pointList.append(Geom.Pnt(9.1, armWidth, 0.3))
        pointList.append(Geom.Pnt(9.2, armWidth, 0.2))
        pointList.append(Geom.Pnt(9.2, armWidth, -0.05))
        pointList.append(Geom.Pnt(9.25, armWidth, -0.1))
        pointList.append(Geom.Pnt(9.35, armWidth, -0.15))
        pointList.append(Geom.Pnt(9.4, armWidth, -0.25))
        pointList.append(Geom.Pnt(9.4, armWidth, -0.35))
        pointList.append(Geom.Pnt(9.35, armWidth, -0.45))
        pointList.append(Geom.Pnt(9.25, armWidth, -0.5))
        pointList.append(Geom.Pnt(9.15, armWidth, -0.5))
        pointList.append(Geom.Pnt(9.05, armWidth, -0.45))
        pointList.append(Geom.Pnt(8.95, armWidth, -0.35))
        pointList.append(Geom.Pnt(8.85, armWidth, -0.3))
        pointList.append(Geom.Pnt(8.5, armWidth, -0.25))
        pointList.append(Geom.Pnt(6.75, armWidth, -0.25))
        pointList.append(Geom.Pnt(6.4, armWidth, -0.5))
        pointList.append(Geom.Pnt(4.0, armWidth, -0.35))
        pointList.append(Geom.Pnt(-0.25, armWidth, -0.35))

        orig = Geom.Pnt(0, 0, 0)
        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)

        # axes for setLocalPlacement  
        axis = Geom.Ax2(Geom.Pnt(0, 0, height + z_c), zDir) # width/2., 0
   
        base_plate = Pumpenkran._createFacetedBrepSubElement(pointList, 2*armWidth, -yDir)

        element = lx.SubElement.createIn(doc)
        element.setGeometry(base_plate)
        element.setLocalPlacement(axis)
        element.setDiffuseColor(self._color_Arm)
        
        ang = -math.pi*arm1Angle/180.0
        ax_rot = Geom.Ax1(Geom.Pnt(0, 0, height + z_c), yDir) 
        element.rotate(ax_rot, ang)

        ang0 = -math.pi*angle/180.0
        ax_rot = Geom.Ax1(Geom.Pnt(0, 0, height + z_c), zDir) 
        element.rotate(ax_rot, ang0)
        self.addSubElement(element)
 
    def _createArm2(self):
        angle = self._angle.getValue()
        arm1Angle = self._arm1Angle.getValue()
        arm2Angle = self._arm2Angle.getValue()

        # length = self._length.getValue()
        # width  = self._width.getValue()
        # seatSize = self._seatSize.getValue()
        height = self._height.getValue()
        armWidth = 0.2
        z_c = 0.85

        pointList = []
        pointList.append(Geom.Pnt(1.0, armWidth, -1.0))
        pointList.append(Geom.Pnt(1.05, armWidth, -0.9))
        pointList.append(Geom.Pnt(1.15, armWidth, -0.85))
        pointList.append(Geom.Pnt(3.1, armWidth, -0.75))
        pointList.append(Geom.Pnt(3.5, armWidth, -0.35))
        pointList.append(Geom.Pnt(3.65, armWidth, -0.35))
        pointList.append(Geom.Pnt(3.95, armWidth, -0.65))
        pointList.append(Geom.Pnt(8.25, armWidth, -0.45))       
        pointList.append(Geom.Pnt(8.85, armWidth, -0.3))
        pointList.append(Geom.Pnt(9, armWidth, -0.2))
        pointList.append(Geom.Pnt(9.15, armWidth, -0.1))
        pointList.append(Geom.Pnt(9.25, armWidth, -0.1))
        pointList.append(Geom.Pnt(9.35, armWidth, -0.15))
        pointList.append(Geom.Pnt(9.4, armWidth, -0.25))
        pointList.append(Geom.Pnt(9.4, armWidth, -0.35))
        pointList.append(Geom.Pnt(9.35, armWidth, -0.45))
        pointList.append(Geom.Pnt(9, armWidth, -0.75))
        pointList.append(Geom.Pnt(8.85, armWidth, -0.8))
        pointList.append(Geom.Pnt(1.15, armWidth, -1.2))
        pointList.append(Geom.Pnt(1.05, armWidth, -1.1))


        orig = Geom.Pnt(0, 0, 0)
        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)


        # axes for setLocalPlacement  
        axis = Geom.Ax2(Geom.Pnt(0, 0, height + z_c), zDir) # width/2., 0
        # axis2 = Geom.Ax2(Geom.Pnt(0, -(width-b)/2., h/2.), zDir, xDir) # width/2., 0
        # axis3 = Geom.Ax2(Geom.Pnt(-(length-b)/2., 0, h/2.), zDir, yDir) # width/2., 0
        # axis4 = Geom.Ax2(Geom.Pnt((length-b)/2., 0, h/2.), zDir, yDir) # width/2., 0
        
        base_plate = Pumpenkran._createFacetedBrepSubElement(pointList, 2*armWidth, -yDir)

        element = lx.SubElement.createIn(doc)
        element.setGeometry(base_plate)
        # axis = Geom.Ax2(Geom.Pnt(0, 0, 0), zDir) # width/2., 0
        element.setLocalPlacement(axis)
        element.setDiffuseColor(self._color_Arm)
        pt1_rot = Geom.Pnt(0, 0, height + z_c)
        pt2_rot = Geom.Pnt(9.25, 0, height + z_c - 0.3)

        ang2 = -math.pi*arm2Angle/180.0
        ax_rot1 = Geom.Ax1(pt1_rot, yDir)         
        ax_rot2 = Geom.Ax1(pt2_rot, yDir) 

        element.rotate(ax_rot2, ang2)

        ang = -math.pi*arm1Angle/180.0
        # pt2_rot.rotate(ax_rot2, ang2)
        element.rotate(ax_rot1, ang)

        ang0 = -math.pi*angle/180.0
        ax_rot = Geom.Ax1(Geom.Pnt(0, 0, height + z_c), zDir) 
        element.rotate(ax_rot, ang0)

        self.addSubElement(element)

    def _createArm3(self):
        angle = self._angle.getValue()
        arm1Angle = self._arm1Angle.getValue()
        arm2Angle = self._arm2Angle.getValue()
        arm3Angle = self._arm3Angle.getValue()

        height = self._height.getValue()
        armWidth = 0.16
        z_c = 0.85

        pointList = []
        pointList.append(Geom.Pnt(1.0, armWidth, -1.0))
        pointList.append(Geom.Pnt(1.05, armWidth, -0.9))
        pointList.append(Geom.Pnt(1.15, armWidth, -0.85))
        pointList.append(Geom.Pnt(1.3, armWidth, -0.825))
        pointList.append(Geom.Pnt(1.45, armWidth, -0.9))
        pointList.append(Geom.Pnt(1.7, armWidth, -1.15))
        pointList.append(Geom.Pnt(8.85, armWidth, -0.8))
        pointList.append(Geom.Pnt(9, armWidth, -0.85))
        pointList.append(Geom.Pnt(9.35, armWidth, -1.1))
        pointList.append(Geom.Pnt(9.4, armWidth, -1.2))
        pointList.append(Geom.Pnt(9.35, armWidth, -1.3))
        pointList.append(Geom.Pnt(9.25, armWidth, -1.4))
        pointList.append(Geom.Pnt(9.1, armWidth, -1.35))
        pointList.append(Geom.Pnt(9, armWidth, -1.2))
        pointList.append(Geom.Pnt(8.85, armWidth, -1.1))
        pointList.append(Geom.Pnt(7.5, armWidth, -1.175))
        pointList.append(Geom.Pnt(7.35, armWidth, -1.5))
        pointList.append(Geom.Pnt(6.75, armWidth, -1.525))
        pointList.append(Geom.Pnt(6.55, armWidth, -1.225))
        pointList.append(Geom.Pnt(1.55, armWidth, -1.5))
        pointList.append(Geom.Pnt(1.45, armWidth, -1.45))
        pointList.append(Geom.Pnt(1.05, armWidth, -1.1))


        orig = Geom.Pnt(0, 0, 0)
        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)


        # axes for setLocalPlacement  
        axis = Geom.Ax2(Geom.Pnt(0, 0, height + z_c), zDir) # width/2., 0
        # axis2 = Geom.Ax2(Geom.Pnt(0, -(width-b)/2., h/2.), zDir, xDir) # width/2., 0
        # axis3 = Geom.Ax2(Geom.Pnt(-(length-b)/2., 0, h/2.), zDir, yDir) # width/2., 0
        # axis4 = Geom.Ax2(Geom.Pnt((length-b)/2., 0, h/2.), zDir, yDir) # width/2., 0
        
        base_plate = Pumpenkran._createFacetedBrepSubElement(pointList, 2*armWidth, -yDir)

        element = lx.SubElement.createIn(doc)
        element.setGeometry(base_plate)
        # axis = Geom.Ax2(Geom.Pnt(0, 0, 0), zDir) # width/2., 0
        element.setLocalPlacement(axis)
        element.setDiffuseColor(self._color_Arm)
        pt1_rot = Geom.Pnt(0, 0, height + z_c)
        pt2_rot = Geom.Pnt(9.25, 0, height + z_c - 0.3)
        pt3_rot = Geom.Pnt(1.25, 0, height + z_c - 1.025)

        ax_rot1 = Geom.Ax1(pt1_rot, yDir)         
        ax_rot2 = Geom.Ax1(pt2_rot, yDir) 
        ax_rot3 = Geom.Ax1(pt3_rot, yDir) 

        ang3 = math.pi*arm3Angle/180.0
        element.rotate(ax_rot3, ang3)

        ang2 = -math.pi*arm2Angle/180.0
        element.rotate(ax_rot2, ang2)

        ang = -math.pi*arm1Angle/180.0
        element.rotate(ax_rot1, ang)

        ang0 = -math.pi*angle/180.0
        ax_rot = Geom.Ax1(Geom.Pnt(0, 0, height + z_c), zDir) 
        element.rotate(ax_rot, ang0)

        self.addSubElement(element)

    def _createArm4(self):
        angle = self._angle.getValue()
        arm1Angle = self._arm1Angle.getValue()
        arm2Angle = self._arm2Angle.getValue()
        arm3Angle = self._arm3Angle.getValue()
        arm4Angle = self._arm4Angle.getValue()

        height = self._height.getValue()
        armWidth = 0.10
        z_c = 0.85

        pointList = []
        pointList.append(Geom.Pnt(9, armWidth, -1.2))
        pointList.append(Geom.Pnt(9.1, armWidth, -1.1))
        pointList.append(Geom.Pnt(9.2, armWidth, -1.05))
        pointList.append(Geom.Pnt(9.3, armWidth, -1.05))
        pointList.append(Geom.Pnt(9.35, armWidth, -1.1))
        pointList.append(Geom.Pnt(9.4, armWidth, -1.2))
        pointList.append(Geom.Pnt(9.35, armWidth, -1.3))
        pointList.append(Geom.Pnt(9, armWidth, -1.65))
        pointList.append(Geom.Pnt(8.85, armWidth, -1.75))
        pointList.append(Geom.Pnt(1.7, armWidth, -1.75))
        pointList.append(Geom.Pnt(1.7, armWidth, -1.6))
        pointList.append(Geom.Pnt(2.45, armWidth, -1.6))
        pointList.append(Geom.Pnt(2.5, armWidth, -1.45))
        pointList.append(Geom.Pnt(2.65, armWidth, -1.44))
        pointList.append(Geom.Pnt(2.7, armWidth, -1.6))
        pointList.append(Geom.Pnt(8.55, armWidth, -1.5))

        # pointList.append(Geom.Pnt(6.75, armWidth, -1.525))
        # pointList.append(Geom.Pnt(6.55, armWidth, -1.225))
        # pointList.append(Geom.Pnt(1.55, armWidth, -1.5))
        # pointList.append(Geom.Pnt(1.45, armWidth, -1.45))
        # pointList.append(Geom.Pnt(1.05, armWidth, -1.1))


        orig = Geom.Pnt(0, 0, 0)
        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)


        # axes for setLocalPlacement  
        axis = Geom.Ax2(Geom.Pnt(0, 0, height + z_c), zDir) 
        
        base_plate = Pumpenkran._createFacetedBrepSubElement(pointList, 2*armWidth, -yDir)

        element = lx.SubElement.createIn(doc)
        element.setGeometry(base_plate)
        element.setLocalPlacement(axis)
        element.setDiffuseColor(self._color_Arm)

        pt1_rot = Geom.Pnt(0, 0, height + z_c)
        pt2_rot = Geom.Pnt(9.25, 0, height + z_c - 0.3)
        pt3_rot = Geom.Pnt(1.25, 0, height + z_c - 1.025)
        pt4_rot = Geom.Pnt(9.25, 0, height + z_c - 1.2)

        ax_rot1 = Geom.Ax1(pt1_rot, yDir)         
        ax_rot2 = Geom.Ax1(pt2_rot, yDir) 
        ax_rot3 = Geom.Ax1(pt3_rot, yDir)
        ax_rot4 = Geom.Ax1(pt4_rot, yDir) 

        ang4 = -math.pi*arm4Angle/180.0
        element.rotate(ax_rot4, ang4)

        ang3 = math.pi*arm3Angle/180.0
        element.rotate(ax_rot3, ang3)

        ang2 = -math.pi*arm2Angle/180.0
        element.rotate(ax_rot2, ang2)

        ang = -math.pi*arm1Angle/180.0
        element.rotate(ax_rot1, ang)

        ang0 = -math.pi*angle/180.0
        ax_rot = Geom.Ax1(Geom.Pnt(0, 0, height + z_c), zDir) 
        element.rotate(ax_rot, ang0)

        self.addSubElement(element)


    def createCompound(self):
        self._createSeat()
        self._createTower()
        self._createArmHolder()
        self._createArm1()
        self._createArm2()
        self._createArm3()
        self._createArm4()

        # self._createUpperLevel()
        # self.createTrosBase()
        # self.createHook()


    # def setLength(self, p):
    #     # nBeam = self._topBeamNumber.getValue()
    #     topPlateWidth = 1
    #     # seatSize = self._seatSize.getValue()
    #     minV = 5
    #     with EditMode(self.getDocument()):
    #         self._length.setValue(clamp(p, minV, 1e04))
    #         self._updateGeometry()
    #     if p < minV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
    #         # self._insidePropUpdate = True
            
            
    # def setWidth(self, p):
    #     # nBeam = self._topBeamNumber.getValue()
    #     minpWidth = 1
    #     # seatSize = self._seatSize.getValue()
    #     minV = 2*(minpWidth + 0.31)
    #     # if not self._insidePropUpdate:
    #     with EditMode(self.getDocument()):
    #         self._width.setValue(clamp(p, minV, 1e04))
    #         self._updateGeometry()
    #     if p < minV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def setHeight(self, p):
        minV = 0.2
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(p, minV, 1e04))
            self._updateGeometry()
        # if p < minV:
        #     Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def setAngle(self, p):
        minV = -3000
        maxV =  3000
        with EditMode(self.getDocument()):
            self._angle.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setArm1Angle(self, p):
        minV = 0
        maxV = 90
        with EditMode(self.getDocument()):
            self._arm1Angle.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))
    
    def setArm2Angle(self, p):
        minV = 0
        maxV = 177
        with EditMode(self.getDocument()):
            self._arm2Angle.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setArm3Angle(self, p):
        minV = 0
        maxV = 177
        with EditMode(self.getDocument()):
            self._arm3Angle.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setArm4Angle(self, p):
        minV = 0
        maxV = 177
        with EditMode(self.getDocument()):
            self._arm4Angle.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    # def setSeatHeight(self, p):
    #     minV = 0.2
    #     with EditMode(self.getDocument()):
    #         self._seatHeight.setValue(clamp(p, minV, 1e04))
    #         self._updateGeometry()
    #     # if p < minV:
    #     #     Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    # def setSeatSize(self, p):
    #     minV = 0.5
    #     maxV = min(self._length.getValue()-0.01, self._width.getValue()-0.01)
    #     # print(maxV)
    #     with EditMode(self.getDocument()):
    #         self._seatSize.setValue(clamp(p, minV, maxV))
    #         self._updateGeometry()
    #     if p < minV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
    #     if p > maxV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))





    # def setTopPlateSize(self, p):
    #     # length = self._length.getValue()
    #     # width  = self._width.getValue()
    #     # nBeam = self._topPlateNumber.getValue()
    #     maxV = 1e2
    #     with EditMode(self.getDocument()):
    #         self._topPlateSize.setValue(clamp(p, 0.01, maxV))
    #         self._updateGeometry()
    #     if p > maxV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    # def setTopPlateWidth(self, p):
    #     length = self._length.getValue()
    #     width  = self._width.getValue()
    #     # nBeam = self._topPlateNumber.getValue()
    #     minV = 0.01
    #     maxV = min(length/2., width/2. - 0.32)
    #     with EditMode(self.getDocument()):
    #         self._topPlateWidth.setValue(clamp(p, minV, maxV))
    #         self._updateGeometry()
    #     if p > maxV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))
    #     if p < minV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    # def setTopPlateNumber(self, p):
    #     # length = self._length.getValue()
    #     # width  = self._width.getValue()
    #     # topBeamSize = self._topBeamSize.getValue() 
    #     # maxV = min(int(length/topBeamSize/2.), int(width/topBeamSize/2.))
    #     # print(maxV)
    #     with EditMode(self.getDocument()):
    #         self._topPlateNumber.setValue(clamp(p, 0, 1e3))
    #         self._updateGeometry()
    #     if p < 0:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
    #     # if p > maxV:
    #     #     Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    # def setAnkerAngle(self, p):
    #     # nBeam = self._topPlateNumber.getValue()
    #     minV = 0
    #     maxV = 90
    #     with EditMode(self.getDocument()):
    #         self._ankerAngle.setValue(clamp(p, minV, maxV))
    #         self._updateGeometry()
    #     if p > maxV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))
    #     if p < minV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
    
    # def setRailsLength(self, p):
    #     # nBeam = self._topPlateNumber.getValue()
    #     minV = self._width.getValue() + 2.4
    #     maxV = 1000
    #     with EditMode(self.getDocument()):
    #         self._railsLength.setValue(clamp(p, minV, maxV))
    #         self._updateGeometry()
    #     if p > maxV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))
    #     if p < minV:
    #         Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
    

    def removeBeams(self):
        #print "removeBeams"
        beams = self.getSubElements() # removeSubElements()
        for b in beams:
            self.removeSubElement(b)
            doc.removeObject(b)


    def _updateGeometry(self):
        doc = self.getDocument()
        with EditMode(doc):
            self.removeBeams()
            self.createCompound()

    def onPropertyChanged(self, aPropertyName):
        #doc.beginEditing()
        # self._topBeamNumber.setMinValue(1)
        # if aPropertyName == self._lengthName:
        #     self.setLength(self._length.getValue())
        # elif aPropertyName == self._widthName:
        #     self.setWidth(self._width.getValue())
        # elif aPropertyName == self._seatHeightName:
        #     self.setSeatHeight(self._seatHeight.getValue())
        # elif aPropertyName == self._seatSizeName:
        #     self.setSeatSize(self._seatSize.getValue())
        if aPropertyName == self._heightName:
            self.setHeight(self._height.getValue())

        # elif aPropertyName == self._metallprofileTypeName1:
        #     self.setMetallprofileType1(self._metallprofileType1.getValue())
        # elif aPropertyName == self._metallprofileName1:
        #     self.setMetallprofile1(self._metallprofile1.getValue())
        # elif aPropertyName == self._metallprofileTypeName2:
        #     self.setMetallprofileType2(self._metallprofileType2.getValue())
        # elif aPropertyName == self._metallprofileName2:
        #     self.setMetallprofile2(self._metallprofile2.getValue())
        # elif aPropertyName == self._metallprofileTypeName0:
        #     self.setMetallprofileType0(self._metallprofileType0.getValue())
        # elif aPropertyName == self._metallprofileName0:
        #     self.setMetallprofile0(self._metallprofile0.getValue())

        # elif aPropertyName == self._topPlateSizeName:
        #     self.setTopPlateSize(self._topPlateSize.getValue())
        # elif aPropertyName == self._topPlateWidthName:
        #     self.setTopPlateWidth(self._topPlateWidth.getValue())
        elif aPropertyName == self._angleName:
            self.setAngle(self._angle.getValue())
        elif aPropertyName == self._arm1AngleName:
            self.setArm1Angle(self._arm1Angle.getValue())
        elif aPropertyName == self._arm2AngleName:
            self.setArm2Angle(self._arm2Angle.getValue())
        elif aPropertyName == self._arm3AngleName:
            self.setArm3Angle(self._arm3Angle.getValue())
        elif aPropertyName == self._arm4AngleName:
            self.setArm4Angle(self._arm4Angle.getValue())

        # elif aPropertyName == self._topPlateNumberName:
        #     self.setTopPlateNumber(self._topPlateNumber.getValue())
            
        
        # self._insidePropUpdate = False



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

def main():
    doc.registerPythonScript(Base.GlobalId("{11ad86ef-690c-4966-9aa4-07a0a75d7f72}"))

    try:
        pm = Pumpenkran(doc)
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
            pm.setLocalPlacement(pos)
    except Exception as e:
        print("{}".format(e))
        traceback.print_exc()
    finally:
        doc.recompute()
    
if __name__ == "__main__":
    main()
    

