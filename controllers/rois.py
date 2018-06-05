# -*- coding: utf-8 -*-
"""
Created on: 2015.02.14.

Author: turbo


"""

import os

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore

class Roi(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super(Roi, self).__init__(*args, **kwargs)
        self.setText(args[0].split(os.sep)[-1])
        self.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        # self.StormData = []
        self.roi = None
        
    def ChangeName(self,NewName):
        self.setText(NewName)
        
class CircleRoi(Roi):
    def __init__(self, *args, **kwargs):
        super(CircleRoi, self).__init__(*args, **kwargs)
        
class EllipseRoi(Roi):
    def __init__(self, *args, **kwargs):
        super(EllipseRoi, self).__init__(*args, **kwargs)

class FreehandRoi(Roi):
    def __init__(self, *args, **kwargs):
        super(FreehandRoi, self).__init__(*args, **kwargs)

class ActiveContourRoi(Roi):
    def __init__(self, *args, **kwargs):
        super(ActiveContourRoi, self).__init__(*args, **kwargs)
