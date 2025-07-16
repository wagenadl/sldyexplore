# pyuic6 mainwin.ui >| mainwin_ui.py

import numpy as np
import os.path
from PyQt6 import QtCore, QtGui, QtWidgets

from mainwin_ui import Ui_MainWindow


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.image.setScaledContents(True)
        self.data = None
        self.key = (-1, -1) # c,t
        self.z = 0
        self.c = 0
        self.t = 0
        self.Z = 0
        self.C = 0
        self.T = 0
        self.imgdir = None
        

    def _filename(self, c, t):
        """Filename for a given channel and time point"""
        return f"{self.imgdir}/ImageData_Ch{c}_TP{t:07d}.npy"

    
    def _count(self):
        self.Z = 0
        self.C = 0
        self.T = 0
        self.Z = 0
        while os.path.exists(self._filename(self.C, 0)):
            self.C += 1
        if self.C == 0:
            return
        while os.path.exists(self._filename(0, self.T)):
            self.T += 1
        dat = np.load(self._filename(0, 0), mmap_mode='r')
        self.Z = len(dat)
        self.ui.channel.setMaximum(self.C - 1)
        self.ui.z.setMaximum(self.Z - 1)
        self.ui.time.setMaximum(self.T - 1)

        
    def load(self, imgdir=None):
        self.ui.image.setText("Image")
        if not(imgdir):
            if not(self.imgdir):
                imgdir = QtCore.QDir.home().path()
            else:
                imgdir = self.imgdir
            imgdir = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                "Choose an imgdir",
                                                                directory=imgdir)
            if not(imgdir):
                return
        self.imgdir = imgdir
        self._count()
        if self.C == 0:
            QtWidgets.QMessageBox.warning(self, "SLDY explore",
                                          "Not an image dir!?")
            return
        self.ui.channel.setValue(0)
        self.ui.z.setValue(0)
        self.ui.time.setValue(0)
        self.shownumbers()
        self.showimage()
        self.setWindowTitle(imgdir)

        
    def gamma(self):
        return 2**(self.ui.gamma.value()/30.0)

    def black(self):
        return int(65535 * (self.ui.black.value()/255)**3)
    
    def white(self):
        return int(65535 * (self.ui.white.value()/255)**3)

    def shownumbers(self):
        self.ui.iblack.setText(f"{self.black()}")
        self.ui.iwhite.setText(f"{self.white()}")
        self.ui.igamma.setText(f"{self.gamma():.2f}")
        self.ui.ichannel.setText(f"{self.ui.channel.value()}")
        self.ui.iz.setText(f"{self.ui.z.value()}")
        self.ui.itime.setText(f"{self.ui.time.value()}")


    def showimage(self):
        w = self.windowHandle()
        if w:
            ratio = w.devicePixelRatio()
        else:
            ratio = 2
        key = (self.ui.channel.value(), self.ui.time.value())
        if key != self.key:
            self.data = np.load(self._filename(key[0], key[1]), mmap_mode="r")
            self.key = key
        img = self.data[self.ui.z.value()].astype(np.float32) - self.black()
        img /= max(1.0, self.white() - self.black())
        img[img<0] = 0
        img[img>1] = 1
        img **= self.gamma()
        img = (255.99*img).astype(np.uint8)
        qimg = QtGui.QImage(img, img.shape[1], img.shape[0],
                            QtGui.QImage.Format.Format_Grayscale8)
        pxmp = QtGui.QPixmap(qimg)
        pxmp.setDevicePixelRatio(ratio)
        self.ui.image.setPixmap(pxmp)

        
    def moveSlider(self):
        self.shownumbers()
        self.showimage()


    def about(self):
        QtWidgets.QMessageBox.about(self, "SLDY explore",
                                    """<b>SLDY explore</b> (CNTL 395)<br>
(C) Daniel Wagenaar 2025<br>
A simple viewer for Slidebook image directories""")                                    
