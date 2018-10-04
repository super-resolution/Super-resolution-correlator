# -*- coding: utf-8 -*-
"""
Created on: 2015.01.12.

Author: turbo


"""

from functools import partial


from controllers import bunwarpJ_cmd_support


from .active_contour import morphsnakes


from .viewer import tifffile


from views.dialog_error import Ui_Dialog_error


from views.dialog_loading import Ui_Dialog_loading


from views.dialog_scale import Ui_Dialog_scale


from views.dialog_tool_active_contour import Ui_Dialog_active_contour


from views.dialog_tool_analysis import Ui_Dialog_analysis


from views.dialog_tool_lut import Ui_Dialog_lut


from views.dialog_tool_imageregistration import Ui_Dialog_imageregistration


from views.dialog_imagereg import Ui_Dialog_Imagereg


from views.dialog_tool_positioning import Ui_Dialog_positioning


from views.dialog_roi import Ui_Dialog_Roi


from views.dialog_view_3d import Ui_Dialog_3d


from views.dialog_view_dots import Ui_Dialog_dots


from views.dialog_view_gaussian import Ui_Dialog_gaussian


from views.dialog_about import Ui_Dialog_about


from views.dialog_help import Ui_Dialog_help_2


from views.diolog_input_openSTORM import Ui_Dialog_openSTORM


from views.dialog_matrix_parameters import Ui_Dialog_Matrix_Parameters


from views.dialog_export_roi import Ui_Dialog_Export_Roi


from .default_config import version as version_num


from .analyses import *


from scipy import ndimage


from scipy.interpolate import splev


from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg


from pandas import read_csv


import PIL



from controllers import TransformLocFile



try:
    QString = unicode
except NameError:
    # Python 3
    QString = str

class AboutDialog(Ui_Dialog_about):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)


class HelpDialog(Ui_Dialog_help_2):
    def __init__(self, *args, **kwargs):
        super(HelpDialog, self).__init__(*args, **kwargs)


class ErrorDialog(Ui_Dialog_error):
    def __init__(self, *args, **kwargs):
        super(ErrorDialog, self).__init__(*args, **kwargs)


class LoadingDialog(Ui_Dialog_loading):
    def __init__(self, *args, **kwargs):
        super(LoadingDialog, self).__init__(*args, **kwargs)


class ScaleDialog(Ui_Dialog_scale):
    def __init__(self, *args, **kwargs):
        super(ScaleDialog, self).__init__(*args, **kwargs)
        self._connected = False

    def _setup_components(self):
        widgets = list(self.__dict__.keys())
        self.push_buttons = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('pushButton') != -1]

    def custom_scale(self):
        pos = QtGui.QVector3D(self.spinBox_X.value(),self.spinBox_Y.value(),self.spinBox_Z.value())
        length = self.spinBox_size.value()
        width = self.spinBox_width.value()
        self.main_window.viewer.push_custom_scale_to_display(pos, length, width)

    def _add_input_handlers(self):
        for push_button in self.push_buttons:
            mode = push_button.objectName().split('_')[-1]
            push_button.clicked.connect(partial(self.main_window.viewer.show_scale, mode))
        self.show_custom_scale.clicked.connect(lambda:self.custom_scale())
        self._connected = True

    def setup(self):
        self._setup_components()
        if not self._connected:
            self._add_input_handlers()


class openSTORMDialog(Ui_Dialog_openSTORM):
    def __init__(self, *args, **kwargs):
            super(openSTORMDialog, self).__init__(*args, **kwargs)
            self.file_dialog = None

    def clear(self):
            self.listWidget_storm_input.clear()
            self.listWidget_trans_matrix_input.clear()
            self.storm_image = []

    def _add_input_handlers(self):
        self.pushButton_open_storm.clicked.connect(lambda: self.add_input("Storm"))
        self.pushButton_open_matrix.clicked.connect(lambda: self.add_input("Matrix"))


    def setup(self):

        self._add_input_handlers()

    def add_input(self, type):
        file_dialog = QtWidgets.QFileDialog()
        if type == 'Storm':
            title = "Open STORM files"
            extensions = "STORM coordinates (*.txt)"
            storm_image = QtWidgets.QFileDialog.getOpenFileNames(file_dialog, title,
                                                            self.main_window.working_directory, extensions)[0][0]
            #self.listWidget_storm_input.addItem(storm_image)
        elif type == 'Matrix':
            title = "Open Matrix files"
            extensions = "Matrix (*.txt)"
            self.Matrix = QtWidgets.QFileDialog.getOpenFileNames(None, title,
                                                            self.working_directory, extensions)[0]
            self.listWidget_trans_matrix_input.addItem(self.Matrix[0])#nicht im gebrauch


