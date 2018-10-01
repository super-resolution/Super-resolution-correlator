# -*- coding: utf-8 -*-
"""
Created on: 2015.01.11.

Author: turbo


"""
import os


from PyQt5.QtWidgets import *
import xml.etree.ElementTree as XMLET


import threading


import numpy as numpy,datetime


from PyQt5.QtGui import *
from scipy import misc


from .ReadSTORM import stormfile


from .TransformLocFile import *


from .viewer import czifile


from .viewer import tifffile

class stormfile(object):
    def __init__(self, input_loc_path):
        self.dataColumn = np.zeros((6))
        self.data = []
        self.size = []
        self.path = input_loc_path

    def readfile(self):
        self.data = pd.read_csv(self.path, skiprows=1, header=None, delim_whitespace=True).as_matrix()

    def clear(self):
        self.data = []
        self.loc_size = []

    def get_header_info(self):
        with open(self.path) as loc:
            self.Header = list(islice(loc, 1))
            headerSplit = self.Header[0].split("/><")
            default_header_args = ["X", "Y", "Precision", "Z", "Emission", "Frame"]
        for j,arg in enumerate(default_header_args):
            for i in range(len(headerSplit)):
                if "semantic" in headerSplit[i]:
                    identifierString = headerSplit[i].split('semantic="')
                    identifier = identifierString[-1].split('"', 1)[0]
                    if arg.lower() in identifier.lower():
                        self.dataColumn[j] = i
                        break
                self.dataColumn[j] = -1
                            # try:
                        #     max_value = headerSplit[i].split('max="')[-1].split('"',1)[0]
                        #     max_value = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", max_value)
                        #     self.dataColumn[arg + " max value"] = float(max_value[0])
                        # except:
                        #     print("no max value" + identifier)



    def save_loc_file(self, path, file):
        x_max = "%.5e" %(file[:,0].max()*10**(-9))
        x_min = 0 #"%.5e" %(loc_input_1[:,0].min()*10**(-9))
        y_max = "%.5e" %(file[:,1].max()*10**(-9))
        y_min = 0 #"%.5e" %(loc_input_1[:,1].min()*10**(-9))
        frame_min = '%u' %file[:2].min()
        header = '<localizations insequence="true" repetitions="variable"><field identifier="Position-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="position in sample space in X" unit="nanometer" min=\"'+str(x_min)+' m\" max=\"'+str(x_max)+' m\" /><field identifier="Position-1-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="position in sample space in Y" unit="nanometer" min=\"'+str(y_min)+' m\" max=\"'+str(y_max)+' m\" /><field identifier="ImageNumber-0-0" syntax="integer" semantic="frame number" unit="frame" min=\"'+str(frame_min)+' fr\" /><field identifier=\"Amplitude-0-0\" syntax=\"floating point with . for decimals and optional scientific e-notation\" semantic=\"emission strength\" unit=\"A/D count\" /><field identifier="FitResidues-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="fit residue chi square value" unit="dimensionless" /><field identifier="Fluorophore-0-0" syntax="integer" semantic="index of fluorophore type" unit="dimensionless" min="0 dimensionless" max="1 dimensionless" /><field identifier="LocalBackground-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="local background" unit="A/D count" /></localizations>'
        np.savetxt(path, file, delimiter=' ', fmt=['%1.1f','%1.1f','%u','%.10g','%.10g','%u','%1.3f'], header= header)


