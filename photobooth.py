#!/usr/bin/env python

import sys

try:
    from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QRectF, QSettings, QSize, QUrl,
                              Qt, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QDateTime, QIODevice,
                              QElapsedTimer)
    from PyQt5.QtGui import QIcon, QKeySequence, QFont, QPixmap, QPainter, QPen, QColor, QMovie
    from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow,QToolTip)
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
    import socket
    import urllib.request
except:
    print("socket or urllib.request import error")

try:
    from PIL import Image
except:
    print("import Image from PIL error")

try:
    import logging
except:
    print("import logging error")

if EMULATE is False:
    try:
        import usb.core
    except:
        print("import usb.core error")

if EMULATE is False:
    GPIO.setmode(GPIO.BCM)



class PhotoBoothSettings():

    class GPIOPin(IntEnum):

        LED_BUTTON_1 = 1
        LED_BUTTON_2 = 2
        LED_BUTTON_3 = 3
        LED_0 = 4
        BUTTON_1 = 5
        BUTTON_2 = 6
        BUTTON_3 = 7
        BUTTON_4 = 8
        RELAY_POWER_TOP_LIGHT = 9
        RELAY_LED_STRIP = 10
        POWER_SPEEDLIGHT = 11
        ON_OFF_SPEEDLIGHT = 12
        POWER_DSLR = 13

        # RELAY_2 = ?
        # RELAY_3 = ?
        # WIRE_3_4 = ?
        # WIRE_3_5 = ?
        # WIRE_3_6 = ?

    GPIO_Pinout = {}
    logger = logging.getLogger("PhotoBoothSetti")

    def __init__(self):
        pass

    def getName(self):
        return "Photobooth name not set"

    def has_external_flash(self):
        return False

    def can_restart_external_flash(self):
        return False

    def has_constant_light(self):
        return True

    def can_restart_DSLR(self):
        return False

    def is_DSLR_up(self):
        return True

    def is_DSLR_up(self):
        return True

    def can_restart_led_strip(self):
        return False

    def has_led_strip(self):
        return True

    def get_led_strip_serial_Speed(self):
        return 115200

    def get_led_strip_serial_Port(self):
        return "/dev/ttyUSB_LED_CONTROLLER"

    def has_printer_port(self):
        return True

    def is_LedPullUp(self):
        return True

    def getCameraName(self):
        return "Camera name not set"

    def getScreenResolution(self):
        return 1024, 768

    def getGPIO(self, pinName):
        if pinName in self.GPIOPin:
            if pinName in self.GPIO_Pinout:
                return self.GPIO_Pinout[pinName]
            else:
                self.logger.error("ERROR, pinName not set.")
        else:
            self.logger.error("ERROR, unknown pinName.")
            return 0


    def setGPIO(self, pinName, pinNumber):

        if pinName in self.GPIOPin:
            self.GPIO_Pinout[pinName]=pinNumber
        else:
            self.logger.error("ERROR, pinName not available.")

    def printGPIOs(self):

        self.logger.info("GPIO_Pinout : ")
        for x in self.GPIOPin:
            if x in self.GPIO_Pinout:
                self.logger.info(str(x) + " -> " + str(self.GPIO_Pinout[x]))
            else:
                self.logger.info(str(x) + " -> unused")

    def printDetails(self):

        self.logger.info("========          Photobooth details          ========")
        self.logger.info("name : " + str( self.getName()) )
        self.logger.info("getCameraName : " + str(self.getCameraName()))
        self.logger.info("getScreenResolution : " + str(self.getScreenResolution()))
        self.logger.info("has_external_flash : " + str( self.has_external_flash()) )
        self.logger.info("can_restart_external_flash : " + str(self.can_restart_external_flash()))
        self.logger.info("has_constant_light : " + str(self.has_constant_light()))
        self.logger.info("can_restart_DSLR : " + str(self.can_restart_DSLR()))
        self.logger.info("can_restart_led_strip : " + str(self.can_restart_led_strip()))
        self.logger.info("has_led_strip : " + str(self.has_led_strip()))
        self.logger.info("get_led_strip_serial_Speed : " + str(self.get_led_strip_serial_Speed()))
        self.logger.info("get_led_strip_serial_Port : " + str(self.get_led_strip_serial_Port()))
        self.logger.info("has_printer_port : " + str(self.has_printer_port()))
        self.printGPIOs()
        self.logger.info("========        EOF Photobooth details        ========")

class PhotoBoothSettings_1(PhotoBoothSettings):

    def __init__(self):

        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_1, 13)
        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_2, 26)
        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_3, 6)
        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_0, 19)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_1, 12)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_2, 16)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_3, 20)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_4, 21 )
        self.setGPIO(PhotoBoothSettings.GPIOPin.RELAY_POWER_TOP_LIGHT, 17)
        self.setGPIO(PhotoBoothSettings.GPIOPin.RELAY_LED_STRIP, 4)

    def getName(self):
        return "PHOTOBOOTH 1"

    def has_external_flash(self):
        return False

    def can_restart_DSLR(self):
        return False

    def can_restart_external_flash(self):
        return False

    def can_restart_led_strip(self):
        return True

    def is_LedPullUp(self):
        return False

    def getCameraName(self):
        return "Nikon DSC D3200"

class PhotoBoothSettings_2(PhotoBoothSettings):

    def __init__(self):

        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_1, 13)
        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_2, 26)
        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_3, 6)
        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_0, 19)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_1, 20)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_2, 16)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_3, 12)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_4, 21)
        self.setGPIO(PhotoBoothSettings.GPIOPin.RELAY_POWER_TOP_LIGHT, 22)
        # self.setGPIO(PhotoBoothSettings.GPIOPin.RELAY_LED_STRIP, 4)
        # self.setGPIO(PhotoBoothSettings.GPIOPin.POWER_SPEEDLIGHT, 17)
        # self.setGPIO(PhotoBoothSettings.GPIOPin.ON_OFF_SPEEDLIGHT, 23)
        self.setGPIO(PhotoBoothSettings.GPIOPin.POWER_DSLR, 4)

    def getName(self):
        return "PHOTOBOOTH 2"

    def has_external_flash(self):
        return False

    def can_restart_DSLR(self):
        return True

    def is_DSLR_up(self):
        return True

    def can_restart_external_flash(self):
        return False

    def can_restart_led_strip(self):
        return False

    def is_LedPullUp(self):
        return True

    def getCameraName(self):
        return "Nikon DSC D70s (PTP mode)"


class PhotoBoothSettings_10(PhotoBoothSettings):

    def __init__(self):

        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_1, 13)
        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_2, 26)
        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_3, 6)
        self.setGPIO(PhotoBoothSettings.GPIOPin.LED_0, 19)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_1, 20)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_2, 16)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_3, 12)
        self.setGPIO(PhotoBoothSettings.GPIOPin.BUTTON_4, 21)
        self.setGPIO(PhotoBoothSettings.GPIOPin.RELAY_POWER_TOP_LIGHT, 22)
        self.setGPIO(PhotoBoothSettings.GPIOPin.RELAY_LED_STRIP, 4)
        self.setGPIO(PhotoBoothSettings.GPIOPin.POWER_SPEEDLIGHT, 17)
        self.setGPIO(PhotoBoothSettings.GPIOPin.ON_OFF_SPEEDLIGHT, 23)
        self.setGPIO(PhotoBoothSettings.GPIOPin.POWER_DSLR, 4)

    def getName(self):
        return "PHOTOBOOTH 10"

    def has_external_flash(self):
        return True

    def can_restart_DSLR(self):
        return True

    def is_DSLR_up(self):
        return True

    def can_restart_external_flash(self):
        return True

    def can_restart_led_strip(self):
        return False

    def is_LedPullUp(self):
        return True

    def getCameraName(self):
        return "Nikon DSC D70s (PTP mode)"



class DisplayMode(Enum):

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
    HELP_PRINTER = 16
    UNDEFINED = 255

class PrinterMonitoringThread(QThread):

    # printerFailure = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    logger = logging.getLogger("PrinterMonitori")

    def __init__(self, mainWindow):
        QThread.__init__(self)
        self.mainWindow = mainWindow

    def run(self):

        while True:
            try:
                if EMULATE is False and self.mainWindow.boxSettings.has_printer_port() is True and self.mainWindow.printingEnabled is True:

                    printerSerial = self.mainWindow.getOnlinePrinters()
                    if len(printerSerial) >= 1:
                        self.mainWindow.setCurrentPrinter(self.mainWindow.getPrinterName(printerSerial[0]))
                    else:
                        self.mainWindow.setCurrentPrinter("")

                    if self.mainWindow.printerName == "" :
                        if self.mainWindow.label.hasPrinterOffline() is False:
                            self.logger.warning("PRINTER : PLUG/POWER THE PRINTER!")
                            self.mainWindow.label.setPrinterOffline(True)
                            self.mainWindow.ledStrip.showWarning(1)

                    else :
                        if self.mainWindow.label.hasPrinterOffline() is True:
                            self.mainWindow.label.setPrinterOffline(False)
                            self.mainWindow.ledStrip.showWarning(0)
                        try:
                            conn = cups.Connection()
                            printers = conn.getPrinters()
                            for printer in printers:
                                if self.mainWindow.printerName == printer:
                                    if printers[printer]['printer-state'] == 5:
                                        if printers[printer]["printer-state-message"] == "No paper tray loaded, aborting!":
                                            self.logger.warning("PRINTER : NO PAPER TRAY LOADED, ABORTING!")
                                            self.mainWindow.label.setTrayMissing(True)
                                            self.mainWindow.ledStrip.showWarning(1)

                                        if printers[printer]["printer-state-message"] == "No ribbon loaded, aborting job!":
                                            self.logger.warning("PRINTER : NO RIBBON LOADED, ABORTING!")
                                            self.mainWindow.label.setRibbonMissing(True)
                                            self.mainWindow.ledStrip.showWarning(1)

                                    if printers[printer]['printer-state'] == 3:
                                        if printers[printer]["printer-state-message"] == "Ribbon depleted!":
                                            self.logger.warning("PRINTER : RIBBON DEPLETED!")
                                            self.mainWindow.label.setRibbonEmpty(True)
                                            self.mainWindow.ledStrip.showWarning(1)

                                        if printers[printer]["printer-state-message"] == "Paper feed problem!":
                                            self.logger.warning("PRINTER : PAPER FEED PROBLEM!")
                                            self.mainWindow.label.setPaperEmpty(True)
                                            self.mainWindow.ledStrip.showWarning(1)

                            self.mainWindow.refreshLedButtons()

                        except cups.IPPError as e:
                            self.logger.error("CUPS.IPPERROR " + str(e))
                        except RuntimeError as e1:
                            self.logger.error("RUNTIMEERROR " + str(e1))
                            break

                else:
                    self.mainWindow.label.setTrayMissing(False)
                    self.mainWindow.label.setRibbonMissing(False)
                    self.mainWindow.label.setRibbonEmpty(False)
                    self.mainWindow.label.setPaperEmpty(False)
                    self.mainWindow.label.setPrinterOffline(False)
                    self.mainWindow.ledStrip.showWarning(0)
                    self.mainWindow.refreshLedButtons()
                    time.sleep(240)

                self.mainWindow.label.update()

            except:
                self.logger.error("PRINTERMONITORINGTHREAD EXCEPTION")

            finally:
                time.sleep(5)

