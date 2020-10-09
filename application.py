#!/usr/bin/env python


from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QRectF, QSettings, QSize,
                          Qt, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QDateTime, QIODevice, QElapsedTimer)
from PyQt5.QtGui import QIcon, QKeySequence, QFont, QPixmap, QPainter, QPen, QColor, QMovie
from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow)

import platform

if platform.system() == 'Windows':
    EMULATE = True
    print("Windows detected we emulate GPIO")
else:
    EMULATE = False
    print("Windows not detected we use GPIO")

    import RPi.GPIO as GPIO
    import pyautogui

from random import randint
from random import randrange
from datetime import datetime
from ressourceManager import *
from six.moves.queue import Queue
from enum import Enum
import threading, time, random, shutil, os, subprocess
import cups
import glob
import json
from subprocess import Popen, PIPE
from boothFilters import *
import cv2

class GPIOMode(Enum):
    WAITING = 1
    RUNNING = 2
    MENU = 3
    SETUP_MENU = 4
    TRIGGER_ERROR_PAGE = 5
    PRINTING = 6
    PRINTER_MAINTENANCE = 7
    DISPLAY_ASSEMBLY = 8
    COMPUTING = 9
    VALIDATING = 10
    STYLISHING = 11


if EMULATE is False:
    GPIO.setmode(GPIO.BCM)


class InputButtonThread(QThread):
    inputButtonEventDetected = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.queue = Queue()
        if EMULATE is False:
            GPIO.add_event_detect(21, GPIO.FALLING, callback=self.queue.put, bouncetime=500)
            GPIO.add_event_detect(26, GPIO.FALLING, callback=self.queue.put, bouncetime=500)
            GPIO.add_event_detect(6, GPIO.FALLING, callback=self.queue.put, bouncetime=500)
        # GPIO 20 wired also

    def run(self):
        while True:
            self.inputButtonEventDetected.emit(self.queue.get())


class SimulatorButtonThread(QThread):

    def __init__(self, mm, delay):
        QThread.__init__(self)
        self.mainWindow = mm
        self.delay = delay

    def run(self):
        while True:
            j = random.randint(1, 3)
            print(str(j))
            time.sleep(self.delay)
            if j == 1:
                self.mainWindow.onRightButtonPressed()
            if j == 2:
                self.mainWindow.onLeftButtonPressed()
            if j == 3:
                self.mainWindow.onDownButtonPressed()


class SaveToUSB(QThread):

    # signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, localFilePath, usbFilePath, fileName, number):
        QThread.__init__(self)
        self.captureFileName = fileName
        self.captureLocalPath = localFilePath
        self.captureUSBPath = usbFilePath
        self.captureNumber = number

    # run method gets called when we start the thread
    def run(self):

        # 1st : make a copy
        for index in range(self.captureNumber):
            localFile = self.captureLocalPath + "/" + self.captureFileName + "_" + str(index) + ".jpg"
            usbFile = self.captureUSBPath + "/" + self.captureFileName + "_" + str(index) + ".jpg"
            if (not os.path.isfile(usbFile)):
                if (os.path.isfile(localFile)):
                    print("Copying : " + localFile + " to USB")
                    shutil.copyfile(localFile, usbFile)
        print("copy just finished")
        # 2nd : delete original files
        for index in range(self.captureNumber):
            localFile = self.captureLocalPath + "/" + self.captureFileName + "_" + str(index) + ".jpg"
            usbFile = self.captureUSBPath + "/" + self.captureFileName + "_" + str(index) + ".jpg"
            if (os.path.isfile(usbFile)):
                if (os.path.isfile(localFile)):
                    print("Copying : " + localFile + " to USB")
                    os.remove(localFile)
        # self.signal.emit(True)
        print("removal just finished")
        print("SaveToUSB just finished")


class SaveToUSBClass():

    def __init__(self, localFilePath, usbFilePath, fileName, number):
        self.captureFileName = fileName
        self.captureLocalPath = localFilePath
        self.captureUSBPath = usbFilePath
        self.captureNumber = number

    # run method gets called when we start the thread
    def save(self):

        # 1st : make a copy
        for index in range(self.captureNumber):
            localFile = self.captureLocalPath + "/" + self.captureFileName + "_" + str(index) + ".jpg"
            usbFile = self.captureUSBPath + "/" + self.captureFileName + "_" + str(index) + ".jpg"
            if (not os.path.isfile(usbFile)):
                if (os.path.isfile(localFile)):
                    print("Copying : " + localFile + " to USB")
                    shutil.copyfile(localFile, usbFile)
        print("copy just finished")
        # 2nd : delete original files
        for index in range(self.captureNumber):
            localFile = self.captureLocalPath + "/" + self.captureFileName + "_" + str(index) + ".jpg"
            usbFile = self.captureUSBPath + "/" + self.captureFileName + "_" + str(index) + ".jpg"
            if (os.path.isfile(usbFile)):
                if (os.path.isfile(localFile)):
                    print("Copying : " + localFile + " to USB")
                    os.remove(localFile)
        # self.signal.emit(True)
        print("removal just finished")
        print("SaveToUSB just finished")


class CaptureImageThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, filePath, fileName, fileIndex):
        QThread.__init__(self)
        self.captureFileName = fileName
        self.capturePath = filePath
        self.captureIndex = fileIndex

    # run method gets called when we start the thread
    def run(self):

        p = Popen(["gphoto2", "--capture-image-and-download",
                   "--filename=" + self.capturePath + "/" + self.captureFileName + "_" + str(
                       self.captureIndex) + ".jpg"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode

        if len(err) > 0:
            print(err)
            self.signal.emit(False)
        else:
            print(err)
            self.signal.emit(True)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.interuptsConnected = False
        self.currentAssemblyPath = "/home/pi/photobooth-datas/usb_datas/assemblies/20182107_17_18_41"

        self.resources = ressourcesManager()
        self.resources.loadCurrentXmlSkinDescriptor()
        self.resources.getLogger().addInfo("INITIALIZING PHOTOBOOTH")

        # PRINTER SETTINGS
        self.printDuration = 60
        self.numberOfPrint = 0
        self.maxNumberOfPrint = 36

        # DSLR SETTINGS
        self.Wcapture = 3008
        self.Hcapture = 2000

        # PHOTOBOOTH SETTINGS
        self.screenWidth = 1280
        self.screenHeight = 1024

        self.GPIO_buttonRightPin = 21
        self.GPIO_buttonRightLedPin = 13

        self.GPIO_buttonLeftPin = 6
        self.GPIO_buttonLeftLedPin = 19

        self.GPIO_buttonDownPin = 26
        self.GPIO_buttonDownLedPin = 18

        self.GPIO_POWER_SPEEDLIGHT = 23
        self.GPIO_ON_OFF_SPEEDLIGHT = 25
        self.GPIO_POWER_DSLR = 24
        self.GPIO_POWER_PRINTER = 23

        self.currentGPIOMode = GPIOMode.WAITING
        self.nbCapturesMax = self.resources.nbImageMax

        self.nbCaptures = 1
        self.nbCapturesDone = 0
        self.idName = ""
        self.lastAssemblyPixmap = None
        self.lastAssemblyLandscape = 1
        self.countDown = 4

        self.initGPIO()
        self.inputButtonThread = InputButtonThread()
        self.connectInputButtonInterupts()
        self.inputButtonThread.start()

        self.showFullScreen()

        self.fontName = "Right Chalk"
        self.label = QLabel()
        self.font = QFont(self.fontName, 110, QFont.Bold)
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        self.label.setMinimumSize(self.screenWidth, self.screenHeight)
        self.label.setMaximumSize(self.screenWidth, self.screenHeight)
        self.setCentralWidget(self.label)

        self.pwm = 0
        self.sign = 1

        self.buttonDownLedEnabled = True
        self.buttonRightLedEnabled = True
        self.buttonLeftLedEnabled = True

        self.blinkingTimer = QTimer()
        self.blinkingTimer.timeout.connect(self.blink)
        self.blinkingTimer.start(100)

        self.switchLed(False, False, False)

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)

        self.instructionsEnabled = settings.value("instructionsEnabled", True, bool)
        self.printingEnabled = settings.value("printingEnabled", False, bool)
        self.sharingEnabled = settings.value("sharingEnabled", True, bool)
        self.showPrintingStatusEnabled = settings.value("showPrintingStatusEnabled", False, bool)
        self.movie = QMovie("giphy.gif")
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.loopCount()
        
        self.showStartupPixmap()
        #self.initDevices()
        self.initDevicesFast()
        
        self.initActions()
        self.initMenu()
        self.initAdvancedMenu()

        self.timerGoToStart = QTimer()
        self.timerGoToStart.timeout.connect(self.goHomeCallback)

        QApplication.processEvents()
        self.resources.getLogger().addInfo("SETING UP DSLR DATETIME")
        subprocess.call("gphoto2 --set-config datetime=$(date +%s)", shell=True)
        self.switchLed(True, True, True)
        self.setPhotoBoothMode(self.nbCaptures)
        self.resources.getLogger().addInfo("PHOTOBOOTH READY TO USE")

        return

    def generateRandomIO(self, delay):

        generator = SimulatorButtonThread(self, delay)
        generator.start()
        QApplication.processEvents()
        time.sleep(2)

    def showComputingPixmap(self):

        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/computing.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def generateAllSingleAssemblies(self, inputFolder, outputFolder):

        self.currentGPIOMode == GPIOMode.COMPUTING
        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)
        self.showComputingPixmap()

        choosenLayoutList = self.resources.getSkinLayoutDatas()[0]
        choosenLayout = None

        if len(choosenLayoutList) >= 1:
            choosenLayout = choosenLayoutList[0]
        else:
            return

        layoutId = choosenLayout["layoutId"]

        fileList = [f for f in glob.glob(inputFolder + "/*.jpg")]

        for files in fileList:

            idName = os.path.basename(files)
            for ind in range(self.nbCapturesMax):
                idName = idName.replace("_" + str(ind) + ".jpg", "", 1)

            outFile = outputFolder + "/" + idName + "_" + layoutId + ".jpg"

            self.resources.buildSingleLayout(files, outFile, choosenLayout)

        self.gotoStart()

    def testAssemblies(self):

        for i in range(10):
            self.resources.buildAvailableAssemblies(
                self.resources.getPath(ressourcesManager.PATH.CAPTURE_LOCAL) + "/test", i)

    def capture(self):

        self.currentGPIOMode == GPIOMode.RUNNING
        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)

        self.countDown = 4
        for x in range(0, self.countDown):
            time.sleep(
                1 - self.showPixmap(self.nbCapturesDone + 1, self.countDown - x, True, False, False, False, False,
                                    False))
        self.showPixmap(0, 0, True, True, False, False, False, False)

        captureThread = CaptureImageThread(self.resources.getPath(
            ressourcesManager.PATH.CAPTURE_LOCAL), self.idName, self.nbCapturesDone)
        captureThread.signal.connect(self.finished)
        captureThread.start()

        time.sleep(0.7)
        self.showPixmap(0, 0, True, True, True, False, False, False)

        if self.nbCaptures == self.nbCapturesDone + 1:
            self.showPixmap(0, 0, True, False, False, False, True, False)
        else:
            self.showPixmap(0, 0, False, False, False, True, True, False)

    def finished(self, result):

        if result is True:
            self.startValidationProcess()
        else:
            self.showTriggerErrorPage()

    def startValidationProcess(self):

        self.showValidatingPage()

    def startStylishProcess(self):

        self.generateFilterThumbs()
        self.buildAllFilteredAssemblies()
        self.selectedFilter = 0
        self.showStylishingPage()

    def showValidatingPage(self):

        self.currentGPIOMode = GPIOMode.VALIDATING
        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/validatePicture.png")
        self.label.setPixmap(outPixmap)
        
        preview = QPixmap(self.resources.getPath(ressourcesManager.PATH.CAPTURE_LOCAL) +"/"+ self.idName + "_" + str(self.nbCapturesDone) + ".jpg")
        
        x = 150
        y = 150
        w = 900
        h = 600
        
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        print("x:" + str(x) + ", y:" + str(y) + ", w:" + str(w) + ", h:" + str(h))

        painter.translate(x, y)
        painter.drawPixmap(0, 0, preview.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        pen = QPen(Qt.white)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawRect(0,0,w,h)

        painter.translate(-x, -y)

        self.label.setPixmap(outPixmap)
        
        
        
        QApplication.processEvents()
        self.connectInputButtonInterupts()
        self.switchLed(True, True, True)

    def generateFilterThumbs(self):

        for ind in range(self.nbCapturesDone):

            originalPicture = self.resources.getPath(ressourcesManager.PATH.CAPTURE_LOCAL) +"/"+ self.idName + "_" + str(ind) + ".jpg"
            print(originalPicture)
            img_rgb = cv2.imread(originalPicture)
            img_rgb = cv2.resize(img_rgb, (1200, 800))
            height, width, channels = img_rgb.shape
            cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_0.jpg", img_rgb)

            try:
                Cartoonize = Cartoonizer()
                im = Cartoonize.render(img_rgb)
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_1.jpg", im)
            except:
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_1.jpg", img_rgb)

            try:
                Cooling = CoolingFilter()
                im2 = Cooling.render(img_rgb)
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_2.jpg", im2)
            except:
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_2.jpg", img_rgb)

            try:
                Warming = WarmingFilter()
                im3 = Warming.render(img_rgb)
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_3.jpg", im3)
            except:
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_3.jpg", img_rgb)

            
            try:
                Pencil = PencilSketch(width, height)
                im4 = Pencil.render(img_rgb)
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_4.jpg", im4)
            except:
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_4.jpg", img_rgb)

            try:
                Gray = GrayScale()
                im5 = Gray.render(img_rgb)
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_5.jpg", im5)
            except:
                cv2.imwrite(self.resources.getPath(ressourcesManager.PATH.THUMB_LOCAL)+"/"+self.idName + "_" + str(ind) + "_thumb_5.jpg", img_rgb)


    def showStylishingPage(self):

        self.currentGPIOMode = GPIOMode.STYLISHING
        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/stylishPicture.png")

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.lastAssemblyPixmap is not None:
            if self.lastAssemblyLandscape == 1:
                x = self.resources.skinDiplayLayoutDatas["landscape"]["x"]
                y = self.resources.skinDiplayLayoutDatas["landscape"]["y"]
                w = self.resources.skinDiplayLayoutDatas["landscape"]["w"]
                h = self.resources.skinDiplayLayoutDatas["landscape"]["h"]
            else:
                x = self.resources.skinDiplayLayoutDatas["portrait"]["x"]
                y = self.resources.skinDiplayLayoutDatas["portrait"]["y"]
                w = self.resources.skinDiplayLayoutDatas["portrait"]["w"]
                h = self.resources.skinDiplayLayoutDatas["portrait"]["h"]

            print("x:" + str(x) + ", y:" + str(y) + ", w:" + str(w) + ", h:" + str(h))

            painter.translate(x, y)
            painter.drawPixmap(0, 0, self.filteredAssembliesPixmap[self.selectedFilter].scaled(w, h, Qt.KeepAspectRatio,
                                                                    transformMode=Qt.SmoothTransformation))
            pen = QPen(Qt.white)
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawRect(0,0,w,h)

            painter.translate(-x, -y)

        self.label.setPixmap(outPixmap)
        del painter

        QApplication.processEvents()
        self.connectInputButtonInterupts()
        self.switchLed(True, True, True)

    def startPictureAssembly(self):
        
        self.movie.stop()
        self.currentGPIOMode = GPIOMode.RUNNING
        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)

        if EMULATE is True:
            self.idName = "test"
        else:
            self.idName = QDateTime(datetime.now()).toString("yyyyddMM_hh_mm_ss")

        self.nbCapturesDone = 0
        self.capture()


    def showAssemblyPixmap(self):

        templatePixmap = None

        # if self.lastAssemblyLandscape == 1:
        #     print("LANDSCAPE MODE")
        #     templatePixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/r0.png")
        # elif self.lastAssemblyLandscape == 0:
        #     print("PORTRAIT MODE")
        #     templatePixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/r2.png")

        templatePixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/r3.png")

        painter = QPainter(templatePixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.printingEnabled is False:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/r1.png"))

        if self.lastAssemblyPixmap is not None:
            if self.lastAssemblyLandscape == 1:
                x = self.resources.skinDiplayLayoutDatas["landscape"]["x"]
                y = self.resources.skinDiplayLayoutDatas["landscape"]["y"]
                w = self.resources.skinDiplayLayoutDatas["landscape"]["w"]
                h = self.resources.skinDiplayLayoutDatas["landscape"]["h"]
            else:
                x = self.resources.skinDiplayLayoutDatas["portrait"]["x"]
                y = self.resources.skinDiplayLayoutDatas["portrait"]["y"]
                w = self.resources.skinDiplayLayoutDatas["portrait"]["w"]
                h = self.resources.skinDiplayLayoutDatas["portrait"]["h"]

            print("x:" + str(x) + ", y:" + str(y) + ", w:" + str(w) + ", h:" + str(h))

            painter.translate(x, y)
            painter.drawPixmap(0, 0, self.lastAssemblyPixmap.scaled(w, h, Qt.KeepAspectRatio,
                                                                    transformMode=Qt.SmoothTransformation))
            pen = QPen(Qt.white)
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawRect(0,0,w,h)

            painter.translate(-x, -y)

        self.label.setPixmap(templatePixmap)
        del painter
        QApplication.processEvents()


    def buildShuffleAssembly(self):

        choosenLayout = self.resources.chooseRandomLayout(self.nbCaptures)

        if choosenLayout == None:
            return

        self.timerGoToStart.stop()
        self.lastAssemblyPixmap = None
        self.lastAssemblyLandscape = choosenLayout["landscape"]
        self.showAssemblyPixmap()
        [self.lastAssemblyPixmap, self.currentAssemblyPath] = self.resources.buildLayout(self.idName, choosenLayout)

        self.currentGPIOMode = GPIOMode.DISPLAY_ASSEMBLY
        self.connectInputButtonInterupts()
        self.switchLed(True, self.printingEnabled, True)
        self.showAssemblyPixmap()
        self.timerGoToStart.start(120000)


    def buildAllFilteredAssemblies(self):

        self.currentGPIOMode = GPIOMode.STYLISHING
        self.disconnectInputButtonInterupts()

        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/buildFilteredAssemblies.png")
        self.label.setPixmap(outPixmap)

        QApplication.processEvents()
        QApplication.processEvents()
        QApplication.processEvents()

        choosenLayout = self.resources.chooseRandomLayout(self.nbCaptures)
        self.lastAssemblyLandscape = choosenLayout["landscape"]

        if choosenLayout == None:
            return

        self.filteredAssembliesPixmap=[None] * 6
        self.filteredAssembliesPath=[None] * 6
        
        for ind in range(5):
            print(ind)
            [self.filteredAssembliesPixmap[ind], self.filteredAssembliesPath[ind]] = self.resources.buildLayout2(self.idName, choosenLayout, ind)

        self.connectInputButtonInterupts()
        self.switchLed(True, True, True)

    def showPixmapMenu(self):

        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/menu.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()
        QApplication.processEvents()
        QApplication.processEvents()


    def showStartupPixmap(self):

        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/startup.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()


    def showShutdownPixmap(self):

        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/shutdown.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()


    def showGoHomePixmap(self):

        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/goHome.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()


    def showPixmap(self, photoNumber, chrono, title, smiley, flash, dontMove, download, asembly):

        start = time.time()
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p0.png")

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        if photoNumber == 1:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p5.png"))
        elif photoNumber == 2:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p6.png"))
        elif photoNumber == 3:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p7.png"))
        elif photoNumber == 4:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p8.png"))

        if chrono >= 1 or chrono <= 10:
            painter.drawPixmap(0, 0, QPixmap(
                self.resources.getPath(ressourcesManager.PATH.PAGE) + "/" + str(chrono) + ".png"))

        if title is True:
            painter.drawPixmap(0, 0,
                               QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p1.png"))
        if smiley is True:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p2.png"))
        if flash is True:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p3.png"))
        if dontMove is True:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p4.png"))
        if download is True:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p14.png"))
        if asembly is True:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/p13.png"))

        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

        del painter
        end = time.time()
        print(str(end - start) + " to showPixmap")
        if end - start >= 1:
            return 1
        else:
            return end - start


    def blink(self):
        if EMULATE is True:
            return
        self.pwm += 10 * self.sign

        if self.pwm > 30:
            self.pwm = 30
            self.sign = -1

        if self.pwm < 5:
            self.sign = 1
            self.pwm = 5

        if self.buttonRightLedEnabled:
            self.buttonRightLedPWM.start(self.pwm)
        else:
            self.buttonRightLedPWM.start(0)

        if self.buttonDownLedEnabled:
            self.buttonDownLedPWM.start(self.pwm)
        else:
            self.buttonDownLedPWM.start(0)

        if self.buttonLeftLedEnabled:
            self.buttonLeftLedPWM.start(self.pwm)
        else:
            self.buttonLeftLedPWM.start(0)


    def onRightButtonPressed(self):

        if self.interuptsConnected is False:
            return

        if self.currentGPIOMode == GPIOMode.WAITING:
            self.increaseNbPhoto()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.RUNNING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            self.startStylishProcess()

        elif self.currentGPIOMode == GPIOMode.MENU or self.currentGPIOMode == GPIOMode.SETUP_MENU:
            self.onRightButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR_PAGE:
            self.resources.logger.addWarning(
                "RETRYING CAPTURE " + self.idName + "_" + str(self.nbCapturesDone) + " " + str(
                    self.nbCapturesDone) + "/" + str(
                    self.nbCaptures))
            self.capture()

        elif self.currentGPIOMode == GPIOMode.PRINTER_MAINTENANCE:
            # maintenance and goto redo assembly
            self.cancelNotCompletedJobs()
            self.enablePrinter()
            self.currentGPIOMode = GPIOMode.RUNNING
            self.redoAssembly()

        elif self.currentGPIOMode == GPIOMode.PRINTING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.VALIDATING:
            self.capture()

        elif self.currentGPIOMode == GPIOMode.STYLISHING:

            self.lastAssemblyPixmap = self.filteredAssembliesPixmap[self.selectedFilter]
            self.currentAssemblyPath = self.filteredAssembliesPath[self.selectedFilter]
            self.currentGPIOMode = GPIOMode.DISPLAY_ASSEMBLY
            self.connectInputButtonInterupts()
            self.switchLed(True, self.printingEnabled, True)
            self.showAssemblyPixmap()

        else:
            print("No valid mode selected " + str(int(self.currentGPIOMode)))

    def onLeftButtonPressed(self):

        if self.interuptsConnected is False:
            return

        if self.currentGPIOMode == GPIOMode.WAITING:
            start = time.time()
            stop = 0
            duration = 0
            if EMULATE is False:
                while GPIO.input(6) == 0:
                    time.sleep(0.2)
                    print("pressed")
            duration = (time.time() - start)
            print("unpressed")
            print(GPIO.input(6))
            if duration < 5:
                self.decreaseNbPhoto()
            elif duration >= 5 and duration < 10:
                self.onShowMenu()
            elif duration >= 10 and duration < 20:
                if EMULATE is False:
                    self.currentGPIOMode = GPIOMode.SETUP_MENU
                    self.onShowAdvancedMenu()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.RUNNING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            if self.printingEnabled is True:
                
                self.sendPrintingJob(True)
                # not sure if we go to home page maybe users wants to print several times.
                self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.MENU or self.currentGPIOMode == GPIOMode.SETUP_MENU:
            self.onLeftButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR_PAGE:

            self.resources.logger.addWarning(
                "IGNORING THIS CAPTURE " + self.idName + "_" + str(self.nbCapturesDone) + " " + str(
                    self.nbCapturesDone) + "/" + str(
                    self.nbCaptures))

            self.nbCaptures = self.nbCaptures - 1
            self.resources.logger.addInfo("REDUCE ASSEMBLY SIZE TO " + str(self.nbCaptures))

            if self.nbCapturesDone < self.nbCaptures:
                self.capture()

            elif self.nbCapturesDone == self.nbCaptures:
                self.buildShuffleAssembly()

            else:
                self.resources.logger.addWarning("ASSEMBLY SIZE = 0 -> GO HOME")
                self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.PRINTER_MAINTENANCE:
            # ignorer
            self.cancelNotCompletedJobs()
            self.enablePrinter()
            self.resources.logger.addWarning("ASSEMBLY SIZE = 0 -> GO HOME")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.PRINTING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.VALIDATING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.STYLISHING:
            self.buildShuffleAssembly()

        else:
            print("No valid mode selected " + str(int(self.currentGPIOMode)))


    def onDownButtonPressed(self):

        if self.interuptsConnected is False:
            return

        if self.currentGPIOMode == GPIOMode.WAITING:

            self.currentGPIOMode = GPIOMode.RUNNING
            self.startPictureAssembly()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.RUNNING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.MENU or self.currentGPIOMode == GPIOMode.SETUP_MENU:
            self.onDownButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR_PAGE:
            self.resources.logger.addWarning(
                "CANCELING THE WHOLE CAPTURES " + self.idName + " " + str(self.nbCapturesDone) + "/" + str(
                    self.nbCaptures))
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.PRINTER_MAINTENANCE:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.PRINTING:
            print("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.VALIDATING:

            self.nbCapturesDone = self.nbCapturesDone + 1
            if self.nbCapturesDone < self.nbCaptures:
                self.capture()
            else:
                self.buildShuffleAssembly()

        elif self.currentGPIOMode == GPIOMode.STYLISHING:
            self.selectedFilter += 1
            if self.selectedFilter >= 5:
                self.selectedFilter = 0
            self.showStylishingPage()

        else:
            print("No valid mode selected " + str(int(self.currentGPIOMode)))


    @pyqtSlot(int)
    def onInputButtonPressed(self, channel):

        if channel == 21:
            self.onRightButtonPressed()
        elif channel == 6:
            self.onLeftButtonPressed()
        elif channel == 26:
            self.onDownButtonPressed()


    def onRightButtonGPIO(self):

        print("go right")
        pyautogui.press('enter')


    def onLeftButtonGPIO(self):

        print("go lef")
        pyautogui.press('left')


    def onDownButtonGPIO(self):

        print("go bottom")
        pyautogui.press('down')


    def onShowMenu(self):

        self.currentGPIOMode = GPIOMode.MENU
        self.showPixmapMenu()
        self.switchLed(False, False, False)
        self.updateMenu()
        self.mainMenu.exec_(QPoint(500, 500))
        self.resources.getLogger().addInfo("SHOW MENU")
        self.switchLed(True, True, True)
        self.currentGPIOMode = GPIOMode.WAITING
        self.gotoStart()


    def initMenu(self):

        self.mainMenu = QMenu("Menu principal", self)
        self.mainMenuDevices = QMenu("Appareil photo / Flash", self)
        self.mainMenu.addAction(self.actionRestartCups)
        self.mainMenu.addAction(self.actionRestartSharingService)
        self.mainMenuDevices.addAction(self.actionEnableSpeedLight)
        self.mainMenuDevices.addAction(self.actionRestartSpeedLight)
        self.mainMenuDevices.addAction(self.actionRestartDSLR)
        self.mainMenu.addMenu(self.mainMenuDevices)
        self.mainMenu.addAction(self.actionShutdown)
        self.mainMenu.addAction(self.actionReboot)
        self.mainMenu.addAction(self.actionExit)


    def updateMenu(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        speedLightEnabled = settings.value("speedLightEnabled", True, bool)
        printingEnabled = settings.value("printingEnabled", True, bool)
        sharingEnabled = settings.value("sharingEnabled", True, bool)

        self.actionEnableSpeedLight.setChecked(speedLightEnabled)
        self.actionRestartSpeedLight.setVisible(speedLightEnabled)

        self.actionRestartSpeedLight.setVisible(speedLightEnabled)
        self.actionRestartCups.setVisible(printingEnabled)
        self.actionRestartSharingService.setVisible(sharingEnabled)

        if self.is_service_running("cups") == 0:
            self.actionRestartCups.setText("Redemarrer service impression (off)")
        else:
            self.actionRestartCups.setText("Redemarrer service impression (on)")

        if self.is_service_running("samba") == 0:
            self.actionRestartSharingService.setText("Redemarrer service partage (off)")
        else:
            self.actionRestartSharingService.setText("Redemarrer service partage (on)")

    def setImagequality0(self):
        subprocess.call("gphoto2 --set-config imagequality=0", shell=True)

    def setImagequality1(self):
        subprocess.call("gphoto2 --set-config imagequality=1", shell=True)

    def setImagequality2(self):
        subprocess.call("gphoto2 --set-config imagequality=2", shell=True)
    
    
    def setCP800Printer(self):
        self.printerName="Canon_CP800"
        
    def setCP760Printer(self):
        self.printerName="Canon_CP760"


    def initActions(self):
        
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.imagequality = settings.value("imagequality", 0, int)
        self.printerName = settings.value("printerName", "Canon_CP800")
                
        subprocess.call("gphoto2 --set-config imagequality=0", shell=True)

        self.actionImagequality0 = QAction("Low image quality (763ko) fast", self)
        self.actionImagequality0.triggered.connect(self.setImagequality0)
        
        self.actionImagequality1 = QAction("Medium image quality (1.1Mo) slow", self)
        self.actionImagequality1.triggered.connect(self.setImagequality1)
        
        self.actionImagequality2 = QAction("High image quality (2.5Mo) very slow", self)
        self.actionImagequality2.triggered.connect(self.setImagequality2)

        self.actionChooseCP800Printer = QAction("Use Canon Selphy CP800 as printer", self)
        self.actionChooseCP800Printer.triggered.connect(self.setCP800Printer)
        
        self.actionChooseCP760Printer = QAction("Use Canon Selphy CP760 as printer", self)
        self.actionChooseCP760Printer.triggered.connect(self.setCP760Printer)


        self.actionCleanUSBCaptures = QAction("Effacer toutes les photos de la memoire usb", self)
        self.actionCleanUSBCaptures.triggered.connect(self.cleanUSBCaptures)

        self.actionCleanLocalCaptures = QAction("Effacer toutes les photos de la memoire interne", self)
        self.actionCleanLocalCaptures.triggered.connect(self.cleanLocalCaptures)

        self.actionCleanUSBAssemblies = QAction("Effacer tous les assemblages de la memoire usb", self)
        self.actionCleanUSBAssemblies.triggered.connect(self.cleanUSBAssemblies)

        self.actionCleanAll = QAction("Effacer toutes les donnees", self)
        self.actionCleanAll.triggered.connect(self.cleanAll)

        self.actionEnableSpeedLight = QAction("Activer flash", self)
        self.actionEnableSpeedLight.setCheckable(True)
        self.actionEnableSpeedLight.triggered.connect(self.toogleEnableSpeedlight)

        self.actionRestartSpeedLight = QAction("Redemarrer flash", self)
        self.actionRestartSpeedLight.triggered.connect(self.restartSpeedLight)

        self.actionRestartDSLR = QAction("Redemarrer appareil photo", self)
        self.actionRestartDSLR.triggered.connect(self.restartDSLR)

        self.actionEnablePrinting = QAction("Activer", self)
        self.actionEnablePrinting.setCheckable(True)
        self.actionEnablePrinting.triggered.connect(self.toogleEnablePrinting)

        if self.is_service_running("cups") == 0:
            self.actionRestartCups = QAction("Redemarrer service impression (off)", self)
            self.actionStartCups = QAction("Demarrer service impression (off)", self)
            self.actionStopCups = QAction("Arreter service impression (off)", self)
        else:
            self.actionRestartCups = QAction("Redemarrer service impression (on)", self)
            self.actionStartCups = QAction("Demarrer service impression (on)", self)
            self.actionStopCups = QAction("Arreter service impression (on)", self)

        self.actionRestartCups.triggered.connect(self.restartCUPS)
        self.actionStartCups.triggered.connect(self.startCUPS)
        self.actionStopCups.triggered.connect(self.stopCUPS)

        if self.is_service_running("samba") == 0:
            self.actionRestartSharingService = QAction("Redemarrer service partage (off)", self)
            self.actionStartSharingService = QAction("Demarrer service partage (off)", self)
            self.actionStopSharingService = QAction("Arreter service partage (off)", self)
        else:
            self.actionRestartSharingService = QAction("Redemarrer service partage (on)", self)
            self.actionStartSharingService = QAction("Demarrer service partage (on)", self)
            self.actionStopSharingService = QAction("Arreter service partage (on)", self)

        self.actionRestartSharingService.triggered.connect(self.restartSamba)
        self.actionStartSharingService.triggered.connect(self.startSamba)
        self.actionStopSharingService.triggered.connect(self.stopSamba)

        self.actionEnableSharing = QAction("Activer", self)
        self.actionEnableSharing.setCheckable(True)
        self.actionEnableSharing.triggered.connect(self.toogleEnableSharing)

        self.actionShutdown = QAction("Arreter l'appareil", self)
        self.actionShutdown.triggered.connect(self.onShutdown)

        self.actionReboot = QAction("Redemarrer l'appareil", self)
        self.actionReboot.triggered.connect(self.onReboot)

        self.actionEnableInstrucions = QAction("Activer", self)
        self.actionEnableInstrucions.setCheckable(True)
        self.actionEnableInstrucions.triggered.connect(self.toogleEnableInstructions)

        self.actionGenerateSingleAssemblies = QAction("Creer tous les assemblages 1 photo", self)
        self.actionGenerateSingleAssemblies.triggered.connect(self.onGenerateAllSingleAssemblies)

        self.actionExit = QAction("<- Sortir du menu", self)


    def initAdvancedMenu(self):

        self.menu = QMenu("Menu principal", self)

        self.menuCleaning = QMenu("Donnees", self)
        self.menuDevices = QMenu("Appareil photo / flash", self)
        self.menuPrinters = QMenu("Impressions", self)
        self.menuSharing = QMenu("Partage", self)
        self.menuDisplay = QMenu("Affichage", self)
        self.menuInstructions = QMenu("Instructions", self)
        self.menuDisplay.addMenu(self.menuInstructions)
        self.menuSkin = QMenu("Themes", self)
        self.menuSetup = QMenu("Installation", self)
        self.menuFeatures = QMenu("Features", self)

        self.menuCleaning.addAction(self.actionCleanUSBCaptures)
        self.menuCleaning.addAction(self.actionCleanLocalCaptures)
        self.menuCleaning.addAction(self.actionCleanUSBAssemblies)
        self.menuCleaning.addAction(self.actionCleanAll)

        self.menuDevices.addAction(self.actionEnableSpeedLight)
        self.menuDevices.addAction(self.actionRestartSpeedLight)
        self.menuDevices.addAction(self.actionRestartDSLR)

        self.menuPrinters.addAction(self.actionEnablePrinting)
        self.menuPrinters.addAction(self.actionRestartCups)
        self.menuPrinters.addAction(self.actionStartCups)
        self.menuPrinters.addAction(self.actionStopCups)

        self.menuSharing.addAction(self.actionEnableSharing)
        self.menuSharing.addAction(self.actionRestartSharingService)
        self.menuSharing.addAction(self.actionStartSharingService)
        self.menuSharing.addAction(self.actionStopSharingService)

        self.menuInstructions.addAction(self.actionEnableInstrucions)

        self.menuSetup.addAction(self.actionShutdown)
        self.menuSetup.addAction(self.actionReboot)

        self.menuFeatures.addAction(self.actionGenerateSingleAssemblies)

        self.menu.addMenu(self.menuCleaning)
        self.menu.addMenu(self.menuDevices)
        self.menu.addMenu(self.menuPrinters)
        self.menu.addMenu(self.menuSkin)
        self.menu.addMenu(self.menuSharing)
        self.menu.addMenu(self.menuDisplay)
        self.menu.addMenu(self.menuSetup)
        self.menu.addMenu(self.menuFeatures)

        self.menu.addAction(self.actionExit)


    def updateAdvancedMenu(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        speedLightEnabled = settings.value("speedLightEnabled", True, bool)
        printingEnabled = settings.value("printingEnabled", True, bool)
        sharingEnabled = settings.value("sharingEnabled", True, bool)
        instructionsEnabled = settings.value("instructionsEnabled", True, bool)

        self.actionEnableSpeedLight.setChecked(speedLightEnabled)
        self.actionEnablePrinting.setChecked(printingEnabled)
        self.actionEnableSharing.setChecked(sharingEnabled)
        self.actionEnableInstrucions.setChecked(instructionsEnabled)

        self.actionRestartSpeedLight.setVisible(speedLightEnabled)

        self.actionRestartCups.setVisible(printingEnabled)
        self.actionStartCups.setVisible(printingEnabled)
        self.actionStopCups.setVisible(printingEnabled)

        self.actionRestartSharingService.setVisible(sharingEnabled)
        self.actionStartSharingService.setVisible(sharingEnabled)
        self.actionStopSharingService.setVisible(sharingEnabled)

        if self.is_service_running("samba") == 0:
            self.menuSharing.setTitle("Partage (off)")
        else:
            self.menuSharing.setTitle("Partage (on)")

        if self.is_service_running("cups") == 0:
            self.menuPrinters.setTitle("Impressions (off)")
        else:
            self.menuPrinters.setTitle("Impressions (on)")

        sizeCapturesUSB = self.resources.getDirectorySize(self.resources.PATH.CAPTURE_USB)
        sizeCapturesLocal = self.resources.getDirectorySize(self.resources.PATH.CAPTURE_LOCAL)
        sizeAssembliesUSB = self.resources.getDirectorySize(self.resources.PATH.ASSEMBLIES_USB)

        self.actionCleanLocalCaptures.setText(
            "Effacer toutes les photos de la memmoire interne (" + str("{:.2f}".format(sizeCapturesLocal)) + " MB)")
        self.actionCleanUSBCaptures.setText(
            "Effacer toutes les photos de la memmoire usb (" + str("{:.2f}".format(sizeCapturesUSB)) + " MB)")
        self.actionCleanUSBAssemblies.setText(
            "Effacer tous les assemblages de la memmoire usb (" + str("{:.2f}".format(sizeAssembliesUSB)) + " MB)")
        self.actionCleanAll.setText("Effacer toutes les donnees (" + str(
            "{:.2f}".format(sizeCapturesLocal + sizeCapturesUSB + sizeAssembliesUSB)) + " MB)")
        self.menuCleaning.setTitle(
            "Donnees (" + str("{:.2f}".format(sizeCapturesLocal + sizeCapturesUSB + sizeAssembliesUSB)) + " MB)")
        QApplication.processEvents()


    def showTriggerErrorPage(self):

        self.resources.getLogger().addError("TRIGGER CAPTURE ERROR")
        self.currentGPIOMode = GPIOMode.TRIGGER_ERROR_PAGE

        txt = "LA  PHOTO " + str(int(self.nbCapturesDone + 1)) + "/" + str(
            int(self.nbCaptures)) + " N'A  PAS  PU  ETRE  PRISE !"

        if self.nbCapturesDone + 1 == self.nbCaptures:
            txt = "LA  PHOTO  N'A  PAS  PU  ETRE  PRISE !"

        pix = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/onError.png")
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)
        x = 50
        y = 160
        r = QRectF(0, 0, 1180, 150)
        painter.setPen(QColor(160, 160, 160))
        painter.setFont(QFont("Right Chalk", 40))
        painter.translate(x, y)
        painter.drawText(r, txt)
        painter.translate(-x, -y)
        del painter
        self.label.setPixmap(pix)
        QApplication.processEvents()

        self.switchLed(True, True, True)
        self.connectInputButtonInterupts()
        QApplication.processEvents()


    def onShowAdvancedMenu(self):

        self.currentGPIOMode = GPIOMode.MENU
        self.showPixmapMenu()
        self.switchLed(False, False, False)
        self.updateAdvancedMenu()
        self.menu.exec_(QPoint(500, 500))

        self.resources.getLogger().addInfo("SHOW MENU")
        self.switchLed(True, True, True)
        self.currentGPIOMode = GPIOMode.WAITING
        self.gotoStart()


    def cleanUSBCaptures(self):

        self.resources.getLogger().addInfo("ERASE USB CAPTURES")
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB))


    def cleanLocalCaptures(self):

        self.resources.getLogger().addInfo("ERASE LOCAL CAPTURES")
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.CAPTURE_LOCAL))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.CAPTURE_LOCAL))


    def cleanAll(self):

        self.resources.getLogger().addInfo("ERASE ALL")
        self.cleanUSBAssemblies()
        self.cleanUSBCaptures()
        self.cleanLocalCaptures()


    def cleanUSBAssemblies(self):

        self.resources.getLogger().addInfo("ERASE USB ASSEMBLIES")
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES_USB))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES_USB))


    def toogleEnableSpeedlight(self):

        self.resources.getLogger().addInfo("ENABLE SPEEDLIGHT")
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        enable = not settings.value("speedLightEnabled", True, bool)
        settings.setValue("speedLightEnabled", enable)
        self.switchSpeedLight(enable)


    def restartSpeedLight(self):

        self.resources.getLogger().addInfo("RESTART SPEEDLIGHT")
        self.switchSpeedLight(False)
        time.sleep(2)
        self.switchSpeedLight(True)


    def restartDSLR(self):

        self.resources.getLogger().addInfo("RESTART DSLR")
        self.switchDSLR(False)
        time.sleep(2)
        self.switchDSLR(True)


    def initDevicesFast(self):
        self.switchDSLR(True)


    def initDevices(self):

        self.restartDSLR()
        QApplication.processEvents()
        self.restartSpeedLight()
        QApplication.processEvents()
        self.switchPrinter(True)
        QApplication.processEvents()
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.printingEnabled = settings.value("printingEnabled", True, bool)
        if self.printingEnabled is False:
            self.stopCUPS()
        else:
            self.startCUPS()

        self.sharingEnabled = settings.value("sharingEnabled", True, bool)
        if self.sharingEnabled is False:
            self.stopSamba()
        else:
            self.startSamba()


    def toogleEnablePrinting(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.printingEnabled = not settings.value("printingEnabled", True, bool)
        settings.setValue("printingEnabled", self.printingEnabled)
        if self.printingEnabled is False:
            self.stopCUPS()
        else:
            self.startCUPS()


    def restartCUPS(self):

        if EMULATE is True:
            return

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        en = settings.value("printingEnabled", True, bool)
        if en is True:
            subprocess.Popen(["/etc/init.d/cups", "restart"])
        else:
            subprocess.Popen(["/etc/init.d/cups", "stop"])


    def startCUPS(self):

        if EMULATE is True:
            return
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        en = settings.value("printingEnabled", True, bool)
        if en is True:
            subprocess.Popen(["/etc/init.d/cups", "start"])
        else:
            subprocess.Popen(["/etc/init.d/cups", "stop"])


    def stopCUPS(self):

        if EMULATE is True:
            return
        subprocess.Popen(["/etc/init.d/cups", "stop"])


    def toogleEnableSharing(self):

        if EMULATE is True:
            return
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        sharingEnabled = not settings.value("sharingEnabled", True, bool)
        settings.setValue("sharingEnabled", sharingEnabled)
        if sharingEnabled is False:
            self.stopSamba()
        else:
            self.startSamba


    def restartSamba(self):

        if EMULATE is True:
            return
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        en = settings.value("sharingEnabled", True, bool)
        if en is True:
            subprocess.Popen(["/etc/init.d/samba", "restart"])
        else:
            subprocess.Popen(["/etc/init.d/samba", "stop"])


    def startSamba(self):

        if EMULATE is True:
            return
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        en = settings.value("sharingEnabled", True, bool)
        if en is True:
            subprocess.Popen(["/etc/init.d/samba", "start"])
        else:
            subprocess.Popen(["/etc/init.d/samba", "stop"])


    def stopSamba(self):

        if EMULATE is True:
            return
        subprocess.Popen(["/etc/init.d/samba", "stop"])


    def onShutdown(self):

        self.showShutdownPixmap()
        self.resources.getLogger().addInfo("ARRET NORMAL DU PHOTOBOOTH")
        self.switchSpeedLight(False)
        self.switchDSLR(False)
        self.command("shutdown")


    def onReboot(self):

        self.showShutdownPixmap()
        self.resources.getLogger().addInfo("REDEMARRAGE NORMAL DU PHOTOBOOTH")
        self.switchSpeedLight(False)
        self.switchDSLR(False)
        self.command("reboot")


    def onGenerateAllSingleAssemblies(self):
        self.generateAllSingleAssemblies(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB),
                                         self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES_USB))


    def toogleEnableInstructions(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.instructionsEnabled = not settings.value("instructionsEnabled", True, bool)
        settings.setValue("instructionsEnabled", self.instructionsEnabled)


    def deleteAllMedias(self):

        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB))
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.CAPTURE_LOCAL))
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES_USB))

        os.mkdir(self.resources.getPath(ressourcesManager.PATH.CAPTURE_LOCAL))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES_USB))


    def is_service_running(self, name):

        if EMULATE is True:
            return 0
        with open(os.devnull, 'wb') as hide_output:
            exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()
            return exit_code == 0


    def command(self, cmd):

        if EMULATE is True:
            return
        commands = {"shutdown": "sudo shutdown -h now", "reboot": "sudo shutdown -r now"}
        subprocess.call(commands[cmd], shell=True)


    def initGPIO(self):

        if EMULATE is True:
            return
        # GPIO IN 20 wired

        GPIO.setup(self.GPIO_buttonRightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.GPIO_buttonRightLedPin, GPIO.OUT)
        self.buttonRightLedPWM = GPIO.PWM(self.GPIO_buttonRightLedPin, 150)
        self.buttonRightLedPWM.start(0)

        GPIO.setup(self.GPIO_buttonDownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.GPIO_buttonDownLedPin, GPIO.OUT)
        self.buttonDownLedPWM = GPIO.PWM(self.GPIO_buttonDownLedPin, 150)
        self.buttonDownLedPWM.start(0)

        GPIO.setup(self.GPIO_buttonLeftPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.GPIO_buttonLeftLedPin, GPIO.OUT)
        self.buttonLeftLedPWM = GPIO.PWM(self.GPIO_buttonLeftLedPin, 150)
        self.buttonLeftLedPWM.start(0)

        GPIO.setup(self.GPIO_POWER_SPEEDLIGHT, GPIO.OUT, initial=1)
        GPIO.setup(self.GPIO_ON_OFF_SPEEDLIGHT, GPIO.OUT, initial=1)
        GPIO.setup(self.GPIO_POWER_DSLR, GPIO.OUT, initial=0)
        GPIO.setup(self.GPIO_POWER_PRINTER, GPIO.OUT, initial=1)


    def switchPrinter(self, on):

        if EMULATE is True:
            return

        if on is True:

            GPIO.output(self.GPIO_POWER_PRINTER, 0)
            time.sleep(2)

        else:

            GPIO.output(self.GPIO_POWER_PRINTER, 1)
            time.sleep(2)


    def switchSpeedLight(self, on):

        if EMULATE is True:
            return

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        en = settings.value("speedLightEnabled", True, bool)

        if on is True and en is True:

            GPIO.output(self.GPIO_POWER_SPEEDLIGHT, 0)
            time.sleep(1)
            GPIO.output(self.GPIO_ON_OFF_SPEEDLIGHT, 0)
            time.sleep(2)
            GPIO.output(self.GPIO_ON_OFF_SPEEDLIGHT, 1)

        else:

            GPIO.output(self.GPIO_ON_OFF_SPEEDLIGHT, 0)
            time.sleep(2)
            GPIO.output(self.GPIO_ON_OFF_SPEEDLIGHT, 1)
            GPIO.output(self.GPIO_POWER_SPEEDLIGHT, 1)
            time.sleep(1)


    def switchDSLR(self, on):

        if EMULATE is True:
            return

        if on is True:
            GPIO.output(self.GPIO_POWER_DSLR, 0)
            time.sleep(1)
        else:
            GPIO.output(self.GPIO_POWER_DSLR, 1)
            time.sleep(1)


    # create a function to show last assembly after print success.
    def displayLastAssemblyPage(self):

        self.timerGoToStart.stop()
        self.currentGPIOMode = GPIOMode.DISPLAY_ASSEMBLY
        self.showAssemblyPixmap()
        self.switchLed(True, self.printingEnabled, True)
        self.connectInputButtonInterupts()
        QApplication.processEvents()
        self.timerGoToStart.start(120000)


    def goHomeCallback(self):
        print("go home call")
        self.timerGoToStart.stop()
        if self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            self.gotoStart()


    def redoAssembly(self):

        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)
        time.sleep(0.2)
        QApplication.processEvents()
        self.buildShuffleAssembly()
        self.switchLed(True, self.printingEnabled, True)
        self.connectInputButtonInterupts()
        QApplication.processEvents()


    def connectInputButtonInterupts(self):

        if self.interuptsConnected is False:
            self.inputButtonThread.inputButtonEventDetected.connect(self.onInputButtonPressed)
            self.interuptsConnected = True


    def disconnectInputButtonInterupts(self):

        if self.interuptsConnected is True:
            self.inputButtonThread.inputButtonEventDetected.disconnect(self.onInputButtonPressed)
            self.interuptsConnected = False


    def sendPrintingJob(self):

        if EMULATE is True:
            return
            
        if hideOutput is True:
            
            self.enablePrinter()
            #?self.cancelNotCompletedJobs()
            
            self.erasePrinterStatusBox()            
            conn = cups.Connection()
            self.resources.logger.addInfo("NEW JOB PRINT : " + self.currentAssemblyPath)
            conn.printFile(self.printerName, self.currentAssemblyPath, title='boxaselfi_job', options={})
            
            self.showPrintSentPage()
            QApplication.processEvents()
            QApplication.processEvents()
            QApplication.processEvents()
            time.sleep(2)
            
            self.switchLed(True, self.printingEnabled, True)
            QApplication.processEvents()
            self.connectInputButtonInterupts()
            self.displayLastAssemblyPage()
            
        else:

            self.timerGoToStart.stop()
            self.disconnectInputButtonInterupts()
            self.switchLed(False, False, False)
            self.currentGPIOMode = GPIOMode.PRINTING
            QApplication.processEvents()

            self.printJobStatusList = []
            start = time.time()
            current = start
            last = start
            conn = cups.Connection()
            printerName = 'Canon_CP800'
            # printerName = 'Canon_CP760'
            self.resources.logger.addInfo("NEW JOB PRINT : " + self.currentAssemblyPath)
            conn.printFile(printerName, self.currentAssemblyPath, title='boxaselfi_job', options={})
            # conn.printFile(printerName, "/home/pi/Documents/IMG_6473.JPG", title='boxaselfi_job', options={})
            # conn.printFile(printerName, "/home/pi/Documents/IMG_6507.JPG", title='boxaselfi_job', options={})
            percentPrint = 0
            percentage = 0

            self.showPrintingPage(percentPrint)
            QApplication.processEvents()

            while (time.time() - start < self.printDuration):

                percentage = (1 - (time.time() - start) / self.printDuration) * 100

                if time.time() - last > 2:
                    # each 2 seconds...

                    conn = cups.Connection()
                    printers = conn.getPrinters()
                    self.fillPrinterStatusBox(percentage, printers[self.printerName]["printer-state-message"])
                    self.resources.logger.addInfo(json.dumps(printers))

                    if printers[self.printerName]['printer-state'] == 5:

                        if printers[self.printerName]["printer-state-message"] == "No paper tray loaded, aborting!":
                            print("no paper tray")

                            self.erasePrinterStatusBox()
                            self.resources.logger.addError("JOB PRINT STATUS : No paper tray loaded, aborting!")
                            self.showNoPaperTrayPage()
                            return

                    if printers[self.printerName]['printer-state'] == 3:

                        if printers[self.printerName]["printer-state-message"] == "Ribbon depleted!":
                            self.erasePrinterStatusBox()
                            self.resources.logger.addError("JOB PRINT STATUS : Ribbon depleted!")
                            self.showChangeCartridgePage()
                            return
                        if printers[self.printerName]["printer-state-message"] == "Paper feed problem!":
                            self.erasePrinterStatusBox()
                            self.resources.logger.addError("JOB PRINT STATUS : Paper feed problem!")
                            self.showChangeCartridgePage()
                            return

                    last = time.time()

                current = time.time() - start
                if current <= 25 * self.printDuration / 100 and percentPrint != 0:
                    percentPrint = 0
                    self.showPrintingPage(percentPrint)

                elif current > 25 * self.printDuration / 100 and current <= 50 * self.printDuration / 100 and percentPrint != 1:
                    percentPrint = 1
                    self.showPrintingPage(percentPrint)

                elif current > 50 * self.printDuration / 100 and current <= 75 * self.printDuration / 100 and percentPrint != 2:
                    percentPrint = 2
                    self.showPrintingPage(percentPrint)

                elif current > 75 * self.printDuration / 100 and current <= 90 * self.printDuration / 100 and percentPrint != 3:
                    percentPrint = 3
                    self.showPrintingPage(percentPrint)
                elif current > 90 * self.printDuration / 100 and current <= 100 * self.printDuration / 100 and percentPrint != 4:
                    percentPrint = 4
                    self.showPrintingPage(percentPrint)

            self.erasePrinterStatusBox()
            self.switchLed(True, self.printingEnabled, True)
            QApplication.processEvents()
            self.connectInputButtonInterupts()
            self.displayLastAssemblyPage()

    def showPrintSentPage(self):       
        self.currentGPIOMode = GPIOMode.PRINTING
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/printingSent.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()


    def showPrintingPage(self, percentPrint):

        filename = "tt"
        if percentPrint == 0:
            filename = "printing_5.png"
        elif percentPrint == 1:

            filename = "printing_25.png"
        elif percentPrint == 2:
            filename = "printing_50.png"
        elif percentPrint == 3:
            filename = "printing_75.png"
        elif percentPrint == 4:
            filename = "printing_100.png"
        print(filename)
        basePixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/printing.png")
        printingOverlayPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/" + filename)

        painter = QPainter(basePixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.showPrintingStatusEnabled is True:

            painter.translate(200, 0)
            painter.drawPixmap(0, 0, printingOverlayPixmap)
            painter.translate(-200, 0)
            printingStatusPixmap = QPixmap(
                self.resources.getPath(ressourcesManager.PATH.PAGE) + "/printing_boxStatus.png")
            painter.drawPixmap(0, 0, printingStatusPixmap)

        else:

            painter.drawPixmap(0, 0, printingOverlayPixmap)

        del painter
        self.basePrintingPixmap = basePixmap.copy()
        self.label.setPixmap(basePixmap)
        QApplication.processEvents()


    def fillPrinterStatusBox(self, percentage, status):

        pixCopy = self.basePrintingPixmap.copy()
        painter = QPainter(pixCopy)
        painter.setRenderHint(QPainter.Antialiasing)

        if len(self.printJobStatusList) > 0 and self.printJobStatusList[-1] != status:
            self.printJobStatusList.append(status)
            self.resources.logger.addInfo("JOB PRINT STATUS : " + status)

        if len(self.printJobStatusList) == 0:
            self.printJobStatusList.append(status)
            self.resources.logger.addInfo("JOB PRINT STATUS : " + status)

        if self.showPrintingStatusEnabled is True:

            x = 700
            y = 475
            r = QRectF(0, 0, 350, 50)
            painter.setPen(Qt.white)
            painter.setFont(QFont("DejaVu Sans", 30))
            painter.translate(700, 400)
            painter.drawText(r, "{:.0f}".format(100 - percentage) + " % : ")
            painter.translate(-700, -400)

            painter.setFont(QFont("DejaVu Sans", 10))
            for i in range(3):
                if len(self.printJobStatusList) >= 3 - i:
                    painter.translate(x, y)
                    painter.drawText(r, "> " + self.printJobStatusList[-(3 - i)])
                    painter.translate(-x, -y)
                    y = y + 30

        else:

            x = 800
            y = 475
            r = QRectF(0, 0, 350, 50)
            painter.setPen(Qt.white)
            painter.setFont(QFont("DejaVu Sans", 30))
            painter.translate(800, 400)
            painter.drawText(r, "{:.0f}".format(100 - percentage) + " % : ")
            painter.translate(-800, -400)

        del painter
        self.label.setPixmap(pixCopy)
        QApplication.processEvents()


    def erasePrinterStatusBox(self):

        self.resources.logger.addInfo("JOB PRINT STATUS : CLEANING THE LIST")
        self.printJobStatusList = []


    def showNoPaperTrayPage(self):

        self.currentGPIOMode = GPIOMode.PRINTER_MAINTENANCE
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/noTray.png")
        self.label.setPixmap(outPixmap)
        self.switchLed(True, True, False)
        self.connectInputButtonInterupts()
        QApplication.processEvents()


    def showAddPaperPage(self):

        self.currentGPIOMode = GPIOMode.PRINTER_MAINTENANCE
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/noMorePaper.png")
        self.label.setPixmap(outPixmap)
        self.switchLed(True, True, False)
        self.connectInputButtonInterupts()
        QApplication.processEvents()


    def showChangeCartridgePage(self):

        self.currentGPIOMode = GPIOMode.PRINTER_MAINTENANCE
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/noMoreInk.png")
        self.label.setPixmap(outPixmap)
        self.switchLed(True, True, False)
        self.connectInputButtonInterupts()
        QApplication.processEvents()


    def gotoStart(self, index=1):

        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)
        self.showGoHomePixmap()
                
        # start Thread that create copy and erase local captures

        self.resources.logger.addInfo("SAVE LOCAL FILES PROCESS STARTED")

        # saveThread = SaveToUSB(self.resources.getPath(
        # ressourcesManager.PATH.CAPTURE_LOCAL), self.resources.getPath(
        # ressourcesManager.PATH.CAPTURE_USB), self.idName, self.nbCapturesDone)
        # saveThread.start()

        saver = SaveToUSBClass(self.resources.getPath(
            ressourcesManager.PATH.CAPTURE_LOCAL), self.resources.getPath(
            ressourcesManager.PATH.CAPTURE_USB), self.idName, self.nbCapturesDone)
        saver.save()

        self.nbCapturesDone = 0
        self.idName = ""
        self.nbCaptures = index

        self.resources.logger.addInfo("GO HOME")
        self.currentGPIOMode = GPIOMode.WAITING
        self.switchLed(True, True, True)
        self.connectInputButtonInterupts()

        self.setPhotoBoothMode(self.nbCaptures)


    def increaseNbPhoto(self):

        self.nbCaptures += 1
        if self.nbCaptures > self.nbCapturesMax:
            self.nbCaptures = 1
        self.setPhotoBoothMode(self.nbCaptures)


    def decreaseNbPhoto(self):

        self.nbCaptures -= 1
        if self.nbCaptures < 1:
            self.nbCaptures = self.nbCapturesMax
        self.setPhotoBoothMode(self.nbCaptures)


    def setPhotoBoothMode(self, index):
        
        self.label.setMovie(self.movie)
        self.movie.start()
        return

        self.pixmap_mode_0 = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/m0.png")

        if index == 1:
            currentModePixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/m1.png")
        if index == 2:
            currentModePixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/m2.png")
        if index == 3:
            currentModePixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/m3.png")
        if index == 4:
            currentModePixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/m4.png")

        painter = QPainter(self.pixmap_mode_0)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.instructionsEnabled is True:
            pix = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/m7.png")
            painter.drawPixmap(0, 0, pix)

        painter.drawPixmap(0, 0, currentModePixmap)
        del painter
        self.label.setPixmap(self.pixmap_mode_0)
        QApplication.processEvents()


    def switchLed(self, Right, Left, Downn):

        self.setButtonRightLedEnabled(Right)
        self.setButtonLeftLedEnabled(Left)
        self.setButtonDownLedEnabled(Downn)
        QApplication.processEvents()


    def setButtonRightLedEnabled(self, enabled):

        self.buttonRightLedEnabled = enabled


    def setButtonLeftLedEnabled(self, enabled):

        self.buttonLeftLedEnabled = enabled


    def setButtonDownLedEnabled(self, enabled):

        self.buttonDownLedEnabled = enabled


    def contextMenuEvent(self, event):

        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            self.onShowAdvancedMenu()
        else:
            self.onShowMenu()


    def keyReleaseEvent(self, e):

        if e.key() == Qt.Key_Plus:
            self.onRightButtonPressed()
        if e.key() == Qt.Key_Minus:
            self.onLeftButtonPressed()
        if e.key() == Qt.Key_Space:
            self.onDownButtonPressed()


    def closeEvent(self, event):
        event.ignore()
        exit(140)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    ret = app.exec_()
    if EMULATE is False:
        GPIO.cleanup()
    sys.exit(ret)
