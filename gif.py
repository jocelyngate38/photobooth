#!/usr/bin/env python


from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QRectF, QSettings, QSize,
                          Qt, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QDateTime, QIODevice, QElapsedTimer)
from PyQt5.QtGui import QIcon, QKeySequence, QFont, QPixmap, QPainter, QPen, QColor, QMovie
from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow)

import platform

if platform.system() == 'Windows':
    EMULATE = True
else:
    EMULATE = False

    import RPi.GPIO as GPIO
    import pyautogui

from random import randint
from random import randrange
from datetime import datetime
from ressourceManager import *

import threading, time, random, shutil, os, subprocess

import glob
import json
from subprocess import Popen, PIPE, check_output
from boothFilters import *

import uuid
from enum import Enum


class Label(QLabel):

    ribbonEmptyRight = True
    trayMissingRight = True
    paperEmptyRight = True
    ribbonEmptyLeft = True
    trayMissingLeft = True
    paperEmptyLeft = True

    def setRibbonEmptyRight(self, b):
        self.ribbonEmptyRight = b

    def setPaperEmptyRight(self, b):
        self.trayMissingRight = b

    def setTrayMissingRight(self, b):
        self.paperEmptyRight = b

    def setRibbonEmptyLeft(self, b):
        self.ribbonEmptyLeft = b

    def setPaperEmptyLeft(self, b):
        self.trayMissingLeft = b

    def setTrayMissingLeft(self, b):
        self.paperEmptyLeft = b

    def __init__(self, parent=None):
        super(Label, self).__init__(parent=parent)

    def paintEvent(self, e):
        iL = 0
        jL = 0
        iR = 1280-229
        jR = 0
        incw = 0
        inch = 85
        super().paintEvent(e)
        qp = QPainter(self)
        if self.ribbonEmptyLeft is True:
            qp.drawPixmap(iL, jL, QPixmap("ribbonEmpty.png"))
            iL = iL + incw
            jL = jL + inch
        if self.trayMissingLeft is True:
            qp.drawPixmap(iL, jL, QPixmap("trayMissing.png"))
            iL = iL + incw
            jL = jL + inch
        if self.paperEmptyLeft is True:
            qp.drawPixmap(iL, jL, QPixmap("paperEmpty.png"))

        if self.ribbonEmptyRight is True:
            qp.drawPixmap(iR, jR, QPixmap("ribbonEmpty.png"))
            iR = iR + incw
            jR = jR + inch
        if self.trayMissingRight is True:
            qp.drawPixmap(iR, jR, QPixmap("trayMissing.png"))
            iR = iR + incw
            jR = jR + inch
        if self.paperEmptyRight is True:
            qp.drawPixmap(iR, jR, QPixmap("paperEmpty.png"))


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.movie = None
        self.label = None

        self.showFullScreen()
        self.initGUI()

        self.showHomePage()
        QApplication.processEvents()
        QApplication.processEvents()

    def initGUI(self):
        self.label = Label()
        self.label.setFont(QFont("Right Chalk", 110, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        self.label.setMinimumHeight(1024)
        self.label.setMinimumWidth(1280)
        self.label.setMaximumHeight(1024)
        self.label.setMaximumWidth(1280)

        self.setCentralWidget(self.label)

        self.movie = QMovie("home.gif")
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.loopCount()

    def showHomePage(self):
        # if self.trayMissing is True:
        # if self.paperEmpty is True:
        # if self.ribbonEmpty is True:

        self.label.setMovie(self.movie)
        self.movie.start()
        QApplication.processEvents()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    # sim = SimulatorButtonThread(mainWin, 1)
    # sim.start()
    mainWin.show()
    ret = app.exec_()
    sys.exit(ret)
