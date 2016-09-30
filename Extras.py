# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 11:45:02 2016

This file contains tool, test, and experimental modules

@author: Kozmik
"""
from JObject import *
import pickle

"""------------------------Tools-------------------------"""

class Conversion:
    def __init__(self, journal):
        self.journal = journal
        self.JObj = JObject()
        
    def convert(self):
        for date in sorted(self.journal):
            body = self.journal[date][0]
            tags = self.journal[date][1]
            parent = self.journal[date][2]
            if parent:
                self.JObj.getEntry(parent).setChild(date)
            entry = JEntry(date, body, tags, parent)
            self.JObj.add(entry)
        return self.JObj
            
    def getJObject(self):
        return self.JObj
        
    def mergeJObjects(self, jobj):
        for date in jobj.getAllDates():
            if date not in self.JObj.getAllDates():
                self.JObj.add(jobj.getEntry(date))
        return self.JObj
        
"""--------------------Experiments------------------------"""
       
class Encyption:
    def __init__(self):
        None
        
class JGraph:
    def __init__(self, journal):
        self.journal = journal
        self.number_vertices = 0
        self.adjacency = {}
        self.parent = {}
        self.color = {}
        self.discovered = {}
        self.finished = {}
        self.time = 0
        for date in self.journal.getAllDates():
            self.adjacency[date] = []
            parent = self.journal[date].getParent()
            if parent:
                self.adjacency[parent].append(date)
            self.number_vertices += 1
        self.tree_list = []
            
    def DFS(self):
        for date in self.journal.getAllDates():
            self.color[date] = 'white'
            self.parent[date] = None
        self.time = 0
        self.tree_list = list(0 for x in range(0, self.number_vertices*2))
        for date in self.journal.getAllDates():
            if self.color[date] == 'white':
                self.DFSVisit(date)
    def DFSVisit(self, date):
        self.time += 1
        self.discovered[date] = self.time
        self.tree_list[self.time-1] = date
        self.color[date] = 'gray'
        for item in self.adjacency[date]:
            if self.color[item] == 'white':
                self.parent[item] = date
                self.DFSVisit(item)
        self.color[date] = 'black'
        self.time += 1
        self.finished[date] = self.time
        self.tree_list[self.time-1] = date
            
    def addVertex(self, vertex):
        self.adjacency[vertex] = []
        self.number_vertices += 1
    def addArc(self, parent, child):
        if parent in self.adjacency:
            if child in self.adjacency:
                self.adjacency[parent].append(child)
                self.parent[child] = parent
    def deleteVertex(self, vertex):
#        pdb.set_trace()
        if vertex in self.adjacency:
            while len(self.adjacency[vertex]) > 0:
                child = self.adjacency[vertex][0]
                self.deleteArc(vertex, child)
                self.journal.changeParent(child, None)
            del self.adjacency[vertex]
            self.number_vertices -= 1
    def deleteArc(self, parent, child):
        if self.parent[child] == parent:
            self.parent[child] = None
            self.adjacency[parent].remove(child)
            
    def getGraph(self):
        None
    def getTreeRoot(self, date):
        if not self.parent:
            self.DFS()
        parent = self.parent[date]
        root = date
        while parent:
            root = parent
            parent = self.parent[parent]
        return root
    def getDiscovered(self, date=None):
        if not date:
            return self.discovered
        else:
            return self.discovered[date]
    def getFinished(self, date=None):
        if not date:
            return self.finished
        else:
            return self.finished[date]
    def getAdjacency(self):
        return self.adjacency
    def getParentDict(self):
        return self.parent
    def getTreeList(self):
        return self.tree_list
    def getTree(self, date):
        self.DFS()
        root = self.getTreeRoot(date)        
        top = self.tree_list.index(root)
        bottom = self.tree_list.index(root, top+1)
        return self.tree_list[top: bottom+1]
        