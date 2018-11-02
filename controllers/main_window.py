# -*- coding: utf-8 -*-
"""
Created on: 2014.12.30.

Author: turbo

Edit by: Sebastian Reinhard 31.10.2018

"""

from PyQt5 import QtCore, QtGui, QtWidgets
# from views.main_window import Ui_MainWindow
from . import default_config


from views.main_window import Ui_MainWindow


from .viewer.viewer import Viewer


from .dialogs import *


from .images import *


from .rois import FreehandRoi


from .settings import *


from functools import partial


import os



try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig)


class MainWindow(Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()

        self.viewer = None
        self.storm_settings = StormSettings()
        self.confocal_settings = ConfocalSettings()
        if not os.path.isfile('WorkDir.ini'):
            file('WorkDir.ini', 'w').close()
        f = open('WorkDir.ini', 'r')
        
        workdirCandidate=f.read()
        if os.path.isdir(workdirCandidate):
            self.working_directory=workdirCandidate
        else:
            self.working_directory=os.getcwd()
        self.working_directory_unset = True
        f.close()      
        try:
            os.makedirs(self.working_directory)
        except OSError:
            if not os.path.isdir(self.working_directory):
                raise

    def init_component(self, qt_window):
        self.qt_window = qt_window
        self._create_dialogs()
        self._setup_components()
        self._add_handlers()
        self._load_config()
        self.status_bar = QtWidgets.QStatusBar()
        self.qt_window.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Welcome to VividSTORM")

    #viewerdef
    def save_config(self):
        x= ""
        with open(os.getcwd() + r"\resources\Settings.txt", "r") as settings:
            Keywords = ["filter_z", "filter_photon", "filter_frame"]
            for key in Keywords:
                if getattr(self, "groupBox_storm_" + key).isChecked():
                    asdf = ""
                    for line in settings.read().split("\n"):
                        if key in line:
                            asdf = key + " True min " + str(getattr(self, "spinBox_storm_" + key+ "_from").value()) + " max " + str(getattr(self, "spinBox_storm_" + key + "_to").value())
                        else:
                            asdf = key + " True min " + str(getattr(self, "spinBox_storm_" + key+ "_from").value()) + " max " + str(getattr(self, "spinBox_storm_" + key + "_to").value())
                    x += asdf + "\n"


        with open(os.getcwd() + r"\resources\Settings.txt", "w") as settings:
            settings.write(x)

    #viewerdef
    def _load_config(self):
        with open(os.getcwd() + r"\resources\Settings.txt", "r") as settings:
            Keywords = ["filter_z", "filter_photon", "filter_frame", "filter_localdensity"]
            for line in settings.read().split("\n"):
                for i in range(len(Keywords)):
                    minmaxvalue = []
                    if Keywords[i] in line and "False" not in line:
                        for word in line.split(" "):
                            try:
                                minmaxvalue.append(float(word))
                            except ValueError:
                                pass
                        getattr(self, "groupBox_storm_" + Keywords[i]).setChecked(True)
                        getattr(self, "spinBox_storm_" + Keywords[i]+ "_from").setValue(minmaxvalue[0])
                        getattr(self, "spinBox_storm_" + Keywords[i]+ "_to").setValue(minmaxvalue[1])

    #viewerdef
    def _paint_slider(self, ch, color):
        getattr(self, "slider_confocal_channel"+ch+"_slice").setStyleSheet("""QSlider::add-page:horizontal {\n"
                background: """+color+""";\n
                }\n
                """)

    def deactivate_sliders(self, checked):
        if checked:
            for i in range(4):
                confocal_slider = getattr(self, "slider_confocal_channel" + str(i) + "_slice")
                confocal_slider.setEnabled(False)
        elif not checked:
            for i in range(4):
                confocal_slider = getattr(self, "slider_confocal_channel" + str(i) + "_slice")
                confocal_slider.setEnabled(True)

    def _setup_components(self):
        self.viewer = Viewer(main_window=self)
        self.viewer.change_drag_mode(self.actionDragging_mode.isChecked(), 1)
        self.viewer.change_drag_mode(self.action_Roi_to_export.isChecked(), 3)
        self.viewer.change_drag_mode(self.action_correlation_selecting.isChecked(), 3)
        self.viewer.change_drag_mode(self.actionImage_Registration.isChecked(), 2)

        self.storm_settings.setup(self, 'storm')
        self.storm_settings.set_default_values()
        self.storm_settings.setup_filters()

        self.confocal_settings.setup(self, 'confocal')
        self.confocal_settings.set_default_values()

        self.dialog_tool_analysis.setup()
        self.dialog_tool_lut.setup()
        self.dialog_tool_active_contour.setup()
        self.dialog_tool_roi.setup()
        self.dialog_imageregistration.setup()
        self.dialog_matrix_parameters.setup()
        self.dialog_export_roi.setup()

    def _add_dialog(self, new_dialog):
        qtDialog = QtWidgets.QDialog()
        new_dialog.setupUi(qtDialog)
        new_dialog.qtDialog = qtDialog
        new_dialog.main_window = self
        return new_dialog

    def _create_dialogs(self):
        self.dialog_tool_lut = self._add_dialog(LutDialog())
        self.dialog_tool_active_contour = self._add_dialog(ActiveContourDialog())

        self.dialog_openSTORM = self._add_dialog(openSTORMDialog())
        self.dialog_tool_analysis = self._add_dialog(AnalysisDialog())
        self.dialog_view_dots = self._add_dialog(DotsDialog())
        self.dialog_view_gaussian = self._add_dialog(GaussianDialog())
        self.dialog_view_3d = self._add_dialog(ThreeDDialog())
        self.dialog_scale = self._add_dialog(ScaleDialog())
        self.dialog_loading = self._add_dialog(LoadingDialog())
        self.dialog_error = self._add_dialog(ErrorDialog())
        self.dialog_about=self._add_dialog(AboutDialog())
        self.dialog_help=self._add_dialog(HelpDialog())
        self.dialog_imageregistration = self._add_dialog(ImageRegistrationDia())
        self.dialog_tool_roi = self._add_dialog(RoiDialog())
        self.dialog_matrix_parameters = self._add_dialog(MatrixParameters())
        self.dialog_export_roi = self._add_dialog(ExportDialog())
        

    def _add_action_handlers(self):
        self.actionOpen_STORM_files.triggered.connect(
            lambda: self._open_files('storm'))
        self.actionClose_STORM_files.triggered.connect(
            lambda: self._close_files('storm'))
        self.actionOpen_Confocal_files.triggered.connect(
            lambda: self._open_files('confocal'))
        self.actionClose_Confocal_files.triggered.connect(
            lambda: self._close_files('confocal'))

        self.actionSet_working_directory.triggered.connect(self._set_working_directory)
        # self.actionExport_As_Image.triggered.connect(lambda: self._export_as_image())

        self.actionDots.triggered.connect(
            lambda: self._open_dialog(self.dialog_view_dots))
        self.actionGaussian.triggered.connect(
            lambda: self._open_dialog(self.dialog_view_gaussian))

        self.action_correlation_selecting.triggered.connect(
            lambda: (self._open_dialog(self.dialog_tool_roi),self.viewer.change_drag_mode(self.actionDragging_mode.isChecked(),3)))
        self.action_Roi_to_export.triggered.connect(
            lambda: (self._open_dialog(self.dialog_export_roi),self.viewer.change_drag_mode(self.actionDragging_mode.isChecked(),3)))
        #self.actionCircle_ROI_selecting.triggered.connect(
        #    lambda: self._draw_roi('circle'))
        #self.actionActiveContour_selector.triggered.connect(
        #    lambda: self._open_dialog(self.dialog_tool_active_contour))

        self.actionShow_1_m_scale.triggered.connect(
            lambda: self._open_dialog(self.dialog_scale))
        self.actionDragging_mode.triggered.connect(
            lambda: self.viewer.change_drag_mode(self.actionDragging_mode.isChecked(),1))
        self.actionLUT_changer.triggered.connect(
            lambda: self._open_dialog(self.dialog_tool_lut))
        self.action3D.triggered.connect(
            lambda: self._open_dialog(self.dialog_matrix_parameters))#(self.viewer.change_view_dim(), self._deactivate_sliders()))

        self.actionAbout_VividSTORM.triggered.connect(
            lambda: self._open_dialog(self.dialog_about))
        self.actionVividSTORM_help.triggered.connect(
            lambda: self._open_dialog(self.dialog_help))
        self.actionImage_Registration.triggered.connect(
            lambda: (self._open_dialog(self.dialog_imageregistration), self.viewer.change_drag_mode(self.actionDragging_mode.isChecked(),3)))
        self.actionExport.triggered.connect(
            lambda: self._save_current_overlay())

    def _add_key_shortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageDown), self.pushButton_next_batch).activated.connect(lambda: self._batch_step_files_by(1))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageUp), self.pushButton_prev_batch).activated.connect(lambda: self._batch_step_files_by(-1))

    def _add_input_handlers(self):
        self.pushButton_apply_storm_filters.clicked.connect(
            lambda: self.save_config())
        self.pushButton_apply_storm_config.clicked.connect(
            lambda: self.viewer.show_storm_image(self.storm_images_list.selectedItems()))
        self.pushButton_open_storm.clicked.connect(
            lambda: self._open_files('storm'))
        self.pushButton_open_confocal.clicked.connect(
            lambda: self._open_files('confocal'))
        self.pushButton_unload_storm.clicked.connect(
            lambda: self.viewer.unload_storm_image(self.storm_images_list.currentItem()))
        self.pushButton_unload_confocal.clicked.connect(
            lambda: self.viewer.unload_confocal_image(self.confocal_images_list.currentItem()))
        self.pushButton_close_all_storm.clicked.connect(
            lambda: self._close_files('storm'))
        self.pushButton_close_all_confocal.clicked.connect(
            lambda: self._close_files('confocal'))
        self.pushButton_close_storm.clicked.connect(
            lambda: self._close_file('storm', self.storm_images_list.currentRow()))
        self.pushButton_close_confocal.clicked.connect(
            lambda: self._close_file('confocal', self.confocal_images_list.currentRow()))
        self.pushButton_next_batch.clicked.connect(
            lambda: self._batch_step_files_by(1))
        self.pushButton_prev_batch.clicked.connect(
            lambda: self._batch_step_files_by(-1))
        self.pushButton_show_storm.clicked.connect(
            lambda: self.viewer.show_storm_image(self.storm_images_list.selectedItems()))
        self.pushButton_show_confocal.clicked.connect(
            lambda: self.viewer.show_confocal_image(self.confocal_images_list.selectedItems()))

        for i in range(4):
            storm_channel = getattr(self, "checkBox_storm_channel"+ str(i))
            storm_color = getattr(self, "comboBox_storm_channel" + str(i) + "_color")
            confocal_color = getattr(self, "comboBox_confocal_channel" + str(i) + "_color")
            confocal_channel = getattr(self, "checkBox_confocal_channel" + str(i))
            confocal_slider = getattr(self, "slider_confocal_channel" + str(i) + "_slice")
            getattr(self, "slider_confocal_channel"+str(i)+"_slice").setStyleSheet(
                "QSlider::sub-page:horizontal {background:"+confocal_color.currentText()+"}")

            storm_channel.stateChanged.connect(
                lambda state, i=i, item=storm_channel: self.viewer.display.SetStormChannelVisible(i, item.isChecked()))
            storm_color.currentIndexChanged.connect(
                lambda state, i=i, item=storm_color: self.viewer.display.SetStormChannelColor(
                i, str(item.currentText())))

            confocal_color.currentIndexChanged.connect(
                lambda state, i=i, item=confocal_color: (
                    self.viewer.display.SetConfocalChannelColor(i, str(item.currentText())),
                getattr(self, "slider_confocal_channel"+str(i)+"_slice").setStyleSheet(
                    "QSlider::sub-page:horizontal {background:"+item.currentText()+"}")))
            confocal_channel.stateChanged.connect(
                lambda state, i=i, item=confocal_channel: (
                    self.viewer.display.SetConfocalChannelVisible(i, item.isChecked()),
                    self.viewer.show_confocal_image(self.confocal_images_list.selectedItems())))
            confocal_slider.valueChanged.connect(
                lambda state, i=i, : self.viewer.update_confocal_image())



    def _add_event_handlers(self):
        self.storm_images_list.itemSelectionChanged.connect(self.storm_settings.apply_storm_config)

    def _add_handlers(self):
        self._add_action_handlers()
        self._add_key_shortcuts()
        self._add_input_handlers()
        self._add_event_handlers()

    def show_loading(self, title='Please wait', message='Loading...'):
        self.dialog_loading.setWindowTitle(title)
        self.dialog_loading.findChild(QtWidgets.QLabel, 'label').setText(message)
        self._open_dialog(self.dialog_loading)

    def finish_loading(self):
        self.dialog_loading.close()

    def show_error(self, title='Attention', message='Something happened'):
        self.dialog_error.qtDialog.setWindowTitle(title)
        self.dialog_error.qtDialog.findChild(QtWidgets.QLabel, 'label').setText(message)
        self._open_dialog(self.dialog_error)

    def _set_working_directory(self):
        #try to read the file        
        if not os.path.isfile('WorkDir.ini'):
            file('WorkDir.ini', 'w').close()
        f = open('WorkDir.ini', 'r')
        workdirCandidate=f.read()
        if os.path.isdir(workdirCandidate):
            self.working_directory=workdirCandidate
        else:
            self.working_directory=os.getcwd()
        self.working_directory_unset = True
        f.close()
        file_dialog = QtWidgets.QFileDialog()
        working_directory = QtWidgets.QFileDialog.getExistingDirectory(file_dialog, 'Select working directory',
                                                                   self.working_directory)
        if working_directory.length() > 0:
            self.working_directory = str(working_directory)
            self.working_directory_unset = False
        #write working directory to file
        f = open('WorkDir.ini', 'w')
        f.write(self.working_directory )
        f.close()

    def _save_current_overlay(self):
        #file_dialog = QtGui.QFileDialog()
        #file_dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        #title = "Save current overlay"
        #path = QtGui.QFileDialog.getSaveFileName(file_dialog, title,
        #                                                    self.working_directory,)
        path = os.getcwd() +r"\Screenshots\\"

        self.viewer.save_screenshot(str(path))

    def _open_files(self, mode):
        if mode == 'storm':
            if self.checkBox_trans_Matrix.isChecked():
                file_dialog = QtWidgets.QFileDialog()
                title = "Open dSTORM files"
                extensions = "dSTORM coordinates (*.txt)"
                storm_image = QtWidgets.QFileDialog.getOpenFileNames(file_dialog, title,
                                                            self.working_directory, extensions)[0][0]
                if storm_image != None:
                    storm_image = StormImage(storm_image)
                    title = "Open Matrix files"
                    extensions = "Matrix (*.txt)"
                    storm_image.matrix = QtWidgets.QFileDialog.getOpenFileNames(file_dialog, title,
                                                                self.working_directory, extensions)[0][0]
                    self.storm_images_list.addItem(storm_image)
            else:
                file_dialog = QtWidgets.QFileDialog()
                title = "Open dSTORM files"
                extensions = "dSTORM coordinates (*.txt)"
                try:
                    storm_image = QtWidgets.QFileDialog.getOpenFileNames(file_dialog, title,
                                                            self.working_directory, extensions)[0][0]
                except:
                    print("None Selected")
                    return
                if storm_image != None:
                    storm_image = StormImage(storm_image)
                    self.storm_images_list.addItem(storm_image)
            #self._open_dialog(self.dialog_openSTORM)
            #try:
                #file = self.dialog_openSTORM.storm_image
                #self.Matrix = self.dialog_openSTORM.Matrix[0]
                #storm_image = StormImage(file)
                #self.storm_images_list.addItem(storm_image)

            #except:
                #print "None selected"
        elif mode == 'confocal':
            file_dialog = QtWidgets.QFileDialog()
            title = "Open SIM files"
            # extensions = "Confocal images (*.jpg; *.png; *.tif;);;Confocal stacks (*.ics)"
            #extensions = "Confocal images (*.jpg *.png *.tif *.ics)"
            extensions = "Confocal images (*.czi *.tif *.lsm *.png"  \
                         ")"
            files_list = QtWidgets.QFileDialog.getOpenFileNames(file_dialog, title,
                                                            self.working_directory, extensions)[0]
            for file_ in files_list:
                confocal_image = ConfocalImage(file_)
                self.confocal_images_list.addItem(confocal_image)

    def _close_files(self, mode):
        image_list = []
        if mode == 'storm':
            image_list = self.storm_images_list
        elif mode == 'confocal':
            image_list = self.confocal_images_list
        for i in range(image_list.count()):
            self._close_file(mode, 0)
            # image_list.clear()

    def _close_file(self, mode, index):
        # TODO: destroy img obj
        if mode == 'storm':
            removed = self.storm_images_list.takeItem(index)
            if removed:
                self.viewer.unload_storm_image(removed)
                removed.reset_data()
                self.storm_images_list.setCurrentRow(-1)
        elif mode == 'confocal':
            removed = self.confocal_images_list.takeItem(index)
            if removed:
                self.viewer.unload_confocal_image(removed)
                removed.reset_data()
                self.confocal_images_list.setCurrentRow(-1)

    def _batch_step_files_by(self, step_size):
        storm_num = self.storm_images_list.count()
        next_active_row = self.storm_images_list.currentRow() + step_size
        if 0 <= next_active_row <= storm_num - 1:
            self.storm_images_list.setCurrentRow(next_active_row)
        else:
            if step_size > 0:
                self.storm_images_list.setCurrentRow(storm_num - 1)
            elif step_size < 0:
                self.storm_images_list.setCurrentRow(0)

        confocal_num = self.confocal_images_list.count()
        next_active_row = self.confocal_images_list.currentRow() + step_size
        if 0 <= next_active_row <= confocal_num - 1:
            self.confocal_images_list.setCurrentRow(next_active_row)
        else:
            if step_size > 0:
                self.confocal_images_list.setCurrentRow(confocal_num - 1)
            elif step_size < 0:
                self.confocal_images_list.setCurrentRow(0)

    def _close_dialog(self, dialog):
        dialog.qtDialog.close()

    def _open_dialog(self, dialog):
        # dialog.findChild(QtGui.QDialogButtonBox).clicked.connect(lambda: self.test(dialog))
        if type(dialog).__name__ == 'AnalysisDialog':
            if self.viewer.current_storm_image:
                roi = self.storm_roi_list.currentItem()
                if roi:
                    if type(roi).__name__ == 'EllipseRoi' or type(roi).__name__ == 'CircleRoi':
                        storm_data = self.viewer.display.getEllipseROIPoints(roi.roi)
                        roi_perimeter = self.viewer.display.lengthOfEllipseROI(roi.roi)
                        roi_area = self.viewer.display.areaOfEllipseROI(roi.roi)
                    elif type(roi).__name__ == 'FreehandRoi':
                        storm_data = self.viewer.display.getFreehandROIPoints(roi.roi)
                        roi_perimeter = self.viewer.display.lengthOfFreehandROI()
                        roi_area = self.viewer.display.areaOfFreehandROI()
                    elif type(roi).__name__ == 'ActiveContourRoi':
                        storm_data = self.viewer.display.getActiveContourROIPoints(roi.roi)
                        roi_perimeter = self.viewer.display.lengthOfActiveContourROI(roi.roi)
                        roi_area = self.viewer.display.areaOfActiveContourROI(roi.roi)
                    # self.show_error(message=roi_tag + ' ROI is selected. Using data selected by this ROI.')
                else:
                    storm_data = self.viewer.display.StormData_filtered
                    roi_perimeter = None
                    roi_area = None
                    # self.show_error(message='No ROI is selected. Full STORM data is used.')



                dialog.setup_analyses(
                    storm_data,
                    roi, roi_perimeter, roi_area
                )
                # set up Euclidean/confocal combobox
                if len(self.viewer.display.ConfocalMetaData) > 0:
                    dialog.setup_conf_channel(list(range(self.viewer.display.ConfocalMetaData['ChannelNum'])),
                                         self.viewer.display.ConfocalChannelVisible)
            else:
                self.show_error(message='No STORM file is opened!')
                return False

        if type(dialog).__name__ == 'LutDialog':
            dialog.reset_channels()
            if len(self.viewer.display.StormChannelList) > 0:
                dialog.setup_channels('storm',
                    self.viewer.display.StormChannelList,
                    self.viewer.display.StormChannelVisible,
                )
            if len(self.viewer.display.ConfocalMetaData) > 0:
                dialog.setup_channels('confocal',
                    list(range(self.viewer.display.ConfocalMetaData['ChannelNum'])),
                    self.viewer.display.ConfocalChannelVisible
                )

        if type(dialog).__name__ == 'ActiveContourDialog':
            if self.viewer.current_confocal_image:
                roi = self.storm_roi_list.currentItem()
                if roi and type(roi).__name__ == 'CircleRoi':
                    dialog.reset_channel()
                    dialog.confocal_image = self.confocal_images_list.currentItem()
                    if len(self.viewer.display.ConfocalMetaData) > 0:
                        dialog.setup_channel(
                            list(range(self.viewer.display.ConfocalMetaData['ChannelNum'])),
                            self.viewer.display.ConfocalChannelVisible
                        )
                        dialog.setup_data(
                            self.viewer,
                            roi,
                            self.viewer.display.ConfocalZNum,
                            self.viewer.display.ConfocalOffset(),
                            self.viewer.current_confocal_image.ConfocalMetaData['SizeX']
                        )
                else:
                    self.show_error(message='Create and select a Circle ROI to use active contour evolution feature.')
                    return False
            else:
                self.show_error(message='No Confocal file is opened!')
                return False

        if type(dialog).__name__ == 'ScaleDialog':
            dialog.setup()
        if type(dialog).__name__ == 'openSTORMDialog':
            #dialog.clear()
            dialog.setup()

        if type(dialog).__name__ == 'ImageRegistrationDia':
            #at least one channels are shwon
            if self.viewer.current_storm_image:
                if self.viewer.current_confocal_image:
                    self.viewer.display.ChangePanMode("Reg")
                    #dialog.reset_channels()
                    # if len(self.viewer.display.StormChannelList) > 0:
                    #     dialog.setup_channels('storm',
                    #         self.viewer.display.StormChannelList,
                    #         self.viewer.display.StormChannelVisible,
                    #         self.viewer.display.Viewbox.ConfRegistrationChannel
                    #     )
                    # if len(self.viewer.display.ConfocalMetaData) > 0:
                    #     dialog.setup_channels('confocal',
                    #         range(self.viewer.display.ConfocalMetaData['ChannelNum']),
                    #         self.viewer.display.ConfocalChannelVisible,
                    #         self.viewer.display.Viewbox.StormRegistrationChannel
                    #     )
                else:
                    self.show_error(message='No Confocal file is opened!')
                    return False
            else:
                    self.show_error(message='No STORM file is opened!')
                    return False
        if type(dialog).__name__ == 'RoiDialog' or type(dialog).__name__ =='ExportDialog':
            #at least one channels are shwon
            #if self.viewer.current_storm_image:
                #if self.viewer.current_confocal_image:
                    self.viewer.display.ChangePanMode("Roi")
        dialog.qtDialog.exec_()

    def _draw_roi(self, shape):
        if self.viewer.current_storm_image:
            if len(self.viewer.current_storm_image.roi_list) > 0:
                self.viewer.remove_roi(self.storm_roi_list.currentItem())
            if shape == 'freehand':
                    self.actionDragging_mode.setChecked(False)
                    if self.actionFreehand_selecting.isChecked():
                        self.viewer.add_roi(shape)
                    else:
                        roi = self.viewer.display.addFreehandROI()
                        num = str(self.storm_settings.get_roi_counter())
                        freehand_roi = FreehandRoi('freehandROI_' + num)
                        freehand_roi.roi = roi
                        self.storm_settings.add_roi(freehand_roi)
                        self.viewer.display.ChangePanMode('Pan')
            elif shape == 'ellipse':
                    self.viewer.add_roi(shape)
            elif shape == 'circle':
                    self.viewer.add_roi(shape)
        else:
            self.actionFreehand_selecting.setChecked(False)
            self.show_error(message='No storm image is opened')

    def _export_as_image(self):
        file_dialog = QtWidgets.QFileDialog()
        filename = str(QtWidgets.QFileDialog.getSaveFileName(file_dialog, 'Save File', self.working_directory,
                                                         "PNG image file (*.png)"))[0]
        self.viewer.display.export_as_image(filename)



