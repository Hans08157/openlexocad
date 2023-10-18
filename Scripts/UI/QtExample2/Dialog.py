# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/s\Dialog.ui'
#
# Created: Fri Oct 07 19:59:50 2016
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(355, 118)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Size = QtWidgets.QGroupBox(Dialog)
        self.Size.setObjectName("Size")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Size)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fileEdit = QtWidgets.QLineEdit(self.Size)
        self.fileEdit.setEnabled(True)
        self.fileEdit.setReadOnly(True)
        self.fileEdit.setObjectName("fileEdit")
        self.horizontalLayout.addWidget(self.fileEdit)
        self.fileChoose = QtWidgets.QToolButton(self.Size)
        self.fileChoose.setObjectName("fileChoose")
        self.horizontalLayout.addWidget(self.fileChoose)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addWidget(self.Size)
        self.Widget = QtWidgets.QWidget(Dialog)
        self.Widget.setObjectName("Widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.OK = QtWidgets.QPushButton(self.Widget)
        self.OK.setEnabled(False)
        self.OK.setObjectName("OK")
        self.horizontalLayout_2.addWidget(self.OK)
        self.Cancel = QtWidgets.QPushButton(self.Widget)
        self.Cancel.setEnabled(True)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout_2.addWidget(self.Cancel)
        self.verticalLayout.addWidget(self.Widget)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.OK, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QObject.connect(self.Cancel, QtCore.SIGNAL("clicked()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.fileEdit, self.fileChoose)
        Dialog.setTabOrder(self.fileChoose, self.OK)
        Dialog.setTabOrder(self.OK, self.Cancel)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Open a file", None, -1))
        self.Size.setTitle(QtWidgets.QApplication.translate("Dialog", "File", None, -1))
        self.fileEdit.setPlaceholderText(QtWidgets.QApplication.translate("Dialog", "Choose a .lxz file", None, -1))
        self.fileChoose.setText(QtWidgets.QApplication.translate("Dialog", "...", None, -1))
        self.OK.setText(QtWidgets.QApplication.translate("Dialog", "Ok", None, -1))
        self.Cancel.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

