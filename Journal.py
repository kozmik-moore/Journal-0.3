# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:00:50 2016

@author: Kozmik
"""
from tkinter import *
from tkinter.ttk import *
import pickle
import tkinter.messagebox as messagebox
from inspect import getsourcefile
from os.path import abspath
from tkinter import filedialog as filedialog
import os
import pdb
from JObject import *
from BodyFrame import *
from DateFrame import *
from TagsFrame import *
                
class Main(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w*.9, h*.8))
        self.title('Journal')
        self.storage = Storage()
        self.storage.LoadIniFile()
        self.storage.openJournalFile()
        self.journal = self.storage.getJournal()
        self.entry = None
        if self.journal.isEmpty():
            date = 19000101000000
            body = ("Welcome!\n\nThis entry is an introduction and a bugfix " 
"(working on it!). I know what the date says, but it's not really that " 
"year and the program is not (terribly) broken. A few things to know:\n\n"
"-The main box here is for the body of your thoughts.\n\n-The field " 
"labeled \"Tags\" is for assigning a tag to your body of thoughts. " 
"You can assign multiple tags; just make sure to separate them with " 
"commas.\n\n-The \"Parent Entry\" field is for future implementation"
", a system to link thoughts together. For now, it just holds a date, if "
"applicable.\n\n-The \"Create Linked Entry\""
" button is used to create a thought branching off of the one currently on the "
"screen (something for the \"Display Linked Entries\" button to do, eventually)."
"\n\n-This thing likes to save like crazy, sometimes unnecessarily."
" It shouldn't present too many problems, but you might end up with copies "
"of entries floating around; you can safely delete those using the \"Delete\""
" button.\n\n-Development is ongoing. Have a suggestion? Send me a message."
"\n\nFeel free to do whatever you want with this entry: use it "
"for notes or reference, delete it, write mocking jibes about the project developer in "
"the safety and comfort of your own home, impress your friends by writing mocking"
" jibes about the project developer, the possiblities are endless!\n\n\nGood writing!")
            tags = ['Welcome']
            self.entry = JEntry(date, body, tags)
            self.journal.add(self.entry)
        self.entry = JEntry()
        self.buffer_entry = None
        self.backup_interval = self.storage.getBackupIntervalVar()
        self.journal_auto_save = self.storage.getAutosaveVar()
        
        self.top_frame = Frame(self)
        self.date_frame = DateFrame(self, self.entry, self.journal)
        self.body_frame = BodyFrame(self, self.entry)
        self.tags_frame = TagsFrame(self, self.entry, self.journal)
        self.options_frame = Frame(self)
        
        self.date_frame.pack(side=TOP, expand=True, fill=X)
        self.body_frame.pack(side=TOP, expand=True, fill=BOTH)
        self.tags_frame.pack(side=TOP, expand=True, fill=X)
        
        self.SAVE = Button(self.options_frame, text="Save", command=self.save).grid(row=0, column=0, columnspan=2)
        self.LINK = Button(self.options_frame, text="Create Linked Entry", command=self.newLink).grid(row=0, column=2, columnspan=2, sticky=EW)
        self.NEW = Button(self.options_frame, text="New Entry", command=self.newEntry).grid(row=0, column=4, columnspan=2)
        self.QUIT = Button(self.options_frame, text="Quit", command=self.destroyApp).grid(row=1, column=0, columnspan=2)
        self.LINKS = Button(self.options_frame, text="Display Linked Entries", command=self.displayLinks).grid(row=1, column=2, columnspan=2)
        self.DELETE = Button(self.options_frame, text="Delete", command=self.delete).grid(row=1, column=4)
        
        self.options_frame.pack(side=TOP)
        
        menubar = Menu(self)
        pref_menu = Menu(menubar, tearoff=0)
        pref_menu.add_command(label='Autosave changes on exit', command=self.changeAutoSavePref)
        pref_menu.add_command(label="Select Save Directory", command=self.storage.changeSaveDirectory)
        backup_menu = Menu(pref_menu, tearoff=0)
        backup_menu.add_command(label='Select Backup Directory', command=self.storage.changeBackupDirectory)
#        self.interval_menu = Menu(backup_menu, tearoff=0)
        self.interval_menu = OptionMenu(self, self.backup_interval, self.storage.getBackupIntervalOptions())
#        self.interval_menu.add_command(label='Immediately', command=self.storage.backupDatabase)
#        self.refreshIntervalMenu()
#        interval_menu.add_command(label='Day', command=lambda:self.storage.changeBackupSchedule(24))
#        interval_menu.add_command(label='3 Days', command=lambda:self.storage.changeBackupSchedule(72))
#        interval_menu.add_command(label='Week', command=lambda:self.storage.changeBackupSchedule(168))
#        interval_menu.add_command(label='Never', command=lambda:self.storage.changeBackupSchedule(-1))
        backup_menu.add_cascade(label='Backup Database Every: ', menu=self.interval_menu)
        pref_menu.add_cascade(label='Backup Options', menu=backup_menu)
        
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.createAboutWindow)
        
        menubar.add_cascade(label="Preferences", menu=pref_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)
        
        self.protocol("WM_DELETE_WINDOW", self.destroyApp)
        self.bindDateControl()
        self.storage.runBackup()
                
    def createAboutWindow(self):
        message = "Journal 0.3\nAuthor: kozmik-moore @ GitHub\nDeveloped using the Anaconda 3 Python Suite"
        main = messagebox.Message(title="About", message=message)
        main.show()
        
    def destroyApp(self):
        if self.entry.getDate():
            if self.isEntryChanged():
                self.throwSaveWarning()
        elif not self.body_frame.isBodyFieldEmpty():
            self.throwSaveWarning()
        if self.isJournalChanged():
            if not self.journal_auto_save.get():
                self.throwFinalSaveWarning()
            else:
                self.storage.saveJournal(self.journal)
        self.storage.saveIniFile()
        self.destroy()
        
    def refreshIntervalMenu(self):
        self.interval_menu['menu'].delete(1, END)
        interval_list = self.storage.getBackupIntervalOptions()
        style = Style()
        style.configure('Bold.TMenuButton', font=('Sans', '10', 'bold'))
        for item in interval_list:
            if item[1] == self.backup_interval.get():
                self.interval_menu.add_command(label=item[0], command=lambda interval=item(1):self.storage.changeBackupSchedule(interval), style='Bold.TMenuButton')
            else:
                self.interval_menu.add_command(label=item[0], command=lambda interval=item(1):self.storage.changeBackupSchedule(interval))

    def changeAutoSavePref(self):
        self.storage.toggleAutoSave()
        if self.journal_auto_save.get():
            message = 'Journal autosave is ON.'
        else:
            message = 'Journal autosave is OFF'
        messagebox.showinfo(title='Autosave', message=message)
        
    def updateGUI(self, event):
        if self.isEntryChanged():
            self.throwSaveWarning()
        elif not self.body_frame.isBodyFieldEmpty():
            self.throwSaveWarning()
#        pdb.set_trace()
        date = self.date_frame.ConvertFromUserFormat(self.date_frame.getDate())
        self.clearGUI()
        if date:
            self.entry = self.journal.getEntry(date)
        else:
            self.entry = JEntry()
#        self.buffer_entry = entry.getCopy()
        self.date_frame.updateGUI(self.entry)
        self.body_frame.updateGUI(self.entry)
        self.tags_frame.updateGUI(self.entry)
        
    def clearGUI(self):
        self.date_frame.clearGUI()
        self.body_frame.clearGUI()
        self.tags_frame.clearGUI()
        self.entry = JEntry()
        self.date_frame.updateGUI(self.entry)
        self.body_frame.updateGUI(self.entry)
        self.tags_frame.updateGUI(self.entry)
        
    def bindDateControl(self):
        self.date_frame.bindDatebox(self.updateGUI)
        
    def isJournalChanged(self):
        if self.storage.isJournalSaved(self.journal):
            return False
        else:
            return True
            
    def isEntryChanged(self):
        date = self.entry.getDate()
        if date in self.journal.getAllDates():
            if date in self.storage.getJournal().getAllDates():
                if self.entry.equals(self.storage.getJournal().getEntry(date)):
                    return False
                else:
                    return True
                
    def throwSaveWarning(self):
        selection = messagebox.askyesno("Save Entry", "Save before continuing?")
        if selection:
            self.save()
            
    def throwFinalSaveWarning(self):
        selection = messagebox.askyesno("Save All Changes", "Save all changes before exiting?")
        if selection:
            self.storage.saveJournal(self.journal)
            
    def save(self):
        self.date_frame.save()
        self.body_frame.save()
        self.tags_frame.save()
        if self.entry.getParent():
           self.journal.getEntry(self.entry.getParent()).setChild(self.entry.getDate()) 
        
    def delete(self):
        if self.entry.getDate():
            selection = messagebox.askyesno("Delete Entry", "Delete this entry?")
            if selection:
                self.journal.delete(self.entry.getDate())
                self.entry = JEntry()
                self.clearGUI()
        elif not self.body_frame.isBodyFieldEmpty():
            self.throwSaveWarning()
            self.entry = JEntry()
            self.clearGUI()
            
    def newEntry(self):
        if self.entry.getDate():
            if self.isEntryChanged():
                self.throwSaveWarning()
            self.entry = JEntry()
            self.clearGUI()
        elif not self.body_frame.isBodyFieldEmpty():
            self.throwSaveWarning()
            self.entry = JEntry()
            self.clearGUI()
        
    def newLink(self):
        if self.entry.getDate():
            if self.isEntryChanged():
                self.throwSaveWarning()
            self.entry = JEntry(parent=self.entry.getDate())
            self.clearGUI()
        elif not self.body_frame.isBodyFieldEmpty():
            self.throwSaveWarning()
            self.entry = JEntry(parent=self.entry.getDate())
            self.clearGUI()
        
    def displayLinks(self):
        None
             
class Storage:
    def __init__(self, master=None):
        self.config_path = abspath(getsourcefile(lambda:0)).strip('Journal.py')
        self.ini = {'SAVE LOCATION': None, 'BACKUP LOCATION': None, 'LAST BACKUP': None, 'BACKUP INTERVAL': 'Never', 'AUTOSAVE': False}
        self.journal = None
        self.master = master
        self.auto_save = None
        self.interval_options = ['Day', '3 Days', 'Week', 'Never']
        self.interval_dict = {'Day': 24, '3 Days': 72, 'Week': 168}
#        for item in self.interval_options:
#            item[2] = BooleanVar(self, name=item[1], value=False)
#            if item[1] == self.ini['BACKUP INTERVAL']:
#                item[2].set(True)
        self.backup_interval = None
        
    def LoadIniFile(self):
        try:
            fin = open(self.config_path + "Journal.ini", "rb")
            self.ini = pickle.load(fin)
        except FileNotFoundError:
            self.changeSaveDirectory()
            fin = open(self.config_path + "Journal.ini", "wb")
            pickle.dump(self.ini, fin)
        fin.close()
        self.auto_save = BooleanVar(master=self.master, name='Autosave', value=self.ini['AUTOSAVE'])
        self.backup_interval = StringVar(master=self.master, name='Backup Interval', value=self.ini['BACKUP INTERVAL'])
        
    def openJournalFile(self):
        try:
            fin = open(self.ini['SAVE LOCATION'] + "journal_db", "rb")
            self.journal = pickle.load(fin)
        except FileNotFoundError:
            fin = open(self.ini['SAVE LOCATION'] + "journal_db", "wb")
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
#        pdb.set_trace()
        self.ini['AUTOSAVE'] = self.auto_save.get()
        
    def checkBackup(self):
        if self.backup_interval.get() != 'Never':
            today = datetime.today()
            if self.ini['LAST BACKUP']:
                if (today-self.ini['LAST BACKUP']).total_seconds() > self.interval_dict[self.ini['BACKUP INTERVAL']]*3600:
                    self.backupDatabase()
        else:
            self.backupDatabase()
            
    def backupDatabase(self):
        if self.ini['BACKUP LOCATION']:
            fout = open(self.ini['BACKUP LOCATION'] + "journal_db", "wb")
        else:
            self.changeBackupDirectory()
            fout = open(self.ini['BACKUP LOCATION'] + "journal_db", "wb")
        pickle.dump(self.journal, fout)
        fout.close()
        self.ini['LAST BACKUP'] = datetime.today()
            
    def getSaveDirectory(self):
        return self.ini['SAVE LOCATION']
        
    def getBackupDirectory(self):
        return self.ini['BACKUP LOCATION']
        
    def getAutosaveVar(self):
        return self.auto_save
        
    def getBackupIntervalVar(self):
        return self.backup_interval
        
    def getBackupIntervalOptions(self):
        return self.interval_options
        
    def getJournal(self):
        return self.journal.getCopy()
        
    def isJournalSaved(self, journal):
        if self.journal.equals(journal):
            return True
        else:
            return False
        
    def runBackup(self):
        if self.ini['BACKUP INTERVAL'] != 'Never':
            if self.ini['BACKUP LOCATION']:
                self.checkBackup()
            else:
                self.changeBackupDirectory()
                self.checkBackup()
    
    def saveIniFile(self):
        fout = open(self.config_path + 'Journal.ini', 'wb')
        pickle.dump(self.ini, fout)
        fout.close()
        
    def saveJournal(self, journal):
        fout = open(self.ini['SAVE LOCATION'] + "journal_db", "wb")
        pickle.dump(journal, fout)
#        pdb.set_trace()
        fout.close()