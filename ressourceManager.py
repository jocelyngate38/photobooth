#!/usr/bin/env python

from enum import Enum
import os
from PyQt5.QtCore import (QFile, QFileInfo, QSettings,
                          Qt, QIODevice)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow)
from logger import *
import sys
import xml.etree.ElementTree as ET
import random
import json
import platform
import uuid

if platform.system() == 'Windows':
    EMULATE = True
else:
    EMULATE = False
    import cups


class ressourcesManager:
    logger = None

    class PATH(Enum):

        CAPTURE_LOCAL = 1
        CAPTURE_USB = 2
        ASSEMBLIES_USB = 3
        SKIN = 4
        APPLICATION = 5
        PAGE = 6
        EVENT = 7
        LOG = 8
        LOG_FILE = 9
        THUMB_LOCAL=10

    def getDirectorySize(self, Path):
        start_path = self.getPath(Path)
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return float(total_size / 1024.0 / 1024.0)

    def __init__(self, ):

        basePath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), os.pardir))

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)

        self.skinName = settings.value("skin", "modern_chalk")
        self.eventName = settings.value("event", "openningWallstreat")

        self.logPath = basePath + "/photobooth-datas/local_datas/logs"
        if not os.path.exists(self.logPath):
            os.makedirs(self.logPath)
        self.logPath = os.path.normpath(self.logPath)

        self.logFile = self.logPath + '/photobooth.log'
        self.logFile = os.path.normpath(self.logFile)

        self.logger = logger(self.logFile)

        self.logger.addInfo("STARTING RESSOURCE MANAGER")
        self.printDuration = 60
        self.numberOfPrint = 0
        self.maxNumberOfPrint = 36

        self.applicationPath = basePath + "/photobooth"
        self.applicationPath = os.path.normpath(self.applicationPath)
        
        self.skinPath = self.applicationPath + "/resources/skins/" + self.skinName 
        self.skinPath = os.path.normpath(self.skinPath)

        self.pagesPath = self.skinPath
        self.pagesPath = os.path.normpath(self.pagesPath)

        self.layoutPath = self.applicationPath + "/resources/events/" + self.eventName
        self.layoutPath = os.path.normpath(self.layoutPath)

        self.thumbLocalPath = basePath + "/photobooth-datas/local_datas/thumbs"
        if not os.path.exists(self.thumbLocalPath):
            os.makedirs(self.thumbLocalPath)
        self.thumbLocalPath = os.path.normpath(self.thumbLocalPath)

        self.applicationLocalDataPath = basePath + "/photobooth-datas/local_datas"
        if not os.path.exists(self.applicationLocalDataPath):
            os.makedirs(self.applicationLocalDataPath)
        self.applicationLocalDataPath = os.path.normpath(self.applicationLocalDataPath)

        self.captureLocalPath = self.applicationLocalDataPath + "/" + self.eventName + "/captures"
        if not os.path.exists(self.captureLocalPath):
            os.makedirs(self.captureLocalPath)
        self.captureLocalPath = os.path.normpath(self.captureLocalPath)

        self.applicationUSBDataPath = basePath + "/photobooth-datas/usb_datas"
        if not os.path.exists(self.applicationUSBDataPath):
            os.makedirs(self.applicationUSBDataPath)
        self.applicationUSBDataPath = os.path.normpath(self.applicationUSBDataPath)

        self.assembliesPath = self.applicationUSBDataPath + "/" + self.eventName + "/assemblies"
        if not os.path.exists(self.assembliesPath):
            os.makedirs(self.assembliesPath)
        self.assembliesPath = os.path.normpath(self.assembliesPath)

        self.captureUSBPath = self.applicationUSBDataPath + "/" + self.eventName + "/captures"
        if not os.path.exists(self.captureUSBPath):
            os.makedirs(self.captureUSBPath)
        self.captureUSBPath = os.path.normpath(self.captureUSBPath)

        self.skinLayoutDatas = [[], [], [], []]
        #self.skinGeneratorThemes = []
        # self.skinGeneratorLayoutDatas = [[], [], [], []]

        self.nbImageMax = 0
        
        self.homePageDisplayFilename=""
        # self.loadCurrentXmlSkinDescriptor()

    def logInfos(self):

        self.logger.addInfo("RESSOURCE PATHS")
        self.logger.addInfo("CAPTURE_LOCAL : " + self.getPath(self.PATH.CAPTURE_LOCAL))
        self.logger.addInfo("CAPTURE_USB : " + self.getPath(self.PATH.CAPTURE_USB))
        self.logger.addInfo("ASSEMBLIES_USB : " + self.getPath(self.PATH.ASSEMBLIES_USB))
        self.logger.addInfo("SKIN : " + self.getPath(self.PATH.SKIN))
        self.logger.addInfo("APPLICATION : " + self.getPath(self.PATH.APPLICATION))
        self.logger.addInfo("PAGE : " + self.getPath(self.PATH.PAGE))
        self.logger.addInfo("EVENT : " + self.getPath(self.PATH.EVENT))
        self.logger.addInfo("LOG : " + self.getPath(self.PATH.LOG))
        self.logger.addInfo("LOG_FILE : " + self.getPath(self.PATH.LOG_FILE))
        self.logger.addInfo("THUMB_LOCAL : " + self.getPath(self.PATH.THUMB_LOCAL))

    def printPaths(self):

        print("============================================================")
        print("                       RESSOURCE PATHS                      ")
        print("============================================================")
        print("CAPTURE_LOCAL : " + self.getPath(self.PATH.CAPTURE_LOCAL))
        print("CAPTURE_USB : " + self.getPath(self.PATH.CAPTURE_USB))
        print("ASSEMBLIES_USB : " + self.getPath(self.PATH.ASSEMBLIES_USB))
        print("SKIN : " + self.getPath(self.PATH.SKIN))
        print("APPLICATION : " + self.getPath(self.PATH.APPLICATION))
        print("PAGE : " + self.getPath(self.PATH.PAGE))
        print("EVENT : " + self.getPath(self.PATH.EVENT))
        print("LOG : " + self.getPath(self.PATH.LOG))
        print("LOG_FILE : " + self.getPath(self.PATH.LOG_FILE))
        print("THUMB_LOCAL : " + self.getPath(self.PATH.THUMB_LOCAL))
        print("============================================================")

    def getSkinPageDatas(self):
        return self.skinPageDatas

    def getSkinLayoutDatas(self):
        return self.skinLayoutDatas

    def getLogger(self):
        return self.logger

    def setPath(self, Path, value):
        if not os.path.exists(value):
            os.makedirs(value)
        if Path == ressourcesManager.PATH.CAPTURE_LOCAL:
            self.captureLocalPath = value
        if Path == ressourcesManager.PATH.CAPTURE_USB:
            self.captureUSBPath = value
        if Path == ressourcesManager.PATH.ASSEMBLIES_USB:
            self.assembliesPath = value
        if Path == ressourcesManager.PATH.SKIN:
            self.skinPath = value
        if Path == ressourcesManager.PATH.APPLICATION:
            self.applicationPath = value
        if Path == ressourcesManager.PATH.PAGE:
            self.pagesPath = value
        if Path == ressourcesManager.PATH.EVENT:
            self.layoutPath = value
        if Path == ressourcesManager.PATH.LOG:
            self.logPath = value
        if Path == ressourcesManager.PATH.LOG_FILE:
            self.logFile = value
        if Path == ressourcesManager.PATH.THUMB_LOCAL:
            self.thumbLocalPath = value

    def getPath(self, Path):
        if Path == ressourcesManager.PATH.CAPTURE_LOCAL:
            return self.captureLocalPath
        if Path == ressourcesManager.PATH.CAPTURE_USB:
            return self.captureUSBPath
        if Path == ressourcesManager.PATH.ASSEMBLIES_USB:
            return self.assembliesPath
        if Path == ressourcesManager.PATH.SKIN:
            return self.skinPath
        if Path == ressourcesManager.PATH.APPLICATION:
            return self.applicationPath
        if Path == ressourcesManager.PATH.PAGE:
            return self.pagesPath
        if Path == ressourcesManager.PATH.EVENT:
            return self.layoutPath
        if Path == ressourcesManager.PATH.LOG:
            return self.logPath
        if Path == ressourcesManager.PATH.LOG_FILE:
            return self.logFile
        if Path == ressourcesManager.PATH.THUMB_LOCAL:
            return self.thumbLocalPath

    #def loadXmlSkinGeneratorDescriptor(self, path):

        ## print(path)
        #self.nbImageMax = 0
        #self.rootTemplate = path
        #tree = ET.parse(path + "/descriptor.xml")
        #root = tree.getroot()
        #layouts = root.findall("./layouts/layout")
        #subThemes = root.findall("./subThemes/subTheme")
        #pages = root.findall("./pages/page")

        #self.skinGeneratorPagesDatas = []
        #self.skinGeneratorThemes = []

        #for theme in subThemes:
            #self.skinGeneratorThemes.append([str(theme.find("./name").text), str(theme.find("./folder").text)])

        ## print(self.skinGeneratorThemes)

        #self.skinGeneratorLayoutDatas = [[], [], [], []]

        #for lay in layouts:
            #layoutDict = {}
            #n = int(lay.find("./nbImages").text)
            #if n > self.nbImageMax:
                #self.nbImageMax = n
            #path = str(lay.find("./template").text)
            #isLandscape = int(lay.find("./landscape").text)
            #layoutId = str(lay.find("./layoutId").text)

            #layoutDict["landscape"] = isLandscape
            #layoutDict["nbImages"] = n
            #layoutDict["filename"] = path
            #layoutDict["layoutId"] = layoutId

            #curfile = self.rootTemplate + "/layouts/" + path
            #if not os.path.isfile(curfile):
                #print("XML error no such file " + curfile)
                #self.getLogger().addError(
                    #"XML error no such file " + curfile)
                #continue

            #messages = lay.findall("./messages/message")

            #messagesDict = {}
            #for mess in messages:
                #messDict = {}
                #messDict["x1"] = int(mess.find("./point1/x").text)
                #messDict["y1"] = int(mess.find("./point1/y").text)
                #messDict["x2"] = int(mess.find("./point2/x").text)
                #messDict["y2"] = int(mess.find("./point2/y").text)
                #messDict["x3"] = int(mess.find("./point3/x").text)
                #messDict["y3"] = int(mess.find("./point3/y").text)
                #messDict["x4"] = int(mess.find("./point4/x").text)
                #messDict["y4"] = int(mess.find("./point4/y").text)
                #messDict["defaultFontSize"] = int(mess.find("./defaultFontSize").text)
                #messDict["location"] = mess.find("./location").text
                #messDict["defaultMessage"] = mess.find("./defaultMessage").text
                #messDict["type"] = mess.find("./type").text
                #messagesDict[int(mess.find("./index").text)] = messDict

            #layoutDict["messages"] = messagesDict

            #self.skinGeneratorLayoutDatas[n - 1].append(layoutDict)

        #for page in pages:
            #pageDict = {}
            #pageDict["filename"] = page.find("./filename").text

            #messagesDict = {}
            #messages = page.findall("./message")
            #for mess in messages:
                #messDict = {}
                #messDict["x1"] = int(mess.find("./point1/x").text)
                #messDict["y1"] = int(mess.find("./point1/y").text)
                #messDict["x2"] = int(mess.find("./point2/x").text)
                #messDict["y2"] = int(mess.find("./point2/y").text)
                #messDict["x3"] = int(mess.find("./point3/x").text)
                #messDict["y3"] = int(mess.find("./point3/y").text)
                #messDict["x4"] = int(mess.find("./point4/x").text)
                #messDict["y4"] = int(mess.find("./point4/y").text)
                #messDict["defaultFontSize"] = int(mess.find("./defaultFontSize").text)
                #messDict["location"] = mess.find("./location").text
                #messDict["defaultMessage"] = mess.find("./defaultMessage").text
                #messDict["type"] = mess.find("./type").text
                #messagesDict[int(mess.find("./index").text)] = messDict

            #pageDict["messages"] = messagesDict
            #self.skinGeneratorPagesDatas.append(pageDict)

    def loadCurrentXmlSkinDescriptor(self):

        self.nbImageMax = 0

        descriptor = self.getPath(ressourcesManager.PATH.EVENT) + "/descriptor.xml"
        print(descriptor)
        tree = ET.parse(descriptor)
        root = tree.getroot()
        layouts = root.findall("./layouts/layout")
        homePageDisplay = root.findall("./homepage")
        self.homePageDisplayFilename = str(homePageDisplay[0].find("./filename").text)
        self.skinDiplayLayoutDatas = {}

        displayDictPortrait = {}
        displayDictPortrait["x"] = 352
        displayDictPortrait["y"] = 50
        displayDictPortrait["w"] = 582
        displayDictPortrait["h"] = 870
        self.skinDiplayLayoutDatas["portrait"] = displayDictPortrait

        displayDictLandscape = {}
        displayDictLandscape["x"] = 76
        displayDictLandscape["y"] = 86
        displayDictLandscape["w"] = 1029
        displayDictLandscape["h"] = 676
        self.skinDiplayLayoutDatas["landscape"] = displayDictLandscape

        self.skinLayoutDatas = [[], [], [], []]

        for lay in layouts:
            layoutDict = {}
            n = int(lay.find("./nbImages").text)
            if n > self.nbImageMax:
                self.nbImageMax = n
            path = str(lay.find("./filename").text)
            isLandscape = int(lay.find("./landscape").text)
            layoutId = str(lay.find("./layoutId").text)

            layoutDict["landscape"] = isLandscape
            layoutDict["nbImages"] = n
            layoutDict["filename"] = path
            layoutDict["layoutId"] = layoutId

            if not os.path.isfile(self.getPath(ressourcesManager.PATH.EVENT) + "/" + path):
                print("XML error no such file " + self.getPath(ressourcesManager.PATH.EVENT) + "/" + path)
                self.getLogger().addError(
                    "XML error no such file " + self.getPath(ressourcesManager.PATH.EVENT) + "/" + path)
                continue

            images = lay.findall("./images/image")
            if len(images) != int(lay.find("./nbImages").text):
                print("XML error too much images for this layout")
                self.getLogger().addError("XML error too much/less images for this layout")
                continue

            imagesDict = {}
            for im in images:
                imageDict = {}
                imageDict["x"] = int(im.find("./x").text)
                imageDict["y"] = int(im.find("./y").text)
                imageDict["w"] = int(im.find("./w").text)
                imageDict["h"] = int(im.find("./h").text)
                imageDict["angle"] = int(im.find("./angle").text)
                imagesDict[int(im.find("./index").text)] = imageDict

            layoutDict["images"] = imagesDict
            self.skinLayoutDatas[n - 1].append(layoutDict)

    def buildShuttleAssembly(self, filepath, n):

        choosenLayout = self.chooseRandomLayout(n)
        if choosenLayout == None:
            return
        self.buildLayout(filepath, choosenLayout)

    def buildAvailableAssemblies(self, filepath, n):

        choosenLayoutList = self.getSkinLayoutDatas()[n - 1]
        for i in range(len(choosenLayoutList)):
            choosenLayout = choosenLayoutList[i]
            self.buildLayout(filepath, choosenLayout)

    def chooseRandomLayout(self, n):

        choosenLayoutList = self.getSkinLayoutDatas()[n - 1]
        ran = range(len(choosenLayoutList))
        if len(choosenLayoutList) == 0:
            return None
        choices = [*ran]
        random.shuffle(choices)
        index = choices.pop()
        choosenLayout = choosenLayoutList[index]
        return choosenLayout



    def buildLayout2(self, idName, choosenLayout, thumb):
        #print(choosenLayout)

        layoutId = choosenLayout["layoutId"]
        nbImages = choosenLayout["nbImages"]

        outFile = self.getPath(ressourcesManager.PATH.ASSEMBLIES_USB) + "/" + idName + "_" + layoutId + "_" + str(thumb) + ".jpg"

        if os.path.isfile(outFile):
            print("This assembly already exists, we dont loose time to rebuild it")
            return QPixmap(outFile), os.path.normpath(outFile)

        layoutPixPath = self.getPath(ressourcesManager.PATH.EVENT) + "/" + choosenLayout["filename"]

        if not os.path.isfile(layoutPixPath):
            print("The current layout template does not exists")
            return

        pixLayout = QPixmap(layoutPixPath)
        outPixmap = QPixmap(pixLayout.size())
        outPixmap.fill(Qt.black)
        pictures = []
        for i in range(nbImages):
            pictures.append(str(int(i)))

        random.shuffle(pictures)

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        for i in range(nbImages):
            ext = pictures.pop()
            x = choosenLayout["images"][(i + 1)]["x"]
            y = choosenLayout["images"][(i + 1)]["y"]
            w = choosenLayout["images"][(i + 1)]["w"]
            h = choosenLayout["images"][(i + 1)]["h"]
            angle = choosenLayout["images"][(i + 1)]["angle"]

            pix = QPixmap(self.getPath(ressourcesManager.PATH.THUMB_LOCAL) + "/" + idName + "_" + ext + "_thumb_" + str(thumb) + ".jpg")
            pix = pix.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

            painter.translate(x, y)
            painter.drawPixmap(0, 0, pix)
            painter.translate(-x, -y)

        painter.drawPixmap(0, 0, pixLayout)

        savedPath = self.savePicture(outPixmap, outFile, 0, 0, "JPG")

        del painter

        return outPixmap, savedPath
        
        
            
    def buildLayoutFromList(self, captureList, choosenLayout):
        
        #print(choosenLayout)

        layoutId = choosenLayout["layoutId"]
        nbImages = choosenLayout["nbImages"]
        
        outFile = self.getPath(ressourcesManager.PATH.ASSEMBLIES_USB) + "/" + str(uuid.uuid4()) + ".jpg"
        layoutPixPath = self.getPath(ressourcesManager.PATH.EVENT) + "/" + choosenLayout["filename"]

        if not os.path.isfile(layoutPixPath):
            print("The current layout template does not exists")
            return

        pixLayout = QPixmap(layoutPixPath)
        outPixmap = QPixmap(pixLayout.size())
        outPixmap.fill(Qt.black)
        
        pictures = captureList.copy()
        random.shuffle(pictures)

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        for i in range(nbImages):
            path = pictures.pop()
            x = choosenLayout["images"][(i + 1)]["x"]
            y = choosenLayout["images"][(i + 1)]["y"]
            w = choosenLayout["images"][(i + 1)]["w"]
            h = choosenLayout["images"][(i + 1)]["h"]
            angle = choosenLayout["images"][(i + 1)]["angle"]

            pix = QPixmap(path)
            
            if(w/h > 4/3):           
                pix = pix.scaledToWidth(w)#, transformMode=Qt.SmoothTransformation)
            else:
                pix = pix.scaledToHeight(h)#, transformMode=Qt.SmoothTransformation)
            painter.translate(x, y)
            painter.drawPixmap(0, 0, pix)
            painter.translate(-x, -y)

        painter.drawPixmap(0, 0, pixLayout)

        savedPath = self.savePicture(outPixmap, outFile, 0, 0, "JPG")

        del painter

        return outPixmap, savedPath
        
        
        
    def buildLayout(self, idName, choosenLayout):

        layoutId = choosenLayout["layoutId"]
        nbImages = choosenLayout["nbImages"]

        outFile = self.getPath(ressourcesManager.PATH.ASSEMBLIES_USB) + "/" + idName + "_" + layoutId + ".jpg"

        if os.path.isfile(outFile):
            #print("This assembly already exists, we dont loose time to rebuild it")
            return QPixmap(outFile), os.path.normpath(outFile)

        layoutPixPath = self.getPath(ressourcesManager.PATH.EVENT) + "/" + choosenLayout["filename"]

        if not os.path.isfile(layoutPixPath):
            #print("The current layout template does not exists")
            return

        pixLayout = QPixmap(layoutPixPath)
        outPixmap = QPixmap(pixLayout.size())
        outPixmap.fill(Qt.black)
        pictures = []
        for i in range(nbImages):
            pictures.append(str(int(i)))

        random.shuffle(pictures)

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        for i in range(nbImages):
            ext = pictures.pop()
            x = choosenLayout["images"][(i + 1)]["x"]
            y = choosenLayout["images"][(i + 1)]["y"]
            w = choosenLayout["images"][(i + 1)]["w"]
            h = choosenLayout["images"][(i + 1)]["h"]
            angle = choosenLayout["images"][(i + 1)]["angle"]

            pix = QPixmap(self.getPath(ressourcesManager.PATH.CAPTURE_LOCAL) + "/" + idName + "_" + ext + ".jpg")
            pix = pix.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

            painter.translate(x, y)
            painter.drawPixmap(0, 0, pix)
            painter.translate(-x, -y)

        painter.drawPixmap(0, 0, pixLayout)

        savedPath = self.savePicture(outPixmap, outFile, 0, 0, "JPG")

        del painter

        return outPixmap, savedPath

    def buildSingleLayout(self, inFile, outFile, choosenLayout):

        if os.path.isfile(outFile):
            #print("This assembly already exists, we dont loose time to rebuild it")
            return

        layoutPixPath = self.getPath(ressourcesManager.PATH.EVENT) + "/" + choosenLayout["filename"]

        if not os.path.isfile(layoutPixPath):
            #print("The current layout template does not exists")
            return

        pixLayout = QPixmap(layoutPixPath)
        outPixmap = QPixmap(pixLayout.size())
        outPixmap.fill(Qt.black)

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        h = choosenLayout["images"][1]["h"]
        x = choosenLayout["images"][1]["x"]
        y = choosenLayout["images"][1]["y"]
        w = choosenLayout["images"][1]["w"]

        pix = QPixmap(inFile)
        pix = pix.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        painter.translate(x, y)
        painter.drawPixmap(0, 0, pix)
        painter.translate(-x, -y)
        painter.drawPixmap(0, 0, pixLayout)
        self.savePicture(outPixmap, outFile, 0, 0, "JPG")
        del painter


    def savePicture(self, pixmap, path, w, h, format):

        normPath = os.path.normpath(path)
        file = QFile(normPath)
        file.open(QIODevice.WriteOnly)
        if w == 0 or h == 0:
            pixmap.save(file, format)
        else:
            pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation).save(file, format)
        return normPath


if __name__ == '__main__':
    app = QApplication(sys.argv)
    resources = ressourcesManager()
    conn = cups.Connection()
    printers = conn.getPrinters()
    resources.logger.addInfo(json.dumps(printers))

    # resources.loadXmlSkinGeneratorDescriptor("../external/skin/chalk/templates/descriptor.xml")
    # resources.loadCurrentXmlSkinDescriptor()
    sys.exit(1)
