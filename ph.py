#!/usr/bin/env python

try:
    print("Importing PyQt5")    
    from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QRectF, QSettings, QSize,
                              Qt, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QDateTime, QIODevice, QElapsedTimer)
    from PyQt5.QtGui import QIcon, QKeySequence, QFont, QPixmap, QPainter, QPen, QColor, QMovie
    from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow)
except:
    print("PyQt5 import error")
    
try:
    print("Importing platform") 
    import platform

    if platform.system() == 'Windows':
        EMULATE = True
    else:
        EMULATE = False

        try:
            print("Importing GPIO") 
            import RPi.GPIO as GPIO
        except:
            print("GPIO import error")
        try:
            print("Importing pyautogui") 
            import pyautogui
        except:
            print("pyautogui import error")
except:
    print("platform import error")
        
try:
    print("Importing randint, randrange") 
    from random import randint, randrange
except:
    print("randint, randrange import error")

try:
    print("Importing datetime") 
    from datetime import datetime
except:
    print("datetime import error")
try:
    print("Importing ressourceManager") 
    from ressourceManager import *
except:
    print("ressourceManager import error")
try:
    print("Importing Queue") 
    from six.moves.queue import Queue
except:
    print("Queue import error")

try:
    print("Importing threading, time, random, shutil, os, subprocess") 
    import threading, time, random, shutil, os, subprocess
except:
    print("threading, time, random, shutil, os, subprocess import error")
try:
    print("Importing cups") 
    import cups
except:
    print("cups import error")
try:
    print("Importing glob") 
    import glob
except:
    print("glob import error")
try:
    print("Importing json") 
    import json
except:
    print("json import error")
try:
    print("Importing Popen, PIPE, check_output") 
    from subprocess import Popen, PIPE, check_output
except:
    print("Popen, PIPE, check_output import error")
try:
    print("Importing uuid")     
    import uuid
except:
    print("uuid import error")
try:
    print("Importing Enum")     
    from enum import Enum,IntEnum  
except:
    print("Enum import error")

try:
    print("Importing serial")     
    import serial  
except:
    print("Enum import serial")


class ColorLED():
    BLUE=[0,0,255]
    GREEN=[0,255,0]
    RED=[255,0,0]
    LIGHT_BLUE=[0,180,180]

class GPIOPin(IntEnum):

    LED_LEFT = 6
    LED_DOWN = 26
    LED_RIGHT = 13
    LED_0 = 19
    
    BUTTON_LEFT = 20
    BUTTON_DOWN = 16
    BUTTON_RIGHT = 12
    BUTTON_0 = 21
    
    RELAY_POWER_TOP_LIGHT = 17
    RELAY_LED_STRIP = 4
    RELAY_2 = 23
    RELAY_3 = 22
    
    WIRE_3_4 = 23
    WIRE_3_5 = 24
    WIRE_3_6 = 25




class GPIOMode(Enum):

    HOMEPAGE = 1
    PRINT = 2
    MENU = 3
    MENU_SETUP = 4
    COMPUTING = 5
    VALIDATE = 6
    DISPLAY_ASSEMBLY = 7
    TRIGGER_ERROR = 8
    RUNNING = 8


if EMULATE is False:
    GPIO.setmode(GPIO.BCM)

class PrinterMonitoringThread(QThread):
    printerFailure = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')
    label = None
    def __init__(self,label,led):
        QThread.__init__(self,label)
        self.label=label
        self.led=led
        # run method gets called when we start the thread
    def run(self):

        while True:
            conn = cups.Connection()
            printers = conn.getPrinters ()
            for printer in printers:
            
                if printers[printer]['printer-state'] == 5:
                    if printers[printer]["printer-state-message"] == "No paper tray loaded, aborting!":
                        print("no more paper, contact smbdy to add papers again")
                        self.printerFailure.emit(printer, 1)
                        self.label.setTrayMissingLeft(True)
                        self.label.setTrayMissingRight(True)
                        self.led.showWarning(1)
                                

                if printers[printer]['printer-state'] == 3:
                    if printers[printer]["printer-state-message"] == "Ribbon depleted!":
                        print("Carttouche d'encre vide, contact smbdy to add papers again")
                        self.printerFailure.emit(printer, 2)
                        self.label.setRibbonEmptyLeft(True)
                        self.label.setRibbonEmptyRight(True)
                        self.led.showWarning(1)

                    if printers[printer]["printer-state-message"] =="Paper feed problem!" :
                        print("Plus de papier, veuillez en rajouter")
                        self.printerFailure.emit(printer, 3)
                        self.label.setPaperEmptyLeft(True)
                        self.label.setPaperEmptyRight(True)
                        self.led.showWarning(1)

            time.sleep(2)
            self.label.update()
            


class InputButtonThread(QThread):
    inputButtonEventDetected = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.queue = Queue()
        if EMULATE is False:
            GPIO.add_event_detect(GPIOPin.BUTTON_LEFT, GPIO.FALLING, callback=self.queue.put, bouncetime=500)
            GPIO.add_event_detect(GPIOPin.BUTTON_RIGHT, GPIO.FALLING, callback=self.queue.put, bouncetime=500)
            GPIO.add_event_detect(GPIOPin.BUTTON_DOWN, GPIO.FALLING, callback=self.queue.put, bouncetime=500)
        # GPIO 20 wired also

    def run(self):
        while True: 
            self.inputButtonEventDetected.emit(self.queue.get())


class CaptureImageThread(QThread):
    signal = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, path):
        QThread.__init__(self)
        self.capture = path

    # run method gets called when we start the thread
    def run(self):

        camera = "Nikon DSC D3200"