class InputButtonThread(QThread):
    inputButtonEventDetected = pyqtSignal(int)

    def __init__(self, boxSettings):
        QThread.__init__(self)
        self.boxSettings=boxSettings
        self.queue = Queue()
        if EMULATE is False:
            GPIO.add_event_detect(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_1), GPIO.FALLING, callback=self.queue.put, bouncetime=500)
            GPIO.add_event_detect(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_2), GPIO.FALLING, callback=self.queue.put, bouncetime=500)
            GPIO.add_event_detect(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_3), GPIO.FALLING, callback=self.queue.put, bouncetime=500)

    def run(self):
        while True:
            self.inputButtonEventDetected.emit(self.queue.get())


class CaptureImageThread(QThread):
    signal = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    logger = logging.getLogger("CaptureImageThr")
    def __init__(self, path, ressourceManager, photoboothSettings):
        QThread.__init__(self)
        self.capture = path
        self.ressourceManager = ressourceManager
        self.photoboothSettings = photoboothSettings
    # run method gets called when we start the thread

    def getCameraName(self):
        return self.photoboothSettings.getCameraName()

    def run(self):

        self.logger.info("CAPTURE REQUEST")

        if EMULATE is True:
            self.logger.info("IMAGE CAPTURED : " + self.capture)
            time.sleep(1)
            Original_Image = Image.open(self.ressourceManager.getPath(self.ressourceManager.PATH.CALIBRATION_IMAGE))
            Original_Image.save(self.capture)
            self.signal.emit(True, self.capture)
            return

        p = Popen(["gphoto2", "--camera", self.photoboothSettings.getCameraName(), "--capture-image-and-download",
                   "--filename=" + self.capture], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode

        if len(err) > 0:
            self.logger.error(str(err))
            self.signal.emit(False, None)
        else:
            self.logger.info( "IMAGE CAPTURED : " + self.capture)
            if self.photoboothSettings.is_DSLR_up() is False:
                Original_Image = Image.open(self.capture)
                rotated_image1 = Original_Image.rotate(180)
                Original_Image.close()
                rotated_image1.save(self.capture)

            self.signal.emit(True, self.capture)


class Label(QLabel):

    ribbonEmpty = False
    ribbonMissing = False
    trayMissing = False
    paperEmpty = False
    warningVisible = False
    printerOffline = False
    printerHelpButtonVisible = False
    debugVisible = False
    localIp = "127.0.0.1"
    externIp = "127.0.0.1"
    printerName = ""

    def setRibbonEmpty(self, b):
        self.ribbonEmpty = b

    def setRibbonMissing(self, b):
        self.ribbonMissing = b

    def setPaperEmpty(self, b):
        self.paperEmpty = b

    def setTrayMissing(self, b):
        self.trayMissing = b

    def setWarningVisible(self, visible):
        self.warningVisible = visible

    def setWarningVisible(self, visible):
        self.warningVisible = visible

    def hasVisibleWarning(self):
        return (self.ribbonEmpty is True or self.trayMissing is True or self.paperEmpty is True or self.ribbonMissing is True) and self.printerHelpButtonVisible is True

    def setPrinterHelpButtonVisible(self, visible):
        self.printerHelpButtonVisible = visible

    def setPrinterOffline(self, b):
        self.printerOffline = b

    def hasPrinterOffline(self):
        return self.printerOffline

    def setDebugVisible(self, visible):
        self.debugVisible = visible

    def setIpValues(self, localIP, extIp):
        self.localIp=localIP
        self.externIp=extIp

    def setPrinterName(self, printerName):
        self.printerName=printerName

    def __init__(self, path, parent=None):
        super(Label, self).__init__(parent=parent)
        self.path = path

    def paintEvent(self, e):

        super().paintEvent(e)
        qp = QPainter(self)
        if self.warningVisible is True:

            iL = 10
            jL = 10
            incw = 0
            inch = 155

            if self.printerOffline is True:
                qp.drawPixmap(iL, jL, QPixmap(self.path + "/printerOffline.png"))
                iL = iL + incw
                jL = jL + inch

            if self.paperEmpty is True:
                qp.drawPixmap(iL, jL, QPixmap(self.path + "/paperEmpty.png"))
                iL = iL + incw
                jL = jL + inch

            if self.ribbonEmpty is True:
                qp.drawPixmap(iL, jL, QPixmap(self.path + "/ribbonEmpty.png"))
                iL = iL + incw
                jL = jL + inch

            if self.trayMissing is True:
                qp.drawPixmap(iL, jL, QPixmap(self.path + "/trayMissing.png"))
                iL = iL + incw
                jL = jL + inch

            if self.ribbonMissing is True:
                qp.drawPixmap(iL, jL, QPixmap(self.path + "/ribbonMissing.png"))
                iL = iL + incw
                jL = jL + inch

            if self.hasVisibleWarning() is True:
                qp.drawPixmap(40, 768-170, QPixmap(self.path + "/printerHelp.png"))

        if self.debugVisible is True:

            w = 190
            h = 15
            x = 1024 - w - 10
            y = 5
            if self.localIp != "127.0.0.1":
                qp.drawText(QRect(x,y,w,h), Qt.AlignRight, "loc : " + self.localIp)
                y = y + h
            if self.externIp != "127.0.0.1":
                qp.drawText(QRect(x,y,w,h), Qt.AlignRight, "ext : " + self.externIp)
                y = y + h
            if self.printerName != "":
                qp.drawText(QRect(x,y,w,h), Qt.AlignRight, "printer : " + self.printerName + " (ON)")
                y = y + h
            else:
                qp.drawText(QRect(x,y,w,h), Qt.AlignRight, "printer : OFF")
                y = y + h


class ledStripControler():

    serialDevice = None
    logger = logging.getLogger("LedStripControl")

    class Color():

        BLUE = [0, 0, 255]
        GREEN = [0, 255, 0]
        RED = [255, 0, 0]
        LIGHT_BLUE = [0, 180, 255]
        WHITE = [255, 255, 255]
        ORANGE = [255, 180, 0]
        YELLOW = [255, 255, 0]
        BLACK = [0, 0, 0]

    class Location(Enum):

        RIGHT_SIDE = 1
        LEFT_SIDE = 2
        BOTH_SIDE = 3
        TEXT_BACK = 4
        CAMERA_ARROWS = 5
        CAMERA_BACK = 6
        ERROR = 7
        ALL = 8

    def __init__(self, port, speed, ressourceManager):

        self.ressourceManager = ressourceManager

        if EMULATE is True:
            self.logger.info("INITIALIZING LEDCONTROLER")
            return

        self.port = port
        self.speed = speed
        self.init()

    def init(self):

        try:

            self.serialDevice = serial.Serial(self.port)
            self.serialDevice.baudrate = self.speed

            self.setColor(self.Location.RIGHT_SIDE, [self.Color.BLUE])
            self.setColor(self.Location.LEFT_SIDE, [self.Color.BLUE])
            self.setColor(self.Location.CAMERA_ARROWS, [self.Color.BLUE, self.Color.BLACK])
            self.setColor(self.Location.CAMERA_BACK, [self.Color.RED])
            self.setColor(self.Location.TEXT_BACK, [self.Color.BLUE])
            self.setColor(self.Location.ERROR, [self.Color.RED, self.Color.GREEN])

        except:
            self.logger.error("LEDCONTROLER:SERIALDEVICE INIT EXCEPTION")

    def sendCommand(self, command, retryMax=4):

        if EMULATE is True:
            return

        retry = retryMax - 1
        exception = False

        if retry < 0:
            self.logger.error("LEDCONTROLER:TOO MUCH EXCEPTION IN SENDCOMMAND " + command)
            return

        try:
            self.serialDevice.write((command).encode('utf-8'))
        except serial.SerialException as e:
            self.logger.error("LEDCONTROLER:SENDCOMMAND:SERIAL.SERIALEXCEPTION " + str(e) + " command : " + command)
            exception = True
        except TypeError as e:
            self.logger.error("LEDCONTROLER:SENDCOMMAND:SERIAL.TYPEERROR " + str(e) + " command : " + command)
            exception = True
        except AttributeError as e:
            self.logger.error("LEDCONTROLER:SENDCOMMAND:SERIAL.ATTRIBUTEERROR " + str(e) + " command : " + command)
            exception = True

        if exception is True:
            self.init()
            self.sendCommand(command, retry)

    @pyqtSlot(int)
    def blinkFront(self, ms):
        self.logger.info("LEDCONTROLER:BLINKFRONT")
        self.sendCommand('4,' + str(ms) + ';')

    def setColor(self, location, colors):

        self.logger.info("LEDCONTROLER:SETCOLOR " + str(location) + str(colors))

        if location == self.Location.RIGHT_SIDE:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('6,' + str(r) + ',' + str(g) + ',' + str(b) + ';')

        if location == self.Location.LEFT_SIDE:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('7,' + str(r) + ',' + str(g) + ',' + str(b) + ';')

        if location == self.Location.CAMERA_ARROWS:
            r1 = colors[0][0]
            g1 = colors[0][1]
            b1 = colors[0][2]
            r2 = colors[1][0]
            g2 = colors[1][1]
            b2 = colors[1][2]
            self.sendCommand(
                '5,' + str(r1) + ',' + str(g1) + ',' + str(b1) + ',' + str(r2) + ',' + str(g2) + ',' + str(b2) + ';')

        if location == self.Location.CAMERA_BACK:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('9,' + str(r) + ',' + str(g) + ',' + str(b) + ';')

        if location == self.Location.TEXT_BACK:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('8,' + str(r) + ',' + str(g) + ',' + str(b) + ';')

        if location == self.Location.BOTH_SIDE:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('6,' + str(r) + ',' + str(g) + ',' + str(b) + ';')
            self.sendCommand('7,' + str(r) + ',' + str(g) + ',' + str(b) + ';')

        if location == self.Location.ERROR:
            r1 = colors[0][0]
            g1 = colors[0][1]
            b1 = colors[0][2]
            r2 = colors[1][0]
            g2 = colors[1][1]
            b2 = colors[1][2]
            self.sendCommand(
                '11,' + str(r1) + ',' + str(g1) + ',' + str(b1) + ',' + str(r2) + ',' + str(g2) + ',' + str(b2) + ';')

        if location == self.Location.ALL:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('5,' + str(r) + ',' + str(g) + ',' + str(b) + ';')
            self.sendCommand('6,' + str(r) + ',' + str(g) + ',' + str(b) + ';')
            self.sendCommand('7,' + str(r) + ',' + str(g) + ',' + str(b) + ';')
            self.sendCommand('8,' + str(r) + ',' + str(g) + ',' + str(b) + ';')
            self.sendCommand('9,' + str(r) + ',' + str(g) + ',' + str(b) + ';')
            self.sendCommand('11,' + str(r) + ',' + str(g) + ',' + str(b)
                             + ',' + str(r) + ',' + str(g) + ',' + str(b) + ';')

    def showWarning(self, isDefault):
        self.logger.info("LEDCONTROLER:SHOWDEFAULT " + str(isDefault))
        self.setBrightness(255)
        self.sendCommand('10,' + str(isDefault) + ';')

    def restart(self):
        self.logger.info("LEDCONTROLER:RESTART")
        self.sendCommand('3;')

    def setBrightness(self, brightness):
        self.logger.info("LEDCONTROLER:SETBRIGHTNESS")
        self.sendCommand('12,' + str(brightness) + ';')


if EMULATE is False:
    pyautogui.FAILSAFE = False

class MainWindow(QMainWindow):

    DebugGPIO = False
    boxSettings = None

    logger = logging.getLogger("MainWindow")

    printerNameSerial = {}

    def __init__(self, box_index):
        super(MainWindow, self).__init__()

        if box_index == 1:
            self.boxSettings = PhotoBoothSettings_1()
        elif box_index == 2:
            self.boxSettings = PhotoBoothSettings_2()
        else:
            self.boxSettings = PhotoBoothSettings_1()

        self.logger.info("####################################################################################")
        self.logger.info("##      NEW INSTANCE STARTED                            NEW INSTANCE STARTED      ##")
        self.logger.info("##                              NEW INSTANCE STARTED                              ##")
        self.logger.info("##      NEW INSTANCE STARTED                            NEW INSTANCE STARTED      ##")
        self.logger.info("####################################################################################")

        self.local_ip = "127.0.0.1"
        self.external_ip = "127.0.0.1"

        self.boxSettings.printDetails()

        self.interuptsConnected = False
        self.currentAssemblyPath = ""
        self.displayMode = DisplayMode.HOMEPAGE
        self.timeoutTimer = None
        self.showCuttingLines = False
        self.captureList = []
        self.lastAssemblyPixmap = None
        self.inputButtonThread = None
        self.label = None
        self.resources = None
        self.printingEnabled = False
        self.blinkState = 0
        self.button1LedEnabled = True
        self.button2LedEnabled = True
        self.button3LedEnabled = True
        self.topLightOn = False
        self.lastPrintId = 0
        self.lastAssemblyLandscape = 1
        self.DebugGPIO = False

        self.resources = ressourcesManager()
        self.resources.loadResources()
        self.resources.logInfos()

        self.logger.info("INITIALIZING PHOTOBOOTH")
        self.setDisplayMode(DisplayMode.UNDEFINED)
        self.initGPIO()
        self.switchOnLedStrip(True)

        self.ledStrip = ledStripControler("/dev/ttyUSB_LED_CONTROLLER", 115200, self.resources)
        self.ledStrip.showWarning(1)

        if EMULATE is True:
            self.show()
        else:
            self.showFullScreen()

        self.initGUI()

        self.showStartupPixmap()
        self.setLedButonBlinking(False, False, False)

        self.initSettings()
        self.initDevices()
        self.populatePrintersDictionary()
        self.initActions()
        self.initMenu()
        self.initDSLRTime()

        if self.boxSettings.has_printer_port() is True:
            self.printerMonitoring = PrinterMonitoringThread( self)
            self.printerMonitoring.start()

        printerSerial = self.getOnlinePrinters()

        if len(printerSerial) >= 1:
            self.setCurrentPrinter(self.getPrinterName(printerSerial[0]))
        else:
            self.setCurrentPrinter("")
        if self.boxSettings.has_printer_port() is True and self.printingEnabled is True:
            if self.printerName == "":
                self.showPowerOnPrinter()
            else:
                self.gotoStart()
                self.ledStrip.showWarning(0)
        else:
            self.gotoStart()
            self.ledStrip.showWarning(0)

        self.switchConstantLight(False)


    def refreshLedButtons(self):
        if self.displayMode == DisplayMode.HOMEPAGE:
            self.setLedButonBlinking(False, True, False)
            if self.label is not None:
                if self.boxSettings.has_printer_port() is True and self.printingEnabled is True:
                    if self.label.hasVisibleWarning() is True:
                        self.setLedButonBlinking(True, True, False)


    def populatePrintersDictionary(self):

        if EMULATE is True:
            return

        try:
            conn = cups.Connection()
            printers = conn.getPrinters()

            for printer in printers:
                if "Canon_CP800_" in printer:
                    id = printers[printer]["device-uri"].replace('gutenprint53+usb://canon-cp800/', '')
                    self.printerNameSerial[id] = printer

            # if len(self.printerNameSerial)==0:
            #     self.logger.error("PRINTER : CANNOT POPULATE printerNameSerial dic based on cups infos!")
            #     self.printerNameSerial ={   'DN00121700003777': 'Canon_CP800_0',
            #                                 'GL04120400020191': 'Canon_CP800_1',
            #                                 'G200090100000410': 'Canon_CP800_2',
            #                                 'DX01122500001574': 'Canon_CP800_3'}

            for key, value in self.printerNameSerial.items():
                self.logger.info("Printer name : " + value + ", id : " + key)

        except:

            if self.boxSettings.has_printer_port() is False or self.printingEnabled is False:
                self.logger.info("POPULATE PRINTER DICTIONNARY EXCEPTION, PRINTING DISABLED")
            else:
                self.logger.error("POPULATE PRINTER DICTIONNARY EXCEPTION, PRINTING ENABLED!!!")

    def getPrinterName(self,id):

        pName = ""
        if id in self.printerNameSerial.keys():
            pName = self.printerNameSerial[id]
        return pName

    def getOnlinePrinters(self):

        onlinePrinterSerials = []

        if EMULATE is True:
            return onlinePrinterSerials

        try:
            xdevV = usb.core.find(idVendor=0x04a9, idProduct=0x3214, find_all=True)
            for xdev in xdevV:
                if xdev._serial_number is None:
                    xdev._serial_number = usb.util.get_string(xdev, xdev.iSerialNumber)
                    onlinePrinterSerials.append(str(xdev._serial_number).strip())
        except:
            pass

        return onlinePrinterSerials

    def defineTimeout(self, delaySec):

        if self.timeoutTimer is None:
            self.logger.warning("NOT INITIALIZED VARIABLE : (self.timeoutTimer is None)")
            return

        if delaySec <= 0:
            self.logger.info("REMOVING TIMEOUT")
            self.timeoutTimer.stop()
        else:
            self.timeoutTimer.start(1000 * delaySec)
            self.logger.info("SETTING TIMEOUT TO " + str(delaySec) + " SECONDES")

    def initDSLRTime(self):

        self.logger.info("INITIALIZING DSLR DATETIME")

        if EMULATE is True:
            return

        subprocess.call("gphoto2 --set-config datetime=$(date +%s)", shell=True)

    def initSettings(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.printingEnabled = settings.value("printingEnabled", self.printingEnabled, bool)
        self.menuDelaySecond = 4
        self.menuOffsetSecond = 4
        self.menuDelaySecond = settings.value("menuDelaySecond", self.menuDelaySecond, int)
        self.menuOffsetSecond = settings.value("menuOffsetSecond", self.menuOffsetSecond, int)

    def initGUI(self):

        self.label = Label(self.resources.getPath(ressourcesManager.PATH.SKIN))

        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)

        self.label.setMinimumSize(self.boxSettings.getScreenResolution()[0], self.boxSettings.getScreenResolution()[1])
        self.label.setMaximumSize(self.boxSettings.getScreenResolution()[0], self.boxSettings.getScreenResolution()[1])
        self.setCentralWidget(self.label)
        self.cacheHomePicture()

        self.timeoutTimer = QTimer()
        self.timeoutTimer.timeout.connect(self.onTimeout)

    def cacheHomePicture(self):
        #used to speedup go home
        self.homeDisplay = self.resources.getPath(
            ressourcesManager.PATH.EVENT) + "/" + self.resources.homePageDisplayFilename

    def setDisplayMode(self, mode):

        if self.displayMode == mode:
            self.logger.warning(
                "CHANGING CURRENT MODE TO THE SAME MODE " + mode.name + "(" + str(mode.value) + ")")
        else:
            self.logger.info(
                "CHANGING CURRENT MODE " + self.displayMode.name + "(" + str(
                    self.displayMode.value) + ") to mode " + mode.name + "(" + str(mode.value) + ")")

        self.displayMode = mode

        #Only allow warning display on the home page
        if self.label is not None:
            if self.boxSettings.has_printer_port() is True and self.printingEnabled is True:
                if mode == DisplayMode.HOMEPAGE:
                        self.label.setWarningVisible(True)
                        self.label.setPrinterHelpButtonVisible(True)
                elif mode == DisplayMode.HELP_PRINTER:
                    self.label.setWarningVisible(True)
                    self.label.setPrinterHelpButtonVisible(False)
                else:
                    self.label.setWarningVisible(False)
                    self.label.setPrinterHelpButtonVisible(False)
            else:
                self.label.setWarningVisible(False)
                self.label.setPrinterHelpButtonVisible(False)

            if mode != DisplayMode.HOMEPAGE:
                self.label.setDebugVisible(False)

        if mode == DisplayMode.HOMEPAGE:
            self.label.setWarningVisible(True)
            self.defineTimeout(-1)

        elif mode == DisplayMode.PRINT:
            self.defineTimeout(-1)

        elif mode == DisplayMode.MENU:
            self.defineTimeout(-1)
            self.defineTimeout(40)

        elif mode == DisplayMode.POWER_PRINTER:
            self.defineTimeout(-1)
            self.defineTimeout(60 * 5)

        elif mode == DisplayMode.HELP_PRINTER:
            self.defineTimeout(-1)
            self.defineTimeout(60 * 5)

        elif mode == DisplayMode.MENU_SETUP:
            self.defineTimeout(-1)
            self.defineTimeout(40)

        elif mode == DisplayMode.COMPUTING:
            self.defineTimeout(-1)
            self.defineTimeout(60 * 4)

        elif mode == DisplayMode.VALIDATE:
            self.defineTimeout(-1)
            self.defineTimeout(30)

        elif mode == DisplayMode.DISPLAY_ASSEMBLY:
            self.defineTimeout(-1)
            self.defineTimeout(60 * 2)

        elif mode == DisplayMode.TRIGGER_ERROR:
            self.defineTimeout(-1)
            self.defineTimeout(30)

        elif mode == DisplayMode.RUNNING:
            self.defineTimeout(30)

        else:
            self.logger.error("DEFINETIMEOUT NOT DONE, " + mode.name + "(" + str(mode.value) + ") NOT HANDLED")
            self.defineTimeout(-1)
            self.defineTimeout(60)


    def showHomePage(self):

        if self.displayMode == DisplayMode.HOMEPAGE:
            return

        self.setDisplayMode(DisplayMode.HOMEPAGE)
        outPixmap = QPixmap(self.homeDisplay)
        self.label.setPixmap(outPixmap)
        self.refreshLedButtons()
        QApplication.processEvents()

    def showComputingPixmap(self):

        if self.displayMode == DisplayMode.COMPUTING:
            return

        self.setDisplayMode(DisplayMode.COMPUTING)
        self.logger.info("COMPUTING PAGE")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/computing.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def startPictureAssembly(self):

        self.logger.info("START PICTURE ASSEMBLY")
        QApplication.processEvents()
        QApplication.processEvents()
        QApplication.processEvents()
        self.startCaptureProcess()

    def startCaptureProcess(self):

        imPath = self.resources.getPath(ressourcesManager.PATH.CAPTURE) + "/" + str(uuid.uuid4()) + ".jpg"
        self.logger.info("CAPTURE PROCESS " + imPath)
        self.setDisplayMode(DisplayMode.RUNNING)
        self.disconnectInputButtonInterupts()

        self.setLedButonBlinking(False, False, False)

        countDown = 4
        for x in range(0, countDown):

            if x == 0:
                self.ledStrip.setColor(ledStripControler.Location.CAMERA_ARROWS, [ledStripControler.Color.BLUE, ledStripControler.Color.BLACK])
                self.ledStrip.blinkFront(400)
            if x == 1:
                self.ledStrip.setColor(ledStripControler.Location.CAMERA_ARROWS, [ledStripControler.Color.BLUE, ledStripControler.Color.BLACK])
                self.ledStrip.blinkFront(300)
            if x == 2:
                self.ledStrip.setColor(ledStripControler.Location.CAMERA_ARROWS, [ledStripControler.Color.BLUE, ledStripControler.Color.BLACK])
                self.ledStrip.blinkFront(200)
                self.switchConstantLight(True)

            delay = self.showPixmap(countDown - x, False, False, False)
            self.wait(0.6 - delay)
            delay = self.showPixmap(0, True, False, False)
            self.wait(0.6 - delay)

        captureThread = CaptureImageThread(imPath, self.resources, self.boxSettings)
        captureThread.signal.connect(self.onCaptureProcessFinished)
        self.start = time.time()
        self.ledStrip.setColor(ledStripControler.Location.CAMERA_ARROWS, [ledStripControler.Color.BLUE, ledStripControler.Color.BLACK])

        captureThread.start()

        self.showPixmap(0, True, True, False)
        self.wait(2.7)
        self.showPixmap(0, False, False, True)
        self.switchConstantLight(False)

    def onCaptureProcessFinished(self, result, capture):

        if result is True:
            self.logger.info("CAPTURE PROCESS FINISHED TRUE :" + str(time.time() - self.start) + "s")
            self.showValidatingPage(capture)
        else:
            self.logger.warning("CAPTURE PROCESS FINISHED FALSE")
            self.showTriggerErrorPage()

        self.switchConstantLight(False)

    def showValidatingPage(self, capture):

        self.logger.info("SHOW VALIDATION PAGE")
        self.setDisplayMode(DisplayMode.VALIDATE)
        self.lastCapture = capture
        self.disconnectInputButtonInterupts()
        self.setLedButonBlinking(False, False, False)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        hideB1 = len(self.captureList) >= 3
        validatePixmap = self.getFilteredPixmap(QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/validate-capture.png"),
                                                hideB1, QColor(255,255,255,80),
                                                False, None,
                                                False, None)

        painter.drawPixmap(0, 0, validatePixmap)

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


            else:
                preview = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/avatar.png")
                painter.translate(x, y)
                painter.drawPixmap(0, 0,
                                   preview.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
                pen = QPen(Qt.gray)
                pen.setWidth(3)

            painter.setPen(pen)
            painter.drawRect(0, 0, w, h)

            painter.translate(-x, -y)

        self.label.setPixmap(outPixmap)
        del painter

        QApplication.processEvents()
        self.connectInputButtonInterupts()
        self.setLedButonBlinking(not hideB1, True, True)

    def buildNextAssembly(self):

        self.logger.info("BUILD NEXT ASSEMBLY")
        choosenLayout = self.resources.chooseNextLayout(len(self.captureList))

        if choosenLayout == None:
            return

        self.lastAssemblyPixmap = None
        self.lastAssemblyLandscape = choosenLayout["landscape"]
        #display assembly page without the assembly itself
        self.showAssemblyPixmap()
        [self.lastAssemblyPixmap, self.currentAssemblyPath] = self.resources.buildLayoutFromList(captureList=self.captureList,
                                                                                                 choosenLayout=choosenLayout,
                                                                                                 showCuttingLine=self.showCuttingLines)

        #display assembly page without the assembly we just build
        self.showAssemblyPixmap()

    def getFilteredPixmap(self, pixmapPath, hideButton1, color1, hideButton2, color2, hideButton3,color3):

        assPixmap = QPixmap(pixmapPath)
        painterFrame = QPainter(assPixmap)
        painterFrame.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        w = assPixmap.size().width()
        h = assPixmap.size().height()

        color = Qt.transparent

        if hideButton1 is True:
            c = color
            if color1 is not None:
                c = color1
            painterFrame.fillRect(0, h - h / 5, w / 3 + 60, h / 5 + 1, c)

        if hideButton2 is True:
            c = color
            if color2 is not None:
                c = color2
            painterFrame.fillRect(w / 3, h - h / 5, w / 3 + 1, h / 5 + 1, c)

        if hideButton3 is True:
            c = color
            if color3 is not None:
                c = color3
            painterFrame.fillRect(w * 2 / 3, h - h / 5, w / 3 + 1, h / 5 + 1, c)

        painterFrame.end()
        del painterFrame
        return assPixmap

    def showAssemblyPixmap(self):

        self.logger.info("SHOW ASSEMBLY PAGE")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)


        hideB3 = self.boxSettings.has_printer_port() is False or self.printingEnabled is False or self.printerName==""
        cB3 = None

        if self.printingEnabled is True and self.printerName=="" and self.boxSettings.has_printer_port() is True:
            cB3 = QColor(255,255,255,80)

        assPixmap = self.getFilteredPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/assembly.png",
                                           False, None,
                                           False, None,
                                           hideB3, cB3
                                           )

        painter.drawPixmap(0, 0, assPixmap)

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

        self.logger.info("SHOW MENU PAGE")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/menu.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def showPowerOnPrinter(self):

        if self.displayMode == DisplayMode.POWER_PRINTER:
            return

        self.setDisplayMode(DisplayMode.POWER_PRINTER)
        self.logger.info("SHOW POWER ON PRINTER")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/power_printer.png"))
        self.label.setPixmap(outPixmap)
        del painter
        self.connectInputButtonInterupts()
        self.setLedButonBlinking(False, True, False)


    def showHelpPrinter(self):

        self.setDisplayMode(DisplayMode.HELP_PRINTER)
        self.logger.info("SHOW HELP FOR PRINTER")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/help_printer.png"))
        self.label.setPixmap(outPixmap)
        del painter
        self.connectInputButtonInterupts()
        self.setLedButonBlinking(True, True, True)


    def showStartupPixmap(self):

        self.logger.info("SHOW STARTUP PAGE")
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/startup.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def showShutdownPixmap(self):

        self.logger.info("SHOW SHUTDOWN PAGE")

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/shutdown.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

    def showGoHomePixmap(self):

        self.logger.info("SHOW GO HOME PAGE")

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

        if self.boxSettings.is_LedPullUp() is False:
            onValue = 0
        else:
            onValue = 1

        if self.blinkState == 0:
            self.blinkState = 1
        else:
            self.blinkState = 0

        if self.button1LedEnabled:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_1), self.blinkState)
        else:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_1), onValue)

        if self.button2LedEnabled:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_2), self.blinkState)
        else:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_2), onValue)

        if self.button3LedEnabled:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_3), self.blinkState)
        else:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_3), onValue)

    def onButton1Pressed(self):

        delay = self.menuDelaySecond
        offset = self.menuOffsetSecond
        reset_default = [0, 2]
        reprint = [reset_default[1] + offset, reset_default[1] + offset + delay]
        shutdown = [reprint[1] + 3*offset, reprint[1] + 3*offset + delay]
        menu = [shutdown[1] + offset, shutdown[1] + offset + delay]
        menu_advanced = [menu[1] + offset, menu[1] + offset + delay]

        if self.DebugGPIO is True:
            self.logger.info("BUTTON 1 PRESSED")
            self.setLedButonBlinking(True, False, False)
            self.ledStrip.showWarning(0)
            return

        if self.interuptsConnected is False:
            return

            self.logger.info("BUTTON 1 PRESSED")

        if self.displayMode == DisplayMode.HOMEPAGE:
            self.logger.info("BUTTON 1 PRESSED : 4 POSSIBLE ACTIONS")
            self.logger.info("SHOW PRINTER HELP ONLY IF WARNING : " + str(reset_default[0]) + "s to " + str(reset_default[1]) + "s")
            self.logger.info("RE PRINT LAST PHOTO  : " + str(reprint[0]) + "s to " + str(reprint[1]) + "s")
            self.logger.info("SHUTDOWN PHOTOBOOTH  : " + str(shutdown[0]) + "s to " + str(shutdown[1]) + "s")
            self.logger.info("SHOW MENU            : " + str(menu[0]) + "s to " + str(menu[1]) + "s")
            self.logger.info("SHOW EXPERT MENU     : " + str(menu_advanced[0]) + "s to " + str(menu_advanced[1]) + "s")

            start = time.time()
            duration = 0
            if EMULATE is False:
                while GPIO.input(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_1)) == 0:
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
                if self.label.hasVisibleWarning() is True:
                    self.showHelpPrinter()
            elif duration >= reprint[0] and duration < reprint[1]:
                self.logger.info("BUTTON 1 PRESSED : RESET PRINTER ERROR, PRINT LAST ASSEMBLY")
                self.sendPrintingJob()
            elif duration >= shutdown[0] and duration < shutdown[1]:
                self.logger.info("BUTTON 1 PRESSED : SHUTDOWN")
                self.onShutdown()
            elif duration >= menu[0] and duration < menu[1]:
                self.logger.info("BUTTON 1 PRESSED : SHOW MENU")
                self.onShowMenu()
            elif duration >= menu_advanced[0] and duration < menu_advanced[1]:
                self.logger.info("BUTTON 1 PRESSED : SHOW MENU ADVANCED")
                self.onShowAdvancedMenu()

        elif self.displayMode == DisplayMode.PRINT:
            self.logger.warning("BUTTON 1 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.MENU:
            self.logger.info("BUTTON 1 PRESSED : TRIGGER ACTION MENU")
            self.onRightButtonGPIO()

        elif self.displayMode == DisplayMode.MENU_SETUP:
            self.logger.info("BUTTON 1 PRESSED : TRIGGER ACTION MENU")
            self.onRightButtonGPIO()

        elif self.displayMode == DisplayMode.COMPUTING:
            self.logger.warning("BUTTON 1 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.VALIDATE:
            if len(self.captureList) < 3:
                self.logger.info("BUTTON 1 PRESSED : PHOTO VALIDATED")
                self.storeLastCapture()
                self.startCaptureProcess()
            else:
                self.logger.warning("BUTTON 1 PRESSED : NO OPTION MAP TO THIS BUTTON IMAGES NUMBER >= 4")

        elif self.displayMode == DisplayMode.DISPLAY_ASSEMBLY:
            self.logger.info("BUTTON 1 PRESSED : OTHER ASSEMBLY")
            self.redoAssembly()

        elif self.displayMode == DisplayMode.TRIGGER_ERROR:
            self.logger.warning("RETRYING CAPTURE ")
            self.startCaptureProcess()

        elif self.displayMode == DisplayMode.RUNNING:
            self.logger.warning("BUTTON 1 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.POWER_PRINTER:
            self.logger.warning("BUTTON 1 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.HELP_PRINTER:
            self.logger.warning("BUTTON 1 PRESSED : GOTO START")
            self.resetPrinterErrors()
            self.enablePrinter()
            self.cancelAllNotCompletedJobs()
            self.gotoStart()
            self.label.setDebugVisible(True)
            self.label.update()

        else:
            self.logger.warning(
                "BUTTON 1 PRESSED : THIS MODE (" + str(self.displayMode.value) + ") IS NOT HANDLED.")

    def onButton3Pressed(self):

        delay = self.menuDelaySecond
        offset = self.menuOffsetSecond
        reset_default = [0, 2]
        reprint = [reset_default[1] , reset_default[1] + delay]
        shutdown = [reprint[1] + 3*offset, reprint[1] + 3*offset + delay]
        menu = [shutdown[1] + 3*offset, shutdown[1] + 3*offset + delay]
        menu_advanced = [menu[1] + 3*offset, menu[1] + 3*offset + delay]

        if self.DebugGPIO is True:
            self.logger.info("BUTTON 3 PRESSED")
            self.setLedButonBlinking(False, False, True)
            self.ledStrip.showWarning(1)
            return

        if self.interuptsConnected is False:
            return

        self.logger.info("BUTTON 3 PRESSED")

        if self.displayMode == DisplayMode.HOMEPAGE:
            self.logger.info("BUTTON 3 PRESSED : 4 POSSIBLE ACTIONS")

            self.logger.info("RESET PRINTER ERRORS : " + str(reset_default[0]) + "s to " + str(reset_default[1]) + "s")
            self.logger.info("RE PRINT LAST PHOTO  : " + str(reprint[0]) + "s to " + str(reprint[1]) + "s")
            self.logger.info("SHUTDOWN PHOTOBOOTH  : " + str(shutdown[0]) + "s to " + str(shutdown[1]) + "s")
            self.logger.info("SHOW MENU            : " + str(menu[0]) + "s to " + str(menu[1]) + "s")
            self.logger.info("SHOW EXPERT MENU     : " + str(menu_advanced[0]) + "s to " + str(menu_advanced[1]) + "s")

            start = time.time()
            duration = 0
            if EMULATE is False:
                while GPIO.input(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_3)) == 0:
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
                self.logger.info("BUTTON 3 PRESSED : RESET PRINTER ERROR, CANCEL LAST PRINT")
                self.resetPrinterErrors()
                self.enablePrinter()
                self.cancelAllNotCompletedJobs()
#                self.printerMonitoring.resume()
                self.gotoStart()
                self.label.setDebugVisible(True)
                self.label.update()
            elif duration >= reprint[0] and duration < reprint[1]:
                self.logger.info("BUTTON 3 PRESSED : RESET PRINTER ERROR, PRINT LAST ASSEMBLY")
                self.sendPrintingJob()
            elif duration >= shutdown[0] and duration < shutdown[1]:
                self.logger.info("BUTTON 3 PRESSED : SHUTDOWN")
                self.onShutdown()
            elif duration >= menu[0] and duration < menu[1]:
                self.logger.info("BUTTON 3 PRESSED : SHOW MENU")
                self.onShowMenu()
            elif duration >= menu_advanced[0] and duration < menu_advanced[1]:
                self.logger.info("BUTTON 3 PRESSED : SHOW MENU ADVANCED")
                self.onShowAdvancedMenu()

        elif self.displayMode == DisplayMode.PRINT:
            self.logger.warning("BUTTON 3 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.MENU:
            self.logger.info("BUTTON 3 PRESSED : MENU BACK")
            self.onLeftButtonGPIO()


        elif self.displayMode == DisplayMode.MENU_SETUP:
            self.logger.info("BUTTON 3 PRESSED : MENU BACK")
            self.onLeftButtonGPIO()

        elif self.displayMode == DisplayMode.COMPUTING:
            self.logger.warning("BUTTON 3 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.VALIDATE:
            self.logger.info("BUTTON 3 PRESSED : PHOTO VALIDATED CREATE ASSEMBLY")
            self.storeLastCapture()
            self.resources.resetChoices()
            self.redoAssembly()

        elif self.displayMode == DisplayMode.DISPLAY_ASSEMBLY:
            if self.boxSettings.has_printer_port() is True and self.printingEnabled is True and self.printerName != "":
                self.logger.info("BUTTON 3 PRESSED : PRINT")
                self.sendPrintingJob()
            else:
                self.logger.info("BUTTON 3 PRESSED : PRINT NOT ENABLED, DO NOTHING")

        elif self.displayMode == DisplayMode.TRIGGER_ERROR:

            self.logger.warning("IGNORING THIS CAPTURE ")
            if len(self.captureList) < self.resources.nbImageMax:
                self.startCaptureProcess()

            else:
                self.redoAssembly()


        elif self.displayMode == DisplayMode.RUNNING:
            self.logger.warning("BUTTON 3 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.POWER_PRINTER:
            self.logger.warning("BUTTON 3 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.HELP_PRINTER:
            self.logger.info("BUTTON 3 PRESSED : RESET PRINTER ERROR, PRINT LAST ASSEMBLY OR START CAPTURE")
            exists = os.path.isfile(self.currentAssemblyPath)
            if exists:
                self.sendPrintingJob()
            else:
                self.startCaptureProcess()
        else:
            self.logger.warning(
                "BUTTON 3 PRESSED : THIS MODE (" + str(self.displayMode.value) + ") IS NOT HANDLED.")

    def onButton2Pressed(self):

        capture = [0, 2]
        constant_light = [4, 8]

        if self.DebugGPIO is True:
            self.logger.info("BUTTON 2 PRESSED")
            self.setLedButonBlinking(False, True, False)
            self.ledStrip.blinkFront(300)
            return

        if self.interuptsConnected is False:
            return

        self.logger.info("BUTTON 2 PRESSED")

        if self.displayMode == DisplayMode.HOMEPAGE:

            start = time.time()
            stop = 0
            duration = 0
            if EMULATE is False:
                while GPIO.input(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_2)) == 0:
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
                self.logger.info("BUTTON 2 PRESSED : START ASSEMBLY")
                self.startPictureAssembly()

            elif duration < constant_light[1] and duration >= constant_light[0]:
                self.logger.info("BUTTON 2 PRESSED : TOGGLE TOP LIGHT")
                self.topLightOn = not self.topLightOn
                self.switchConstantLight(self.topLightOn)
                self.showHomePage()

        elif self.displayMode == DisplayMode.PRINT:
            self.logger.warning("BUTTON 2 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.POWER_PRINTER:
            self.logger.info("BUTTON 2 PRESSED : POWER_PRINTER ACK -> HOMEPAGE")

            printerSerial = self.getOnlinePrinters()

            if len(printerSerial) >= 1:
                self.setCurrentPrinter(self.getPrinterName(printerSerial[0]))
            else:
                self.setCurrentPrinter("")
                #self.printerMonitoring.resume()

            self.ledStrip.showWarning(0)
            self.gotoStart()
            self.switchConstantLight(False)

        elif self.displayMode == DisplayMode.MENU:
            self.logger.info("BUTTON 2 PRESSED : NAVIGATE MENU")
            self.onDownButtonGPIO()

        elif self.displayMode == DisplayMode.MENU_SETUP:
            self.logger.info("BUTTON 2 PRESSED : NAVIGATE MENU")
            self.onDownButtonGPIO()

        elif self.displayMode == DisplayMode.COMPUTING:
            self.logger.warning("BUTTON 2 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.VALIDATE:
            self.logger.info("BUTTON 2 PRESSED : REDO LAST PICTURE")
            self.startCaptureProcess()

        elif self.displayMode == DisplayMode.DISPLAY_ASSEMBLY:
            self.logger.info("BUTTON 2 PRESSED : DISPLAY_ASSEMBLY -> HOMEPAGE")
            self.gotoStart()

        elif self.displayMode == DisplayMode.TRIGGER_ERROR:
            self.logger.warning(
                "BUTTON 2 PRESSED : CANCELING")
            self.gotoStart()

        elif self.displayMode == DisplayMode.RUNNING:
            self.logger.warning("BUTTON 2 PRESSED : NO OPTION MAP TO THIS BUTTON")

        elif self.displayMode == DisplayMode.HELP_PRINTER:
            self.logger.info("BUTTON 2 PRESSED : GO BACK TO HOME")
            self.gotoStart()

        else:
            self.logger.warning(
                "BUTTON 2 PRESSED : THIS MODE (" + str(self.displayMode.value) + ") IS NOT HANDLED.")

    def resetPrinterErrors(self):

        self.disconnectInputButtonInterupts()
        self.setLedButonBlinking(False, False, False)
        self.label.setRibbonEmpty(False)
        self.label.setRibbonMissing(False)
        self.label.setTrayMissing(False)
        self.label.setPaperEmpty(False)
        self.label.setPrinterOffline(False)
        self.ledStrip.showWarning(0)

    @pyqtSlot(int)
    def onInputButtonPressed(self, channel):

        if channel == self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_1):
            self.onButton1Pressed()
        elif channel == self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_2):
            self.onButton2Pressed()
        elif channel == self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_3):
            self.onButton3Pressed()

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

        self.setDisplayMode(DisplayMode.MENU)
        self.setLedButonBlinking(False, False, False)
        self.showPixmapMenu()
        self.updateMenu(False)
        self.contextMenu.exec_(QPoint(30, 200))
        self.logger.info("SHOW MENU")
        self.setLedButonBlinking(True, True, True)
        if self.displayMode == DisplayMode.MENU:
            self.gotoStart()

    def storeLastCapture(self):

        self.logger.info("STORE CAPTURE")
        self.captureList.append(self.lastCapture)

    @pyqtSlot()
    def setImagequality0(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("imagequality", 0)
        self.logger.info("SET IMAGE QUALITY=0")

        if EMULATE is False:
            subprocess.call("gphoto2 --set-config imagequality=0", shell=True)

    @pyqtSlot()
    def setImagequality1(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("imagequality", 1)
        self.logger.info("SET IMAGE QUALITY=1")
        if EMULATE is False:
            subprocess.call("gphoto2 --set-config imagequality=1", shell=True)

    @pyqtSlot()
    def setImagequality2(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("imagequality", 2)
        self.logger.info("SET IMAGE QUALITY=2")
        if EMULATE is False:
            subprocess.call("gphoto2 --set-config imagequality=2", shell=True)

    def setCurrentPrinter(self, printerName):

        if printerName == self.printerName:
            return
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.printerName = printerName
        self.label.setPrinterName(printerName)
        settings.setValue("printerName", self.printerName)
        self.enablePrinter()
        self.cancelAllNotCompletedJobs()


    @pyqtSlot()
    def onSetCurrentPrinter(self):

        if self.sender().text() == self.printerName:
            return

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.printerName = self.sender().text()
        settings.setValue("printerName", self.printerName)
        self.enablePrinter()


    def wait(self, delay):

        if EMULATE is True:
            time.sleep(delay/10)
            return
        try:
            time.sleep(delay)
        except ValueError as e:
            self.logger.error("TIME.SLEEP EXCEPTION " + str(e))

    @pyqtSlot()
    def onSetCurrentEvent(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("event", self.sender().text())
        self.resources.loadResources()
        self.resources.logInfos()
        self.cacheHomePicture()

    @pyqtSlot()
    def onSetCurrentSkin(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("skin", self.sender().text())
        self.resources.loadResources()
        self.cacheHomePicture()

    @pyqtSlot()
    def onSetCurrentBackGround(self):
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("background", self.sender().text())
        self.resources.loadResources()
        self.cacheHomePicture()

    @pyqtSlot()
    def onShowAllTestAssemblies(self):

        self.onShowAssemblyCalibration1()
        self.wait(5)
        self.onShowAssemblyCalibration2()
        self.wait(5)
        self.onShowAssemblyCalibration3()
        self.wait(5)
        self.onShowAssemblyCalibration4()

    @pyqtSlot()
    def onShowAssemblyCalibration1(self):
        self.buildCalibrationAssembly(1)

    @pyqtSlot()
    def onShowAssemblyCalibration2(self):
        self.buildCalibrationAssembly(2)

    @pyqtSlot()
    def onShowAssemblyCalibration3(self):
        self.buildCalibrationAssembly(3)

    @pyqtSlot()
    def onShowAssemblyCalibration4(self):
        self.buildCalibrationAssembly(4)

    def buildCalibrationAssembly(self, n):

        self.showCuttingLines = True
        self.captureList.clear()
        for i in range(n):
            self.captureList.append(QPixmap(self.resources.getPath(ressourcesManager.PATH.CALIBRATION_IMAGE)))
        self.redoAssembly()


    def initActions(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.imagequality = settings.value("imagequality", 0, int)
        self.printerName = ""
        #settings.value("printerName", "Canon_CP800_0")
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

        # printerList = ["Canon_CP800_0","Canon_CP800_1","Canon_CP800_2","Canon_CP800_3"]
        # self.printerNameSerial.values()

        self.printerActionList=[]
        for f in self.printerNameSerial.values():
            act = QAction(f, self)
            act.setCheckable(True)
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

        self.local_ip = self.get_ip()
        self.external_ip = "127.0.0.1"

        try:
            self.external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        except urllib.error.URLError as e:
            print(e)

        self.label.setIpValues(self.local_ip,self.external_ip)


    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


    @pyqtSlot(QAction)
    def onMoveMouseAbove(self, act):

        if self.lastAct != act:
            self.lastAct = act
            QToolTip.showText(QPoint(0,0), act.toolTip())


    def initMenu(self):

        self.lastAct = None

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.printingEnabled = settings.value("printingEnabled", True, bool)

        self.contextMenu = QMenu("Context menu", self)

        self.dataMenu = QMenu("Données",self)
        self.settingMenu = QMenu("Réglages",self)
        self.displayMenu = QMenu("Affichage",self)
        self.eventMenu = QMenu("Evennement",self)
        self.functionalitiesMenu = QMenu("Fonctionalités",self)

        self.dataMenu.addAction(self.actionCleanCaptures)
        self.dataMenu.addAction(self.actionCleanAssemblies)
        self.dataMenu.addAction(self.actionCleanEventDatas)

        self.dslrMenu  = QMenu(self.boxSettings.getCameraName(),self)
        self.settingMenu.addMenu(self.dslrMenu)

        self.speedLightMenu = QMenu("Eclairage flash", self)
        self.speedLightMenu.addAction(self.actionEnableSpeedLight)
        self.speedLightMenu.addAction(self.actionRestartSpeedLight)

        if self.boxSettings.has_external_flash() is True:
            self.settingMenu.addMenu(self.speedLightMenu)

        self.constantLightMenu = QMenu("Eclairage constant", self)
        self.constantLightMenu.addAction(self.actionEnableConstantLight)
        self.constantLightMenu.addAction(self.actionSwitchOnConstantLight)
        self.constantLightMenu.addAction(self.actionSwitchOffConstantLight)

        if self.boxSettings.has_constant_light() is True:
            self.settingMenu.addMenu(self.constantLightMenu)

        self.printerMenu = QMenu("Impression", self)
        self.cupsMenu = QMenu("Cups", self)
        self.printerMenu.addAction(self.actionEnablePrinting)
        self.printerMenu.addMenu(self.cupsMenu)
        self.printerMenu.addActions(self.printerActionList)
        self.cupsMenu.addAction(self.actionRestartCups)
        self.cupsMenu.addAction(self.actionStartCups)
        self.cupsMenu.addAction(self.actionStopCups)

        if self.boxSettings.has_printer_port() is True:
            self.settingMenu.addMenu(self.printerMenu)

        if self.boxSettings.can_restart_DSLR() is True:
            self.dslrMenu.addAction(self.actionRestartDSLR)

        self.dslrMenu.addAction(self.actionImagequality0)
        self.dslrMenu.addAction(self.actionImagequality1)
        self.dslrMenu.addAction(self.actionImagequality2)

        self.backgroundMenu  = QMenu("Arriere plan",self)
        self.backgroundMenu.hovered.connect(self.onMoveMouseAbove)
        self.skinMenu  = QMenu("Theme",self)
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

        self.logger.error("TRIGGER CAPTURE ERROR")
        self.setDisplayMode(DisplayMode.TRIGGER_ERROR)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/on-error.png"))
        self.label.setPixmap(outPixmap)
        del painter
        QApplication.processEvents()

        self.setLedButonBlinking(True, True, True)
        self.connectInputButtonInterupts()

    def onShowAdvancedMenu(self):

        self.setDisplayMode(DisplayMode.MENU_SETUP)
        self.setLedButonBlinking(False, False, False)
        self.showPixmapMenu()
        self.updateMenu(True)
        self.contextMenu.exec_(QPoint(30, 200))

        self.logger.info("SHOW MENU")
        self.setLedButonBlinking(True, True, True)

        if self.displayMode == DisplayMode.MENU_SETUP:
            self.gotoStart()

    @pyqtSlot()
    def cleanCaptures(self):

        self.logger.info("ERASE CAPTURES")
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.CAPTURE))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.CAPTURE))

    @pyqtSlot()
    def cleanEventDatas(self):

        self.logger.info("ERASE ALL")
        self.cleanAssemblies()
        self.cleanCaptures()

    @pyqtSlot()
    def cleanAssemblies(self):

        self.logger.info("ERASE ASSEMBLIES")
        shutil.rmtree(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES))
        os.mkdir(self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES))

    @pyqtSlot()
    def toogleEnableSpeedlight(self):

        self.logger.info("ENABLE SPEEDLIGHT")
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        enable = not settings.value("speedLightEnabled", True, bool)
        settings.setValue("speedLightEnabled", enable)
        self.switchSpeedLight(enable)

    @pyqtSlot()
    def restartSpeedLight(self):

        self.logger.info("RESTART SPEEDLIGHT")
        if EMULATE is True:
            return

        if self.boxSettings.has_external_flash() is True and self.boxSettings.can_restart_external_flash() is True:
            self.switchSpeedLight(False)
            self.wait(2)
            self.switchSpeedLight(True)

    @pyqtSlot()
    def restartDSLR(self):

        self.logger.info("RESTART DSLR")
        if EMULATE is True:
            return
        if self.boxSettings.can_restart_DSLR() is True:
            self.switchDSLR(False)
            self.wait(2)
            self.switchDSLR(True)

    def initDevicesFast(self):

        self.logger.info("INIT DEVICES FAST")
        self.switchDSLR(True)

    def initDevices(self):

        self.logger.info("INIT DEVICES")
        self.restartDSLR()
        self.restartSpeedLight()
        QApplication.processEvents()
        self.startCUPS()
        self.switchConstantLight(True)

    @pyqtSlot()
    def toogleEnablePrinting(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.printingEnabled = not settings.value("printingEnabled", True, bool)
        settings.setValue("printingEnabled", self.printingEnabled)
        if self.printingEnabled is False:
            self.stopCUPS()
        else:
            self.startCUPS()

    @pyqtSlot()
    def restartCUPS(self):

        self.logger.info("RESTARTING CUPS")
        if EMULATE is True:
            return

        if self.boxSettings.has_printer_port() is False or self.printingEnabled is False:
            return

        subprocess.Popen(["/etc/init.d/cups", "restart"])

    @pyqtSlot()
    def startCUPS(self):

        self.logger.info("STARTING CUPS")

        if EMULATE is True:
            return

        if self.boxSettings.has_printer_port() is False or self.printingEnabled is False:
            return

        subprocess.Popen(["/etc/init.d/cups", "start"])

    @pyqtSlot()
    def stopCUPS(self):

        self.logger.info("STOPING CUPS")

        if EMULATE is True:
            return

        if self.boxSettings.has_printer_port() is False or self.printingEnabled is False:
            return

        subprocess.Popen(["/etc/init.d/cups", "stop"])

    @pyqtSlot()
    def onShutdown(self):

        self.showShutdownPixmap()
        self.logger.info("ARRET NORMAL DU PHOTOBOOTH")

        if EMULATE is False:
            self.switchSpeedLight(False)
            self.switchDSLR(False)
            self.setLedButonBlinking(False, False, False)
            self.ledStrip.setColor(ledStripControler.Location.RIGHT_SIDE, [ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.LEFT_SIDE, [ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.CAMERA_ARROWS, [ledStripControler.Color.BLACK, ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.CAMERA_BACK, [ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.TEXT_BACK, [ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.ERROR, [ledStripControler.Color.BLACK, ledStripControler.Color.BLACK])

        self.command("shutdown")

    @pyqtSlot()
    def onReboot(self):

        self.showShutdownPixmap()
        self.logger.info("REDEMARRAGE NORMAL DU PHOTOBOOTH")

        if EMULATE is False:
            self.switchSpeedLight(False)
            self.switchDSLR(False)
            self.setLedButonBlinking(False, False, False)
            self.ledStrip.setColor(ledStripControler.Location.RIGHT_SIDE, [ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.LEFT_SIDE, [ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.CAMERA_ARROWS, [ledStripControler.Color.BLACK, ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.CAMERA_BACK, [ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.TEXT_BACK, [ledStripControler.Color.BLACK])
            self.ledStrip.setColor(ledStripControler.Location.ERROR, [ledStripControler.Color.BLACK, ledStripControler.Color.BLACK])
        self.command("reboot")

    @pyqtSlot()
    def onGenerateAllSingleAssemblies(self):

        self.logger.info("GENERATE ALL SINGLE ASSEMBLIES")
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


    def switchOnLedStrip(self, on):

        if EMULATE is True:
            return
        
        if self.boxSettings.has_led_strip() is True and self.boxSettings.can_restart_led_strip() is True:
            if on is True:
                GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.RELAY_LED_STRIP), 0)
            else:
                GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.RELAY_LED_STRIP), 1)
            time.sleep(0.5)


    def initGPIO(self):

        self.logger.info("INITIALIZING PARSPBERRY PI GPIOS.")

        if EMULATE is True:
            return

        GPIO.cleanup()

        # GPIO IN 20 wired

        GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_3), GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_2), GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.BUTTON_1), GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_3), GPIO.OUT, initial=1)
        GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_2), GPIO.OUT, initial=1)
        GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.LED_BUTTON_1), GPIO.OUT, initial=1)

        if self.boxSettings.has_constant_light() is True:
            GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.RELAY_POWER_TOP_LIGHT), GPIO.OUT, initial=0)

        if self.boxSettings.has_led_strip() is True and self.boxSettings.can_restart_led_strip() is True:
            GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.RELAY_LED_STRIP), GPIO.OUT, initial=0)

        if  self.boxSettings.has_external_flash() is True and self.boxSettings.can_restart_external_flash() is True:
            GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.POWER_SPEEDLIGHT), GPIO.OUT, initial=1)
            GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.ON_OFF_SPEEDLIGHT), GPIO.OUT, initial=1)

        if self.boxSettings.can_restart_DSLR() is True:
            GPIO.setup(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.POWER_DSLR), GPIO.OUT, initial=1)

        self.blinkingTimer = QTimer()
        self.blinkingTimer.timeout.connect(self.blink)
        self.blinkingTimer.start(300)

        self.inputButtonThread = InputButtonThread(self.boxSettings)
        self.disconnectInputButtonInterupts()
        self.inputButtonThread.start()

    def switchConstantLight(self, on):

        if self.boxSettings.has_constant_light() is False:
            self.logger.info("NO CONSTANT LIGHT ON THIS DEVICE")
            return

        self.logger.info("CONSTANT LIGHT SWITCHED TO " + str(on))
        if EMULATE is True:
            return

        if on is True:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.RELAY_POWER_TOP_LIGHT), 0)
        else:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.RELAY_POWER_TOP_LIGHT), 1)

    @pyqtSlot()
    def toogleEnableConstantLight(self):

        if self.boxSettings.has_constant_light() is False:
            self.logger.info("NO CONSTANT LIGHT ON THIS DEVICE")
            return

        self.logger.info("ENABLE CONSTANT LIGHT")
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        constantLightEnabled = not settings.value("constantLightEnabled", True, bool)
        settings.setValue("constantLightEnabled", constantLightEnabled)
        self.switchConstantLight(constantLightEnabled)
        if constantLightEnabled is True:
            self.wait(2)
            self.switchConstantLight(False)

    @pyqtSlot()
    def switchOnConstantLight(self):
        self.switchConstantLight(True)

    @pyqtSlot()
    def switchOffConstantLight(self):
        self.switchConstantLight(False)


    def testRelays(self):

        GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.RELAY_POWER_TOP_LIGHT), 0)
        self.wait(2)
        GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.RELAY_LED_STRIP), 0)
        self.wait(2)

    def switchSpeedLight(self, on):

        if EMULATE is True:
            return

        if self.boxSettings.has_external_flash() is False or self.boxSettings.can_restart_external_flash() is False:
            return

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        en = settings.value("speedLightEnabled", True, bool)

        if on is True and en is True:

            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.POWER_SPEEDLIGHT), 0)
            self.wait(1)
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.ON_OFF_SPEEDLIGHT), 0)
            self.wait(2)
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.ON_OFF_SPEEDLIGHT), 1)

        else:

            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.ON_OFF_SPEEDLIGHT), 0)
            self.wait(2)
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.ON_OFF_SPEEDLIGHT), 1)
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.POWER_SPEEDLIGHT), 1)
            self.wait(1)

    def switchDSLR(self, on):

        if EMULATE is True:
            return

        if self.boxSettings.can_restart_DSLR() is False:
            return

        if on is True:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.POWER_DSLR), 0)
            self.wait(1)
        else:
            GPIO.output(self.boxSettings.getGPIO(PhotoBoothSettings.GPIOPin.POWER_DSLR), 1)
            self.wait(1)

    @pyqtSlot()
    def onTimeout(self):

        self.defineTimeout(-1)

        if self.displayMode == DisplayMode.HOMEPAGE:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED DO NOTHING")
            pass

        elif self.displayMode == DisplayMode.PRINT:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.displayMode == DisplayMode.MENU:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            if EMULATE is True:
                self.gotoStart()
                return
            try:
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
            except pyautogui.FailSafeException as e:
                print(e)

            self.gotoStart()

        elif self.displayMode == DisplayMode.MENU_SETUP:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            if EMULATE is True:
                self.gotoStart()
                return
            try:
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
                pyautogui.press('esc')
            except pyautogui.FailSafeException as e:
                print(e)
            self.gotoStart()

        elif self.displayMode == DisplayMode.COMPUTING:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.displayMode == DisplayMode.VALIDATE:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED BUTTON 3 EMULATED")
            self.onButton3Pressed()

        elif self.displayMode == DisplayMode.DISPLAY_ASSEMBLY:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.displayMode == DisplayMode.TRIGGER_ERROR:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED BUTTON 3 EMULATED")
            self.onButton3Pressed()

        elif self.displayMode == DisplayMode.RUNNING:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.displayMode == DisplayMode.POWER_PRINTER:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.ledStrip.showWarning(0)
            self.gotoStart()

        elif self.displayMode == DisplayMode.HELP_PRINTER:
            self.logger.info(self.displayMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        else:
            self.logger.error(self.displayMode.name + "(" + str(self.displayMode.value) + ")" + "NOT HANDLED -> TIMEOUT GO HOME")
            self.gotoStart()


    def redoAssembly(self):

        self.setDisplayMode(DisplayMode.DISPLAY_ASSEMBLY)
        self.disconnectInputButtonInterupts()
        self.setLedButonBlinking(False, False, False)
        self.wait(0.2)
        QApplication.processEvents()
        self.buildNextAssembly()
        self.setLedButonBlinking(True, True, self.boxSettings.has_printer_port() is True and self.printingEnabled is True and self.printerName != "")
        self.connectInputButtonInterupts()
        QApplication.processEvents()

    def connectInputButtonInterupts(self):

        self.logger.info("ENABLE BUTTON HANDLER")
        if EMULATE is True:
            if self.interuptsConnected is False:
                self.interuptsConnected = True
            return
        if self.interuptsConnected is False:
            self.inputButtonThread.inputButtonEventDetected.connect(self.onInputButtonPressed)
            self.interuptsConnected = True
            QApplication.processEvents()

    def disconnectInputButtonInterupts(self):

        self.logger.info("DISABLE BUTTON HANDLER")
        if EMULATE is True:
            if self.interuptsConnected is True:
                self.interuptsConnected = False
            return
        if self.interuptsConnected is True:
            self.inputButtonThread.inputButtonEventDetected.disconnect(self.onInputButtonPressed)
            self.interuptsConnected = False
            QApplication.processEvents()

    def sendPrintingJob(self):

        if self.boxSettings.has_printer_port() is False:
            self.gotoStart()
            return

        if self.printingEnabled is False:
            self.gotoStart()
            return

        if EMULATE is True:
            self.showPrintSentPage()
            self.wait(3)
            self.gotoStart()
            return

        printerSerial = self.getOnlinePrinters()

        if len(printerSerial) >= 1:
            self.setCurrentPrinter(self.getPrinterName(printerSerial[0]))
        else:
            self.setCurrentPrinter("")

        if self.printerName == "":
            self.gotoStart()
            return

        self.disconnectInputButtonInterupts()
        self.setLedButonBlinking(False, False, False)
        self.enablePrinter()

        self.resetPrinterErrors()

        self.cancelAllNotCompletedJobs()
        try:
            conn = cups.Connection()

            exists = os.path.isfile(self.currentAssemblyPath)
            if exists:
                self.lastPrintId = conn.printFile(self.printerName, self.currentAssemblyPath, title='boxaselfi_job',
                                                  options={})
                self.logger.info(
                    "NEW JOB PRINT(" + str(self.lastPrintId) + ") : " + self.currentAssemblyPath)
                self.showPrintSentPage()
                self.wait(13)
            else:
                self.logger.error("NEW JOB PRINT : " + self.currentAssemblyPath + "file does not exists")
        except:
            self.logger.error("sendPrintingJob EXCEPTION")
        self.gotoStart()

    def cancelNotCompletedJobs(self):

        if self.boxSettings.has_printer_port() is False or self.printingEnabled is False:
            return

        try:
            conn = cups.Connection()
            # printers = conn.getPrinters()
            for key, val in conn.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1).items():
                if key != self.lastPrintId:
                    self.logger.info("CANCEL JOB ID : " + str(key))
                    conn.cancelJob(key, purge_job=False)
                else:
                    self.logger.info("DO NOT CANCEL LAST JOB ID : " + str(key))
        except:
            self.logger.error("cancelNotCompletedJobs EXCEPTION")

    def cancelAllNotCompletedJobs(self):

        if self.boxSettings.has_printer_port() is False or self.printingEnabled is False:
            return

        try:
            conn = cups.Connection()
            # printers = conn.getPrinters()
            for key, val in conn.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1).items():
                self.logger.info("CANCEL JOB ID : " + str(key))
                conn.cancelJob(key, purge_job=False)
        except:
            self.logger.error("cancelAllNotCompletedJobs EXCEPTION")

    def enablePrinter(self):

        if self.boxSettings.has_printer_port() is False or self.printingEnabled is False:
            return

        if self.printerName in self.printerNameSerial.values():
            try:
                conn = cups.Connection()
                conn.enablePrinter(self.printerName)

                self.logger.info("ENABLE PRINTER " + self.printerName)
            except:
                self.logger.error("ENABLE PRINTER CUPS EXCEPTION")


    def showPrintSentPage(self):

        self.logger.info("SHOW NEW PRINT JOB SENT")
        self.setDisplayMode(DisplayMode.PRINT)
        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/printing.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showReleaseForSwitchConstantLightPage(self):

        if (self.displayMode == DisplayMode.INFO_SWITCH_CONSTANT_LIGHT):
            return
        self.logger.info("SHOW RELEASE TO SWITCH CONSTANT LIGHT")
        self.setDisplayMode(DisplayMode.INFO_SWITCH_CONSTANT_LIGHT)
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

        if (self.displayMode == DisplayMode.INFO_SHUTDOWN):
            return
        self.logger.info("SHOW RELEASE TO SHUTDOWN")
        self.setDisplayMode(DisplayMode.INFO_SHUTDOWN)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/info-shutdown.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showReleaseForMenuPage(self):

        if (self.displayMode == DisplayMode.INFO_MENU):
            return
        self.logger.info("SHOW RELEASE FO MENU")
        self.setDisplayMode(DisplayMode.INFO_MENU)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/info-menu.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showReleaseForAdvancedMenuPage(self):

        if (self.displayMode == DisplayMode.INFO_MENU_ADVANCED):
            return
        self.logger.info("SHOW RELEASE FOR ADVANCED MENU")
        self.setDisplayMode(DisplayMode.INFO_MENU_ADVANCED)

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

        if (self.displayMode == DisplayMode.INFO_REPRINT):
            return
        self.logger.info("SHOW RELEASE FOR REPRINT")
        self.setDisplayMode(DisplayMode.INFO_REPRINT)

        outPixmap = None
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.BACKGROUND_IMAGE))
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/info-reprint.png"))
        del painter
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def erasePrinterStatusBox(self):

        self.logger.info("JOB PRINT STATUS : CLEANING THE LIST")
        self.printJobStatusList = []

    def gotoStart(self):

        self.showCuttingLines = False
        self.logger.info("GO HOME")
        self.connectInputButtonInterupts()
        self.captureList.clear()
        self.showHomePage()

    def setLedButonBlinking(self, bt1, bt2, bt3):

        self.setButton1LedEnabled(bt1)
        self.setButton2LedEnabled(bt2)
        self.setButton3LedEnabled(bt3)
        QApplication.processEvents()
        QApplication.processEvents()
        QApplication.processEvents()

    def setButton1LedEnabled(self, enabled):

        self.button1LedEnabled = enabled

    def setButton3LedEnabled(self, enabled):

        self.button3LedEnabled = enabled

    def setButton2LedEnabled(self, enabled):

        self.button2LedEnabled = enabled

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
            self.setLedButonBlinking(False, False, False)
            self.ledStrip.setColor(ledStripControler.Location.ALL, [ledStripControler.Color.BLACK])

        exit(140)

    def generateAllSingleAssemblies(self, inputFolder, outputFolder):

        self.showComputingPixmap()
        self.disconnectInputButtonInterupts()
        self.setLedButonBlinking(False, False, False)

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
        self.wait(1)


