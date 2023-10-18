# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom
import math

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

# A Python Command derived from Core.Command
class pyCmdRotateAlongLocalXAxis(Core.Command):
    def __init__(self):
        Core.Command.__init__(self)
        self.elem   = uidoc.getActiveElement()
        self.angle  = math.pi/2.
        self.center = uidoc.getActivePoint()

    def redo(self):  
        if self.elem:
            ax2 = self.elem.getLocalPlacement()
            self.elem.rotate(Geom.Ax1(self.center, ax2.xDirection()), self.angle, Geom.CoordSpace_WCS)
            doc.recompute()
            return True

    def undo(self):
        if self.elem:
            ax2 = self.elem.getLocalPlacement()
            self.elem.rotate(Geom.Ax1(self.center, ax2.xDirection()), -self.angle, Geom.CoordSpace_WCS)
            doc.recompute()
            return True


if __name__ == '__main__':

    app   = lx.Application.getInstance()
    doc   = app.getActiveDocument()    
    uiapp = ui.UIApplication.getInstance()
    uidoc = uiapp.getUIDocument(doc)
    sel   = uidoc.getSelection()
    
    doc.runCommand(pyCmdRotateAlongLocalXAxis().__disown__())
    
 
    
    
    

    
    
    

    
