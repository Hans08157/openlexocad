# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

# from PySide2 import QtCore, QtGui, QtWidgets

def printElemInfo(aMsg, aUIElem):
    print ( str(aMsg) + str(cstr(aUIElem.getAsElement().getGlobalId().toString())) )
    
    
class pyUIElementFilter(ui.UIElementFilter):
    def __init__(self):
        ui.UIElementFilter.__init__(self)

    def filterUIElement(self, aUIElems):        
        for uie in aUIElems:            
            if uie.getAsElement().getGlobalId() == guid:
                print("Passes Filter!!! The callback will notify you.")
                return False

        print("Filtered out!!! No notification for this object.")
        return True


class PySelectionCB(ui.SelectionCB):

    def __init__(self):
        ui.SelectionCB.__init__(self)

    def test(self):
        print("From PySelectionCB: PySelectionCB.test()")

    # Is calling back when one or more UIElement get selected.
    # It only gets called if the UIElement passes the UIElementFilter.
    def onSelected(self, aUIElems):
        for uie in aUIElems:
            printElemInfo("From PySelectionCB -> Selected: ", uie)
    
    # Is calling back when one or more UIElement get deselected.
    # It only gets called if the UIElement passes the UIElementFilter.
    def onDeselected(self, aUIElems):
        for uie in aUIElems:
            printElemInfo("From PySelectionCB -> Deselected: ", uie)
    
    # Is calling back when the selection is cleared.
    # It only gets called if the UIElement passes the UIElementFilter.
    def onClearedSelection(self):
        print("From PySelectionCB -> ClearedSelection")


if __name__ == '__main__':   

    app   = lx.Application.getInstance()
    doc   = app.getActiveDocument()    
    uiapp = ui.UIApplication.getInstance()
    uidoc = uiapp.getUIDocument(doc)
    # Selection is the caller of the SelectionCB callback
    sel   = uidoc.getSelection()
    
    # Add an Element
    e = lx.Element.createIn(doc)
    b = lx.Block.createIn(doc)
    e.setGeometry(b)
    doc.recompute()
    
    guid = e.getGlobalId()

    print()
    print("1: Adding and calling a Python callback")
    print("------------------------------------")

    # Add a Python callback (sel owns the callback, so we
    # disown it first by calling __disown__).

    cb = PySelectionCB()
    sel.addCallback(cb.__disown__(), pyUIElementFilter().__disown__())
    
    # It is possible to deactivate a callback
    #cb.setActive(False)
    
    # It is possible to remove the callback
    #sel.removeCallback(cb)