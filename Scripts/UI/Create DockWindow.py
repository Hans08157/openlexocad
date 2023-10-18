import Base
import Gui
import OpenLxApp as lx
import OpenLxUI as ui
# Import the Qt libraries and the dialog
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2 import shiboken2

lexocadsingleton = Gui.LexocadSingleton.instance()
parentWin = lexocadsingleton.getParentForDialogs()
# wrap the raw ptr to a PySide-Object
ptr = int(parentWin)
mainWin = shiboken2.wrapInstance(int(ptr), QMainWindow)

dockWin = QDockWidget("Dockable", mainWin)
mainWin.addDockWidget(Qt.LeftDockWidgetArea, dockWin)
dockedWidget = QWidget(mainWin)
dockWin.setWidget(dockedWidget)
dockedWidget.setLayout(QVBoxLayout())
for i in range(5):
    dockedWidget.layout().addWidget(QPushButton("{}".format(i)))
dockWin.show()


