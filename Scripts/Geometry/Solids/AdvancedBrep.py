#===============================================================================
#
# CREATING AN ADVANCEDBREP
#
#===============================================================================

import OpenLxApp as lx
import OpenLxUI  as ui
import Geom, Topo
import math

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()

c = Geom.Circ()
c.setRadius(2)
f = Topo.FaceTool.makeCylindricalFace(c, 0, math.pi, 2)
s = Topo.ShapeTool.makeShape(f)
error = Base.String()
res = Topo.ShapeTool.thickenSheets(error, s, .2)
brep = lx.AdvancedBrep.createIn(doc)
brep.setShape(res)

elem  = lx.Element.createIn(doc)
elem.setGeometry(brep)
doc.recompute()