class ActiveContourDialog(Ui_Dialog_active_contour):
    def __init__(self, *args, **kwargs):
        super(ActiveContourDialog, self).__init__(*args, **kwargs)
        self.confocal_image = None

        self.viewer = None
        self.roi = None
        self.z_position = None
        self.confocal_offset = None
        self.calibration_px = None

    def setup(self):
        self._add_input_handlers()

    def _add_input_handlers(self):
        self.pushButton_run.clicked.connect(lambda: self.run())

    def reset_channel(self):
        self.resetting = True
        while self.comboBox_confocal_channel_changer.count() > 0:
            self.comboBox_confocal_channel_changer.removeItem(0)
        self.resetting = False

    def setup_data(self, viewer, roi, z_position, confocal_offset, calibration_px):
        self.viewer = viewer
        self.roi = roi
        self.z_position = z_position
        self.confocal_offset = confocal_offset
        self.calibration_px = calibration_px

    def setup_channel(self, channel_list, channels_visible):
        comboBox = self.comboBox_confocal_channel_changer
        channels_to_add = []
        for i, channel in enumerate(channel_list):
            if channels_visible[i]:
                channels_to_add.append(str(channel))
        comboBox.addItems(channels_to_add)

    # Convert a RGB image to gray scale. (from morphsnakes)
    def Rgb2Gray(self, img):
        return 0.2989 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]

    # Build a binary function with a circle as the 0.5-levelset
    # from morphsnakes
    def ActiveContourCircleLevelset(self, shape, center, sqradius, scalerow=1.0):

        R, C = numpy.mgrid[:shape[0], :shape[1]]

        phi = sqradius - (numpy.sqrt(scalerow * (R[:, :] - center[0]) ** 2 + (C[:, :] - center[1]) ** 2))
        u = numpy.float_(phi > 0)
        return u

    def GetEdgeCoords(self, matrix):
        edgecoords = []
        outmatrix = numpy.copy(matrix)

        for x in range(numpy.shape(matrix)[0]):
            for y in range(numpy.shape(matrix)[1]):
                if matrix[x, y] == 1:
                    nn = self.CountNeighborNumber(x, y, matrix)
                    if nn > 0:

                        edgecoords.append([x, y])
                    else:
                        outmatrix[x, y] = 0

        return [edgecoords, outmatrix]

    #counts how many bordering white neighbors a black pixel has
    def CountNeighborNumber(self, x, y, matrix):
        nn = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if matrix[x + i, y + j] == 0:
                    nn += 1
        return nn

    def run(self):
        print("Active contour")

        iteration = numpy.int(self.spinBox_iteration_cycles.value())
        mu = numpy.int(self.spinBox_mu.value())
        lambda1 = numpy.int(self.spinBox_lambda1.value())
        lambda2 = numpy.int(self.spinBox_lambda2.value())
        channel = int(str(self.comboBox_confocal_channel_changer.currentText()))
        dilation_nr=numpy.int(self.spinBox_dilation.value())
        is_spline_on=self.checkBox_spline_fit.isChecked()

        """
        zpos = self.z_position

        if len(self.confocal_image.ConfocalData.shape)==2: # if 1channel, non-zstack
            img=self.confocal_image.ConfocalData/255.0 # its values should be normalized between 0 and 1
        else:
            if self.confocal_image.ConfocalMetaData['ChannelNum']>1:
                if len(self.confocal_image.ConfocalData.shape)==4:  #if non-1-channel, zstack
                    img =self.confocal_image.ConfocalData[zpos][channel] / 255.0
                else:
                    img =self.confocal_image.ConfocalData[channel] / 255.0 #if non-1-channel, non-zstack
            else:
                img =self.confocal_image.ConfocalData[zpos] / 255.0 #if 1-channel, zstack
        """
        img=self.main_window.viewer.display.ConfChannelToShow[channel]
        #downscale the image:
        
        # in case tracking active contour is needed
        #plt.figure()
        #plt.imshow(img)
        #plt.show()
        #if self.main_window.viewer.display.Viewbox.AffineTransform != []:
        #    img=cv2.warpAffine(img,self.main_window.viewer.display.Viewbox.AffineTransform,(img.shape))
        
        # Morphological ACWE. Initialization of the level-set.
        
        img=scipy.ndimage.zoom(img,  1.0/self.viewer.display.ConfocalSizeMultiplier, order=0)

        #plt.figure()
        #plt.imshow(img)
        #plt.show()

        macwe = morphsnakes.MorphACWE(img, smoothing=mu, lambda1=lambda1, lambda2=lambda2)
        zoom = 1000.0 * self.viewer.display.ConfocalMetaData['SizeX']
        
        
        conf_offset = [self.confocal_offset[0] * 100.0 * self.viewer.display.ConfocalMetaData['SizeX'],
                       self.confocal_offset[1] * 100.0 * self.viewer.display.ConfocalMetaData['SizeY']]

        position = [numpy.int((self.roi.roi.pos()[1] + self.roi.roi.size()[0] / 2.0 - conf_offset[0]) / zoom),
                    numpy.int((self.roi.roi.pos()[0] + self.roi.roi.size()[0] / 2.0 - conf_offset[1]) / zoom)]
        r = numpy.int(self.roi.roi.size()[0] / zoom / 2)

        macwe.levelset = self.ActiveContourCircleLevelset(img.shape, position, r)  #circle center coordinates, radius

        # Visual evolution.
        #plt.figure()

        acroi = morphsnakes.evolve_visual(macwe, num_iters=iteration,
                                          background=img)  # its final state is a ROI, which should be used to filter
                                          # the STORM coordinates

        # applies dilation
        if dilation_nr!=0:
            acroi = scipy.ndimage.morphology.binary_dilation(acroi, iterations=dilation_nr)

        #plt.imshow(acroi)
        #plt.figure()
        #plt.imshow(dilated_acroi)
        #plt.show()



        [edgecoords, outroi] = self.GetEdgeCoords(acroi)
        ACROI = []
        CurrentPoint = edgecoords[0]
        ACROI.append(CurrentPoint)
        PointAdded = True
        while PointAdded:
            PointAdded=False
            NeighbouringPoints=0
            MinDist=2
            MinPoint=[]
            for point in edgecoords:
                if math.fabs(CurrentPoint[0]-point[0])<2 and math.fabs(CurrentPoint[1]-point[1])<2:
                    Dist=math.sqrt((CurrentPoint[0]-point[0])*(CurrentPoint[0]-point[0])+(CurrentPoint[1]-point[1])
                                   *(CurrentPoint[1]-point[1]))
                    if Dist<MinDist and Dist!=0:
                        MinDist=Dist
                        MinPoint=point
            if MinPoint!=[]:
                PointAdded=True
                edgecoords.remove(MinPoint)
                ACROI.append(MinPoint)
                CurrentPoint=MinPoint

        for i in range(len(ACROI)):
            ACROI[i] = [ACROI[i][1] * 1000.0 * self.viewer.display.ConfocalMetaData['SizeY'] + conf_offset[1] + zoom / 2.0,
                        ACROI[i][0] * 1000.0 * self.viewer.display.ConfocalMetaData['SizeX'] + conf_offset[0] + zoom / 2.0]#zoom

        if is_spline_on==True:
            # applying spline
            # spline parameters
            s = 5.0  # smoothness parameter
            k = 4  # spline order
            nest = -1  # estimate of number of knots needed (-1 = maximal)
            # find the knot points
            x = numpy.asarray(ACROI)[:, 0]

            y = numpy.asarray(ACROI)[:, 1]


            z=numpy.zeros(len(x))
            #tckp,u = scipy.interpolate.splprep([x,y,z],s=s,k=k)
            tckp,u = scipy.interpolate.splprep([x,y,z],s=s,k=k,nest=-1)

            # evaluate spline, including interpolated points
            xnew, ynew, znew = splev(numpy.linspace(0, 1, len(x) / 2), tckp)
            
            xmin=numpy.amin(x)
            xmax=numpy.amax(x)
            ymin=numpy.amin(y)
            ymax=numpy.amax(y)
            
            sxmin=numpy.amin(xnew)
            sxmax=numpy.amax(xnew)
            symin=numpy.amin(ynew)
            symax=numpy.amax(ynew)
            
            Spline=True
            if sxmin<xmin-500:
                Spline=False
            if symin<ymin-500:
                Spline=False
            if sxmax>xmax+500:
                Spline=False
            if symax>ymax+500:
                Spline=False
            # print Spline

            if Spline:
                ACROI = []
                for k in range(len(xnew)):
                    ACROI.append([xnew[k], ynew[k]])

        self.viewer.remove_roi(self.roi)
        self.viewer.add_roi('active_contour', new_roi=ACROI)
        self.formWidget.window().close()


