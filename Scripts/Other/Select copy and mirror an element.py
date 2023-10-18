import App, Base, Geom, Gui
import math

# Get the active Document
doc = App.castToDocument(App.GetApplication().getActiveDocument())

# Get the selected elements
elems =  Gui.getSelectedElements(doc)
if(elems.size() == 0):
    title = Base.StringTool.toString("Lexocad")
    text = Base.StringTool.toString("Please select at least one element and try again.")
    ok = Gui.showMessageBox(title, text)
else:
    # The mirror plane
    ax2 = Geom.Ax2(Geom.Pnt(0,0,0),Geom.Dir(1,0,0))
    for e in elems:
        # Mirror the element. The method returns a mirrored copy of the element
        mirroredElem = App.ElementTool.mirrored(e,ax2)
        # Check for error
        if(mirroredElem == None): print("Could not mirror element")
    doc.recompute()