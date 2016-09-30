# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:00:50 2016

@author: Kozmik
"""
from tkinter import *
from tkinter.ttk import *
import pickle
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from tkinter import font
from datetime import datetime
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
        self.journal = journal
        
        self.user_date = ''
        self.program_date = 0
        
        self.MONTHS = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", 
        "05":"May", "06":"Jun", "07":"Jul", "08":"Aug", 
        "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}
        
        self.dates_registry = {}
        self.updateDateRegistry()
        
        self.date_box = Combobox(self, postcommand=self.updateDateboxList)
        
    def updateGUI(self, entry):
        self.entry = entry
        self.date_box.set(self.ConvertToUserFormat(self.entry.getDate()))
    def bindDatebox(self, function):
        self.date_box.bind("<ComboboxSelected>", function)
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
    def get(self):
        return self.date.get()
    def ConvertToUserFormat(self, date):
        stringdate = str(date)
        if stringdate != '':
            datestr = ''
            datestr = stringdate[6:8] + ' ' + self.MONTHS[stringdate[4:6]] + ' ' + stringdate[:4] + ', ' + stringdate[8:]
            return datestr
    def updateDateboxList(self):
#        self.clear()
        self.implementFilters()
        self.date_box['values'] = self.getUserDates()
    def getUserDates(self):
        dates_list = []
        for date in sorted(self.dates_registry.keys()):
            dates_list.append(self.dates_registry[date])
        return dates_list
    def getProgramDates(self):
        return sorted(self.dates_registry.keys())
        
class DateFilter:
    def __init__(self, entry=None, journal=None):
        self.entry = entry
        if not self.entry:
            self.entry = JEntry()
        self.journal = journal
        self.filter_type = StringVar(name="Search Type", value="OR")
        self.tagslist = []
        if self.journal:
            self.tagslist + self.journal.getAllTags()
        self.tagslist += self.entry.getTags()
        self.check_box_dialog = TagsCheckboxDialog(self.entry, self.journal, None, True)

    def createFilterDialog(self):
        main = Toplevel()
        top = Frame(main)
        middle = Frame(main)
        bottom = Frame(main)
        
        cb_canvas = self.check_box_dialog.getCheckboxCanvas(main)
        main.title("Filters")
        
        ORPTYPE = Radiobutton(top, text="OR(P)", value="OR(P)", variable=self.filter_type)
        ORPTYPE.grid(row=0, column=1, sticky=W)
        ORTYPE = Radiobutton(top, text="OR", value="OR", variable=self.filter_type)
        ORTYPE.grid(row=0, column=0, sticky=W)
        ANDTYPE = Radiobutton(top, text="AND", value="AND", variable=self.filter_type)
        ANDTYPE.grid(row=0, column=2, sticky=W)
        
        cb_canvas.grid(row=1, column=0, rowspan=10, columnspan=2)
        ALL = Button(bottom, text="All", command=lambda:self.selectAllCheckboxes(filter_list))
        NONE = Button(bottom, text="None", command=lambda:self.deselectAllCheckboxes(filter_list))
        INVERT = Button(bottom, text="Invert", command=lambda:self.invertSelection(filter_list))
        ALL.grid(row=2, column=0)
        NONE.grid(row=2, column=1)
        INVERT.grid(row=2, column=2)
        top.pack(side=TOP)
        middle.pack(side=TOP)
        bottom.pack(side=TOP)
        main.grab_set()
        self.clear()
        self.entry_obj.update()
        return main
        
        
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
        self.dialog = TagsCheckboxDialog(self.entry, self.journal)
        style = Style(self)
        style.configure("TagsFrame.TButton", side=TOP)
        frame1 = Frame(self)
        frame2 = Frame(self)
        frame3 = Frame(self)
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
        canvas = self.dialog.getCheckboxCanvas(main)
        canvas.pack()
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
        self.vars = []
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
            
    def update(self, entry):
        self.entry = entry
        for tag in self.entry.getTags():
            if tag not in self.all_tags:
                self.all_tags.append(tag)
                
    def createCheckboxGrid(self, value):
        for tag in sorted(self.all_tags):
                var = None
                if tag in self.entry.getTags():
                    var = BooleanVar(name=tag, value=True)
                else:
                    var = BooleanVar(name=tag, value=value)
                self.vars_dict[tag] = Checkbutton(self.canvas, text=tag, variable=var)
                self.vars.append(var)
        tmp = sorted(self.vars_dict)
        row = 6
        col = math.ceil(len(tmp) / row)
        grid = [(x, y) for x in range(0, col) for y in range(0, row) ]
        for i in range(0, len(tmp)):
            x, y = grid[i]
            self.vars_dict[tmp[i]].grid(row=y, column=x, sticky=W)
            
    def selectAllBoxes(self):
        for index in self.vars:
            self.vars[index] = True
            
    def deselectAllBoxes(self):
        for index in self.vars:
            self.vars[index] = False
            
    def invertAllBoxes(self):
        for index in self.vars:
            if self.vars[index]:
                self.vars[index] = False
            else:
                self.vars[index] = True
            
    def state(self):
        self.tags = {}
        for i in range(0, len(self.vars)):
            self.tags[sorted(self.vars_dict.keys())[i]] = self.vars[i].get()
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
            self.createCheckboxGrid(self.bool_value)
        else:
            message = Message(self, text='There are no tags to display.', width=200)
            message.pack(expand=True, fill=X)
            
        if root:
            self.canvas.pack(side=TOP)
            root.mainloop()
            
        return self.canvas
        

        
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
        