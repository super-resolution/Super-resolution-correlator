# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_imagereg.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_Imagereg(object):
    def setupUi(self, Dialog_Imagereg):
        Dialog_Imagereg.setObjectName("Dialog_Imagereg")
        Dialog_Imagereg.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_Imagereg.setEnabled(True)
        Dialog_Imagereg.resize(600, 503)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        Dialog_Imagereg.setFont(font)
        Dialog_Imagereg.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Dialog_Imagereg.setStyleSheet("\n"
"QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"")
        Dialog_Imagereg.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_Imagereg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(Dialog_Imagereg)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.line = QtWidgets.QFrame(Dialog_Imagereg)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(20, -1, -1, -1)
        self.gridLayout.setHorizontalSpacing(70)
        self.gridLayout.setObjectName("gridLayout")
        self.fijiPathLabel = QtWidgets.QLabel(Dialog_Imagereg)
        self.fijiPathLabel.setObjectName("fijiPathLabel")
        self.gridLayout.addWidget(self.fijiPathLabel, 0, 0, 1, 1)
        self.fijiPathLineEdit = QtWidgets.QLineEdit(Dialog_Imagereg)
        self.fijiPathLineEdit.setObjectName("fijiPathLineEdit")
        self.gridLayout.addWidget(self.fijiPathLineEdit, 0, 2, 1, 1)
        self.landmarkPathLineEdit = QtWidgets.QLineEdit(Dialog_Imagereg)
        self.landmarkPathLineEdit.setObjectName("landmarkPathLineEdit")
        self.gridLayout.addWidget(self.landmarkPathLineEdit, 1, 2, 1, 1)
        self.landmark_file = QtWidgets.QLabel(Dialog_Imagereg)
        self.landmark_file.setObjectName("landmark_file")
        self.gridLayout.addWidget(self.landmark_file, 1, 0, 1, 1)
        self.open_landmark_file = QtWidgets.QPushButton(Dialog_Imagereg)
        self.open_landmark_file.setObjectName("open_landmark_file")
        self.gridLayout.addWidget(self.open_landmark_file, 1, 3, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.line_2 = QtWidgets.QFrame(Dialog_Imagereg)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.tabWidget = QtWidgets.QTabWidget(Dialog_Imagereg)
        self.tabWidget.setStyleSheet("QTabWidget::pane { /* The tab widget frame */\n"
"    border-top: 2px solid #000000;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 5px; /* move to the right by 5px */\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    background: #4d4d4d;\n"
"   /* border: 2px solid #C4C4C3;\n"
"    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"    /*border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;*/\n"
"    min-width: 20ex;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"/*QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
"                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
"}*/\n"
"QTabBar::tab:hover{\n"
"    background:#000099; \n"
"}\n"
"QTabBar::tab:selected {\n"
"    /*border-color: #9B9B9B;*/\n"
"    background: #000000; /* same as pane color */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 4px; /* make non-selected tabs look smaller */\n"
"}")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName("tabWidget")
        self.dSTORM = QtWidgets.QWidget()
        self.dSTORM.setObjectName("dSTORM")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.dSTORM)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 10, 451, 301))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_5.addWidget(self.line_5)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_10.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_5.addWidget(self.label_10, 0, QtCore.Qt.AlignVCenter)
        self.line_7 = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_5.addWidget(self.line_7)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setVerticalSpacing(20)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.pushButton_delete_STORM = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_delete_STORM.setStyleSheet("QPushButton{\n"
"    color: #ff9900;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #661a00;\n"
"    border-style: inset;\n"
"}")
        self.pushButton_delete_STORM.setObjectName("pushButton_delete_STORM")
        self.horizontalLayout_6.addWidget(self.pushButton_delete_STORM)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 3, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 0, 1, 1)
        self.comboBox_MarkerNr_STORM = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.comboBox_MarkerNr_STORM.setEnabled(True)
        self.comboBox_MarkerNr_STORM.setObjectName("comboBox_MarkerNr_STORM")
        self.gridLayout_3.addWidget(self.comboBox_MarkerNr_STORM, 0, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 1)
        self.doubleSpinBox_MarkerSTORMX = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_3)
        self.doubleSpinBox_MarkerSTORMX.setMinimum(-100000.0)
        self.doubleSpinBox_MarkerSTORMX.setMaximum(100000.0)
        self.doubleSpinBox_MarkerSTORMX.setObjectName("doubleSpinBox_MarkerSTORMX")
        self.gridLayout_3.addWidget(self.doubleSpinBox_MarkerSTORMX, 1, 1, 1, 1)
        self.doubleSpinBox_MarkerSTORMY = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_3)
        self.doubleSpinBox_MarkerSTORMY.setMinimum(-100000.0)
        self.doubleSpinBox_MarkerSTORMY.setMaximum(100000.0)
        self.doubleSpinBox_MarkerSTORMY.setProperty("value", 0.0)
        self.doubleSpinBox_MarkerSTORMY.setObjectName("doubleSpinBox_MarkerSTORMY")
        self.gridLayout_3.addWidget(self.doubleSpinBox_MarkerSTORMY, 2, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_set_STORM = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_set_STORM.setStyleSheet("QPushButton{\n"
"    color: #ff9900;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #661a00;\n"
"    border-style: inset;\n"
"}")
        self.pushButton_set_STORM.setObjectName("pushButton_set_STORM")
        self.horizontalLayout_2.addWidget(self.pushButton_set_STORM)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.gridLayout_3.setRowMinimumHeight(0, 40)
        self.verticalLayout_5.addLayout(self.gridLayout_3)
        self.line_8 = QtWidgets.QFrame(self.verticalLayoutWidget_3)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_5.addWidget(self.line_8)
        self.verticalLayout_5.setStretch(3, 10)
        self.tabWidget.addTab(self.dSTORM, "")
        self.SIM = QtWidgets.QWidget()
        self.SIM.setObjectName("SIM")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.SIM)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, 451, 301))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_4.addWidget(self.line_3)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_6.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6, 0, QtCore.Qt.AlignVCenter)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_4.addWidget(self.line_4)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setVerticalSpacing(20)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.pushButton_delete_SIM = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_delete_SIM.setStyleSheet("QPushButton{\n"
"    color: #ff9900;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #661a00;\n"
"    border-style: inset;\n"
"}\n"
"")
        self.pushButton_delete_SIM.setObjectName("pushButton_delete_SIM")
        self.horizontalLayout_5.addWidget(self.pushButton_delete_SIM)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 3, 1, 1, 1)
        self.doubleSpinBox_MarkerSIMX = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.doubleSpinBox_MarkerSIMX.setMinimum(-100000.0)
        self.doubleSpinBox_MarkerSIMX.setMaximum(100000.0)
        self.doubleSpinBox_MarkerSIMX.setObjectName("doubleSpinBox_MarkerSIMX")
        self.gridLayout_2.addWidget(self.doubleSpinBox_MarkerSIMX, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)
        self.doubleSpinBox_MarkerSIMY = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.doubleSpinBox_MarkerSIMY.setMinimum(-100000.0)
        self.doubleSpinBox_MarkerSIMY.setMaximum(100000.0)
        self.doubleSpinBox_MarkerSIMY.setProperty("value", 0.0)
        self.doubleSpinBox_MarkerSIMY.setObjectName("doubleSpinBox_MarkerSIMY")
        self.gridLayout_2.addWidget(self.doubleSpinBox_MarkerSIMY, 2, 1, 1, 1)
        self.comboBox_MarkerNr_SIM = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_MarkerNr_SIM.setObjectName("comboBox_MarkerNr_SIM")
        self.gridLayout_2.addWidget(self.comboBox_MarkerNr_SIM, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_set_SIM = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_set_SIM.setStyleSheet("QPushButton{\n"
"    color: #ff9900;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #661a00;\n"
"    border-style: inset;\n"
"}\n"
"")
        self.pushButton_set_SIM.setObjectName("pushButton_set_SIM")
        self.horizontalLayout.addWidget(self.pushButton_set_SIM)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.gridLayout_2.setRowMinimumHeight(0, 40)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.line_6 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_4.addWidget(self.line_6)
        self.verticalLayout_4.setStretch(3, 10)
        self.tabWidget.addTab(self.SIM, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.pushButton_GHT = QtWidgets.QPushButton(Dialog_Imagereg)
        self.pushButton_GHT.setStyleSheet("")
        self.pushButton_GHT.setObjectName("pushButton_GHT")
        self.verticalLayout.addWidget(self.pushButton_GHT)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_info_registration = QtWidgets.QLabel(Dialog_Imagereg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_info_registration.sizePolicy().hasHeightForWidth())
        self.label_info_registration.setSizePolicy(sizePolicy)
        self.label_info_registration.setObjectName("label_info_registration")
        self.horizontalLayout_4.addWidget(self.label_info_registration)
        self.comboBox_registration_mode = QtWidgets.QComboBox(Dialog_Imagereg)
        self.comboBox_registration_mode.setMinimumSize(QtCore.QSize(110, 0))
        self.comboBox_registration_mode.setObjectName("comboBox_registration_mode")
        self.comboBox_registration_mode.addItem("")
        self.comboBox_registration_mode.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_registration_mode)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_Imagereg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog_Imagereg)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog_Imagereg.accept)
        self.buttonBox.rejected.connect(Dialog_Imagereg.reject)
        self.comboBox_MarkerNr_STORM.currentIndexChanged['int'].connect(self.doubleSpinBox_MarkerSTORMX.clear)
        self.comboBox_MarkerNr_STORM.currentIndexChanged['int'].connect(self.doubleSpinBox_MarkerSTORMY.clear)
        self.pushButton_delete_STORM.released.connect(self.comboBox_MarkerNr_STORM.clearEditText)
        self.comboBox_MarkerNr_SIM.currentIndexChanged['int'].connect(self.doubleSpinBox_MarkerSIMX.clear)
        self.comboBox_MarkerNr_SIM.currentIndexChanged['int'].connect(self.doubleSpinBox_MarkerSIMY.clear)
        self.pushButton_delete_SIM.released.connect(self.comboBox_MarkerNr_SIM.clear)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Imagereg)

    def retranslateUi(self, Dialog_Imagereg):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Imagereg.setWindowTitle(_translate("Dialog_Imagereg", "Dialog"))
        self.label.setText(_translate("Dialog_Imagereg", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ffaa00;\">Image registration</span></p></body></html>"))
        self.fijiPathLabel.setText(_translate("Dialog_Imagereg", "FijiPath"))
        self.landmark_file.setText(_translate("Dialog_Imagereg", "LandmarkPath"))
        self.open_landmark_file.setText(_translate("Dialog_Imagereg", "Open"))
        self.label_10.setWhatsThis(_translate("Dialog_Imagereg", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#aa0000;\">dSTORM configuration:</span></p></body></html>"))
        self.label_10.setText(_translate("Dialog_Imagereg", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffaa00;\">dSTORM configuration:</span></p><p align=\"center\"><span style=\" font-size:6pt; font-weight:600; color:#ffffff;\">Double click left mouse button</span></p><p align=\"center\"><span style=\" font-size:6pt; font-weight:600; color:#ffffff;\">Change position with control + right click and dragging or by changing values and set</span></p></body></html>"))
        self.pushButton_delete_STORM.setText(_translate("Dialog_Imagereg", "Delete"))
        self.label_11.setText(_translate("Dialog_Imagereg", "position X"))
        self.label_12.setText(_translate("Dialog_Imagereg", "marker number"))
        self.label_13.setText(_translate("Dialog_Imagereg", "position Y"))
        self.pushButton_set_STORM.setText(_translate("Dialog_Imagereg", "Set"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dSTORM), _translate("Dialog_Imagereg", "dSTORM"))
        self.label_6.setWhatsThis(_translate("Dialog_Imagereg", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#aa0000;\">dSTORM configuration:</span></p></body></html>"))
        self.label_6.setText(_translate("Dialog_Imagereg", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffaa00;\">SIM configuration:</span></p><p align=\"center\"><span style=\" font-size:6pt; font-weight:600; color:#ffffff;\">Double click right mouse button</span></p><p align=\"center\"><span style=\" font-size:6pt; font-weight:600; color:#ffffff;\">Change position with control + right click and dragging or by changing values and set</span></p></body></html>"))
        self.pushButton_delete_SIM.setText(_translate("Dialog_Imagereg", "Delete"))
        self.label_8.setText(_translate("Dialog_Imagereg", "marker number"))
        self.label_7.setText(_translate("Dialog_Imagereg", "position X"))
        self.label_9.setText(_translate("Dialog_Imagereg", "position Y"))
        self.pushButton_set_SIM.setText(_translate("Dialog_Imagereg", "Set"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SIM), _translate("Dialog_Imagereg", "SIM"))
        self.pushButton_GHT.setText(_translate("Dialog_Imagereg", "Find markers with General Hough Transform"))
        self.label_info_registration.setText(_translate("Dialog_Imagereg", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600; color:#ffffff;\">-</span></p></body></html>"))
        self.comboBox_registration_mode.setItemText(0, _translate("Dialog_Imagereg", "bUnwarpJ (slow)"))
        self.comboBox_registration_mode.setItemText(1, _translate("Dialog_Imagereg", "Affine (fast)"))

