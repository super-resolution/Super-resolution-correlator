# -*- coding: utf-8 -*-

from .StormDisplay import StormDisplay


from .. import default_config


from ..rois import EllipseRoi, CircleRoi, ActiveContourRoi


import os


import numpy as np,datetime

from impro.processing.CudaAlphaShape import get_k_simplices

from impro.processing.utility import *


try:
    QString = unicode
except NameError:
    # Python 3
    QString = str

class Viewer(object):
    def __init__(self, *args, **kwargs):
        self.main_window = kwargs['main_window']
        self.__init_path__()
        self.display = StormDisplay(self.main_window)
        self.init_channel_colors('storm')
        self.init_channel_colors('confocal')
        self.current_storm_image = None
        self.current_confocal_image = None
        self.current_confocal_image = None

    def __init_path__(self):
        temp = os.getcwd()+r"\temp"
        resource = os.getcwd()+r"\resources"
        try:
            os.stat(temp)
        except:
            os.mkdir(temp)
        try:
            os.stat(resource)
        except:
            print("Critical error resources not found")
            raise

    def init_channel_colors(self, mode):
        for i in range(0, 4):
            color = getattr(self.main_window, 'comboBox_'+ mode + '_channel' + str(i) + '_color').currentText()
            if mode == 'storm':
                self.display.StormChannelColors[i] = default_config.channel_colors[str(color)]
            if mode == 'confocal':
                self.display.ConfocalChannelColors[i] = default_config.channel_colors[str(color)]

    def reset_all_channels_bottom_settings(self, mode):
        for i in range(0, 4):
            getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(i)).setEnabled(False)
            # getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(i)).setChecked(False)
            getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(i)).setText('Ch' + str(i+1))
            getattr(self.main_window, 'comboBox_'+ mode + '_channel' + str(i) + '_color').setEnabled(False)

        if mode == 'storm':
            for i in range(0, 4):
                getattr(self.main_window, 'label_' + mode + '_channel' + str(i) + '_info').setText('-')
        elif mode == 'confocal':
            getattr(self.main_window, 'label_' + mode + '_info').setText('-')

    def set_channel_bottom_settings(self, mode, channel_num, channel_name, text):
        getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(channel_num)).setEnabled(True)
        getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(channel_num)).setText(channel_name)
        getattr(self.main_window, 'comboBox_'+ mode + '_channel' + str(channel_num) + '_color').setEnabled(True)

        if mode == 'storm':
            getattr(self.main_window, 'label_' + mode + '_channel' + str(channel_num) + '_info').setText(text)
        elif mode == 'confocal':
            getattr(self.main_window, 'label_' + mode + '_info').setText(text)

    def set_offset(self, dStorm_offset):
        self.display.QWindow.set_sim_position(-dStorm_offset)

    def push_markers_to_dialoge(self):
        sim, storm, color = self.display.QWindow.get_marker()
        self.main_window.dialog_imageregistration.setCombo((storm, sim), color)
        self.main_window.dialog_imageregistration.setSpin("STORM")
        self.main_window.dialog_imageregistration.setSpin("SIM")

    def push_markers_to_display(self, STORM, SIM):
        self.display.QWindow.set_marker(STORM, SIM)

    def push_view_to_dialog(self):
        opts = self.display.QWindow.get_opts()
        self.main_window.dialog_matrix_parameters.set_opts(opts)

    def push_view_to_display(self, default=False):
        if default:
            self.display.QWindow.reset_view()
        else:
            opts = self.main_window.dialog_matrix_parameters.get_opts()
            self.display.QWindow.set_opts(opts)
            self.display.ShowAllChonfocalChannels()

    def push_custom_scale_to_display(self, pos, length, width):
        self.display.QWindow.set_scale_custom(pos, length, width,)

    def change_dstorm_dim(self, checked):
        if checked == True:
            self.display.QWindow.set_dstorm_dimension("3D")
        elif checked == False:
            self.display.QWindow.set_dstorm_dimension("2D")

    def change_sim_dim(self, checked):
        if checked == True:
            self.display.QWindow.set_sim_dimension("3D")
        elif checked == False:
            self.display.QWindow.set_sim_dimension("2D")

    def save_current_overlay(self, path):
        self.display.QWindow.save_current_overlay(path=path)

    def save_screenshot(self, path):
        screenshot = self.display.QWindow.get_screenshot()
        prefix = str(datetime.datetime.now()).split(" ")[1].replace(":","_").split(".")[0]
        asdf = QString(path + prefix + ".png")
        print(screenshot.save(asdf))

    def freehand_roi(self):
        self.display.ChangePanMode("FreehandRoi")

    def delete_roi(self):
        self.display.QWindow.delete_roi()

    def show_alpha_complex(self, alpha, show):
        points = []
        if show:
            data = self.display.StormData_filtered[0]
            k_simplices = get_k_simplices(data[...,0:2])[0]

            points = np.empty((2*k_simplices.shape[0],5))
            points[::2,0] = data[(k_simplices[...,0]).astype(np.int32),0]
            points[::2,1] = data[(k_simplices[...,0]).astype(np.int32),1]
            points[1::2,0] = data[(k_simplices[...,1]).astype(np.int32),0]
            points[1::2,1] = data[(k_simplices[...,1]).astype(np.int32),1]
            points[...,2] = np.repeat(k_simplices[...,2],2,)
            points[...,3] = np.repeat(k_simplices[...,3],2,)
            points[...,4] = np.repeat(k_simplices[...,4],2,)
        self.display.QWindow.set_alpha_shape(points, alpha, show)

    def perform_ght(self, ch_num):
        #try:
        alpha = np.array(self.display.QWindow.get_alpha_shape())
        sim = self.display.QWindow.sim.data[ch_num]
        img = self.current_confocal_image
        if not img.flip["UpsideDown"]:
            sim = np.flipud(sim)
        if not img.flip["LeftRight"]:
            sim = np.fliplr(sim)
        #except:
        #    print("No alpha shape/ SIM data")
        points1, points2, z, t_list = find_mapping(np.clip(sim,0,255).astype(np.uint8), alpha.astype(np.uint8))
        p_dstorm, q_sim = error_management(t_list, points1, points2)
        x = p_dstorm[:,1]
        y = p_dstorm[:,0].copy()
        p_dstorm[:,0]=x
        p_dstorm[:,1]=y
        x = q_sim[:,1]
        y = q_sim[:,0].copy()
        q_sim[:,0]=x
        q_sim[:,1]=y

        print(p_dstorm,q_sim)
        p_dstorm = np.asarray(p_dstorm)*self.current_confocal_image.metaData['SizeX']*1000
        q_sim = np.asarray(q_sim)*self.current_confocal_image.metaData['SizeX']*1000
        self.main_window.viewer.current_storm_image.transformAffine(src=p_dstorm,dst=q_sim)
        self.main_window.viewer.show_storm_image(self.main_window.storm_images_list.selectedItems())
        #self.set_offset(self.current_storm_image.offset)
        #for marker in p_dstorm:
        #    self.main_window.dialog_imageregistration.set_markers(marker[0], marker[1], "STORM")
        #for marker in q_sim:
        #    self.main_window.dialog_imageregistration.set_markers(marker[0], marker[1], "SIM")
        #self.main_window.dialog_imageregistration.pushGL()
        #map = estimate_transform("affine", q_sim, p_dstorm)
        #self.current_storm_image.stormData[0][:,0:2] = map.inverse(self.current_storm_image.stormData[0][:,0:2])

    def correlation_test(self):
        self.display.QWindow.analyse_correlation_test()

    def construct_new_image_storm(self, imgs):
        basic_image = imgs[0]
        List = []
        ChannelList = []
        for i in range(len(imgs)):
            List.append(imgs[i].stormData[0])
            ChannelList.append("ch" + str(i))
        basic_image.stormData = np.array(List)
        basic_image.StormChannelList = ChannelList
        return basic_image

    def show_storm_image(self, Imgs, prevImage=None):
        if Imgs:
            if self.main_window.working_directory_unset:
                if len(Imgs[0].file_path.split('/'))>1:
                    wd=''
                    parts=Imgs[0].file_path.split('/')
                    for ind in range(len(parts)-1):
                        wd+=parts[ind]+'/'
                    self.main_window.working_directory=wd
                    self.main_window.working_directory_unset=False
                elif len(Imgs[0].file_path.split('\\'))>1:
                    wd=''
                    parts=Imgs[0].file_path.split('\\')
                    for ind in range(len(parts)-1):
                        wd+=parts[ind]+'\\'
                    self.main_window.working_directory=wd
                    self.main_window.working_directory_unset=False

            self.main_window.status_bar.showMessage('Loading image, please wait...')
            self.display.DeleteStormData()
            self.reset_all_channels_bottom_settings('storm')
            for Img in Imgs:
                if Img.isParsingNeeded:
                    #try:
                        Img.parse()
                    #except ValueError:
                       # Img.isParsingNeeded = True
                       # self.main_window.status_bar.showMessage('File format error / wrong headers used!')
                        return False
            build_Basic = self.construct_new_image_storm(Imgs)

            self.current_storm_image = build_Basic
            self.display.AddStormData(build_Basic)
            #  self.openGL_Display.setSTORM(build_Basic)
            for i, channel_name in enumerate(build_Basic.StormChannelList):
                self.set_channel_bottom_settings('storm', i, channel_name,
                                                 'Points: ' + str(len(self.display.StormData_filtered[i])))

            self.main_window.storm_settings.set_rois()

            self.display.ShowAllStormChannels()
            StormFileName=''
            if self.main_window.viewer.current_storm_image!=None:
                StormFileName=str.split(self.main_window.viewer.current_storm_image.file_path,os.sep)[-1]
            ConfocalFileName='' 
            if self.main_window.viewer.current_confocal_image!=None:  
                ConfocalFileName=str.split(self.main_window.viewer.current_confocal_image.file_path,os.sep)[-1]
            self.main_window.status_bar.showMessage('Ready '+'dStormFile:'+StormFileName+' SimFile:'+ConfocalFileName)


    #multiple images not supported atm
    def show_confocal_image(self, Imgs, prevImage=None, skip = False, ApplyButton=False):#nex
        if Imgs:
            self.main_window.status_bar.showMessage('Loading image, please wait...')
            #self.display.DeleteConfocalData()
            self.reset_all_channels_bottom_settings('confocal')
            for i in range(len(Imgs)):
                if Imgs[i].isParsingNeeded:
                    try:
                        Imgs[i].parse(self.main_window.confocal_settings.confocal_config_calibration_px, self.main_window, ApplyButton)
                        for y in range(Imgs[i].metaData["ShapeSizeC"]):
                            getattr(self.main_window, 'slider_confocal_channel' + str(y) + '_slice').setMaximum(Imgs[i].metaData["ShapeSizeZ"]-1)
                        # TODO: UNHACKING
                        opts = self.display.QWindow.get_opts()
                        opts["slices"] = [0,Imgs[0].metaData['ShapeSizeZ']]
                        self.display.QWindow.set_opts(opts)
                    except ValueError:
                        Imgs[i].isParsingNeeded = True
                        self.main_window.status_bar.showMessage('File format error / wrong headers used!')
                        return False

                for y in range(Imgs[i].metaData["ShapeSizeC"]):
                    Imgs[i].setIndex(y, getattr(self.main_window, 'slider_confocal_channel' + str(y) + '_slice').value())
                t1 = datetime.datetime.now()
                Imgs[i].setFlip("LeftRight", getattr(self.main_window, 'checkBox_flip_lr').isChecked())
                Imgs[i].setFlip("UpsideDown", getattr(self.main_window, 'checkBox_flip_ud').isChecked())


                #Imgs[i].getRelevantData()

            self.current_confocal_image = Imgs[0]

            self.display.AddConfocalData(Imgs[0])
            t2 = datetime.datetime.now()
            print(t2-t1)
            #self.display.ConfocalZ = getattr(self.main_window, "doubleSpinBox_confocal_z").value()
            # self.main_window.label_confocal_channel0_info.setText(str(currentImage.ConfocalMetaData))
            Z_Slices = ""
            for i in range(self.current_confocal_image.metaData['ChannelNum']):
                Z_Slices += str(self.current_confocal_image.index[i]+1) + ', '
                self.set_channel_bottom_settings('confocal', i, 'i',
                    '[All channels] ' +
                    'Pixel size: ' + str(self.display.ConfocalMetaData['SizeX']) +' | '+
                    'Z slices: ' + Z_Slices)

            self.main_window.dialog_matrix_parameters.set_sim_slices(self.current_confocal_image.metaData['ShapeSizeZ'])

            self.display.ShowAllChonfocalChannels()

            StormFileName=''
            if self.main_window.viewer.current_storm_image!=None:
                StormFileName=str.split(self.main_window.viewer.current_storm_image.file_path,os.sep)[-1]
            ConfocalFileName=''
            if self.main_window.viewer.current_confocal_image!=None:
                ConfocalFileName=str.split(self.main_window.viewer.current_confocal_image.file_path,os.sep)[-1]
            self.main_window.status_bar.showMessage('Ready '+'StormFile:'+StormFileName+' ConfocalFile:'+ConfocalFileName)

    def update_confocal_image(self):
        if self.current_confocal_image != None:
            for y in range(self.current_confocal_image.metaData["ShapeSizeC"]):
                self.current_confocal_image.setIndex(y, getattr(self.main_window, 'slider_confocal_channel' + str(y) + '_slice').value())
                self.display.ConfocalDataAll.setIndex(y, getattr(self.main_window, 'slider_confocal_channel' + str(y) + '_slice').value())
            self.display.ShowAllChonfocalChannels()
            Z_Slices = ""
            for i in range(self.current_confocal_image.metaData['ChannelNum']):
                    Z_Slices += str(self.current_confocal_image.index[i]+1) + ', '
                    self.set_channel_bottom_settings('confocal', i, 'i',
                        '[All channels] ' +
                        'Pixel size: ' + str(self.display.ConfocalMetaData['SizeX']) +' | '+
                        'Z slices: ' + Z_Slices)

    def unload_storm_image(self, image):
        if image:
            # TODO: destroy image obj
            self.current_storm_image = None
            self.reset_all_channels_bottom_settings('storm')
            # self.display.ClearPlot()
            self.main_window.storm_settings.clear_rois()
            #avoid recursion
            if  self.display.StormData != []:
                self.display.DeleteStormData()


    def unload_confocal_image(self, image):
        if image:
            # TODO: destroy image obj
            #DeleteConfocalData
            self.current_confocal_image = None
            self.reset_all_channels_bottom_settings('confocal')
            # self.display.ClearPlot()
            if  self.display.ConfocalData != []:
                self.display.DeleteConfocalData()

    def add_roi(self, shape, new_roi=None):
        if shape == 'ellipse':
            roi = self.display.addEllipseROI('ellipse')
            num = str(self.main_window.storm_settings.get_roi_counter())
            ellipse_roi = EllipseRoi('ellipseROI_' + num)
            ellipse_roi.roi = roi
            self.main_window.storm_settings.add_roi(ellipse_roi)
        elif shape == 'circle':
            roi = self.display.addEllipseROI('circle')
            num = str(self.main_window.storm_settings.get_roi_counter())
            circle_roi = CircleRoi('circleROI_' + num)
            circle_roi.roi = roi
            self.main_window.storm_settings.add_roi(circle_roi)
        elif shape == 'freehand':
            self.display.ChangePanMode('Roi')
        elif shape == 'active_contour':
            roi = self.display.createActiveContourROI(new_roi)
            num = str(self.main_window.storm_settings.get_roi_counter())
            active_contour_roi = ActiveContourRoi('activeContourROI_' + num)
            active_contour_roi.roi = roi
            self.main_window.storm_settings.add_roi(active_contour_roi)

    def remove_roi(self, roi):
        if type(roi).__name__ == 'EllipseRoi' or type(roi).__name__ == 'CircleRoi':
            self.display.deleteEllipseROI(roi.roi)
        elif type(roi).__name__ == 'FreehandRoi':
            self.display.deleteFreehandROI(roi)
        elif type(roi).__name__ == 'ActiveContourRoi':
            self.display.deleteActiveContourROI(roi.roi)
        self.main_window.storm_settings.remove_roi(self.main_window.storm_roi_list.currentRow())

    def change_drag_mode(self, checked, mode):
        if checked:
            if mode == 1:
                self.display.ChangePanMode('Drag')
            if mode == 2:
                self.display.ChangePanMode('Reg')
            if mode == 3:
                self.display.ChangePanMode('Roi')
        else:
            self.display.ChangePanMode("Pan")

    def set_view_mode(self, mode):
        pass

    def show_scale(self, mode):
        self.display.QWindow.set_scale(mode)
        self.display.QWindow.update()
