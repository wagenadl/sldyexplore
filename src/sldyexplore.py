#!/usr/bin/python3

from PyQt6 import QtCore, QtGui, QtWidgets
import sys

from mainwin import MainWindow


def maincli():
    if len(sys.argv) == 2:
        ifn = sys.argv[1]
    else:
        ifn = None
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.show()
    if ifn:
        win.load(ifn)
    app.exec()


    
if __name__ == "__main__":
    maincli()
