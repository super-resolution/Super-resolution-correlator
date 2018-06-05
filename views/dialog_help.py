# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_help.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_help_2(object):
    def setupUi(self, Dialog_help_2):
        Dialog_help_2.setObjectName("Dialog_help_2")
        Dialog_help_2.resize(274, 258)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_help_2.sizePolicy().hasHeightForWidth())
        Dialog_help_2.setSizePolicy(sizePolicy)
        Dialog_help_2.setMaximumSize(QtCore.QSize(640, 480))
        Dialog_help_2.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_help_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Dialog_help = QtWidgets.QPlainTextEdit(Dialog_help_2)
        self.Dialog_help.setObjectName("Dialog_help")
        self.verticalLayout.addWidget(self.Dialog_help)
        self.label = QtWidgets.QLabel(Dialog_help_2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_help_2)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_help_2)
        self.buttonBox.accepted.connect(Dialog_help_2.accept)
        self.buttonBox.rejected.connect(Dialog_help_2.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_help_2)

    def retranslateUi(self, Dialog_help_2):
        _translate = QtCore.QCoreApplication.translate
        Dialog_help_2.setWindowTitle(_translate("Dialog_help_2", "VividSTORM help"))
        self.Dialog_help.setPlainText(_translate("Dialog_help_2", "VividSTORM User Guide can be downloaded from:\n"
"www.katonalab/VividSTORM\n"
"\n"
""))