#        camera = "Nikon DSC D70s (PTP mode)"

        p = Popen(["gphoto2", "--camera", camera, "--capture-image-and-download",
                   "--filename=" + self.capture], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode

        if len(err) > 0:
            ressourcesManager().getLogger().addError(str(err))
            self.signal.emit(False, None)
        else:
            print(err)
            self.signal.emit(True, self.capture)


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
        self.path=path

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
            qp.drawPixmap(iL, jL, QPixmap(self.path+"/ribbonEmpty.png"))
            iL = iL + incw
            jL = jL + inch
        if self.trayMissingLeft is True:
            qp.drawPixmap(iL, jL, QPixmap(self.path+"/trayMissing.png"))
            iL = iL + incw
            jL = jL + inch
        if self.paperEmptyLeft is True:
            qp.drawPixmap(iL, jL, QPixmap(self.path+"/paperEmpty.png"))

        if self.ribbonEmptyRight is True:
            qp.drawPixmap(iR, jR, QPixmap(self.path+"/ribbonEmpty.png"))
            iR = iR + incw
            jR = jR + inch
        if self.trayMissingRight is True:
            qp.drawPixmap(iR, jR, QPixmap(self.path+"/trayMissing.png"))
            iR = iR + incw
            jR = jR + inch
        if self.paperEmptyRight is True:
            qp.drawPixmap(iR, jR, QPixmap(self.path+"/paperEmpty.png"))


class ledControler():
    
    class LEDLocation(Enum):

        RIGHT_SIDE = 1
        LEFT_SIDE = 2
        BOTH_SIDE = 3
        TEXT_BACK = 4
        CAMERA_ARROWS = 5
        CAMERA_BACK = 6
        ERROR = 7
    
    def __init__(self,port,speed):    
        try:  
            #self.serialDevice=serial.Serial ("/dev/ttyUSB0")
            #self.serialDevice.baudrate = 115200
            self.port=port
            self.speed=speed
            self.serialDevice=serial.Serial (port)
            self.serialDevice.baudrate = speed
        except:
            print("serialDevice init exception")    
    
    def sendCommand(self,command):
        try:
            self.serialDevice.write((command).encode('utf-8'))
        except:
            print("sendCommand exception")  
    
    def blinkFront(self,ms):
        print("blinkFront")
        self.sendCommand('4,'+str(ms)+';')
                
    def setColor(self, location, colors):
        print("setColor")
        if location==self.LEDLocation.RIGHT_SIDE:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('6,'+str(r)+',' +str(g)+',' +str(b)+';')
        if location==self.LEDLocation.LEFT_SIDE:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('7,'+str(r)+',' +str(g)+',' +str(b)+';')
        if location==self.LEDLocation.CAMERA_ARROWS:
            r1 = colors[0][0] 
            g1 = colors[0][1] 
            b1 = colors[0][2] 
            r2 = colors[1][0] 
            g2 = colors[1][1] 
            b2 = colors[1][2] 
            self.sendCommand('5,'+str(r1)+','+str(g1)+','+str(b1)+','+str(r2)+','+str(g2)+','+str(b2)+';')
            
        if location==self.LEDLocation.CAMERA_BACK:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('9,'+str(r)+',' +str(g)+',' +str(b)+';')
            
        if location==self.LEDLocation.TEXT_BACK:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('8,'+str(r)+',' +str(g)+',' +str(b)+';')
                    
        if location==self.LEDLocation.BOTH_SIDE:
            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            self.sendCommand('6,'+str(r)+',' +str(g)+',' +str(b)+';')
            self.sendCommand('7,'+str(r)+',' +str(g)+',' +str(b)+';')
            
        if location==self.LEDLocation.ERROR:
            r1 = colors[0][0] 
            g1 = colors[0][1] 
            b1 = colors[0][2] 
            r2 = colors[1][0] 
            g2 = colors[1][1] 
            b2 = colors[1][2] 
            self.sendCommand('11,'+str(r1)+','+str(g1)+','+str(b1)+','+str(r2)+','+str(g2)+','+str(b2)+';')
            
        
        
    def showWarning(self,isDefault):
        print("showDefault " + str(isDefault))
        if isDefault==1:
            self.setBrightness(255)
        else:
            self.setBrightness(180)
        self.sendCommand('10,'+str(isDefault)+';')
     
            
    def restart(self):
        print("restart")
        self.sendCommand('3;')     
            
    def setBrightness(self,brightness):
        print("setBrightness")
        self.sendCommand('12,'+str(brightness)+';')
        
    

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.interuptsConnected = False
        self.currentAssemblyPath = ""
        self.currentGPIOMode=GPIOMode.HOMEPAGE
        self.timeoutTimer=None
                
        self.captureList = []
        self.lastAssemblyPixmap = None
        self.inputButtonThread = None
        self.movie = None
        self.label = None
        self.resources = None

        self.printingEnabled = False
        self.sharingEnabled = True

        self.resources = ressourcesManager()
        self.resources.loadCurrentXmlSkinDescriptor()
        self.resources.logInfos()
        self.resources.getLogger().addInfo("INITIALIZING PHOTOBOOTH")

        # DSLR SETTINGS
        self.Wcapture = 3008
        self.Hcapture = 2000

        # PHOTBOOTH GPIO SETTINGS


        #self.GPIO_POWER_SPEEDLIGHT = 23
        #self.GPIO_ON_OFF_SPEEDLIGHT = 25
        #self.GPIO_POWER_DSLR = 24
        #self.GPIO_POWER_PRINTER = 23

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
        
        self.initGPIO()
                
        self.led = ledControler("/dev/ttyS0",115200)
        
        self.led.setColor(ledControler.LEDLocation.RIGHT_SIDE,[ColorLED.LIGHT_BLUE])
        self.led.setColor(ledControler.LEDLocation.LEFT_SIDE,[ColorLED.LIGHT_BLUE])
        self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS,[ColorLED.BLUE,ColorLED.LIGHT_BLUE])
        self.led.setColor(ledControler.LEDLocation.CAMERA_BACK,[ColorLED.RED])
        self.led.setColor(ledControler.LEDLocation.TEXT_BACK,[ColorLED.LIGHT_BLUE])
        self.led.setColor(ledControler.LEDLocation.ERROR,[ColorLED.RED,ColorLED.GREEN])

        self.led.showWarning(1)
        
        self.showFullScreen()        

        self.initGUI()
        
        self.setCurrentMode(GPIOMode.HOMEPAGE)
        self.showStartupPixmap()
        QApplication.processEvents()
        QApplication.processEvents()
        self.switchLed(True, True, True)
        QApplication.processEvents()
        QApplication.processEvents()
        
        self.initSettings()
        
        self.testRelays()

        #self.initDevices()
        #self.initDevicesFast()

        self.initActions()
        self.initMenu()
        self.initAdvancedMenu()

        self.initDSLRTime()
        
        self.printerMonitoring = PrinterMonitoringThread(self.label, self.led)
        self.printerMonitoring.start()
        
        self.gotoStart()
        self.resources.getLogger().addInfo("PHOTOBOOTH READY TO USE")

        self.led.showWarning(0)
        

    def testGPIO(self):
        
        for i in range(30):
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        i=0
        while 1:
            if i>=30:
                i=0
            if i != 6 and i != 13 and i != 19 and i != 26:
                if GPIO.input(i) == 0:
                    print("GPIO " + str(i))
            i=i+1
        GPIO.cleanup()
        

        #print("tes gpio output mode")
        #for i in range(30):
            #print("Test GPIO " + str(i) + " output Begin" )
            #GPIO.setup(i, GPIO.OUT)
            #pwm = GPIO.PWM(i, 150)
            #pwm.start(30)
            #time.sleep(2)
            #print("Test GPIO " + str(i) + " output End" )
        #GPIO.cleanup()


    def initDSLRTime(self):
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
        self.printer1="CP800"
        self.printer2="CP760"
        self.sharingEnabled = settings.value("sharingEnabled", self.sharingEnabled, bool)

    def initGUI(self):

        self.label = Label(self.resources.getPath(ressourcesManager.PATH.APPLICATION)+"/resources/skins/default/")

        self.label.setFont(QFont("Right Chalk", 110, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        self.label.setMinimumSize(self.screenWidth, self.screenHeight)
        self.label.setMaximumSize(self.screenWidth, self.screenHeight)

        self.setCentralWidget(self.label)

        self.homeDisplay = self.resources.getPath(ressourcesManager.PATH.EVENT) + "/" + self.resources.homePageDisplayFilename
        
        self.movie = None
        
        if self.homeDisplay.endswith(('.gif')):

            self.movie = QMovie(self.homeDisplay)
            self.movie.setCacheMode(QMovie.CacheAll)
            self.movie.loopCount()

        self.timeoutTimer = QTimer()
        self.timeoutTimer.timeout.connect(self.onTimeout)

    def setCurrentMode(self, mode):

        if self.currentGPIOMode == mode:
            self.resources.getLogger().addWarning(
                "CHANGING CURRENT MODE TO THE SAME MODE " + mode.name + "(" + str(mode.value) + ")")
        else:
            self.resources.getLogger().addInfo(
                "CHANGING CURRENT MODE " + self.currentGPIOMode.name + "(" + str(self.currentGPIOMode.value) + ") to mode " + mode.name + "(" + str(mode.value) + ")")

        self.currentGPIOMode = mode

        if mode == GPIOMode.HOMEPAGE:
            self.defineTimeout(-1)

        elif mode == GPIOMode.PRINT:
            self.defineTimeout(-1)

        elif mode == GPIOMode.MENU:
            self.defineTimeout(-1)
            self.defineTimeout(40)

        elif mode == GPIOMode.MENU_SETUP:
            self.defineTimeout(-1)
            self.defineTimeout(40)

        elif mode == GPIOMode.COMPUTING:
            self.defineTimeout(-1)
            self.defineTimeout(240)

        elif mode == GPIOMode.VALIDATE:
            self.defineTimeout(-1)
            self.defineTimeout(30)

        elif mode == GPIOMode.DISPLAY_ASSEMBLY:
            self.defineTimeout(-1)
            self.defineTimeout(120)

        elif mode == GPIOMode.TRIGGER_ERROR:
            self.defineTimeout(-1)
            self.defineTimeout(30)

        elif mode == GPIOMode.RUNNING:
            self.defineTimeout(30)

    def showHomePage(self):

        if self.movie is None:
            outPixmap = QPixmap(self.homeDisplay)
            self.label.setPixmap(outPixmap)
        
        else:
            self.label.setMovie(self.movie)
            self.movie.start()
        QApplication.processEvents()

    def showComputingPixmap(self):

        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/computing.png")
        self.label.setPixmap(outPixmap)
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
        
        imPath = self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB) + "/" + str(uuid.uuid4()) + ".jpg"
        self.resources.getLogger().addInfo("CAPTURE PROCESS " + imPath)
        self.setCurrentMode(GPIOMode.RUNNING)
        self.disconnectInputButtonInterupts()
                
        self.switchLed(False, False, False)
        QApplication.processEvents()
        QApplication.processEvents()
        QApplication.processEvents()

        self.countDown = 4
        for x in range(0, self.countDown):
            
            if x == 0:
                self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS,[ColorLED.RED,ColorLED.BLUE])
                self.led.blinkFront(400)
            if x == 1 :
                self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS,[ColorLED.RED,ColorLED.BLUE])
                self.led.blinkFront(300)
            if x == 2 :
                self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS,[ColorLED.RED,ColorLED.BLUE])
                self.led.blinkFront(200)
                self.switchTopLight(True)

            delay = self.showPixmap(0, self.countDown - x, True, False, False, False, False, False)
            time.sleep(1 - delay)

        self.showPixmap(0, 0, True, True, False, False, False, False)

        captureThread = CaptureImageThread(imPath)
        captureThread.signal.connect(self.onCaptureProcessFinished)
        self.start = time.time()       
        self.led.setColor(ledControler.LEDLocation.CAMERA_ARROWS,[ColorLED.BLUE,ColorLED.LIGHT_BLUE])
                
        captureThread.start()

        time.sleep(0.7)
        self.showPixmap(0, 0, True, True, True, False, False, False)
        self.showPixmap(0, 0, True, False, False, False, True, False)


    def onCaptureProcessFinished(self, result, capture):

        if result is True:
            self.resources.getLogger().addInfo("CAPTURE PROCESS FINISHED TRUE :" + str(time.time()-self.start) + "s")
            self.showValidatingPage(capture)
        else:
            self.resources.getLogger().addWarning("CAPTURE PROCESS FINISHED FALSE")
            self.showTriggerErrorPage()
        
        self.switchTopLight(False)
            

    def showValidatingPage(self, capture):

        self.resources.getLogger().addInfo("SHOW VALIDATION PAGE")
        self.setCurrentMode(GPIOMode.VALIDATE)
        self.lastCapture = capture
        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/validatePicture1.png")

        x0 = 120
        y0 = 200
        w = 450
        h = 300
        b = 20

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

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
                pen = QPen(Qt.gray)
                pen.setWidth(5)

            elif i == len(self.captureList):
                preview = QPixmap(capture)
                pen = QPen(Qt.white)
                pen.setWidth(10)

            else:
                preview = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/avatar.png")
                pen = QPen(Qt.gray)
                pen.setWidth(3)

            painter.translate(x, y)
            painter.drawPixmap(0, 0, preview.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            painter.setPen(pen)
            painter.drawRect(0, 0, w, h)

            painter.translate(-x, -y)

        self.label.setPixmap(outPixmap)
        del painter

        QApplication.processEvents()
        self.connectInputButtonInterupts()
        self.switchLed(True, True, True)

    def buildShuffleAssembly(self):
                                                    
        self.resources.getLogger().addInfo("BUILD SHUFFLE ASSEMBLY")

        choosenLayout = self.resources.chooseRandomLayout(len(self.captureList))

        if choosenLayout == None:
            return

        self.lastAssemblyPixmap = None
        self.lastAssemblyLandscape = choosenLayout["landscape"]
        self.showAssemblyPixmap()
        [self.lastAssemblyPixmap, self.currentAssemblyPath] = self.resources.buildLayoutFromList(self.captureList,
                                                                                                 choosenLayout)
        self.showAssemblyPixmap()

    def showAssemblyPixmap(self):

        self.resources.getLogger().addInfo("SHOW ASSEMBLY PAGE")

        templatePixmap = None
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

            painter.translate(x, y)
            p = self.lastAssemblyPixmap.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, p)
            pen = QPen(Qt.white)
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawRect(0, 0, p.width(), p.height())

            painter.translate(-x, -y)

        self.label.setPixmap(templatePixmap)
        del painter
        QApplication.processEvents()

    def showPixmapMenu(self):

        self.resources.getLogger().addInfo("SHOW MENU PAGE")
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/menu.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showStartupPixmap(self):

        self.resources.getLogger().addInfo("SHOW STARTUP PAGE")
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/startup.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showShutdownPixmap(self):

        self.resources.getLogger().addInfo("SHOW SHUTDOWN PAGE")
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/shutdown.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def showGoHomePixmap(self):

        self.resources.getLogger().addInfo("SHOW GO HOME PAGE")
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
        if end - start >= 1:
            return 1
        else:
            return end - start

    def blink(self):

        if self.blinkState==0:
            self.blinkState = 1
        else:
            self.blinkState = 0

        if self.buttonRightLedEnabled:
            GPIO.output(GPIOPin.LED_RIGHT, self.blinkState)
        else:
            GPIO.output(GPIOPin.LED_RIGHT, 0)

        if self.buttonLeftLedEnabled:
            GPIO.output(GPIOPin.LED_LEFT, self.blinkState)
        else:
            GPIO.output(GPIOPin.LED_LEFT, 0)

        if self.buttonDownLedEnabled:
           GPIO.output(GPIOPin.LED_DOWN, self.blinkState)
        else:
            GPIO.output(GPIOPin.LED_DOWN, 0)


    def onRightButtonPressed(self):
        
        if self.interuptsConnected is False:
            return

        if self.currentGPIOMode == GPIOMode.HOMEPAGE:
            self.resources.logger.addInfo("RIGHT PRESSED :  4 POSSIBLE ACTIONS")
            start = time.time()
            stop = 0
            duration = 0
            if EMULATE is False:
                while GPIO.input(GPIOPin.BUTTON_RIGHT) == 0:
                    time.sleep(0.2)
            duration = (time.time() - start)

            if duration < 2:
                self.resources.logger.addInfo("RIGHT PRESSED : RESET PRINTER ERROR, CANCEL LAST PRINT")
                self.resetPrinterErrors()
                self.enablePrinter()
                self.cancelAllNotCompletedJobs()
                self.printerMonitoring.start()
                self.gotoStart()
            elif duration >= 3 and duration < 8:
                self.resources.logger.addInfo("RIGHT PRESSED : RESET PRINTER ERROR, PRINT LAST ASSEMBLY")
                self.sendPrintingJob()
            elif duration >= 8 and duration < 15:
                self.resources.logger.addInfo("RIGHT PRESSED : SHUTDOWN")
                self.onShutdown()
            elif duration >= 15 and duration < 20:
                self.resources.logger.addInfo("RIGHT PRESSED : SHOW MENU")
                if EMULATE is False:
                    self.onShowMenu()
            elif duration >= 20:
                self.resources.logger.addInfo("RIGHT PRESSED : SHOW MENU ADVANCED")
                self.onShowAdvancedMenu()
            
            

        elif self.currentGPIOMode == GPIOMode.PRINT:
            self.resources.logger.addWarning("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.MENU:
            self.resources.logger.addInfo("RIGHT PRESSED : TRIGGER ACTION MENU")
            self.onRightButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.MENU_SETUP:
            self.resources.logger.addInfo("RIGHT PRESSED : TRIGGER ACTION MENU")
            self.onRightButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            self.resources.logger.addWarning("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.VALIDATE:
            self.resources.logger.addInfo("RIGHT PRESSED : PHOTO VALIDATED")
            self.storeLastCapture()
            if len(self.captureList) >= 4:
                self.redoAssembly()
            else:
                self.startCaptureProcess()

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            self.resources.logger.addInfo("RIGHT PRESSED : OTHER ASSEMBLY")
            self.redoAssembly()

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR:
            self.resources.logger.addWarning("RETRYING CAPTURE ")
            self.startCaptureProcess()

        elif self.currentGPIOMode == GPIOMode.RUNNING:
            self.resources.logger.addWarning("No option map to this button")

        else:
            self.resources.logger.addWarning("No valid mode selected " + str(int(self.currentGPIOMode)))

    def onLeftButtonPressed(self):

        if self.interuptsConnected is False:
            return

        if self.currentGPIOMode == GPIOMode.HOMEPAGE:
            self.resources.logger.addInfo("LEFT PRESSED : 4 POSSIBLE ACTIONS")
            start = time.time()
            stop = 0
            duration = 0
            if EMULATE is False:
                while GPIO.input(GPIOPin.BUTTON_LEFT) == 0:
                    time.sleep(0.2)
            duration = (time.time() - start)

            if duration < 2:
                self.resources.logger.addInfo("LEFT PRESSED : RESET PRINTER ERROR, CANCEL LAST PRINT")
                self.resetPrinterErrors()
                self.enablePrinter()
                self.cancelAllNotCompletedJobs()
                self.printerMonitoring.start()
                self.gotoStart()
            elif duration >= 3 and duration < 8:
                self.resources.logger.addInfo("LEFT PRESSED : RESET PRINTER ERROR, PRINT LAST ASSEMBLY")
                self.sendPrintingJob()
            elif duration >= 8 and duration < 15:
                self.resources.logger.addInfo("LEFT PRESSED : SHUTDOWN")
                self.onShutdown()
            elif duration >= 15 and duration < 20:
                self.resources.logger.addInfo("LEFT PRESSED : SHOW MENU")
                if EMULATE is False:
                    self.onShowMenu()
            elif duration >= 20:
                self.resources.logger.addInfo("LEFT PRESSED : SHOW MENU ADVANCED")
                self.onShowAdvancedMenu()
                
                
        elif self.currentGPIOMode == GPIOMode.PRINT:
            self.resources.logger.addWarning("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.MENU:
            self.resources.logger.addInfo("LEFT PRESSED : MENU BACK")
            self.onLeftButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.MENU_SETUP:
            self.resources.logger.addInfo("LEFT PRESSED : MENU BACK")
            self.onLeftButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            self.resources.logger.addWarning("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.VALIDATE:
            self.resources.logger.addInfo("LEFT PRESSED : PHOTO VALIDATED CREATE ASSEMBLY")
            self.storeLastCapture()
            self.redoAssembly()

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            if self.printingEnabled is True:
                self.resources.logger.addInfo("LEFT PRESSED : PRINT")
                self.sendPrintingJob()

            else:
                self.resources.logger.addInfo("LEFT PRESSED : PRINT NOT ENABLED, DO NOTHING")

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR:

            self.resources.logger.addWarning("IGNORING THIS CAPTURE ")
            if len(self.captureList) < self.resources.nbImageMax:
                self.startCaptureProcess()

            else:
                self.redoAssembly()


        elif self.currentGPIOMode == GPIOMode.RUNNING:
            self.resources.logger.addWarning("No option map to this button")

        else:
            self.resources.logger.addWarning("No valid mode selected " + str(int(self.currentGPIOMode)))

    # HOMEPAGE = 1
    # PRINT = 2
    # MENU = 3
    # MENU_SETUP = 4
    # COMPUTING = 5
    # VALIDATE = 6
    # DISPLAY_ASSEMBLY = 7
    # TRIGGER_ERROR = 8
    # RUNNING = 8

    def onDownButtonPressed(self):
 

        if self.interuptsConnected is False:
            return
            
        if self.currentGPIOMode == GPIOMode.HOMEPAGE:
            
            start = time.time()
            stop = 0
            duration = 0
            if EMULATE is False:
                while GPIO.input(GPIOPin.BUTTON_DOWN) == 0:
                    time.sleep(0.1)
                    QApplication.processEvents()

            duration = (time.time() - start)

            if duration < 2:
                self.resources.logger.addInfo("DOWN PRESSED : START ASSEMBLY")
                self.startPictureAssembly()

            elif duration < 6 and duration >=2:
                self.resources.logger.addInfo("DOWN PRESSED : TOGGLE TOP LIGHT")
                self.topLightOn=not self.topLightOn
                self.switchTopLight(self.topLightOn)


        elif self.currentGPIOMode == GPIOMode.PRINT:
            self.resources.logger.addWarning("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.MENU:
            self.resources.logger.addInfo("DOWN PRESSED : NAVIGATE MENU")
            self.onDownButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.MENU_SETUP:
            self.resources.logger.addInfo("DOWN PRESSED : NAVIGATE MENU")
            self.onDownButtonGPIO()

        elif self.currentGPIOMode == GPIOMode.COMPUTING:
            self.resources.logger.addWarning("No option map to this button")

        elif self.currentGPIOMode == GPIOMode.VALIDATE:
            self.resources.logger.addInfo("DOWN PRESSED : REDO LAST PICTURE")
            self.startCaptureProcess()

        elif self.currentGPIOMode == GPIOMode.DISPLAY_ASSEMBLY:
            self.resources.logger.addInfo("DOWN PRESSED : DISPLAY_ASSEMBLY -> HOMEPAGE")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR:
            self.resources.logger.addWarning(
                "DOWN PRESSED : CANCELING")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.RUNNING:
            self.resources.logger.addWarning("No option map to this button")

        else:
            self.resources.logger.addWarning("No valid mode selected " + str(int(self.currentGPIOMode)))


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
        print( "Button pressed " + str(channel))

        if channel == GPIOPin.BUTTON_RIGHT:
            self.onRightButtonPressed()
        elif channel == GPIOPin.BUTTON_LEFT:
            self.onLeftButtonPressed()
        elif channel == GPIOPin.BUTTON_DOWN:
            self.onDownButtonPressed()

    def onRightButtonGPIO(self):

        pyautogui.press('enter')

    def onLeftButtonGPIO(self):

        pyautogui.press('left')

    def onDownButtonGPIO(self):

        pyautogui.press('down')

    def onShowMenu(self):

        self.setCurrentMode(GPIOMode.MENU)
        self.switchLed(False, False, False)
        self.showPixmapMenu()
        self.updateMenu()
        self.mainMenu.exec_(QPoint(500, 500))
        self.resources.getLogger().addInfo("SHOW MENU")
        self.switchLed(True, True, True)
        self.gotoStart()

    def initMenu(self):

        self.mainMenu = QMenu("Menu principal", self)
        self.mainMenuDevices = QMenu("Appareil photo / Flash", self)
        self.menuPrinters = QMenu("Impressions", self)
        self.menuSharing = QMenu("Partage", self)        
        self.menuPrinters.addAction(self.actionEnablePrinting)
        self.menuPrinters.addAction(self.actionRestartCups)
        self.menuSharing.addAction(self.actionRestartSharingService)
        self.mainMenuDevices.addAction(self.actionEnableSpeedLight)
        self.mainMenuDevices.addAction(self.actionRestartSpeedLight)
        self.mainMenuDevices.addAction(self.actionRestartDSLR)
        self.mainMenu.addMenu(self.menuPrinters)
        self.mainMenu.addMenu(self.mainMenuDevices)
        self.mainMenu.addMenu(self.menuSharing)
        self.mainMenu.addAction(self.actionShutdown)
        self.mainMenu.addAction(self.actionReboot)
        self.mainMenu.addAction(self.actionExit)

    def storeLastCapture(self):

        self.resources.getLogger().addInfo("STORE CAPTURE")
        self.captureList.append(self.lastCapture)

    def updateMenu(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.speedLightEnabled = settings.value("speedLightEnabled", True, bool)
        self.printingEnabled = settings.value("printingEnabled", True, bool)
        self.sharingEnabled = settings.value("sharingEnabled", True, bool)

        self.actionEnableSpeedLight.setChecked(self.speedLightEnabled)
        self.actionRestartSpeedLight.setVisible(self.speedLightEnabled)
        self.actionEnablePrinting.setChecked(self.printingEnabled)
        
        self.actionRestartSpeedLight.setVisible(self.speedLightEnabled)
        self.actionRestartCups.setVisible(self.printingEnabled)
        self.actionRestartSharingService.setVisible(self.sharingEnabled)

        if self.is_service_running("cups") is False:
            self.actionRestartCups.setText("Redemarrer service impression (not started)")
        else:
            self.actionRestartCups.setText("Redemarrer service impression (started)")

        if self.isSambaRunning() is False:
            self.actionRestartSharingService.setText("Redemarrer service partage (not started)")
        else:
            self.actionRestartSharingService.setText("Redemarrer service partage (started)")

    def setImagequality0(self):
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("imagequality", 0)
        self.resources.getLogger().addInfo("SET IMAGE QUALITY=0")
        subprocess.call("gphoto2 --set-config imagequality=0", shell=True)

    def setImagequality1(self):
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("imagequality", 1)
        self.resources.getLogger().addInfo("SET IMAGE QUALITY=1")
        subprocess.call("gphoto2 --set-config imagequality=1", shell=True)

    def setImagequality2(self):
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        settings.setValue("imagequality", 2)
        self.resources.getLogger().addInfo("SET IMAGE QUALITY=2")
        subprocess.call("gphoto2 --set-config imagequality=2", shell=True)

    def setCP800Printer(self):
        
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.resources.getLogger().addInfo("SET USE Canon_CP800 printer")
        self.printerName = "Canon_CP800"
        settings.setValue("printerName", self.printerName)

    def setCP760Printer(self):
        
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.resources.getLogger().addInfo("SET USE Canon_CP760 printer")
        self.printerName = "Canon_CP760"
        settings.setValue("printerName", self.printerName)

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

        if self.is_service_running("cups") is False:
            self.actionRestartCups = QAction("Redemarrer service impression (not started)", self)
            self.actionStartCups = QAction("Demarrer service impression (not started)", self)
            self.actionStopCups = QAction("Arreter service impression (not started)", self)
        else:
            self.actionRestartCups = QAction("Redemarrer service impression (started)", self)
            self.actionStartCups = QAction("Demarrer service impression (started)", self)
            self.actionStopCups = QAction("Arreter service impression (started)", self)

        self.actionRestartCups.triggered.connect(self.restartCUPS)
        self.actionStartCups.triggered.connect(self.startCUPS)
        self.actionStopCups.triggered.connect(self.stopCUPS)
        
        if self.isSambaRunning() is False:
            self.actionRestartSharingService = QAction("Redemarrer service partage (not started)", self)
            self.actionStartSharingService = QAction("Demarrer service partage (not started)", self)
            self.actionStopSharingService = QAction("Arreter service partage (not started)", self)
        else:
            self.actionRestartSharingService = QAction("Redemarrer service partage (started)", self)
            self.actionStartSharingService = QAction("Demarrer service partage (started)", self)
            self.actionStopSharingService = QAction("Arreter service partage (started)", self)
            
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

        self.actionGenerateSingleAssemblies = QAction("Creer tous les assemblages 1 photo", self)
        self.actionGenerateSingleAssemblies.triggered.connect(self.onGenerateAllSingleAssemblies)

        self.actionExit = QAction("<- Sortir du menu", self)

    def initAdvancedMenu(self):

        self.menu = QMenu("Menu principal", self)

        self.menuCleaning = QMenu("Donnees", self)
        self.menuDevices = QMenu("Appareil photo / flash", self)
        self.menuPrinters = QMenu("Impressions", self)
        self.menuSharing = QMenu("Partage", self)
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
        self.menuDevices.addAction(self.actionImagequality0)
        self.menuDevices.addAction(self.actionImagequality1)
        self.menuDevices.addAction(self.actionImagequality2)

        self.menuPrinters.addAction(self.actionEnablePrinting)
        self.menuPrinters.addAction(self.actionRestartCups)
        self.menuPrinters.addAction(self.actionStartCups)
        self.menuPrinters.addAction(self.actionStopCups)
        self.menuPrinters.addAction(self.actionChooseCP800Printer)
        self.menuPrinters.addAction(self.actionChooseCP760Printer)
        

        self.menuSharing.addAction(self.actionEnableSharing)
        self.menuSharing.addAction(self.actionRestartSharingService)
        self.menuSharing.addAction(self.actionStartSharingService)
        self.menuSharing.addAction(self.actionStopSharingService)

        self.menuSetup.addAction(self.actionShutdown)
        self.menuSetup.addAction(self.actionReboot)

        self.menuFeatures.addAction(self.actionGenerateSingleAssemblies)

        self.menu.addMenu(self.menuCleaning)
        self.menu.addMenu(self.menuDevices)
        self.menu.addMenu(self.menuPrinters)
        self.menu.addMenu(self.menuSkin)
        self.menu.addMenu(self.menuSharing)
        self.menu.addMenu(self.menuSetup)
        self.menu.addMenu(self.menuFeatures)

        self.menu.addAction(self.actionExit)

    def updateAdvancedMenu(self):

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        self.speedLightEnabled = settings.value("speedLightEnabled", True, bool)
        self.printingEnabled = settings.value("printingEnabled", True, bool)
        self.sharingEnabled = settings.value("sharingEnabled", True, bool)

        self.actionEnableSpeedLight.setChecked(self.speedLightEnabled)
        self.actionEnablePrinting.setChecked(self.printingEnabled)
        self.actionEnableSharing.setChecked(self.sharingEnabled)

        self.actionRestartSpeedLight.setVisible(self.speedLightEnabled)

        self.actionRestartCups.setVisible(self.printingEnabled)
        self.actionStartCups.setVisible(self.printingEnabled)
        self.actionStopCups.setVisible(self.printingEnabled)

        self.actionRestartSharingService.setVisible(self.sharingEnabled)
        self.actionStartSharingService.setVisible(self.sharingEnabled)
        self.actionStopSharingService.setVisible(self.sharingEnabled)

        if self.sharingEnabled is False:
            self.menuSharing.setTitle("Partage (not allowed)")
        else:
            if self.isSambaRunning() is False:
                self.menuSharing.setTitle("Partage (allowed not started)")
            else :
                self.menuSharing.setTitle("Partage (allowed started)")
        
        if self.printingEnabled is False:
            self.menuPrinters.setTitle("Impressions (not allowed)")
        else:
            if self.is_service_running("cups") is False:
            
                self.menuPrinters.setTitle("Impressions (allowed not started)")
            else:
                self.menuPrinters.setTitle("Impressions (allowed started)")
                
        if self.is_service_running("cups") is False:
            self.actionRestartCups = QAction("Redemarrer service impression (not started)", self)
            self.actionStartCups = QAction("Demarrer service impression (not started)", self)
            self.actionStopCups = QAction("Arreter service impression (not started)", self)
        else:
            self.actionRestartCups = QAction("Redemarrer service impression (started)", self)
            self.actionStartCups = QAction("Demarrer service impression (started)", self)
            self.actionStopCups = QAction("Arreter service impression (started)", self)

            

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
        self.setCurrentMode(GPIOMode.TRIGGER_ERROR)

        txt = "LA  PHOTO N'A  PAS  PU  ETRE  PRISE !"

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

        self.setCurrentMode(GPIOMode.MENU_SETUP)
        self.switchLed(False, False, False)
        self.showPixmapMenu()
        self.updateAdvancedMenu()
        self.menu.exec_(QPoint(500, 500))

        self.resources.getLogger().addInfo("SHOW MENU")
        self.switchLed(True, True, True)
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

        self.resources.getLogger().addInfo("INIT DEVICES FAST")
        self.switchDSLR(True)

    def initDevices(self):

        self.resources.getLogger().addInfo("INIT DEVICES")
        self.restartDSLR()
        self.restartSpeedLight()
        self.switchPrinter(True)
        QApplication.processEvents()

        if self.printingEnabled is True:
            self.startCUPS()
        else:
            self.stopCUPS()

        if self.sharingEnabled is True:
            self.startSamba()
        else:
            self.stopSamba()

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

        self.resources.logger.addInfo("RESTARTING SAMBA")

        if EMULATE is True:
            return
        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)
        en = settings.value("sharingEnabled", True, bool)
        
        if en is True:
            if self.wifiInterface0Enabled() is True:
                subprocess.Popen(["/etc/init.d/samba", "restart"])
            else:
                subprocess.Popen(["/etc/init.d/samba", "stop"])
        else:
            subprocess.Popen(["/etc/init.d/samba", "stop"])

    def startSamba(self):

        self.resources.logger.addInfo("STARTING SAMBA")

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

        self.resources.logger.addInfo("STOPPING SAMBA")
        if EMULATE is True:
            return
        subprocess.Popen(["/etc/init.d/samba", "stop"])

    def isSambaRunning(self):
        
        return self.is_service_running("smbd") and self.is_service_running("nmbd")

    def wifiInterface0Enabled(self):
        
        allowSmb = False
        out = check_output(["cat", "/sys/class/net/wlan0/operstate"])
        print(str(out))
        if "up" in str(out):
            allowSmb = True
            print("wlan0 is up : do allow samba sharing via wifi:")
        elif "down" in str(out):
            allowSmb = False
            print("wlan0 is down : do not samba sharing via wifi:")
        else:
            allowSmb = False
            print("cannot check wlan0 status : do not samba sharing via wifi:")
            
        return allowSmb

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

        self.resources.getLogger().addInfo("GENERATE ALL SINGLE ASSEMBLIES")
        self.generateAllSingleAssemblies(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB),
                                         self.resources.getPath(ressourcesManager.PATH.ASSEMBLIES_USB))

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

        GPIO.cleanup()

        if EMULATE is True:
            return
        # GPIO IN 20 wired

        GPIO.setup(GPIOPin.BUTTON_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(GPIOPin.BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(GPIOPin.BUTTON_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        GPIO.setup(GPIOPin.LED_RIGHT, GPIO.OUT, initial=1)
        GPIO.setup(GPIOPin.LED_DOWN, GPIO.OUT, initial=1)
        GPIO.setup(GPIOPin.LED_LEFT, GPIO.OUT, initial=1)
        
        GPIO.setup(GPIOPin.RELAY_POWER_TOP_LIGHT, GPIO.OUT, initial=0)
        GPIO.setup(GPIOPin.RELAY_LED_STRIP, GPIO.OUT, initial=0)
        GPIO.setup(GPIOPin.RELAY_2, GPIO.OUT, initial=0)
        GPIO.setup(GPIOPin.RELAY_3, GPIO.OUT, initial=0)
        
        self.blinkingTimer = QTimer()
        self.blinkingTimer.timeout.connect(self.blink)
        self.blinkingTimer.start(300)

        self.inputButtonThread = InputButtonThread()
        self.disconnectInputButtonInterupts()
        self.inputButtonThread.start()

    def switchTopLight(self, on):
        if on is True:
            GPIO.output(GPIOPin.RELAY_POWER_TOP_LIGHT, 0)
        else:
            GPIO.output(GPIOPin.RELAY_POWER_TOP_LIGHT, 1)
    


    def testRelays(self):
        
        GPIO.output(GPIOPin.RELAY_POWER_TOP_LIGHT, 0)
        time.sleep(2)
        GPIO.output(GPIOPin.RELAY_LED_STRIP, 0)
        time.sleep(2)


    def switchPrinter(self, on):
        return
        #if EMULATE is True:
            #return

        #if on is True:

            #GPIO.output(self.GPIO_POWER_PRINTER, 0)
            #time.sleep(2)

        #else:

            #GPIO.output(self.GPIO_POWER_PRINTER, 1)
            #time.sleep(2)

    def switchSpeedLight(self, on):
        return
        #if EMULATE is True:
            #return

        #settings = QSettings('settings.ini', QSettings.IniFormat)
        #settings.setFallbacksEnabled(False)
        #en = settings.value("speedLightEnabled", True, bool)

        #if on is True and en is True:

            #GPIO.output(self.GPIO_POWER_SPEEDLIGHT, 0)
            #time.sleep(1)
            #GPIO.output(self.GPIO_ON_OFF_SPEEDLIGHT, 0)
            #time.sleep(2)
            #GPIO.output(self.GPIO_ON_OFF_SPEEDLIGHT, 1)

        #else:

            #GPIO.output(self.GPIO_ON_OFF_SPEEDLIGHT, 0)
            #time.sleep(2)
            #GPIO.output(self.GPIO_ON_OFF_SPEEDLIGHT, 1)
            #GPIO.output(self.GPIO_POWER_SPEEDLIGHT, 1)
            #time.sleep(1)

    def switchDSLR(self, on):
        return
        #if EMULATE is True:
            #return

        #if on is True:
            #GPIO.output(self.GPIO_POWER_DSLR, 0)
            #time.sleep(1)
        #else:
            #GPIO.output(self.GPIO_POWER_DSLR, 1)
            #time.sleep(1)

    def onTimeout(self):

        self.defineTimeout(-1)
   
        if self.currentGPIOMode  == GPIOMode.HOMEPAGE:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED DO NOTHING")
            pass
            
        elif self.currentGPIOMode  == GPIOMode.PRINT:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.currentGPIOMode  == GPIOMode.MENU:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('esc') 
            pyautogui.press('esc')
            self.gotoStart()
            
            
        elif self.currentGPIOMode  == GPIOMode.MENU_SETUP:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            pyautogui.press('esc')
            pyautogui.press('esc')
            pyautogui.press('esc') 
            pyautogui.press('esc')
            self.gotoStart()

        elif self.currentGPIOMode  == GPIOMode.COMPUTING:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.currentGPIOMode  == GPIOMode.VALIDATE:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED LEFT BUTTON EMULATED")
            self.onLeftButtonPressed()

        elif self.currentGPIOMode  == GPIOMode.DISPLAY_ASSEMBLY:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()

        elif self.currentGPIOMode == GPIOMode.TRIGGER_ERROR:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED LEFT BUTTON EMULATED")
            self.onLeftButtonPressed()

        elif self.currentGPIOMode == GPIOMode.RUNNING:
            self.resources.logger.addInfo(self.currentGPIOMode.name + " TIMEOUT CALLBACK TRIGGERED GO HOME")
            self.gotoStart()


    def redoAssembly(self):

        self.setCurrentMode(GPIOMode.DISPLAY_ASSEMBLY)
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

        self.disconnectInputButtonInterupts()
        self.switchLed(False, False, False)
        self.enablePrinter()
        
        self.resetPrinterErrors()

        self.cancelAllNotCompletedJobs()

        conn = cups.Connection()
        import os
        exists = os.path.isfile(self.currentAssemblyPath)
        if exists:
    
            self.lastPrintId = conn.printFile(self.printerName, self.currentAssemblyPath, title='boxaselfi_job', options={})
            self.resources.logger.addInfo("NEW JOB PRINT("+str(self.lastPrintId)+") : " + self.currentAssemblyPath)
            self.showPrintSentPage()
            time.sleep(5)
            
            
        else:

            self.resources.logger.addError("NEW JOB PRINT : " + self.currentAssemblyPath + "file does not exists")

        self.printerMonitoring.start()
        # not sure if we go to home page maybe users wants to print several times.
        self.gotoStart()
        
        
    def cancelNotCompletedJobs(self):
        
        conn = cups.Connection()
        #printers = conn.getPrinters()
        for key, val in conn.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1).items():
            if key != self.lastPrintId:
                self.resources.logger.addInfo("CANCEL JOB ID : " + str(key))
                conn.cancelJob(key, purge_job=False)
            else :
                self.resources.logger.addInfo("DO NOT CANCEL LAST JOB ID : " + str(key))


    def cancelAllNotCompletedJobs(self):
        
        conn = cups.Connection()
        #printers = conn.getPrinters()
        for key, val in conn.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1).items():
            self.resources.logger.addInfo("CANCEL JOB ID : " + str(key))
            conn.cancelJob(key, purge_job=False)
    

    def enablePrinter(self):
        conn = cups.Connection()            
        conn.enablePrinter(self.printerName)
    

    def showPrintSentPage(self):

        self.resources.logger.addInfo("SHOW NEW PRINT JOB SENT")

        self.setCurrentMode(GPIOMode.PRINT)
        outPixmap = QPixmap(self.resources.getPath(ressourcesManager.PATH.PAGE) + "/printingSent.png")
        self.label.setPixmap(outPixmap)
        QApplication.processEvents()

    def erasePrinterStatusBox(self):

        self.resources.logger.addInfo("JOB PRINT STATUS : CLEANING THE LIST")
        self.printJobStatusList = []

    def gotoStart(self, index=1):

        self.resources.logger.addInfo("GO HOME")
        self.setCurrentMode(GPIOMode.HOMEPAGE)
        self.switchLed(False, False, True)
        self.connectInputButtonInterupts()
        self.captureList.clear()
        self.showHomePage()
        self.switchTopLight(False)

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

    def generateAllSingleAssemblies(self, inputFolder, outputFolder):

        self.setCurrentMode(GPIOMode.COMPUTING)
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
            for ind in range(self.resources.nbImageMax):
                idName = idName.replace("_" + str(ind) + ".jpg", "", 1)

            outFile = outputFolder + "/" + idName + "_" + layoutId + ".jpg"

            self.resources.buildSingleLayout(files, outFile, choosenLayout)

        self.gotoStart()

    def generateRandomIO(self, delay):

        generator = SimulatorButtonThread(self, delay)
        generator.start()
        QApplication.processEvents()
        time.sleep(2)

    def testAssemblies(self):

        for i in range(10):
            self.resources.buildAvailableAssemblies(
                self.resources.getPath(ressourcesManager.PATH.CAPTURE_LOCAL) + "/test", i)


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
                self.mainWindow.onRightButtonPressed()
            if j == 2:
                self.mainWindow.onLeftButtonPressed()
            if j == 3:
                self.mainWindow.onDownButtonPressed()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    #sim = SimulatorButtonThread(mainWin, 1)
    #sim.start()
    mainWin.show()
    ret = app.exec_()
    if EMULATE is False:
        GPIO.cleanup()
    sys.exit(ret)
