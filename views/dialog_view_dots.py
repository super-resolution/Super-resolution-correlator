# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_view_dots.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_dots(object):
    def setupUi(self, Dialog_dots):
        Dialog_dots.setObjectName("Dialog_dots")
        Dialog_dots.resize(220, 128)
        Dialog_dots.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_dots)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog_dots)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(Dialog_dots)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_dots)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_dots)
        self.buttonBox.accepted.connect(Dialog_dots.accept)
        self.buttonBox.rejected.connect(Dialog_dots.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_dots)

    def retranslateUi(self, Dialog_dots):
        _translate = QtCore.QCoreApplication.translate
        Dialog_dots.setWindowTitle(_translate("Dialog_dots", "Select STORM view mode - Dots"))
        self.label.setText(_translate("Dialog_dots", "Dot size [nm]"))

