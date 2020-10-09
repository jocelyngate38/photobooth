#!/usr/bin/env python
from enum import Enum
import os
from datetime import datetime
from PyQt5.QtCore import (QDateTime)

        
class logger():
    
    logFile=None
    
    def __init__(self, logFile):
        self.logFile=logFile
    
    def addInfo(self, message):
        dt=QDateTime(datetime.now()) 
        dateName=dt.toString("yyyyddMM_hh_mm_ss")
        with open(self.logFile, 'a') as file:
            file.write("INFO    : " + dateName + " : " + message + "\n")
        print("INFO    : " + dateName + " : " + message)

    def addWarning(self, message):
        dt=QDateTime(datetime.now()) 
        dateName=dt.toString("yyyyddMM_hh_mm_ss")
        with open(self.logFile, 'a') as file:
            file.write("WARNING : " + dateName + " : " + message + "\n")
        print("WARNING    : " + dateName + " : " + message)
            
    def addError(self, message):
        dt=QDateTime(datetime.now()) 
        dateName=dt.toString("yyyyddMM_hh_mm_ss")
        with open(self.logFile, 'a') as file:
            file.write("ERROR   : " + dateName + " : " + message + "\n")
        print("ERROR    : " + dateName + " : " + message)
            
