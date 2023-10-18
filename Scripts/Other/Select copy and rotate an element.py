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
    # The copy vector
    vec  = Geom.Vec(0,0,1)
    # The rotation axis
    ax1 = Geom.Ax1(Geom.Pnt(0,0,0),Geom.Dir(0,0,1))
    # The concatenated copy vector
    copyVec  = Geom.Vec(0,0,0)
    # The number of copies
    nbCopies = 36
    # Concatenated rotation
    rot = 0.0
    for n in range(nbCopies):
        for e in elems:
            # Make a copy of the element. The method returns an object
            copyElem = doc.copyObject(e)
            # Cast the object to an element
            copyElem = App.castToElement(copyElem)
            # Sum up the copy vector
            copyVec.add(vec)
            # Translate  an d rotate the copy
            rot += math.pi/18.
            copyElem.placement.translate(copyVec,Base.CoordSpace_WCS)
            copyElem.placement.rotate(ax1,rot,Base.CoordSpace_WCS)
    doc.recompute()