class SimulatorButtonThread(QThread):

    logger = logging.getLogger("SimulatorButton")
    def __init__(self, mm, delay):
        QThread.__init__(self)
        self.mainWindow = mm
        self.delay = delay
        self.logger.info("SIMULATOR STARTED WITH DELAY OF " + str(self.delay) + " SEC.")

    def run(self):
        while True:
            j = random.randint(1, 3)
            time.sleep(self.delay)
            self.logger.info("BUTTON " + str(j) + " SIMULATED.")
            if j == 1:
                self.mainWindow.onButton1Pressed()
            if j == 2:
                self.mainWindow.onButton2Pressed()
            if j == 3:
                self.mainWindow.onButton3Pressed()


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s][%(levelname)7s] [%(name)15s-%(lineno)5s] > %(message)s",
        handlers=[
            logging.FileHandler("../photobooth-datas/logs/trace.log"),
            logging.StreamHandler()
        ]
    )

    app = QApplication(sys.argv)

    args = sys.argv[1:]
    n=1
    if len(args) >= 2 and len(args) <= 4 and args[0] == '-photobooth':
        n = int(args[1])
    else :
        print("ERROR : USAGE -photobooth <int> photobooth_number [1..n]")
        sys.exit(1)
    dsim = -1
    if len(args) == 4 and args[2] == '-simulate':
        dsim = int(args[3])
    else :
        print("USAGE -simulate <int> simulation delay msec [500ms, -> 50000ms]")

    if isinstance(n, int) is False :
        sys.exit(1)

    mainWin = MainWindow(n)

    if dsim > 0:
        mainWin.generateRandomIO(dsim/1000.0)

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
        mainWin.setLedButonBlinking(False, False, False)
        mainWin.ledStrip.setColor(ledStripControler.Location.ALL,[ledStripControler.Color.BLACK])

        GPIO.cleanup()

    sys.exit(ret)
