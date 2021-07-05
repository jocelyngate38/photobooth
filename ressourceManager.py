#!/usr/bin/env python

from enum import Enum
import os
from PyQt5.QtCore import (QFile, QFileInfo, QSettings,
                          Qt, QIODevice)
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow)

import sys
import xml.etree.ElementTree as ET
import random
import json
import platform
import uuid
import logging



if platform.system() == 'Windows':
    EMULATE = True
else:
    EMULATE = False
    import cups


class ressourcesManager:

    logger = None
    lastChoice = -1
    logger = logging.getLogger("RessourcesManag")

    class PATH(Enum):

        CAPTURE = 1
        CALIBRATION_IMAGE=2
        ASSEMBLIES = 3
        SKIN = 4
        APPLICATION = 5
        PAGE = 6
        EVENT = 7
        THUMB=10
        BACKGROUND_IMAGE=11
        BACKGROUND_LIST_PATH=12
        SKIN_LIST_PATH=13
        EVENT_LIST_PATH=14

    def getDirectorySize(self, Path):

        start_path = self.getPath(Path)
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return float(total_size / 1024.0 / 1024.0)

    def getDirectoryFileNumber(self, Path):

        totalFiles=0
        for base, dirs, files in os.walk(self.getPath(Path)):
            for Files in files:
                totalFiles += 1
        return totalFiles

    def __init__(self ):

        pass

    def logInfos(self):

        self.logger.info("RESSOURCE PATHS")
        self.logger.info("CAPTURE : " + self.getPath(self.PATH.CAPTURE))
        self.logger.info("ASSEMBLIES : " + self.getPath(self.PATH.ASSEMBLIES))
        self.logger.info("SKIN : " + self.getPath(self.PATH.SKIN))
        self.logger.info("BACKGROUND_IMAGE : " + self.getPath(self.PATH.BACKGROUND_IMAGE))
        self.logger.info("APPLICATION : " + self.getPath(self.PATH.APPLICATION))
        self.logger.info("PAGE : " + self.getPath(self.PATH.PAGE))
        self.logger.info("EVENT : " + self.getPath(self.PATH.EVENT))
        self.logger.info("THUMB : " + self.getPath(self.PATH.THUMB))
        self.logger.info("BACKGROUND_LIST_PATH : " + self.getPath(self.PATH.BACKGROUND_LIST_PATH))
        self.logger.info("SKIN_LIST_PATH : " + self.getPath(self.PATH.SKIN_LIST_PATH))
        self.logger.info("EVENT_LIST_PATH : " + self.getPath(self.PATH.EVENT_LIST_PATH))
        self.logger.info("CALIBRATION_IMAGE : " + self.getPath(self.PATH.CALIBRATION_IMAGE))

    def printPaths(self):

        print("============================================================")
        print("                       RESSOURCE PATHS                      ")
        print("============================================================")
        print("CAPTURE : " + self.getPath(self.PATH.CAPTURE))
        print("ASSEMBLIES : " + self.getPath(self.PATH.ASSEMBLIES))
        print("SKIN : " + self.getPath(self.PATH.SKIN))
        print("BACKGROUND_IMAGE : " + self.getPath(self.PATH.BACKGROUND_IMAGE))
        print("APPLICATION : " + self.getPath(self.PATH.APPLICATION))
        print("PAGE : " + self.getPath(self.PATH.PAGE))
        print("EVENT : " + self.getPath(self.PATH.EVENT))
        print("THUMB : " + self.getPath(self.PATH.THUMB))
        print("BACKGROUND_LIST_PATH : " + self.getPath(self.PATH.BACKGROUND_LIST_PATH))
        print("SKIN_LIST_PATH : " + self.getPath(self.PATH.SKIN_LIST_PATH))
        print("EVENT_LIST_PATH : " + self.getPath(self.PATH.EVENT_LIST_PATH))
        print("CALIBRATION_IMAGE : " + self.getPath(self.PATH.CALIBRATION_IMAGE))
        print("============================================================")

    def getSkinPageDatas(self):

        return self.skinPageDatas

    def getSkinLayoutDatas(self):

        return self.skinLayoutDatas

    def setPath(self, Path, value):

        if not os.path.exists(value):
            os.makedirs(value)
        if Path == ressourcesManager.PATH.CAPTURE:
            self.capturePath = value
        if Path == ressourcesManager.PATH.CALIBRATION_IMAGE:
            self.calibrationImagePath = value
        if Path == ressourcesManager.PATH.ASSEMBLIES:
            self.assembliesPath = value
        if Path == ressourcesManager.PATH.SKIN:
            self.skinPath = value
        if Path == ressourcesManager.PATH.APPLICATION:
            self.applicationPath = value
        if Path == ressourcesManager.PATH.PAGE:
            self.pagesPath = value
        if Path == ressourcesManager.PATH.EVENT:
            self.layoutPath = value
        if Path == ressourcesManager.PATH.THUMB:
            self.thumbPath = value
        if Path == ressourcesManager.PATH.BACKGROUND_IMAGE:
            self.backgroundImagePath = value
        if Path == ressourcesManager.PATH.BACKGROUND_LIST_PATH:
            self.backgroundListPath = value
        if Path == ressourcesManager.PATH.EVENT_LIST_PATH:
            self.eventListPath = value
        if Path == ressourcesManager.PATH.SKIN_LIST_PATH:
            self.skinListPath = value

    def getPath(self, Path):

        if Path == ressourcesManager.PATH.CAPTURE:
            return self.capturePath
        if Path == ressourcesManager.PATH.CALIBRATION_IMAGE:
            return self.calibrationImagePath
        if Path == ressourcesManager.PATH.ASSEMBLIES:
            return self.assembliesPath
        if Path == ressourcesManager.PATH.SKIN:
            return self.skinPath
        if Path == ressourcesManager.PATH.APPLICATION:
            return self.applicationPath
        if Path == ressourcesManager.PATH.PAGE:
            return self.pagesPath
        if Path == ressourcesManager.PATH.EVENT:
            return self.layoutPath
        if Path == ressourcesManager.PATH.THUMB:
            return self.thumbPath
        if Path == ressourcesManager.PATH.BACKGROUND_IMAGE:
            return self.backgroundImagePath
        if Path == ressourcesManager.PATH.BACKGROUND_LIST_PATH:
            return self.backgroundListPath
        if Path == ressourcesManager.PATH.EVENT_LIST_PATH:
            return self.eventListPath
        if Path == ressourcesManager.PATH.SKIN_LIST_PATH:
            return self.skinListPath

    def loadResources(self):

        basePath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), os.pardir))

        settings = QSettings('settings.ini', QSettings.IniFormat)
        settings.setFallbacksEnabled(False)

        self.skinName = settings.value("skin", "error")
        self.eventName = settings.value("event", "error")
        self.background = settings.value("background", "error")

        self.logger.info("STARTING RESSOURCE MANAGER")
        self.printDuration = 60
        self.numberOfPrint = 0
        self.maxNumberOfPrint = 36

        if EMULATE is True:
            self.applicationPath = basePath + "/photobooth-software"
        else:
            self.applicationPath = basePath + "/photobooth"

        self.applicationPath = os.path.normpath(self.applicationPath)

        self.backgroundListPath = self.applicationPath + "/resources/backgrounds"
        self.backgroundListPath = os.path.normpath(self.backgroundListPath)

        self.calibrationImagePath = self.applicationPath + "/resources/calibration_image.jpg"
        self.calibrationImagePath = os.path.normpath(self.calibrationImagePath)

        self.skinListPath = self.applicationPath + "/resources/skins"
        self.skinListPath = os.path.normpath(self.skinListPath)

        self.eventListPath = self.applicationPath + "/resources/events"
        self.eventListPath = os.path.normpath(self.eventListPath)

        self.backgroundImagePath = self.applicationPath + "/resources/backgrounds/" + self.background
        self.backgroundImagePath = os.path.normpath(self.backgroundImagePath)

        self.skinPath = self.applicationPath + "/resources/skins/" + self.skinName
        self.skinPath = os.path.normpath(self.skinPath)

        self.pagesPath = self.skinPath
        self.pagesPath = os.path.normpath(self.pagesPath)

        self.layoutPath = self.applicationPath + "/resources/events/" + self.eventName
        self.layoutPath = os.path.normpath(self.layoutPath)

        self.thumbPath = basePath + "/photobooth-datas/thumbs"
        if not os.path.exists(self.thumbPath):
            os.makedirs(self.thumbPath)
        self.thumbPath = os.path.normpath(self.thumbPath)

        self.applicationDataPath = basePath + "/photobooth-datas"
        if not os.path.exists(self.applicationDataPath):
            os.makedirs(self.applicationDataPath)
        self.applicationDataPath = os.path.normpath(self.applicationDataPath)

        self.assembliesPath = self.applicationDataPath + "/" + self.eventName + "/assemblies"
        if not os.path.exists(self.assembliesPath):
            os.makedirs(self.assembliesPath)
        self.assembliesPath = os.path.normpath(self.assembliesPath)

        self.capturePath = self.applicationDataPath + "/" + self.eventName + "/captures"
        if not os.path.exists(self.capturePath):
            os.makedirs(self.capturePath)
        self.capturePath = os.path.normpath(self.capturePath)

        self.skinLayoutDatas = [[], [], [], []]

        self.nbImageMax = 0

        self.homePageDisplayFilename = ""

        self.nbImageMax = 0

        descriptor = self.getPath(ressourcesManager.PATH.EVENT) + "/descriptor.xml"
        tree = ET.parse(descriptor)
        root = tree.getroot()
        layouts = root.findall("./layouts/layout")
        homePageDisplay = root.findall("./homepage")
        self.homePageDisplayFilename = str(homePageDisplay[0].find("./filename").text)
        self.skinDiplayLayoutDatas = {}

        displayDictPortrait = {}
        displayDictPortrait["x"] = 352
        displayDictPortrait["y"] = 50
        displayDictPortrait["w"] = 545
        displayDictPortrait["h"] = 820
        self.skinDiplayLayoutDatas["portrait"] = displayDictPortrait

        displayDictLandscape = {}
        displayDictLandscape["x"] = 155
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
                self.logger.error("XML ERROR NO SUCH FILE " + self.getPath(ressourcesManager.PATH.EVENT) + "/" + path)
                self.logger.error(
                    "XML error no such file " + self.getPath(ressourcesManager.PATH.EVENT) + "/" + path)
                continue

            images = lay.findall("./images/image")
            if len(images) != n and n !=1:
                self.logger.error("XML ERROR TOO MUCH/LESS IMAGES FOR THIS LAYOUT")
                continue
            if len(images) != n and n ==1:
                self.logger.info("XML SEVERAL IMAGES FOR LAYOUT 1")

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

        choosenLayout = self.chooseNextLayout(n)
        if choosenLayout == None:
            return
        self.buildLayout(filepath, choosenLayout)

    def buildAvailableAssemblies(self, filepath, n):

        choosenLayoutList = self.getSkinLayoutDatas()[n - 1]
        for i in range(len(choosenLayoutList)):
            choosenLayout = choosenLayoutList[i]
            self.buildLayout(filepath, choosenLayout)

    def resetChoices(self):

        self.lastChoice=-1

    def chooseNextLayout(self, n):

        choosenLayoutList = self.getSkinLayoutDatas()[n - 1]
        nLayouts = len(choosenLayoutList)

        if nLayouts == 0:
            return None

        c = self.lastChoice
        if c < -1 or c >= nLayouts-1 :
            c = -1

        if c == -1:
            c = 0
        else:
            c = c+1
        self.lastChoice=c

        self.logger.info("CHOOSEN LAYOUT ID : " + str(c) + " over [" + str(range(nLayouts-1)) +"]")
        return choosenLayoutList[c]


    def buildLayout2(self, idName, choosenLayout, thumb):

        layoutId = choosenLayout["layoutId"]
        nbImages = choosenLayout["nbImages"]

        outFile = self.getPath(ressourcesManager.PATH.ASSEMBLIES) + "/" + idName + "_" + layoutId + "_" + str(thumb) + ".jpg"

        if os.path.isfile(outFile):
            self.logger.info("THIS ASSEMBLY ALREADY EXISTS, WE DONT LOOSE TIME TO REBUILD IT")
            return QPixmap(outFile), os.path.normpath(outFile)

        layoutPixPath = self.getPath(ressourcesManager.PATH.EVENT) + "/" + choosenLayout["filename"]

        if not os.path.isfile(layoutPixPath):
            self.logger.warning("THE CURRENT LAYOUT TEMPLATE DOES NOT EXISTS")
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

            pix = QPixmap(self.getPath(ressourcesManager.PATH.THUMB) + "/" + idName + "_" + ext + "_thumb_" + str(thumb) + ".jpg")
            pix = pix.scaled(w, h, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

            painter.translate(x, y)
            painter.drawPixmap(0, 0, pix)
            painter.translate(-x, -y)

        painter.drawPixmap(0, 0, pixLayout)

        savedPath = self.savePicture(outPixmap, outFile, 0, 0, "JPG")

        del painter

        return outPixmap, savedPath

            
    def buildLayoutFromList(self, captureList, choosenLayout, showCuttingLine=False):

        layoutId = choosenLayout["layoutId"]
        nbImages = choosenLayout["nbImages"]
        
        outFile = self.getPath(ressourcesManager.PATH.ASSEMBLIES) + "/" + str(uuid.uuid4()) + ".jpg"
        layoutPixPath = self.getPath(ressourcesManager.PATH.EVENT) + "/" + choosenLayout["filename"]

        if not os.path.isfile(layoutPixPath):
            self.logger.warning("THE CURRENT LAYOUT TEMPLATE DOES NOT EXISTS")
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
                pix = pix.scaledToWidth(w)
            else:
                pix = pix.scaledToHeight(h)
            painter.translate(x, y)
            painter.drawPixmap(0, 0, pix)
            painter.translate(-x, -y)

            if nbImages == 1 and len(choosenLayout["images"]) == 2:
                x = choosenLayout["images"][(i + 2)]["x"]
                y = choosenLayout["images"][(i + 2)]["y"]
                w = choosenLayout["images"][(i + 2)]["w"]
                h = choosenLayout["images"][(i + 2)]["h"]
                angle = choosenLayout["images"][(i + 1)]["angle"]

                pix = QPixmap(path)

                if (w / h > 4 / 3):
                    pix = pix.scaledToWidth(w)
                else:
                    pix = pix.scaledToHeight(h)
                painter.translate(x, y)
                painter.drawPixmap(0, 0, pix)
                painter.translate(-x, -y)

        painter.drawPixmap(0, 0, pixLayout)

        if showCuttingLine is True:
            painter.setPen(QColor(255,110,0))  # add a red pen
            borderMargin = 28

            x00 = borderMargin
            y00 = 0
            x01 = x00
            y01 = pixLayout.size().height()

            x10 = pixLayout.size().width() - borderMargin
            y10 = 0
            x11 = x10
            y11 = pixLayout.size().height()

            x20 = 0
            y20 = borderMargin
            x21 = pixLayout.size().width()
            y21 = y20

            x30 = 0
            y30 = pixLayout.size().height() - borderMargin
            x31 = pixLayout.size().width()
            y31 = y30

            painter.drawLine(x00, y00, x01, y01)
            painter.drawLine(x10, y10, x11, y11)
            painter.drawLine(x20, y20, x21, y21)
            painter.drawLine(x30, y30, x31, y31)

            marginErrorPrint = 5
            painter.setPen(QColor(0, 255, 0))

            painter.drawLine(x00 + marginErrorPrint, y00, x01 + marginErrorPrint, y01)
            painter.drawLine(x10 - marginErrorPrint, y10, x11 - marginErrorPrint, y11)
            painter.drawLine(x20, y20 + marginErrorPrint, x21, y21 + marginErrorPrint)
            painter.drawLine(x30, y30 - marginErrorPrint, x31, y31 - marginErrorPrint)


            painter.setPen(QColor(255, 0, 0))
            painter.drawLine(x00 - marginErrorPrint, y00, x01 - marginErrorPrint, y01)
            painter.drawLine(x10 + marginErrorPrint, y10, x11 + marginErrorPrint, y11)
            painter.drawLine(x20, y20 - marginErrorPrint, x21, y21 - marginErrorPrint)
            painter.drawLine(x30, y30 + marginErrorPrint, x31, y31 + marginErrorPrint)

        savedPath = self.savePicture(outPixmap, outFile, 0, 0, "JPG")

        del painter

        return outPixmap, savedPath
        
    def buildLayout(self, idName, choosenLayout):

        layoutId = choosenLayout["layoutId"]
        nbImages = choosenLayout["nbImages"]

        outFile = self.getPath(ressourcesManager.PATH.ASSEMBLIES) + "/" + idName + "_" + layoutId + ".jpg"

        if os.path.isfile(outFile):
            return QPixmap(outFile), os.path.normpath(outFile)

        layoutPixPath = self.getPath(ressourcesManager.PATH.EVENT) + "/" + choosenLayout["filename"]

        if not os.path.isfile(layoutPixPath):
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

            pix = QPixmap(self.getPath(ressourcesManager.PATH.CAPTURE) + "/" + idName + "_" + ext + ".jpg")
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
            return

        layoutPixPath = self.getPath(ressourcesManager.PATH.EVENT) + "/" + choosenLayout["filename"]

        if not os.path.isfile(layoutPixPath):
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
    self.logger.info(json.dumps(printers))
    sys.exit(1)
