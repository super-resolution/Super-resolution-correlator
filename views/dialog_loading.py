# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_loading.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_loading(object):
    def setupUi(self, Dialog_loading):
        Dialog_loading.setObjectName("Dialog_loading")
        Dialog_loading.resize(255, 120)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_loading.sizePolicy().hasHeightForWidth())
        Dialog_loading.setSizePolicy(sizePolicy)
        Dialog_loading.setMaximumSize(QtCore.QSize(640, 480))
        Dialog_loading.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_loading)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog_loading)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_loading)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_loading)
        self.buttonBox.accepted.connect(Dialog_loading.accept)
        self.buttonBox.rejected.connect(Dialog_loading.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_loading)

    def retranslateUi(self, Dialog_loading):
        pass

