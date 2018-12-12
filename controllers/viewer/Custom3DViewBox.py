__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Sebastian Reinhard'

import os

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import cv2
from OpenGL.GL import *
from scipy import stats

from impro.visualisation.Render import points,raycast,image,roi,alpha_complex

## make a widget for displaying 3D objects

class Display(gl.GLViewWidget):
    """3D display Add On for VividSTORM."""
    def __init__(self, main_window, *args, **kwds):
        """
        Initialisation of basic display attributes
        ================================================
        *Attributes*
        ------------------------------------------------
        Active Marker STORM/SIM: Two GL lines adding up to a cross.
        Color Table: Table of the colors used for the markers.
        Image: Placeholder for a GL image in the X;Y plane.
        Storm: Placeholder for a scatter plot with STORM data.
        Click Mode: Basic image modes: Reg for setting markers;
                                       Drag for dragging the SIM image;
                                       Pan for rotation and view.
        Marker World Position: Position of the markers in world space.
                               Used to calculate image offset.
        Image Offset: Offset of SIM image in nm.
        Offset: Offset of both images to world zero.
        ------------------------------------------------
        """
        gl.GLViewWidget.__init__(self, *args, **kwds)
        self.main_window = main_window
        #Initialize variables
        self.mousePos = pg.QtCore.QPoint()
        self.clickMode = 'FreehandRoi'
        self.markerSize= 50
        self.showScale = True
        self.scaleMode = "world"
        self.testCluster = {}
        self.opts['slices'] = [0,0]
        self.roi = roi(filename=r"\Roi")
        self.freeHandpointlist = []
        self._roiStart = None
        self._roiEnd = None
        self.roiData = {'locdSTORM':None,'imagedSTORM':None,'imageSIM':None}
        self.point =0
        self.addItem(self.roi)
        self._twoDim = True
        self.__initRGBAColors__()
        self.__initScale__()
        self.__initStorm__()
        self.__initSim__()

    #inits
    def __initRGBAColors__(self):
        """Define Colors for Markers"""
        self.colorTable = np.array([[
        255,64,64,255], [210,105,30,255], [238,180,180,255], [139,90,43,255], [151,255,255,255], [47,79,79,255], [0,100,0,255], [189,183,107,255], [255,140,0,255], [255,20,147,255]],dtype=int)

    def __initScale__(self):
        """Rework Scale"""
        numbersToShow = 10
        #self.scale = Scale(filename = os.getcwd()+ r"\resources\Shader\Scale")
        #self.addItem(self.scale)
        #self.scale.setVisible(True)
        self.xgrid = gl.GLGridItem(size=pg.QtGui.QVector3D(2000,1,1))
        self.ygrid = gl.GLGridItem(size=pg.QtGui.QVector3D(1,2000,1))
        #self.addItem(self.xgrid)
        #self.addItem(self.ygrid)
        self.xgrid.scale(10, 10, 1.2)
        self.ygrid.scale(10, 10, 1.2)
        self.customScale = {"Position":pg.QtGui.QVector3D(0,0,0),"Length":0,'Width':0,'Line':gl.GLLinePlotItem(),'Show':False}
        self.addItem(self.customScale["Line"])

    def __initStorm__(self):
        """
        Create list of dstorm objects for multi selection
        Create instance of customMarkers in STORM mode
        """
        self.storm = []
        for i in range(4):
            self.storm.append(points(filename = r"\STORM2"))
            self.storm[i].setVisible(False)
            self.addItem(self.storm[i])
        self.alpha_complex = alpha_complex(filename = r"\Alpha")
        self.alpha_complex.setVisible(False)
        self.addItem(self.alpha_complex)
        self.stormMarker = CustomMarker("STORM", antialias=True)
        self.stormMarker.setVisible(False)
        self.addItem(self.stormMarker)

    def __initSim__(self):
        """
        Create Image item for texture display
        Create customMarkers in SIM mode
        """
        self.z_stack = 0
        self.z_offset = 0
        self.metaData = {"SizeX":0,"SizeY":0,"SizeZ":0}
        self.sim = image(data=None, smooth=False, filename=r"\image")
        self.sim3D = raycast(filename=r"\image")
        self.sim.setVisible(False)
        self.sim3D.setVisible(False)
        self.simMarker = CustomMarker("SIM", antialias=True)
        self.simMarker.setVisible(False)
        self.addItem(self.sim)
        self.addItem(self.sim3D)
        self.addItem(self.simMarker)
        self.imageOffset = pg.QtGui.QVector2D()

    def set_sim_position(self, position):
        sim_size = np.array((self.sim.data[0].shape[-1],self.sim.data[0].shape[-2]))*self.metaData["SizeX"]*1000
        print(self.storm[0].position[:,1].max())
        new_offset = -position[1]-sim_size[0]+self.storm[0].position[:,1].max(),position[0]
        self.sim.translate(-self.imageOffset.x()+new_offset[0], -self.imageOffset.y()+new_offset[1],0)
        self.sim3D.translate(-self.imageOffset.x()+new_offset[0], -self.imageOffset.y()+new_offset[1],0)
        self.imageOffset.setX(new_offset[0])
        self.imageOffset.setY(new_offset[1])


    def set_dstorm_image(self, data, Lut, color, channel):
        colorfloat = list([c/255 for c in color])
        colorfloat[3] = 1.0
        maxemission = data[...,4].max()*Lut
        size = self.main_window.spinBox_storm_config_dot_size.value()
        if data.shape[0] != len(self.testCluster):
            self.testCluster = np.zeros(data.shape[0])
        self.storm[channel].set_data(position=data, size=float(size), color=colorfloat, maxEmission=maxemission, cluster=self.testCluster)
        self.storm[channel].setVisible(True)

    def set_alpha_shape(self, points, alpha, show):
        if show:
            self.alpha_complex.set_data(position=points[...,0:2], simplices=points[...,2:5], alpha=130.0, size=float(20))
            self.alpha_complex.setVisible(True)
        else:
            self.alpha_complex.setVisible(False)


    def set_dstorm_dimension(self, dim):
        if dim == "3D":
            self.main_window.viewer.display.ShowAllStormChannels()
        elif dim == "2D":
            self.storm[0].position[...,3] = 0
            self.storm[0].updateData = True
            self.storm[0].update()

    def set_marker(self, STORM, SIM):
        SimMarkers = self.transformPixelToWorld(SIM)
        StormMarkers = self.transformPixelToWorld(STORM)
        self.simMarker.centerPos = SimMarkers
        if len(self.simMarker.centerPos) == 0:
            self.simMarker.setVisible(False)
        else:
            self.simMarker.setVisible(True)
        self.simMarker.set_data(pos=None, color=self.colorTable, width=self.markerSize)
        self.stormMarker.centerPos = StormMarkers
        if len(self.stormMarker.centerPos) == 0:
            self.stormMarker.setVisible(False)
        else:
            self.stormMarker.setVisible(True)
        self.stormMarker.set_data(pos=None, color=self.colorTable, width=self.markerSize)
        self.main_window.viewer.push_markers_to_dialoge()

    def set_scale(self, mode):
        self.scaleMode = mode

    def set_scale_custom(self, pos, length, width):
        if not self.customScale["Show"]:
            if length > 0 and width >0:
                self.customScale["Show"] = True
                self.customScale["Position"] = pos
                self.customScale["Length"] = length
                self.customScale["Width"] = width
                pox = np.array([[pos.x()-length/2, pos.y(), pos.z()],
                                [pos.x()+length/2, pos.y(), pos.z()]])
                self.customScale["Line"].setData(width=width, pos=pox)
                self.customScale["Line"].setVisible(True)
                self.update()
            else:
                print("length and width not valid")
        else:
            self.customScale["Line"].setVisible(False)
            self.customScale["Show"] = False
            self.update()

    def set_sim_image(self, image, chNumb, pxSize, lut, mininterpolation=True, maginterpolation=True, update= True):
        #only works if ch0 is visible fix!
        if image != None and len(chNumb) != 0:
            self.metaData = pxSize
            dat = []
            #self.opts['slices'] = [0,image.data.shape[1]]
            for i in range(image.data.shape[0]):
                #print glGetIntegerv(GL_MAX_3D_TEXTURE_SIZE)
                if self._twoDim:
                    data = image.data[i][image.index[i]].astype(np.float32)#[1000:2400,200:1600]
                else:

                    data = image.data[i].astype(np.float32)
                data *= 255*5/(data.max())
                np.clip(data,0,255,out=data)
                data = np.take(lut[i], data.astype(np.int32))
                dat.append(data)
            if self._twoDim:
                self.sim.set_data(dat, image.color, chNumb,
                                  flip_ud=image.flip["UpsideDown"], flip_lr=image.flip["LeftRight"])
                self.sim.update()
                self.sim.setVisible(True)
                if not self.sim.scaled:
                     self.sim.scale(pxSize['SizeX']*data.shape[0]*1000,
                                    pxSize['SizeY']*data.shape[1]*1000,0 )
                     self.opts["distance"] = 100000
                     self.sim.scaled = True
            else:

                # TODO:normalized rect for slicing
                #if self.opts['roi'] == True:
                #    [color[self.opts['slices'][0]:self.opts['slices'][1]] for color in dat]
                #if self.opts['roi']== True:
                    #y = []
                    #for i in dat:
                        #y.append([[stack[self.coords_roi_sim.x():self.coords_roi_sim.x()+self.coords_roi_sim.width(),
                                   #self.coords_roi_sim.y():self.coords_roi_sim.y()+self.coords_roi_sim.height()] for stack in i]])
                        #dat = np.array(y)
                dat = [color[self.opts['slices'][0]:self.opts['slices'][1]] for color in dat]
                self.sim3D.set_data(np.array(dat), image.color, chNumb,
                                  flip_ud=image.flip["UpsideDown"], flip_lr=image.flip["LeftRight"])
                self.sim3D.update()
                self.sim3D.setVisible(True)
                y = self.sim3D.viewTransform()
                z = y.column(2)
                z.setZ(pxSize['SizeZ']*1000*self.sim3D.data.shape[1]/2)
                y.setColumn(2,z)
                self.sim3D.setTransform(y)
                if not self.sim3D.scaled:
                    self.sim3D.scale(
                        pxSize['SizeX']*self.sim3D.data.shape[2]/2*1000,
                        pxSize['SizeY']*self.sim3D.data.shape[3]/2*1000, 1,)
                    self.sim3D.translate(
                        pxSize['SizeX']*1000*self.sim3D.data.shape[2]/2,
                        pxSize['SizeY']*1000*self.sim3D.data.shape[3]/2,
                        0)
                    self.sim3D.scaled = True
            if self.clickMode == "Roi":
                try:
                    storm, sim = self.get_roi_images(self.roi.rect, 1)
                    self.main_window.dialog_tool_roi.add_images(storm, sim) #np.rot90(sim,3))
                except:
                    print("Draw roi first or change mode")
        else:
            self.sim.setVisible(False)

    def set_sim_interpolation(self, min, mag):
        self.sim.mag = mag
        self.sim.min = min

    def set_sim_dimension(self, dim):
        if dim == "3D":
            self._twoDim = False
            self.sim.setVisible(False)
            self.main_window.viewer.display.ShowAllChonfocalChannels()
        elif dim == "2D":
            self.sim3D.setVisible(False)
            self._twoDim = True
            self.main_window.viewer.display.ShowAllChonfocalChannels()

    def set_opts(self, opts):
        self.opts = opts
        self.update()

    def set_z_stack_offset(self, value):
        if self.metaData is not None:
            z_position = value*self.metaData["SizeZ"]*1000
            self.z_stack = z_position
            self._update_z()

    def set_z_offset(self, value):
        self.z_offset = value
        self._update_z()

    def get_alpha_shape(self):
        size = self.metaData["SizeX"]
        print(self.storm[0].position[:,0].max()/(size*1000), self.storm[0].position[:,1].max()/(size*1000))
        if self.alpha_complex.visible():
            self.alpha_complex.background_render(pg.QtCore.QPoint(self.storm[0].position[:,0].max()/(size*1000), self.storm[0].position[:,1].max()/(size*1000)),1.0)
        else:
            print("create alpha shape first")
        return self.alpha_complex.image

    def get_marker(self):
        #Position to total Zero
        SimMarkers = [self.transformWorldToPixel(i.toVector2D()-self._get_offset("dSTORM")) for i in self.simMarker.centerPos]
        StormMarkers = [self.transformWorldToPixel(i.toVector2D()-self._get_offset("dSTORM")) for i in self.stormMarker.centerPos]
        return SimMarkers, StormMarkers, self.colorTable

    def get_opts(self):
        return self.opts

    def get_roi_images(self, rect, ratio):
        storm_max = pg.QtGui.QVector2D(self.storm[0].position[:,0].max(), self.storm[0].position[:,1].max())
        storm_size = self.transformSimTodStorm(storm_max).toPoint()

        rect_roi_sim = self.transformWorldToPixel(rect)
        rect_roi_dstorm = rect_roi_sim.translated(self.transformSimTodStorm(-self._get_offset("dSTORM")).toPoint())

        #self.sim.getImage(rect_roi_sim, ratio)
        self.storm[0].background_render(storm_size, ratio, (rect_roi_dstorm.x(),rect_roi_dstorm.y(),rect_roi_dstorm.width(),rect_roi_dstorm.height()))
        self.alpha_complex.background_render(storm_size, ratio, (rect_roi_dstorm.x(),rect_roi_dstorm.y(),rect_roi_dstorm.width(),rect_roi_dstorm.height()))
        #self.storm[0].getImage(storm_size, rect_roi_dstorm, ratio)

        roi_sim = self.get_roi_sim(rect_roi_sim, self.sim.data[0])
        roi_storm = self.alpha_complex.image#self.storm[0].image

        return roi_storm, roi_sim

    def get_roi_sim(self, roi, sim_data):
        x = list(roi.getCoords())
        y = [0,0,0,0]
        if x[1] < 0:
            y[1] = x[1]
            x[1] = 0
        if x[0] < 0:
            y[0] = x[0]
            x[0] = 0
        if x[2]>sim_data.shape[1]:
            y[2] = x[2]-sim_data.shape[1]+1
            x[2] = sim_data.shape[1]-1
        if x[3]>sim_data.shape[0]:
            y[3] = x[3]-sim_data.shape[0]+1
            x[3] = sim_data.shape[0]-1
        data = np.zeros((roi.height(), roi.width()))
        sim = np.flipud(sim_data)
        if self.sim.flip_ud and not self.sim.flip_lr:
             sim = np.flipud(sim)
        if self.sim.flip_lr and not self.sim.flip_ud:
            sim = np.fliplr(sim)
        if self.sim.flip_lr and self.sim.flip_ud:
            sim = np.fliplr(np.flipud(sim))
        #srsly fucked up mapping
        roi = roi.intersected(pg.QtCore.QRect(0,0,sim.shape[0],sim.shape[1]))
        relevant_data = sim[roi.y():roi.y()+roi.height(),
                            roi.x():roi.x()+roi.width()]
        relevant_data = np.flipud(relevant_data)
        relevant_data = np.rot90(relevant_data,2)
        data[-y[1]:data.shape[0]-y[3],y[2]:data.shape[1]+y[0]]= relevant_data
        return data

    def get_screenshot(self):
        return self.readQImage()
    #Resetting
    def reset_view(self):
        """Reset View."""
        self.opts['distance'] = 200
        self.opts['elevation'] = 90
        self.opts['fov'] = 60
        self.opts['azimuth'] = 90
        self.update()

    def delete_marker(self, index, channel):
        """Delete specific marker."""
        if channel == "Storm":
            del self.stormMarker.centerPos[index]
            self.stormMarker.set_data(pos=None, color=self.colorTable, size=self.markerSize, pxMode=False,)
        elif channel == "SIM":
            del self.simMarker.centerPos[index]
            self.simMarker.set_data(pos=None, color=self.colorTable, size=self.markerSize, pxMode=False,)

    def delete_roi(self):
        self._roiStart = None
        self._roiEnd = None
        self.testCluster[:] = 0
        self.storm[0].set_data(cluster=self.testCluster)
        self.storm[0].update()
        self.roi.setVisible(False)
    #Events

    def mouseMoveEvent(self, ev):
        """Drag event converts mouse position to world space. Z axis is set to zero."""
        diff = self.transformClipToWorld(ev.pos()) - self.transformClipToWorld(self.mousePos)
        if self.clickMode == 'Drag':
            if ev.buttons() == pg.QtCore.Qt.LeftButton:
                self.sim.translate(diff.x(), diff.y(), 0)
                self.sim3D.translate(diff.x(), diff.y(), 0)
                self.imageOffset += diff.toVector2D()
                self.mousePos = ev.pos()

        elif self.clickMode == 'Pan' or self.clickMode == 'Reg':
            if ev.buttons() == pg.QtCore.Qt.RightButton and pg.QtGui.QApplication.keyboardModifiers() == pg.QtCore.Qt.ControlModifier:
                self.translate_single_marker(diff)
            elif ev.buttons() == pg.QtCore.Qt.RightButton:
                #self.viewMatrix.translate(diff.x(),diff.y(),0)
                self.opts["center"] -= diff.toVector3D()#pg.QtGui.QVector3D(diff.x(),diff.y(),0)
                self.update()
                #self.sim.translate(diff.x(), diff.y(), 0)
                #self.sim3D.translate(diff.x(), diff.y(), 0)
                #translate storm
                #[item.translate(diff.x(), diff.y(), 0) for item in self.storm]
                #self.alpha_complex.translate(diff.x(), diff.y(), 0)
                #self.stormMarker.translate(diff.x(), diff.y(),0)
                #self.simMarker.translate(diff.x(), diff.y(),0)
            self.main_window.viewer.push_markers_to_dialoge()
            gl.GLViewWidget.mouseMoveEvent(self, ev)

        elif self.clickMode == 'Roi':
            if ev.buttons() == pg.QtCore.Qt.LeftButton:
                start = self._roiStart
                end = self.transformClipToWorld(ev.pos())
                self.roi.set_data(start=start, end=end)
                self.roi.update()
                self.roi.setVisible(True)

        elif self.clickMode == 'FreehandRoi':
            if ev.buttons() == pg.QtCore.Qt.LeftButton:
                # until hit start pos
                newpoint = self.transformWorldToPixel(self.transformClipToWorld(ev.pos()).toVector2D()).toPoint()
                if newpoint != self.point:
                    self.point = newpoint
                    if self.point in self.freeHandpointlist:
                        print("finish")
                    self.freeHandpointlist.append(self.point)
                self.mousePos = ev.pos()

    def mouseDoubleClickEvent(self, ev):
        """Set markers to mouse position in world space.
        ===============================================
        Left button = STORM marker
        Right button = SIM marker
        ===============================================
        """
        gl.GLViewWidget.mouseDoubleClickEvent(self, ev)
        if self.clickMode == 'Reg':
            QMarkerWorld = self.transformClipToWorld(self.mousePos)
            if ev.buttons() == pg.QtCore.Qt.LeftButton:
                self.stormMarker.set_data(pos=QMarkerWorld, color=self.colorTable, width=self.markerSize)
                self.stormMarker.setVisible(True)

            if ev.buttons() == pg.QtCore.Qt.RightButton:
                self.simMarker.set_data(pos=QMarkerWorld, color=self.colorTable, width=self.markerSize)
                self.simMarker.setVisible(True)
            self.main_window.viewer.push_markers_to_dialoge()

        #elif self.clickMode == 'Pan':
            #pos = self.transformClipToWorld(self.viewMatrix(), self.projectionMatrix(), self.mousePos)
            #pos = pos.toVector2D() - self.offset
            #indices, clusternumber = filters.customShit(self.storm[0].position[...,0:3], np.array([pos.x(),pos.y(),0]))
            #test
            #for i, j in enumerate(indices):
            #    self.testCluster[j] = clusternumber[i]
            #self.storm[0].set_data(cluster=self.testCluster)

    def mousePressEvent(self, ev):
        gl.GLViewWidget.mousePressEvent(self,ev)
        if self.clickMode == 'Roi':
            if ev.buttons() == pg.QtCore.Qt.LeftButton:
                self._roiStart = self.transformClipToWorld(ev.pos()).toVector2D()

    def mouseReleaseEvent(self, ev):
        gl.GLViewWidget.mouseReleaseEvent(self,ev)
        if self.clickMode == 'Roi':
            if ev.button() == pg.QtCore.Qt.LeftButton:
                self._roiEnd = self.transformClipToWorld(ev.pos()).toVector2D()
                loc_dstorm = self.paint_roi(self.roi.rect)
                render_size = self.main_window.dialog_export_roi.render_px_size.value()
                ratio = self.metaData["SizeX"]/render_size
                storm, sim = self.get_roi_images(self.roi.rect, ratio)
                self.roiData["locdSTORM"] = loc_dstorm
                self.roiData["imagedSTORM"] = np.asarray(storm)
                self.roiData["imageSIM"] = sim#np.rot90(sim,3)
                self.main_window.dialog_tool_roi.add_images(self.roiData["imagedSTORM"], self.roiData["imageSIM"])
                self.main_window.dialog_export_roi.add_images(self.roiData["locdSTORM"],
                                                              self.roiData["imagedSTORM"], self.roiData["imageSIM"])
        if self.clickMode == 'FreehandRoi':
            self.free_hand_roi()

    def paint_roi(self, bounds):
        rect = bounds.translated(-self._get_offset("complete").toPoint())
        self.testCluster[:]=0
        if self.storm[0] != None:
            indices=[]
            for j, point in enumerate(self.storm[0].position):
                if rect.contains(point[0],point[1]):
                #if Mapping.contains_point(point, rect):
                    indices.append(j)
            self.testCluster[indices] = 1.0
            loc_roi = self.storm[0].position[indices]
            #TransformLocFile.saveLocFile(os.getcwd() + r"\temp\dSTORMRoi_temp.txt", relevantPositions)
            self.storm[0].set_data(cluster=self.testCluster)
            self.storm[0].update()
            return loc_roi

    def paint_scale_text(self):
        """
        Textures for scale
        """
        glColor3f(1.0,1.0,1.0)
        font = pg.QtGui.QFont("Arial", 12, pg.QtGui.QFont.Bold, False)
        dist = round(self.opts['distance'],-2)
        x= 21
        if (self.sim.visible() or self.sim3D.visible()) and self.scaleMode == "pixel":
            for i in range(x):
                y= i-x/2
                value = Mapping.round_two_digits(y * dist / 5)
                string = str(int(value/(self.metaData["SizeX"]*1000)))+"px"
                self.renderText(value,0,0,string,font)
                self.renderText(0,value,0,string,font)
        elif self.scaleMode == "world":
            for i in range(x):
                y= i-x/2
                value = Mapping.round_two_digits(y * dist / 5)
                string = str(value)+"nm"
                self.renderText(value,0,0,string,font)
                self.renderText(0,value,0,string,font)

    def paintGL(self, *args, **kwds):
        gl.GLViewWidget.paintGL(self, *args, **kwds)
        self.main_window.viewer.push_view_to_dialog()
        if self.scaleMode != "noscale":
            self.paint_scale_text()
        if self.customScale["Show"]:
            self.renderText(self.customScale["Position"].x(),
                            self.customScale["Position"].y()-self.customScale["Width"]/2,
                            self.customScale["Position"].z(),
                            str(self.customScale["Length"]) + " nm",
                            pg.QtGui.QFont("Arial", 12, pg.QtGui.QFont.Bold, False))

    #Functions
    def save_current_overlay(self, path=None):
        height = self.storm[0].position[...,0].max()
        width = self.storm[0].position[...,1].max()
        rect = pg.QtCore.QRect(self._get_offset("complete").toPoint(), (self._get_offset("complete")+pg.QtGui.QVector2D(height, width)).toPoint())
        storm, sim = self.get_roi_images(rect, 1)
        #simI = PilImage.fromarray(sim.astype(np.uint8))
        if path is not None:
            cv2.imwrite(path + r"\dSTORM_temp.png", storm )
            cv2.imwrite(path + r"\SIM_temp.png", sim)
        else:
            cv2.imwrite(os.getcwd() + r"\temp\dSTORM_temp.png", np.array(storm))
            cv2.imwrite(os.getcwd() + r"\temp\SIM_temp.png", sim)

    def translate_single_marker(self, diff):
        for i, center in enumerate(self.stormMarker.centerPos):
            vec4_dist = self.transformClipToWorld(self.mousePos) - center#.toVector4D()
            if np.sqrt(vec4_dist.lengthSquared()) < 30:
                self.stormMarker.translate(diff.x(), diff.y(), 0, index=i)
        for i, center in enumerate(self.simMarker.centerPos):
            vec4_dist = self.transformClipToWorld(self.mousePos) - center#.toVector4D()
            if np.sqrt(vec4_dist.lengthSquared()) < 30:
                self.simMarker.translate(diff.x(), diff.y(), 0, index=i)

    def transformClipToWorld(self, position):
        return Mapping.transformClipToWorld(self.viewMatrix(), self.projectionMatrix(), position, self.size().width(), self.size().height())

    def transformWorldToPixel(self, position):
        total_offset = self._get_offset("SIM")
        return Mapping.transformWorldToPixel(total_offset, position, self.metaData["SizeX"] * 1000)

    def transformPixelToWorld(self, positions):
        total_offset = self._get_offset("complete")
        return [Mapping.transformPixelToWorld(total_offset.toVector3D(), i.toVector3D(), self.metaData["SizeX"] * 1000)
                for i in positions]

    #rename
    def transformSimTodStorm(self, position):
        return (position)/(self.metaData["SizeX"]*1000)

    def analyse_correlation_test(self, dStorm, SIM):  # roi
        a = dStorm.astype(np.uint8)[..., 0:2].sum(2)
        b = SIM.astype(np.uint8)
        corr = stats.pearsonr(b.flatten(), a.flatten())
        print(corr)
        self.main_window.dialog_tool_roi.set_bottom_text("Correlation SIM0, dSTORM0: " + str(corr[0]))

    def free_hand_roi(self):
        mask = np.zeros(self.sim.data[0][0].shape)
        x = self.sim.data[0]
        for i in self.freeHandpointlist:
            for j in self.freeHandpointlist:
                if i.x() == j.x():
                    x[i.x(),i.y():j.y()]=0
        self.sim.data[0] = x
        self.sim._needUpdate = True
        #track mouse till connect
        #create mask
        #cut mask

    def _update_z(self):
        transform_sim = self.sim.viewTransform()
        vec4_zcomp = transform_sim.row(2)
        vec4_zcomp.setW(self.z_stack+self.z_offset)
        transform_sim.setRow(2, vec4_zcomp)
        self.sim.setTransform(transform_sim)

        if self.sim3D.scaled:
            transform_sim = self.sim3D.viewTransform()
            vec4_zcomp = transform_sim.row(2)
            vec4_zcomp.setW(self.metaData['SizeZ']*1000*self.sim3D.data.shape[1]/2+self.opts['slices'][0]*self.metaData["SizeZ"]*1000+self.z_offset)
            transform_sim.setRow(2, vec4_zcomp)
            self.sim3D.setTransform(transform_sim)

    def _get_offset(self, mode):
        sim_offset = pg.QtGui.QVector2D(self.sim.viewTransform().toTransform().dx(),
                                        self.sim.viewTransform().toTransform().dy())
        complete_offset = pg.QtGui.QVector2D(self.storm[0].viewTransform().toTransform().dx(),
                                             self.storm[0].viewTransform().toTransform().dy())
        storm_offset = complete_offset-sim_offset
        if mode == "SIM":
            return sim_offset
        elif mode == "dSTORM":
            return storm_offset
        elif mode == "complete":
            return complete_offset

