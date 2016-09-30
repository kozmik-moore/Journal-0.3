# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:47:15 2016

@author: Kozmik
"""
from tkinter import *
from tkinter.ttk import *
from JObject import *
from datetime import datetime
from TagsFrame import TagsCheckboxDialog

class DateFrame(Frame):
    def __init__(self, master=None, entry=None, journal=None):
        root = None
        self.master = master
        if not self.master:
            root = Tk()
            Frame.__init__(self, root)
        else:
            Frame.__init__(self, self.master)
        self.entry = entry
        if not self.entry:
            self.entry = JEntry()
        self.journal = journal
        self.filter = DateFilter(journal=self.journal)
        
        self.user_date = ''
        self.program_date = 0
        
        self.MONTHS_NUM_TO_ABR = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", 
        "05":"May", "06":"Jun", "07":"Jul", "08":"Aug", 
        "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}
        
        self.MONTHS_ABR_TO_NUM = {'Dec': '12', 'Oct': '10', 'Feb': '02', 'Nov': '11', 
        'Apr': '04', 'Jun': '06', 'Sep': '09', 'Jul': '07', 
        'Jan': '01', 'May': '05', 'Aug': '08', 'Mar': '03'}
        
        self.dates_registry = {}
        self.updateDateRegistry()
        
        inner_frame = Frame(self)
        self.date_box = Combobox(inner_frame, postcommand=self.updateDateboxList)
        self.updateDateboxList()
        FILTER = Button(inner_frame, text="Filter", command=self.getFilters)

        self.style = Style()
        self.style.configure('NetInd.TLabel', foreground='gray')
        self.is_linked = StringVar(self, value='Not Linked')
        self.HASLINKS = Label(inner_frame, width=12, anchor=CENTER, textvariable=self.is_linked, style='NetInd.TLabel')
        self.setNetworkedIndicator()
        
        self.HASLINKS.pack(side=LEFT)
        self.date_box.pack(side=LEFT)
        FILTER.pack(side=LEFT)
        inner_frame.pack()
        
    def updateGUI(self, entry):
        self.clearGUI()
        self.entry = entry
        if self.entry.getDate():
            self.program_date = self.entry.getDate()
            self.user_date = self.ConvertToUserFormat(self.program_date)
            self.date_box.set(self.user_date)
        self.setNetworkedIndicator()
        self.filter.update(entry)
        
    def clearGUI(self):
        self.date_box.set('')
        self.program_date = 0
        self.user_date = ''
        self.setNetworkedIndicator()
        
    def save(self):
        self.entry.setDate(self.getCurrentDate())
#        self.updateGUI(self.entry)
        
    def bindDatebox(self, function):
        self.date_box.bind("<<ComboboxSelected>>", function)
    def updateDateRegistry(self):
        self.dates_registry = {}
        for item in self.journal.getAllDates():
            self.dates_registry[item] = self.ConvertToUserFormat(item)        
    def getDateUserFormat(self):
        return self.user_date
    def getDateProgramFormat(self):
        return self.program_date
    def getCurrentDate(self): #Program format
        date=datetime.today()
        return int(datetime.strftime(date, '%Y%m%d%H%M%S'))
    def getDate(self):
        return self.date_box.get()
    def ConvertToUserFormat(self, date):
        stringdate = str(date)
        if stringdate != '':
            datestr = ''
            datestr = stringdate[6:8] + ' ' + self.MONTHS_NUM_TO_ABR[stringdate[4:6]] + ' ' + stringdate[:4] + ', ' + stringdate[8:]
            return datestr
    def ConvertFromUserFormat(self, string):
        day = string[:2]
        month = self.MONTHS_ABR_TO_NUM[string[3:6]]
        year = string[7:11]
        time = string[13:]
        return int(year+month+day+time)
    def updateDateboxList(self):
#        self.clear()
        combo_list = self.filter.implementFilters()
        if not combo_list and self.filter.tagsSelected():
            combo_list = self.journal.getAllDates()
        for i in range(0, len(combo_list)):
            date = combo_list.pop(0)
            combo_list.append(self.ConvertToUserFormat(date))
        self.date_box['values'] = combo_list
    def getUserDates(self):
        dates_list = []
        for date in sorted(self.dates_registry.keys()):
            dates_list.append(self.dates_registry[date])
        return dates_list
    def getProgramDates(self):
        return sorted(self.dates_registry.keys())
    def getFilters(self):
        self.master.clearGUI()
        self.filter.createFilterDialog()
        
    def setNetworkedIndicator(self):
        if self.entry.getParent() or self.entry.getChild():
            self.is_linked.set('Linked')
            self.style.configure('NetInd.TLabel', foreground='blue')
        else:
            self.is_linked.set('Not Linked')
            self.style.configure('NetInd.TLabel', foreground='gray')
        
class DateFilter:
    def __init__(self, entry=None, journal=None):
#        self.entry = entry
#        if not self.entry:
#            self.entry = JEntry()
        self.journal = journal
        self.dates_list = self.journal.getAllDates()
        self.filter_type = StringVar(name="Search Type", value="OR")
        self.tagslist = []
        if self.journal:
            self.tagslist + self.journal.getAllTags()
#        self.tagslist += self.entry.getTags()
        self.check_box_dialog = TagsCheckboxDialog(None, self.journal, None, True)
        self.check_box_dialog.update(value=True)        
        self.dialog = None
        
    def update(self, entry):
        self.dates_list = self.journal.getAllDates()
#        self.entry = entry

    def createFilterDialog(self):
        self.dialog = Toplevel()
        top = Frame(self.dialog)
        middle = Frame(self.dialog)
        bottom = Frame(self.dialog)
        
        cb_canvas = self.check_box_dialog.getCheckboxCanvas(middle)
        self.dialog.title("Filters")
        
        ORPTYPE = Radiobutton(top, text="OR(P)", value="OR(P)", variable=self.filter_type)
        ORPTYPE.grid(row=0, column=1, sticky=W)
        ORTYPE = Radiobutton(top, text="OR", value="OR", variable=self.filter_type)
        ORTYPE.grid(row=0, column=0, sticky=W)
        ANDTYPE = Radiobutton(top, text="AND", value="AND", variable=self.filter_type)
        ANDTYPE.grid(row=0, column=2, sticky=W)
        
        cb_canvas.grid(row=1, column=0, rowspan=10, columnspan=2)
        ALL = Button(bottom, text="All", command=self.check_box_dialog.selectAllBoxes)
        NONE = Button(bottom, text="None", command=self.check_box_dialog.deselectAllBoxes)
        INVERT = Button(bottom, text="Invert", command=self.check_box_dialog.invertAllBoxes)
        ALL.grid(row=2, column=0)
        NONE.grid(row=2, column=1)
        INVERT.grid(row=2, column=2)
        top.pack(side=TOP)
        middle.pack(side=TOP)
        bottom.pack(side=TOP)
        self.dialog.grab_set()
#        self.clear()
        self.dialog.protocol("WM_DELETE_WINDOW", self.destroyDialog)
        
    def destroyDialog(self):
        self.dialog.destroy()
        self.dialog = None
        
    def implementFilters(self):
        combobox_list = []
        filtered_tags = []
#        pdb.set_trace()
        states_list = self.check_box_dialog.state()
        if self.filter_type.get() == 'OR(P)':
            combobox_list = self.journal.getAllDates()
            for tag in states_list:
                if not states_list[tag]:
                    filtered_tags.append(tag)
            for date in sorted(self.dates_list):
                for tag in self.journal.getEntry(date).getTags():
                    if tag in filtered_tags:
                        if date in combobox_list:
                            combobox_list.remove(date)
        elif self.filter_type.get() == 'OR':
            for tag in states_list:
                if states_list[tag]:
                    filtered_tags.append(tag)        
            for date in sorted(self.dates_list):
                for tag in self.journal.getEntry(date).getTags():
                    if tag in filtered_tags:
                        if date not in combobox_list:
                            combobox_list.append(date)
        elif self.filter_type.get() == 'AND':
            combobox_list = self.dates_list
            for tag in states_list:
                if states_list[tag]:
                    filtered_tags.append(tag)
            for date in sorted(self.dates_list):
                if len(self.journal.getEntry(date).getTags()) != len(filtered_tags):
                    combobox_list.remove(date)
                else:
                    for tag in self.journal.getEntry(date).getTags():
                        if tag not in filtered_tags:
                            if date in combobox_list:
                                combobox_list.remove(date)
        return sorted(combobox_list)
        
    def tagsSelected(self):
        if self.check_box_dialog.noTagsSelected():
            return False
        else:
            return True