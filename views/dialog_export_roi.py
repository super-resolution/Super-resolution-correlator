# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_export_roi.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_Export_Roi(object):
    def setupUi(self, Dialog_Export_Roi):
        Dialog_Export_Roi.setObjectName("Dialog_Export_Roi")
        Dialog_Export_Roi.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_Export_Roi.setEnabled(True)
        Dialog_Export_Roi.resize(600, 390)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        Dialog_Export_Roi.setFont(font)
        Dialog_Export_Roi.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Dialog_Export_Roi.setStyleSheet("\n"
"QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:checked{\n"
"    background-color: rgb(7, 2, 148);\n"
"}\n"
"QPushButton{\n"
"    color: rgb(255, 170,0);\n"
"}\n"
"QPushButton:disabled{\n"
"    color: rgb(96,96,96);\n"
"}")
        Dialog_Export_Roi.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_Export_Roi)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(Dialog_Export_Roi)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.label_6 = QtWidgets.QLabel(Dialog_Export_Roi)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.line_3 = QtWidgets.QFrame(Dialog_Export_Roi)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog_Export_Roi)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.pushButton_Mode_FreeHand = QtWidgets.QPushButton(Dialog_Export_Roi)
        self.pushButton_Mode_FreeHand.setEnabled(False)
        self.pushButton_Mode_FreeHand.setObjectName("pushButton_Mode_FreeHand")
        self.horizontalLayout.addWidget(self.pushButton_Mode_FreeHand)
        self.pushButton_Mode_Rect = QtWidgets.QPushButton(Dialog_Export_Roi)
        self.pushButton_Mode_Rect.setCheckable(True)
        self.pushButton_Mode_Rect.setChecked(True)
        self.pushButton_Mode_Rect.setObjectName("pushButton_Mode_Rect")
        self.horizontalLayout.addWidget(self.pushButton_Mode_Rect)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(Dialog_Export_Roi)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Dialog_Export_Roi)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.checkBox_save_loc = QtWidgets.QCheckBox(Dialog_Export_Roi)
        self.checkBox_save_loc.setChecked(True)
        self.checkBox_save_loc.setObjectName("checkBox_save_loc")
        self.verticalLayout_4.addWidget(self.checkBox_save_loc)
        self.checkBox_save_dstorm_image = QtWidgets.QCheckBox(Dialog_Export_Roi)
        self.checkBox_save_dstorm_image.setChecked(True)
        self.checkBox_save_dstorm_image.setObjectName("checkBox_save_dstorm_image")
        self.verticalLayout_4.addWidget(self.checkBox_save_dstorm_image)
        self.checkBox_save_sim_image = QtWidgets.QCheckBox(Dialog_Export_Roi)
        self.checkBox_save_sim_image.setChecked(True)
        self.checkBox_save_sim_image.setObjectName("checkBox_save_sim_image")
        self.verticalLayout_4.addWidget(self.checkBox_save_sim_image)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(Dialog_Export_Roi)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.render_px_size = QtWidgets.QDoubleSpinBox(Dialog_Export_Roi)
        self.render_px_size.setDecimals(8)
        self.render_px_size.setObjectName("render_px_size")
        self.horizontalLayout_5.addWidget(self.render_px_size)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(Dialog_Export_Roi)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.lineEdit_path = QtWidgets.QLineEdit(Dialog_Export_Roi)
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.verticalLayout_5.addWidget(self.lineEdit_path)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pushButton_Save = QtWidgets.QPushButton(Dialog_Export_Roi)
        self.pushButton_Save.setObjectName("pushButton_Save")
        self.horizontalLayout_4.addWidget(self.pushButton_Save)
        self.pushButton_Cancel = QtWidgets.QPushButton(Dialog_Export_Roi)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout_4.addWidget(self.pushButton_Cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog_Export_Roi)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Export_Roi)

    def retranslateUi(self, Dialog_Export_Roi):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Export_Roi.setWindowTitle(_translate("Dialog_Export_Roi", "Dialog"))
        self.label.setText(_translate("Dialog_Export_Roi", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ffaa00;\">Export Roi</span></p></body></html>"))
        self.label_6.setText(_translate("Dialog_Export_Roi", "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">Draw ROI after defining a pixel size. The data can then be saved in the given path.</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog_Export_Roi", "Mode"))
        self.pushButton_Mode_FreeHand.setText(_translate("Dialog_Export_Roi", "FreeHand"))
        self.pushButton_Mode_Rect.setText(_translate("Dialog_Export_Roi", "Rect"))
        self.label_3.setText(_translate("Dialog_Export_Roi", "Data to save"))
        self.checkBox_save_loc.setText(_translate("Dialog_Export_Roi", "Save dSTORM loc data"))
        self.checkBox_save_dstorm_image.setText(_translate("Dialog_Export_Roi", "Save dSTORM image"))
        self.checkBox_save_sim_image.setText(_translate("Dialog_Export_Roi", "Save SIM image"))
        self.label_5.setText(_translate("Dialog_Export_Roi", "Render pixel size [µm/pixel]"))
        self.label_4.setText(_translate("Dialog_Export_Roi", "Path"))
        self.pushButton_Save.setText(_translate("Dialog_Export_Roi", "Save"))
        self.pushButton_Cancel.setText(_translate("Dialog_Export_Roi", "Cancel"))