class AnalysisDialog(Ui_Dialog_analysis):
    def __init__(self, *args, **kwargs):
        super(AnalysisDialog, self).__init__(*args, **kwargs)
        self.StormData_to_analyse = []
        self.roi_tag = None
        self.roi_perimeter = None
        self.roi_area = None

        self.analyses = []
        self.analyses.append(NlpAnalysis('analysis_nlp'))
        self.analyses.append(ConvexHullAnalysis('analysis_convex_hull'))
        self.analyses.append(DBScanAnalysis('analysis_dbscan'))
        self.analyses.append(InternalizationSurfaceAnalysis('analysis_internalization_surface'))
        self.analyses.append(InternalizationDrAnalysis('analysis_internalization_dr'))
        self.analyses.append(EuclideanDistanceWithinChannelAnalysis('analysis_euclidean_within'))
        self.analyses.append(EuclideanDistanceBetweenChannelsAnalysis('analysis_euclidean_between'))
        self.analyses.append(SurfaceDistanceBetweenChannelsAnalysis('analysis_euclidean_surface_between'))
        self.analyses.append(SurfaceDensityAnalysis('analysis_surface_density'))
        self.analyses.append(SurfaceDensityDistributionAnalysis('analysis_surface_density_distribution'))
        self.analyses.append(ExportCoordinatesTxtAnalysis('analysis_export_coords'))
        self.analyses.append(ExportCoordinatesPdbAnalysis('analysis_export_pdb'))
        self.analyses.append(QualityControlAnalysis('analysis_quality_control')) # appending new analysis
        # self.analyses.append(NewAnalysis('analysis_new')) # appending new analysis


    def setup_analyses(self, StormData_to_analyse, roi, roi_perimeter, roi_area):
        self.StormData_to_analyse = StormData_to_analyse
        if roi:
            roi_tag = str(roi.text())
        else:
            roi_tag = 'FULL_STORM_DATA'
        self.roi_tag = roi_tag
        self.roi_perimeter = roi_perimeter
        self.roi_area = roi_area
        
        for analysis in self.analyses:
            analysis.setup(self)
            analysis.setup_data(
                self.main_window.viewer.display.StormChannelList,
                self.main_window.viewer.display.StormChannelVisible,
                self.main_window.viewer.display.StormChannelColors,
                self.main_window.viewer.display.ConfocalChannelVisible,
                self.main_window.viewer.display.ConfocalChannelColors,
                self.main_window.viewer.display.ConfocalZNum,
                self.main_window.viewer.display.ConfocalData,
                self.main_window.viewer.display.ConfocalMetaData,

                roi, roi_tag, roi_perimeter, roi_area, self.main_window.viewer.display.ConfocalOffset(),
                self.checkBox_analysis_export_plots, self.groupBox_analysis_euclidean_between_confocal,
                self.main_window.viewer.display

            )
            analysis.setup_filenames(
                self.main_window.working_directory,
                self.main_window.viewer.current_storm_image.file_path,
                self.main_window.viewer.current_confocal_image
            )

    def setup(self):
        self._setup_components()
        # self._init_settings_values()
        self._add_input_handlers()

    def _setup_components(self):
        widgets = list(self.__dict__.keys())
        self.radio_buttons = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('radioButton') != -1]
        self.check_boxes = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('checkBox') != -1]
        self.combo_boxes = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('comboBox') != -1]
        self.spin_boxes = [getattr(self, obj_name) for obj_name in widgets if
                           (obj_name.find('spinBox') != -1 or obj_name.find('doubleSpinBox') != -1)]
        self.group_boxes = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('groupBox') != -1]


    def _add_input_handlers(self):
        for group_box in self.group_boxes:
            group_box.toggled.connect(partial(self._on_setting_changed, group_box))
        self.pushButton_analysis_run.clicked.connect(lambda: self.run_analyses())

    def setup_conf_channel(self, channel_list, channels_visible):
        comboBox = self.comboBox_analysis_euclidean_between_channel_from_confocal
        comboBox.clear()
        channels_to_add = []
        for i, channel in enumerate(channel_list):
            if channels_visible[i]:
                channels_to_add.append(str(channel))
        comboBox.addItems(channels_to_add)

    def _on_setting_changed(self, widget, is_init=False):
        setting_widget_qt_type = type(widget).__name__
        setting_key = '_'.join(str(widget.objectName()).split('_')[1:])
        if str(widget.objectName()).find('analysis') != -1:
            if setting_widget_qt_type == 'QGroupBox':
                # if this groupbox is a analysis, enable/disable the analysis
                if setting_key.find('analysis') != -1:
                    for analysis in self.analyses:
                        if analysis.name_prefix == setting_key:
                            analysis.enabled = widget.isChecked()

    def run_analyses(self):
        self.main_window.status_bar.showMessage('Running analyses, please wait...')

        values_simple = []
        for analysis in self.analyses:
            if analysis.enabled:
                StormData_to_analyse = self.StormData_to_analyse
                dimensions = '3d' if self.main_window.storm_settings.storm_config_fileheader_z else '2d'
                channels_num = len([ch for ch in self.main_window.viewer.display.StormChannelVisible if ch])
                values = analysis.run(
                    StormData_to_analyse,
                    channels_num,
                    dimensions
                )
                values_simple.append(values)
        self.write_results_common_to_file(values_simple)

        num = str(self.main_window.storm_settings.get_roi_counter())
        if type(self.analyses[0].ROI).__name__ == 'EllipseRoi':
            self.analyses[0].ROI.ChangeName("ellipseROI_"+num)
        elif type(self.analyses[0].ROI).__name__ == 'CircleRoi':
            self.analyses[0].ROI.ChangeName("circleROI_"+num)
        elif type(self.analyses[0].ROI).__name__ == 'FreehandRoi':
            self.analyses[0].ROI.ChangeName("freehandROI_"+num)   
        elif type(self.analyses[0].ROI).__name__ == 'ActiveContourRoi':
            self.analyses[0].ROI.ChangeName("activeContourROI_"+num)               
        self.main_window.storm_settings.clear_rois()
        self.main_window.storm_settings.add_roi(self.analyses[0].ROI)
       
        
        
        StormFileName=''
        if self.main_window.viewer.current_storm_image!=None:
                StormFileName=str.split(self.main_window.viewer.current_storm_image.file_path,os.sep)[-1]
        ConfocalFileName='' 
        if self.main_window.viewer.current_confocal_image!=None:  
                ConfocalFileName=str.split(self.main_window.viewer.current_confocal_image.file_path,os.sep)[-1]
        self.main_window.status_bar.showMessage('Ready '+'StormFile:'+StormFileName+' ConfocalFile:'+ConfocalFileName)
        self.scrollAreaWidgetContents.window().close()


    def write_results_common_to_file(self, computed_values_simple):
        # write to common file, simple values
        storm_file_name = os.path.basename(self.main_window.viewer.current_storm_image.file_path).split('.')[0]
        output_file_common = os.path.join(
            self.main_window.working_directory,
            storm_file_name + '_' + self.roi_tag + '_' + 'Results' + '.txt'
        )

        firstline = ''
        secondline = ''
        headers = []
        headers.append(['date_time', str(datetime.datetime.now()).split('.')[0]])
        headers.append(['version', version_num])
        headers.append(['storm_file', storm_file_name])
        headers.append(['ROI_tag', self.roi_tag])
        for header in headers:
            firstline += header[0] + '\t'
            secondline += header[1] + '\t'

        for analysis_values in computed_values_simple:
            if analysis_values:
                for value in analysis_values:
                    firstline += value[0] + '\t'
                    secondline += value[1] + '\t'
        f = open(output_file_common, 'w')
        f.write(firstline[:-1] + '\n')
        f.write(secondline[:-1]+ '\n')
        f.close()


