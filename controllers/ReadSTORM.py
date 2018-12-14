import pandas as pd

import numpy as np
from itertools import islice
import re

class stormfile(object):
    def __init__(self, input_loc_path):
        self.dataColumn = {}
        self.data = []
        self.size = []
        self.path = input_loc_path


    def readfile(self):
        self.data = pd.read_csv(self.path, skiprows=1, header=None, delim_whitespace=True).as_matrix()

    def clear(self):
        self.data = []
        self.loc_size = []

    def getHeaderInfo(self):
        with open(self.path) as loc:
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



    def save_loc_file(self, path, file):
        x_max = "%.5e" %(file[:,0].max()*10**(-9))
        x_min = 0 #"%.5e" %(loc_input_1[:,0].min()*10**(-9))
        y_max = "%.5e" %(file[:,1].max()*10**(-9))
        y_min = 0 #"%.5e" %(loc_input_1[:,1].min()*10**(-9))
        frame_min = '%u' %file[:2].min()

#        header = '<localizations insequence=\\"true\\" repetitions=\\"variable\\"><field identifier=\\"Position-0-0\\" syntax=\\"floating point with . for decimals and optional scientific e-notation\\" semantic=\\"position in sample space in X\\" unit=\\"nanometer\\" min=\\"'+str(x_min)+' m\\" max=\\"'+str(x_max)+' m\\" /><field identifier=\\"Position-1-0\\" syntax=\\"floating point with . for decimals and optional scientific e-notation\\" semantic=\\"position in sample space in Y\\" unit=\\"nanometer\\" min=\\"'+str(y_min)+' m\\" max=\\"'+str(y_max)+' m\\" /><field identifier=\\"ImageNumber-0-0\\" syntax=\\"integer\\" semantic=\\"frame number\\" unit=\\"frame\\" min=\\"'+str(frame_min)+' fr\\" /><field identifier=\"Amplitude-0-0\" syntax=\"floating point with . for decimals and optional scientific e-notation\" semantic=\"emission strength\" unit=\"A/D count\" /><field identifier=\\"FitResidues-0-0\\" syntax=\\"floating point with . for decimals and optional scientific e-notation\\" semantic=\\"fit residue chi square value\\" unit=\\"dimensionless\\" /><field identifier=\\"Fluorophore-0-0\\" syntax=\\"integer\\" semantic=\\"index of fluorophore type\\" unit=\\"dimensionless\\" min=\\"0 dimensionless\\" max=\\"1 dimensionless\\" /><field identifier=\\"LocalBackground-0-0\\" syntax=\\"floating point with . for decimals and optional scientific e-notation\\" semantic=\\"local background\\" unit=\\"A/D count\\" /></localizations>'
        header = '<localizations insequence="true" repetitions="variable"><field identifier="Position-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="position in sample space in X" unit="nanometer" min=\"'+str(x_min)+' m\" max=\"'+str(x_max)+' m\" /><field identifier="Position-1-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="position in sample space in Y" unit="nanometer" min=\"'+str(y_min)+' m\" max=\"'+str(y_max)+' m\" /><field identifier="ImageNumber-0-0" syntax="integer" semantic="frame number" unit="frame" min=\"'+str(frame_min)+' fr\" /><field identifier=\"Amplitude-0-0\" syntax=\"floating point with . for decimals and optional scientific e-notation\" semantic=\"emission strength\" unit=\"A/D count\" /><field identifier="FitResidues-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="fit residue chi square value" unit="dimensionless" /><field identifier="Fluorophore-0-0" syntax="integer" semantic="index of fluorophore type" unit="dimensionless" min="0 dimensionless" max="1 dimensionless" /><field identifier="LocalBackground-0-0" syntax="floating point with . for decimals and optional scientific e-notation" semantic="local background" unit="A/D count" /></localizations>'
        np.savetxt(path, file, delimiter=' ', fmt=['%1.1f','%1.1f','%u','%.10g','%.10g','%u','%1.3f'], header= header)

