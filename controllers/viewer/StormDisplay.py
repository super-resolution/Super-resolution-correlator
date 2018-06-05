# -*- coding: utf-8 -*-
"""
VividSTORM imageDisplay
"""

import pyqtgraph as pg


from pyqtgraph.Qt import QtGui


import pyqtgraph.exporters


import numpy as np, datetime


from PyQt5.QtGui import *
import math


from . import StormLUT


from .. import default_config


import scipy.ndimage


import os


from . import ConfocalLUT


import gc


import copy


import sys


import matplotlib.pyplot as plt


from . import Custom3DViewBox








class StormDisplay(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.StormData = []
        self.StormData_filtered = []
        self.StormChannelList = []
        self.ConfocalImage=[]
        self.DisplayedStormChannel = [0, 0, 0, 0]  # this is a pointer to the image
        self.StormChannelVisible = [False, False, False, False]
        self.StormChannelColors = [(), (), (), ()]

        #rename


        self.ConfocalData = []
        self.ConfocalMetaData = {}
        #self.ConfChannelToShow = []

        self.StormLUTTickValues = [[0, 0.5], [0, 0.5], [0, 0.5], [0, 0.5]]
        self.ConfocalLUTTickValues = [[0, 1], [0, 1], [0, 1], [0, 1]]

        self.ConfocalInterpolationMethod = 3  # 0 nearest neighbour 1 bilinear 2 square 3 cubic
        self.DisplayedConfocalChannel = [0, 0, 0, 0]  # this is a pointer to the image
        self.ConfocalChannelVisible = [False, False, False, False]
        self.ConfocalChannelColors = [(), (), (), ()]
        self.ConfocalTransparency = 0.8
        self.StormTransparency = 0.5
        self.StormZColoring = False
        
        self.ConfocalSizeMultiplier = 10.0
        #See init widget
        #self.plot_widget = QWidget()
        self.marker = []
        #self.Viewbox = []

        self.ScaleBar = []
        self.ScaleText = []
        self.ConfocalZNum = 0
        self.NumOfZSlices = 0

        self.ConfocalLUTWidget = []
        self.StormLutImages = [0, 0, 0, 0]
        self.init_widget()

        self.storm_dot_size=[]
        self.ConfocalZ = 0.0

    def ChangePanMode(self, Mode):
        #self.Viewbox.PanMode = Mode
        #x=0
        self.QWindow.clickMode = Mode

    def filter_data(self, data):
        return self.main_window.storm_settings.filter_storm_data(data)

    def AddStormData(self, storm_image):
        self.StormData = storm_image.stormData
        self.StormData_filtered = self.filter_data(self.StormData)
        self.StormChannelList = storm_image.StormChannelList
        #channels= [str(self.main_window.comboBox_storm_filter_ROI_channel.currentText())]
        #if we have roi filter switched on and we have a roi - filter the points
        #if self.main_window.groupBox_storm_filter_ROI.isChecked():
        #    roi = self.main_window.storm_roi_list.currentItem()
        #    if roi:
        #        if type(roi).__name__ == 'EllipseRoi' or type(roi).__name__ == 'CircleRoi':
        #           self.StormData_filtered = self.filterROIPoints(roi.roi,'Circle',channels)
        #        elif type(roi).__name__ == 'FreehandRoi':
        #           self.StormData_filtered = self.filterROIPoints( roi.roi,'Freehand',channels)
        #        elif type(roi).__name__ == 'ActiveContourRoi':
        #            self.StormData_filtered = self.filterROIPoints(roi.roi,'Activecontour',channels)

         

    def SetStormChannelVisible(self, ChannelNumber, Visible):
        self.StormChannelVisible[ChannelNumber] = Visible
        #set the dropdown menu items for visible channels:
        #while self.main_window.comboBox_storm_filter_ROI_channel.count() > 0:
        #    self.main_window.comboBox_storm_filter_ROI_channel.removeItem(0)
        #index=0
        #for V in self.StormChannelVisible:
        #    if V:
        #        self.main_window.comboBox_storm_filter_ROI_channel.addItem(self.StormChannelList[index])
        #    index+=1


        self.ShowAll()



    def SetStormChannelColor(self, ChannelNumber, Color):
        self.StormChannelColors[ChannelNumber] = default_config.channel_colors[Color]
        if self.StormChannelVisible[ChannelNumber]:
            self.ShowAll()

    def SetConfocalChannelVisible(self, ChannelNumber, Visible):
        self.ConfocalChannelVisible[ChannelNumber] = Visible
        self.ShowAll()

    def SetConfocalChannelColor(self, ChannelNumber, Color):
        self.ConfocalChannelColors[ChannelNumber] = default_config.channel_colors[Color]
        if self.ConfocalChannelVisible[ChannelNumber]:
            self.ShowAll()

    def DeleteStormData(self):
        #for StormCh in self.DisplayedStormChannel:
            #if StormCh!=0:
                #self.Viewbox.removeItem(StormCh)
        #for R in self.Viewbox.StormMarkerRois:
                #self.plot_widget.removeItem(R)
        #self.Viewbox.StormMarkerRois = []
        self.StormData = []
        self.StormData_filtered = []
        self.StormChannelList = []
        self.DisplayedStormChannel = [0, 0, 0, 0]
        #try:
        #    self.plot_widget.clear()
        #except:
        #    pass
        self.ShowAll()
        
        
    def ClearAll(self):
        self.plot_widget.clear() 
        self.DisplayedStormChannel = [0, 0, 0, 0]
        self.DisplayedConfocalChannel = [0, 0, 0, 0]

    def ClearPlot(self):
        #clear only the channels,not the ROI or other elements
        for ConfCh in self.DisplayedConfocalChannel:
            if ConfCh!=0:
                #self.Viewbox.removeItem(ConfCh)
                self.QWindow.set_sim_image(None, 0, 0)
        for StormCh in self.DisplayedStormChannel:
            if StormCh!=0:
                self.Viewbox.removeItem(StormCh)
        self.DisplayedStormChannel = [0, 0, 0, 0]
        self.DisplayedConfocalChannel = [0, 0, 0, 0]

    def AddConfocalData(self, confocal_image):
        self.ConfocalSizeMultiplier=10.0
        self.ConfocalDataAll = confocal_image
        self.ConfocalMetaData = copy.deepcopy(confocal_image.metaData)


    def DeleteConfocalData(self):              
        if self.Viewbox != []:
            self.Viewbox.deleteConfocalImage()
            for R in self.Viewbox.ConfMarkerRois:
                self.plot_widget.removeItem(R)
            self.Viewbox.ConfMarkerRois = []            
            self.Viewbox.AffineTransform = []
        for ConfCh in self.DisplayedConfocalChannel:
            if ConfCh!=0:
                self.Viewbox.removeItem(ConfCh)       
        if self.ConfocalImage!=[]:
            self.ConfocalImage.reset_data()
        self.ConfocalMetaData = {}
        self.DisplayedConfocalChannel[:]        
        for a in self.DisplayedConfocalChannel:
            del a
        del self.DisplayedConfocalChannel[:]
        del self.DisplayedConfocalChannel
        self.DisplayedConfocalChannel = [0, 0, 0, 0]
        self.ConfChannelToShow = [] 
        self.ConfocalSizeMultiplier=10.0
        del self.ConfocalData
        self.ConfocalData = []
        self.main_window.viewer.unload_confocal_image(True)  
        try:
            self.plot_widget.clear()
        except:
            pass
        gc.collect()
        gc.collect()
        self.ShowAll()
        
   
    def ShowAll(self):
        self.main_window.status_bar.showMessage('Recalculating image, please wait...')
        self.ClearPlot()
        self.ShowAllStormChannels()
        #self.ShowAllConfocalChannels()
        StormFileName=''
        if self.main_window.viewer.current_storm_image!=None:
                StormFileName=str.split(self.main_window.viewer.current_storm_image.file_path,os.sep)[-1]
        ConfocalFileName='' 
        if self.main_window.viewer.current_confocal_image!=None:  
                ConfocalFileName=str.split(self.main_window.viewer.current_confocal_image.file_path,os.sep)[-1]
        self.main_window.status_bar.showMessage('Ready '+'StormFile:'+StormFileName+' ConfocalFile:'+ConfocalFileName)


    def init_widget(self):
        self.QWindow = Custom3DViewBox.Display(self.main_window)
        self.main_window.viewer_container_layout.addWidget(self.QWindow)
        self.QWindow.reset_view()
        self.QWindow.show()
        #self.QWindow.showScale = True



    def ShowAllChonfocalChannels(self):
        #for ChannelNum in range(self.ConfocalMetaData['ChannelNum']):

        visibleChannels= [i for i, x in enumerate(self.ConfocalChannelVisible) if x]
        self.ConfocalColorLut = []
        for i in range(4):
            pos = np.array([self.ConfocalLUTTickValues[i][0], self.ConfocalLUTTickValues[i][1]])
            map = pg.ColorMap(pos, np.array([[0,0,0,255],[255,0,0,255]]))
            self.ConfocalColorLut.append(map.getLookupTable(0.0, 1.0, 256)[...,0])
        self.ConfocalDataAll.color[...,0:3] = np.asarray(self.ConfocalChannelColors)/255
        #not gamp
        self.QWindow.set_sim_image(self.ConfocalDataAll, visibleChannels, self.ConfocalMetaData, self.ConfocalColorLut)
        self.QWindow.set_z_stack_offset(getattr(self.main_window, 'slider_confocal_channel' + str(0) + '_slice').value())
        self.QWindow.set_z_offset(getattr(self.main_window, 'spinBox_confocal_display_appear_zposition').value())


    def ShowConfocalLut(self, ChannelNumber, ChannelColor):
        #if self.DisplayedConfocalChannel != []:
            #if self.DisplayedConfocalChannel[ChannelNumber] != 0:
                container = self.main_window.dialog_tool_lut.verticalLayout_confocal_lut
                for i in reversed(list(range(container.count()))):
                    container.itemAt(i).widget().setParent(None)

                self.ConfocalLUTWidget = pg.GraphicsWindow()
                self.main_window.dialog_tool_lut.verticalLayout_confocal_lut.addWidget(self.ConfocalLUTWidget)
                LowerSpin=self.main_window.dialog_tool_lut.spinBox_confocal_LUT_lower
                UpperSpin=self.main_window.dialog_tool_lut.spinBox_confocal_LUT_upper
                self.main_window.dialog_tool_lut.spinBox_confocal_LUT_lower.setValue(self.ConfocalLUTTickValues[ChannelNumber][0]*100)
                self.main_window.dialog_tool_lut.spinBox_confocal_LUT_upper.setValue(self.ConfocalLUTTickValues[ChannelNumber][1]*100)
                grad = ConfocalLUT.GradientEditorItem(self, ChannelNumber, LowerSpin, UpperSpin, orientation='top', )
                C0 = ChannelColor[0]
                C1 = ChannelColor[1]
                C2 = ChannelColor[2]
                gradcolors = {'ticks': [(0.0, (0, 0, 0, 255)), (1.0, (C0, C1, C2, 255))], 'mode': 'rgb'}
                grad.restoreState(gradcolors)
                grad.setTickValue(grad.listTicks()[0][0], self.ConfocalLUTTickValues[ChannelNumber][0])
                grad.setTickValue(grad.listTicks()[1][0], self.ConfocalLUTTickValues[ChannelNumber][1])
                grad.updateGradient()
                self.ConfocalLUTWidget.addItem(grad, 0, 0)
                data = self.ConfocalDataAll.data[ChannelNumber][self.ConfocalDataAll.index[ChannelNumber]]
                y,x = np.histogram(255*5*data.flatten().astype("f")/data.max(),bins=np.linspace(0, 255, 200))
                #x = self.DisplayedConfocalChannel[ChannelNumber].getHistogram()
                for d in range(len(y)):
                    if y[d]>0:
                        y[d]=math.log(y[d])
                curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))

                plt1 = self.ConfocalLUTWidget.addPlot(1, 0)
                plt1.addItem(curve)
                plt1.setLogMode(False,True)

                #plt1.setXRange(MinIntensity, MaxIntensity)
                                                  

                


    def setConfocalLUTTickValues(self, ChannelNumber, Values):
        self.ConfocalLUTTickValues[ChannelNumber] = Values
        
    def ShowStormLut(self, ChannelNumber, ChannelColor):
        if self.DisplayedStormChannel != []:
            container = self.main_window.dialog_tool_lut.verticalLayout_storm_lut
            for i in reversed(list(range(container.count()))):
                container.itemAt(i).widget().setParent(None)

            # self.StormLUTWidget = pg.PlotWidget()
            self.StormLUTWidget = pg.GraphicsWindow()
            self.main_window.dialog_tool_lut.verticalLayout_storm_lut.addWidget(self.StormLUTWidget)
            
            LowerSpin=self.main_window.dialog_tool_lut.spinBox_storm_LUT_lower
            UpperSpin=self.main_window.dialog_tool_lut.spinBox_storm_LUT_upper 
            self.main_window.dialog_tool_lut.spinBox_storm_LUT_lower.setValue(self.StormLUTTickValues[ChannelNumber][0]*100)
            self.main_window.dialog_tool_lut.spinBox_storm_LUT_upper.setValue(self.StormLUTTickValues[ChannelNumber][1]*100)    
            grad = StormLUT.GradientEditorItem(self, ChannelNumber,LowerSpin,UpperSpin, orientation='top')
            C0 = ChannelColor[0]
            C1 = ChannelColor[1]
            C2 = ChannelColor[2]
            gradcolors = {'ticks': [(0.0, (0, 0, 0, 255)), (1.0, (C0, C1, C2, 255))], 'mode': 'rgb'}
            grad.restoreState(gradcolors)
            grad.setTickValue(grad.listTicks()[0][0], self.StormLUTTickValues[ChannelNumber][0])
            grad.setTickValue(grad.listTicks()[1][0], self.StormLUTTickValues[ChannelNumber][1])
            grad.updateGradient()
            self.StormLUTWidget.addItem(grad, 0, 0)
            
            Gausses = np.array(self.StormData_filtered[ChannelNumber])
            if self.StormZColoring == True:
                Intensity = Gausses[:, 3]
                Intensity = Intensity - np.amin(Intensity) + 0.1
            else:
                Intensity = Gausses[:, 4]
            MaxIntensity = Intensity.max()
            MinIntensity = np.amin(Intensity)

            y, x = np.histogram(Intensity, bins=np.linspace(MinIntensity, MaxIntensity, 200))
            curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
            plt1 = self.StormLUTWidget.addPlot(1, 0)
            plt1.addItem(curve)
            plt1.setXRange(MinIntensity, MaxIntensity)
            self.UpdateStormChannel(ChannelNumber, self.StormLUTTickValues[ChannelNumber])

    def UpdateConfocalChannel(self, ChannelNum, LutPositions):
        self.ConfocalLUTTickValues[ChannelNum] = LutPositions
        pos = np.array([self.ConfocalLUTTickValues[ChannelNum][0], self.ConfocalLUTTickValues[ChannelNum][1]])
        color = np.array([[0, 0, 0, 255], [self.ConfocalChannelColors[ChannelNum][0],
                                                   self.ConfocalChannelColors[ChannelNum][1],
                                                   self.ConfocalChannelColors[ChannelNum][2], 255]], dtype=np.ubyte)
        #map = pg.ColorMap(pos, color)
        #ColorLut = map.getLookupTable(0.0, 1.0, 256)
                
        #self.DisplayedConfocalChannel[ChannelNum].setLookupTable(ColorLut)
        self.ShowAllChonfocalChannels()
        
        
    def UpdateStormChannel(self, ChannelNumber, LutPositions):
        self.StormLUTTickValues[ChannelNumber] = LutPositions
        Gausses = np.array(self.StormData_filtered[ChannelNumber])
        XCoords = []
        YCoords = []
        DrawTogether=False
        if self.StormZColoring == True:
            Intensity = Gausses[:, 3]
            Intensity = Intensity - np.amin(Intensity) + 0.1
            Intensity = Intensity / np.amax(Intensity)
        else:
            Intensity = Gausses[:, 2]
            if all( Intensity==Intensity[0])or self.main_window.groupBox_storm_config_display.isChecked():
                    DrawTogether=True
            # else:    #
            Intensity = 25.0 / (Gausses[:, 2]**2) #
            #Intensity = Intensity / np.amax(Intensity)
        # Prec = Gausses[:, 2]
        # Prec = Prec / np.amax(Prec)
        # Sigma = 1.0 / (np.sqrt(2 * np.pi) * Prec)

        #Sizes = Sigma * self.storm_dot_size*2.5  # five
        Sizes= Gausses[:, 2]  #
        if not DrawTogether:
            # create an individual pen and brush for every gauss
            ListOfPens = []
            ListOfBrushes = []
            InsertSize = []
            for a in range(len(Gausses)):
                if Intensity[a] > LutPositions[0]:
                    #this could be changed to where-indexing, instead of append
                    XCoords.append(Gausses[a, 0])
                    YCoords.append(Gausses[a, 1])
                    InsertSize.append(Sizes[a])
                    Int = Intensity[a];
                    if Intensity[a] > LutPositions[1]:
                        Int = 1;
                    else:
                        Int = (Int - LutPositions[0]) / (LutPositions[1] - LutPositions[0])
                    Color = (
                        self.StormChannelColors[ChannelNumber][0] * Int, self.StormChannelColors[ChannelNumber][1] * Int,
                        self.StormChannelColors[ChannelNumber][2] * Int, 255 * self.StormTransparency)
                    ListOfPens.append(pg.mkPen(Color))
                    ListOfBrushes.append(pg.mkBrush(Color))
                    #display the channel
            self.DisplayedStormChannel[ChannelNumber].clear()
            # self.DisplayedStormChannel[ChannelNumber] = self.plot_widget.plot(x=XCoords, y=YCoords, pen=None, symbol='o',
            #                                                                   symbolSize=InsertSize, pxMode=False,
            #                                                                   symbolPen=ListOfPens,
            #                                                                   symbolBrush=ListOfBrushes,
            #                                                                   compositionMode=pg.QtGui.QPainter.CompositionMode_Plus,
            #                                                                   opacity=self.StormTransparency)
        else:
                 ListOfPens = []
                 ListOfBrushes = []
                 InsertSize = []
                 XCoords=Gausses[:, 0]
                 YCoords=Gausses[:, 1]
                 InsertSize=self.storm_dot_size # Sizes[0]
                 Int = Intensity[0];
                 if Intensity[0] > LutPositions[1]:
                            Int = 1;
                 else:
                            Int = (Int - LutPositions[0]) / (LutPositions[1] - LutPositions[0])
                 Color = (self.StormChannelColors[ChannelNumber][0] * Int, self.StormChannelColors[ChannelNumber][1] * Int,
                            self.StormChannelColors[ChannelNumber][2] * Int, 255 * self.StormTransparency)
                 #self.DisplayedStormChannel[ChannelNumber].clear()
                 # self.DisplayedStormChannel[ChannelNumber] = self.plot_widget.plot(x=XCoords, y=YCoords, pen=None, symbol='o',
                 #                                                                  symbolSize=InsertSize, pxMode=False,
                 #                                                                  symbolPen=pg.mkPen(Color),
                 #                                                                  symbolBrush=pg.mkBrush(Color),
                 #                                                                  compositionMode=pg.QtGui.QPainter.CompositionMode_Plus,
                 #                                                                  opacity=self.StormTransparency)
        #only give two if no z

        self.QWindow.set_dstorm_image(Gausses, LutPositions[1], Color, ChannelNumber)

    def ShowAllStormChannels(self):
        for ChannelNum in range(len(self.StormChannelList)):
            self.ShowStormChannel(ChannelNum)

    def ShowStormChannel(self, ChannelNumber):
        if self.StormChannelVisible[ChannelNumber] and len(np.array(self.StormData_filtered[ChannelNumber]))>0:
            Gausses = np.array(self.StormData_filtered[ChannelNumber])
            LutPositions=self.StormLUTTickValues[ChannelNumber]
            XCoords = []
            YCoords = []
            DrawTogether=False
            if self.StormZColoring == True:
                # print "Zcoloring"
                Intensity = Gausses[:, 3]
                Intensity = Intensity - np.amin(Intensity) + 0.1
                Intensity = Intensity / np.amax(Intensity)
            else:
                Intensity = Gausses[:, 2]
                if all( Intensity==Intensity[0]) or self.main_window.groupBox_storm_config_display.isChecked():
                    DrawTogether=True
                else:
                    Intensity = 25.0 / (Gausses[:, 2]**2)
            # Prec = Gausses[:, 2]
            # Prec = Prec / np.amax(Prec)
            # Sigma = 1.0 / (np.sqrt(2 * np.pi) * Prec)

            # Sizes = Sigma * self.storm_dot_size *2.5  # five
            Sizes= Gausses[:, 2]
            if not DrawTogether:
                # create an individual pen and brush for every gauss
                ListOfPens = []
                ListOfBrushes = []
                InsertSize = []
                for a in range(len(Gausses)):
                    if Intensity[a] > LutPositions[0]:
                        #this could be changed to where-indexing, instead of append
                        XCoords.append(Gausses[a, 0])
                        YCoords.append(Gausses[a, 1])
                        InsertSize.append(Sizes[a])
                        Int = Intensity[a];
                        if Intensity[a] > LutPositions[1]:
                            Int = 1;
                        else:
                            Int = (Int - LutPositions[0]) / (LutPositions[1] - LutPositions[0])
                        Color = (
                            self.StormChannelColors[ChannelNumber][0] * Int, self.StormChannelColors[ChannelNumber][1] * Int,
                            self.StormChannelColors[ChannelNumber][2] * Int, 255 * self.StormTransparency)
                        ListOfPens.append(pg.mkPen(Color))
                        ListOfBrushes.append(pg.mkBrush(Color))
                        #display the channel

                # self.DisplayedStormChannel[ChannelNumber] = self.plot_widget.plot(x=XCoords, y=YCoords, pen=None, symbol='o',
                #                                                                   symbolSize=InsertSize, pxMode=False,
                #                                                                   symbolPen=ListOfPens,
                #                                                                   symbolBrush=ListOfBrushes,
                #                                                                   compositionMode=pg.QtGui.QPainter.CompositionMode_Plus,
                #                                                                   opacity=self.StormTransparency)

            else:
                 # ListOfPens = []
                 # ListOfBrushes = []
                 # InsertSize = []
                 # XCoords=Gausses[:, 0]
                 # YCoords=Gausses[:, 1]
                 # InsertSize=self.storm_dot_size
                 Int = Intensity[0];
                 if Intensity[0] > LutPositions[1]:
                            Int = 1;
                 else:
                            Int = (Int - LutPositions[0]) / (LutPositions[1] - LutPositions[0])
                 Color = (self.StormChannelColors[ChannelNumber][0] * Int, self.StormChannelColors[ChannelNumber][1] * Int,
                            self.StormChannelColors[ChannelNumber][2] * Int, 255 * self.StormTransparency)
                 # self.DisplayedStormChannel[ChannelNumber] = self.plot_widget.plot(x=XCoords, y=YCoords, pen=None, symbol='o',
                 #                                                                  symbolSize=InsertSize, pxMode=False,
                 #                                                                  symbolPen=pg.mkPen(Color),
                 #                                                                  symbolBrush=pg.mkBrush(Color),
                 #                                                                  compositionMode=pg.QtGui.QPainter.CompositionMode_Plus,
                 #                                                                  opacity=self.StormTransparency)
            self.QWindow.set_dstorm_image(Gausses, LutPositions[1], Color, ChannelNumber)
        else:
            self.QWindow.storm[ChannelNumber].setVisible(False)
                 
