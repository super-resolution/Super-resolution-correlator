# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_roi.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_Roi(object):
    def setupUi(self, Dialog_Roi):
        Dialog_Roi.setObjectName("Dialog_Roi")
        Dialog_Roi.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_Roi.setEnabled(True)
        Dialog_Roi.resize(600, 503)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        Dialog_Roi.setFont(font)
        Dialog_Roi.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Dialog_Roi.setStyleSheet("\n"
"QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"")
        Dialog_Roi.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_Roi)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(Dialog_Roi)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.line = QtWidgets.QFrame(Dialog_Roi)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(20, -1, -1, -1)
        self.gridLayout.setHorizontalSpacing(70)
        self.gridLayout.setObjectName("gridLayout")
        self.push_buttom_correlate = QtWidgets.QPushButton(Dialog_Roi)
        self.push_buttom_correlate.setObjectName("push_buttom_correlate")
        self.gridLayout.addWidget(self.push_buttom_correlate, 0, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.line_2 = QtWidgets.QFrame(Dialog_Roi)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.tabWidget = QtWidgets.QTabWidget(Dialog_Roi)
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
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.dSTORM)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 581, 331))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.view_container_layout_dstorm = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.view_container_layout_dstorm.setContentsMargins(0, 0, 0, 0)
        self.view_container_layout_dstorm.setObjectName("view_container_layout_dstorm")
        self.tabWidget.addTab(self.dSTORM, "")
        self.SIM = QtWidgets.QWidget()
        self.SIM.setObjectName("SIM")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.SIM)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 581, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.view_container_layout_sim = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.view_container_layout_sim.setContentsMargins(0, 0, 0, 0)
        self.view_container_layout_sim.setObjectName("view_container_layout_sim")
        self.tabWidget.addTab(self.SIM, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_info_registration = QtWidgets.QLabel(Dialog_Roi)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_info_registration.sizePolicy().hasHeightForWidth())
        self.label_info_registration.setSizePolicy(sizePolicy)
        self.label_info_registration.setObjectName("label_info_registration")
        self.horizontalLayout_4.addWidget(self.label_info_registration)
        self.comboBox_registration_mode = QtWidgets.QComboBox(Dialog_Roi)
        self.comboBox_registration_mode.setMinimumSize(QtCore.QSize(110, 0))
        self.comboBox_registration_mode.setObjectName("comboBox_registration_mode")
        self.comboBox_registration_mode.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_registration_mode)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_Roi)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog_Roi)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog_Roi.accept)
        self.buttonBox.rejected.connect(Dialog_Roi.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Roi)

    def retranslateUi(self, Dialog_Roi):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Roi.setWindowTitle(_translate("Dialog_Roi", "Dialog"))
        self.label.setText(_translate("Dialog_Roi", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ffaa00;\">Roi</span></p></body></html>"))
        self.push_buttom_correlate.setText(_translate("Dialog_Roi", "correlate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dSTORM), _translate("Dialog_Roi", "dSTORM"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SIM), _translate("Dialog_Roi", "SIM"))
        self.label_info_registration.setText(_translate("Dialog_Roi", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600; color:#ffffff;\">-</span></p></body></html>"))
        self.comboBox_registration_mode.setItemText(0, _translate("Dialog_Roi", "Pearson"))

