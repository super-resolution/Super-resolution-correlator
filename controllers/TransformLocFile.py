#Copyright (c) 2016-2017 Sebastian Reinhard

import pandas as pd
import numpy as np
pumba = False
try:
    import numba
    pumba = True
except:
    print("no acceleration of bunwarpj")
from skimage import transform
import xml.etree.ElementTree as XMLET
from itertools import islice
import re

#Class to get the relevant information from the header of a with rapidstorm processed file.as
#Takes an input path of a lokalisation file and converts the data to a numpy array delimiter is whitespace
#Parses the relevant info of file header with regular expressions
class Header(object):
    def __init__(self):
        self.semantic = 0

class TransformLocFile(object):
    def __init__(self, inputLocalisationPath):
        self.dataColumn = {}
        self.getRapidSTORMHeaderInfo(inputLocalisationPath)
        try:
            self.stormData = pd.read_csv(inputLocalisationPath, skiprows=1,engine="c", na_filter=False, header=None, delim_whitespace=True, dtype=np.float32).as_matrix()
        except:
            self.stormData = pd.read_csv(inputLocalisationPath, skiprows=1, header=None, delim_whitespace=True, dtype=np.float32).as_matrix()

    def clear(self):
        self.stormData = []
        self.trans_size = []
        self.loc_size = []
        self.trans_matrix = []
        self.dataColumn = {}

    #Read rapidSTORM header info with regular expressions
    def getRapidSTORMHeaderInfo(self, inputLocalisationPath):
        with open(inputLocalisationPath) as loc:
            self.Header = list(islice(loc, 1))
            headerSplit = self.Header[0].split("/><")
        for i in range(len(headerSplit)):
            if "semantic" in headerSplit[i]:
                identifierString = headerSplit[i].split('semantic="')
                identifier = identifierString[-1].split('"', 1)[0]
                self.dataColumn[identifier] = i
                try:
                    max_value = headerSplit[i].split('max="')[-1].split('"',1)[0]
                    max_value = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", max_value)
                    self.dataColumn[identifier + " max value"] = float(max_value[0])
                except:
                    print("no max value" + identifier)
        self.loc_size = np.array([float(self.dataColumn["position in sample space in X max value"]), float(self.dataColumn["position in sample space in Y max value"])])

    #read matrix header
    def getMatrixHeaderInfo(self, input_trans_path):
        with open(input_trans_path) as file:
            self.header = list(islice(file, 2))
        #Get image heigth and width
        width = int(self.header[0].split("=")[1])
        height = int(self.header[1].split("=")[1])
        self.trans_size = np.array([width, height])

    #Get maximum value in e notation
    def get_max_value(self, string):
        string_split = string.split()
        for value in string_split:
            if value.__contains__("max"):
                try:
                    max_value = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", value)
                except:
                    print("fuck")
        return max_value[0]

    #Read matrix into x transformation and y transformation array
    def matrixAsArray(self, input_trans_path):
        self.trans_matrix_X = pd.read_csv(input_trans_path, skiprows=4, header=None, nrows=self.trans_size[1], delim_whitespace=True).as_matrix()
        self.trans_matrix_Y = pd.read_csv(input_trans_path, skiprows=(6+self.trans_size[1]), header=None, delim_whitespace=True).as_matrix()

    #Save localisation file into "rapidSTORM like" file
