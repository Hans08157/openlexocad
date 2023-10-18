import  Geom
import  OpenLxApp as lx

##########################################################################
lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString
##########################################################################
doc   = lx.Application.getInstance().getActiveDocument()

if __name__ == '__main__':
    slab = lx.Slab.createIn(doc)
    rec = lx.RectangleProfileDef.createIn(doc)
    rec.setXDim(1)
    rec.setYDim(2)
    eas = lx.ExtrudedAreaSolid.createIn(doc)
    eas.setExtrudedDirection(Geom.Dir(0,0,1))
    eas.setDepth(.2)
    eas.setSweptArea(rec)
    slab.setGeometry(eas)
    doc.recompute()