#!/usr/bin/env python


from PyQt5.QtCore import (QUrl, QFile, QFileInfo, QPoint, QRect, QRectF, QSettings, QSize, QPointF,
                          Qt, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QDateTime, QIODevice, QElapsedTimer)

from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QBrush, QPixmap, QPainter, QPen, QColor, QPainterPath, \
                         QDesktopServices, QFontMetrics)
from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow, QDialog, QProgressBar, QLabel,
                             QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QGroupBox, QComboBox,
                             QSpacerItem, QSizePolicy, QInputDialog)

import time
import threading, time
from random import randint
from subprocess import call
import subprocess
from datetime import datetime
import random
import shutil
import os
from shutil import copyfile
from enum import Enum
import math

from ressourceManager import *
import glob
import sys


class Assembly():

    def __init__(self, input, output):

        self.resources = ressourcesManager()
        self.resources.loadCurrentXmlSkinDescriptor()
        if input != "":
            self.resources.setPath(ressourcesManager.PATH.CAPTURE_USB, input)
        if output != "":
            self.resources.setPath(ressourcesManager.PATH.ASSEMBLIES_USB, output)

    def redoAssemblies(self, all):

        mylist = [f for f in glob.glob(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB) + "/*.jpg")]

        for files in mylist:

            # print(files)
            if os.path.isfile(files):
                basename = os.path.basename(files)
                basename = basename.replace("_0.jpg", "", 1)
                basename = basename.replace("_1.jpg", "", 1)
                basename = basename.replace("_2.jpg", "", 1)
                basename = basename.replace("_3.jpg", "", 1)
                mylist1 = [ff for ff in
                           glob.glob(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB) + "/" + basename + "*")]
                n = len(mylist1)
                dir_path = os.path.dirname(os.path.realpath(files))
                for i in range(n):
                    os.rename(mylist1[i], dir_path + "\\" + basename + "_" + str(int(i)) + ".jpg")
                if all == False:
                    self.resources.buildShuttleAssembly(
                        self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB) + "\\" + basename, n)
                else:
                    self.resources.buildAvailableAssemblies(
                        self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB) + "\\" + basename, n)

    def redoAssemblies1Pict(self):

        mylist = [f for f in glob.glob(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB) + "/*.jpg")]
        i = 0
        for files in mylist:
            i += 1
            # print(files)
            dir_path = os.path.dirname(os.path.realpath(files))
            if os.path.isfile(files):
                basename = os.path.basename(files)
                os.rename(files, dir_path + "\\file" + str(i) + "_0.jpg")
        self.redoAssembliest()

    def redoAssembliest(self):

        mylist = [f for f in glob.glob(self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB) + "/*.jpg")]
        for files in mylist:
            if os.path.isfile(files):
                basename = os.path.basename(files)
                basename = basename.replace("_0.jpg", "", 1)
            self.resources.buildAvailableAssemblies(
                self.resources.getPath(ressourcesManager.PATH.CAPTURE_USB) + "\\" + basename, 1)


