#===============================================================================
#
# CREATING A LINE (TRIMMED CURVE)
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Geom

def pyCreateTrimmedCurve(aDoc, aFromPnt, aToPnt):
    res = Geom.Vec(aToPnt.xyz() - aFromPnt.xyz())
    dir = Geom.Dir(res.normalized())

    line = lx.Line.createIn(aDoc)
    line.setPoint(aFromPnt)
    line.setDirection(dir)

    tc = lx.TrimmedCurve.createIn(aDoc)
    tc.setBasisCurve(line)
    tc.setTrim1(0)
    tc.setTrim2(res.magnitude())
    return tc

#----------------------------
# 2. Get the active document.
#----------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

#--------------------------------------------
# 3. Define start and end point of the curve.
#--------------------------------------------
fromPnt = Geom.Pnt(0, 0, 0)
toPnt = Geom.Pnt(5, 5, 0)

#--------------------------------------
# 4. Create a geometry in the document.
#--------------------------------------
tc = pyCreateTrimmedCurve(doc, fromPnt, toPnt)

# There is also a built-in function that does the same:
#tc = lx.createTrimmedCurve(doc, fromPnt, toPnt)

#--------------------------------------------------------------------
# 5. Create an element in the document and assign the geometry to it.
#--------------------------------------------------------------------
elem = lx.Element.createIn(doc)
elem.setGeometry(tc)

#--------------------------- 
# 6. Recompute the document.
#---------------------------
doc.recompute()