# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 09:03:58 2016

@author: Kozmik
"""

from TagsCheckboxModule import TagsCheckboxModule
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from math import ceil
import pdb

class TagsCanvas(Canvas, TagsCheckboxModule):
    def __init__(self, master=None, entry=None, journal=None, **kwargs):
        h = 1
        w = 0
        self.tagslist = {}
        self.dialog = None
        Canvas.__init__(self, master=master, height=h, width=w, highlightthickness=0)
        TagsCheckboxModule.__init__(self, entry=entry, journal=journal)
        
    def clear(self):
        for tag in self.tagslist:
            self.tagslist[tag].destroy()
        self.tagslist = {}
        self.deselectAllBoxes()
        
    def updateCanvas(self, entry):
        self.clear()
        self.updateModule(self, entry)
        
    def addTag(self, tag):
        TagsCheckboxModule.addTag(self, tag)
        if tag not in self.tagslist:
            self.tagslist[tag] = TagButton(self, tag, self)
#            self.tagslist[tag].pack(side=LEFT, padx=1)
        self.sortTags()
        
    def deleteTag(self, tag):
        TagsCheckboxModule.deleteTag(self, tag)
        if tag in self.tagslist:
            self.tagslist[tag].destroy()
            del self.tagslist[tag]
        self.sortTags()
            
    def sortTags(self):
        self.delete('all')
        col = 10
        row = ceil(len(self.tagslist) / col)
        grid = []
        grid = [(x,y) for y in range(0, row) for x in range(0, col)]
        index = 0
        for tag in sorted(self.tagslist):
            self.tagslist[tag].makeInvisible()
        for tag in sorted(self.tagslist):
            x, y = grid[index]
            self.tagslist[tag].grid(column=x, row=y, sticky=EW)
            index += 1#.pack(side=LEFT, padx=1)
            
    def getTags(self):
        return sorted(self.tagslist.keys())
        
    def addDialog(self):
        tags = simpledialog.askstring(title='Add Tags', prompt='Enter at least one tag, separating multiple tags with a comma:')
        if tags:
            tags = tags.split(',')
            for tag in tags:
                if tag.strip():
                    self.addTag(tag.strip())
                    
    def selectDialog(self):
        self.dialog = Toplevel()
        self.dialog.title('Select Tags')
        canvas = self.getCheckboxCanvas(self.dialog)
        canvas.pack()
        self.dialog.protocol("WM_DELETE_WINDOW", self.propogateTags)
                
    def propogateTags(self):
        selected_tags = self.getStates()
        for tag in selected_tags:
            if selected_tags[tag]:
                self.addTag(tag)
            elif not selected_tags[tag]:
                self.deleteTag(tag)
        self.sortTags()
        self.dialog.destroy()
        self.dialog = None
        
    def save(self):
        tags = self.entry.getTags()
        while not tags:
            tags = self.entry.getTags()
            self.addDialog()
                
class TagButton(Button):
    def __init__(self, master=None, text=None, controller=None):
        root = None
        self.master = master
        self.controller = controller
        if not self.master:
            root = Tk()
            self.master = TagsCanvas(root)
        Button.__init__(self, master=self.master, text=text, command=self.changeTagDialog)
        self.tag = text
        self.dialog = None
        self.entry_box = None
        if root:
            self.pack(side=LEFT)
            self.master.pack()
            root.mainloop()
        
    def changeTagDialog(self):
        self.dialog = Toplevel()
        self.dialog.grab_set()
        self.dialog.title('Change Tag')
        message = Message(self.dialog, text='Enter a new tag here:', width=150)
        self.entry_box = Entry(self.dialog)
        self.entry_box.insert(0, self.tag)
        button_box = Frame(self.dialog)
        OK = Button(button_box, text='OK', command=self.updateButton)
        OK.bind("<Return>", self.update)
        CANCEL = Button(button_box, text='Cancel', command=self.dialog.destroy)
        DELETE = Button(button_box, text='Delete', command=self.delete)
        message.pack(side=TOP)
        self.entry_box.pack(side=TOP)
        OK.pack(side=LEFT)
        CANCEL.pack(side=LEFT)
        DELETE.pack(side=LEFT)
        button_box.pack(side=TOP)
        
    def updateButton(self):
        self.tag = self.entry_box.get()
        coords = self.grid_info()
        self.dialog.destroy()
        self.dialog = None
        self.config(text=self.tag)
        self.grid(row=coords["row"], column=coords["column"], sticky=EW)
        
    def delete(self):
        delete = messagebox.askyesno(title='Delete?', message='Are you sure you want to delete this tag?')
        self.dialog.destroy()
        self.dialog = None
        if delete:
            self.destroy()
            if type(self.controller) is TagsCanvas:
                self.controller.deleteTag(self.tag)
                
    def makeInvisible(self):
        self.grid_forget()
        
    def __str__(self):
        return self.tag
        
    def getTag(self):
        return self.tag