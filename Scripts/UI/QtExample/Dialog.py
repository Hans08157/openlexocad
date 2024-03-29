# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/QtExample\Dialog.ui'
#
# Created: Tue Aug 23 12:38:40 2016
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(275, 349)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Color = QtWidgets.QGroupBox(Dialog)
        self.Color.setObjectName("Color")
        self.gridLayout = QtWidgets.QGridLayout(self.Color)
        self.gridLayout.setObjectName("gridLayout")
        self.Red = QtWidgets.QRadioButton(self.Color)
        self.Red.setChecked(True)
        self.Red.setObjectName("Red")
        self.gridLayout.addWidget(self.Red, 0, 0, 1, 1)
        self.Blue = QtWidgets.QRadioButton(self.Color)
        self.Blue.setObjectName("Blue")
        self.gridLayout.addWidget(self.Blue, 2, 0, 1, 1)
        self.Green = QtWidgets.QRadioButton(self.Color)
        self.Green.setObjectName("Green")
        self.gridLayout.addWidget(self.Green, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.Color)
        self.Transparency = QtWidgets.QGroupBox(Dialog)
        self.Transparency.setObjectName("Transparency")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Transparency)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.T0 = QtWidgets.QLabel(self.Transparency)
        self.T0.setObjectName("T0")
        self.horizontalLayout.addWidget(self.T0)
        self.TransparencyRatio = QtWidgets.QSlider(self.Transparency)
        self.TransparencyRatio.setMaximum(100)
        self.TransparencyRatio.setSingleStep(1)
        self.TransparencyRatio.setPageStep(20)
        self.TransparencyRatio.setOrientation(QtCore.Qt.Horizontal)
        self.TransparencyRatio.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.TransparencyRatio.setTickInterval(20)
        self.TransparencyRatio.setObjectName("TransparencyRatio")
        self.horizontalLayout.addWidget(self.TransparencyRatio)
        self.T100 = QtWidgets.QLabel(self.Transparency)
        self.T100.setObjectName("T100")
        self.horizontalLayout.addWidget(self.T100)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addWidget(self.Transparency)
        self.Size = QtWidgets.QGroupBox(Dialog)
        self.Size.setObjectName("Size")
        self.formLayout = QtWidgets.QFormLayout(self.Size)
        self.formLayout.setObjectName("formLayout")
        self.Length = QtWidgets.QLabel(self.Size)
        self.Length.setObjectName("Length")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Length)
        self.L = QtWidgets.QDoubleSpinBox(self.Size)
        self.L.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.L.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.L.setMinimum(0.5)
        self.L.setMaximum(1000.0)
        self.L.setProperty("value", 2.0)
        self.L.setObjectName("L")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.L)
        self.Width = QtWidgets.QLabel(self.Size)
        self.Width.setObjectName("Width")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Width)
        self.W = QtWidgets.QDoubleSpinBox(self.Size)
        self.W.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.W.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.W.setMinimum(0.5)
        self.W.setMaximum(1000.0)
        self.W.setProperty("value", 2.0)
        self.W.setObjectName("W")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.W)
        self.Height = QtWidgets.QLabel(self.Size)
        self.Height.setObjectName("Height")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Height)
        self.H = QtWidgets.QDoubleSpinBox(self.Size)
        self.H.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.H.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.H.setMinimum(0.5)
        self.H.setMaximum(1000.0)
        self.H.setProperty("value", 2.0)
        self.H.setObjectName("H")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.H)
        self.verticalLayout.addWidget(self.Size)
        self.Widget = QtWidgets.QWidget(Dialog)
        self.Widget.setObjectName("Widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(157, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.OK = QtWidgets.QPushButton(self.Widget)
        self.OK.setObjectName("OK")
        self.horizontalLayout_2.addWidget(self.OK)
        self.verticalLayout.addWidget(self.Widget)
        self.Length.setBuddy(self.L)
        self.Width.setBuddy(self.W)
        self.Height.setBuddy(self.H)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.OK, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.Red, self.Green)
        Dialog.setTabOrder(self.Green, self.Blue)
        Dialog.setTabOrder(self.Blue, self.TransparencyRatio)
        Dialog.setTabOrder(self.TransparencyRatio, self.L)
        Dialog.setTabOrder(self.L, self.W)
        Dialog.setTabOrder(self.W, self.H)
        Dialog.setTabOrder(self.H, self.OK)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Create a cube", None, -1))
        self.Color.setTitle(QtWidgets.QApplication.translate("Dialog", "Color", None, -1))
        self.Red.setText(QtWidgets.QApplication.translate("Dialog", "Red", None, -1))
        self.Blue.setText(QtWidgets.QApplication.translate("Dialog", "Blue", None, -1))
        self.Green.setText(QtWidgets.QApplication.translate("Dialog", "Green", None, -1))
        self.Transparency.setTitle(QtWidgets.QApplication.translate("Dialog", "Transparency", None, -1))
        self.T0.setText(QtWidgets.QApplication.translate("Dialog", "0", None, -1))
        self.T100.setText(QtWidgets.QApplication.translate("Dialog", "100", None, -1))
        self.Size.setTitle(QtWidgets.QApplication.translate("Dialog", "Size", None, -1))
        self.Length.setText(QtWidgets.QApplication.translate("Dialog", "&Length", None, -1))
        self.Width.setText(QtWidgets.QApplication.translate("Dialog", "&Width", None, -1))
        self.Height.setText(QtWidgets.QApplication.translate("Dialog", "&Height", None, -1))
        self.OK.setText(QtWidgets.QApplication.translate("Dialog", "Ok", None, -1))

