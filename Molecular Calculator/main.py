"""
Created on Tue Dec 13 08:38:33 2022

@author: g.mayneord
"""
import sys
from PyQt5 import QtWidgets, QtCore

from gui_functions.MainWindowInterface import MainWindow

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


if __name__ == "__main__":
    App = QtWidgets.QApplication.instance()
    if App is None:
        App = QtWidgets.QApplication(sys.argv)
    Main = MainWindow()
    Main.GUI.show()
    sys.exit(App.exec_())