class skinBuilder():

    def __init__(self):
        self.resources = None
        self.baseSkinTemplate = "D:/photobooth/trunk/external/skin/halloween/templates"

    def setDescriptorFolder(self, path):
        self.baseSkinTemplate = path

    def init(self):
        self.resources = ressourcesManager()
        self.resources.loadXmlSkinGeneratorDescriptor(self.baseSkinTemplate)

    def createHierarchy(self):
        # print("createHierarchy")
        self.generationPath = "../external/skin/chalk/testGene/tmp"

        if not os.path.exists(self.generationPath):
            os.makedirs(self.generationPath)

        if not os.path.exists(self.generationPath + "/layouts/"):
            os.makedirs(self.generationPath + "/layouts/")

        if not os.path.exists(self.generationPath + "/pages/"):
            os.makedirs(self.generationPath + "/pages/")

    def setOutpuFolder(self, folder):

        self.currentOutputFolder = folder
        if not os.path.exists(self.currentOutputFolder):
            os.makedirs(self.currentOutputFolder)

        if not os.path.exists(self.currentOutputFolder + "/layouts/"):
            os.makedirs(self.currentOutputFolder + "/layouts/")

        if not os.path.exists(self.currentOutputFolder + "/pages/"):
            os.makedirs(self.currentOutputFolder + "/pages/")

    def copyLayouts(self):

        # print("copyLayouts")
        source = [s for s in os.listdir(self.baseSkinTemplate + "/layouts/") if s.endswith('.png')]
        destination = self.currentOutputFolder + "/layouts/"
        for files in source:
            # print(files)
            shutil.copy(self.baseSkinTemplate + "/layouts/" + files, destination)

    def copyPages(self):

        # print("copyPages")
        source = [s for s in os.listdir(self.baseSkinTemplate + "/pages/") if s.endswith('.png')]
        destination = self.currentOutputFolder + "/pages/"
        for files in source:
            # print(files)
            shutil.copy(self.baseSkinTemplate + "/pages/" + files, destination)

    def copyDescriptor(self):

        # print("copyDescriptor")
        source = self.baseSkinTemplate + "/descriptor.xml"
        destination = self.currentOutputFolder + "/"
        shutil.copy(source, destination)

    def copyFiles(self):
        self.copyLayouts()
        self.copyPages()
        self.copyDescriptor()

    def flattenSubtheme(self, copyright):
        # print("flattenSubtheme")

        generatorLayoutDatas = self.resources.skinGeneratorLayoutDatas
        generatorPageDatas = self.resources.skinGeneratorPagesDatas

        for lay in generatorLayoutDatas:
            for i in range(len(lay)):
                fileAA = lay[i]['template']
                fileBB = self.choosenSkinTheme[0] + "/" + fileAA
                outFile = self.generationPath + "/layouts/" + fileAA
                fileA = self.baseSkinTemplate + "/layouts/" + fileAA
                fileB = self.baseSkinTemplate + "/layouts/" + fileBB
                self.flattenFiles(fileA, fileB, outFile, lay[i], copyright)

        self.createOverlayFile(generatorPageDatas, copyright)

    def buildSkinInteractively(self):

        generatorLayoutDatas = self.resources.skinGeneratorLayoutDatas
        generatorPageDatas = self.resources.skinGeneratorPagesDatas

        builder = dialogSkinPreviewBuilder(self.currentOutputFolder)

        for lay in generatorLayoutDatas:
            for i in range(len(lay)):
                cLay = lay[i]
                print(cLay)
                dbuilder = dialogSkinBuilder(self.currentOutputFolder + "/layouts", cLay["template"],
                                             self.baseSkinTemplate + "/layouts")
                for ii in range(1, len(cLay["messages"]) + 1):
                    if cLay['messages'][ii]["type"] == "cubic":
                        dbuilder.addTextInput(cLay["messages"][ii])

                builder.addBuilder(dbuilder)

        for lay in generatorPageDatas:
            cLay = lay
            dbuilder = dialogSkinBuilder(self.currentOutputFolder + "/pages", cLay["filename"],
                                         self.baseSkinTemplate + "/pages/")
            for ii in range(1, len(cLay["messages"]) + 1):
                if cLay['messages'][ii]["type"] == "cubic":
                    dbuilder.addTextInput(cLay["messages"][ii])
            builder.addBuilder(dbuilder)

        for t in self.resources.skinGeneratorThemes:
            builder.addSubThemes(t[0], t[1])

        builder.arrangeLayout()
        builder.exec()

    def createOverlayFile(self, generatorPageDatas, copyright):

        # print(generatorPageDatas)
        for ol in generatorPageDatas:

            base = QPixmap(self.currentOutputFolder + "/pages/" + ol["filename"])

            painter = QPainter(base)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QColor(0, 0, 0))
            for ii in range(1, len(ol["messages"]) + 1):
                if ol['messages'][ii]["type"] == "cubic":
                    self.drawTextAlongCubic(ol["messages"][ii], painter, ol["filename"])
            f = self.resources.savePicture(base, self.currentOutputFolder + "/pages/" + ol["filename"], 0, 0, "JPG")
            del painter

    def flattenFiles(self, fileA, fileB, output, lay, copyright):

        overLay = QPixmap(fileB)
        outPixmap = QPixmap(fileA)
        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, overLay)
        painter.setPen(QColor(255, 255, 255))

        # font = QFont('Arial', fs)

        for ii in range(1, len(lay["messages"]) + 1):
            if lay['messages'][ii]["type"] == "cubic":
                if QFileInfo(fileA).fileName() == lay['template']:
                    self.drawTextAlongCubic(lay["messages"][ii], painter, lay['template'])

        if copyright == True:
            if lay["landscape"] == 0:
                overLayCopyright = QPixmap(self.baseSkinTemplate + "/copyrightPortrait.png")
                painter.drawPixmap(0, 0, overLayCopyright)
            else:
                overLayCopyright = QPixmap(self.baseSkinTemplate + "/copyrightLandscape.png")
                painter.drawPixmap(0, 0, overLayCopyright)

        f = self.resources.savePicture(outPixmap, output, 0, 0, "JPG")
        del painter
        return f

    def drawTextAlongCubic(self, lay, painter, filename):

        fs = lay["defaultFontSize"]
        font = QFont('Right Chalk', fs)

        defaultMessage = lay["defaultMessage"]

        c1 = QPointF(lay["x1"], lay["y1"])
        c2 = QPointF(lay["x2"], lay["y2"])
        c3 = QPointF(lay["x3"], lay["y3"])
        c4 = QPointF(lay["x4"], lay["y4"])
        path = QPainterPath(c1)
        path.cubicTo(c2, c3, c4)
        # painter.drawPath(path)

        pathLength = path.length()
        textMetricLength = QFontMetrics(font).width(defaultMessage)

        fsn = int(fs * pathLength / (textMetricLength) * .95)
        if fsn > 70:
            fsn = 70
        font = QFont('Right Chalk', fsn)

        textMetricLength = QFontMetrics(font).width(defaultMessage)

        messageSpacing = []
        defaultMessageM = []
        sumMessageSpacing = 0.0

        for i in range(len(defaultMessage)):
            messageSpacing.append(QFontMetrics(font).width(defaultMessage[i]))
            sumMessageSpacing += messageSpacing[i]

        for i in range(len(defaultMessage)):
            messageSpacing[i] = messageSpacing[i] / sumMessageSpacing

        steps = 0
        painter.setFont(font)

        for i in range(len(defaultMessage)):

            steps += messageSpacing[i] / 2
            point = QPointF(path.pointAtPercent(steps))
            angle = path.angleAtPercent(steps)

            painter.save()
            painter.translate(point)
            painter.rotate(-angle)
            x = -QFontMetrics(font).width(defaultMessage[i]) / 2
            y = -QFontMetrics(font).height() / 2
            w = QFontMetrics(font).width(defaultMessage[i])
            h = QFontMetrics(font).height()

            r = QRectF(x, y, w, h)
            painter.setPen(QPen(Qt.white, 2))
            painter.drawText(r, defaultMessage[i])
            if i % 2 == 0:
                painter.setPen(QPen(Qt.red, 2))
            else:
                painter.setPen(QPen(Qt.green, 2))

            painter.restore()
            steps += messageSpacing[i] / 2


