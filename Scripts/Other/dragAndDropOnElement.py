# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import traceback

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString
doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()


def printDragAndDropInfo(aScript):
    if aScript.isDragAndDropped():
        print("Script was drag and dropped.\n")
        
        pnt = thisScript.getInsertionPoint()
        print("Insertion point: ", pnt.x(), ", ", pnt.y(), ", ", pnt.z())
        print("\n")
        
        elem = thisScript.getDroppedOnElement()
        if elem is not None:
            print("Dropped on element: ", elem)
            print("\n")
            return elem
        else:
            print("No dropped on element.\n")
    else:
        print("Script was NOT drag and dropped.\n")
        
    return None





if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{008A372E-0A31-49AC-9764-8340C9E49288}"))

    try:
        thisScript = lx.Application.getInstance().getActiveScript()    
        elem = printDragAndDropInfo(thisScript)
    except Exception as e:
        # print(e.message)
        traceback.print_exc()
    finally:
        pass
