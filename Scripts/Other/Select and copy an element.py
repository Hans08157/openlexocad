import App, Base, Gui

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
    vec  = Geom.Vec(10,10,0)
    # The concatenated copy vector
    copyVec  = Geom.Vec(0,0,0)
    # The number of copies
    nbCopies = 40
    for n in range(nbCopies):
        for e in elems:
            # Make a copy of the element. The method returns an object
            copyElem = doc.copyObject(e)
            # Cast the object to an element
            copyElem = App.castToElement(copyElem)
            # Sum up the copy vector
            copyVec.add(vec)
            # Translate the copy
            copyElem.placement.translate(copyVec,Base.CoordSpace_WCS)		
    doc.recompute()


