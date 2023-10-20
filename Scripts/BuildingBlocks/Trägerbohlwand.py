# OpenLexocad libraries
# version 1.0  24.06.2020

# attributes

# ========================================
# ====  Supported by Roman Davydiuk   ====
# ====  Mail: davydjukroman@gmail.com ====
# ====  Skype: live:davydjukroman     ====
# ========================================

import collections
import math
import traceback

import Base
import Core
import Geom
import OpenLxApp as lx
import OpenLxUI as ui
import Topo

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

epsilon = 0.0001
pi2 = math.pi * 0.5

# Python dictionary of all profiles listed in Lexocad...
profiles = collections.OrderedDict()

profiles.update({'HEA 100': {'h': 96E-03, 'b': 100E-03, 's': 5.0E-03, 't': 8.0E-03, 'r': 12.0E-03}})
profiles.update({'HEA 120': {'h': 114E-03, 'b': 120E-03, 's': 5.0E-03, 't': 8.0E-03, 'r': 12.0E-03}})
profiles.update({'HEA 140': {'h': 133E-03, 'b': 140E-03, 's': 5.5E-03, 't': 8.5E-03, 'r': 12.0E-03}})
profiles.update({'HEA 160': {'h': 152E-03, 'b': 160E-03, 's': 6.0E-03, 't': 9.0E-03, 'r': 15.0E-03}})
profiles.update({'HEA 180': {'h': 171E-03, 'b': 180E-03, 's': 6.0E-03, 't': 9.5E-03, 'r': 15.0E-03}})
profiles.update({'HEA 200': {'h': 190E-03, 'b': 200E-03, 's': 6.5E-03, 't': 10.0E-03, 'r': 18.0E-03}})
profiles.update({'HEA 220': {'h': 210E-03, 'b': 220E-03, 's': 7.0E-03, 't': 11.0E-03, 'r': 18.0E-03}})
profiles.update({'HEA 240': {'h': 230E-03, 'b': 240E-03, 's': 7.5E-03, 't': 12.0E-03, 'r': 21.0E-03}})
profiles.update({'HEA 260': {'h': 250E-03, 'b': 260E-03, 's': 7.5E-03, 't': 12.5E-03, 'r': 24.0E-03}})
profiles.update({'HEA 280': {'h': 270E-03, 'b': 280E-03, 's': 8.0E-03, 't': 13.0E-03, 'r': 24.0E-03}})
profiles.update({'HEA 300': {'h': 290E-03, 'b': 300E-03, 's': 8.5E-03, 't': 14.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 320': {'h': 310E-03, 'b': 300E-03, 's': 9.0E-03, 't': 15.5E-03, 'r': 27.0E-03}})
profiles.update({'HEA 340': {'h': 330E-03, 'b': 300E-03, 's': 9.5E-03, 't': 16.5E-03, 'r': 27.0E-03}})
profiles.update({'HEA 360': {'h': 350E-03, 'b': 300E-03, 's': 10.0E-03, 't': 17.5E-03, 'r': 27.0E-03}})
profiles.update({'HEA 400': {'h': 390E-03, 'b': 300E-03, 's': 11.0E-03, 't': 19.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 450': {'h': 440E-03, 'b': 300E-03, 's': 11.5E-03, 't': 21.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 500': {'h': 490E-03, 'b': 300E-03, 's': 12.0E-03, 't': 23.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 550': {'h': 540E-03, 'b': 300E-03, 's': 12.5E-03, 't': 24.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 600': {'h': 590E-03, 'b': 300E-03, 's': 13.0E-03, 't': 25.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 650': {'h': 640E-03, 'b': 300E-03, 's': 13.5E-03, 't': 26.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 700': {'h': 690E-03, 'b': 300E-03, 's': 14.5E-03, 't': 27.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 800': {'h': 790E-03, 'b': 300E-03, 's': 15.0E-03, 't': 28.0E-03, 'r': 30.0E-03}})
profiles.update({'HEA 900': {'h': 890E-03, 'b': 300E-03, 's': 16.0E-03, 't': 30.0E-03, 'r': 30.0E-03}})
profiles.update({'HEA 1000': {'h': 990E-03, 'b': 300E-03, 's': 16.5E-03, 't': 31.0E-03, 'r': 30.0E-03}})

profiles.update({'HEB 100': {'h': 100E-03, 'b': 100E-03, 's': 6.0E-03, 't': 10.0E-03, 'r': 12.0E-03}})
profiles.update({'HEB 120': {'h': 120E-03, 'b': 120E-03, 's': 6.5E-03, 't': 11.0E-03, 'r': 12.0E-03}})
profiles.update({'HEB 140': {'h': 140E-03, 'b': 140E-03, 's': 7.0E-03, 't': 12.0E-03, 'r': 12.0E-03}})
profiles.update({'HEB 160': {'h': 160E-03, 'b': 160E-03, 's': 8.0E-03, 't': 13.0E-03, 'r': 15.0E-03}})
profiles.update({'HEB 180': {'h': 180E-03, 'b': 180E-03, 's': 8.5E-03, 't': 14.0E-03, 'r': 15.0E-03}})
profiles.update({'HEB 200': {'h': 200E-03, 'b': 200E-03, 's': 9.0E-03, 't': 15.0E-03, 'r': 18.0E-03}})
profiles.update({'HEB 220': {'h': 220E-03, 'b': 220E-03, 's': 9.5E-03, 't': 16.0E-03, 'r': 18.0E-03}})
profiles.update({'HEB 240': {'h': 240E-03, 'b': 240E-03, 's': 10.0E-03, 't': 17.0E-03, 'r': 21.0E-03}})
profiles.update({'HEB 260': {'h': 260E-03, 'b': 260E-03, 's': 10.0E-03, 't': 17.5E-03, 'r': 24.0E-03}})
profiles.update({'HEB 280': {'h': 280E-03, 'b': 280E-03, 's': 10.5E-03, 't': 18.0E-03, 'r': 24.0E-03}})
profiles.update({'HEB 300': {'h': 300E-03, 'b': 300E-03, 's': 11.0E-03, 't': 19.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 320': {'h': 320E-03, 'b': 300E-03, 's': 11.5E-03, 't': 20.5E-03, 'r': 27.0E-03}})
profiles.update({'HEB 340': {'h': 340E-03, 'b': 300E-03, 's': 12.0E-03, 't': 21.5E-03, 'r': 27.0E-03}})
profiles.update({'HEB 360': {'h': 360E-03, 'b': 300E-03, 's': 12.5E-03, 't': 22.5E-03, 'r': 27.0E-03}})
profiles.update({'HEB 400': {'h': 400E-03, 'b': 300E-03, 's': 13.5E-03, 't': 24.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 450': {'h': 450E-03, 'b': 300E-03, 's': 14.0E-03, 't': 26.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 500': {'h': 500E-03, 'b': 300E-03, 's': 14.5E-03, 't': 28.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 550': {'h': 550E-03, 'b': 300E-03, 's': 15.0E-03, 't': 29.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 600': {'h': 600E-03, 'b': 300E-03, 's': 15.5E-03, 't': 30.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 650': {'h': 650E-03, 'b': 300E-03, 's': 16.0E-03, 't': 31.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 700': {'h': 700E-03, 'b': 300E-03, 's': 17.0E-03, 't': 32.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 800': {'h': 800E-03, 'b': 300E-03, 's': 17.5E-03, 't': 33.0E-03, 'r': 30.0E-03}})
profiles.update({'HEB 900': {'h': 900E-03, 'b': 300E-03, 's': 18.5E-03, 't': 35.0E-03, 'r': 30.0E-03}})
profiles.update({'HEB 1000': {'h': 1000E-03, 'b': 300E-03, 's': 19.0E-03, 't': 36.0E-03, 'r': 30.0E-03}})

profiles.update({'UNP 65': {'h': 65E-03, 'b': 42E-03, 's': 5.5E-03, 't': 7.5E-03}})
profiles.update({'UNP 80': {'h': 80E-03, 'b': 45E-03, 's': 6.0E-03, 't': 8.0E-03}})
profiles.update({'UNP 100': {'h': 100E-03, 'b': 50E-03, 's': 6.0E-03, 't': 8.5E-03}})
profiles.update({'UNP 120': {'h': 120E-03, 'b': 55E-03, 's': 7.0E-03, 't': 9.0E-03}})
profiles.update({'UNP 140': {'h': 140E-03, 'b': 60E-03, 's': 7.0E-03, 't': 10.0E-03}})
profiles.update({'UNP 160': {'h': 160E-03, 'b': 65E-03, 's': 7.5E-03, 't': 10.5E-03}})
profiles.update({'UNP 180': {'h': 180E-03, 'b': 70E-03, 's': 8.0E-03, 't': 11.0E-03}})
profiles.update({'UNP 200': {'h': 200E-03, 'b': 75E-03, 's': 8.5E-03, 't': 11.5E-03}})
profiles.update({'UNP 220': {'h': 220E-03, 'b': 80E-03, 's': 9.0E-03, 't': 12.5E-03}})
profiles.update({'UNP 240': {'h': 240E-03, 'b': 85E-03, 's': 9.5E-03, 't': 13.0E-03}})
profiles.update({'UNP 260': {'h': 260E-03, 'b': 90E-03, 's': 10.0E-03, 't': 14.0E-03}})
profiles.update({'UNP 280': {'h': 280E-03, 'b': 95E-03, 's': 10.0E-03, 't': 15.0E-03}})
profiles.update({'UNP 300': {'h': 300E-03, 'b': 100E-03, 's': 10.0E-03, 't': 16.0E-03}})
profiles.update({'UNP 320': {'h': 320E-03, 'b': 100E-03, 's': 14.0E-03, 't': 17.5E-03}})
profiles.update({'UNP 350': {'h': 350E-03, 'b': 100E-03, 's': 14.0E-03, 't': 16.0E-03}})
profiles.update({'UNP 380': {'h': 380E-03, 'b': 102E-03, 's': 13.5E-03, 't': 16.0E-03}})
profiles.update({'UNP 400': {'h': 400E-03, 'b': 110E-03, 's': 14.0E-03, 't': 18.0E-03}})

profiles.update({'UPE 80': {'h': 80E-03, 'b': 50E-03, 's': 4.0E-03, 't': 7.0E-03}})
profiles.update({'UPE 100': {'h': 100E-03, 'b': 55E-03, 's': 4.5E-03, 't': 7.5E-03}})
profiles.update({'UPE 120': {'h': 120E-03, 'b': 60E-03, 's': 5.0E-03, 't': 8.0E-03}})
profiles.update({'UPE 140': {'h': 140E-03, 'b': 65E-03, 's': 5.0E-03, 't': 9.0E-03}})
profiles.update({'UPE 160': {'h': 160E-03, 'b': 70E-03, 's': 5.5E-03, 't': 9.5E-03}})
profiles.update({'UPE 180': {'h': 180E-03, 'b': 75E-03, 's': 5.5E-03, 't': 10.5E-03}})
profiles.update({'UPE 200': {'h': 200E-03, 'b': 80E-03, 's': 6.0E-03, 't': 11.0E-03}})
profiles.update({'UPE 220': {'h': 220E-03, 'b': 85E-03, 's': 6.5E-03, 't': 12.0E-03}})
profiles.update({'UPE 240': {'h': 240E-03, 'b': 90E-03, 's': 7.0E-03, 't': 12.5E-03}})
profiles.update({'UPE 270': {'h': 270E-03, 'b': 95E-03, 's': 7.5E-03, 't': 13.5E-03}})
profiles.update({'UPE 300': {'h': 300E-03, 'b': 100E-03, 's': 9.5E-03, 't': 15.0E-03}})
profiles.update({'UPE 330': {'h': 330E-03, 'b': 105E-03, 's': 11.0E-03, 't': 16.0E-03}})
profiles.update({'UPE 360': {'h': 360E-03, 'b': 110E-03, 's': 12.0E-03, 't': 17.0E-03}})
profiles.update({'UPE 400': {'h': 400E-03, 'b': 115E-03, 's': 13.5E-03, 't': 18.0E-03}})

# Für die erweiterung der Liste kann profiles upgedatet werden und types müsssen angepasst werden, falls ein neuer Typ entsteht.
# Zudem muss bei den Leerzeichen aufgepasst werden => Bsp LARSSEN 22_10  !!!!!
first_types = ['HEA', 'HEB']
second_types = ['UNP', 'UPE']

first_typ2 = []
second_typ2 = []

list1 = list(profiles.keys())

for i in range(0, len(list1)):
    list2 = list1[i].split(' ')
    for j in range(0, len(first_types)):
        if list2[0] == first_types[j]:
            first_typ2.append([list2[0], list2[1]])


for i in range(0, len(list1)):
    list2 = list1[i].split(' ')
    for j in range(0, len(second_types)):
        if list2[0] == second_types[j]:
            second_typ2.append([list2[0], list2[1]])


# =====================================================================================================================

def qstr(str):
    return Base.StringTool.toQString(lxstr(str))


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


def vecsAreSame(v1, v2, tolerance=epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)


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

        dt = 0.001

        dArc = None
        if (1.0 - t) < dt:
            pt1 = self.paramPt(t - dt)
            pt2 = self.paramPt(t)

            dArc = Geom.Vec(pt1, pt2)
        elif (t - 0.0) < dt:
            pt1 = self.paramPt(t)
            pt2 = self.paramPt(t + dt)

            dArc = Geom.Vec(pt1, pt2)
        else:
            pt1 = self.paramPt(t - dt)
            pt2 = self.paramPt(t + dt)

            dArc = Geom.Vec(pt1, pt2)
        dArc.normalize()

        return dArc


class PolylineData:
    SegmType_Line = 0
    SegmType_Arc = 1

    _closedSuffix = "_closed"
    _ptListSuffix = "_points"
    _edgeListSuffix = "_edges"

    class _Segment:
        def __init__(self, type, data):
            self.type = type
            self.data = data

    class _LineSegmData:
        def __init__(self, startIndex, closeSegm=False):
            self.startIndex = startIndex

            if not closeSegm:
                self.endIndex = startIndex + 1
            else:
                self.endIndex = 0

    class _ArcSegmData:
        def __init__(self, ptList, p1Index, closeSegm=False):
            self.p1Index = p1Index
            self.p2Index = p1Index + 1
            if not closeSegm:
                self.p3Index = p1Index + 2
            else:
                self.p3Index = 0

            self.arc = Arc3Pnt(ptList[self.p1Index], ptList[self.p2Index], ptList[self.p3Index])

    def __init__(self):
        self._closed = False

        self._ptList = []
        self._segmList = []

    def getPntList(self):
        return self._ptList

    @staticmethod
    def fromElement(lineElem):
        newPD = PolylineData()

        firstEdge = True
        startIndex = 0
        for edgeIndex in range(len(lineElem)):
            # edge = edges[edgeIndex]
            #
            # edgeTypeRes = Topo.EdgeTool.getGeomCurveType(edge)
            # if not edgeTypeRes.ok:
            #     raise RuntimeError("Can't get edge type")

            if lineElem[edgeIndex][0] == PolylineData.SegmType_Line:
                p1Res = lineElem[edgeIndex][1]
                if firstEdge:
                    newPD._ptList.append(Geom.Pnt(p1Res))
                    firstEdge = False

                p2Res = lineElem[edgeIndex][2]
                newPD._ptList.append(Geom.Pnt(p2Res))

                segmData = PolylineData._LineSegmData(startIndex, False)
                newPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))

                startIndex += 1
            elif lineElem[edgeIndex][0] == PolylineData.SegmType_Arc:
                p1Res = lineElem[edgeIndex][1]
                if firstEdge:
                    newPD._ptList.append(Geom.Pnt(p1Res))
                    firstEdge = False

                p2Res = lineElem[edgeIndex][2]
                newPD._ptList.append(Geom.Pnt(p2Res))

                p3Res = lineElem[edgeIndex][3]
                newPD._ptList.append(Geom.Pnt(p3Res))

                segmData = PolylineData._ArcSegmData(newPD._ptList, startIndex, False)
                newPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))

                startIndex += 2
            else:
                raise RuntimeError("Unsupported edge type")

        i_n = len(lineElem[len(lineElem) - 1]) - 1
        newPD._closed = lineElem[len(lineElem) - 1][i_n]
        return newPD

    def isClosed(self):
        return self._closed

    def pointCount(self):
        return len(self._ptList)

    def point(self, id):
        return self._ptList[id]

    def segmentCount(self):
        return len(self._segmList)

    def segmentType(self, id):
        return self._segmList[id].type

    def segmStartPt(self, id):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
        else:
            startPtId = self._segmList[id].data.p1Index

        return self._ptList[startPtId]

    def segmStartTangent(self, id, normalize=False):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
            endPtId = self._segmList[id].data.endIndex

            tangVec = Geom.Vec(self._ptList[startPtId], self._ptList[endPtId])
            if normalize:
                tangVec.normalize()

            return tangVec
        else:
            return self._segmList[id].data.arc.startTangent()

    def segmStartBisector(self, id, normalize=False):
        if id <= 0:
            return self.segmStartTangent(id, normalize)
        else:
            prevTang = self.segmEndTangent(id - 1, True)
            currTang = self.segmStartTangent(id, True)

            bisect = prevTang + currTang
            if normalize:
                bisect.normalize()

            return bisect

    def segmEndPt(self, id):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.endIndex
        else:
            startPtId = self._segmList[id].data.p3Index

        return self._ptList[startPtId]

    def segmEndTangent(self, id, normalize=False):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
            endPtId = self._segmList[id].data.endIndex

            tangVec = Geom.Vec(self._ptList[endPtId], self._ptList[startPtId])
            if normalize:
                tangVec.normalize()

            return tangVec
        else:
            return -self._segmList[id].data.arc.endTangent()

    def segmEndBisector(self, id, normalize=False):
        lastSegmId = len(self._segmList)
        if id >= lastSegmId:
            return self.segmEndTangent(id, normalize)
        else:
            currTang = self.segmEndTangent(id, True)
            nextTang = self.segmStartTangent(id + 1, True)

            bisect = currTang + nextTang
            if normalize:
                bisect.normalize()

            return bisect

    def segmArc(self, id):
        if self._segmList[id].type == PolylineData.SegmType_Arc:
            return self._segmList[id].data.arc
        else:
            raise TypeError("Segment is not of arc type")

    def _buildEdgeList(self):
        edgeList = []

        for edge in self._segmList:
            edgeList.append(int(edge.type))

        return edgeList

    def _buildSegmentList(self, edgeList):
        self._segmList = []

        segmCount = len(edgeList)
        lastSegmId = segmCount

        startIndex = 0
        for edge in range(lastSegmId):
            edgeType = edgeList[edge]

            if edgeType == PolylineData.SegmType_Line:
                segmData = PolylineData._LineSegmData(startIndex, False)
                self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))

                startIndex += 1
            elif edgeType == PolylineData.SegmType_Arc:
                segmData = PolylineData._ArcSegmData(self._ptList, startIndex, False)
                self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))

                startIndex += 2
            else:
                self._segmList = None
                return

        # Last edge
        edgeType = edgeList[lastSegmId]

        if edgeType == PolylineData.SegmType_Line:
            segmData = PolylineData._LineSegmData(startIndex, self._closed)
            self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))
        elif edgeType == PolylineData.SegmType_Arc:
            segmData = PolylineData._ArcSegmData(self._ptList, startIndex, self._closed)
            self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))
        else:
            self._segmList = None
            return

    @staticmethod
    def prepareParamSet(paramSet, name):
        closedParamName = name + PolylineData._closedSuffix
        ptListParamName = name + PolylineData._ptListSuffix
        edgeListParamName = name + PolylineData._edgeListSuffix

        paramSet.setParameter(closedParamName, False)
        paramSet.setParameter(ptListParamName, None)
        paramSet.setParameter(edgeListParamName, None)

    def writeIntoParamSet(self, paramSet, name):
        closedParamName = name + PolylineData._closedSuffix
        ptListParamName = name + PolylineData._ptListSuffix
        edgeListParamName = name + PolylineData._edgeListSuffix

        paramSet.setParameter(closedParamName, self._closed, False)
        paramSet.setParameter(ptListParamName, self._ptList, False)
        paramSet.setParameter(edgeListParamName, self._buildEdgeList(), False)

    @staticmethod
    def fromParamSet(paramSet, name):
        closedParamName = name + PolylineData._closedSuffix
        ptListParamName = name + PolylineData._ptListSuffix
        edgeListParamName = name + PolylineData._edgeListSuffix

        if not paramSet.hasParameter(closedParamName) or \
                not paramSet.hasParameter(ptListParamName) or \
                not paramSet.hasParameter(edgeListParamName):
            return None

        newPD = PolylineData()

        newPD._closed = paramSet.getBoolParameter(closedParamName)

        newPD._ptList = paramSet.getPointListParameter(ptListParamName)
        if newPD._ptList is None:
            return None

        newPD._buildSegmentList(paramSet.getIntListParameter(edgeListParamName))
        if newPD._segmList is None:
            return None

        return newPD

    def makeCopy(self):
        copyPD = PolylineData()

        copyPD._closed = self._closed

        for pt in self._ptList:
            copyPD._ptList.append(Geom.Pnt(pt))

        for segm in self._segmList:
            if segm.type == PolylineData.SegmType_Line:
                closeSegm = bool(segm.data.endIndex == 0)
                lineData = PolylineData._LineSegmData(segm.data.startIndex, closeSegm)

                copyPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, lineData))
            elif segm.type == PolylineData.SegmType_Arc:
                closeSegm = bool(segm.data.p3Index == 0)
                arcData = PolylineData._ArcSegmData(copyPD._ptList, segm.data.p1Index, closeSegm)

                copyPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, arcData))

        return copyPD


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
                "Faceted ModelAssembler.endModel() must be called after FacetedModelAssembler.beginModel()")

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


class PolylineReader:
    #  ne lamaty, ruky vidorvu
    def __init__(self, polyLine):
        self.polyline = polyLine
        self.segmCount = polyLine.segmentCount()
        self.e = 0.0001
        self.pointListWithDistance = []
        self.segmentsList = []

        if self.segmCount <= 0:
            # print("There are anything segments")
            return

        for segmId in range(self.segmCount):
            segmType = self.polyline.segmentType(segmId)

            if segmType == PolylineData.SegmType_Line:
                startPt = self.polyline.segmStartPt(segmId)
                endPt = self.polyline.segmEndPt(segmId)
                lineSegment = self.SegmLine(startPt, endPt)
                self.segmentsList.append(lineSegment)

            elif segmType == PolylineData.SegmType_Arc:
                arc = PolylineData.segmArc(self.polyline, segmId)
                # print("Radius = ", arc.radius(), ", angle = ", arc.angle(), arc.angle() * 180.0 / math.pi)
                n = int(math.fabs(arc.angle() / (math.acos(((arc.radius() - self.e) / arc.radius())) * 2.0)))
                # print("N = ", n)
                for i in range(n):
                    pnt0 = arc.paramPt(float(i) / float(n))
                    pnt1 = arc.paramPt((float(float(i) + 1.0) / float(n)))
                    if ((float(float(i) + 1.0) / float(n))) <= 1.0:
                        lineSegment = self.SegmLine(pnt0, pnt1)
                        self.segmentsList.append(lineSegment)
                # print("ARC")
            else:
                # print("Unknown segment")
                return

    def getListPointWithDistanceOnPolyline(self, dist, radius, withLast):
        listPoint = []
        for segm in self.segmentsList:
            endPoint = self.segmentsList[len(self.segmentsList) - 1].p1
            if segm == self.segmentsList[len(self.segmentsList) - 1]:
                ifLast = True
            else:
                ifLast = False
            if len(listPoint) >= 1:
                distToPrev = segm.getDistanceToFirstPnt(listPoint[len(listPoint) - 1], dist)
            else:
                distToPrev = segm.getDistanceToFirstPnt(self.segmentsList[0].p0, radius)
            listSegmentPoint = segm.getListPointWithDistance(dist, ifLast, radius, distToPrev)
            if listSegmentPoint is not None:
                for pnt in listSegmentPoint:
                    if withLast is False:
                        pntPro1 = Geom.Pnt(pnt.x(), pnt.y(), 0.0)
                        pntPro2 = Geom.Pnt(endPoint.x(), endPoint.y(), 0.0)
                        if pntPro1.distance(pntPro2) < radius:
                            pass
                        else:
                            listPoint.append(pnt)
                    else:
                        listPoint.append(pnt)
        return listPoint

    class SegmLine:
        def __init__(self, startPnt, endPnt):
            self.p0 = startPnt
            self.p1 = endPnt
            self.p0x = startPnt.x()
            self.p0y = startPnt.y()
            self.p1x = endPnt.x()
            self.p1y = endPnt.y()
            self.vecSegm = Geom.Vec(startPnt, endPnt)
            self.len = self.vecSegm.magnitude()

        def getNumberOfParts(self, dist):
            n = self.vecSegm.magnitude() / dist
            return n

        def getPntByCoef(self, t):
            if t == 0:
                return self.p0
            elif t == 1:
                return self.p1
            elif 0 < t < 1:
                return self.p0.translated(self.vecSegm.scaled(t))
            else:
                # print("COEFICIENT T OUT OF RANGE!!!")
                return None

        def getPntByDist(self, dist):
            if dist == 0:
                return self.p0
            elif dist == self.len:
                return self.p1
            else:
                normalVec = self.vecSegm.normalized()
                resPnt = self.p0.translated(normalVec.multiplied(dist))
                return resPnt

        def getDistanceToFirstPnt(self, q, dist):
            qx = q.x()
            qy = q.y()
            len = 4.0 * math.pow(dist * 0.5, 2)
            p0x = self.p0x
            p0y = self.p0y
            dirVec = self.vecSegm.normalized()
            dx = dirVec.x()
            dy = dirVec.y()
            a = math.pow(dx, 2.0) + math.pow(dy, 2.0)
            b = (-2. * dx * qx) + (p0x * dx) + (dx * p0x) - (2.0 * dy * qy) + (p0y * dy) + (dy * p0y)
            c = (math.pow(qx, 2)) - (2.0 * qx * p0x) + (math.pow(p0x, 2)) + (math.pow(qy, 2)) - (2.0 * qy * p0y) + (
                math.pow(p0y, 2)) - len
            D = math.pow(b, 2) - (4.0 * a * c)
            if D > 0.0:
                t1 = (-b + math.sqrt(D)) / (2.0 * a)
                t2 = (-b - math.sqrt(D)) / (2.0 * a)
                if t1 >= t2:
                    resPnt = self.getPntByDist(math.fabs(t1))
                    vecDist = Geom.Vec(self.p0, resPnt)
                    return vecDist.magnitude()
                elif t1 < t2:
                    resPnt = self.getPntByDist(math.fabs(t2))
                    vecDist = Geom.Vec(self.p0, resPnt)
                    return vecDist.magnitude()
            elif D == 0:
                t = - b / (2.0 * a)
                resPnt = self.getPntByDist(t)
                vecDist = Geom.Vec(self.p0, resPnt)
                return vecDist.magnitude()
            elif D < 0:
                # print("D", D)
                # print("WRONG DISCRIMINANT")
                return None

        def getListPointWithDistance(self, distance, ifLast, rad, startDistance):
            pointList = []

            vecForAngle = Geom.Vec(Geom.Pnt(self.p0.x(), self.p0.y(), self.p0.z()),
                                   Geom.Pnt(self.p1.x(), self.p1.y(), self.p0.z()))
            angle = self.vecSegm.angle(vecForAngle)
            len = self.len
            dist = distance
            radius = rad
            startDist = startDistance
            if angle == 0.5 * math.pi:
                return pointList
            elif angle < 0.00001:
                dist = distance / math.cos(angle)
            if ifLast:
                segmN = int(((len - startDist) / dist) + 1.0)
            elif startDist is not None:
                segmN = int(((len - startDist) / dist) + 1.0)
            else:
                segmN = int(((len - radius) / dist) + 1.0)

            for i in range(segmN):
                resPnt = self.getPntByDist(startDist + (dist * float(i)))
                pointList.append(resPnt)
            return pointList


class BeamWall(lx.PythonElement):
    _interval_param_name = "Interval"
    _height_param_name = "Height"
    _depth_param_name = "Depth of profiles"
    _type_param_name = "Type of construction"
    _profiles_type_param_name = "Profiles type"
    _profiles_size_param_name = "Profiles size"

    #  if second type:
    _distance_between_profiles_param_name = "Distance between profiles"

    _wooden_partitions_type_prop_name = "Type of wooden partitions"
    _rotate_the_construction_prop_name = "Rotate the construction"
    _polyline_param_name = "Polyline"

    def getGlobalClassId(self):
        return Base.GlobalId("{F7EE32DD-C3C3-4653-9044-B371909A7A64}")

    def __init__(self, aArg):
        lx.PythonElement.__init__(self, aArg)
        self.registerPythonClass("BeamWall", "OpenLxApp.PythonElement")

        # Register properties
        self._interval = self.registerPropertyDouble(self._interval_param_name, 2.0,
                                                     lx.Property.VISIBLE, lx.Property.EDITABLE)

        self._height = self.registerPropertyDouble(self._height_param_name, 1.5,
                                                   lx.Property.VISIBLE, lx.Property.EDITABLE)

        self._depth = self.registerPropertyDouble(self._depth_param_name, 1.0,
                                                  lx.Property.VISIBLE, lx.Property.EDITABLE)

        self._type = self.registerPropertyEnum(self._type_param_name, 0, lx.Property.VISIBLE,
                                               lx.Property.EDITABLE, -1)
        self._type.setEmpty()
        self._type.addEntry(lxstr("Berliner Verbau"), -1)
        self._type.addEntry(lxstr("Essener Verbau"), -1)
        self._type.addEntry(lxstr("Hamburger Verbau"), -1)

        # profiles settings
        self._profiles_type = self.registerPropertyEnum(self._profiles_type_param_name, 0,
                                                        lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._profiles_type.setEmpty()
        for i in range(0, 2):
            print(first_types[i])
            self._profiles_type.addEntry(lxstr(first_types[i]), -1)

        self._profiles_size = self.registerPropertyEnum(self._profiles_size_param_name, 0,
                                                        lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._profiles_size.setEmpty()
        for i in range(len(first_typ2)):
            if first_types[0] == first_typ2[i][0]:
                self._profiles_size.addEntry(lxstr(first_typ2[i][1]), -1)

        #  if second type:
        self._distance_between_profiles = self.registerPropertyDouble(self._distance_between_profiles_param_name, 0.02,
                                                                      lx.Property.NOT_VISIBLE, lx.Property.EDITABLE)

        #  wooden partitions
        self._wooden_partitions_type = self.registerPropertyEnum(self._wooden_partitions_type_prop_name, 0,
                                                                 lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._wooden_partitions_type.setEmpty()
        self._wooden_partitions_type.addEntry(lxstr("Least"), -1)
        self._wooden_partitions_type.addEntry(lxstr("Roundwood"), -1)

        self._rotate_the_construction = self.registerPropertyEnum(self._rotate_the_construction_prop_name, 0,
                                                                  lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._rotate_the_construction.setEmpty()
        self._rotate_the_construction.addEntry(lxstr("No"), -1)
        self._rotate_the_construction.addEntry(lxstr("Yes"), -1)

        self._modules = self.registerPropertyDouble("Modules", 0.0, lx.Property.NOT_VISIBLE,
                                                    lx.Property.NOT_EDITABLE, -1)
        self._polyline = self.registerPropertyString(self._polyline_param_name, lxstr(""), lx.Property.NOT_VISIBLE,
                                                     lx.Property.NOT_EDITABLE, -1)  # NOT_VISIBLE

        self._baseData = None
        dataStr = cstr(self._polyline.getValue())
        if dataStr:
            self._baseData = self.readFromString(dataStr)

        self.set_steps()

        

    def set_steps(self):
        self._interval.setSteps(0.1)
        self._height.setSteps(0.1)
        self._depth.setSteps(0.1)
        self._distance_between_profiles.setSteps(0.01)

    def create_profile(self):
        height = self._height.getValue()
        depth = self._depth.getValue()
        if self._type.getValue() is 1:
            profile_type = str(second_types[self._profiles_type.getValue()])
            profile_size = str(second_typ2[self._profiles_size.getValue()][1])
        else:
            profile_type = str(first_types[self._profiles_type.getValue()])
            profile_size = str(first_typ2[self._profiles_size.getValue()][1])

        if profile_type == 'UNP' or profile_type == 'UPE':
            b = float(profiles[str(second_types[self._profiles_type.getValue()]) + ' ' + str(
                second_typ2[self._profiles_size.getValue()][1])]['b'])
            h = float(profiles[str(second_types[self._profiles_type.getValue()]) + ' ' + str(
                second_typ2[self._profiles_size.getValue()][1])]['h'])
            s = float(profiles[str(second_types[self._profiles_type.getValue()]) + ' ' + str(
                second_typ2[self._profiles_size.getValue()][1])]['s'])
            t = float(profiles[str(second_types[self._profiles_type.getValue()]) + ' ' + str(
                second_typ2[self._profiles_size.getValue()][1])]['t'])
            print(b, h, s)
            pnt0 = Geom.Pnt(b, -h * 0.5, 0.0)
            pnt1 = Geom.Pnt(0.0, -h * 0.5, 0.0)
            pnt2 = Geom.Pnt(0.0, h * 0.5, 0.0)
            pnt3 = Geom.Pnt(b, h * 0.5, 0.0)
            pnt4 = Geom.Pnt(b, (h * 0.5) - t, 0.0)
            pnt5 = Geom.Pnt(s, (h * 0.5) - t, 0.0)
            pnt6 = Geom.Pnt(s, -(h * 0.5) + t, 0.0)
            pnt7 = Geom.Pnt(b, -(h * 0.5) + t, 0.0)

            pnt8 = Geom.Pnt(b, -h * 0.5, height + depth)
            pnt9 = Geom.Pnt(0.0, -h * 0.5, height + depth)
            pnt10 = Geom.Pnt(0.0, h * 0.5, height + depth)
            pnt11 = Geom.Pnt(b, h * 0.5, height + depth)
            pnt12 = Geom.Pnt(b, (h * 0.5) - t, height + depth)
            pnt13 = Geom.Pnt(s, (h * 0.5) - t, height + depth)
            pnt14 = Geom.Pnt(s, -(h * 0.5) + t, height + depth)
            pnt15 = Geom.Pnt(b, -(h * 0.5) + t, height + depth)

            element = FacetedModelAssembler(doc)
            element.beginModel()

            element.beginFace()
            element.addVertexList([pnt0, pnt1, pnt2, pnt3, pnt4, pnt5, pnt6, pnt7])
            element.endFace()

            element.beginFace()
            element.addVertexList([pnt15, pnt14, pnt13, pnt12, pnt11, pnt10, pnt9, pnt8])
            element.endFace()

            element.beginFace()
            element.addVertexList([pnt2, pnt1, pnt9, pnt10])
            element.endFace()

            element.beginFace()
            element.addVertexList([pnt10, pnt11, pnt3, pnt2])
            element.endFace()

            element.beginFace()
            element.addVertexList([pnt4, pnt3, pnt11, pnt12])
            element.endFace()

            element.beginFace()
            element.addVertexList([pnt5, pnt4, pnt12, pnt13])
            element.endFace()

            element.beginFace()
            element.addVertexList([pnt6, pnt5, pnt13, pnt14])
            element.endFace()

            element.beginFace()
            element.addVertexList([pnt7, pnt6, pnt14, pnt15])
            element.endFace()

            element.beginFace()
            element.addVertexList([pnt0, pnt7, pnt15, pnt8])
            element.endFace()

            element.beginFace()
            element.addVertexList([pnt1, pnt0, pnt8, pnt9])
            element.endFace()

            return element.endModel()
        else:
            profile = lx.IShapeProfileDef.createIn(doc)
            profile.setValuesFromPredefinedSteelProfile(lxstr(profile_type + ' ' + profile_size))
            eas2 = lx.ExtrudedAreaSolid.createIn(doc)
            eas2.setSweptArea(profile)
            eas2.setExtrudedDirection(Geom.Dir(0, 0, 1))
            eas2.setDepth(height + depth)

            return eas2

    @staticmethod
    def _create_cylinder_element(pnt, length, radius, color=None):
        geom = lx.RightCircularCylinder.createIn(doc)
        geom.setHeight(length)
        geom.setRadius(radius)
        geom.setPosition(Geom.Ax2(pnt, Geom.Dir(0.0, 0.0, 1.0)))

        beam = lx.SubElement.createIn(doc)
        beam.setGeometry(geom)
        if color is not None:
            beam.setDiffuseColor(color)
        return beam

    @staticmethod
    def _create_extruded_element(listPoint, heightStep, color=None):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, Geom.Dir(0, 0, 1), heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)

        # axis = Geom.Ax2(Geom.Pnt(pnt.x(), pnt.y(), pnt.z()), Geom.Dir(0.0, 0.0, 1.0), direction)

        beam = lx.SubElement.createIn(doc)
        beam.setGeometry(geom)
        if color is not None:
            beam.setDiffuseColor(color)
        # beam.setLocalPlacement(axis)
        return beam

    #  methods for first type
    def create_profiles_for_first_type(self, points_list):
        x_retreat = float(profiles[str(first_types[self._profiles_type.getValue()]) + ' ' + str(
            first_typ2[self._profiles_size.getValue()][1])]['h']) * 0.5 - float(
            profiles[str(first_types[self._profiles_type.getValue()]) + ' ' + str(
                first_typ2[self._profiles_size.getValue()][1])]['t'])

        for i in range(len(points_list)):
            if i == 0:
                direction = Geom.Dir(Geom.Vec(points_list[0], points_list[1]))
            elif i == len(points_list) - 1:
                direction = Geom.Dir(Geom.Vec(points_list[len(points_list) - 2],
                                              points_list[len(points_list) - 1]))
            else:
                direction = Geom.Dir(Geom.Vec(points_list[i - 1], points_list[i + 1]))

            rotated_dir = direction.rotated(Geom.Ax1(points_list[i], Geom.Dir(0.0, 0.0, 1.0)), 0.5 * math.pi)
            retreat_vec = Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0),
                                   Geom.Pnt(rotated_dir.x(), rotated_dir.y(), rotated_dir.z()))
            retreat_vec.normalize()
            retreat_vec.scale(x_retreat)

            element = lx.SubElement.createIn(doc)
            profile_geometry = self.create_profile()
            element.setGeometry(profile_geometry)

            axis = Geom.Ax2(
                Geom.Pnt(points_list[i].x(), points_list[i].y(), points_list[i].z() - self._depth.getValue()),
                Geom.Dir(0.0, 0.0, 1.0), direction)
            element.setLocalPlacement(axis)
            element.translate(retreat_vec)

            self.addSubElement(element)

    def create_bulkhead_for_first_type(self, points_list):
        if str(first_types[self._profiles_type.getValue()]) == 'UNP' or str(first_types[self._profiles_type.getValue()]) == 'UPE':
            print('Dont use UNP or UPE profile here')
            return
        wood_element = None

        x_retreat = 0.0

        z_retreat = (float(profiles[str(first_types[self._profiles_type.getValue()]) + ' ' + str(
            first_typ2[self._profiles_size.getValue()][1])]['s']) * 0.5) + float(profiles[str(first_types[self._profiles_type.getValue()]) + ' ' + str(
            first_typ2[self._profiles_size.getValue()][1])]['r'])

        for i in range(len(points_list) - 1):
            if i + 1 == len(points_list):
                print('last')
            if i == 0:
                direction = Geom.Dir(Geom.Vec(points_list[0], points_list[1]))
            else:
                direction = Geom.Dir(Geom.Vec(points_list[i], points_list[i + 1]))

            if self._wooden_partitions_type.getValue() is 0:
                step = 0.2
            else:
                step = 0.1

            for j in range(int(self._height.getValue() / step)):
                if wood_element is None:
                    if self._wooden_partitions_type.getValue() is 0:
                        #  least
                        thickness = 0.05
                        wood_element = self._create_extruded_element([Geom.Pnt(-x_retreat, -step * 0.5, z_retreat),
                                                                      Geom.Pnt(-x_retreat, step * 0.5, z_retreat),
                                                                      Geom.Pnt(-x_retreat + thickness, step * 0.5,
                                                                               z_retreat),
                                                                      Geom.Pnt(-x_retreat + thickness, -step * 0.5,
                                                                               z_retreat)],
                                                                     self._interval.getValue() - (z_retreat * 2))

                        pnt = Geom.Pnt(points_list[i].x(), points_list[i].y(), points_list[i].z() + (step * 0.5))
                        axis = Geom.Ax2(pnt, direction)
                        wood_element.setLocalPlacement(axis)
                        self.addSubElement(wood_element)

                    else:
                        #  roundwood
                        radius = 0.05
                        step = 0.1
                        wood_element = self._create_cylinder_element(Geom.Pnt(-x_retreat + radius, 0.0, z_retreat),
                                                                     self._interval.getValue() - (z_retreat * 2),
                                                                     radius)
                        pnt = Geom.Pnt(points_list[i].x(), points_list[i].y(), points_list[i].z() + (j * step))
                        axis = Geom.Ax2(pnt, direction)
                        wood_element.setLocalPlacement(axis)
                        self.addSubElement(wood_element)
                else:
                    pnt = Geom.Pnt(points_list[i].x(), points_list[i].y(),
                                   points_list[i].z() + (j * step) + (step * 0.5))
                    axis = Geom.Ax2(pnt, direction)
                    wood_part = wood_element.copy()
                    wood_part.setLocalPlacement(axis)
                    self.addSubElement(wood_part)

    #  methods for second type
    def create_profiles_for_second_type(self, points_list):
        x_retreat = float(profiles[str(second_types[self._profiles_type.getValue()]) + ' ' + str(
            second_typ2[self._profiles_size.getValue()][1])]['h']) * 0.5 - float(
            profiles[str(second_types[self._profiles_type.getValue()]) + ' ' + str(
                second_typ2[self._profiles_size.getValue()][1])]['t'])

        profile_type = str(second_types[self._profiles_type.getValue()])
        if profile_type == 'HEA' or profile_type == 'HEB':
            print('Dont use HEA or HEB profile here')
            return

        distance_btwn_profiles = self._distance_between_profiles.getValue()

        for pnt in range(len(points_list)):
            if pnt == 0:
                direction = Geom.Dir(Geom.Vec(points_list[0], points_list[1]))
                first_y_retreat = Geom.Vec(points_list[0], points_list[1])
                first_y_retreat.normalize()
                first_y_retreat.scale(distance_btwn_profiles * 0.5)

                first_x_retreat = Geom.Vec(points_list[0], points_list[1])
                first_x_retreat.rotate(Geom.Ax1(points_list[0], Geom.Dir(0.0, 0.0, 1.0)), math.radians(90))
                first_x_retreat.normalize()
                first_x_retreat.scale(x_retreat)

                axis = Geom.Ax2(
                    Geom.Pnt(points_list[0].x(), points_list[0].y(), points_list[0].z() - self._depth.getValue()),
                    Geom.Dir(0.0, 0.0, 1.0), direction)

                profile_element = lx.SubElement.createIn(doc)
                profile_geometry = self.create_profile()
                profile_element.setGeometry(profile_geometry)

                profile_element.setLocalPlacement(axis)
                profile_element.translate(first_y_retreat)
                profile_element.translate(first_x_retreat)
                self.addSubElement(profile_element)

            elif pnt == len(points_list) - 1:
                last_x_retreat = Geom.Vec(points_list[-2], points_list[-1])
                last_x_retreat.rotate(Geom.Ax1(points_list[-2], Geom.Dir(0.0, 0.0, 1.0)), math.radians(90))
                last_x_retreat.normalize()
                last_x_retreat.scale(x_retreat)

                print("Create last!!!!!!")
                second_profile = lx.SubElement.createIn(doc)
                profile_geometry = self.create_profile()
                second_profile.setGeometry(profile_geometry)

                direction = Geom.Dir(Geom.Vec(points_list[-1], points_list[-2]))
                axis = Geom.Ax2(
                    Geom.Pnt(points_list[pnt].x(), points_list[pnt].y(), points_list[pnt].z() - self._depth.getValue()),
                    Geom.Dir(0.0, 0.0, 1.0), direction)

                last_y_retreat = Geom.Vec(points_list[-1], points_list[-2])
                last_y_retreat.normalize()
                last_y_retreat.scale(distance_btwn_profiles * 0.5)

                second_profile.setLocalPlacement(axis)
                # second_profile.rotate(Geom.Ax1(points_list[pnt], Geom.Dir(0.0, 0.0, 1.0)), math.radians(180.0),
                #                       Geom.CoordSpace_WCS)

                second_profile.translate(last_y_retreat)
                second_profile.translate(last_x_retreat)

                self.addSubElement(second_profile)
            else:
                first_x_retreat = Geom.Vec(points_list[pnt - 1], points_list[pnt + 1])
                first_x_retreat.rotate(Geom.Ax1(points_list[0], Geom.Dir(0.0, 0.0, 1.0)), math.radians(90))
                first_x_retreat.normalize()
                first_x_retreat.scale(x_retreat)

                first_profile = lx.SubElement.createIn(doc)
                profile_geometry = self.create_profile()
                first_profile.setGeometry(profile_geometry)

                second_profile = lx.SubElement.createIn(doc)
                profile_geometry = self.create_profile()
                second_profile.setGeometry(profile_geometry)

                direction = Geom.Dir(Geom.Vec(points_list[pnt - 1], points_list[pnt + 1]))
                axis = Geom.Ax2(
                    Geom.Pnt(points_list[pnt].x(), points_list[pnt].y(), points_list[pnt].z() - self._depth.getValue()),
                    Geom.Dir(0.0, 0.0, 1.0), direction)

                first_y_retreat = Geom.Vec(points_list[pnt - 1], points_list[pnt + 1])
                first_y_retreat.normalize()
                first_y_retreat.scale(distance_btwn_profiles * 0.5)

                last_y_retreat = Geom.Vec(points_list[pnt + 1], points_list[pnt - 1])
                last_y_retreat.normalize()
                last_y_retreat.scale(distance_btwn_profiles * 0.5)

                first_profile.setLocalPlacement(axis)
                second_profile.setLocalPlacement(axis)
                second_profile.rotate(Geom.Ax1(points_list[pnt], Geom.Dir(0.0, 0.0, 1.0)), math.radians(180.0), Geom.CoordSpace_WCS)

                first_profile.translate(first_y_retreat)
                second_profile.translate(last_y_retreat)

                first_profile.translate(first_x_retreat)
                second_profile.translate(first_x_retreat)

                self.addSubElement(first_profile)
                self.addSubElement(second_profile)

            # rotated_dir = direction.rotated(Geom.Ax1(points_list[pnt], Geom.Dir(0.0, 0.0, 1.0)), 0.5 * math.pi)
            # retreat_vec = Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0),
            #                        Geom.Pnt(rotated_dir.x(), rotated_dir.y(), rotated_dir.z()))
            # retreat_vec.normalize()
            # retreat_vec.scale(x_retreat)
            #
            # element = lx.SubElement.createIn(doc)
            # profile_geometry = self.create_profile()
            # element.setGeometry(profile_geometry)
            #
            # axis = Geom.Ax2(
            #     Geom.Pnt(points_list[pnt].x(), points_list[pnt].y(), points_list[pnt].z() - self._depth.getValue()),
            #     Geom.Dir(0.0, 0.0, 1.0), direction)
            # element.setLocalPlacement(axis)
            # element.translate(retreat_vec)
            #
            # self.addSubElement(element)

    def create_bulkhead_for_second_type(self, points_list):
        wood_element = None

        x_retreat = 0.0

        z_retreat = (float(profiles[str(second_types[self._profiles_type.getValue()]) + ' ' + str(
            second_typ2[self._profiles_size.getValue()][1])]['s'])) + (self._distance_between_profiles.getValue() * 0.5)

        for i in range(len(points_list) - 1):
            if i + 1 == len(points_list):
                print('last')
            if i == 0:
                direction = Geom.Dir(Geom.Vec(points_list[0], points_list[1]))
            else:
                direction = Geom.Dir(Geom.Vec(points_list[i], points_list[i + 1]))

            if self._wooden_partitions_type.getValue() is 0:
                step = 0.2
            else:
                step = 0.1

            for j in range(int(self._height.getValue() / step)):
                if wood_element is None:
                    if self._wooden_partitions_type.getValue() is 0:
                        #  least
                        thickness = 0.05
                        wood_element = self._create_extruded_element([Geom.Pnt(-x_retreat, -step * 0.5, z_retreat),
                                                                      Geom.Pnt(-x_retreat, step * 0.5, z_retreat),
                                                                      Geom.Pnt(-x_retreat + thickness, step * 0.5,
                                                                               z_retreat),
                                                                      Geom.Pnt(-x_retreat + thickness, -step * 0.5,
                                                                               z_retreat)],
                                                                     self._interval.getValue() - (z_retreat * 2))

                        pnt = Geom.Pnt(points_list[i].x(), points_list[i].y(), points_list[i].z() + (step * 0.5))
                        axis = Geom.Ax2(pnt, direction)
                        wood_element.setLocalPlacement(axis)
                        self.addSubElement(wood_element)

                    else:
                        #  roundwood
                        radius = 0.05
                        step = 0.1
                        wood_element = self._create_cylinder_element(Geom.Pnt(-x_retreat + radius, 0.0, z_retreat),
                                                                     self._interval.getValue() - (z_retreat * 2),
                                                                     radius)
                        pnt = Geom.Pnt(points_list[i].x(), points_list[i].y(), points_list[i].z() + (j * step))
                        axis = Geom.Ax2(pnt, direction)
                        wood_element.setLocalPlacement(axis)
                        self.addSubElement(wood_element)
                else:
                    pnt = Geom.Pnt(points_list[i].x(), points_list[i].y(),
                                   points_list[i].z() + (j * step) + (step * 0.5))
                    axis = Geom.Ax2(pnt, direction)
                    wood_part = wood_element.copy()
                    wood_part.setLocalPlacement(axis)
                    self.addSubElement(wood_part)

    def create_profiles_for_third_type(self, points_list):
        if self._wooden_partitions_type.getValue() is 0:
            #  least
            bulk_thickness = 0.05

        else:
            #  roundwood
            bulk_thickness = 0.1

        x_retreat = float(profiles[str(first_types[self._profiles_type.getValue()]) + ' ' + str(
            first_typ2[self._profiles_size.getValue()][1])]['h']) * 0.5 + bulk_thickness

        for i in range(len(points_list)):
            if i == 0:
                direction = Geom.Dir(Geom.Vec(points_list[0], points_list[1]))
            elif i == len(points_list) - 1:
                direction = Geom.Dir(Geom.Vec(points_list[len(points_list) - 2],
                                              points_list[len(points_list) - 1]))
            else:
                direction = Geom.Dir(Geom.Vec(points_list[i - 1], points_list[i + 1]))

            rotated_dir = direction.rotated(Geom.Ax1(points_list[i], Geom.Dir(0.0, 0.0, 1.0)), 0.5 * math.pi)
            retreat_vec = Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0),
                                   Geom.Pnt(rotated_dir.x(), rotated_dir.y(), rotated_dir.z()))
            retreat_vec.normalize()
            retreat_vec.scale(x_retreat)

            element = lx.SubElement.createIn(doc)
            profile_geometry = self.create_profile()
            element.setGeometry(profile_geometry)

            axis = Geom.Ax2(
                Geom.Pnt(points_list[i].x(), points_list[i].y(), points_list[i].z() - self._depth.getValue()),
                Geom.Dir(0.0, 0.0, 1.0), direction)
            element.setLocalPlacement(axis)
            element.translate(retreat_vec)

            self.addSubElement(element)

    #  Berliner Verbau
    def first_type(self, points_list):
        self.create_profiles_for_first_type(points_list)
        self.create_bulkhead_for_first_type(points_list)

    #  Essener Verbau
    def second_type(self, points_list):
        self.create_profiles_for_second_type(points_list)
        self.create_bulkhead_for_second_type(points_list)

    #  Hamburger Verbau
    def third_type(self, points_list):
        self.create_profiles_for_third_type(points_list)
        self.create_bulkhead_for_first_type(points_list)

    def _create_construction(self, polyline):
        print("Start")
        construction_type = self._type.getValue()
        interval = self._interval.getValue()

        main_polyline = PolylineReader(polyline)
        points_list = main_polyline.getListPointWithDistanceOnPolyline(interval, 0.0, True)

        if self._rotate_the_construction.getValue() is 1:
            print("<<<< Rotated >>>>")
            points_list.reverse()
        else:
            print("<<<< Not rotated >>>>")

        if construction_type is 0:
            self.first_type(points_list)
        elif construction_type is 1:
            self.second_type(points_list)
        elif construction_type is 2:
            self.third_type(points_list)

    def create_compound(self):
        print('Create')
        polyLine = PolylineData.fromElement(self._baseData)
        self._create_construction(polyLine)

    def _updateGeometry(self):
        with EditMode(self.getDocument()):
            self.removeSubElements()
            self.create_compound()

    def set_interval(self, param):
        min_value = 1.5
        max_value = 2.5
        with EditMode(self.getDocument()):
            self._interval.setValue(clamp(param, min_value, max_value))
            self._updateGeometry()
        if param < min_value:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small, minimum is 1.5 m"))
        elif param > max_value:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big, maximum is 2.5 m"))

    def set_height(self, param):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(param, 0.1, 1000.0))
            self._updateGeometry()

    def set_depth(self, param):
        with EditMode(self.getDocument()):
            self._depth.setValue(clamp(param, 0.0, 100.0))
            self._updateGeometry()

    def set_type(self, param):
        with EditMode(self.getDocument()):
            self._type.setValue(param)
            if param is 0 or param is 2:
                self._distance_between_profiles.setVisible(False)
                print("Set only H profiles types")
                self._profiles_type.setEmpty()
                for i in range(len(first_types)):
                    print(first_types[i])
                    self._profiles_type.addEntry(lxstr(first_types[i]), -1)

                self._profiles_size.setEmpty()
                for i in range(len(first_typ2)):
                    if first_types[0] == first_typ2[i][0]:
                        self._profiles_size.addEntry(lxstr(first_typ2[i][1]), -1)
            elif param is 1:
                print("Set only U profiles types")
                self._distance_between_profiles.setVisible(True)
                self._profiles_type.setEmpty()
                for i in range(len(second_types)):
                    print(second_types[i])
                    self._profiles_type.addEntry(lxstr(second_types[i]), -1)

                self._profiles_size.setEmpty()
                for i in range(len(second_typ2)):
                    if second_types[0] == second_typ2[i][0]:
                        self._profiles_size.addEntry(lxstr(second_typ2[i][1]), -1)
            self._profiles_type.setValue(0)
            self._profiles_size.setValue(0)
            self._updateGeometry()

    def set_profiles_type(self, param):
        with EditMode(self.getDocument()):
            self._profiles_type.setValue(param)
            self._updateGeometry()

    def set_profiles_size(self, param):
        with EditMode(self.getDocument()):
            self._profiles_size.setValue(param)
            self._updateGeometry()

    def set_wooden_partitions_type(self, param):
        with EditMode(self.getDocument()):
            self._wooden_partitions_type.setValue(param)
            self._updateGeometry()

    def set_distance_btwn_profiles(self, param):
        with EditMode(self.getDocument()):
            self._distance_between_profiles.setValue(clamp(param, 0.02, 0.1))
            self._updateGeometry()

    def set_rotate_the_construction(self, param):
        with EditMode(self.getDocument()):
            self._rotate_the_construction.setValue(param)
            print("Param is ", param)
            self._updateGeometry()

    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == BeamWall._interval_param_name:
            self.set_interval(self._interval.getValue())
        elif aPropertyName == BeamWall._height_param_name:
            self.set_height(self._height.getValue())
        elif aPropertyName == BeamWall._depth_param_name:
            self.set_depth(self._depth.getValue())
        elif aPropertyName == BeamWall._type_param_name:
            self.set_type(self._type.getValue())
        elif aPropertyName == BeamWall._profiles_type_param_name:
            self.set_profiles_type(self._profiles_type.getValue())
        elif aPropertyName == BeamWall._profiles_size_param_name:
            self.set_profiles_size(self._profiles_size.getValue())
        elif aPropertyName == BeamWall._distance_between_profiles_param_name:
            self.set_distance_btwn_profiles(self._distance_between_profiles.getValue())
        elif aPropertyName == BeamWall._wooden_partitions_type_prop_name:
            self.set_wooden_partitions_type(self._wooden_partitions_type.getValue())
        elif aPropertyName == BeamWall._rotate_the_construction_prop_name:
            self.set_rotate_the_construction(self._rotate_the_construction.getValue())

    def setPolylineData(self, polylineData):
        if lxstr(self.writeToString(polylineData)) is self._modules.getValue():
            print("Select another polyline")
            return
        self._baseData = polylineData
        self._polyline.setValue(lxstr(self.writeToString(polylineData)))
        self._updateGeometry()

    @staticmethod
    def writeToString(lineData):
        strn = ""
        strn += "{};".format(len(lineData))
        for i in range(len(lineData)):
            if lineData[i][0] == PolylineData.SegmType_Line:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};".format(lineData[i][0], \
                                                                                      lineData[i][1].x(),
                                                                                      lineData[i][1].y(),
                                                                                      lineData[i][1].z(), \
                                                                                      lineData[i][2].x(),
                                                                                      lineData[i][2].y(),
                                                                                      lineData[i][2].z())
            elif lineData[i][0] == PolylineData.SegmType_Arc:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};{7:.5f};{8:.5f};{9:.5f};".format(
                    lineData[i][0], \
                    lineData[i][1].x(), lineData[i][1].y(), lineData[i][1].z(), \
                    lineData[i][2].x(), lineData[i][2].y(), lineData[i][2].z(), \
                    lineData[i][3].x(), lineData[i][3].y(), lineData[i][3].z())
            # if i != len(lineData)-1:
            #     strn += ";"
        i_n = len(lineData[len(lineData) - 1]) - 1
        strn += "{}".format(lineData[len(lineData) - 1][i_n])
        return strn

    @staticmethod
    def readFromString(strn):
        lineData = []
        st = strn.split(";")
        # lenList = int(st[0])
        index = 0
        for i in range(int(st[0])):
            if int(st[index + 1]) == PolylineData.SegmType_Line:
                lineData.append(
                    [int(st[index + 1]), Geom.Pnt(float(st[index + 2]), float(st[index + 3]), float(st[index + 4])), \
                     Geom.Pnt(float(st[index + 5]), float(st[index + 6]), float(st[index + 7]))])
                index += 7
            elif int(st[index + 1]) == PolylineData.SegmType_Arc:
                lineData.append(
                    [int(st[index + 1]), Geom.Pnt(float(st[index + 2]), float(st[index + 3]), float(st[index + 4])), \
                     Geom.Pnt(float(st[index + 5]), float(st[index + 6]), float(st[index + 7])), \
                     Geom.Pnt(float(st[index + 8]), float(st[index + 9]), float(st[index + 10]))])
                index += 10

        i_n = len(lineData[int(st[0]) - 1])
        if st[len(st) - 1] == "True":
            bl = True
        else:
            bl = False
        lineData[int(st[0]) - 1].append(bl)
        # print "i_n={} , st[last]={}".format(i_n, lineData[int(st[0])-1][i_n])

        return lineData

    def polyline(self):
        return self._polyline.getValue()


