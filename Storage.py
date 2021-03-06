# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 18:18:35 2017

@author: Kozmik
"""

from os.path import abspath
import os
import pickle
from tkinter import *
import DateTools
from tkinter import filedialog as filedialog
from inspect import getsourcefile
from JObject import JObject

class Storage:
    def __init__(self, master=None):
        self.config_path = abspath(getsourcefile(lambda:0)).strip('Storage.py')
        self.ini = {'SAVE LOCATION': None, 'BACKUP LOCATION': None, 'LAST BACKUP': None, 'BACKUP INTERVAL': 168, 'AUTOSAVE': False}
        self.journal = None
        self.master = master
        self.auto_save = BooleanVar(master=self.master, name='Autosave', value=self.ini['AUTOSAVE'])
        self.backup_interval = IntVar(master=self.master, name='Backup Interval', value=self.ini['BACKUP INTERVAL'])
        self.last_backup = StringVar(master=self.master, name='Last Backup', value=self.ini['LAST BACKUP'])
        
    def LoadIniFile(self):
        try:
            fin = open(self.config_path + "Journal.ini", "rb")
            self.ini = pickle.load(fin)
        except FileNotFoundError:
            self.changeSaveDirectory()
            fin = open(self.config_path + "Journal.ini", "wb")
            pickle.dump(self.ini, fin)
        fin.close()
        self.auto_save.set(self.ini['AUTOSAVE'])
        self.backup_interval.set(self.ini['BACKUP INTERVAL'])
        if not self.ini['LAST BACKUP']:
            self.last_backup.set('Never')
        else:
            self.last_backup.set(DateTools.getDateGUIFormat(self.ini['LAST BACKUP']))
        
    def openJournalFile(self):
        try:
            fin = open(self.ini['SAVE LOCATION'] + "journal_db", "rb")
            self.journal = pickle.load(fin)
        except FileNotFoundError:
            fin = open(self.ini['SAVE LOCATION'] + "journal_db", "wb")
            self.journal = JObject()
        fin.close()
        
    def changeSaveDirectory(self):
        self.dir_opt = options = {}
        if not self.ini['SAVE LOCATION']:
            options['initialdir'] = self.config_path
        else:
            options['initialdir'] = self.ini['SAVE LOCATION']
        options['mustexist'] = False
        options['parent'] = self.master
        options['title'] = 'Choose a Save Location'
        location = filedialog.askdirectory(**self.dir_opt)
        if location != '':
            self.ini['SAVE LOCATION'] = location + "/"
        
    def changeBackupDirectory(self):
        self.backup_opt = options = {}
        if not self.ini['BACKUP LOCATION']:
            options['initialdir'] = self.config_path
        else:
            options['initialdir'] = self.ini['BACKUP LOCATION']
        options['mustexist'] = False
        options['parent'] = self.master
        options['title'] = 'Choose a Location for the Backup Folder'
        location = filedialog.askdirectory(**self.backup_opt)
        if location != '':
            self.ini['BACKUP LOCATION'] = location + "/Backup/"
            if not os.path.exists(self.ini['BACKUP LOCATION']):
                os.makedirs(self.ini['BACKUP LOCATION'])
            
    def changeBackupSchedule(self):
        self.ini['BACKUP INTERVAL'] = self.backup_interval.get()            
        
    def toggleAutoSave(self):
        if self.auto_save.get() == True:
            self.auto_save.set(False)
        else:
            self.auto_save.set(True)
        self.ini['AUTOSAVE'] = self.auto_save.get()
        
#    def checkBackup(self):
#        today = DateTools.getCurrentDate()
#        if self.ini['LAST BACKUP']:
#            if (today-self.ini['LAST BACKUP']).total_seconds() > self.ini['BACKUP INTERVAL']*3600:
#                self.backupDatabase()
#        else:
#            self.backupDatabase()
            
    def backupDatabase(self):
        """Backs up the database held by the storage object(not the one
        passed to the journal object) and updates associated variables"""
        
        if self.ini['BACKUP LOCATION']:
            fout = open(self.ini['BACKUP LOCATION'] + "journal_db", "wb")
        else:
            self.changeBackupDirectory()
            fout = open(self.ini['BACKUP LOCATION'] + "journal_db", "wb")
        pickle.dump(self.journal, fout)
        fout.close()
        date = DateTools.getCurrentDate()
        self.ini['LAST BACKUP'] = date
        self.last_backup.set(DateTools.getDateGUIFormat(date))
            
    def getSaveDirectory(self):
        return self.ini['SAVE LOCATION']
        
    def getBackupDirectory(self):
        return self.ini['BACKUP LOCATION']
        
    def getAutosaveVar(self):
        return self.auto_save
        
    def getBackupIntervalVar(self):
        return self.backup_interval
        
    def getLastBackupVar(self):
        return self.last_backup
        
    def getJournal(self):
        return self.journal.__deepcopy__()
        
    def journalIsSaved(self, journal):
        if self.journal.equals(journal):
            return True
        else:
            return False
        
    def runBackup(self):
        if self.ini['BACKUP INTERVAL'] != -1:
            if not self.ini['BACKUP LOCATION']:
                self.changeBackupDirectory()
            today = DateTools.getCurrentDate()
            if self.ini['LAST BACKUP']:
                if (today-self.ini['LAST BACKUP']).total_seconds() > self.ini['BACKUP INTERVAL']*3600:
                    self.backupDatabase()
            else:
                self.backupDatabase()
    
    def saveIniFile(self):
        fout = open(self.config_path + 'Journal.ini', 'wb')
        pickle.dump(self.ini, fout)
        fout.close()
        
    def saveJournal(self, journal):
        """Saves the journal of the storage object (not the journal of t
        the journal object)"""
        
        fout = open(self.ini['SAVE LOCATION'] + "journal_db", "wb")
        pickle.dump(journal, fout)
        fout.close()
        
    def closeStreams(self):
        None