# OpenLexocad libraries
import Core
import OpenLxApp as lx
import OpenLxUI  as ui

# A Python Command derived from Core.Command
class pyCmdAddWall(Core.Command):
    def __init__(self):
        Core.Command.__init__(self)
        self.isRedo = False
        self.wall   = None

    def redo(self):  
        if self.isRedo:
            doc.removeObject(self.wall)
            doc.recompute()
            return True
        else:
            # Create a WallStandardCase
            self.wall = lx.WallStandardCase.createIn(doc)
            b = lx.Block.createIn(doc)
            b.setLength(5)
            b.setWidth(0.2)
            b.setHeight(2.8)
            self.wall.setGeometry(b)
            doc.recompute() 
            return True

    def undo(self):
        doc.removeObject(self.wall)
        doc.recompute()
        return True
        
if __name__ == '__main__': 
    app   = lx.Application.getInstance()
    doc   = app.getActiveDocument()  
    # Run the command in the Document. 
    # The Document owns the command.  
    # This is why we have to disown it from Python.
    doc.runCommand(pyCmdAddWall().__disown__())

   
    
    
    

    
    
    

    