class dialogSkinPreviewBuilder(QDialog):

    def __init__(self, rootFolder):
        super(dialogSkinPreviewBuilder, self).__init__()
        self.init_ui()
        self.builderList = []
        self.rootFolder = rootFolder
        self.subTheme = {}

    def init_ui(self):

        self.refreshButton = QPushButton("Refresh", self)
        self.loadXMLTextButton = QPushButton("Build from xml", self)
        self.openXMLButton = QPushButton("Open xml file", self)
        self.resetButton = QPushButton("Reset All", self)
        self.saveSkinButton = QPushButton("Save As ...")
        self.exitSkinButton = QPushButton("Exit")
        self.combobox = QComboBox(self)
        self.applySubThemeButton = QPushButton("Apply sub-theme")

        self.applySubThemeButton.clicked.connect(self.applySelectedSubTheme)
        self.loadXMLTextButton.clicked.connect(self.fillTextFromXML)
        self.openXMLButton.clicked.connect(self.openXMLFile)
        self.saveSkinButton.clicked.connect(self.onSaveSkin)
        self.resetButton.clicked.connect(self.resetAll)
        self.refreshButton.clicked.connect(self.arrangeLayout)
        self.exitSkinButton.clicked.connect(self.reject)

        self.box = QGroupBox("Skin managment", self)
        hlayout = QHBoxLayout(self)
        hlayout.addWidget(self.combobox)
        hlayout.addWidget(self.applySubThemeButton)
        hSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        hlayout.addItem(hSpacer)
        hlayout.addWidget(self.refreshButton)
        hlayout.addWidget(self.loadXMLTextButton)
        hlayout.addWidget(self.openXMLButton)
        hlayout.addWidget(self.resetButton)
        hlayout.addWidget(self.saveSkinButton)
        hlayout.addWidget(self.exitSkinButton)

        self.box.setLayout(hlayout)
        self.layout = QGridLayout(self)

    def addSubThemes(self, name, folderName):
        self.combobox.addItem(name)
        self.subTheme[name] = folderName

    def fillTextFromXML(self):
        for builder in self.builderList:
            builder.updatePix(True)

    def openXMLFile(self):
        QDesktopServices.openUrl(QUrl(self.rootFolder + "/descriptor.xml"))

    def addBuilder(self, builder):
        self.builderList.append(builder)

    def resetAll(self):
        for builder in self.builderList:
            builder.resetPixmap()

        self.arrangeLayout()
        QApplication.processEvents()

    def applySelectedSubTheme(self):

        i=0
        for builder in self.builderList:
            i= i+1
            print("Applying overlay : " + str(i) + "/" +  str(len(self.builderList)))
            builder.applyOverlay(self.subTheme[self.combobox.currentText()])

        self.arrangeLayout()
        QApplication.processEvents()

    def onSaveSkin(self):

        name, ok = QInputDialog.getText(self, 'Skin name', 'Enter the name for your skin:')
        if ok:
            self.generationPath = "../photobooth/skin/chalk/" + name

            if not os.path.exists(self.generationPath):
                os.makedirs(self.generationPath)
            if not os.path.exists(self.generationPath + "/pages"):
                os.makedirs(self.generationPath + "/pages")
            if not os.path.exists(self.generationPath + "/layouts"):
                os.makedirs(self.generationPath + "/layouts")

            source = [s for s in os.listdir(self.rootFolder + "/layouts/") if s.endswith('.png')]
            destination = self.generationPath + "/layouts/"
            for files in source:
                shutil.copy(self.rootFolder + "/layouts/" + files, destination)

            source = [s for s in os.listdir(self.rootFolder + "/pages/") if s.endswith('.png')]
            destination = self.generationPath + "/pages/"
            for files in source:
                shutil.copy(self.rootFolder + "/pages/" + files, destination)

            shutil.copy(self.rootFolder + "/descriptor.xml", self.generationPath + "/")

    def arrangeLayout(self):

        n = len(self.builderList)

        i = 1
        j = 0
        for builder in self.builderList:
            vlayout = QVBoxLayout(self)
            previewLabel = QLabel(self)
            previewLabel.setToolTip(builder.inputFilePath + "/" + builder.inputFileName)
            edit = QPushButton("Fill text", self)
            resetItem = QPushButton("Reset", self)
            vlayout.addWidget(previewLabel)
            vlayout.addWidget(resetItem)
            vlayout.addWidget(edit)
            p = QPixmap(builder.inputFilePath + "/" + builder.inputFileName)
            previewLabel.setPixmap(
                p.scaled(p.width() / 10, p.height() / 10, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            self.layout.addLayout(vlayout, i, j)
            edit.clicked.connect(builder.exec)
            #builder.finished.connect(self.arrangeLayout)
            resetItem.clicked.connect(builder.resetPixmap)
            j += 1
            if j == 4:
                j = 0
                i += 1

        self.layout.addWidget(self.box, i + 1, 0, 4, 0)
        self.setLayout(self.layout)


class dialogSkinBuilder(QDialog):

    def __init__(self, input, filename, inputTemplate):
        super(dialogSkinBuilder, self).__init__()
        self.inputFilePath = input
        self.inputFileName = filename
        self.inputTemplateFilePath = inputTemplate

        self.init_ui()
        self.currentMessagesDatas = []

    def init_ui(self):

        # Creating a label
        self.previewLabel = QLabel(self)
        self.updatePushButton = QPushButton("Preview", self)
        self.updatePushButton.clicked.connect(self.onUpdate)

        self.savePushButton = QPushButton("Validate", self)
        self.savePushButton.clicked.connect(self.onSave)

        self.skipPushButton = QPushButton("Cancel", self)
        self.skipPushButton.clicked.connect(self.onSkip)

        self.vboxLayout = QVBoxLayout(self)
        # Adding the widgets
        self.vboxLayout.addWidget(self.previewLabel)

        hl = QVBoxLayout(self)
        hl.addWidget(self.updatePushButton)
        hl.addWidget(self.savePushButton)
        hl.addWidget(self.skipPushButton)

        self.vboxLayout.addLayout(hl)

        # Setting the hBoxLayout as the main layout
        self.setLayout(self.vboxLayout)
        self.setWindowTitle('Skin builder for ' + self.inputFilePath + "/" + self.inputFileName)
        self.copyBasePixmap()

    def resetPixmap(self):
        shutil.copy(self.inputFilePath + "/" + self.inputFileName + ".origin",
                    self.inputFilePath + "/" + self.inputFileName)

    def copyBasePixmap(self):
        shutil.copy(self.inputFilePath + "/" + self.inputFileName,
                    self.inputFilePath + "/" + self.inputFileName + ".origin")

    def applyOverlay(self, filename):

        self.overlayFilename = self.inputTemplateFilePath + "/" + filename + "/" + self.inputFileName

        # print(self.overlayFilename)
        overLay = QPixmap(self.overlayFilename)
        outPixmap = QPixmap(self.inputFilePath + "/" + self.inputFileName)

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, overLay)
        painter.setPen(QColor(255, 255, 255))

        normPath = os.path.normpath(self.inputFilePath + "/" + self.inputFileName)
        file = QFile(normPath)
        file.open(QIODevice.WriteOnly)
        outPixmap.save(file, "PNG")

        del painter

    def addTextInput(self, data):

        hboxLayout = QHBoxLayout(self)
        label = QLabel("Texte " + data["location"], self)
        lineEdit = QLineEdit(data["defaultMessage"], self)
        hboxLayout.addWidget(label)
        hboxLayout.addWidget(lineEdit)
        self.vboxLayout.addLayout(hboxLayout)
        dataDict = {}
        dataDict["linedit"] = lineEdit
        dataDict["descriptor"] = data
        self.currentMessagesDatas.append(dataDict)

    #  c1 = QPointF(lay["x1"], lay["y1"])
    #  c2 = QPointF(lay["x2"], lay["y2"])
    #  c3 = QPointF(lay["x3"], lay["y3"])
    #  c4 = QPointF(lay["x4"], lay["y4"])

    def onUpdate(self):
        self.updatePix(False)

    def onSkip(self):
        self.reject()

    def onSave(self):
        self.updatePix(True)
        self.accept()

    def exec(self):
        self.onUpdate()
        super(dialogSkinBuilder, self).exec()

    def updatePix(self, save):

        # print("update")
        outPixmap = QPixmap(self.inputFilePath + "/" + self.inputFileName)
        # print(self.inputFilePath)

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(255, 255, 255))

        for dict in self.currentMessagesDatas:
            msg = dict["linedit"].text()
            self.drawTextAlongCubic(dict["descriptor"], painter, "", msg)

        self.previewLabel.setPixmap(outPixmap.scaled(outPixmap.width() / 3, outPixmap.height() / 3, Qt.KeepAspectRatio,
                                                     transformMode=Qt.SmoothTransformation))

        if save == True:
            normPath = os.path.normpath(self.inputFilePath + "/" + self.inputFileName)
            file = QFile(normPath)
            file.open(QIODevice.WriteOnly)
            outPixmap.save(file, "PNG")

        del painter

    def drawTextAlongCubic(self, lay, painter, filename, msg):

        fs = lay["defaultFontSize"]
        font = QFont('Right Chalk', fs)

        defaultMessage = msg

        if len(msg) == 0:
            return

        c1 = QPointF(lay["x1"], lay["y1"])
        c2 = QPointF(lay["x2"], lay["y2"])
        c3 = QPointF(lay["x3"], lay["y3"])
        c4 = QPointF(lay["x4"], lay["y4"])
        path = QPainterPath(c1)
        path.cubicTo(c2, c3, c4)
        # painter.drawPath(path)

        pathLength = path.length()
        textMetricLength = QFontMetrics(font).width(defaultMessage)

        fsn = int(fs * pathLength / (textMetricLength) * .95)
        if fsn > 70:
            fsn = 70
        font = QFont('Right Chalk', fsn)

        textMetricLength = QFontMetrics(font).width(defaultMessage)

        messageSpacing = []
        defaultMessageM = []
        sumMessageSpacing = 0.0

        for i in range(len(defaultMessage)):
            messageSpacing.append(QFontMetrics(font).width(defaultMessage[i]))
            sumMessageSpacing += messageSpacing[i]

        for i in range(len(defaultMessage)):
            messageSpacing[i] = messageSpacing[i] / sumMessageSpacing

        steps = 0
        painter.setFont(font)

        for i in range(len(defaultMessage)):

            steps += messageSpacing[i] / 2
            point = QPointF(path.pointAtPercent(steps))
            angle = path.angleAtPercent(steps)

            painter.save()
            painter.translate(point)
            painter.rotate(-angle)
            x = -QFontMetrics(font).width(defaultMessage[i]) / 2
            y = -QFontMetrics(font).height() / 2
            w = QFontMetrics(font).width(defaultMessage[i])
            h = QFontMetrics(font).height()

            r = QRectF(x, y, w, h)
            painter.setPen(QPen(Qt.white, 2))
            painter.drawText(r, defaultMessage[i])
            if i % 2 == 0:
                painter.setPen(QPen(Qt.red, 2))
            else:
                painter.setPen(QPen(Qt.green, 2))
            # painter.drawRect(r)

            painter.restore()
            steps += messageSpacing[i] / 2


