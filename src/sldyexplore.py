#!/usr/bin/python3

from PyQt6 import QtCore, QtGui, QtWidgets
import sys

from mainwin import MainWindow

if len(sys.argv) == 2:
    ifn = sys.argv[1]
else:
    ifn = None
    
print(ifn)
app = QtWidgets.QApplication([])
win = MainWindow()
win.show()
win.load(ifn)
app.exec()
