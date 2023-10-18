import OpenLxApp as lx
import OpenLxCmd as cmd

import Base

import os

from PySide2.QtWidgets import *
from QtExample2.Dialog import *


# Setup the dialog
class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.fileChoose.clicked.connect(self.showFileDialog)

    def showFileDialog(self):
        initialDir = "/"
        fileName = QFileDialog.getOpenFileName(self, "Open LXZ", initialDir, "Lexocad Files (*.lxz)")[0]
        self.fileEdit.setText(fileName)
        self.OK.setDisabled(not fileName)  # Disable OK button if user did not choose anything


if __name__ == '__main__':
    # Execute the dialog
    dialog = Dialog()
    result = dialog.exec_()

    if result == QDialog.Accepted:
        lxz_file = str(dialog.fileEdit.text())
        if os.path.isfile(lxz_file):
            cmd = cmd.CmdImportFile(Base.StringTool.toString(lxz_file), "lxz", True, True)
            doc = lx.Application.getInstance().getActiveDocument()
            doc.runCommand(cmd)