class Mapping():
    @staticmethod
    def transformClipToWorld(view, projection, position, width, height):
            """Creates a QVector4D in world position with incoming QPoint.
            Read http://trac.bookofhook.com/bookofhook/trac.cgi/wiki/MousePicking for detailed explanation"""
            #Get camera Position in real space.
            camera_position_clip = pg.QtGui.QVector4D(0,0,0,1)
            #Screen coordinates on orthogonal view in pixel (0,0)= top left.
            #Z and W value for point out of camera plane.
            z = 1.0
            w = 1.0
            #Normalize screen coordinates. (0,0) is the center. Right upper corner is (1 ,1).
            QMousePos = pg.QtGui.QVector2D(position)
            scale = pg.QtGui.QVector2D(2.0/width, -2.0/height)
            transform = pg.QtGui.QVector2D(-1,1)
            #Wrap point in QVector4D 4th component is either 0 for vector or 1 for point.
            QPointClip = pg.QtGui.QVector4D((QMousePos*scale+transform), z, w)

            #Wrap matrices in QMatrix 4x4.
            QProjectionMatrix = projection#pg.QtGui.QMatrix4x4(np.reshape(projectionMatrix,[16]))
            QModelviewMatrix = view#pg.QtGui.QMatrix4x4(np.reshape(modelviewMatrix,[16]))

            #Invert matrices.
            QProjectionMatrixInverse = QProjectionMatrix.inverted()
            QModelviewMatrixInverse = QModelviewMatrix.inverted()

            #Check invertible and transform point from camera to world space.
            if QProjectionMatrixInverse[1] and QModelviewMatrixInverse[1] == True:
                QPointView = QProjectionMatrixInverse[0]*QPointClip
                cameraPositionView = QProjectionMatrixInverse[0]*camera_position_clip
                #Normalize.
                QPointViewNormalized = QPointView/QPointView.w()
                cameraPositionNormalized = cameraPositionView/cameraPositionView.w()

                QPointWorld = QModelviewMatrixInverse[0]*QPointViewNormalized
                cameraPosition = QModelviewMatrixInverse[0]*cameraPositionNormalized
            else:
                print("Error in matrix inversion")
            #Get intersection with x axis.
            QPointWorld = cameraPosition-cameraPosition.z()/(
                cameraPosition.z()-QPointWorld.z())*(cameraPosition-QPointWorld)

            return QPointWorld

    @staticmethod
    def transformWorldToPixel(offset, position, px_size):
        if isinstance(position, pg.QtGui.QVector2D):
            return (position - offset) / px_size
        if isinstance(position, pg.QtCore.QRect):
            coords = position.topLeft()/px_size
            size = position.size()/px_size
            new = pg.QtCore.QRect(coords,size)
            new.translate(-offset.toPoint() / px_size)
            return new
        if isinstance(position, pg.QtCore.QPoint):
            return (position - offset.toPoint()) / px_size

    @staticmethod
    def transformPixelToWorld(offset, position, px_size):
        """
        px postion
        world offset
        """
        return position * px_size + offset

    @staticmethod
    def contains_point(point, rect):
        if point[0]>rect.x()and point[0]<rect.x()+rect.width() \
                and point[1] > rect.y() and point[1]<rect.y()+rect.height():
            return True

    @staticmethod
    def round_two_digits(number):
        x = len(str(abs(int(number))))
        y = round(number,-(x-2))
        return y