class MatrixParameters(Ui_Dialog_Matrix_Parameters):
    def __init__(self, *args, **kwargs):
        super(MatrixParameters, self).__init__(*args,**kwargs)
        self.opts = {}

    def setup(self):
        self.main_window.viewer.push_view_to_dialog()
        self._add_input_handlers()

    def set_opts(self, opts):
        self.opts = opts
        self._set_center(opts['center'])
        self.distance.setValue(self.opts['distance'])
        self.elevation.setValue(self.opts['elevation'])
        self.fov.setValue(self.opts['fov'])
        self.azimuth.setValue(self.opts['azimuth'])

    def get_opts(self):
        self.opts['center'] = self._get_center()
        self.opts['distance'] = self.distance.value()
        self.opts['elevation'] = self.elevation.value()
        self.opts['fov'] = self.fov.value()
        self.opts['azimuth'] = self.azimuth.value()
        # TODO:CHECK if changed
        self.opts['slices'] = [self.from_sim_stack.value(), self.to_sim_stack.value()]
        #self.opts['roi'] = self.slice_sim_with_roi.isChecked()
        return self.opts

    def _set_center(self, center):
        self.center_x.setValue(center.x())
        self.center_y.setValue(center.y())
        self.center_z.setValue(center.z())

    def _get_center(self):
        return QtGui.QVector3D(self.center_x.value(), self.center_y.value(), self.center_z.value())

    def _ortho(self):
        self.pushButton_sim_3d.setChecked(False)
        self.pushButton_dstorm_3d.setChecked(False)
        self.main_window.viewer.change_dstorm_dim(False)
        self.main_window.viewer.change_sim_dim(False)
        self.elevation.setValue(90)
        self.fov.setValue(60)
        self.azimuth.setValue(90)
        self.main_window.viewer.push_view_to_display()
        self.main_window.viewer.push_view_to_dialog()

    def push_to_display(self, default=False):
        self.main_window.viewer.push_view_to_display(default=default)

    def set_sim_slices(self, maximum):
        self.to_sim_stack.setValue(maximum)
        self.to_sim_stack.setMaximum(maximum)

    def _add_input_handlers(self):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(
            lambda: self.push_to_display())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).clicked.connect(
            lambda: self.push_to_display(default=True))
        self.pushButton_sim_3d.clicked.connect(
            lambda: (self.main_window.viewer.change_sim_dim(
                self.pushButton_sim_3d.isChecked()),
                self.main_window.deactivate_sliders(self.pushButton_sim_3d.isChecked()),
                self.pushButton_ortho.setChecked(False)))
        self.pushButton_dstorm_3d.clicked.connect(
            lambda: (self.main_window.viewer.change_dstorm_dim(self.pushButton_dstorm_3d.isChecked()),
                self.pushButton_ortho.setChecked(False)))
        self.pushButton_alpha_shape.clicked.connect(
            lambda: self.main_window.viewer.show_alpha_complex(130, self.pushButton_alpha_shape.isChecked()))
        self.pushButton_ortho.clicked.connect(
            lambda: self._ortho())


class ExportDialog(Ui_Dialog_Export_Roi):
    def __init__(self, *args, **kwargs):
        super(ExportDialog, self).__init__(*args,**kwargs)

    def setup(self):
        self._add_input_handlers()
        self.lineEdit_path.setText(QString(os.getcwd()))


    def save_roi(self):
        to_save = [self.checkBox_save_loc.isChecked(),
                   self.checkBox_save_dstorm_image.isChecked(),
                   self.checkBox_save_sim_image.isChecked()]
        path = str(self.lineEdit_path.text()+"\\")
        #self.main_window.viewer.save_roi(path, to_save)
        #x= PIL.Image.fromarray(numpy.swapaxes(numpy.fliplr(self.sim.astype(numpy.uint8)),0,1)).convert('RGBA')
        both = PIL.Image.blend(self.sim, self.dstorm, 0.5)
        if to_save[0]:
            TransformLocFile.saveLocFile(path + r"_localizations.txt", self.loc[...,[0,1,3,5,4,2]])
        if to_save[1]:
            self.dstorm.save(path + r"dSTORM_image.png")
        if to_save[2]:
            self.sim.save(path + r"SIM_image.png")
        if numpy.all(to_save[1:3]):
            both.save(path + r"both_image.png")

    def add_images(self, loc, dstorm, sim):
        self.loc = loc
        self.dstorm = dstorm
        self.sim = sim

    def _add_input_handlers(self):
        self.pushButton_Mode_Rect.clicked.connect(lambda: self.viewer.change_roi_mode("Rect"))
        self.pushButton_Cancel.clicked.connect(lambda: self.viewer.change_drag_mode(False), 0)
        self.pushButton_Save.clicked.connect(lambda: self.save_roi())


class RoiDialog(Ui_Dialog_Roi):
    def __init__(self, *args, **kwargs):
        super(RoiDialog, self).__init__(*args,**kwargs)
        self.markerSTORM = []
        self.markerSIM = []
        self.box = pg.PlotWidget()
        self.box2 = pg.PlotWidget()

    def setup(self):
        self._add_input_handlers()
        self.view_container_layout_sim.addWidget(self.box)
        self.view_container_layout_dstorm.addWidget(self.box2)
        self.box.show()
        self.box2.show()

    def delete_roi(self):
        self.main_window.viewer.delete_roi()

    def _add_input_handlers(self):
        self.buttonBox.accepted.connect(lambda: (QtWidgets.QDialog.accept(self.qtDialog),
                                                 self.main_window.viewer.display.ChangePanMode("Pan")))
        self.buttonBox.rejected.connect(lambda: (self.delete_roi(), QtWidgets.QDialog.accept(self.qtDialog),
                                                 self.main_window.viewer.display.ChangePanMode("Pan")))
        self.push_buttom_correlate.pressed.connect(lambda: self.main_window.viewer.QWindow.correlationTest())

    def closeEvent(self, event):
        self.main_window.viewer.display.ChangePanMode("Pan")

    def set_bottom_text(self, text):
        self.label_info_registration.setText(QString(text))

    #add interface
    def add_images(self, dStorm, SIM):
        self.box.clear()
        self.box2.clear()
        x = dStorm.copy()
        x[...,0] += SIM.astype(numpy.uint8)#why read only? gaussian blur...
        #dstorm_data = numpy.rot90(numpy.asarray(dStorm).reshape(dStorm.size[1], dStorm.size[0], 4),3)
        #sim_data = numpy.rot90(numpy.asarray(SIM).reshape(SIM.shape[1], SIM.shape[0], 4),3)

        sim_image = pg.ImageItem(x.astype("f"))
        dstorm_image = pg.ImageItem(dStorm.astype("f"))
        self.box.addItem(sim_image)
        self.box2.addItem(dstorm_image)
        sim_image.show()
        dstorm_image.show()
        self.main_window.viewer.display.QWindow.analyse_correlation_test(dStorm, SIM)