def getPolylineData(lineSet):
    lineData = []
    # edges = Topo.ShapeTool.getEdges(lineSet.getShape())
    wire = Topo.ShapeTool.isSingleWire(lineSet.getShape())
    if Topo.WireTool.isClosed(wire):
        edges = Topo.WireTool.getEdges(Topo.WireTool.reversed(wire))
    else:
        edges = Topo.WireTool.getEdges(wire)
    # edges = Topo.WireTool.getEdges(wire)

    for edgeIndex in range(len(edges)):
        edge = edges[edgeIndex]

        edgeTypeRes = Topo.EdgeTool.getGeomCurveType(edge)
        if not edgeTypeRes.ok:
            raise RuntimeError("Can't get edge type")

        if edgeTypeRes.type == Geom.CurveType_LINE:
            lineParamRes = Topo.EdgeTool.getLineParameters(edge)
            if not lineParamRes.ok:
                raise RuntimeError("Can't get line parameters")
            p1Res = Topo.EdgeTool.d0(edge, lineParamRes.startParam)
            p2Res = Topo.EdgeTool.d0(edge, lineParamRes.endParam)
            if (not p1Res.ok) or (not p2Res.ok):
                raise RuntimeError("Can't get line start or end point")
            lineData.append([PolylineData.SegmType_Line, Geom.Pnt(p1Res.p), Geom.Pnt(p2Res.p)])

            # print "LineNumb[{}] has type {}: startPt ({}, {}, {}), " \
            #       "\n endPt ({}, {}, {})".format(edgeIndex, lineData[edgeIndex][0],
            #                                      lineData[edgeIndex][1].x(), lineData[edgeIndex][1].y(), lineData[edgeIndex][1].z(),
            #                                      lineData[edgeIndex][2].x(), lineData[edgeIndex][2].y(), lineData[edgeIndex][2].z())

        elif edgeTypeRes.type == Geom.CurveType_CIRCLE:
            arcParamsRes = Topo.EdgeTool.getArcParameters(edge)
            if not arcParamsRes.ok:
                raise RuntimeError("Can't get arc parameters")
            p1Res = Topo.EdgeTool.d0(edge, arcParamsRes.startParam)
            middleParam = (arcParamsRes.startParam + arcParamsRes.endParam) * 0.5
            p2Res = Topo.EdgeTool.d0(edge, middleParam)
            p3Res = Topo.EdgeTool.d0(edge, arcParamsRes.endParam)
            if (not p1Res.ok) or (not p2Res.ok) or (not p3Res.ok):
                raise RuntimeError("Can't get arc start or middle or end point")
            lineData.append([PolylineData.SegmType_Arc, Geom.Pnt(p1Res.p), Geom.Pnt(p2Res.p), Geom.Pnt(p3Res.p)])

            # print "LineNumb[{}] has type {}: startPt ({}, {}, {}), " \
            #       "\n endPt ({}, {}, {})".format(edgeIndex, lineData[edgeIndex][0],
            #                                      lineData[edgeIndex][1].x(), lineData[edgeIndex][1].y(), lineData[edgeIndex][1].z(),
            #                                      lineData[edgeIndex][2].x(), lineData[edgeIndex][2].y(), lineData[edgeIndex][2].z(),
            #                                      lineData[edgeIndex][3].x(), lineData[edgeIndex][3].y(), lineData[edgeIndex][3].z())
        else:
            raise RuntimeError("Unsupported edge type")
    lineData[len(edges) - 1].append(Topo.WireTool.isClosed(wire))
    # print(lineData[len(edges)-1])
    return lineData


def selectPolyline(uidoc):
    uidoc.highlightByShapeType(Topo.ShapeType_WIRE)
    ok = uidoc.pickPoint()
    uidoc.stopHighlightByShapeType()
    if ok:
        return uidoc.getPickedElement()
    else:
        return None


def pickPolyline(uidoc):
    ui.showStatusBarMessage(lxstr("[L] Select base line [Esc] Cancel"))
    lineSet = selectPolyline(uidoc)
    ui.showStatusBarMessage(lxstr(""))

    if lineSet is not None:
        return getPolylineData(lineSet)
    else:
        return None


if __name__ == "__main__":
    doc.registerPythonScript(Base.GlobalId("{0764BABF-B96B-489A-B688-A0EA2573FEEF}"))

    try:
        with EditMode(doc):
            polylineData = pickPolyline(uidoc)
            if polylineData is not None:
                comp = BeamWall(doc)
                comp.setDiffuseColor(Base.Color_fromCdwkColor(4))
                comp.setPolylineData(polylineData)
    except Exception as e:
        print("{}".format(e))
        print(traceback.print_exc())
