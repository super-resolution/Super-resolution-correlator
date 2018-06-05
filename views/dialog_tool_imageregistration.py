# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_imageregistration.ui'
#
# Created: Sat Oct 10 18:11:35 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig)

class Ui_Dialog_imageregistration(object):
    def setupUi(self, Dialog_imageregistration):
        Dialog_imageregistration.setObjectName("Dialog_imageregistration")
        Dialog_imageregistration.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_imageregistration.resize(658, 123)
        Dialog_imageregistration.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")

        self.formLayout = QtWidgets.QFormLayout(Dialog_imageregistration)
        self.formLayout.setObjectName("formLayout")
        self.widget = QtWidgets.QWidget(Dialog_imageregistration)
        self.widget.setObjectName("widget")
        self.formLayout_2 = QtWidgets.QFormLayout(self.widget)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_3.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.comboBox_storm_channel_changer = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_storm_channel_changer.setObjectName("comboBox_storm_channel_changer")
        self.gridLayout_3.addWidget(self.comboBox_storm_channel_changer, 1, 1, 1, 1)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.comboBox_confocal_channel_changer = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_confocal_channel_changer.setObjectName("comboBox_confocal_channel_changer")
        self.gridLayout_4.addWidget(self.comboBox_confocal_channel_changer, 0, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_delete_markers = QtWidgets.QPushButton(self.widget)
        self.pushButton_delete_markers.setObjectName("pushButton_delete_markers")
        self.horizontalLayout.addWidget(self.pushButton_delete_markers)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_manual_selection = QtWidgets.QPushButton(self.widget)
        self.pushButton_manual_selection.setObjectName("pushButton_manual_selection")
        self.horizontalLayout.addWidget(self.pushButton_manual_selection)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_automatic_selection = QtWidgets.QPushButton(self.widget)
        self.pushButton_automatic_selection.setObjectName("pushButton_automatic_selection")
        self.horizontalLayout.addWidget(self.pushButton_automatic_selection)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_Registration = QtWidgets.QPushButton(self.widget)
        self.pushButton_Registration.setObjectName("pushButton_Registration")
        self.horizontalLayout.addWidget(self.pushButton_Registration)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.gridLayout)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.widget)

        self.retranslateUi(Dialog_imageregistration)
        QtCore.QMetaObject.connectSlotsByName(Dialog_imageregistration)

    def retranslateUi(self, Dialog_imageregistration):
        Dialog_imageregistration.setWindowTitle(_translate("Dialog_imageregistration", "Image registration tool", None))
        self.groupBox_3.setTitle(_translate("Dialog_imageregistration", "STORM channel", None))
        self.groupBox_2.setTitle(_translate("Dialog_imageregistration", "Confocal channel", None))
        self.pushButton_delete_markers.setText(_translate("Dialog_imageregistration", "Delete markers", None))
        self.pushButton_manual_selection.setText(_translate("Dialog_imageregistration", "Manual selection", None))
        self.pushButton_automatic_selection.setText(_translate("Dialog_imageregistration", "Automatic selection", None))
        self.pushButton_Registration.setText(_translate("Dialog_imageregistration", "Registration", None))

