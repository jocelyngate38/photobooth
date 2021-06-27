#!/usr/bin/env python

import os
os.environ['DISPLAY'] = ':0'

try:
    from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QRectF, QSettings, QSize, QUrl,
                              Qt, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QDateTime, QIODevice,
                              QElapsedTimer)
    from PyQt5.QtGui import QIcon, QKeySequence, QFont, QPixmap, QPainter, QPen, QColor, QMovie
    from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow,QToolTip)
    # from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
    # from PyQt5.QtMultimediaWidgets import QVideoWidget
except:
    print("PyQt5 import error")

try:
    import platform

    if platform.system() == 'Windows':
        EMULATE = True
    else:
        EMULATE = False
        try:
            import RPi.GPIO as GPIO
        except:
            print("GPIO import error")
        try:
            import cups
        except:
            print("cups import error")
        try:
            import serial
        except:
            print("import serial error")
except:
    print("platform import error")

try:
    import pyautogui
except:
    print("pyautogui import error")

try:
    from random import randint, randrange
except:
    print("randint, randrange import error")

try:
    from datetime import datetime
except:
    print("datetime import error")
try:
    from ressourceManager import *
except:
    print("ressourceManager import error")
try:
    from six.moves.queue import Queue
except:
    print("Queue import error")
try:
    import threading, time, random, shutil, os, subprocess
except:
    print("threading, time, random, shutil, os, subprocess import error")
try:
    import glob
except:
    print("glob import error")
try:
    import json
except:
    print("json import error")
try:
    from subprocess import Popen, PIPE, check_output
except:
    print("Popen, PIPE, check_output import error")
try:
    import uuid
except:
    print("uuid import error")
try:
    from enum import Enum, IntEnum
except:
    print("Enum import error")



try:
    from PIL import Image
except:
    print("import Image from PIL error")


class PhotoBoothSettings():

    def has_external_flash(self):
        pass

    def has_constant_light(self):
        pass

    def can_restart_DSLR(self):
        pass

    def can_restart_external_flash(self):
        pass

    class GPIOPin(IntEnum):
        pass

    def getCameraName(self):
        pass

    def getScreenResolution(self):
        pass


class PhotoBooth_1(PhotoBoothSettings):
    def has_external_flash(self):
        return False

    def has_constant_light(self):
        return True

    def can_restart_DSLR(self):
        return False

    def can_restart_external_flash(self):
        return False

    class GPIOPin(IntEnum):
        LED_BUTTON_1 = 6
        LED_BUTTON_2 = 26
        LED_BUTTON_3 = 13
        LED_0 = 19

        BUTTON_1 = 20
        BUTTON_2 = 16
        BUTTON_3 = 12
        BUTTON_4 = 21

        RELAY_POWER_TOP_LIGHT = 17
        RELAY_LED_STRIP = 4
        RELAY_2 = 23
        RELAY_3 = 22

        WIRE_3_4 = 23
        WIRE_3_5 = 24
        WIRE_3_6 = 25

    def getCameraName(self):
        return "Nikon DSC D3200"
        # camera = "Nikon DSC D70s (PTP mode)"

    def getScreenResolution(self):
        return 1280, 1024


class PhotoBooth_2(PhotoBoothSettings):
    def has_external_flash(self):
        return True

    def has_constant_light(self):
        return True

    def can_restart_DSLR(self):
        return True

    def can_restart_external_flash(self):
        return True

    class GPIOPin(IntEnum):
        LED_BUTTON_1 = 13
        LED_BUTTON_2 = 26
        LED_BUTTON_3 = 6
        LED_0 = 19

        BUTTON_1 = 20
        BUTTON_2 = 16
        BUTTON_3 = 12
        BUTTON_4 = 21

        RELAY_POWER_TOP_LIGHT = 22
        RELAY_LED_STRIP = 4
        RELAY_2 = 22
        RELAY_3 = 22

        POWER_SPEEDLIGHT = 17
        ON_OFF_SPEEDLIGHT = 23
        POWER_DSLR = 4

    def getCameraName(self):
        return "Nikon DSC D70s (PTP mode)"

    def getScreenResolution(self):
        return 1024, 800


PHOTOBOOTH_2 = False
DebugGPIO = False
MAX_SERIAL_RETRY = 4

HAS_EXTERNAL_FLASH = False
HAS_CONSTANT_LIGHT = True

photoBooth = PhotoBooth_1()

if PHOTOBOOTH_2 is True:
    photoBooth = PhotoBooth_2()
    HAS_EXTERNAL_FLASH = True
    HAS_CONSTANT_LIGHT = True

photoBooth = PhotoBooth_2()


class ColorLED():
    BLUE = [0, 0, 255]
    GREEN = [0, 255, 0]
    RED = [255, 0, 0]
    LIGHT_BLUE = [0, 180, 180]
    WHITE = [255, 255, 255]
    ORANGE = [255, 180, 0]
    BLACK = [0, 0, 0]


if PHOTOBOOTH_2 is False:

    class GPIOPin(IntEnum):

        LED_BUTTON_1 = 6
        LED_BUTTON_2 = 26
        LED_BUTTON_3 = 13
        LED_0 = 19

        BUTTON_1 = 20
        BUTTON_2 = 16
        BUTTON_3 = 12
        BUTTON_4 = 21

        RELAY_POWER_TOP_LIGHT = 17
        RELAY_LED_STRIP = 4
        RELAY_2 = 23
        RELAY_3 = 22

        WIRE_3_4 = 23
        WIRE_3_5 = 24
        WIRE_3_6 = 25

else:

    class GPIOPin(IntEnum):

        LED_BUTTON_1 = 13
        LED_BUTTON_2 = 26
        LED_BUTTON_3 = 6
        LED_0 = 19

        BUTTON_1 = 20
        BUTTON_2 = 16
        BUTTON_3 = 12
        BUTTON_4 = 21

        RELAY_POWER_TOP_LIGHT = 22
        RELAY_LED_STRIP = 4
        RELAY_2 = 22
        RELAY_3 = 22

        # WIRE_3_4 = 23
        # WIRE_3_5 = 24
        # WIRE_3_6 = 25

        POWER_SPEEDLIGHT = 17
        ON_OFF_SPEEDLIGHT = 23
        POWER_DSLR = 4


class GPIOMode(Enum):
    HOMEPAGE = 1
    PRINT = 2
    MENU = 3
    MENU_SETUP = 4
    COMPUTING = 5
    VALIDATE = 6
    DISPLAY_ASSEMBLY = 7
    TRIGGER_ERROR = 8
    RUNNING = 9
    POWER_PRINTER = 10
    INFO_SHUTDOWN = 11
    INFO_MENU = 12
    INFO_MENU_ADVANCED = 13
    INFO_REPRINT = 14
    INFO_SWITCH_CONSTANT_LIGHT = 15
    UNDEFINED = 255


if EMULATE is False:
    GPIO.setmode(GPIO.BCM)


class PrinterMonitoringThread(QThread):
    printerFailure = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    label = None

    def __init__(self, label, led, printerName):
        QThread.__init__(self, label)
        self.label = label
        self.led = led
        self.printerName = printerName
        # run method gets called when we start the thread

    def changePrinterName(self, printerName):
        self.printerName = printerName

    def run(self):
        while True:
            if EMULATE is False:
                try:
                    conn = cups.Connection()
                    printers = conn.getPrinters()
                    for printer in printers:

                        if printers[printer]['printer-state'] == 5:
                            if printers[printer]["printer-state-message"] == "No paper tray loaded, aborting!":
                                self.ressourceManager.getLogger().addWarning("NO MORE PAPER, CONTACT SMBDY TO ADD PAPERS AGAIN")
                                self.printerFailure.emit(printer, 1)
                                self.label.setTrayMissingLeft(True)
                                self.label.setTrayMissingRight(True)
                                self.led.showWarning(1)

                        if printers[printer]['printer-state'] == 3:
                            if printers[printer]["printer-state-message"] == "Ribbon depleted!":
                                self.ressourceManager.getLogger().addWarning("CARTOUCHE D'ENCRE VIDE, CONTACT SMBDY TO ADD PAPERS AGAIN")
                                self.printerFailure.emit(printer, 2)
                                self.label.setRibbonEmptyLeft(True)
                                self.label.setRibbonEmptyRight(True)
                                self.led.showWarning(1)

                            if printers[printer]["printer-state-message"] == "Paper feed problem!":
                                self.ressourceManager.getLogger().addWarning("PLUS DE PAPIER, VEUILLEZ EN RAJOUTER")
                                self.printerFailure.emit(printer, 3)
                                self.label.setPaperEmptyLeft(True)
                                self.label.setPaperEmptyRight(True)
                                self.led.showWarning(1)
                except cups.IPPError as e:
                    self.ressourceManager.getLogger().addError("CUPS.IPPERROR " + str(e))
                except RuntimeError as e1:
                    self.ressourceManager.getLogger().addError("RUNTIMEERROR " + str(e1))
                    break
            time.sleep(2)
            self.label.update()


class InputButtonThread(QThread):
    inputButtonEventDetected = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.queue = Queue()
        if EMULATE is False:
            GPIO.add_event_detect(GPIOPin.BUTTON_1, GPIO.FALLING, callback=self.queue.put, bouncetime=500)
            GPIO.add_event_detect(GPIOPin.BUTTON_3, GPIO.FALLING, callback=self.queue.put, bouncetime=500)
            GPIO.add_event_detect(GPIOPin.BUTTON_2, GPIO.FALLING, callback=self.queue.put, bouncetime=500)
        # GPIO 20 wired also

    def run(self):
        while True:
            self.inputButtonEventDetected.emit(self.queue.get())


