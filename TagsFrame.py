# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:54:44 2016

@author: Kozmik
"""
from tkinter import *
from tkinter.ttk import *
from JObject import *
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import math

class TagsFrame(Frame):
    def __init__(self, master=None, entry=None, journal=None):
        root = None
        if not master:
            root = Tk()
            Frame.__init__(self, root)
        else:
            Frame.__init__(self, master)
        self.journal = journal
        self.entry = entry
        if not self.entry:
            self.entry = JEntry()
        self.dialog = TagsCheckboxDialog(self.entry, self.journal)
        self.dialog.update()
        self.dialog_window = None
        style = Style(self)
        style.configure("TagsFrame.TButton", side=TOP)
        inner_frame = Frame(self)
        frame1 = Frame(inner_frame)
        frame2 = Frame(inner_frame)
        frame3 = Frame(inner_frame)
        scrollbar = Scrollbar(frame2, orient=HORIZONTAL)
        self.canvas = TagsCanvas(frame2, self.entry, xscrollcommand=scrollbar.set)
#        scrollbar.config(command=self.canvas.xview)
        TAGS = Button(frame1, text='Tags:', command=self.selectDialog, style='TagsFrame.TButton')
        TAGS.pack(anchor=N)
        ADD = Button(frame3, text='Add Tags', command=self.addDialog, style='TagsFrame.TButton')
        self.canvas.pack(side=TOP)
#        scrollbar.pack(side=BOTTOM, expand=True, fill=X)
        ADD.pack(anchor=N, side=RIGHT)
        frame1.pack(side=LEFT, expand=True, fill=X)
        frame2.pack(side=LEFT, expand=True, fill=X)
        frame3.pack(side=LEFT, expand=True, fill=X)
        inner_frame.pack()
        
        for tag in self.entry.getTags():
            self.canvas.addTag(tag)
                  
        if root:
            root.mainloop()
            self.pack(side=TOP)
        
    def updateGUI(self, entry):
        self.entry = entry
        self.canvas.clear()
        if self.entry.getTags():
            for tag in self.entry.getTags():
                self.canvas.addTag(tag)
        self.dialog.update(self.entry)
        
    def clearGUI(self):
        self.canvas.clear()
        
    def addDialog(self):
        tags = simpledialog.askstring(title='Add Tags', prompt='Enter at least one tag, separating multiple tags with a comma:')
        if tags:
            tags = tags.split(',')
            for tag in tags:
                if tag.strip():
                    self.canvas.addTag(tag.strip())
                    
    def selectDialog(self):
        self.dialog_window = Toplevel()
        self.dialog_window.title('Select Tags')
        canvas = self.dialog.getCheckboxCanvas(self.dialog_window)
        canvas.pack()
        self.dialog_window.protocol("WM_DELETE_WINDOW", lambda self=self, dialog=self.dialog: self.propogateTags(self.dialog))
                
    def propogateTags(self, dialog):
        selected_tags = dialog.state()
        for tag in selected_tags:
            if selected_tags[tag]:
                if tag not in self.entry.getTags():
                    self.canvas.addTag(tag)
            elif not selected_tags[tag]:
                if tag in self.entry.getTags():
                    self.canvas.deleteTag(tag)
        self.canvas.sortTags()
        self.dialog_window.destroy()
        self.dialog_window = None
                    
    def save(self):
        tags = self.entry.getTags()
        while not tags:
            tags = self.entry.getTags()
            self.addDialog()
#            tags = simpledialog.askstring(title='Add Tags', prompt='Add at least one tag, separating multiple tags with commas')
#            tags = tags.split(',')
#            for tag in tags:
#                self.entry.addTag(tag.strip())
                
class TagsCanvas(Canvas):
    def __init__(self, master=None, entry=None, **kwargs):
        h = 1
        w = 0
        Canvas.__init__(self, master, height=h, width=w, highlightthickness=0, xscrollcommand=kwargs['xscrollcommand'])
        self.entry = entry
        
        self.tagslist = {}
        
    def clear(self):
        for tag in self.tagslist:
            self.tagslist[tag].destroy()
        self.tagslist = {}
        
    def addTag(self, tag):
        if tag not in self.entry.getTags():
            self.entry.addTag(tag)
        if tag not in self.tagslist:
            self.tagslist[tag] = TagButton(self, tag)
#            self.tagslist[tag].pack(side=LEFT, padx=1)
        self.sortTags()
        
    def deleteTag(self, tag):
        if tag in self.entry.getTags():
            self.entry.removeTag(tag)
        if tag in self.tagslist:
            self.tagslist[tag].destroy()
            del self.tagslist[tag]
        self.sortTags()
            
    def sortTags(self):
        self.delete('all')
        col = 10
        row = math.ceil(len(self.tagslist) / col)
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
                
class TagButton(Button):
    def __init__(self, master=None, text=None):
        root = None
        self.master = master
        if not self.master:
            root = Tk()
            self.master = TagsCanvas(root)
        Button.__init__(self, master=self.master, text=text, command=self.changeTagDialog)
        self.tag = text
        self.dialog = None
        self.entry = None
        if root:
            self.pack(side=LEFT)
            self.master.pack()
            root.mainloop()
        
    def changeTagDialog(self):
        self.dialog = Toplevel()
        self.dialog.grab_set()
        self.dialog.title('Change Tag')
        message = Message(self.dialog, text='Enter a new tag here:', width=150)
        self.entry = Entry(self.dialog)
        self.entry.insert(0, self.tag)
        button_box = Frame(self.dialog)
        OK = Button(button_box, text='OK', command=self.update)
        OK.bind("<Return>", self.update)
        CANCEL = Button(button_box, text='Cancel', command=self.dialog.destroy)
        DELETE = Button(button_box, text='Delete', command=self.delete)
        message.pack(side=TOP)
        self.entry.pack(side=TOP)
        OK.pack(side=LEFT)
        CANCEL.pack(side=LEFT)
        DELETE.pack(side=LEFT)
        button_box.pack(side=TOP)
        
    def update(self):
        self.tag = self.entry.get()
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
            if type(self.master) is TagsCanvas:
                self.master.deleteTag(self.tag)
                
    def makeInvisible(self):
        self.grid_forget()
        
    def __str__(self):
        return self.tag
        
    def getTag(self):
        return self.tag
               
               
class TagsCheckboxDialog:
    def __init__(self, entry=None, journal=None, tags=None, value=False):
        self.vars_dict = {}
        self.journal = journal
        self.bool_value = value
        self.tags = tags
        self.all_tags = []
        if self.journal:
            self.all_tags = self.journal.getAllTags()
        elif tags:
            self.all_tags = self.tags
        self.entry = entry
        if not self.entry:
            self.entry = JEntry() 
        for tag in self.entry.getTags():
            if tag not in self.all_tags:
                self.all_tags.append(tag)
            
        self.canvas = None
            
    def update(self, entry=None, value=False):
        if entry:
            self.entry = entry
            for tag in self.entry.getTags():
                if tag not in self.vars_dict:
                    self.vars_dict[tag] = [None, None]
                else: 
                    self.vars_dict[tag][1] = None
        for tag in self.journal.getAllTags():
            if tag not in self.vars_dict:
                self.vars_dict[tag] = [None, None]
            else: 
                self.vars_dict[tag][1] = None
        for tag in self.vars_dict:
            if self.vars_dict[tag][0] == None:
                var = None
                if tag in self.entry.getTags():
                    var = BooleanVar(name=tag, value=True)
                else:
                    var = BooleanVar(name=tag, value=value)
                self.vars_dict[tag][0] = var
                    
    def createCheckboxGrid(self):
        self.update(self.entry, value=True)
        for tag in self.vars_dict:
            self.vars_dict[tag][1] = Checkbutton(self.canvas, text=tag, variable=self.vars_dict[tag][0])
        tmp = sorted(self.vars_dict)
        row = 6
        col = math.ceil(len(tmp) / row)
        grid = [(x, y) for x in range(0, col) for y in range(0, row) ]
        for i in range(0, len(tmp)):
            x, y = grid[i]
            self.vars_dict[tmp[i]][1].grid(row=y, column=x, sticky=W)
            
    def selectAllBoxes(self):
        for index in self.vars_dict:
            self.vars_dict[index][0].set(True)
            
    def deselectAllBoxes(self):
        for index in self.vars_dict:
            self.vars_dict[index][0].set(False)
            
    def invertAllBoxes(self):
        for index in self.vars_dict:
            if self.vars_dict[index][0].get() == True:
                self.vars_dict[index][0].set(False)
            else:
                self.vars_dict[index][0].set(True)
            
    def state(self):
        self.tags = {}
        for tag in self.vars_dict:
            self.tags[tag] = self.vars_dict[tag][0].get()
#        pdb.set_trace()
        return self.tags
    def getTags(self):
        return sorted(self.vars_dict.keys())
        
    def getCheckboxCanvas(self, master):
        root = None
        if not master:
            root = Tk()
            self.canvas = Canvas(master=root, highlightthickness=0)
        else:
            self.canvas = Canvas(master, highlightthickness=0)
        if self.all_tags:
            self.createCheckboxGrid()
        else:
            message = Message(self, text='There are no tags to display.', width=200)
            message.pack(expand=True, fill=X)
            
        if root:
            self.canvas.pack(side=TOP)
            root.mainloop()
            
        return self.canvas
        
    def noTagsSelected(self):
        for tag in self.vars_dict:
            if self.vars_dict[tag][0].get() == True:
                return False
        return True