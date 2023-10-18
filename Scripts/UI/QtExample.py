# Import Lexocad libraries
import Base
import OpenLxApp as lx
# Import the Qt libraries and the dialog
from PySide2.QtWidgets import *
from QtExample.Dialog import *


# Setup the dialog
class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    # Execute the dialog
    dialog = Dialog()
    result = dialog.exec_()

    if result == QDialog.Accepted:
        # Get the color from the dialog
        Color = Base.Color(255, 0, 0) if dialog.Red.isChecked() \
            else Base.Color(0, 255, 0) if dialog.Green.isChecked() \
            else Base.Color(0, 0, 255)

        # Get the transparency from the dialog
        Ratio = dialog.TransparencyRatio.value()

        # Get the measures from the dialog
        L = dialog.L.value()
        W = dialog.W.value()
        H = dialog.H.value()

        # Create the geometry in the document
        doc = lx.Application.getInstance().getActiveDocument()
        block = lx.Block.createIn(doc)

        # Assign the properties to the geometry, as set in the dialog
        block.setXLength(L)
        block.setYLength(W)
        block.setZLength(H)

        # Create the element in the document, assign the geometry to it
        elem = lx.Element.createIn(doc)
        elem.setGeometry(block)

        # Assign the properties to the element, as set in the dialog
        elem.setDiffuseColor(Color)
        elem.setTransparency(Ratio)

        # Recompute the document
        doc.recompute()