class CaptureImageThread(QThread):
    signal = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, path, ressourceManager):
        QThread.__init__(self)
        self.capture = path
        self.ressourceManager = ressourceManager
    # run method gets called when we start the thread

    def getCameraName(self):
        if PHOTOBOOTH_2 is False:
            return "Nikon DSC D3200"
        else:
            return "Nikon DSC D70s (PTP mode)"

    def run(self):

        self.ressourceManager.getLogger().addInfo("CAPTURE REQUEST")


        if EMULATE is True:
            self.ressourceManager.getLogger().addInfo("IMAGE CAPTURED : " + self.capture)
            time.sleep(1)
            Original_Image = Image.open(self.ressourceManager.getPath(self.ressourceManager.PATH.CALIBRATION_IMAGE))
            Original_Image.save(self.capture)
            self.signal.emit(True, self.capture)
            return

        camera = self.getCameraName()

        p = Popen(["gphoto2", "--camera", camera, "--capture-image-and-download",
                   "--filename=" + self.capture], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode

        if len(err) > 0:
            self.ressourceManager.getLogger().addError(str(err))
            self.signal.emit(False, None)
        else:
            self.ressourceManager.getLogger().addInfo( "IMAGE CAPTURED : " + self.capture)
            if PHOTOBOOTH_2 is True:
                Original_Image = Image.open(self.capture)
                rotated_image1 = Original_Image.rotate(180)
                Original_Image.close()
                rotated_image1.save(self.capture)

            self.signal.emit(True, self.capture)





# class Menu(QMenu):
#
#     def __init__(self, path, parent=None):
#         super(Menu, self).__init__(parent=parent)
#
#     def event(self,e):
#
#         if activeAction() is not None :
#               QToolTip::showText(helpEvent->globalPos(), activeAction()->toolTip());
#
#         super().event(e)


class Label(QLabel):

    ribbonEmptyRight = False
    trayMissingRight = False
    paperEmptyRight = False
    ribbonEmptyLeft = False
    trayMissingLeft = False
    paperEmptyLeft = False

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

    def __init__(self, path, parent=None):
        super(Label, self).__init__(parent=parent)
        self.path = path

    def paintEvent(self, e):

        iL = 0
        jL = 0
        iR = 1280 - 229
        jR = 0
        incw = 0
        inch = 85

        super().paintEvent(e)
        qp = QPainter(self)
        if self.ribbonEmptyLeft is True:
            qp.drawPixmap(iL, jL, QPixmap(self.path + "/ribbonEmpty.png"))
            iL = iL + incw
            jL = jL + inch
        if self.trayMissingLeft is True:
            qp.drawPixmap(iL, jL, QPixmap(self.path + "/trayMissing.png"))
            iL = iL + incw
            jL = jL + inch
        if self.paperEmptyLeft is True:
            qp.drawPixmap(iL, jL, QPixmap(self.path + "/paperEmpty.png"))

        if self.ribbonEmptyRight is True:
            qp.drawPixmap(iR, jR, QPixmap(self.path + "/ribbonEmpty.png"))
            iR = iR + incw
            jR = jR + inch
        if self.trayMissingRight is True:
            qp.drawPixmap(iR, jR, QPixmap(self.path + "/trayMissing.png"))
            iR = iR + incw
            jR = jR + inch
        if self.paperEmptyRight is True:
            qp.drawPixmap(iR, jR, QPixmap(self.path + "/paperEmpty.png"))


class ledControler():
    serialDevice = None

    class LEDLocation(Enum):

        RIGHT_SIDE = 1
        LEFT_SIDE = 2
        BOTH_SIDE = 3
        TEXT_BACK = 4
        CAMERA_ARROWS = 5
        CAMERA_BACK = 6
        ERROR = 7

    def __init__(self, port, speed, ressourceManager):

        self.ressourceManager = ressourceManager
        if EMULATE is True:
            self.ressourceManager.getLogger().addInfo("INITIALIZING LEDCONTROLER")
            return

        self.port = port
        self.speed = speed
        self.init()

    def init(self):
        try:
            self.serialDevice = serial.Serial(self.port)
            self.serialDevice.baudrate = self.speed
        except:
            self.ressourceManager.getLogger().addError("LEDCONTROLER:SERIALDEVICE INIT EXCEPTION")

    def sendCommand(self, command, retryMax):

        if EMULATE is True:
            return

        retry = retryMax - 1
        exception = False

        if retry < 0:
            self.ressourceManager.getLogger().addError("LEDCONTROLER:TOO MUCH EXCEPTION IN SENDCOMMAND " + command)
            return

        try:
            self.serialDevice.write((command).encode('utf-8'))
        except serial.SerialException as e:
            self.ressourceManager.getLogger().addError("LEDCONTROLER:SENDCOMMAND:SERIAL.SERIALEXCEPTION " + str(e) + " command : " + command)
            exception = True
        except TypeError as e:
            self.ressourceManager.getLogger().addError("LEDCONTROLER:SENDCOMMAND:SERIAL.TYPEERROR " + str(e) + " command : " + command)
            exception = True
        except AttributeError as e:
            self.ressourceManager.getLogger().addError("LEDCONTROLER:SENDCOMMAND:SERIAL.ATTRIBUTEERROR " + str(e) + " command : " + command)
            exception = True

        if exception is True:
            self.init()
            self.sendCommand(command, retry)

    def blinkFront(self, ms):
        self.ressourceManager.getLogger().addInfo("LEDCONTROLER:BLINKFRONT")
        self.sendCommand('4,' + str(ms) + ';', MAX_SERIAL_RETRY)

    def setColor(self, location, colors):
        self.ressourceManager.getLogger().addInfo("LEDCONTROLER:SETCOLOR " + str(location) + str(colors))
        if location == self.LEDLocation.RIGHT_SIDE:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('6,' + str(r) + ',' + str(g) + ',' + str(b) + ';', MAX_SERIAL_RETRY)
        if location == self.LEDLocation.LEFT_SIDE:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('7,' + str(r) + ',' + str(g) + ',' + str(b) + ';', MAX_SERIAL_RETRY)
        if location == self.LEDLocation.CAMERA_ARROWS:
            r1 = colors[0][0]
            g1 = colors[0][1]
            b1 = colors[0][2]
            r2 = colors[1][0]
            g2 = colors[1][1]
            b2 = colors[1][2]
            self.sendCommand(
                '5,' + str(r1) + ',' + str(g1) + ',' + str(b1) + ',' + str(r2) + ',' + str(g2) + ',' + str(b2) + ';',
                MAX_SERIAL_RETRY)

        if location == self.LEDLocation.CAMERA_BACK:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('9,' + str(r) + ',' + str(g) + ',' + str(b) + ';', MAX_SERIAL_RETRY)

        if location == self.LEDLocation.TEXT_BACK:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('8,' + str(r) + ',' + str(g) + ',' + str(b) + ';', MAX_SERIAL_RETRY)

        if location == self.LEDLocation.BOTH_SIDE:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('6,' + str(r) + ',' + str(g) + ',' + str(b) + ';', MAX_SERIAL_RETRY)
            self.sendCommand('7,' + str(r) + ',' + str(g) + ',' + str(b) + ';', MAX_SERIAL_RETRY)

        if location == self.LEDLocation.ERROR:
            r1 = colors[0][0]
            g1 = colors[0][1]
            b1 = colors[0][2]
            r2 = colors[1][0]
            g2 = colors[1][1]
            b2 = colors[1][2]
            self.sendCommand(
                '11,' + str(r1) + ',' + str(g1) + ',' + str(b1) + ',' + str(r2) + ',' + str(g2) + ',' + str(b2) + ';',
                MAX_SERIAL_RETRY)

    def showWarning(self, isDefault):
        self.ressourceManager.getLogger().addInfo("LEDCONTROLER:SHOWDEFAULT " + str(isDefault))
        if isDefault == 1:
            self.setBrightness(255)
        else:
            self.setBrightness(180)
        self.sendCommand('10,' + str(isDefault) + ';', MAX_SERIAL_RETRY)

    def restart(self):
        self.ressourceManager.getLogger().addInfo("LEDCONTROLER:RESTART")
        self.sendCommand('3;', MAX_SERIAL_RETRY)

    def setBrightness(self, brightness):
        self.ressourceManager.getLogger().addInfo("LEDCONTROLER:SETBRIGHTNESS")
        self.sendCommand('12,' + str(brightness) + ';', MAX_SERIAL_RETRY)


if EMULATE is False:
    pyautogui.FAILSAFE = False

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.interuptsConnected = False
        self.currentAssemblyPath = ""
        self.currentGPIOMode = GPIOMode.HOMEPAGE
        self.timeoutTimer = None

        self.captureList = []
        self.lastAssemblyPixmap = None
        self.inputButtonThread = None
        self.movie = None
        self.label = None
        self.resources = None

        self.printingEnabled = False

        self.resources = ressourcesManager()
        self.resources.loadResources()
        self.resources.logInfos()
        self.resources.getLogger().addInfo("INITIALIZING PHOTOBOOTH")

        # DSLR SETTINGS
        self.Wcapture = 3008
        self.Hcapture = 2000

        self.blinkState = 0

        self.buttonDownLedEnabled = True
        self.buttonRightLedEnabled = True
        self.buttonLeftLedEnabled = True

        self.topLightOn = False
        self.lastPrintId = 0

        # PHOTOBOOTH SETTINGS
        self.screenWidth = 1024
        self.screenHeight = 800

        self.lastAssemblyLandscape = 1
        self.countDown = 4

        self.setCurrentMode(GPIOMode.UNDEFINED)

        self.initGPIO()

        self.led = ledControler("/dev/ttyUSB_LED_CONTROLLER", 115200, self.resources)

        self.led.setColor(ledControler.LEDLocation.RIGHT_SIDE, [ColorLED.LIGHT_BLUE])
        self.led.setColor(ledControler.LEDLocation.LEFT_SIDE, [ColorLED.LIGHT_BLUE])
        self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS, [ColorLED.BLACK, ColorLED.WHITE])
        self.led.setColor(ledControler.LEDLocation.CAMERA_BACK, [ColorLED.RED])
        self.led.setColor(ledControler.LEDLocation.TEXT_BACK, [ColorLED.LIGHT_BLUE])
        self.led.setColor(ledControler.LEDLocation.ERROR, [ColorLED.RED, ColorLED.BLACK])

        self.led.showWarning(1)

        if EMULATE is True:
            self.show()
        else:
            self.showFullScreen()
        self.initGUI()

        self.showStartupPixmap()
        self.switchLed(False, False, False)

        self.initSettings()
        self.initDevices()
        self.initActions()
        self.initMenu()
        self.initDSLRTime()

        self.printerMonitoring = PrinterMonitoringThread(self.label, self.led, self.printerName)
        self.printerMonitoring.start()

        self.showPowerOnPrinter()
        self.switchConstantLight(False)

    def initDSLRTime(self):

        self.resources.logger.addInfo("INITIALIZING DSLR DATETIME")

        if EMULATE is True:
            return

        subprocess.call("gphoto2 --set-config datetime=$(date +%s)", shell=True)

    def defineTimeout(self, delaySec):

        if delaySec <= 0:
            self.resources.getLogger().addInfo("REMOVING TIMEOUT")
            self.timeoutTimer.stop()
        else:
            self.timeoutTimer.start(1000 * delaySec)
            self.resources.getLogger().addInfo("SETTING TIMEOUT TO " + str(delaySec) + " SECONDES")

    def initSettings(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.printingEnabled = settings.value("printingEnabled", self.printingEnabled, bool)
        self.printer1 = "CP800"
        self.printer2 = "CP760"
        self.printer3 = "CP910"

    def initGUI(self):

        self.label = Label(self.resources.getPath(ressourcesManager.PATH.APPLICATION) + "/resources/skins/default/")

        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        self.label.setMinimumSize(self.screenWidth, self.screenHeight)
        self.label.setMaximumSize(self.screenWidth, self.screenHeight)

        self.setCentralWidget(self.label)
        self.cacheHomePicture()


        self.timeoutTimer = QTimer()
        self.timeoutTimer.timeout.connect(self.onTimeout)

    def cacheHomePicture(self):
        #used to speedup go home
        self.homeDisplay = self.resources.getPath(
            ressourcesManager.PATH.EVENT) + "/" + self.resources.homePageDisplayFilename

        self.movie = None
        if self.homeDisplay.endswith(('.gif')):
            self.movie = QMovie(self.homeDisplay)
            self.movie.setCacheMode(QMovie.CacheAll)
            self.movie.loopCount()

    def setCurrentMode(self, mode):

        if self.currentGPIOMode == mode:
            self.resources.getLogger().addWarning(
                "CHANGING CURRENT MODE TO THE SAME MODE " + mode.name + "(" + str(mode.value) + ")")
        else:
            self.resources.getLogger().addInfo(
                "CHANGING CURRENT MODE " + self.currentGPIOMode.name + "(" + str(
                    self.currentGPIOMode.value) + ") to mode " + mode.name + "(" + str(mode.value) + ")")

        self.currentGPIOMode = mode

        if mode == GPIOMode.HOMEPAGE:
            self.defineTimeout(-1)

        elif mode == GPIOMode.PRINT:
            self.defineTimeout(-1)

        elif mode == GPIOMode.MENU:
            self.defineTimeout(-1)
            self.defineTimeout(40)

        elif mode == GPIOMode.POWER_PRINTER:
            self.defineTimeout(-1)
            self.defineTimeout(60 * 5)

        elif mode == GPIOMode.MENU_SETUP:
            self.defineTimeout(-1)
            self.defineTimeout(40)

        elif mode == GPIOMode.COMPUTING:
            self.defineTimeout(-1)
            self.defineTimeout(60 * 4)

        elif mode == GPIOMode.VALIDATE:
            self.defineTimeout(-1)
            self.defineTimeout(30)

        elif mode == GPIOMode.DISPLAY_ASSEMBLY:
            self.defineTimeout(-1)
            self.defineTimeout(60 * 2)

        elif mode == GPIOMode.TRIGGER_ERROR:
            self.defineTimeout(-1)
            self.defineTimeout(30)

        elif mode == GPIOMode.RUNNING:
            self.defineTimeout(30)

    def showHomePage(self):

        if self.currentGPIOMode == GPIOMode.HOMEPAGE:
            return

        self.setCurrentMode(GPIOMode.HOMEPAGE)

        if self.movie is None:
            outPixmap = QPixmap(self.homeDisplay)
            self.label.setPixmap(outPixmap)

        else:
            self.label.setMovie(self.movie)
            self.movie.start()

        QApplication.processEvents()

    def showComputingPixmap(self):

        if self.currentGPIOMode == GPIOMode.COMPUTING:
            return

        self.setCurrentMode(GPIOMode.COMPUTING)

        self.resources.getLogger().addInfo("COMPUTING PAGE")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/computing.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def startPictureAssembly(self):

        self.resources.getLogger().addInfo("START PICTURE ASSEMBLY")

        if self.movie is not None:
            self.movie.stop()

        QApplication.processEvents()
        QApplication.processEvents()
        QApplication.processEvents()
        self.startCaptureProcess()

    def startCaptureProcess(self):

        imPath = self.resources.getPath(ressourcesManager.PATH.CAPTURE) + "/" + str(uuid.uuid4()) + ".jpg"
        self.resources.getLogger().addInfo("CAPTURE PROCESS " + imPath)
        self.setCurrentMode(GPIOMode.RUNNING)
        self.disconnectInputButtonInterupts()

        self.switchLed(False, False, False)

        self.countDown = 4
        for x in range(0, self.countDown):

            if x == 0:
                self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS, [ColorLED.BLUE, ColorLED.BLACK])
                self.led.blinkFront(400)
            if x == 1:
                self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS, [ColorLED.BLUE, ColorLED.BLACK])
                self.led.blinkFront(300)
            if x == 2:
                self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS, [ColorLED.BLUE, ColorLED.BLACK])
                self.led.blinkFront(200)
                self.switchConstantLight(True)

            delay = self.showPixmap(self.countDown - x, False, False, False)
            self.wait(0.6 - delay)
            delay = self.showPixmap(0, True, False, False)
            self.wait(0.6 - delay)

        captureThread = CaptureImageThread(imPath, self.resources)
        captureThread.signal.connect(self.onCaptureProcessFinished)
        self.start = time.time()
        self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS, [ColorLED.BLUE, ColorLED.BLACK])

        captureThread.start()

        self.showPixmap(0, True, True, False)
        self.wait(2.7)
        self.showPixmap(0, False, False, True)
        self.switchConstantLight(False)

    def onCaptureProcessFinished(self, result, capture):

        if result is True:
            self.resources.getLogger().addInfo("CAPTURE PROCESS FINISHED TRUE :" + str(time.time() - self.start) + "s")
            self.showValidatingPage(capture)
        else:
            self.resources.getLogger().addWarning("CAPTURE PROCESS FINISHED FALSE")
            self.showTriggerErrorPage()

        self.switchConstantLight(False)

    def showValidatingPage(self, capture):

        self.resources.getLogger().addInfo("SHOW VALIDATION PAGE")
        self.setCurrentMode(GPIOMode.VALIDATE)
        self.lastCapture = capture
        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/validate-capture.png"))

        w = 450
        h = 300
        b = 20
        x0 = (1280 - 2 * w - b) / 2
        y0 = (1024 - 2 * h - b) / 2

        for i in range(4):

            if i == 0:
                x = x0
                y = y0
            if i == 1:
                x = x0 + w + b
                y = y0
            if i == 2:
                x = x0
                y = y0 + h + b
            if i == 3:
                x = x0 + w + b
                y = y0 + h + b

            preview = None
            pen = None

            if i < len(self.captureList):
                preview = QPixmap(self.captureList[i])
                preview2 = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/opacitor.png")
                painter.translate(x, y)
                painter.drawPixmap(0, 0,
                                   preview.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
                painter.drawPixmap(0, 0,
                                   preview2.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
                #
                pen = QPen(Qt.gray)
                pen.setWidth(3)

            elif i == len(self.captureList):
                preview = QPixmap(capture)
                painter.translate(x, y)
                painter.drawPixmap(0, 0,
                                   preview.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
                pen = QPen(Qt.black)
                pen.setWidth(6)
                # painter.setPen(pen)
                # painter.drawRect(-m,-m, w+2*m, h+2*m)


            else:
                preview = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/avatar.png")
                painter.translate(x, y)
                painter.drawPixmap(0, 0,
                                   preview.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
                pen = QPen(Qt.gray)
                pen.setWidth(3)


            #pen.setWidth(3)

            # painter.translate(x, y)
            # painter.drawPixmap(0, 0, preview.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            painter.setPen(pen)
            painter.drawRect(0, 0, w, h)

            painter.translate(-x, -y)

        self.label.setPixmap(outPixmap)
        del painter

        QApplication.processEvents()
        self.connectInputButtonInterupts()
        self.switchLed(True, True, True)

    def buildShuffleAssembly(self, showCuttingLine=False):

        self.resources.getLogger().addInfo("BUILD SHUFFLE ASSEMBLY")
        choosenLayout = self.resources.chooseRandomLayout(len(self.captureList))

        if choosenLayout == None:
            return

        self.lastAssemblyPixmap = None
        self.lastAssemblyLandscape = choosenLayout["landscape"]
        self.showAssemblyPixmap()
        [self.lastAssemblyPixmap, self.currentAssemblyPath] = self.resources.buildLayoutFromList(captureList=self.captureList,
                                                                                                 choosenLayout=choosenLayout,
                                                                                                 showCuttingLine=showCuttingLine)
        self.showAssemblyPixmap()

    def showAssemblyPixmap(self):

        self.resources.getLogger().addInfo("SHOW ASSEMBLY PAGE")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.printingEnabled is False:
            painter.drawPixmap(0, 0,
                               QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/assembly-noprint.png"))
        else:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/assembly.png"))

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

            painter.translate(x, y)
            p = self.lastAssemblyPixmap.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, p)
            pen = QPen(Qt.white)
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawRect(0, 0, p.width(), p.height())

            painter.translate(-x, -y)

        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def showPixmapMenu(self):

        self.resources.getLogger().addInfo("SHOW MENU PAGE")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/menu.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def showPowerOnPrinter(self):

        if self.currentGPIOMode == GPIOMode.POWER_PRINTER:
            return

        self.setCurrentMode(GPIOMode.POWER_PRINTER)
        self.resources.getLogger().addInfo("SHOW POWER ON PRINTER")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/power_printer.png"))
        self.label.setPixmap(outPixmap)
        del painter
        self.connectInputButtonInterupts()
        self.switchLed(False, False, True)

    def showStartupPixmap(self):

        self.resources.getLogger().addInfo("SHOW STARTUP PAGE")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/startup.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def showShutdownPixmap(self):

        self.resources.getLogger().addInfo("SHOW SHUTDOWN PAGE")

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/shutdown.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def showGoHomePixmap(self):

        self.resources.getLogger().addInfo("SHOW GO HOME PAGE")

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/go-home.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def showPixmap(self, chrono, smiley, flash, download):

        start = time.time()
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        if chrono >= 1 or chrono <= 10:
            painter.drawPixmap(0, 0, QPixmap(
                self.resources.getPath(ressourcesManager.PATH.PAGE) + "/" + str(chrono) + ".png"))

        if smiley is True:
            painter.drawPixmap(0, 0,
                               QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/pre-pre-capture.png"))
        if flash is True:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/pre-capture.png"))
        if download is True:
            painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/downloading.png"))

        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

        del painter
        end = time.time()
        if end - start >= 1:
            return 1
        else:
            return end - start

    def blink(self):

        onValue = 0
        if PHOTOBOOTH_2:
            onValue = 1

        if self.blinkState == 0:
            self.blinkState = 1
        else:
            self.blinkState = 0

        if self.buttonRightLedEnabled:
            GPIO.output(GPIOPin.LED_BUTTON_3, self.blinkState)
        else:
            GPIO.output(GPIOPin.LED_BUTTON_3, onValue)

        if self.buttonLeftLedEnabled:
            GPIO.output(GPIOPin.LED_BUTTON_1, self.blinkState)
        else:
            GPIO.output(GPIOPin.LED_BUTTON_1, onValue)

        if self.buttonDownLedEnabled:
            GPIO.output(GPIOPin.LED_BUTTON_2, self.blinkState)
        else:
            GPIO.output(GPIOPin.LED_BUTTON_2, onValue)

    def onButton1Pressed(self):

        delay = 4
        offset = 4
        reset_default = [0, 2]
        reprint = [reset_default[1] + offset, reset_default[1] + offset + delay]
        shutdown = [reprint[1] + offset, reprint[1] + offset + delay]
        menu = [shutdown[1] + offset, shutdown[1] + offset + delay]
        menu_advanced = [menu[1] + offset, menu[1] + offset + delay]

        if DebugGPIO is True:
            self.resources.logger.addInfo("BUTTON 1 PRESSED")
            self.switchLed(True, False, False)
            self.led.showWarning(0)
            return

        if self.interuptsConnected is False:
            return

        self.resources.logger.addInfo("BUTTON 1 PRESSED")

        if self.currentGPIOMode == GPIOMode.HOMEPAGE:
            self.resources.logger.addInfo("BUTTON 1 PRESSED : 4 POSSIBLE ACTIONS")

            start = time.time()
            stop = 0
            duration = 0
            if EMULATE is False:
                while GPIO.input(GPIOPin.BUTTON_1) == 0:
                    self.wait(0.1)
                    QApplication.processEvents()
                    delay = (time.time() - start)
                    if (delay < reprint[1] and delay >= reprint[0]):
                        self.showReleaseForReprintPage()
                    elif (delay < shutdown[1] and delay >= shutdown[0]):
                        self.showReleaseForShutdownPage()
                    elif (delay < menu[1] and delay >= menu[0]):
                        self.showReleaseForMenuPage()
                    elif (delay < menu_advanced[1] and delay >= menu_advanced[0]):
                        self.showReleaseForAdvancedMenuPage()
                    else:
                        self.showHomePage()

            duration = (time.time() - start)

            if duration < reset_default[1] and duration >= reset_default[0]:
                self.resources.logger.addInfo("BUTTON 1 PRESSED : RESET PRINTER ERROR, CANCEL LAST PRINT")
                self.resetPrinterErrors()
                self.enablePrinter()
                self.cancelAllNotCompletedJobs()
                self.printerMonitoring.start()
                self.gotoStart()
            elif duration >= reprint[0] and duration < reprint[1]:
                self.resources.logger.addInfo("BUTTON 1 PRESSED : RESET PRINTER ERROR, PRINT LAST ASSEMBLY")
                self.sendPrintingJob()
            elif duration >= shutdown[0] and duration < shutdown[1]:
                self.resources.logger.addInfo("BUTTON 1 PRESSED : SHUTDOWN")
                self.onShutdown()
            elif duration >= menu[0] and duration < menu[1]:
                self.resources.logger.addInfo("BUTTON 1 PRESSED : SHOW MENU")
                self.onShowMenu()
            elif duration >= menu_advanced[0] and duration < menu_advanced[1]:
                self.resources.logger.addInfo("BUTTON 1 PRESSED : SHOW MENU ADVANCED")
                self.onShowAdvancedMenu()

        elif self.currentGPIOMode == GPIOMode.PRINT:
            self.resources.logger.addWarning("BUTTON 1 PRESSED : No option map to this button")

        elif self.currentGPIOMode == GPIOMode.MENU:
            self.resources.logger.addInfo("BUTTON 1 PRESSED : TRIGGER ACTION MENU")
            self.onRightButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.MENU_SETUP:
            self.resources.logger.addInfo("BUTTON 1 PRESSED : TRIGGER ACTION MENU")
            self.onRightButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            self.resources.logger.addWarning("BUTTON 1 PRESSED : No option map to this button")

        elif self.currentGPIOMode == GPIOMode.VALIDATE:
            self.resources.logger.addInfo("BUTTON 1 PRESSED : PHOTO VALIDATED")
            self.storeLastCapture()
            if len(self.captureList) >= 4:
                self.resources.resetChoices()
                self.redoAssembly()
            else:
                self.startCaptureProcess()

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            self.resources.logger.addInfo("BUTTON 1 PRESSED : OTHER ASSEMBLY")
            self.redoAssembly()

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR:
            self.resources.logger.addWarning("RETRYING CAPTURE ")
            self.startCaptureProcess()

        elif self.currentGPIOMode == GPIOMode.RUNNING:
            self.resources.logger.addWarning("BUTTON 1 PRESSED : No option map to this button")

        elif self.currentGPIOMode == GPIOMode.POWER_PRINTER:
            self.resources.logger.addWarning("BUTTON 1 PRESSED : No option map to this button")

        else:
            self.resources.logger.addWarning(
                "BUTTON 1 PRESSED : This mode (" + str(self.currentGPIOMode.value) + ") is not handled.")

    def onButton3Pressed(self):

        delay = 4
        offset = 3
        reset_default = [0, 2]
        reprint = [reset_default[1] , reset_default[1] + delay]
        shutdown = [reprint[1] + offset, reprint[1] + offset + delay]
        menu = [shutdown[1] + 3*offset, shutdown[1] + 3*offset + delay]
        menu_advanced = [menu[1] + 3*offset, menu[1] + 3*offset + delay]

        if DebugGPIO is True:
            self.resources.logger.addInfo("BUTTON 3 PRESSED")
            self.switchLed(False, True, False)
            self.led.showWarning(1)
            return

        if self.interuptsConnected is False:
            return

        self.resources.logger.addInfo("BUTTON 3 PRESSED")

        if self.currentGPIOMode == GPIOMode.HOMEPAGE:
            self.resources.logger.addInfo("BUTTON 3 PRESSED : 4 POSSIBLE ACTIONS")

            self.resources.logger.addInfo("RESET PRINTER ERRORS : " + str(reset_default[0]) + "s to " + str(reset_default[1]) + "s")
            self.resources.logger.addInfo("RE PRINT LAST PHOTO  : " + str(reprint[0]) + "s to " + str(reprint[1]) + "s")
            self.resources.logger.addInfo("SHUTDOWN PHOTOBOOTH  : " + str(shutdown[0]) + "s to " + str(shutdown[1]) + "s")
            self.resources.logger.addInfo("SHOW MENU            : " + str(menu[0]) + "s to " + str(menu[1]) + "s")
            self.resources.logger.addInfo("SHOW EXPERT MENU     : " + str(menu_advanced[0]) + "s to " + str(menu_advanced[1]) + "s")

            start = time.time()
            stop = 0
            duration = 0
            if EMULATE is False:
                while GPIO.input(GPIOPin.BUTTON_3) == 0:
                    self.wait(0.1)
                    QApplication.processEvents()
                    delay = (time.time() - start)
                    if (delay < reprint[1] and delay >= reprint[0]):
                        self.showReleaseForReprintPage()
                    elif (delay < shutdown[1] and delay >= shutdown[0]):
                        self.showReleaseForShutdownPage()
                    elif (delay < menu[1] and delay >= menu[0]):
                        self.showReleaseForMenuPage()
                    elif (delay < menu_advanced[1] and delay >= menu_advanced[0]):
                        self.showReleaseForAdvancedMenuPage()
                    else:
                        self.showHomePage()

            duration = (time.time() - start)

            if duration < reset_default[1] and duration >= reset_default[0]:
                self.resources.logger.addInfo("BUTTON 3 PRESSED : RESET PRINTER ERROR, CANCEL LAST PRINT")
                self.resetPrinterErrors()
                self.enablePrinter()
                self.cancelAllNotCompletedJobs()
                self.printerMonitoring.start()
                self.gotoStart()
            elif duration >= reprint[0] and duration < reprint[1]:
                self.resources.logger.addInfo("BUTTON 3 PRESSED : RESET PRINTER ERROR, PRINT LAST ASSEMBLY")
                self.sendPrintingJob()
            elif duration >= shutdown[0] and duration < shutdown[1]:
                self.resources.logger.addInfo("BUTTON 3 PRESSED : SHUTDOWN")
                self.onShutdown()
            elif duration >= menu[0] and duration < menu[1]:
                self.resources.logger.addInfo("BUTTON 3 PRESSED : SHOW MENU")
                self.onShowMenu()
            elif duration >= menu_advanced[0] and duration < menu_advanced[1]:
                self.resources.logger.addInfo("BUTTON 3 PRESSED : SHOW MENU ADVANCED")
                self.onShowAdvancedMenu()

        elif self.currentGPIOMode == GPIOMode.PRINT:
            self.resources.logger.addWarning("BUTTON 3 PRESSED : No option map to this button")

        elif self.currentGPIOMode == GPIOMode.MENU:
            self.resources.logger.addInfo("BUTTON 3 PRESSED : MENU BACK")
            self.onLeftButtonGPIO()


        elif self.currentGPIOMode == GPIOMode.MENU_SETUP:
            self.resources.logger.addInfo("BUTTON 3 PRESSED : MENU BACK")
            self.onLeftButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            self.resources.logger.addWarning("BUTTON 3 PRESSED : No option map to this button")

        elif self.currentGPIOMode == GPIOMode.VALIDATE:
            self.resources.logger.addInfo("BUTTON 3 PRESSED : PHOTO VALIDATED CREATE ASSEMBLY")
            self.storeLastCapture()
            self.resources.resetChoices()
            self.redoAssembly()

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            if self.printingEnabled is True:
                self.resources.logger.addInfo("BUTTON 3 PRESSED : PRINT")
                self.sendPrintingJob()

            else:
                self.resources.logger.addInfo("BUTTON 3 PRESSED : PRINT NOT ENABLED, DO NOTHING")

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR:

            self.resources.logger.addWarning("IGNORING THIS CAPTURE ")
            if len(self.captureList) < self.resources.nbImageMax:
                self.startCaptureProcess()

            else:
                self.redoAssembly()


        elif self.currentGPIOMode == GPIOMode.RUNNING:
            self.resources.logger.addWarning("BUTTON 3 PRESSED : No option map to this button")

        elif self.currentGPIOMode == GPIOMode.POWER_PRINTER:
            self.resources.logger.addWarning("BUTTON 3 PRESSED : No option map to this button")

        else:
            self.resources.logger.addWarning(
                "BUTTON 3 PRESSED : This mode (" + str(self.currentGPIOMode.value) + ") is not handled.")

    def onButton2Pressed(self):

        capture = [0, 2]
        constant_light = [4, 8]

        if DebugGPIO is True:
            self.resources.logger.addInfo("BUTTON 2 PRESSED")
            self.switchLed(False, False, True)
            self.led.blinkFront(300)
            return

        if self.interuptsConnected is False:
            return

        self.resources.logger.addInfo("BUTTON 2 PRESSED")

        if self.currentGPIOMode == GPIOMode.HOMEPAGE:

            start = time.time()
            stop = 0
            duration = 0
            if EMULATE is False:
                while GPIO.input(GPIOPin.BUTTON_2) == 0:
                    self.wait(0.1)
                    QApplication.processEvents()
                    delay = (time.time() - start)
                    if (delay < capture[1] and delay >= capture[0]):
                        pass
                    elif (delay < constant_light[1] and delay >= constant_light[0]):
                        self.showReleaseForSwitchConstantLightPage()
                    else:
                        self.showHomePage()

            duration = (time.time() - start)

            if duration < capture[1] and duration >= capture[0]:
                self.resources.logger.addInfo("BUTTON 2 PRESSED : START ASSEMBLY")
                self.startPictureAssembly()

            elif duration < constant_light[1] and duration >= constant_light[0]:
                self.resources.logger.addInfo("BUTTON 2 PRESSED : TOGGLE TOP LIGHT")
                self.topLightOn = not self.topLightOn
                self.switchConstantLight(self.topLightOn)
                self.showHomePage()

        elif self.currentGPIOMode == GPIOMode.PRINT:
            self.resources.logger.addWarning("BUTTON 2 PRESSED : No option map to this button")

        elif self.currentGPIOMode == GPIOMode.POWER_PRINTER:
            self.resources.logger.addInfo("BUTTON 2 PRESSED : POWER_PRINTER ACK -> HOMEPAGE")
            self.led.showWarning(0)
            self.gotoStart()
            self.switchConstantLight(False)

        elif self.currentGPIOMode == GPIOMode.MENU:
            self.resources.logger.addInfo("BUTTON 2 PRESSED : NAVIGATE MENU")
            self.onDownButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.MENU_SETUP:
            self.resources.logger.addInfo("BUTTON 2 PRESSED : NAVIGATE MENU")
            self.onDownButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            self.resources.logger.addWarning("BUTTON 2 PRESSED : No option map to this button")

        elif self.currentGPIOMode == GPIOMode.VALIDATE:
            self.resources.logger.addInfo("BUTTON 2 PRESSED : REDO LAST PICTURE")
            self.startCaptureProcess()

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            self.resources.logger.addInfo("BUTTON 2 PRESSED : DISPLAY_ASSEMBLY -> HOMEPAGE")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR:
            self.resources.logger.addWarning(
                "BUTTON 2 PRESSED : CANCELING")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.RUNNING:
            self.resources.logger.addWarning("BUTTON 2 PRESSED : No option map to this button")

        else:
            self.resources.logger.addWarning(
                "BUTTON 2 PRESSED : This mode (" + str(self.currentGPIOMode.value) + ") is not handled.")

    def resetPrinterErrors(self):

        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)

        self.printerMonitoring.quit()
        self.label.setRibbonEmptyLeft(False)
        self.label.setRibbonEmptyRight(False)
        self.label.setTrayMissingLeft(False)
        self.label.setTrayMissingRight(False)
        self.label.setPaperEmptyLeft(False)
        self.label.setPaperEmptyRight(False)
        self.led.showWarning(0)

    @pyqtSlot(int)
    def onInputButtonPressed(self, channel):
        if channel == GPIOPin.BUTTON_3:
            self.onButton3Pressed()
        elif channel == GPIOPin.BUTTON_1:
            self.onButton1Pressed()
        elif channel == GPIOPin.BUTTON_2:
            self.onButton2Pressed()

    def onRightButtonGPIO(self):
        try:
            self.defineTimeout(-1)
            self.defineTimeout(40)
            pyautogui.press('enter')
        except pyautogui.FailSafeException as e:
            print(e)
    def onLeftButtonGPIO(self):
        try:
            self.defineTimeout(-1)
            self.defineTimeout(40)
            pyautogui.press('left')
        except pyautogui.FailSafeException as e:
            print(e)

    def onDownButtonGPIO(self):
        try:
            self.defineTimeout(-1)
            self.defineTimeout(40)
            pyautogui.press('down')
        except pyautogui.FailSafeException as e:
            print(e)

    def onShowMenu(self):

        self.setCurrentMode(GPIOMode.MENU)
        self.switchLed(False, False, False)
        self.showPixmapMenu()
        self.updateMenu(False)
        self.contextMenu.exec_(QPoint(30, 200))
        self.resources.getLogger().addInfo("SHOW MENU")
        self.switchLed(True, True, True)
        self.gotoStart()

    def storeLastCapture(self):

        self.resources.getLogger().addInfo("STORE CAPTURE")
        self.captureList.append(self.lastCapture)


    def setImagequality0(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("imagequality", 0)
        self.resources.getLogger().addInfo("SET IMAGE QUALITY=0")

        if EMULATE is False:
            subprocess.call("gphoto2 --set-config imagequality=0", shell=True)

    def setImagequality1(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("imagequality", 1)
        self.resources.getLogger().addInfo("SET IMAGE QUALITY=1")
        if EMULATE is False:
            subprocess.call("gphoto2 --set-config imagequality=1", shell=True)

    def setImagequality2(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("imagequality", 2)
        self.resources.getLogger().addInfo("SET IMAGE QUALITY=2")
        if EMULATE is False:
            subprocess.call("gphoto2 --set-config imagequality=2", shell=True)



    def onSetCurrentPrinter(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.printerName = self.sender().text()
        settings.setValue("printerName", self.printerName)
        self.enablePrinter()
        self.printerMonitoring.changePrinterName(self.printerName)


    def wait(self, delay):

        if EMULATE is True:
            time.sleep(delay/10)
            return
        try:
            time.sleep(delay)
        except ValueError as e:
            self.resources.logger.addError("TIME.SLEEP EXCEPTION " + str(e))

    def onSetCurrentEvent(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("event", self.sender().text())
        self.resources.loadResources()
        self.resources.logInfos()
        self.cacheHomePicture()

    def onSetCurrentSkin(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("skin", self.sender().text())
        self.resources.loadResources()
        self.cacheHomePicture()

    def onSetCurrentBackGround(self):
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("background", self.sender().text())
        self.resources.loadResources()
        self.cacheHomePicture()


    def onShowAllTestAssemblies(self):

        self.onShowAssemblyCalibration1()
        self.onShowAssemblyCalibration2()
        self.onShowAssemblyCalibration3()
        self.onShowAssemblyCalibration4()

    def onShowAssemblyCalibration1(self):
        self.buildCalibrationAssembly(1)
        self.wait(5)

    def onShowAssemblyCalibration2(self):
        self.buildCalibrationAssembly(2)
        self.wait(5)

    def onShowAssemblyCalibration3(self):
        self.buildCalibrationAssembly(3)
        self.wait(5)

    def onShowAssemblyCalibration4(self):
        self.buildCalibrationAssembly(4)
        self.wait(5)

    def buildCalibrationAssembly(self, n):

        self.captureList.clear()
        for i in range(n):
            self.captureList.append(QPixmap(self.resources.getPath(ressourcesManager.PATH.CALIBRATION_IMAGE)))
        self.redoAssembly(showCuttingLine=True)


    def initActions(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.imagequality = settings.value("imagequality", 0, int)
        self.printerName = settings.value("printerName", "Canon_CP800")
        security = settings.value("security", True, bool)

        if EMULATE is False:
            subprocess.call("gphoto2 --set-config imagequality=" + str(self.imagequality), shell=True)

        self.actionCleanCaptures = QAction("Effacer les captures", self)
        self.actionCleanAssemblies = QAction("Effacer les montages", self)
        self.actionCleanEventDatas = QAction("Effacer toutes les donnees", self)

        if security is False:
            self.actionCleanCaptures.triggered.connect(self.cleanCaptures)
            self.actionCleanAssemblies.triggered.connect(self.cleanAssemblies)
            self.actionCleanEventDatas.triggered.connect(self.cleanEventDatas)

        self.actionImagequality0 = QAction("Low image quality : fast", self)
        self.actionImagequality0.triggered.connect(self.setImagequality0)
        self.actionImagequality0.setCheckable(True)

        self.actionImagequality1 = QAction("Medium image quality : slow", self)
        self.actionImagequality1.triggered.connect(self.setImagequality1)
        self.actionImagequality1.setCheckable(True)

        self.actionImagequality2 = QAction("High image quality : very slow", self)
        self.actionImagequality2.triggered.connect(self.setImagequality2)
        self.actionImagequality2.setCheckable(True)

        self.actionEnableConstantLight = QAction("Activer/Désactiver", self)
        self.actionEnableConstantLight.setCheckable(True)
        self.actionEnableConstantLight.triggered.connect(self.toogleEnableConstantLight)

        self.actionSwitchOnConstantLight = QAction("Allumer éclairage constant", self)
        self.actionSwitchOnConstantLight.triggered.connect(self.switchOnConstantLight)

        self.actionSwitchOffConstantLight = QAction("Eteindre éclairage constant", self)
        self.actionSwitchOffConstantLight.triggered.connect(self.switchOffConstantLight)

        self.actionEnableSpeedLight = QAction("Activer/Désactiver", self)
        self.actionEnableSpeedLight.setCheckable(True)
        self.actionEnableSpeedLight.triggered.connect(self.toogleEnableSpeedlight)

        self.actionRestartSpeedLight = QAction("Redemarrer flash", self)
        self.actionRestartSpeedLight.triggered.connect(self.restartSpeedLight)

        self.actionRestartDSLR = QAction("Redemarrer appareil photo", self)
        self.actionRestartDSLR.triggered.connect(self.restartDSLR)

        printerList = ["Canon_CP800_0","Canon_CP800_1","Canon_CP800_2","Canon_CP800_3"]

        self.printerActionList=[]
        for f in printerList:
            act = QAction(f, self)
            act.setCheckable(True)
            act.triggered.connect(self.onSetCurrentPrinter)
            self.printerActionList.append(act)


        self.actionEnablePrinting = QAction("Activer/Désactiver", self)
        self.actionEnablePrinting.setCheckable(True)
        self.actionEnablePrinting.triggered.connect(self.toogleEnablePrinting)

        self.actionShutdown = QAction("Arreter l'appareil", self)
        self.actionShutdown.triggered.connect(self.onShutdown)

        self.actionReboot = QAction("Redemarrer l'appareil", self)
        self.actionReboot.triggered.connect(self.onReboot)

        self.actionExit = QAction("<- Sortir du menu", self)


        self.actionRestartCups = QAction("Redemarrer cups", self)
        self.actionStartCups = QAction("Demarrer cups", self)
        self.actionStopCups = QAction("Arreter cups", self)

        self.actionRestartCups.triggered.connect(self.restartCUPS)
        self.actionStartCups.triggered.connect(self.startCUPS)
        self.actionStopCups.triggered.connect(self.stopCUPS)

        self.actionGenerateSingleAssemblies = QAction("Creer tous les assemblages 1 photo", self)
        self.actionGenerateSingleAssemblies.triggered.connect(self.onGenerateAllSingleAssemblies)

        self.actionShowAllAssemblyCalibration = QAction("Calibration de tous les assemblages", self)
        self.actionShowAssemblyCalibration1 = QAction("Calibration assemblage 1", self)
        self.actionShowAssemblyCalibration2 = QAction("Calibration assemblage 2", self)
        self.actionShowAssemblyCalibration3 = QAction("Calibration assemblage 3", self)
        self.actionShowAssemblyCalibration4 = QAction("Calibration assemblage 4", self)

        self.actionShowAllAssemblyCalibration.triggered.connect(self.onShowAllTestAssemblies)
        self.actionShowAssemblyCalibration1.triggered.connect(self.onShowAssemblyCalibration1)
        self.actionShowAssemblyCalibration2.triggered.connect(self.onShowAssemblyCalibration2)
        self.actionShowAssemblyCalibration3.triggered.connect(self.onShowAssemblyCalibration3)
        self.actionShowAssemblyCalibration4.triggered.connect(self.onShowAssemblyCalibration4)

        self.eventActionList=[]
        list = [f.name for f in os.scandir(self.resources.getPath(ressourcesManager.PATH.EVENT_LIST_PATH)) if f.is_dir()]
        for f in list:
            act = QAction(f, self)
            act.setCheckable(True)
            act.triggered.connect(self.onSetCurrentEvent)
            self.eventActionList.append(act)

        self.skinActionList=[]
        list = [f.name for f in os.scandir(self.resources.getPath(ressourcesManager.PATH.SKIN_LIST_PATH)) if f.is_dir()]
        for f in list:
            act = QAction(f, self)
            act.setCheckable(True)
            act.triggered.connect(self.onSetCurrentSkin)
            self.skinActionList.append(act)

        self.backgroundActionList = []
        list = [f.name for f in os.scandir(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_LIST_PATH)) if
                f.is_file()]
        for f in list:
            act = QAction(f, self)
            act.setCheckable(True)
            act.triggered.connect(self.onSetCurrentBackGround)

            self.backgroundActionList.append(act)
            act.setToolTip("<img src='"+self.resources.getPath(ressourcesManager.PATH.BACKGROUND_LIST_PATH) + "/" + f +"'" + " width='350' height='233' >")


    def onMoveMouseAbove(self, act):
        if self.lastAct != act:
            self.lastAct = act
            QToolTip.showText(QPoint(0,0), act.toolTip())


    def initMenu(self):
        self.lastAct = None
        has_speed_light = True
        has_constant_light = True
        has_printer = True
        can_restart_dslr = True

        self.contextMenu = QMenu("Context menu", self)

        self.dataMenu = QMenu("Données",self)
        self.settingMenu = QMenu("Réglages",self)
        self.displayMenu = QMenu("Affichage",self)
        self.eventMenu = QMenu("Evennement",self)
        self.functionalitiesMenu = QMenu("Fonctionalités",self)

        self.dataMenu.addAction(self.actionCleanCaptures)
        self.dataMenu.addAction(self.actionCleanAssemblies)
        self.dataMenu.addAction(self.actionCleanEventDatas)

        self.dslrMenu  = QMenu(CaptureImageThread(None,None).getCameraName(),self)
        self.settingMenu.addMenu(self.dslrMenu)

        self.speedLightMenu = QMenu("Eclairage flash", self)
        self.speedLightMenu.addAction(self.actionEnableSpeedLight)
        self.speedLightMenu.addAction(self.actionRestartSpeedLight)

        if has_speed_light is True:
            self.settingMenu.addMenu(self.speedLightMenu)

        self.constantLightMenu = QMenu("Eclairage constant", self)
        self.constantLightMenu.addAction(self.actionEnableConstantLight)
        self.constantLightMenu.addAction(self.actionSwitchOnConstantLight)
        self.constantLightMenu.addAction(self.actionSwitchOffConstantLight)

        if has_constant_light is True:
            self.settingMenu.addMenu(self.constantLightMenu)


        self.printerMenu = QMenu("Impression", self)
        self.cupsMenu = QMenu("Cups", self)
        self.printerMenu.addAction(self.actionEnablePrinting)
        self.printerMenu.addMenu(self.cupsMenu)
        self.printerMenu.addActions(self.printerActionList)
        self.cupsMenu.addAction(self.actionRestartCups)
        self.cupsMenu.addAction(self.actionStartCups)
        self.cupsMenu.addAction(self.actionStopCups)

        if has_printer is True:
            self.settingMenu.addMenu(self.printerMenu)



        if can_restart_dslr is True:
            self.dslrMenu.addAction(self.actionRestartDSLR)

        self.dslrMenu.addAction(self.actionImagequality0)
        self.dslrMenu.addAction(self.actionImagequality1)
        self.dslrMenu.addAction(self.actionImagequality2)

        self.backgroundMenu  = QMenu("Arriere plan",self)
        self.backgroundMenu.hovered.connect(self.onMoveMouseAbove)
        self.skinMenu  = QMenu("Thème",self)
        self.displayMenu.addMenu(self.backgroundMenu)
        self.displayMenu.addMenu(self.skinMenu)

        self.skinMenu.addActions(self.skinActionList)
        self.backgroundMenu.addActions(self.backgroundActionList)

        self.eventMenu.addActions(self.eventActionList)

        self.calibrateMenu = QMenu("Calibration",self)
        self.taskMenu = QMenu("Taches",self)
        self.functionalitiesMenu.addMenu(self.calibrateMenu)
        self.functionalitiesMenu.addMenu(self.taskMenu)

        self.taskMenu.addAction(self.actionGenerateSingleAssemblies)

        self.calibrateMenu.addAction(self.actionShowAllAssemblyCalibration)
        self.calibrateMenu.addAction(self.actionShowAssemblyCalibration1)
        self.calibrateMenu.addAction(self.actionShowAssemblyCalibration2)
        self.calibrateMenu.addAction(self.actionShowAssemblyCalibration3)
        self.calibrateMenu.addAction(self.actionShowAssemblyCalibration4)

        self.contextMenu.addMenu(self.dataMenu)
        self.contextMenu.addMenu(self.settingMenu)
        self.contextMenu.addMenu(self.displayMenu)
        self.contextMenu.addMenu(self.eventMenu)
        self.contextMenu.addMenu(self.functionalitiesMenu)
        self.contextMenu.addAction(self.actionShutdown)
        self.contextMenu.addAction(self.actionReboot)
        self.contextMenu.addAction(self.actionExit)

    def updateMenu(self, type):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.speedLightEnabled = settings.value("speedLightEnabled", True, bool)
        self.constantLightEnabled = settings.value("constantLightEnabled", True, bool)
        self.printingEnabled = settings.value("printingEnabled", True, bool)
        security = settings.value("security", True, bool)

        printerName = settings.value("printerName", "", str)
        imagequality = settings.value("imagequality", 1, int)
        eventName =  settings.value("event", 'unknown',str)
        skinName =  settings.value("skin", 'unknown',str)
        bgName =  settings.value("background", 'unknown',str)

        self.actionImagequality0.setChecked(imagequality == 0)
        self.actionImagequality1.setChecked(imagequality == 1)
        self.actionImagequality2.setChecked(imagequality == 2)

        for ac in self.eventActionList:
            ac.setChecked( ac.text() == eventName )

        for ac in self.skinActionList:
            ac.setChecked( ac.text() == skinName )

        for ac in self.backgroundActionList:
            ac.setChecked( ac.text() == bgName )

        for ac in self.printerActionList:
            ac.setChecked(ac.text() == printerName)
            ac.setVisible(self.printingEnabled)
        self.actionEnablePrinting.setChecked(self.printingEnabled)

        sizeCaptures = self.resources.getDirectorySize(self.resources.PATH.CAPTURE)
        sizeAssemblies = self.resources.getDirectorySize(self.resources.PATH.ASSEMBLIES)
        nbCaptures = self.resources.getDirectoryFileNumber(self.resources.PATH.CAPTURE)
        nbAssemblies = self.resources.getDirectoryFileNumber(self.resources.PATH.ASSEMBLIES)

        if security is True:

            self.actionCleanCaptures.setText(
                "Espace disque captures (" + str(nbCaptures) + " files, " + str("{:.2f}".format(sizeCaptures)) + " MB)")
            self.actionCleanAssemblies.setText(
                "Espace disque montages (" + str(nbAssemblies) + " files, " + str("{:.2f}".format(sizeAssemblies)) + " MB)")
            self.actionCleanEventDatas.setText("Espace disque total (" + str(nbCaptures + nbAssemblies) + " files, " + str(
                "{:.2f}".format(sizeCaptures + sizeAssemblies)) + " MB)")
            self.dataMenu.setTitle(
                "Donnees (" + str(nbCaptures+nbAssemblies) + " files, " + str("{:.2f}".format(sizeCaptures + sizeAssemblies)) + " MB)")
        else:

            self.actionCleanCaptures.setText(
                "Effacer les captures (" + str(nbCaptures) + " files, " + str("{:.2f}".format(sizeCaptures)) + " MB)")
            self.actionCleanAssemblies.setText(
                "Effacer les montages (" + str(nbAssemblies) + " files, " + str("{:.2f}".format(sizeAssemblies)) + " MB)")
            self.actionCleanEventDatas.setText("Effacer toutes les donnees (" + str(nbCaptures + nbAssemblies) + " files, " + str(
                "{:.2f}".format(sizeCaptures + sizeAssemblies)) + " MB)")
            self.dataMenu.setTitle(
                "Donnees (" + str(nbCaptures+nbAssemblies) + " files, " + str("{:.2f}".format(sizeCaptures + sizeAssemblies)) + " MB)")


        if self.speedLightEnabled is True:
            self.speedLightMenu.setTitle("Eclairage flash (activé)" )
        else:
            self.speedLightMenu.setTitle("Eclairage flash (desactivé)")

        if self.constantLightEnabled is True:
            self.constantLightMenu.setTitle("Eclairage constant (activé)")
        else:
            self.constantLightMenu.setTitle("Eclairage constant (desactivé)")

        if self.printingEnabled is False:
            self.printerMenu.setTitle("Impression (désactivé)")
        else:
            self.printerMenu.setTitle("Impression (activé)")

        if self.is_service_running("cups") is False:
            self.cupsMenu.setTitle("Cups (arreté)")
            self.actionRestartCups.setText("Redemarrer (arreté)")
            self.actionStartCups.setText("Demarrer (arreté)")
            self.actionStopCups.setText("Arreter (arreté)")
        else:
            self.cupsMenu.setTitle("Cups (démarré)")
            self.actionRestartCups.setText("Redemarrer (démarré)")
            self.actionStartCups.setText("Demarrer (démarré)")
            self.actionStopCups.setText("Arreter (démarré)")


        self.actionEnableSpeedLight.setChecked(self.speedLightEnabled)
        self.actionRestartSpeedLight.setVisible(self.speedLightEnabled)

        self.actionEnableConstantLight.setChecked(self.constantLightEnabled)
        self.actionSwitchOnConstantLight.setVisible(self.constantLightEnabled)
        self.actionSwitchOffConstantLight.setVisible(self.constantLightEnabled)

        self.actionEnableConstantLight.setVisible(type)
        self.functionalitiesMenu.menuAction().setVisible(type)
        self.dslrMenu.menuAction().setVisible(type)
        self.eventMenu.menuAction().setVisible(type)
        self.speedLightMenu.menuAction().setVisible(type)
        self.actionEnablePrinting.setVisible(type)
        self.cupsMenu.menuAction().setVisible(type)

        self.printerMenu.menuAction().setVisible(not self.printerMenu.isEmpty())
        self.constantLightMenu.menuAction().setVisible(not self.constantLightMenu.isEmpty())
        self.settingMenu.menuAction().setVisible(not self.settingMenu.isEmpty())

        QApplication.processEvents()

    def showTriggerErrorPage(self):

        self.resources.getLogger().addError("TRIGGER CAPTURE ERROR")
        self.setCurrentMode(GPIOMode.TRIGGER_ERROR)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/on-error.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

        self.switchLed(True, True, True)
        self.connectInputButtonInterupts()

    def onShowAdvancedMenu(self):

        self.setCurrentMode(GPIOMode.MENU_SETUP)
        self.switchLed(False, False, False)
        self.showPixmapMenu()
        self.updateMenu(True)
        self.contextMenu.exec_(QPoint(30, 200))

        self.resources.getLogger().addInfo("SHOW MENU")
        self.switchLed(True, True, True)
        self.gotoStart()

    def cleanCaptures(self):

        self.resources.getLogger().addInfo("ERASE CAPTURES")
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.CAPTURE))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.CAPTURE))


    def cleanEventDatas(self):

        self.resources.getLogger().addInfo("ERASE ALL")
        self.cleanAssemblies()
        self.cleanCaptures()

    def cleanAssemblies(self):

        self.resources.getLogger().addInfo("ERASE ASSEMBLIES")
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES))

    def toogleEnableSpeedlight(self):

        self.resources.getLogger().addInfo("ENABLE SPEEDLIGHT")
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        enable = not settings.value("speedLightEnabled", True, bool)
        settings.setValue("speedLightEnabled", enable)
        self.switchSpeedLight(enable)

    def restartSpeedLight(self):

        self.resources.getLogger().addInfo("RESTART SPEEDLIGHT")
        if EMULATE is True:
            return
        self.switchSpeedLight(False)
        self.wait(2)
        self.switchSpeedLight(True)

    def restartDSLR(self):

        self.resources.getLogger().addInfo("RESTART DSLR")
        if EMULATE is True:
            return
        self.switchDSLR(False)
        self.wait(2)
        self.switchDSLR(True)

    def initDevicesFast(self):

        self.resources.getLogger().addInfo("INIT DEVICES FAST")
        self.switchDSLR(True)

    def initDevices(self):

        self.resources.getLogger().addInfo("INIT DEVICES")
        self.restartDSLR()
        self.restartSpeedLight()
        QApplication.processEvents()

        if self.printingEnabled is True:
            self.startCUPS()
        else:
            self.stopCUPS()

        self.switchConstantLight(True)

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

        self.resources.logger.addInfo("RESTARTING CUPS")
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

        self.resources.logger.addInfo("STARTING CUPS")

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

        self.resources.logger.addInfo("STOPING CUPS")

        if EMULATE is True:
            return
        subprocess.Popen(["/etc/init.d/cups", "stop"])

    def onShutdown(self):

        self.showShutdownPixmap()
        self.resources.getLogger().addInfo("ARRET NORMAL DU PHOTOBOOTH")

        if EMULATE is False:
            self.switchSpeedLight(False)
            self.switchDSLR(False)
            self.switchLed(False, False, False)
            self.led.setColor(ledControler.LEDLocation.RIGHT_SIDE, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.LEFT_SIDE, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS, [ColorLED.BLACK, ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.CAMERA_BACK, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.TEXT_BACK, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.ERROR, [ColorLED.BLACK, ColorLED.BLACK])

        self.command("shutdown")

    def onReboot(self):

        self.showShutdownPixmap()
        self.resources.getLogger().addInfo("REDEMARRAGE NORMAL DU PHOTOBOOTH")

        if EMULATE is False:
            self.switchSpeedLight(False)
            self.switchDSLR(False)
            self.switchLed(False, False, False)
            self.led.setColor(ledControler.LEDLocation.RIGHT_SIDE, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.LEFT_SIDE, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS, [ColorLED.BLACK, ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.CAMERA_BACK, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.TEXT_BACK, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.ERROR, [ColorLED.BLACK, ColorLED.BLACK])

        self.command("reboot")

    def onGenerateAllSingleAssemblies(self):

        self.resources.getLogger().addInfo("GENERATE ALL SINGLE ASSEMBLIES")
        self.generateAllSingleAssemblies(self.resources.getPath(ressourcesManager.PATH.CAPTURE),
                                         self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES))

    def deleteAllMedias(self):

        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.CAPTURE))
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES))

        os.mkdir(self.resources.getPath(ressourcesManager.PATH.CAPTURE))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES))

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

        self.resources.logger.addInfo("INITIALIZING PARSPBERRY PI GPIOS.")

        if EMULATE is True:
            return

        GPIO.cleanup()

        # GPIO IN 20 wired

        GPIO.setup(GPIOPin.BUTTON_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(GPIOPin.BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(GPIOPin.BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(GPIOPin.LED_BUTTON_3, GPIO.OUT, initial=1)
        GPIO.setup(GPIOPin.LED_BUTTON_2, GPIO.OUT, initial=1)
        GPIO.setup(GPIOPin.LED_BUTTON_1, GPIO.OUT, initial=1)

        GPIO.setup(GPIOPin.RELAY_POWER_TOP_LIGHT, GPIO.OUT, initial=0)

        if PHOTOBOOTH_2 is False:
            GPIO.setup(GPIOPin.RELAY_LED_STRIP, GPIO.OUT, initial=1)

        GPIO.setup(GPIOPin.RELAY_2, GPIO.OUT, initial=1)
        GPIO.setup(GPIOPin.RELAY_3, GPIO.OUT, initial=1)

        if PHOTOBOOTH_2 is True:
            GPIO.setup(GPIOPin.POWER_SPEEDLIGHT, GPIO.OUT, initial=1)
            GPIO.setup(GPIOPin.ON_OFF_SPEEDLIGHT, GPIO.OUT, initial=1)
            GPIO.setup(GPIOPin.POWER_DSLR, GPIO.OUT, initial=1)

        self.blinkingTimer = QTimer()
        self.blinkingTimer.timeout.connect(self.blink)
        self.blinkingTimer.start(300)

        self.inputButtonThread = InputButtonThread()
        self.disconnectInputButtonInterupts()
        self.inputButtonThread.start()

    def switchConstantLight(self, on):

        self.resources.logger.addInfo("CONSTANT LIGHT SWITCHED TO " + str(on))
        if EMULATE is True:
            return

        if on is True:
            GPIO.output(GPIOPin.RELAY_POWER_TOP_LIGHT, 0)
        else:
            GPIO.output(GPIOPin.RELAY_POWER_TOP_LIGHT, 1)

    def toogleEnableConstantLight(self):

        self.resources.getLogger().addInfo("ENABLE CONSTANT LIGHT")
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        enable = not settings.value("constantLightEnabled", True, bool)
        settings.setValue("constantLightEnabled", enable)
        self.switchConstantLight(enable)
        if enable is True:
            self.wait(2)
            self.switchConstantLight(False)

    def switchOnConstantLight(self):
        self.switchConstantLight(True)

    def switchOffConstantLight(self):
        self.switchConstantLight(False)


    def testRelays(self):

        GPIO.output(GPIOPin.RELAY_POWER_TOP_LIGHT, 0)
        self.wait(2)
        GPIO.output(GPIOPin.RELAY_LED_STRIP, 0)
        self.wait(2)

    def switchSpeedLight(self, on):

        if PHOTOBOOTH_2 is False:
            return

        if EMULATE is True:
            return

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        en = settings.value("speedLightEnabled", True, bool)

        if on is True and en is True:

            GPIO.output(GPIOPin.POWER_SPEEDLIGHT, 0)
            self.wait(1)
            GPIO.output(GPIOPin.ON_OFF_SPEEDLIGHT, 0)
            self.wait(2)
            GPIO.output(GPIOPin.ON_OFF_SPEEDLIGHT, 1)

        else:

            GPIO.output(GPIOPin.ON_OFF_SPEEDLIGHT, 0)
            self.wait(2)
            GPIO.output(GPIOPin.ON_OFF_SPEEDLIGHT, 1)
            GPIO.output(GPIOPin.POWER_SPEEDLIGHT, 1)
            self.wait(1)

    def switchDSLR(self, on):

        if PHOTOBOOTH_2 is False:
            return

        if EMULATE is True:
            return

        if on is True:
            GPIO.output(GPIOPin.POWER_DSLR, 0)
            self.wait(1)
        else:
            GPIO.output(GPIOPin.POWER_DSLR, 1)
            self.wait(1)

    def onTimeout(self):

        self.defineTimeout(-1)

        if self.currentGPIOMode == GPIOMode.HOMEPAGE:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED DO NOTHING")
            pass

        elif self.currentGPIOMode == GPIOMode.PRINT:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.MENU:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            if EMULATE is True:
                return
            try:
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
            except pyautogui.FailSafeException as e:
                print(e)


            self.gotoStart()


        elif self.currentGPIOMode == GPIOMode.MENU_SETUP:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            if EMULATE is True:
                return
            try:
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
            except pyautogui.FailSafeException as e:
                print(e)
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.VALIDATE:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED BUTTON 3 EMULATED")
            self.onButton3Pressed()

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED BUTTON 3 EMULATED")
            self.onLeftButtonPressed()

        elif self.currentGPIOMode == GPIOMode.RUNNING:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.POWER_PRINTER:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.led.showWarning(0)
            self.gotoStart()

    def redoAssembly(self,showCuttingLine=False):

        self.setCurrentMode(GPIOMode.DISPLAY_ASSEMBLY)
        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)
        self.wait(0.2)
        QApplication.processEvents()
        self.buildShuffleAssembly(showCuttingLine=showCuttingLine)
        self.switchLed(True, self.printingEnabled, True)
        self.connectInputButtonInterupts()
        QApplication.processEvents()

    def connectInputButtonInterupts(self):

        self.resources.logger.addInfo("ENABLE BUTTON HANDLER")
        if EMULATE is True:
            if self.interuptsConnected is False:
                self.interuptsConnected = True
            return
        if self.interuptsConnected is False:
            self.inputButtonThread.inputButtonEventDetected.connect(self.onInputButtonPressed)
            self.interuptsConnected = True
            QApplication.processEvents()

    def disconnectInputButtonInterupts(self):

        self.resources.logger.addInfo("DISABLE BUTTON HANDLER")
        if EMULATE is True:
            if self.interuptsConnected is True:
                self.interuptsConnected = False
            return
        if self.interuptsConnected is True:
            self.inputButtonThread.inputButtonEventDetected.disconnect(self.onInputButtonPressed)
            self.interuptsConnected = False
            QApplication.processEvents()

    def sendPrintingJob(self):

        if EMULATE is True:
            self.showPrintSentPage()
            self.wait(3)
            self.gotoStart()
            return

        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)
        self.enablePrinter()

        self.resetPrinterErrors()

        self.cancelAllNotCompletedJobs()
        try:
            conn = cups.Connection()

            exists = os.path.isfile(self.currentAssemblyPath)
            if exists:

                self.lastPrintId = conn.printFile(self.printerName, self.currentAssemblyPath, title='boxaselfi_job',
                                                  options={})
                self.resources.logger.addInfo(
                    "NEW JOB PRINT(" + str(self.lastPrintId) + ") : " + self.currentAssemblyPath)
                self.showPrintSentPage()
                self.wait(5)


            else:

                self.resources.logger.addError("NEW JOB PRINT : " + self.currentAssemblyPath + "file does not exists")

            self.printerMonitoring.start()
        except:
            self.resources.logger.addError("sendPrintingJob EXCEPTION")

        self.gotoStart()

    def cancelNotCompletedJobs(self):
        try:
            conn = cups.Connection()
            # printers = conn.getPrinters()
            for key, val in conn.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1).items():
                if key != self.lastPrintId:
                    self.resources.logger.addInfo("CANCEL JOB ID : " + str(key))
                    conn.cancelJob(key, purge_job=False)
                else:
                    self.resources.logger.addInfo("DO NOT CANCEL LAST JOB ID : " + str(key))
        except:
            self.resources.logger.addError("cancelNotCompletedJobs EXCEPTION")

    def cancelAllNotCompletedJobs(self):
        try:
            conn = cups.Connection()
            # printers = conn.getPrinters()
            for key, val in conn.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1).items():
                self.resources.logger.addInfo("CANCEL JOB ID : " + str(key))
                conn.cancelJob(key, purge_job=False)
        except:
            self.resources.logger.addError("cancelAllNotCompletedJobs EXCEPTION")

    def enablePrinter(self):
        try:
            conn = cups.Connection()
            conn.enablePrinter(self.printerName)
        except:
            self.resources.logger.addError("ENABLE PRINTER CUPS EXCEPTION")

    def showPrintSentPage(self):

        self.resources.logger.addInfo("SHOW NEW PRINT JOB SENT")
        self.setCurrentMode(GPIOMode.PRINT)
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/printing.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showReleaseForSwitchConstantLightPage(self):

        if (self.currentGPIOMode == GPIOMode.INFO_SWITCH_CONSTANT_LIGHT):
            return
        self.resources.logger.addInfo("SHOW RELEASE TO SWITCH CONSTANT LIGHT")
        self.setCurrentMode(GPIOMode.INFO_SWITCH_CONSTANT_LIGHT)
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(
            self.resources.getPath(ressourcesManager.PATH.PAGE) + "/info-switch-constant-light.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showReleaseForShutdownPage(self):

        if (self.currentGPIOMode == GPIOMode.INFO_SHUTDOWN):
            return
        self.resources.logger.addInfo("SHOW RELEASE TO SHUTDOWN")
        self.setCurrentMode(GPIOMode.INFO_SHUTDOWN)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/info-shutdown.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showReleaseForMenuPage(self):

        if (self.currentGPIOMode == GPIOMode.INFO_MENU):
            return
        self.resources.logger.addInfo("SHOW RELEASE FO MENU")
        self.setCurrentMode(GPIOMode.INFO_MENU)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/info-menu.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showReleaseForAdvancedMenuPage(self):

        if (self.currentGPIOMode == GPIOMode.INFO_MENU_ADVANCED):
            return
        self.resources.logger.addInfo("SHOW RELEASE FOR ADVANCED MENU")
        self.setCurrentMode(GPIOMode.INFO_MENU_ADVANCED)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0,
                           QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/info-menu-advanced.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showReleaseForReprintPage(self):

        if (self.currentGPIOMode == GPIOMode.INFO_REPRINT):
            return
        self.resources.logger.addInfo("SHOW RELEASE FOR REPRINT")
        self.setCurrentMode(GPIOMode.INFO_REPRINT)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/info-reprint.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def erasePrinterStatusBox(self):

        self.resources.logger.addInfo("JOB PRINT STATUS : CLEANING THE LIST")
        self.printJobStatusList = []

    def gotoStart(self, index=1):

        self.resources.logger.addInfo("GO HOME")
        # self.setCurrentMode(GPIOMode.HOMEPAGE)
        self.switchLed(False, False, True)
        self.connectInputButtonInterupts()
        self.captureList.clear()
        self.showHomePage()

    def switchLed(self, Right, Left, Downn):

        self.setButtonRightLedEnabled(Right)
        self.setButtonLeftLedEnabled(Left)
        self.setButtonDownLedEnabled(Downn)
        QApplication.processEvents()
        QApplication.processEvents()
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

        if e.key() == Qt.Key_1:
            self.onButton1Pressed()
        if e.key() == Qt.Key_2:
            self.onButton2Pressed()
        if e.key() == Qt.Key_3:
            self.onButton3Pressed()

    def closeEvent(self, event):

        event.ignore()
        if EMULATE is False:
            self.switchSpeedLight(False)
            self.switchDSLR(False)
            self.switchLed(False, False, False)
            self.led.setColor(ledControler.LEDLocation.RIGHT_SIDE, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.LEFT_SIDE, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS, [ColorLED.BLACK, ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.CAMERA_BACK, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.TEXT_BACK, [ColorLED.BLACK])
            self.led.setColor(ledControler.LEDLocation.ERROR, [ColorLED.BLACK, ColorLED.BLACK])

        exit(140)

    def generateAllSingleAssemblies(self, inputFolder, outputFolder):

        self.showComputingPixmap()
        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)

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
            for ind in range(self.resources.nbImageMax):
                idName = idName.replace("_" + str(ind) + ".jpg", "", 1)

            outFile = outputFolder + "/" + idName + "_" + layoutId + ".jpg"

            self.resources.buildSingleLayout(files, outFile, choosenLayout)

        self.gotoStart()

    def generateRandomIO(self, delay):

        generator = SimulatorButtonThread(self, delay)
        generator.start()
        QApplication.processEvents()
        self.wait(2)


class SimulatorButtonThread(QThread):

    def __init__(self, mm, delay):
        QThread.__init__(self)
        self.mainWindow = mm
        self.delay = delay

    def run(self):
        while True:
            j = random.randint(1, 3)
            time.sleep(self.delay)
            if j == 1:
                self.mainWindow.onButton1Pressed()
            if j == 2:
                self.mainWindow.onButton2Pressed()
            if j == 3:
                self.mainWindow.onButton3Pressed()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.setStyleSheet(
"""
QMenu {
    background-color: rgb(100,100,100);
    color: white;
    font-size: 18px;
    border: 2px solid rgb(160,160,160);
    padding-top:2px;
    padding-left: 2px;
    padding-right: 2px;
    padding-bottom: 2px;
}
QMenu::item{
    padding-top: 8px;
    padding-left: 10px;
    padding-right: 25px;
    padding-bottom: 8px;
}
QMenu::item {
    background-color: transparent;
    margin:2px;
}
QMenu::item:selected {
    background: rgb(50,50,50);
    border: 4px solid rgb(255,122,45);
    margin:2px;
}
"""
    )
    mainWin.show()
    ret = app.exec_()

    if EMULATE is False:
        mainWin.switchSpeedLight(False)
        mainWin.switchDSLR(False)
        mainWin.switchLed(False, False, False)
        mainWin.led.setColor(ledControler.LEDLocation.RIGHT_SIDE, [ColorLED.BLACK])
        mainWin.led.setColor(ledControler.LEDLocation.LEFT_SIDE, [ColorLED.BLACK])
        mainWin.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS, [ColorLED.BLACK, ColorLED.BLACK])
        mainWin.led.setColor(ledControler.LEDLocation.CAMERA_BACK, [ColorLED.BLACK])
        mainWin.led.setColor(ledControler.LEDLocation.TEXT_BACK, [ColorLED.BLACK])
        mainWin.led.setColor(ledControler.LEDLocation.ERROR, [ColorLED.BLACK, ColorLED.BLACK])
        GPIO.cleanup()

    sys.exit(ret)
