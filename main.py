# -*- coding: utf-8 -*-

import sys
#import FileDialog # important to exe build!
from PyQt5.QtWidgets import QApplication, QMainWindow
from controllers.main_window import MainWindow

if __name__ == "__main__":
    """ base qt init """
    qtApp = QApplication(sys.argv)
    qtWindow = QMainWindow()
    mainWindow = MainWindow()
    mainWindow.setupUi(qtWindow)


    """ additional init """
    mainWindow.init_component(qtWindow)


    """ show & run """
    qtWindow.show()
    sys.exit(qtApp.exec_())