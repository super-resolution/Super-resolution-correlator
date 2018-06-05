# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_view_3d.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_3d(object):
    def setupUi(self, Dialog_3d):
        Dialog_3d.setObjectName("Dialog_3d")
        Dialog_3d.resize(331, 163)
        Dialog_3d.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_3d)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog_3d)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formGroupBox = QtWidgets.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formGroupBox.setFont(font)
        self.formGroupBox.setObjectName("formGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.formGroupBox)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(9, 9, 9, 9)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.formGroupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.formGroupBox)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(100)
        self.spinBox_2.setObjectName("spinBox_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox_2)
        self.horizontalLayout.addWidget(self.formGroupBox)
        self.formGroupBox_2 = QtWidgets.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formGroupBox_2.setFont(font)
        self.formGroupBox_2.setCheckable(True)
        self.formGroupBox_2.setObjectName("formGroupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formGroupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.formGroupBox_2)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.spinBox_3 = QtWidgets.QSpinBox(self.formGroupBox_2)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(100)
        self.spinBox_3.setProperty("value", 70)
        self.spinBox_3.setObjectName("spinBox_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox_3)
        self.horizontalLayout.addWidget(self.formGroupBox_2)
        spacerItem = QtWidgets.QSpacerItem(0, 70, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_3d)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_3d)
        self.buttonBox.accepted.connect(Dialog_3d.accept)
        self.buttonBox.rejected.connect(Dialog_3d.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_3d)

    def retranslateUi(self, Dialog_3d):
        _translate = QtCore.QCoreApplication.translate
        Dialog_3d.setWindowTitle(_translate("Dialog_3d", "Select STORM view mode - 3D"))
        self.formGroupBox.setTitle(_translate("Dialog_3d", "Settings"))
        self.label_2.setText(_translate("Dialog_3d", "Size"))
        self.formGroupBox_2.setTitle(_translate("Dialog_3d", "Show convex hull"))
        self.label_3.setText(_translate("Dialog_3d", "Transparency"))

