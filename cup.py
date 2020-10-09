#!/usr/bin/env python


import os
import cups
import time

from PyQt5.QtCore import QThread, pyqtSignal

class MonitorPrinterFaileure(QThread):
    printerFailure = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, path):
        QThread.__init__(self)


    # run method gets called when we start the thread
    def run(self):

        conn = cups.Connection()
        printers = conn.getPrinters ()
        for printer in printers:
        
            if printers[printer]['printer-state'] == 5:
                if printers[printer]["printer-state-message"] == "No paper tray loaded, aborting!":
                    print("no more paper, contact smbdy to add papers again")
                    self.printerFailure.emit(printer, 1)

            if printers[printer]['printer-state'] == 3:
                if printers[printer]["printer-state-message"] == "Ribbon depleted!":
                    print("Carttouche d'encre vide, contact smbdy to add papers again")
                    self.printerFailure.emit(printer, 2)

                if printers[printer]["printer-state-message"] =="Paper feed problem!" :
                    print("Plus de papier, veuillez en rajouter")
                    self.printerFailure.emit(printer, 3)





def removeNotCompletedJobs():
    conn = cups.Connection()
    for key,val in conn.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1).items():
        conn.cancelJob(key, purge_job=False)




conn = cups.Connection()
for key,val in conn.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1).items():
    conn.cancelJob(key, purge_job=False)
conn.enablePrinter('Canon_CP800')
conn.printFile('Canon_CP800', '/home/pi/Documents/boxaselfi_1.jpg', title='savethedate',options={})

while(1):
    printers = conn.getPrinters ()
    #for printer in printers:
    print(printers['Canon_CP800']['printer-state-message'])
    if printers['Canon_CP800']['printer-state'] == 5:
        if printers['Canon_CP800']["printer-state-message"] == "No paper tray loaded, aborting!":
            print("no more paper, contact smbdy to add papers again")
            #self.printerFailure.emit(printer, 1)

    if printers['Canon_CP800']['printer-state'] == 3:
        if printers['Canon_CP800']["printer-state-message"] == "Ribbon depleted!":
            print("Carttouche d'encre vide, contact smbdy to add papers again")
            #self.printerFailure.emit(printer, 2)

        if printers['Canon_CP800']["printer-state-message"] =="Paper feed problem!" :
            print("Plus de papier, veuillez en rajouter")
            #self.printerFailure.emit(printer, 3)
    time.sleep(1)

#removeNotCompletedJobs()
#conn.enablePrinter('Canon_CP800')
#exit()
#conn.printFile('Canon_CP800', '/home/pi/Documents/boxaselfi_1.jpg', title='savethedate',options={})
#time.sleep(10)
#conn.printFile('Canon_CP800', '/home/pi/Documents/boxaselfi_2.jpg', title='savethedate',options={})
#for i in range(70):
    #print(" seconde " + str(i))
    #conn = cups.Connection()
    #printers = conn.getPrinters ()
    #print(printers['Canon_CP800'])
    #print("not-completed jobs : ")
    #print(printers['Canon_CP800']["printer-state-message"] )
    #time.sleep(1)
    
    
    
#print(printers['Canon_CP800'])
#print(conn.getJobs(which_jobs='not-completed', my_jobs=False, limit=-1, first_job_id=-1))
#if printers['Canon_CP800']['printer-state'] == 5:
    #if printers['Canon_CP800']["printer-state-message"] == "No paper tray loaded, aborting!":
        #print("no more paper, contact smbdy to add papers again")

#if printers['Canon_CP800']['printer-state'] == 3:
    #if printers['Canon_CP800']["printer-state-message"] == "Ribbon depleted!":
        #print("Carttouche d'encre vide, contact smbdy to add papers again")
    #if printers['Canon_CP800']["printer-state-message"] =="Paper feed problem!" :
        #print("Plus de papier, veuillez en rajouter")
        
