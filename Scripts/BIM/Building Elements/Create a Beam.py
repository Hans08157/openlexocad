#===============================================================================
#
# CREATING A BEAM
#
#===============================================================================

import OpenLxApp as lx
import OpenLxUI  as ui
import Geom
import math

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()
uiapp = ui.UIApplication.getInstance()
uidoc = uiapp.getUIDocument(doc)
sel   = uidoc.getSelection()

#----------------------------------------------------------------------------------------
# 1. Pick two points 
#----------------------------------------------------------------------------------------
def pickTwoPoints():
    ok = uidoc.pickPoint()
    if not ok:
       return False
    p1 = uidoc.getPickedPoint()
    uidoc.drawRubberBand(p1)
    ok = uidoc.pickPoint()
    uidoc.removeRubberBand()
    if not ok:
       return False    
    p2 = uidoc.getPickedPoint()
    return p1, p2
    

#----------------------------------------------------------------------------------------
# 2. Create Beam  
#----------------------------------------------------------------------------------------
points = pickTwoPoints()

manualCreation = False

if points != False and manualCreation:
    res = Geom.GeomTools.makeAxisPlacementFrom2Points(points[0], points[1])
    if res.ok:
        profile = lx.RectangleProfileDef.createIn(doc)
        profile.setXDim(.1)
        profile.setYDim(.2)
        eas = lx.ExtrudedAreaSolid.createIn(doc)
        eas.setSweptArea(profile)
        eas.setExtrudedDirection(Geom.Dir(0,0,1))
        eas.setDepth(res.xLength)
        # Place extrusion in yz-plane
        eas.setPosition(Geom.Ax2( Geom.Pnt(0,0,0), Geom.Dir(1,0,0), Geom.Dir(0,1,0)))
    
        beam = lx.Beam.createIn(doc)
        beam.setGeometry(eas)
        beam.setLocalPlacement(res.ax2)
        doc.recompute()
    else:
        print("Error")

elif points != False and not manualCreation:
    beam = lx.Beam.buildFrom2Points(doc, .1, .2, points[0], points[1])
    if beam:
        doc.recompute()
    else:
        print("Error")

else:
        print("Error")
