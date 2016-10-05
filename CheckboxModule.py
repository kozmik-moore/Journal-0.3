# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 12:38:07 2016

@author: Kozmik
"""
#from tkinter import Checkbutton
from tkinter import *
from tkinter.ttk import *
from math import ceil
import pdb


class CheckboxModule:
    def __init__(self, master=None, name=None, labels=None, exceptions=None, default=False, **kwargs):
        self.master = master
        self.canvas = None
        self.checkboxlist = {}
        self.labels = []
        self.exceptions = []
        self.value = default
        self.name = ''
        if name:
            self.name = name
#            pdb.set_trace()
        if labels:
            self.update()            
        
    def update(self, labels=None, exceptions=None, value=None):
        if value:
            self.value = value
        self.labels = labels
        self.exceptions = exceptions
        for label in self.labels:
            self.add(label)
        for label in list(self.checkboxlist):
            if label not in self.labels:
                self.delete(label)
#        self.createCanvas()
                
    def add(self, label):
        if label not in self.labels:
            self.labels.append(label)
        if label not in self.checkboxlist:
            if label in self.exceptions:
                var = BooleanVar(self.canvas, value=(not self.value), name=self.name+label)
            else:
                var = BooleanVar(self.canvas, value=self.value, name=self.name+label)
            self.checkboxlist[label] = [var, None]
        else:
            if label in self.exceptions:
                self.checkboxlist[label][0].set(not self.value)
            else:
                self.checkboxlist[label][0].set(self.value)
            
    def delete(self, label):
        if label in self.labels:
            self.labels.remove(label)
        if label in self.checkboxlist:
            del self.checkboxlist[label]
        if label in self.exceptions:
            self.exceptions.remove(label)
            
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
        for label in self.checkboxlist:
            self.checkboxlist[label][1] = Checkbutton(master=self.canvas, text=label, variable=self.checkboxlist[label][0])
        tmp = sorted(self.labels)
        row = 6
        col = ceil(len(tmp) / row)
        grid = [(x, y) for x in range(0, col) for y in range(0, row) ]
        for i in range(0, len(tmp)):
            x, y = grid[i]
            self.checkboxlist[tmp[i]][1].grid(row=y, column=x, sticky=W)
            
    def clearGrid(self):
        for label in self.checkboxlist:
            self.checkboxlist[label][1] = None
        self.canvas = None
            
    def getStates(self):
        states = {}
        for label in self.checkboxlist:
            states[label] = self.checkboxlist[label][0].get()
        return states
        
    def getCheckboxCanvas(self, master):
        if self.labels:
            self.canvas = Canvas(master, highlightthickness=0)
            self.createGrid()
        else:
            message = Message(self, text='There is nothing to display.', width=200)
            message.pack(expand=True, fill=X)
        return self.canvas
        
    def anyBoxesChecked(self):
        for label in self.checkboxlist:
            if self.checkboxlist[label][0].get():
                return True
        return False
        
    def boxChecked(self, label):
        if self.checkboxlist[label][0].get():
            return True
        else:
            return False
        