def saveLocFile( path, file):
        x_max = "%.5e" %(file[:,0].max()*10**(-9))
        x_min = "%.5e" %(file[:,0].min()*10**(-9))
        y_max = "%.5e" %(file[:,1].max()*10**(-9))
        y_min = "%.5e" %(file[:,1].min()*10**(-9))
        frame_min = '%u' %file[:2].min()

        #header = '<localizations insequence="true" repetitions="variable"><field identifier="Position-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="position in sample space in X" unit="nanometer" min=\"'+str(x_min)+' m\" max=\"'+str(x_max)+' m\" /><field identifier="Position-1-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="position in sample space in Y" unit="nanometer" min=\"'+str(y_min)+' m\" max=\"'+str(y_max)+' m\" /><field identifier="ImageNumber-0-0" syntax="integer" semantic="frame number" unit="frame" min=\"'+str(frame_min)+' fr\" /><field identifier=\"Amplitude-0-0\" syntax=\"floating point with . for decimals and optional scientific e-notation\" semantic=\"emission strength\" unit=\"A/D count\" /><field identifier="FitResidues-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="fit residue chi square value" unit="dimensionless" /><field identifier="Fluorophore-0-0" syntax="integer" semantic="index of fluorophore type" unit="dimensionless" min="0 dimensionless" max="1 dimensionless" /><field identifier="LocalBackground-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="local background" unit="A/D count" /></localizations>'
        header = '<localizations insequence="true" repetitions="variable"><field identifier="Position-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="position in sample space in X" unit="nanometer" min=\"'+str(x_min)+' m\" max=\"'+str(x_max)+' m\" /><field identifier="Position-1-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="position in sample space in Y" unit="nanometer" min=\"'+str(y_min)+' m\" max=\"'+str(y_max)+' m\" /><field identifier="Position-2-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="position in sample space in Z" unit="nanometer" min="-7.9e-007 m" max="7.9e-007 m" /><field identifier="ImageNumber-0-0" syntax="integer" semantic="frame number" unit="frame" min="0 fr" max="60809 fr" /><field identifier="Amplitude-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="emission strength" unit="A/D count" /><field identifier="FitResidues-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="fit residue chi square value" unit="dimensionless" /><field identifier="LocalBackground-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="local background" unit="A/D count" /></localizations>'
        np.savetxt(path, file, delimiter=' ', header= header, fmt="%1.3f")

def test(data):
    asdf = pd.read_csv(r"C:\Users\biophys\VividSTORM_total_workover_bugfix_\temp\Landmarks.txt", skiprows=1,engine="c", na_filter=False, header=None, delim_whitespace=True, dtype=np.float32).as_matrix()
    dst = asdf[:,3:5]
    src = asdf[:,1:3]
    affine = transform.estimate_transform("affine",src,dst)
    x = affine.inverse(data[:,0:2])
    data[:,0:2] = x
    return data

#Acceleratet array computation with numba
#Transform localisation file with tranformation matrix
if pumba:
    @numba.jit(nopython= True,)
    def unwarp(loc_input_1, matrix_X , matrix_Y, pixel_size, real_size):
        for i in range(loc_input_1.shape[0]): #drauf achten das x der erste Eintrag und Y der zweite Eintrag ist

                x_1 = (loc_input_1[i][0]*10**-9/real_size[0])*pixel_size[0]-0.5#-1 wegen array indices pixelsize=x arraysize=x-1 startet bei 0+0.5 pixel offset
                y_1 = (loc_input_1[i][1]*10**-9/real_size[1])*pixel_size[1]-0.5
                x_1_G = int(x_1)
                y_1_G = int(y_1)
                x_1_N = x_1-x_1_G
                y_1_N = y_1-y_1_G
                x_2_Ganz = matrix_X[y_1_G, x_1_G]
                y_2_Ganz = matrix_Y[y_1_G, x_1_G]
                if(x_1_G<(pixel_size[0]-1))and(y_1_G<(pixel_size[1]-1)):
                    x_2 = x_2_Ganz+(matrix_X[y_1_G+1, x_1_G]-x_2_Ganz)*x_1_N+(matrix_X[y_1_G, x_1_G+1]-x_2_Ganz)*y_1_N#nur interpolation fuer x interpolation fuer y fehlt. ; interpolation zeile
                    y_2 = y_2_Ganz+(matrix_Y[y_1_G, x_1_G+1]-y_2_Ganz)*y_1_N+(matrix_Y[y_1_G+1, x_1_G]-y_2_Ganz)*x_1_N
                else:
                    x_2 = x_2_Ganz+(x_2_Ganz-matrix_X[y_1_G-1, x_1_G])*x_1_N+(x_2_Ganz-matrix_X[y_1_G, x_1_G-1])*y_1_N
                    y_2 = y_2_Ganz+(y_2_Ganz-matrix_Y[y_1_G, x_1_G-1])*y_1_N+(y_2_Ganz-matrix_Y[y_1_G-1, x_1_G])*x_1_N #interpolation spalte
                y_3 = (y_2/pixel_size[1])*real_size[1]*10**9
                x_3 = (x_2/pixel_size[0])*real_size[0]*10**9
                loc_input_1[i][0]= x_3
                loc_input_1[i][1]= y_3
        x_min = loc_input_1[:,0].min()
        y_min = loc_input_1[:,1].min()
        if x_min<0:
            loc_input_1[:,0] = loc_input_1[:,0]+(x_min*-1)
        if y_min<0:
            loc_input_1[:,1] = loc_input_1[:,1]+(y_min*-1)
        return loc_input_1
