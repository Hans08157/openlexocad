import Base, Geom, Topo
import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()
uiapp = ui.UIApplication.getInstance()
uidoc = uiapp.getUIDocument(doc)

def pickElement():
    uidoc.highlightByShapeType(Topo.ShapeType_SHAPE)
    ok = uidoc.pickPoint()
    if not ok:
        uidoc.stopHighlightByShapeType()
        return None

    uidoc.stopHighlightByShapeType()
    return uidoc.getPickedElement()

ui.showStatusBarMessage(lxstr("Select an element..."))
elem = pickElement()
if elem is not None:
    ui.showStatusBarMessage(lxstr("Select a path..."))
    path = pickElement()
    if path is not None:
        mycmd = cmd.CmdCopyAlongCurve(elem, path, 25)
        mycmd.redo()

ui.showStatusBarMessage(lxstr(""))