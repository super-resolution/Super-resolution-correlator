# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_error.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_error(object):
    def setupUi(self, Dialog_error):
        Dialog_error.setObjectName("Dialog_error")
        Dialog_error.resize(255, 120)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_error.sizePolicy().hasHeightForWidth())
        Dialog_error.setSizePolicy(sizePolicy)
        Dialog_error.setMaximumSize(QtCore.QSize(640, 480))
        Dialog_error.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_error)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog_error)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_error)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_error)
        self.buttonBox.accepted.connect(Dialog_error.accept)
        self.buttonBox.rejected.connect(Dialog_error.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_error)

    def retranslateUi(self, Dialog_error):
        pass

