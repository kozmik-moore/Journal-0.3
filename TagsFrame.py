# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:54:44 2016

@author: Kozmik
"""
from tkinter import *
from tkinter.ttk import *
from JObject import *
from TagsCanvas import *

class TagsFrame(Frame, TagsCanvas):
    def __init__(self, master=None, entry=None, journal=None):
        root = None
        if not master:
            root = Tk()
            Frame.__init__(self, root)
        else:
            Frame.__init__(self, master)
        style = Style(self)
        style.configure('TagsFrame.TButton', background='black')
        inner_frame = Frame(self)
        frame1 = Frame(inner_frame)
        frame2 = Frame(inner_frame)
        frame3 = Frame(inner_frame)
        scrollbar = Scrollbar(frame2, orient=HORIZONTAL)
#        scrollbar.config(command=self.canvas.xview)
        TAGS = Button(frame1, text='Tags:', command=self.selectDialog)
        TAGS.pack(anchor=N)
        TagsCanvas.__init__(self, master=self, entry=entry, journal=journal)
        TagsCanvas.pack(self)
        ADD = Button(frame3, text='Add Tags', command=self.addDialog)#, style='TagsFrame.TButton')
#        self.canvas.pack(side=TOP)
#        scrollbar.pack(side=BOTTOM, expand=True, fill=X)
        ADD.pack(anchor=N, side=RIGHT)
        frame1.pack(side=LEFT, expand=True, fill=X)
        frame2.pack(side=LEFT, expand=True, fill=X)
        frame3.pack(side=LEFT, expand=True, fill=X)
        inner_frame.pack()
                  
        if root:
            self.pack(side=TOP)
            root.mainloop()
            
    def pack(self, **kwargs):
        Frame.pack(self, **kwargs)