class ImageRegistrationDia(Ui_Dialog_Imagereg):
    def __init__(self, *args, **kwargs):
        super(ImageRegistrationDia, self).__init__(*args,**kwargs)


        self.fijiPath = ""
        self.landmarkPath = ""
        try:
            with open(os.getcwd() + r"\resources\SettingsPath.txt", "r") as settings:
                path = settings.read().split("\n")
                self.fijiPath = path[0]
                self.landmarkPath = path[1]
        except:
            print("No path yet")


    def _resetSpinBox(self, mode):
        getattr(self, "doubleSpinBox_Marker"+ mode + "X").setValue(0)
        getattr(self, "doubleSpinBox_Marker"+ mode + "Y").setValue(0)

    def setCombo(self, Pos, color):
        self.markerSTORM, self.markerSIM = Pos
        for i in range(len(self.markerSTORM)):
            if self.comboBox_MarkerNr_STORM.itemText(i) != str(i):
                icon = pg.QtGui.QIcon()
                pixmap = pg.QtGui.QPixmap(22, 22)
                pixmap.fill(pg.QtGui.QColor(color[i][0],color[i][1],color[i][2],alpha = color[i][3]))
                icon.addPixmap(pixmap)
                self.comboBox_MarkerNr_STORM.insertItem(i, icon, str(i))
        for i in range(len(self.markerSIM)):
            if self.comboBox_MarkerNr_SIM.itemText(i) != str(i):
                icon = pg.QtGui.QIcon()
                pixmap = pg.QtGui.QPixmap(22, 22)
                pixmap.fill(pg.QtGui.QColor(color[i][0],color[i][1],color[i][2],alpha = color[i][3]))
                icon.addPixmap(pixmap)
                self.comboBox_MarkerNr_SIM.insertItem(i, icon, str(i))

    def deleteMarker(self, i, mode):
        if i != -1:
            del getattr(self, "marker" + mode)[i]
            box = getattr(self, "comboBox_MarkerNr_" + mode)
            box.removeItem(box.__len__()-1)
            if box.__len__() == 0:
                self._resetSpinBox(mode)
            else:
                self.setSpin(mode)
        self.pushGL()

    def deleteAll(self):
        for i in range(len(self.markerSTORM)):
            self.deleteMarker(0, "STORM")
        for i in range(len(self.markerSIM)):
            self.deleteMarker(0, "SIM")

    def set_markers(self, x, y, mode):
        getattr(self, "marker" + mode)[getattr(self, "comboBox_MarkerNr_" + mode).currentIndex()].setX(x)
        getattr(self, "marker" + mode)[getattr(self, "comboBox_MarkerNr_" + mode).currentIndex()].setY(y)
        self.pushGL()


    def pushGL(self):
        self.main_window.viewer.push_markers_to_display(self.markerSTORM, self.markerSIM)

    def setSpin(self, mode):
        if getattr(self, "comboBox_MarkerNr_" + mode).currentIndex() != -1:
            getattr(self, "doubleSpinBox_Marker" + mode + "X").setValue(getattr(self, "marker" + mode)[getattr(self, "comboBox_MarkerNr_" + mode).currentIndex()].x())
            getattr(self, "doubleSpinBox_Marker" + mode + "Y").setValue(getattr(self, "marker" + mode)[getattr(self, "comboBox_MarkerNr_" + mode).currentIndex()].y())

    def setup(self):
        self.markerSTORM = []
        self.markerSIM = []
        self.fijiPathLineEdit.setText(self.fijiPath)
        self.landmarkPathLineEdit.setText(self.landmarkPath)
        self._add_input_handlers()

    def _add_input_handlers(self):
        self.buttonBox.accepted.connect(lambda: (self.register(), QtWidgets.QDialog.accept(self.qtDialog)))
        #self.buttonBox.rejected.connect(lambda: (self.deleteAll(), QtGui.QDialog.accept(self.qtDialog)))
        self.pushButton_set_SIM.pressed.connect(lambda: self.set_markers(self.doubleSpinBox_MarkerSIMX.value(), self.doubleSpinBox_MarkerSIMY.value(), "SIM"))
        self.pushButton_set_STORM.pressed.connect(lambda: self.set_markers(self.doubleSpinBox_MarkerSTORMX.value(), self.doubleSpinBox_MarkerSTORMY.value(), "STORM"))
        self.comboBox_MarkerNr_STORM.currentIndexChanged.connect(lambda: self.setSpin("STORM"))
        self.pushButton_delete_STORM.clicked.connect(lambda: self.deleteMarker(self.comboBox_MarkerNr_STORM.currentIndex(), "STORM"))
        self.pushButton_delete_SIM.clicked.connect(lambda: self.deleteMarker(self.comboBox_MarkerNr_SIM.currentIndex(), "SIM"))
        self.comboBox_MarkerNr_SIM.currentIndexChanged.connect(lambda: self.setSpin("SIM"))
        self.open_landmark_file.clicked.connect(lambda: self.loadMarkers())
        self.pushButton_GHT.clicked.connect(lambda: self.main_window.viewer.perform_ght(0))

    def loadMarkers(self):
        self.landmarkPath = str(self.landmarkPathLineEdit.text())
        Landmarks = read_csv(self.landmarkPath, skiprows=1, engine="c", na_filter=False, header=None, delim_whitespace=True, dtype=numpy.float32).as_matrix()
        dst = Landmarks[:,3:5]
        src = Landmarks[:,1:3]
        sim = []
        storm = []
        for marker in src:
            sim.append(pg.QtGui.QVector2D(marker[0],marker[1]))
        self.markerSIM = sim
        for marker in dst:
            storm.append(pg.QtGui.QVector2D(marker[0],marker[1]))
        self.markerSTORM = storm
        self.pushGL()
        with open(os.getcwd() + r"\resources\SettingsPath.txt", "w") as settings:
            settings.write(self.fijiPath + "\n" + self.landmarkPath)

    def register(self):
        cwd = os.getcwd()
        Scale=1000.0/self.main_window.viewer.display.ConfocalSizeMultiplier
        ScaleX=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']
        ScaleY=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeY']
        self.setLandmarks(ScaleX, ScaleY)

        #self.main_window.viewer.display.QWindow.save_current_overlay()todo:bUnwarpJ needs overlay

        if self.comboBox_registration_mode.currentIndex() == 0:
            self.fijiPath = str(self.fijiPathLineEdit.text())
            with open(os.getcwd() + r"\resources\SettingsPath.txt", "w") as settings:
                settings.write(self.fijiPath + "\n" + self.landmarkPath)
            self._unwarp()
            self.main_window.viewer.current_storm_image.isParsingNeeded = True
            self.main_window.viewer.current_storm_image.matrix = cwd + r"\temp\converted_Matrix.txt"
            self.main_window.viewer.show_storm_image(self.main_window.storm_images_list.selectedItems())
            self.deleteAll()
        elif self.comboBox_registration_mode.currentIndex() == 1:
            self.main_window.viewer.current_storm_image.transformAffine(path=(cwd + r"\temp\Landmarks.txt"))
            self.main_window.viewer.show_storm_image(self.main_window.storm_images_list.selectedItems())

    def _unwarp(self):
        cwd = os.getcwd()

        warp = bunwarpJ_cmd_support.bUnwarpJPython(self.fijiPath, cwd + r"\temp\SIM_temp.png", cwd + r"\temp\dSTORM_temp.png")
        warp.align( "NULL",  "NULL",
                   0, 2, 0, 0.1, 0.1, 0, 0, cwd + r"\temp\output1.tif", cwd + r"\temp\output2.tif" , landmarks = cwd + r"\temp\Landmarks.txt", save_transformation=True)
        warp.run()
        warp.convert_transformation_to_raw(cwd + r"\temp\output1_transf.txt", cwd + r"\temp\converted_Matrix.txt")
        warp.run()


    def setLandmarks(self, ScaleX, ScaleY):
        cwd = os.getcwd()
        Landmarks = "Index\txSource\tySource\txTarget\tyTarget\n"
        #stormMarkers, simMarkers = self.main_window.viewer.display.getMarkers()
        for i in range(len(self.markerSTORM)):
            SimMarker = self.markerSIM[i]
            StormMarker = self.markerSTORM[i]
            List = [SimMarker.x(),
                    SimMarker.y(), StormMarker.x(), StormMarker.y()]
            Landmarks += "    " + str(int(i))
            for item in List:
                Landmarks += "\t    " + str(int(item))
            Landmarks +="\n"
        with open(cwd + r"\temp\Landmarks.txt", 'w') as file:
            file.write("{}".format(Landmarks))


