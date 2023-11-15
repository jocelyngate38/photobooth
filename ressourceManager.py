#!/usr/bin/env python

import array
from enum import Enum
from operator import contains
import os
from PyQt5.QtCore import (QFile, QFileInfo, QSettings,
                          Qt, QIODevice)
from PyQt5.QtGui import QPixmap, QPainter, QColor, QTransform, QImage
from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow)

import sys
import xml.etree.ElementTree as ET
import random
import json
import platform
import uuid
import logging
import re
from datetime import datetime
import statistics
from glob import glob
from collections import Counter

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
        COPYRIGHT_IMAGE=15
        CALIBRATION_COUPLE_PATH=21
        CALIBRATION_GROUP_PATH=22
        CALIBRATION_WHITE_BG_PATH=23
        CALIBRATION_PATH_DEFAULT=23
        JSON_PATH=30
        CAPTURE_REGEN_PATH=31
        ASSEMBLY_REGEN_PATH=32

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
        self.current_json=None
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
        self.logger.info("CALIBRATION_COUPLE_PATH : " + self.getPath(self.PATH.CALIBRATION_COUPLE_PATH))
        self.logger.info("CALIBRATION_GROUP_PATH : " + self.getPath(self.PATH.CALIBRATION_GROUP_PATH))
        self.logger.info("CALIBRATION_WHITE_BG_PATH : " + self.getPath(self.PATH.CALIBRATION_WHITE_BG_PATH))        
        self.logger.info("JSON_PATH : " + self.getPath(self.PATH.JSON_PATH))
        self.logger.info("COPYRIGHT_IMAGE : " + self.getPath(self.PATH.COPYRIGHT_IMAGE))
        self.logger.info("CAPTURE_REGEN_PATH : " + self.getPath(self.PATH.CAPTURE_REGEN_PATH))
        self.logger.info("CAPTURE_REGEN_PATH : " + self.getPath(self.PATH.CAPTURE_REGEN_PATH))

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
        print("CALIBRATION_COUPLE_PATH : " + self.getPath(self.PATH.CALIBRATION_COUPLE_PATH))
        print("CALIBRATION_GROUP_PATH : " + self.getPath(self.PATH.CALIBRATION_GROUP_PATH))
        print("CALIBRATION_WHITE_BG_PATH : " + self.getPath(self.PATH.CALIBRATION_WHITE_BG_PATH))
        print("JSON_PATH : " + self.getPath(self.PATH.JSON_PATH))
        print("COPYRIGHT_IMAGE : " + self.getPath(self.PATH.COPYRIGHT_IMAGE))
        print("CAPTURE_REGEN_PATH : " + self.getPath(self.PATH.CAPTURE_REGEN_PATH))
        print("CAPTURE_REGEN_PATH : " + self.getPath(self.PATH.CAPTURE_REGEN_PATH))
        print("============================================================")

    def getSkinPageDatas(self):

        return self.skinPageDatas

    def getSkinLayoutDatas(self):

        return self.skinLayoutDatas

    def getMaxImageCount(self):

        return  self.nbImageMax

    def setPath(self, Path, value):

        if not os.path.exists(value):
            os.makedirs(value)
        if Path == ressourcesManager.PATH.CAPTURE:
            self.capturePath = value
        if Path == ressourcesManager.PATH.COPYRIGHT_IMAGE:
            self.copyrightImagePath = value
        if Path == ressourcesManager.PATH.CALIBRATION_GROUP_PATH:
            self.calibrationGroupPath = value
        if Path == ressourcesManager.PATH.CALIBRATION_COUPLE_PATH:
            self.calibrationCouplePath = value
        if Path == ressourcesManager.PATH.CALIBRATION_WHITE_BG_PATH:
            self.calibrationWhiteBgPath = value
        if Path == ressourcesManager.PATH.JSON_PATH:
            self.jsonPath = value
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
        if Path == ressourcesManager.PATH.CAPTURE_REGEN_PATH:
            self.captureRegenPath = value
        if Path == ressourcesManager.PATH.ASSEMBLY_REGEN_PATH:
            self.assembliesRegenPath = value

    def getPath(self, Path):

        if Path == ressourcesManager.PATH.CAPTURE:
            return self.capturePath
        if Path == ressourcesManager.PATH.COPYRIGHT_IMAGE:
            return self.copyrightImagePath
        if Path == ressourcesManager.PATH.CALIBRATION_GROUP_PATH:
            return self.calibrationGroupPath
        if Path == ressourcesManager.PATH.CALIBRATION_COUPLE_PATH:
            return self.calibrationCouplePath
        if Path == ressourcesManager.PATH.CALIBRATION_WHITE_BG_PATH:
            return self.calibrationWhiteBgPath
        if Path == ressourcesManager.PATH.JSON_PATH:
            return self.jsonPath
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
        if Path == ressourcesManager.PATH.CAPTURE_REGEN_PATH:
            return self.captureRegenPath
        if Path == ressourcesManager.PATH.ASSEMBLY_REGEN_PATH:
            return self.assembliesRegenPath

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

        self.calibrationGroupPath = self.applicationPath + "/resources/calibration/group"
        self.calibrationGroupPath = os.path.normpath(self.calibrationGroupPath)
        
        self.calibrationCouplePath = self.applicationPath + "/resources/calibration/couple"
        self.calibrationCouplePath = os.path.normpath(self.calibrationCouplePath)

        self.calibrationWhiteBgPath = self.applicationPath + "/resources/calibration/white-bg"
        self.calibrationWhiteBgPath = os.path.normpath(self.calibrationWhiteBgPath)

        self.copyrightImagePath = self.applicationPath + "/resources/calibration/copyright_image.png"
        self.copyrightImagePath = os.path.normpath(self.copyrightImagePath)

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

        self.jsonPath = self.applicationDataPath + "/" + self.eventName + "/json_files"
        if not os.path.exists(self.jsonPath):
            os.makedirs(self.jsonPath)
        self.jsonPath = os.path.normpath(self.jsonPath)

        self.captureRegenPath = self.applicationDataPath + "/" + self.eventName + "/regen/captures"
        if not os.path.exists(self.captureRegenPath):
            os.makedirs(self.captureRegenPath)
        self.captureRegenPath = os.path.normpath(self.captureRegenPath)

        self.assembliesRegenPath = self.applicationDataPath + "/" + self.eventName + "/regen/assemblies"
        if not os.path.exists(self.assembliesRegenPath):
            os.makedirs(self.assembliesRegenPath)
        self.capturassembliesRegenPathePath = os.path.normpath(self.assembliesRegenPath)

        self.skinLayoutDatas = [[], [], [], []]

        self.nbImageMax = 0

        self.homePageDisplayFilename = ""

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
                self.logger.error("FILE NOT FOUND : " +self.eventName + "/" + path + " IGNORING")
                image = QImage(2000, 1400, QImage.Format_ARGB32)
                image.fill(Qt.transparent)
                image.save(self.getPath(ressourcesManager.PATH.EVENT) + "/" + path)
                

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
                imageDict["angle"] = float(im.find("./angle").text)
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

    def currentLayoutCount(self, n):

        return len(self.getSkinLayoutDatas()[n - 1])

    def randomizeFirstLayoutChoice(self, n):

        choosenLayoutList = self.getSkinLayoutDatas()[n - 1]
        nLayouts = len(choosenLayoutList)
        self.lastChoice = random.randint(0, nLayouts-1)

    def chooseNextLayout(self, n, forcedId=None):

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

        if forcedId is not None:
            for layout in choosenLayoutList:
                if layout["layoutId"] == forcedId:
                    self.lastChoice=0
                    self.logger.info("CHOOSEN LAYOUT ID ("+str(forcedId)+")")
                    return layout

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

            
    def suggest_next_filename(self, path):
        # Regular expression to match filenames like capture_0001.jpg
        pattern = re.compile(r'asm_(\d+)\.jpg')
        
        max_number = 0
        for filename in os.listdir(path):
            match = pattern.match(filename)
            if match:
                num = int(match.group(1))
                if num > max_number:
                    max_number = num

        # Suggest next filename
        next_number = max_number + 1
        return f"asm_{next_number:04}"


    def suggest_session_id(self, path):
        # Regular expression to match filenames like capture_0001.jpg
        pattern = re.compile(r'session_(\d+)\.json')
        
        max_number = 0
        for filename in os.listdir(path):
            match = pattern.match(filename)
            if match:
                num = int(match.group(1))
                if num > max_number:
                    max_number = num

        # Suggest next filename
        next_number = max_number + 1
        return f"session_{next_number:04}"
    
    def create_session_json(self):
        name = self.suggest_session_id(self.getPath(ressourcesManager.PATH.JSON_PATH))
        self.current_json =  {
            'name': name,
            'print_count':0,
            'discarded_files':[],
            'start': datetime.now().timestamp()
        }
        self.write_current_json_file()

    def add_discarded_capture(self,  filePath):
        if self.current_json is not None:
            fName=os.path.basename(filePath)
            self.current_json['discarded_files'].append(fName)
            self.write_current_json_file()

    def add_session_assembly_details(self, layout_id=None, staged_files=None, outputFile=None):
        if self.current_json is not None:
            if staged_files is not None:
                fl=[]
                for f in staged_files:
                    fl.append(os.path.basename(f))
                self.current_json['staged_files'] = fl

            if layout_id is not None and outputFile is not None:

                json_assembly = {"layout_id": layout_id, "output": outputFile}
                # Check if 'assemblies' exists in the data
                if 'assemblies' in self.current_json:
                    # If it exists, append the new object
                    self.current_json['assemblies'].append(json_assembly)
                else:
                    # If it doesn't exist, create it as a new list with the new object
                    self.current_json['assemblies'] = [json_assembly]

            self.write_current_json_file()

    def add_print_event(self, printId, fileName):

        if self.current_json is not None:
            if printId is not None and fileName is not None:

                json_print = {"printId": printId, "fileName": fileName, "timestamp": datetime.now().timestamp()}
                # Check if 'assemblies' exists in the data
                if 'print_jobs' in self.current_json:
                    # If it exists, append the new object
                    self.current_json['print_jobs'].append(json_print)
                else:
                    # If it doesn't exist, create it as a new list with the new object
                    self.current_json['print_jobs'] = [json_print]

                if 'print_count' in self.current_json:
                    self.current_json['print_count']=1+self.current_json['print_count']
                else:
                    self.current_json['print_count']=1

                self.write_current_json_file()

    def add_print_error_event(self, printId, fileName, cause):

        if self.current_json is not None:
            if printId is not None and fileName is not None:
                if 'print_jobs' in self.current_json:
                    json_print_error = {"printId": printId, "fileName": fileName, "error": cause, "timestamp": datetime.now().timestamp()}
                    # Check if 'assemblies' exists in the data
                    if 'print_errors' in self.current_json:
                        # If it exists, append the new object
                        self.current_json['print_errors'].append(json_print_error)
                    else:
                        # If it doesn't exist, create it as a new list with the new object
                        self.current_json['print_errors'] = [json_print_error]

                    self.write_current_json_file()


    def increase_session_value(self, field_name):
        if self.current_json is not None:
            if field_name in self.current_json:
                self.current_json[field_name]=1+self.current_json[field_name]
            else:
                self.current_json[field_name]=1
            self.write_current_json_file()

    def increase_session_trigger_capture_count(self):
        self.increase_session_value(field_name='trigger_capture_error')
    
    def write_current_json_file(self):
        if self.current_json is not None:
            if not 'name' in self.current_json:
                self.logger.error("CANNOT WRITE JSON, name not found")
                return
            jsonPath = self.getPath(ressourcesManager.PATH.JSON_PATH)
            fpath = jsonPath + "/" + self.current_json['name']+".json"
            self.current_json['end'] = datetime.now().timestamp()
            self.current_json['duration'] = self.current_json['end'] - self.current_json['start']
            with open(fpath, 'w') as json_file:
                json.dump(self.current_json, json_file, indent=4)
        


    def load_and_normalize(self, file):
        data = json.load(file)
        return data if isinstance(data, list) else [data]

    def rebuildAllAssembly(self, jsonFolder, scaleFactor=1):

        #Find all JSON files in a particular folder
        folder_path = jsonFolder#
        #self.getPath(ressourcesManager.PATH.JSON_PATH)
        json_file_paths = glob(os.path.join(folder_path, "*.json"))

        #Initialize an empty list to store the JSON data from each file
        json_data_list = []

        #Loop through each file path in the list
        for json_file_path in json_file_paths:
            
            # Check if the file exists
            if os.path.exists(json_file_path):
                
                # Open the file and read the JSON data
                with open(json_file_path, 'r') as json_file:
                    try:
                        json_data_list.extend(self.load_and_normalize(json_file))
                        #json_data = json.load(json_file)
                        # Add the JSON data to the list
                        #json_data_list.append(json_data)
                    except:
                        print(json_file_path)
            else:
                print(f"File not found: {json_file_path}")



        for json_data in json_data_list:
            self.rebuildLayoutFromJson(jsonData=json_data, scaleFactor=scaleFactor)

    def rebuildLayoutFromJson(self, jsonData, scaleFactor):

        if 'assemblies' not in jsonData:
            return

        jsm = jsonData['assemblies']

        for jsonDataAsm in jsm:
        
            if 'name' in jsonData:
                name = jsonData['name']
            else:
                self.logger.error(f"missing key : name -> skipping rebuild")
                return
            
            if 'staged_files' in jsonData:
                staged_files = jsonData['staged_files']
            else:
                self.logger.error(f"missing key : staged_files -> skipping rebuild")
                return
            
            if 'output' in jsonDataAsm:
                asmPath = self.getPath(ressourcesManager.PATH.ASSEMBLY_REGEN_PATH) + "/"
                output = jsonDataAsm['output']
            else:
                self.logger.error(f"missing key : output -> skipping rebuild")
                return
            
            if 'layout_id' in jsonDataAsm:
                layout_id = jsonDataAsm['layout_id']
            else:
                self.logger.error(f"missing key : layout_id -> skipping rebuild")
                return
            
            captures=[]

            self.logger.info(f"REBUILDING ASSEMBLY : {name}")

            regenCaptPath = self.getPath(ressourcesManager.PATH.CAPTURE_REGEN_PATH) + "/"
            captPath = self.getPath(ressourcesManager.PATH.CAPTURE) + "/"

            for filename in staged_files:
                filepath = regenCaptPath + filename
                #check if file is present in regen capture folder first
                if not os.path.isfile(filepath):
                    self.logger.warning(f"MISSING STAGED CAPTURE IN REGEN FOLDER: {filename} CHECKING IN CAPTURE FOLDER")
                    filepath = captPath + filename
                    if not os.path.isfile(filepath):
                        self.logger.error(f"MISSING STAGED CAPTURE IN REGEN AND CAPTURE FOLDER: {filename} ABORTING")
                        return
                    else:
                        captures.append(filepath)
                else:
                    captures.append(filepath)

            choosenLayout = self.chooseNextLayout(len(staged_files), forcedId=layout_id)
                    
            self.buildLayoutFromList(captureList=captures, choosenLayout=choosenLayout, cuttingLines=False, copyright=False, outputPath=asmPath, outFilename=output, regenFlag=True, scaleFactor=scaleFactor)


    def buildLayoutFromList(self, captureList, choosenLayout, cuttingLines=False, copyright=False, outputPath=None, outFilename=None, regenFlag=False, scaleFactor=1):

        layoutId = choosenLayout["layoutId"]
        nbImages = choosenLayout["nbImages"]
        
        if outputPath is None:
            assemblyPath = self.getPath(ressourcesManager.PATH.ASSEMBLIES) + "/"
        else:
            assemblyPath = outputPath

        if outFilename is None:
            _outFileName = self.suggest_next_filename(assemblyPath) + ".jpg"
        else:
            _outFileName = outFilename

        outFile = assemblyPath + _outFileName

        files=[]
        
        layoutPixPath = self.getPath(ressourcesManager.PATH.EVENT) + "/" + choosenLayout["filename"]

        if not os.path.isfile(layoutPixPath):
            self.logger.warning("THE CURRENT LAYOUT TEMPLATE DOES NOT EXISTS")
            return

        pixLayout = QPixmap(layoutPixPath)
        if scaleFactor != 1:
            w = pixLayout.width()*scaleFactor
            pixLayout = pixLayout.scaledToWidth(w)
        outPixmap = QPixmap(pixLayout.size())
        outPixmap.fill(Qt.transparent)
        
        pictures = captureList.copy()
    
        # only randomize to be abble to reproduct
        if regenFlag is False:
            random.shuffle(pictures)

        painter = QPainter(outPixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        for i in range(nbImages):
            path = pictures.pop()
            files = [path] + files

            x = choosenLayout["images"][(i + 1)]["x"]*scaleFactor
            y = choosenLayout["images"][(i + 1)]["y"]*scaleFactor
            w = choosenLayout["images"][(i + 1)]["w"]*scaleFactor
            h = choosenLayout["images"][(i + 1)]["h"]*scaleFactor
            angle = choosenLayout["images"][(i + 1)]["angle"]

            pix = QPixmap(path)
            
            if(w/h > 4/3):           
                pix = pix.scaledToWidth(w)
            else:
                pix = pix.scaledToHeight(h)


            # Create a QTransform object for rotation
            transform = QTransform()

            # Translate so the center of the pixmap goes to the origin, then rotate, then translate it back.
            transform.translate(-x + w/2, -y + h/2)
            transform.rotate(angle)
            transform.translate(x - w/2, y - h/2)

            rotated_pixmap = pix.transformed(transform, Qt.SmoothTransformation)

            # Place the pixmap on the layout image using painter
            painter.drawPixmap(x - rotated_pixmap.width() // 2, y - rotated_pixmap.height() // 2, rotated_pixmap)

            if nbImages == 1 and len(choosenLayout["images"]) > 1:
                for a in range( 1, len(choosenLayout["images"])+1):
                    x = choosenLayout["images"][(i + a)]["x"]*scaleFactor
                    y = choosenLayout["images"][(i + a)]["y"]*scaleFactor
                    w = choosenLayout["images"][(i + a)]["w"]*scaleFactor
                    h = choosenLayout["images"][(i + a)]["h"]*scaleFactor
                    angle = choosenLayout["images"][(i + a)]["angle"]

                    pix = QPixmap(path)

                    if (w / h > 4 / 3):
                        pix = pix.scaledToWidth(w)
                    else:
                        pix = pix.scaledToHeight(h)

                        # Create a QTransform object for rotation
                        transform = QTransform()

                        # Translate so the center of the pixmap goes to the origin, then rotate, then translate it back.
                        transform.translate(-x + w/2, -y + h/2)
                        transform.rotate(angle)
                        transform.translate(x - w/2, y - h/2)

                        rotated_pixmap = pix.transformed(transform, Qt.SmoothTransformation)

                        # Place the pixmap on the layout image using painter
                        painter.drawPixmap(x - rotated_pixmap.width() // 2, y - rotated_pixmap.height() // 2, rotated_pixmap)

        painter.drawPixmap(0, 0, pixLayout)

        if cuttingLines is True:
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

            if copyright is True:
                copyrightPath = self.getPath(ressourcesManager.PATH.COPYRIGHT_IMAGE)
                copyrightPix = QPixmap(copyrightPath)
                painter.drawPixmap(0,0,copyrightPix)

        if regenFlag is False:
            self.add_session_assembly_details( layout_id=str(layoutId), staged_files=files, outputFile=_outFileName)

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




class statisticsToolbox:

    logger = logging.getLogger("statisticsToolb")

    durations={}
    discarded_files={}
    staged_files={}
    prints={}
    print_errors={}
    timeouts={}
    trigger_errros={}
    session_layout_size={}
    session_count=0
    ignored_json = []
    print_errors_causes = {}

    def __init__(self ):
        self.initValues()
        pass

    def initValues(self):
                    
            self.durations['mean']          = 0
            self.durations['median']        = 0
            self.durations['max']           = 0
            self.durations['min']           = 0
            self.durations['total']         = 0

            self.discarded_files['mean']    = 0
            self.discarded_files['median']  = 0
            self.discarded_files['max']     = 0
            self.discarded_files['min']     = 0
            self.discarded_files['total']   = 0

            self.staged_files['mean']       = 0
            self.staged_files['median']     = 0
            self.staged_files['max']        = 0
            self.staged_files['min']        = 0
            self.staged_files['total']      = 0
        
            self.prints['mean']             = 0
            self.prints['median']           = 0
            self.prints['max']              = 0
            self.prints['min']              = 0
            self.prints['total']            = 0
        
            self.print_errors['mean']      = 0
            self.print_errors['median']    = 0
            self.print_errors['max']       = 0
            self.print_errors['min']       = 0
            self.print_errors['total']     = 0

            self.timeouts['mean']           = 0
            self.timeouts['median']         = 0
            self.timeouts['max']            = 0
            self.timeouts['min']            = 0
            self.timeouts['total']          = 0

            self.session_layout_size['1']   = 0
            self.session_layout_size['1%']  = 0
            self.session_layout_size['2']   = 0
            self.session_layout_size['2%']  = 0
            self.session_layout_size['3']   = 0
            self.session_layout_size['3%']  = 0
            self.session_layout_size['4']   = 0
            self.session_layout_size['4%']  = 0

            self.session_count = 0
            self.ignored_json.clear()

    def updateStatistics(self, jsonFolder):

        self.initValues()

        #Find all JSON files in a particular folder
        folder_path = jsonFolder#
        #self.getPath(ressourcesManager.PATH.JSON_PATH)
        json_file_paths = glob(os.path.join(folder_path, "*.json"))

        #Initialize an empty list to store the JSON data from each file
        json_data_list = []
        

        #Loop through each file path in the list
        for json_file_path in json_file_paths:
            
            # Check if the file exists
            if os.path.exists(json_file_path):
                
                # Open the file and read the JSON data
                with open(json_file_path, 'r') as json_file:
                    
                    try:
                        json_data = json.load(json_file)
                        if 'assemblies' in json_data:
                            # Add the JSON data to the list
                            json_data_list.append(json_data)
                        else:
                            self.logger.error(f"File : {json_file_path} have no key assemblies, skipping")
                            self.ignored_json.append(os.path.basename(json_file_path))
                    except:
                        self.logger.error(f"File : {json_file_path} cannot be converted to json, skipping")
                        
            else:
                self.logger.error(f"File not found: {json_file_path}")

        # Initialize lists to store durations and number of discarded files
        durations_list = []
        discarded_file_list = []
        staged_file_list = []
        trigger_capture_error_list = []
        print_jobs_list = []
        print_errors_list = []
        print_errors_cause_list = []
        timeout_list = []

        self.session_count=len(json_data_list)

        # Loop through each JSON object and extract the data
        for json_data in json_data_list:

            if "duration" in json_data:
                durations_list.append(json_data["duration"])
            else:
                durations_list.append(0)
            
            if "discarded_files" in json_data:
                discarded_file_list.append(len(json_data["discarded_files"]))
            else:
                discarded_file_list.append(0)

            if "staged_files" in json_data:
                staged_file_list.append(len(json_data["staged_files"]))
            else:
                staged_file_list.append(0)
                
            if "trigger_capture_error" in json_data:
                trigger_capture_error_list.append(json_data["trigger_capture_error"])
            else:
                trigger_capture_error_list.append(0)
            
            if "print_jobs" in json_data:
                print_jobs_list.append(len(json_data["print_jobs"]))
            else:
                print_jobs_list.append(0)
            
                
            if "print_errors" in json_data:
                print_errors_list.append(len(json_data["print_errors"]))
                array=json_data["print_errors"]
                for item in array:
                    if "error" in item:
                        print_errors_cause_list.append(item["error"])
            else:
                print_errors_list.append(0)

            timeoutCount=0
            if "validate_timeout" in json_data:
                timeoutCount=timeoutCount+json_data["validate_timeout"]
            if "display_assembly_timeout" in json_data:
                timeoutCount=timeoutCount+json_data["display_assembly_timeout"]
            if "trigger_error_timeout" in json_data:
                timeoutCount=timeoutCount+json_data["trigger_error_timeout"]

            timeout_list.append(timeoutCount)

        # Calculate statistics
        if len(durations_list) > 1:
            self.durations['mean'] = statistics.mean(durations_list)
            self.durations['median'] = statistics.median(durations_list)
            self.durations['max'] = max(durations_list)
            self.durations['min'] = min(durations_list)
            self.durations['total'] = sum(durations_list)

        if len(discarded_file_list) > 1:
            self.discarded_files['mean'] = statistics.mean(discarded_file_list)
            self.discarded_files['median'] = statistics.median(discarded_file_list)
            self.discarded_files['max'] = max(discarded_file_list)
            self.discarded_files['min'] = min(discarded_file_list)
            self.discarded_files['total'] = sum(discarded_file_list)

        if len(staged_file_list) > 1:
            self.staged_files['mean'] = statistics.mean(staged_file_list)
            self.staged_files['median'] = statistics.median(staged_file_list)
            self.staged_files['max'] = max(staged_file_list)
            self.staged_files['min'] = min(staged_file_list)
            self.staged_files['total'] = sum(staged_file_list)
        
        if len(print_jobs_list) > 1:
            self.prints['mean'] = statistics.mean(print_jobs_list)
            self.prints['median'] = statistics.median(print_jobs_list)
            self.prints['max'] = max(print_jobs_list)
            self.prints['min'] = min(print_jobs_list)
            self.prints['total']= sum(print_jobs_list)

        if len(print_errors_list) > 1:
            self.print_errors['mean'] = statistics.mean(print_errors_list)
            self.print_errors['median'] = statistics.median(print_errors_list)
            self.print_errors['max'] = max(print_errors_list)
            self.print_errors['min'] = min(print_errors_list)
            self.print_errors['total']= sum(print_errors_list)    

        if len(timeout_list) > 1:
            self.timeouts['mean'] = statistics.mean(timeout_list)
            self.timeouts['median'] = statistics.median(timeout_list)
            self.timeouts['max'] = max(timeout_list)
            self.timeouts['min'] = min(timeout_list)
            self.timeouts['total'] = sum(timeout_list)

        count = Counter(staged_file_list)

        total = len(staged_file_list)

        self.session_layout_size['1'] = count[1]
        self.session_layout_size['1%'] = (count[1] / total) * 100
        
        self.session_layout_size['2'] = count[2]
        self.session_layout_size['2%'] = (count[2] / total) * 100
        
        self.session_layout_size['3'] = count[3]
        self.session_layout_size['3%'] = (count[3] / total) * 100
        
        self.session_layout_size['4'] = count[4]
        self.session_layout_size['4%'] = (count[4] / total) * 100

        counterPrintError = Counter(print_errors_cause_list)

        for item in counterPrintError:
            self.print_errors_causes[item]=counterPrintError[item]

        if EMULATE is True:
            self.display()

        self.logger.info("updateStatistics done for " + jsonFolder)

    def seconds_to_readable_time(self, seconds):
        if seconds < 0:
            return "Invalid Input " + str(seconds) 
        
        seconds = int(seconds)

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        time_string = ""
        
        if hours > 0:
            time_string += f"{hours:02d}h"
        if minutes > 0 or hours > 0:
            time_string += f"{minutes:02d}m"
        if seconds > 0 or minutes > 0 or hours > 0:
            time_string += f"{seconds:02d}s"
        
        return time_string.strip()

    def display(self):

        # Print the statistics
        if len(self.ignored_json) > 0:
            print("================================")
            print(f" Ignored sessions ({len(self.ignored_json)})")
            print("--------------------------------")
            print(self.ignored_json)

        print("================================")        
        print("           STATISTICS")
        print("================================")
        print(" Duration")
        print("--------------------------------")
        print(f"  Average : {self.seconds_to_readable_time(self.durations['mean'])}")
        print(f"  Median  : {self.seconds_to_readable_time(self.durations['median'])}")
        print(f"  Maximum : {self.seconds_to_readable_time(self.durations['max'])}")
        print(f"  Minimum : {self.seconds_to_readable_time(self.durations['min'])}")

        print("================================")
        print(" Discarded images")
        print("--------------------------------")
        print(f"  Average : {round(self.discarded_files['mean'], 2)}")
        print(f"  Median  : {round(self.discarded_files['median'], 2)}")
        print(f"  Maximum : {self.discarded_files['max']}")
        print(f"  Minimum : {self.discarded_files['min']}")
        
        print("================================")
        print(" Staged images")
        print("--------------------------------")
        print(f"  Average : {round(self.staged_files['mean'], 2)}")
        print(f"  Median  : {round(self.staged_files['median'], 2)}")
        print(f"  Maximum : {self.staged_files['max']}")
        print(f"  Minimum : {self.staged_files['min']}")
        
        print("================================")
        print(" Prints")
        print("--------------------------------")
        print(f"  Average : {round(self.prints['mean'], 2)}")
        print(f"  Median  : {round(self.prints['median'], 2)}")
        print(f"  Maximum : {self.prints['max']}")
        print(f"  Minimum : {self.prints['min']}")
        
        print("================================")
        print(" Print errors")
        print("--------------------------------")
        print(f"  Average : {round(self.print_errors['mean'], 2)}")
        print(f"  Median  : {round(self.print_errors['median'], 2)}")
        print(f"  Maximum : {self.print_errors['max']}")
        print(f"  Minimum : {self.print_errors['min']}")

        print("================================")
        print(" Timeouts")
        print("--------------------------------")
        print(f"  Average : {round(self.timeouts['mean'], 2)}")
        print(f"  Median  : {round(self.timeouts['median'], 2)}")
        print(f"  Maximum : {self.timeouts['max']}")
        print(f"  Minimum : {self.timeouts['min']}")

        
        print("================================")
        print(" 1,2,3,4 photos par sessions")
        print("--------------------------------")
        print(f"  1 photo  : {round(self.session_layout_size['1'], 2)} | {round(self.session_layout_size['1%'], 2)} %")
        print(f"  2 photos : {round(self.session_layout_size['2'], 2)} | {round(self.session_layout_size['2%'], 2)} %")
        print(f"  3 photos : {round(self.session_layout_size['3'], 2)} | {round(self.session_layout_size['3%'], 2)} %")
        print(f"  4 photos : {round(self.session_layout_size['4'], 2)} | {round(self.session_layout_size['4%'], 2)} %")

        if self.print_errors['total'] != 0:
            print("================================")
            print(" Print errors types")
            print("--------------------------------")
            for it in self.print_errors_causes:
                print(f"{it} : {self.print_errors_causes[it]} | {round(100.0*self.print_errors_causes[it]/self.print_errors['total'], 2)} %")

        
        print("================================")
        print(" Totals")
        print("--------------------------------")
        print(f"  Sessions       : {self.session_count}")
        print(f"  Duration       : {self.seconds_to_readable_time(self.durations['total'])}")
        print(f"  Captures       : {self.staged_files['total'] + self.discarded_files['total']}")

        div = self.discarded_files['total']+self.staged_files['total']
        if div != 0:
            print(f"    Staged       : {self.staged_files['total']} | {round(100.0*self.staged_files['total']/(div),2)} %")
            print(f"    Discarded    : {self.discarded_files['total']} | {round(100.0*self.discarded_files['total']/(div),2)} %")
            
        print(f"  Print success  : {self.prints['total']-self.print_errors['total']}")
        print(f"    Print tried  : {self.prints['total']}")
        print(f"    Print errors : {self.print_errors['total']}")
        
        print(f"  Timeout        : {self.timeouts['total']}")
        print("================================")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    resources = ressourcesManager()
    conn = cups.Connection()
    printers = conn.getPrinters()
    self.logger.info(json.dumps(printers))
    sys.exit(1)
