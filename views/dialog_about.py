# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_about.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_about(object):
    def setupUi(self, Dialog_about):
        Dialog_about.setObjectName("Dialog_about")
        Dialog_about.resize(466, 266)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_about.sizePolicy().hasHeightForWidth())
        Dialog_about.setSizePolicy(sizePolicy)
        Dialog_about.setMaximumSize(QtCore.QSize(640, 480))
        Dialog_about.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_about)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog_about)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.label = QtWidgets.QLabel(Dialog_about)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_about)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_about)
        self.buttonBox.accepted.connect(Dialog_about.accept)
        self.buttonBox.rejected.connect(Dialog_about.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_about)

    def retranslateUi(self, Dialog_about):
        _translate = QtCore.QCoreApplication.translate
        Dialog_about.setWindowTitle(_translate("Dialog_about", "About VividSTORM"))
        self.plainTextEdit.setPlainText(_translate("Dialog_about", "VividSTORM version 1.3\n"
"\n"
"Copyright © 2015 László Barna, Barna Dudok, Vivien Miczán, András Horváth and István Katona\n"
"This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.\n"
"\n"
"This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details: https://www.gnu.org/licenses/gpl-3.0.html\n"
""))