class GlPosition():
    def __init__(self, scale):
        self.clip = 0
        self.world = 0
        self.pixel = 0
        self.scale = scale

    def set_data(self, value, mode, offset, image_offset, scale):
        self.offset = offset
        self.image_offset = image_offset
        if mode == "world":
            self.world = value
            self.pixel = self.transformWorldToPixel(value)
        if mode == "pixel":
            self.pixel = value
            self.world = self.transformPixelToWorld(value)

    def transformWorldToPixel(self, positions, scale):
        return [(i.toVector2D() - self.offset - self.image_offset)/scale for i in positions]

    def transformPixelToWorld(self, positions, scale):
        return [(i + self.offset + self.image_offset).toVector3D()*scale for i in positions]


class CustomMarker(gl.GLLinePlotItem):
    """" """
    def __init__(self, channel,  **kwds ):
        gl.GLLinePlotItem.__init__(self, **kwds)
        self.mode = "lines"
        self.channel = channel
        self.centerPos = []
        self.antialias = True

    def set_data(self, **kwds):
        if "pos" in kwds:
            if kwds["pos"] != None:
                self.centerPos.append(kwds["pos"])
            if "color" in kwds:
                kwds["color"] = kwds["color"].astype(float).repeat(4,axis=0)/255
            if self.channel == "STORM":
                kwds["pos"]= self.makeSTORM(self.centerPos,100)
            if self.channel == "SIM":
                kwds["pos"] = self.makeSIM(self.centerPos,100)
        gl.GLLinePlotItem.setData(self, **kwds)

    def translate(self, dx, dy, dz, index = None, local=False):
        if index != None:
            self.centerPos[index].setX(self.centerPos[index].x()+dx)
            self.centerPos[index].setY(self.centerPos[index].y()+dy)
        else:
            for i in range(len(self.centerPos)):
                self.centerPos[i].setX(self.centerPos[i].x()+dx)
                self.centerPos[i].setY(self.centerPos[i].y()+dy)
        self.set_data(pos=None)

    def makeSIM(self, position, size):
        """Build two lines rotated by 45 degreee for marker"""
        markers = {}
        for i in range(len(position)):
            xLine = np.array([[position[i].x()-size, position[i].y()-size, position[i].z()], [position[i].x()+size, position[i].y()+size, position[i].z()]])
            yLine = np.array([[position[i].x()+size, position[i].y()-size, position[i].z()], [position[i].x()-size, position[i].y()+size, position[i].z()]])
            if i == 0:
                markers = np.vstack([xLine, yLine])
            else:
                markers = np.vstack([markers, xLine, yLine])
        return markers

    def makeSTORM(self, position, size):
        """Build two lines for marker"""
        markers = {}
        for i in range(len(position)):
            xLine = np.array([[position[i].x()-size, position[i].y(), position[i].z()], [position[i].x()+size, position[i].y(), position[i].z()]])
            yLine = np.array([[position[i].x(), position[i].y()-size, position[i].z()], [position[i].x(), position[i].y()+size, position[i].z()]])
            if i == 0:
                markers = np.vstack([xLine, yLine])
            else:
                markers = np.vstack([markers, xLine, yLine])
        return markers