def test(nb):
    txt = "  UNE  PHOTO  N'A  PAS  PU  ETRE  PRISE ! "
    if nb > 1:
        txt = str(int(nb)) + "  PHOTOS  N'ONT  PAS  PU  ETRE  PRISE !"
    resources = ressourcesManager()
    outPixmap = QPixmap(resources.getPath(ressourcesManager.PATH.PAGE) + "/onError.png")
    painter = QPainter(outPixmap)
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
    outPixmap.save(str(nb) + "toto.png", "PNG")


if __name__ == '__main__':

    app = QApplication(sys.argv)

    if len(sys.argv) == 4:
        if sys.argv[1] == "redoAssemblies":
            ass = Assembly(sys.argv[2], sys.argv[3])
            ass.redoAssemblies(True)
    if len(sys.argv) == 4:
        if sys.argv[1] == "redoAssemblies1Pict":
            ass = Assembly(sys.argv[2], sys.argv[3])
            ass.redoAssemblies1Pict()
    if len(sys.argv) == 4:
        if sys.argv[1] == "redoAssembliesRandom":
            ass = Assembly(sys.argv[2], sys.argv[3])
            ass.redoAssembliesRandom(True)
    if len(sys.argv) == 2:
        if sys.argv[1] == "buildskin":
            skBuilder = skinBuilder()
            # skBuilder.askUserName()
            skBuilder.createHierarchy()
            skBuilder.copyPagesToTemp()
            skBuilder.copyLayoutsToTemp()
            skBuilder.flattenSubtheme(False)
        elif sys.argv[1] == "buildskinCopyright":
            skBuilder = skinBuilder()
            skBuilder.createHierarchy()
            skBuilder.copyPagesToTemp()
            skBuilder.copyLayoutsToTemp()
            skBuilder.copyDescriptor()
            skBuilder.flattenSubtheme(True)
        elif sys.argv[1] == "buildskinInteractive":
            skBuilder = skinBuilder()
            skBuilder.setDescriptorFolder("../external/skin/chalk/templates")
            skBuilder.init()
            skBuilder.setOutpuFolder("../external/skin/chalk/testGene/tmp")
            skBuilder.copyFiles()
            skBuilder.buildSkinInteractively()

    sys.exit(1)