class ImageRegistrationDialog(Ui_Dialog_imageregistration):
    def __init__(self, *args, **kwargs):
        super(ImageRegistrationDialog, self).__init__(*args, **kwargs)
        self.resetting = False

    def reset_channels(self):
        self.resetting = True
        while self.comboBox_storm_channel_changer.count() > 0:
            self.comboBox_storm_channel_changer.removeItem(0)
        while self.comboBox_confocal_channel_changer.count() > 0:
            self.comboBox_confocal_channel_changer.removeItem(0)
        self.resetting = False

    def setup_channels(self, mode, channel_list, channels_visible, RegChannelNum):
        comboBox = None
        if mode == 'storm':
            comboBox = self.comboBox_storm_channel_changer
        elif mode == 'confocal':
            comboBox = self.comboBox_confocal_channel_changer
        channels_to_add = []
        RegChannelVisible=False
        for i, channel in enumerate(channel_list):
            if channels_visible[i]:
                if i==RegChannelNum:
                    RegChannelVisible=True  
                channels_to_add.append(str(channel))
        comboBox.addItems(channels_to_add)
        if RegChannelNum!=-1 and RegChannelVisible:
            index =comboBox.findText(str(channel_list[RegChannelNum]))
            comboBox.setCurrentIndex(index)
        

    def setup(self):
        self._add_input_handlers()


    def _add_input_handlers(self):
        self.comboBox_storm_channel_changer.currentIndexChanged.connect(
            lambda: self.change_channel('storm', self.comboBox_storm_channel_changer.currentText()))
        self.comboBox_confocal_channel_changer.currentIndexChanged.connect(
            lambda: self.change_channel('confocal', self.comboBox_confocal_channel_changer.currentText()))
        self.pushButton_manual_selection.clicked.connect(lambda: self.put_manual_markers())
        self.pushButton_delete_markers.clicked.connect(lambda: self.delete_markers())
        self.open_landmark_file.clicked.connect(lambda: self.loadMarkers())
        #self.pushButton_Registration.clicked.connect(lambda: self.Register())
        self.pushButton_Registration.clicked.connect(lambda: self.Reg())
        self.pushButton_automatic_selection.clicked.connect(lambda: self.AutomaticMarkers())

    def AutomaticMarkers(self): 
        self.delete_markers()
        Scale=1000.0/self.main_window.viewer.display.ConfocalSizeMultiplier
        ScaleX=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']
        ScaleY=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeY']
        #add storm markers
        #k-means on Storm point
        G=numpy.array(self.main_window.viewer.display.StormData_filtered[self.main_window.viewer.display.Viewbox.StormRegistrationChannel])
        #SelectedCentroids,tmp=Clust.kmeans(G[:,0:2],3)
        #Select the three most dense regions instead of k-means:
        AllStormPoints=G[:,0:2]
        SelectedCentroids=[[AllStormPoints[0,0],AllStormPoints[0,1]], [AllStormPoints[1,0],AllStormPoints[1,1]], [AllStormPoints[2,0] , AllStormPoints[2,1]]]
        Neighbours=[0, 0, 0]
        Radius=200
        PointNum=0
        Image = self.main_window.viewer.current_confocal_image.ConfocalData[0]
        for StP in AllStormPoints:
            PointNum+=1
            Neighbourpoints=0
            SumCentroid=[0, 0]
            DistanceMatrix=numpy.sqrt(numpy.square(AllStormPoints[:,0]-StP[0])+numpy.square(AllStormPoints[:,1]-StP[1]))
            Candidates=numpy.where(DistanceMatrix<Radius)
            Neighbourpoints=len(Candidates[0])
            NewCentroid=numpy.mean(AllStormPoints[Candidates],0)
            
            ind=0
            NotInserted=True
            while ind<len(Neighbours) and NotInserted:
                #this is a new maximum, instert it
                if Neighbours[ind]<Neighbourpoints:
                    #check if the current point is not inserted:
                    NotClose=True
                    for a in SelectedCentroids:
                        if math.sqrt(math.pow(a[0]-NewCentroid[0],2)+math.pow(a[1]-NewCentroid[1],2))<Radius:
                            NotClose=False
                    if NotClose:    
                        Neighbours[ind]=Neighbourpoints
                        NotInserted=False
                        SelectedCentroids[ind][0]=NewCentroid[0]
                        SelectedCentroids[ind][1]=NewCentroid[1]
                ind+=1
        for c in SelectedCentroids:
            Marker= pg.ROI([0, 0])
            self.main_window.viewer.display.Viewbox.StormMarkerRois.append(Marker)
            Marker.addTranslateHandle([c[0],c[1]],[0.5, 0.5])   
            Handle=Marker.getHandles()[0]                  
            Handle.sides=4
            Handle.startAng=0
            Handle.buildPath()
            Handle.generateShape()                             
            self.main_window.viewer.display.plot_widget.addItem(Marker)
            #add confocal markers for storm marker

            
            MidX=int(c[1]/ScaleX)
            MidY=int(c[0]/ScaleY)
            #searhc for appropriate point in 5 % of the image distance
            radius=int(Image.shape[0]*0.05)
            FromX=max(MidX-radius,0)
            TillX=min(MidX+radius,Image.shape[0])
            FromY=max(MidY-radius,0)
            TillY=min(MidY+radius,Image.shape[1])
            Cut=Image[FromX:TillX,FromY:TillY]
            Max=numpy.argmax(Cut)
            Xorig=(Max/Cut.shape[0])
            Yorig=(Max-(Xorig*Cut.shape[0]))
            Y=int(ScaleX*(Xorig+MidX-Cut.shape[0]/2))
            X=int(ScaleY*(Yorig+MidY-Cut.shape[1]/2))
            Marker= pg.ROI([0, 0])
            self.main_window.viewer.display.Viewbox.ConfMarkerRois.append(Marker)
            #shift the points based on the confocal shift position
            X+=self.main_window.viewer.display.Viewbox.ConfocalOffset[1]*ScaleX
            Y+=self.main_window.viewer.display.Viewbox.ConfocalOffset[0]*ScaleY
            Marker.addFreeHandle([X,Y])                    
            self.main_window.viewer.display.plot_widget.addItem(Marker)

    #Save temporary STORM and SIM images. SIM image is reduced to overlay with STORM
    #Save Landmarks in txt file(bUnwarpJ syntax)
    #Unwarp via landmarks and save transformation matrix
    #Reload STORM with set matrix
    def Reg(self):
        cwd = os.getcwd()
        Scale=1000.0/self.main_window.viewer.display.ConfocalSizeMultiplier
        ScaleX=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']
        ScaleY=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeY']
        self.setTempImages(ScaleX, ScaleY)
        self.setLandmarks(ScaleX, ScaleY)
        self.unwarp()
        self.main_window.viewer.current_storm_image.transform()
        self.main_window.viewer.current_storm_image.isParsingNeeded = True
        self.main_window.viewer.current_storm_image.matrix = cwd + r"\temp\converted_Matrix.txt"
        self.main_window.viewer.show_storm_image(self.main_window.storm_images_list.selectedItems())

    def unwarp(self):

        cwd = os.getcwd()
        with open(cwd + r"\resources\Settings.txt", "r") as Settings:
            for item in Settings.read().split("\n"):
                if "Fiji Path" in item:
                    fijiPath = item.split("\t")[-1]

        warp = bunwarpJ_cmd_support.bUnwarpJPython(fijiPath, cwd + r"\temp\20151203_sample2_Al532_Tub_1.png", cwd + r"\temp\20151203_sample2_Al532_Tub_1.png")
        warp.align( "NULL",  "NULL",
                   0, 2, 0, 0.1, 0.1, 0, 0, cwd + r"\temp\output1.tif", cwd + r"\temp\output2.tif" , landmarks = cwd + r"\temp\Landmarks.txt", save_transformation=True)
        warp.run()
        warp.convert_transformation_to_raw(cwd + r"\temp\output1_transf.txt", cwd + r"\temp\converted_Matrix.txt")
        warp.run()

    def setLandmarks(self, ScaleX, ScaleY):
        cwd = os.getcwd()
        Landmarks = "Index\txSource\tySource\txTarget\tyTarget\n"
        stormMarkers, simMarkers = self.main_window.viewer.display.getMarkers()
        for i in range(len(stormMarkers)):
            SimMarker = simMarkers[i]
            StormMarker = stormMarkers[i]
            List = [SimMarker.x()/float(ScaleX),
                    SimMarker.y()/float(ScaleX), StormMarker.x()/float(ScaleX), StormMarker.y()/float(ScaleY)]
            Landmarks += "    " + str(int(i))
            for item in List:
                Landmarks += "\t    " + str(int(item))
            Landmarks +="\n"
        with open(cwd + r"\temp\Landmarks.txt", 'w') as file:
            file.write("{}".format(Landmarks))

    #0 x 896 beheben
    def setTempImages(self, ScaleX, ScaleY):
        cwd = os.getcwd()
        imags = self.main_window.viewer.display.ConfChannelToShow
        dSTORM_size = self.main_window.viewer.current_storm_image.size
        xmin = int(self.main_window.viewer.display.Viewbox.ConfocalOffset[0]*-1) #positiver offset
        xmax = int(xmin+dSTORM_size[0]*10**9/ScaleX)
        ymin = int(self.main_window.viewer.display.Viewbox.ConfocalOffset[1]*-1)
        ymax = int(ymin+dSTORM_size[1]*10**9/ScaleY)
        imag = numpy.expand_dims(imags[0][xmin:xmax, ymin:ymax], axis=0)
        tifffile.imsave((cwd + r'\temp\SIMUnwarp.tif'), imag)
        storm = numpy.array(self.main_window.viewer.display.StormData_filtered[self.main_window.viewer.display.Viewbox.StormRegistrationChannel])
        tifffile.imsave((cwd + r"\temp\STORMUnwarp.tif"), storm)

    def Register(self): 
        #check if we have enough markers
        if self.main_window.viewer.display.Viewbox.AffineTransform != []:
            self.main_window.show_error(message='Images are alredy registered, please reload Confocal data for new registration') 
        elif len(self.main_window.viewer.display.Viewbox.StormMarkerRois)!=3 and len(self.main_window.viewer.display.Viewbox.ConfMarkerRois)!=3:
            self.main_window.show_error(message='Not enough marker points for registration')            
        else:
            Aff=numpy.zeros((2,3))
            StormPoints=numpy.ones((3,3))
            ConfocalPoints=numpy.ones((3,3))
            Scale=1000.0/self.main_window.viewer.display.ConfocalSizeMultiplier
            ScaleX=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']
            ScaleY=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeY']
            Index=0
            for roi in self.main_window.viewer.display.Viewbox.ConfMarkerRois:
                P=roi.getLocalHandlePositions()[0][1]
                ConfocalPoints[Index,0]=((P.x()-self.main_window.viewer.display.Viewbox.ConfocalOffset[0])/float(ScaleX))
                ConfocalPoints[Index,1]=((P.y()-self.main_window.viewer.display.Viewbox.ConfocalOffset[1])/float(ScaleY))
                Index+=1
            Index=0
            for roi in self.main_window.viewer.display.Viewbox.StormMarkerRois:
                P=roi.getLocalHandlePositions()[0][1]
                StormPoints[Index,0]=(P.x()/float(ScaleX))
                StormPoints[Index,1]=(P.y()/float(ScaleY))
                Index+=1
            # Pad the data with ones, so that our transformation can do translations too
            n = ConfocalPoints.shape[0]
            X = numpy.matrix(ConfocalPoints)
            Y = numpy.matrix(StormPoints)
            # Solve the least squares problem X * Aff = Y
            # to find our transformation matrix Aff
            A=X.I*Y
            
            ConfShape=self.main_window.viewer.display.ConfChannelToShow.shape
            Aff[:2,:2]=A[:2,:2]
            tmp=Aff[1,0]
            Aff[1,0]=Aff[0,1]
            Aff[0,1]=tmp
            Aff[0,2]=A[2,0]
            Aff[1,2]=A[2,1]
            self.main_window.viewer.display.Viewbox.AffineTransform = Aff
            #apply affine transformation
            for ChInd in range(ConfShape[0]):
                self.main_window.viewer.display.ConfChannelToShow[ChInd,:,:]=cv2.warpAffine(self.main_window.viewer.display.ConfChannelToShow[ChInd,:,:],Aff,(self.main_window.viewer.display.ConfChannelToShow[ChInd,:,:].shape))
            #adjust confocal markers to strom markers
            for RoiInd in range(len(self.main_window.viewer.display.Viewbox.ConfMarkerRois)):
                Marker= pg.ROI([0, 0])
                OldPoints=self.main_window.viewer.display.Viewbox.StormMarkerRois[RoiInd].getLocalHandlePositions()[0][1]
                self.main_window.viewer.display.plot_widget.removeItem(self.main_window.viewer.display.Viewbox.ConfMarkerRois[RoiInd]) 
                self.main_window.viewer.display.Viewbox.ConfMarkerRois[RoiInd]=Marker
                Marker.addFreeHandle([OldPoints.x(),OldPoints.y()])
                self.main_window.viewer.display.plot_widget.addItem(Marker) 
            self.main_window.viewer.display.ShowAll()
            
    def put_manual_markers(self):
        self.main_window.show_error(message='Place storm (◇) and confocal Markers (□)')
        self.main_window.viewer.display.ChangePanMode("Reg")

    def delete_markers(self):
        #self.main_window.viewer.display.QWindow.resetMarkers
        self.main_window.viewer.display.Viewbox.ClickMode='Norm'      
        for Roi in self.main_window.viewer.display.Viewbox.StormMarkerRois:
            self.main_window.viewer.display.plot_widget.removeItem(Roi)                 
        for Roi in self.main_window.viewer.display.Viewbox.ConfMarkerRois:
            self.main_window.viewer.display.plot_widget.removeItem(Roi)
        self.main_window.viewer.display.Viewbox.StormMarkerRois=[]
        self.main_window.viewer.display.Viewbox.ConfMarkerRois=[]
            
    def change_channel(self, mode, channel_name):
        if channel_name and not self.resetting:
            channel_num =  None
            if mode == 'storm':
                channel_num = self.main_window.viewer.display.StormChannelList.index(channel_name)
                self.main_window.viewer.display.Viewbox.SetRegistrationChannelStorm(channel_num)
            elif mode == 'confocal':
                channel_num = list(range(self.main_window.viewer.display.ConfocalMetaData['ChannelNum'])).index(
                    int(str(channel_name)))
                self.main_window.viewer.display.Viewbox.SetRegistrationChannelConf(channel_num)


