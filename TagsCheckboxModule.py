# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 08:39:07 2016

@author: Kozmik
"""
from tkinter import *
from math import ceil

class TagsCheckboxModule:
    def __init__(self, entry, journal, value=False):
        self.journal = journal
        self.entry = entry
        self.value = value
        self.tags = self.journal.getAllTags()
        self.exceptions = self.entry.getTags()
        self.checkboxlist = {}            
        self.canvas = None
        self.updateModule(self.entry)
            
    def updateModule(self, entry):
        self.entry = entry
        self.tags = self.journal.getAllTags()
        self.exceptions = self.entry.getTags()
        for tag in self.tags:
            self.addTag(tag)
        for tag in list(self.checkboxlist):
            if tag not in self.tags:
                self.deleteTag(tag)
                
    def addTag(self, tag):
        self.entry.addTag(tag)
        if tag not in self.tags:
            self.tags.append(tag)
        if tag not in self.checkboxlist:
            if tag in self.exceptions:
                var = BooleanVar(self.canvas, value=(not self.value), name='TF'+tag)
            else:
                var = BooleanVar(self.canvas, value=self.value, name='TF'+tag)
            self.checkboxlist[tag] = [var, None]
        else:
            if tag in self.exceptions:
                self.checkboxlist[tag][0].set(not self.value)
            else:
                self.checkboxlist[tag][0].set(self.value)
            
    def deleteTag(self, tag):
        self.entry.removeTag(tag)
        if tag in self.tags:
            self.tags.remove(tag)
        if tag in self.checkboxlist:
            del self.checkboxlist[tag]
        if tag in self.exceptions:
            self.exceptions.remove(tag)
            
    def selectAllBoxes(self):
        for index in self.checkboxlist:
            self.checkboxlist[index][0].set(True)
            
    def deselectAllBoxes(self):
        for index in self.checkboxlist:
            self.checkboxlist[index][0].set(False)
            
    def invertAllBoxes(self):
        for index in self.checkboxlist:
            if self.checkboxlist[index][0].get() == True:
                self.checkboxlist[index][0].set(False)
            else:
                self.checkboxlist[index][0].set(True)
            
    def createGrid(self):
        for tag in self.checkboxlist:
            self.checkboxlist[tag][1] = Checkbutton(master=self.canvas, text=tag, variable=self.checkboxlist[tag][0])
        tmp = sorted(self.tags)
        row = 6
        col = ceil(len(tmp) / row)
        grid = [(x, y) for x in range(0, col) for y in range(0, row) ]
        for i in range(0, len(tmp)):
            x, y = grid[i]
            self.checkboxlist[tmp[i]][1].grid(row=y, column=x, sticky=W)
            
    def clearGrid(self):
        for tag in self.checkboxlist:
            self.checkboxlist[tag][1] = None
        self.canvas = None
            
    def getStates(self):
        states = {}
        for tag in self.checkboxlist:
            states[tag] = self.checkboxlist[tag][0].get()
        return states
        
    def getCheckboxCanvas(self, master):
        self.canvas = Canvas(master, highlightthickness=0)
        if self.tags:
            self.createGrid()
        else:
            message = Message(self.canvas, text='There is nothing to display.', width=200)
            message.pack(expand=True, fill=X)
        return self.canvas
        
    def anyBoxesChecked(self):
        for tag in self.checkboxlist:
            if self.checkboxlist[tag][0].get():
                return True
        return False
        
    def boxChecked(self, tag):
        if self.checkboxlist[tag][0].get():
            return True
        else:
            return False