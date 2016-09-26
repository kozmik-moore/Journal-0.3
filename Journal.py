# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:00:50 2016

@author: Kozmik
"""
from tkinter import *
import pickle
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from tkinter import font
import math
import pdb

class JEntry:
    def __init__(self, date=None, body=None, tags=None, parent=None, child=None):
        self.date = date
        self.body = body
        self.tags = tags
        if not tags:
            self.tags = []
        self.parent = parent
        self.child = child
        
    def getDate(self):
        return self.date
        
    def getBody(self):
        return self.body
        
    def getTags(self):
        return sorted(self.tags)
        
    def getParent(self):
        return self.parent
        
    def getChild(self):
        return self.child
        
    def setDate(self, date):
        self.date = date
        
    def setBody(self, body):
        self.body = body
        
    def setTags(self, tags):
        self.tags = tags
        
    def setParent(self, parent):
        self.parent = parent
        
    def setChild(self, child):
        self.child = child
        
    def addTag(self, tag):
        self.tags.append(tag)
        
    def removeTag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
            
    def linkParent(self, date):
        self.parent = date
        
    def unlinkParent(self):
        self.parent = None
        
    def linkChild(self, date):
        self.child = date
        
    def unlinkChild(self):
        self.child = None
        
    def copy(self):
        new = JEntry(self.date, self.body, self.tags, self.parent, self.child)
        return new


class JObject(dict):
    def __init__(self):
        dict.__init__(self)
        self.population = 0
        
    def getAllDates(self):
        return sorted(self.keys())
        
    def getAllTags(self):
        tagslist = []
        for date in self:
            for tag in self[date].getTags():
                if tag not in tagslist:
                    tagslist.append(tag)
        return tagslist
        
    def add(self, entry):
        self[entry.getDate()] = entry
        self.population += 1
        
    def delete(self, entry):
        del self[entry.getDate()]
        self.population -= 1
        
        
#class JGraph:
#    def __init__(self, journal):
#        self.journal = journal
#        self.number_vertices = 0
#        self.adjacency = {}
#        self.parent = {}
#        self.color = {}
#        self.discovered = {}
#        self.finished = {}
#        self.time = 0
#        for date in self.journal.getAllDates():
#            self.adjacency[date] = []
#            parent = self.journal[date].getParent()
#            if parent:
#                self.adjacency[parent].append(date)
#            self.number_vertices += 1
#        self.tree_list = []
#            
#    def DFS(self):
#        for date in self.journal.getAllDates():
#            self.color[date] = 'white'
#            self.parent[date] = None
#        self.time = 0
#        self.tree_list = list(0 for x in range(0, self.number_vertices*2))
#        for date in self.journal.getAllDates():
#            if self.color[date] == 'white':
#                self.DFSVisit(date)
#    def DFSVisit(self, date):
#        self.time += 1
#        self.discovered[date] = self.time
#        self.tree_list[self.time-1] = date
#        self.color[date] = 'gray'
#        for item in self.adjacency[date]:
#            if self.color[item] == 'white':
#                self.parent[item] = date
#                self.DFSVisit(item)
#        self.color[date] = 'black'
#        self.time += 1
#        self.finished[date] = self.time
#        self.tree_list[self.time-1] = date
#            
#    def addVertex(self, vertex):
#        self.adjacency[vertex] = []
#        self.number_vertices += 1
#    def addArc(self, parent, child):
#        if parent in self.adjacency:
#            if child in self.adjacency:
#                self.adjacency[parent].append(child)
#                self.parent[child] = parent
#    def deleteVertex(self, vertex):
##        pdb.set_trace()
#        if vertex in self.adjacency:
#            while len(self.adjacency[vertex]) > 0:
#                child = self.adjacency[vertex][0]
#                self.deleteArc(vertex, child)
#                self.journal.changeParent(child, None)
#            del self.adjacency[vertex]
#            self.number_vertices -= 1
#    def deleteArc(self, parent, child):
#        if self.parent[child] == parent:
#            self.parent[child] = None
#            self.adjacency[parent].remove(child)
#            
#    def getGraph(self):
#        None
#    def getTreeRoot(self, date):
#        if not self.parent:
#            self.DFS()
#        parent = self.parent[date]
#        root = date
#        while parent:
#            root = parent
#            parent = self.parent[parent]
#        return root
#    def getDiscovered(self, date=None):
#        if not date:
#            return self.discovered
#        else:
#            return self.discovered[date]
#    def getFinished(self, date=None):
#        if not date:
#            return self.finished
#        else:
#            return self.finished[date]
#    def getAdjacency(self):
#        return self.adjacency
#    def getParentDict(self):
#        return self.parent
#    def getTreeList(self):
#        return self.tree_list
#    def getTree(self, date):
#        self.DFS()
#        root = self.getTreeRoot(date)        
#        top = self.tree_list.index(root)
#        bottom = self.tree_list.index(root, top+1)
#        return self.tree_list[top: bottom+1]
        
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
            
        
class BodyFrame(Frame):
    def __init__(self, master=None, entry=None):
        root = None
        self.master = master
        if not self.master:
            root = Tk()
            Frame.__init__(self, root)
        else:
            Frame.__init__(self, self.master)
        body_font = font.Font(family='Microsoft Sans Serif', size=10)
        self.entry = entry
        if not self.entry:
            self.entry = JEntry()
        
        self.scrollbar = Scrollbar(self)
        self.body_field = Text(self, font=body_font, yscrollcommand=self.scrollbar.set, wrap=WORD)        
        self.scrollbar.config(command=self.body_field.yview)
        self.body_field.pack(side=LEFT, expand=True, fill=BOTH)
        self.scrollbar.pack(side=LEFT, fill=Y)
        
        if self.entry.getBody():
            self.updateGUI(self.entry)
        
        if root:
            root.mainloop()
        
    def updateGUI(self, entry):
        self.entry = entry
        self.clearGUI()
        if entry.getBody():
            self.body_field.insert(CURRENT, entry.getBody())
            
    def clearGUI(self):
        self.body_field.delete('1.0', END)
        
    def save(self):
        if self.body_field.strip():
            entry.setBody(self.body_field.get('1.0', END))
        
        
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
        self.dialog = TagsCheckboxDialog(self, self.entry, self.journal)
        
        self.canvas = TagsCanvas(self, self.entry)
        TAGS = Button(self, text='Tags:', command=self.selectDialog)
        TAGS.pack(side=LEFT, anchor=W)
        ADD = Button(self, text='Add Tags', command=self.addDialog)
        self.canvas.pack(side=LEFT, anchor=W, expand=True, fill=X)
        ADD.pack(side=RIGHT)
        
        for tag in self.entry.getTags():
            self.canvas.addTag(tag)
                
        self.pack(side=TOP)
                
        if root:
            root.mainloop()
        
    def updateGUI(self, entry):
        self.entry = entry
        self.canvas.clear()
        if self.entry.getTags():
            for tag in self.entry.getTags():
                self.canvas.addTag(tag)
        
    def addDialog(self):
        tags = simpledialog.askstring(title='Add Tags', prompt='Enter at least one tag, separating multiple tags with a comma:')
        if tags:
            tags = tags.split(',')
            for tag in tags:
                if tag.strip():
                    self.canvas.addTag(tag.strip())
                    
    def selectDialog(self):
        main = Toplevel()
        main.title('Select Tags')
        self.dialog = TagsCheckboxDialog(main, self.entry, self.journal)
        self.dialog.pack()
        main.protocol("WM_DELETE_WINDOW", lambda self=self, dialog=self.dialog, window=main: self.propogateTags(self.dialog, window))
                
    def propogateTags(self, dialog, window):
        selected_tags = dialog.state()
        for tag in selected_tags:
            if selected_tags[tag]:
                if tag not in self.entry.getTags():
                    self.canvas.addTag(tag)
            elif not selected_tags[tag]:
                if tag in self.entry.getTags():
                    self.canvas.deleteTag(tag)
        self.canvas.sortTags()
        window.destroy()
                    
    def save(self):
        tags = self.canvas.getTags()
        while not tags:
            tags = simpledialog.askstring(title='Add Tags', prompt='Add at least one tag, separating multiple tags with commas')
            tags = tags.split(',')
            for tag in tags:
                self.entry.addTag(tag.strip())
                
class TagsCanvas(Canvas):
    def __init__(self, master=None, entry=None):
        h = 1
        w = 0
        Canvas.__init__(self, master, height=h, width=w)
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
            self.tagslist[tag].pack(side=LEFT, padx=1)
#            self.itemconfig(self.tagslist[tag], tag)
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
        for tag in sorted(self.tagslist):
            self.tagslist[tag].makeInvisible()
        for tag in sorted(self.tagslist):
            self.tagslist[tag].pack(side=LEFT, padx=1)
            
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
        self.dialog.destroy()
        self.dialog = None
        self.config(text=self.tag)
        self.pack(side=LEFT, padx=1)
        
    def delete(self):
        delete = messagebox.askyesno(title='Delete?', message='Are you sure you want to delete this tag?')
        self.dialog.destroy()
        self.dialog = None
        if delete:
            self.destroy()
            if type(self.master) is TagsCanvas:
                self.master.deleteTag(self.tag)
                
    def makeInvisible(self):
        self.pack_forget()
        
    def __str__(self):
        return self.tag
        
    def getTag(self):
        return self.tag
               
               
class TagsCheckboxDialog(Canvas):
    def __init__(self, master=None, entry=None, journal=None, tags=None, value=False, side=TOP):
        self.vars_dict = {}
        self.vars = []
        root = None
        self.master = master
        self.journal = journal
        self.tags = tags
        all_tags = []
        if self.journal:
            all_tags = self.journal.getTags()
        elif tags:
            all_tags = self.tags
        self.entry = entry
        if not self.entry:
            self.entry = JEntry()
        entry_tags = self.entry.getTags()
        for tag in entry_tags:
            if tag not in all_tags:
                all_tags.append(tag)
#        tags = None
#        value = None
#        side = None
            
#        if 'master' in kwargs:
#            self.master = kwargs['master']
#        if 'tags' in kwargs:
#            tags = kwargs[tags]
#        elif 'journal' in kwargs:
#            self.journal = kwargs['journal']
#            tags = self.journal.getTags()
#        if 'value' in kwargs:
#            value = kwargs['value']
#        if 'side' in kwargs:
#            side = kwargs['side']
            
        if not self.master:
            root = Tk()
            Canvas.__init__(self, master=root)
        else:
            Canvas.__init__(self, self.master)
#        self.cb_list = []
        if all_tags:
            for tag in sorted(all_tags):
                var = None
                if tag in entry_tags:
                    var = BooleanVar(name=tag, value=True)
                else:
                    var = BooleanVar(name=tag, value=value)
                self.vars_dict[tag] = Checkbutton(self, text=tag, variable=var)
    #            self.cb_list.append(chk)
    #           chk.pack(side=side, anchor=anchor, expand=YES)
                self.vars.append(var)
#        pdb.set_trace()
            tmp = sorted(self.vars_dict)
#            item = 0
            row = 6
            col = math.ceil(len(tmp) / row)
            grid = [(x, y) for x in range(0, col) for y in range(0, row) ]
            for i in range(0, len(tmp)):
                x, y = grid[i]
                self.vars_dict[tmp[i]].grid(row=y, column=x, sticky=W)
        else:
            message = Message(self, text='There are no tags to display.', width=200)
            message.pack(expand=True, fill=X)
#        while item < len(tmp):
#            for i in range(0, row):
#                try:
#                    self.vars_dict[tmp[i]].grid(row=i, column=col, sticky=W)
#                    item+=1
#                except IndexError:
#                    break
#            col+=1
            
        if root:
            self.pack(side=side)
            root.mainloop()
            
    def state(self):
#        return list(map((lambda var: var.get()), self.vars))
        self.tags = {}
        for i in range(0, len(self.vars)):
            self.tags[sorted(self.vars_dict.keys())[i]] = self.vars[i].get()
        return self.tags
    def getTags(self):
        return sorted(self.vars_dict.keys())

        
class AppFrame(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w*.9, h*.8))
        self.title('Journal')
        
        self.journal = JObject()
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
        welcome = JEntry(date, body, tags)
        self.journal.add(welcome)
        
        self.config_path = abspath(getsourcefile(lambda:0)).strip('Journal0.3.py')
        self.ini = {'SAVE LOCATION': None, 'BACKUP LOCATION': None, 'LAST BACKUP': None, 'BACKUP INTERVAL': -1}
        
        try:
            fin = open(self.config_path + "Journal.ini", "rb")
            self.ini = pickle.load(fin)
        except FileNotFoundError:
            self.changeSaveDirectory()
            fin = open(self.config_path + "Journal.ini", "wb")
            pickle.dump(self.ini, fin)
        fin.close()
        
        try:
            fin = open(self.ini['SAVE LOCATION'] + "Reg.jdb", "rb")
            self.journal = pickle.load(fin)
        except FileNotFoundError:
            fin = open(self.ini['SAVE LOCATION'] + "Reg.jdb", "wb")
        fin.close()
        