#Super class for file handling via widget
class MicroscopeImage(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super(MicroscopeImage, self).__init__(*args, **kwargs)
        self.setText(args[0].split(os.sep)[-1])
        self.file_path = str(args[0])
        self.isParsingNeeded = True
        # self.channels = {}

#Rewritten class to read STOM/dSTORM data from a text file in a numpy array
#Improved performance and logic
#Can transform the localizations if a matrix is given
#Recives metadata from file header
class StormImage(MicroscopeImage):
    """
    Rewritten class to read STOM/dSTORM data from a text file in a numpy array
    Improved performance and logic
    Can transform the localizations if a matrix is given
    Recives metadata from file header
    """
    def __init__(self, *args, **kwargs):
        super(StormImage, self).__init__(*args, **kwargs)
        self.reset_data()

    def reset_data(self):
        self.stormData = []
        self.StormChannelList = []
        self.roi_list = []
        self.coords_cols = []
        self.other_cols = []
        self.matrix = None

    #Read and prepare STORM data
    def parse(self):
        self.isParsingNeeded = False
        localizations = stormfile(self.file_path)
        localizations.readfile()
        localizations.get_header_info()

        #array = stormfile(self.file_path)
        #array.getHeaderInfo()
        self.stormData = localizations.data

        #prevent negative x,y values. Set to Zero
        self.stormData[...,0] = self.stormData[...,0]-self.stormData[...,0].min()
        self.stormData[...,1] = self.stormData[...,1]-self.stormData[...,1].min()
        self.size = self.stormData[...,0].max(), self.stormData[...,1].max()
        #Build structured array with title name and value of columns.
        storm_reshaped = np.negative(np.ones((self.stormData.shape[0], 6)))
        for i,j in enumerate(localizations.dataColumn):
            if j >=0:
                storm_reshaped[...,int(i)] = self.stormData[..., int(j)]
        #set precision to 10 nm if no value given
        if (storm_reshaped[...,2]<0).all():
            storm_reshaped[...,2] = 10
        self.stormData = np.array([storm_reshaped])

    def transformAffine(self, path=None, src=None, dst=None):
        if path is not None:
            landmarks = pd.read_csv(path, skiprows=1,engine="c", na_filter=False, header=None, delim_whitespace=True, dtype=np.float32).as_matrix()
            dst = landmarks[:,3:5]
            src = landmarks[:,1:3]
        affine = transform.estimate_transform("affine",src,dst)
        data = self.stormData[0][:,0:2]
        data = affine.inverse(data)
        self.stormData[0][:,0:2] = data
        #transformLocalization.saveLocFile(os.path.splitext(self.file_path)[0]+"_temp.txt", x)



#Rewritten class to read different formats of microscope images and bring them in the same shape.
#Supportet formats are .czi; .lsm ;.tiff
#Tiff images will most likely not contain the needed metadata -> Pixel size must be set manually.
#Batch mechanism off Zeiss SIM will result in broken header file and is not supported yet.
#Output arrays will be reshaped to [Color[ZStack[X[Y]]]].
#See MicroscopeImage for input.
class ConfocalImage(MicroscopeImage):
    #Initialisation see class MicroscopeImage.
    def __init__(self, *args, **kwargs):
        super(ConfocalImage, self).__init__(*args, **kwargs)
        self.reset_data()

    #Reset ConfocalImage attributes.
    def reset_data(self):
        self.data = []
        self.relevantData = []
        self.metaData = {}
        self.index = {}
        self.isParsingNeeded = True
        self.extend = None
        self.flip = {}

    #Read the image data and metadata und give them into a numpy array.
    #Rearrange the arrays into a consistent shape.
    def parse(self, calibration_px, main_window, ApplyButton=False):
        self.isParsingNeeded = False
        self.metaData = {}
        self.data = []
        self.Shape = np.ones(1,dtype={'names':["SizeX","SizeY","SizeZ","SizeC"],'formats':['i4','i4','i4','i4']})
        self.extend = os.path.splitext(self.file_path)[1]
        self.color = np.ones((4,4),dtype=np.float32)

        #CZI files
        if self.extend == '.czi':
            with czifile.CziFile(self.file_path) as czi:
                self.data = czi.asarray(memmap=False)
                #Get relevant part of file header => Metadata.
                Header_Metadata = czi.metadata#str(czi.decode("utf-8")).split('<ImageDocument>')
                Metadata = XMLET.fromstring(Header_Metadata)
                try:
                    #Query XML fore the metadata for picture shape(X;Y;Z-stacks).
                    #Picture Shape.
                    shapes = Metadata.findall('./Metadata/Information/Image')[0]
                    self.metaData["ShapeSizeX"] = int(shapes.findall('SizeX')[0].text)
                    self.metaData["ShapeSizeY"] = int(shapes.findall('SizeY')[0].text)
                    self.metaData["ShapeSizeZ"] = int(shapes.findall('SizeZ')[0].text)
                    #Get the hyperstack dimension if the image is a hyperstack.
                    try:
                        self.metaData["ShapeSizeC"] = int(shapes.findall('SizeC')[0].text)
                    except:
                        self.metaData["ShapeSizeC"] = 1
                        print("One Channel")
                    #Get physical pixel size of image(nm/px) convert to(µm/px).
                    PixelSizes = Metadata.findall('./Metadata/Scaling/Items/Distance')
                    self.metaData['SizeX'] = float(PixelSizes[0].findall('Value')[0].text)*10**6
                    self.metaData['SizeY'] = float(PixelSizes[1].findall('Value')[0].text)*10**6
                    self.metaData['SizeZ'] = float(PixelSizes[2].findall('Value')[0].text)*10**6
                except:
                    raise
                    print("Metadata fail")

        #Tiff files.
        #Tiff files are problematic because they most likely wont contain the nessecary metadata.
        #Try to get the shape info over common dimensions.
        elif self.extend == '.tif':
            with tifffile.TiffFile(self.file_path) as tif:
                self.data = tif.asarray(memmap=True)
                for shape in tif.pages[0].shape:
                    if shape <5:
                        self.metaData["ShapeSizeC"] = shape
                    elif shape <40:
                        self.metaData["ShapeSizeZ"] = shape
                    else:
                        self.metaData["ShapeSizeY"] = shape
                        self.metaData["ShapeSizeX"] = shape

        #Read Lsm Files.
        elif self.extend == '.lsm':
            with tifffile.TiffFile(self.file_path) as tif:
                self.data = tif.asarray(memmap=True)
                headerMetadata = str(tif.pages[0].cz_lsm_scan_info)
                metadataList = headerMetadata.split("\n*")
                #Get image shape from lsm header SizeC=0 if not given.
                for shapes in metadataList:
                    if "images_height" in shapes:
                        self.metaData["ShapeSizeX"]= int(shapes.split()[-1])
                    if "images_width" in shapes:
                        self.metaData["ShapeSizeY"]= int(shapes.split()[-1])
                    if "images_number_planes" in shapes:
                        self.metaData["ShapeSizeZ"]= int(shapes.split()[-1])
                    if "images_number_channels" in shapes:
                        self.metaData["ShapeSizeC"]= int(shapes.split()[-1])
                #Get physical pixel size of image(nm/px) convert to(µm/px).
                self.data = numpy.swapaxes(self.data,1,2)
                LsmPixelHeader = str(tif.pages[0].tags.cz_lsm_info)
                LsmInfo = LsmPixelHeader.split(", ")
                i = 0
                #Query for pixel size.
                for element in LsmInfo:

                    if "e-0" in element:
                        i += 1
                        if i == 1:
                            self.metaData['SizeX'] = (float(element)*10**6)
                        if i == 2:
                            self.metaData['SizeY'] = (float(element)*10**6)
                        if i == 3:
                            self.metaData['SizeZ'] = (float(element)*10**6)

        elif self.extend == ".png":
            self.data = misc.imread(self.file_path)
            self.data = np.expand_dims(np.expand_dims(self.data[...,0],0),0)
            self.metaData["ShapeSizeC"] = 1
            self.metaData["ShapeSizeZ"] = 1
            self.metaData["ShapeSizeX"] = self.data.shape[2]
            self.metaData["ShapeSizeY"] = self.data.shape[3]
            self.metaData["SizeZ"] = 1
            self.metaData["SizeX"] = 0.01
            self.metaData["SizeY"] = 0.01
        #Bring all formats in the same shape.
        self.data = np.reshape(self.data,(self.metaData["ShapeSizeC"],self.metaData["ShapeSizeZ"],self.metaData["ShapeSizeX"],self.metaData["ShapeSizeY"]))
        self.metaData['ChannelNum'] = self.metaData["ShapeSizeC"]
        #Set pixel size to manuell value if there are no metadata.
        if self.metaData == {}:
            self.set_calibration(calibration_px)
        #Set the box for manuel calibration to the actuell pixel size.
        try:
            for spin_box in main_window.confocal_settings.spin_boxes:
                    obj_name = str(spin_box.objectName())
                    if obj_name=='doubleSpinBox_confocal_config_calibration_px':
                        spin_box.setValue(self.metaData['SizeX'])
                        main_window.dialog_export_roi.render_px_size.setValue(self.metaData['SizeX'])
        except:
            print("set Px Size manually")

    def setIndex(self, channel, value):
        self.index[channel] = value

    def setFlip(self, direction, value):
        """
        directions: UpsideDown, LeftRight
        value: True, False
        """
        self.flip[direction] = value

    #Set pixel size to manuell value.
    def set_calibration(self, px):
        self.metaData['SizeX'] = px
        self.metaData['SizeY'] = px
        self.metaData['SizeZ'] = px

def construct_new_image_storm(imgs):
    basic_image = imgs[0]
    List= []
    ChannelList = []
    for i in range(len(imgs)):
        List.append(imgs[i].stormData[0])
        ChannelList.append("ch"+str(i))
    basic_image.stormData = numpy.array(List)
    basic_image.StormChannelList = ChannelList
    return basic_image
