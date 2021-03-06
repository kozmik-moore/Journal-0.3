# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 17:05:45 2017

@author: Kozmik
"""

from TagsManager import TagsManager
from tkinter import *
from tkinter.ttk import *
import JObject
from math import ceil
import copy

class DateFilter(TagsManager):
    def __init__(self, jobject):
#        self.master = master
        self.jobject = jobject
        if not self.jobject:
            self.jobject = JObject
        self.dateslist = list(self.jobject.getAllDates())
        self.dialog = None
        self.filter_type = StringVar(name='SearchType', value='OR')
        TagsManager.__init__(self, self.jobject)
        
    def createFilterDialog(self):
        self.dialog = Toplevel()
        self.dialog.title("Filters")
        top = Frame(self.dialog)
        middle = Frame(self.dialog)
        bottom = Frame(self.dialog)
        
        canvas = Canvas(self.dialog, highlightthickness=0)
        tagslist = self.getVarsDict()
        if tagslist:
            for tag in tagslist:
                tagslist[tag][1] = Checkbutton(master=canvas, text=tag, variable=tagslist[tag][0])
            tmp = sorted(tagslist.keys())
            row = 10
            col = ceil(len(tagslist) / row)
            grid = [(x, y) for x in range(0, col) for y in range(0, row) ]
            for i in range(0, len(tmp)):
                x, y = grid[i]
                tagslist[tmp[i]][1].grid(row=y, column=x, sticky=W)
        else:
            message = Message(canvas, text='There is nothing to display.')
            message.grid()
        
        ORPTYPE = Radiobutton(top, text="OR(P)", value="OR(P)", variable=self.filter_type)
        ORPTYPE.grid(row=0, column=1, sticky=W)
        ORTYPE = Radiobutton(top, text="OR", value="OR", variable=self.filter_type)
        ORTYPE.grid(row=0, column=0, sticky=W)
        ANDTYPE = Radiobutton(top, text="AND", value="AND", variable=self.filter_type)
        ANDTYPE.grid(row=0, column=2, sticky=W)
        
        canvas.pack()
        ALL = Button(bottom, text="All", command=self.selectAllBoxes)
        NONE = Button(bottom, text="None", command=self.deselectAllBoxes)
        INVERT = Button(bottom, text="Invert", command=self.invertAllBoxes)
        ALL.pack(side=LEFT)
        NONE.pack(side=LEFT)
        INVERT.pack(side=LEFT)
        top.pack(side=TOP)
        middle.pack(side=TOP)
        bottom.pack(side=TOP)
        self.dialog.grab_set()
        self.dialog.protocol("WM_DELETE_WINDOW", self.destroyDialog)
        
    def destroyDialog(self):
        self.dialog.destroy()
        self.dialog = None
        self.filterDates()
        
    def filterDates(self):
        filtered_tags = []
        states_list = self.getStates()
        self.dateslist = list(self.jobject.getAllDates())
        if self.filter_type.get() == 'OR(P)':
            for tag in states_list:
                if not states_list[tag]:
                    filtered_tags.append(tag)
            filter_flag = False
            for date in sorted(self.dateslist):
                for tag in self.jobject.getEntry(date).getTags():
                    if tag in filtered_tags:
                        filter_flag = True
                    if not filter_flag:
                        self.dateslist.remove(date)
        elif self.filter_type.get() == 'OR':
            for tag in states_list:
                if states_list[tag]:
                    filtered_tags.append(tag)
            tmp_list = []
            for date in sorted(self.dateslist):
                for tag in self.journal.getEntry(date).getTags():
                    if tag in filtered_tags:
                        if date not in tmp_list:
                            tmp_list.append(date)
            self.dateslist = tmp_list
        elif self.filter_type.get() == 'AND':
            for tag in states_list:
                if states_list[tag]:
                    filtered_tags.append(tag)
            for date in sorted(self.dateslist):
                if len(self.journal.getEntry(date).getTags()) != len(filtered_tags):
                    self.dateslist.remove(date)
                else:
                    for tag in self.journal.getEntry(date).getTags():
                        if tag not in filtered_tags:
                            if date in self.dateslist:
                                self.dateslist.remove(date)        
        
    def getDatesList(self):
        self.updateVarsDict()
        self.filterDates()
        return copy.copy(self.dateslist)
        
    def getTagsList(self):
        return self.tagslist
        
    def selectAllBoxes(self):
        for tag in self.vars:
            self.vars[tag][0].set(True)
        
    def deselectAllBoxes(self):
        for tag in self.vars:
            self.vars[tag][0].set(False)
        
    def invertAllBoxes(self):
        for tag in self.vars:
            if self.vars[tag][0].get():
                self.vars[tag][0].set(False)
            else:
                self.vars[tag][0].set(True)