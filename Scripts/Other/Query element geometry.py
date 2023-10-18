import App, Base, Gui
doc = App.castToDocument(App.GetApplication().getActiveDocument())
elems = Gui.getSelectedElements(doc)
if elems.empty():
    print("No element selected")
else:
    elem = elems[0]
    geo = elem.getGeometry()
    type = geo.getTypeId()
    print(type.getName())

    type = type.getParent()
    print(type.getName())
