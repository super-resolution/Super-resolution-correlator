# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_view_gaussian.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_gaussian(object):
    def setupUi(self, Dialog_gaussian):
        Dialog_gaussian.setObjectName("Dialog_gaussian")
        Dialog_gaussian.resize(346, 201)
        Dialog_gaussian.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_gaussian)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog_gaussian)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.formGroupBox = QtWidgets.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formGroupBox.setFont(font)
        self.formGroupBox.setObjectName("formGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.formGroupBox)
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
        self.label = QtWidgets.QLabel(self.formGroupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.spinBox = QtWidgets.QSpinBox(self.formGroupBox)
        self.spinBox.setMinimum(5)
        self.spinBox.setMaximum(100)
        self.spinBox.setProperty("value", 10)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_3 = QtWidgets.QLabel(self.formGroupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.spinBox_3 = QtWidgets.QSpinBox(self.formGroupBox)
        self.spinBox_3.setMinimum(10)
        self.spinBox_3.setMaximum(100)
        self.spinBox_3.setProperty("value", 20)
        self.spinBox_3.setObjectName("spinBox_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox_3)
        self.horizontalLayout_4.addWidget(self.formGroupBox)
        self.formGroupBox_2 = QtWidgets.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formGroupBox_2.setFont(font)
        self.formGroupBox_2.setObjectName("formGroupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formGroupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.formGroupBox_2)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.formGroupBox_2)
        self.radioButton_2.setObjectName("radioButton_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.radioButton_2)
        self.horizontalLayout_4.addWidget(self.formGroupBox_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.formGroupBox.raise_()
        self.formGroupBox_2.raise_()
        self.verticalLayout.addWidget(self.widget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_gaussian)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_gaussian)
        QtCore.QMetaObject.connectSlotsByName(Dialog_gaussian)

    def retranslateUi(self, Dialog_gaussian):
        _translate = QtCore.QCoreApplication.translate
        Dialog_gaussian.setWindowTitle(_translate("Dialog_gaussian", "Select STORM view mode - Gaussian"))
        self.formGroupBox.setTitle(_translate("Dialog_gaussian", "Settings"))
        self.label_2.setText(_translate("Dialog_gaussian", "Bin number"))
        self.label.setText(_translate("Dialog_gaussian", "Min FWHM value [nm]"))
        self.label_3.setText(_translate("Dialog_gaussian", "Resolution"))
        self.formGroupBox_2.setTitle(_translate("Dialog_gaussian", "Display mode"))
        self.radioButton.setText(_translate("Dialog_gaussian", "Addition"))
        self.radioButton_2.setText(_translate("Dialog_gaussian", "Maximal intensity"))