class LutDialog(Ui_Dialog_lut):
    def __init__(self, *args, **kwargs):
        super(LutDialog, self).__init__(*args, **kwargs)
        self.resetting = False

    def reset_channels(self):
        self.resetting = True
        while self.comboBox_storm_channel_changer.count() > 0:
            self.comboBox_storm_channel_changer.removeItem(0)
        while self.comboBox_confocal_channel_changer.count() > 0:
            self.comboBox_confocal_channel_changer.removeItem(0)
        self.resetting = False

    def setup_channels(self, mode, channel_list, channels_visible):
        comboBox = None
        if mode == 'storm':
            comboBox = self.comboBox_storm_channel_changer
        elif mode == 'confocal':
            comboBox = self.comboBox_confocal_channel_changer
        channels_to_add = []
        for i, channel in enumerate(channel_list):
            if channels_visible[i]:
                channels_to_add.append(str(channel))
        comboBox.addItems(channels_to_add)

    def setup(self):
        self._add_input_handlers()

    def _add_input_handlers(self):
        self.comboBox_storm_channel_changer.currentIndexChanged.connect(
            lambda: self.change_channel('storm', self.comboBox_storm_channel_changer.currentText()))
        self.comboBox_confocal_channel_changer.currentIndexChanged.connect(
            lambda: self.change_channel('confocal', self.comboBox_confocal_channel_changer.currentText()))

    def change_channel(self, mode, channel_name):
        if channel_name and not self.resetting:
            channel_num = channel_color = None
            if mode == 'storm':
                channel_num = self.main_window.viewer.display.StormChannelList.index(channel_name)
                channel_color = self.main_window.viewer.display.StormChannelColors[channel_num]
                self.main_window.viewer.display.ShowStormLut(channel_num, channel_color)
            elif mode == 'confocal':
                channel_num = list(range(self.main_window.viewer.display.ConfocalMetaData['ChannelNum'])).index(
                    int(str(channel_name)))
                channel_color = self.main_window.viewer.display.ConfocalChannelColors[channel_num]
                self.main_window.viewer.display.ShowConfocalLut(channel_num, channel_color)


class PositioningDialog(Ui_Dialog_positioning):
    def __init__(self, *args, **kwargs):
        super(PositioningDialog, self).__init__(*args, **kwargs)


class ThreeDDialog(Ui_Dialog_3d):
    def __init__(self, *args, **kwargs):
        super(ThreeDDialog, self).__init__(*args, **kwargs)


class DotsDialog(Ui_Dialog_dots):
    def __init__(self, *args, **kwargs):
        super(DotsDialog, self).__init__(*args, **kwargs)


class GaussianDialog(Ui_Dialog_gaussian):
    def __init__(self, *args, **kwargs):
        super(GaussianDialog, self).__init__(*args, **kwargs)