else:
    def unwarp(loc_input_1, matrix_X , matrix_Y, pixel_size, real_size):
        for i in range(loc_input_1.shape[0]): #drauf achten das x der erste Eintrag und Y der zweite Eintrag ist

                x_1 = (loc_input_1[i][0]*10**-9/real_size[0])*pixel_size[0]-0.5#-1 wegen array indices pixelsize=x arraysize=x-1 startet bei 0+0.5 pixel offset
                y_1 = (loc_input_1[i][1]*10**-9/real_size[1])*pixel_size[1]-0.5
                x_1_G = int(x_1)
                y_1_G = int(y_1)
                x_1_N = x_1-x_1_G
                y_1_N = y_1-y_1_G
                x_2_Ganz = matrix_X[y_1_G, x_1_G]
                y_2_Ganz = matrix_Y[y_1_G, x_1_G]
                if(x_1_G<(pixel_size[0]-1))and(y_1_G<(pixel_size[1]-1)):
                    x_2 = x_2_Ganz+(matrix_X[y_1_G+1, x_1_G]-x_2_Ganz)*x_1_N+(matrix_X[y_1_G, x_1_G+1]-x_2_Ganz)*y_1_N#nur interpolation fuer x interpolation fuer y fehlt. ; interpolation zeile
                    y_2 = y_2_Ganz+(matrix_Y[y_1_G, x_1_G+1]-y_2_Ganz)*y_1_N+(matrix_Y[y_1_G+1, x_1_G]-y_2_Ganz)*x_1_N
                else:
                    x_2 = x_2_Ganz+(x_2_Ganz-matrix_X[y_1_G-1, x_1_G])*x_1_N+(x_2_Ganz-matrix_X[y_1_G, x_1_G-1])*y_1_N
                    y_2 = y_2_Ganz+(y_2_Ganz-matrix_Y[y_1_G, x_1_G-1])*y_1_N+(y_2_Ganz-matrix_Y[y_1_G-1, x_1_G])*x_1_N #interpolation spalte
                y_3 = (y_2/pixel_size[1])*real_size[1]*10**9
                x_3 = (x_2/pixel_size[0])*real_size[0]*10**9
                loc_input_1[i][0]= x_3
                loc_input_1[i][1]= y_3
        x_min = loc_input_1[:,0].min()
        y_min = loc_input_1[:,1].min()
        if x_min<0:
            loc_input_1[:,0] = loc_input_1[:,0]+(x_min*-1)
        if y_min<0:
            loc_input_1[:,1] = loc_input_1[:,1]+(y_min*-1)
        return loc_input_1

if __name__ == "__main__":
    #instance = TransformLocFile(r"C:asdf/asdf")#file path to loc file
    #nstance.matrixAsArray(r"C:asdf/asdf")#path to matrix

    #yourData: x position column0 y position column1
    #matrix x
    #matrix y
    #trans_size: sizeof matrix x,y
    #loc_size: size of probe x,y
    out = unwarp(yourData, trans_matrix_X, trans_matrix_Y, trans_size, loc_size)#transform stuff
    saveLocFile(r"C:asdf/asdf", out)#your path






