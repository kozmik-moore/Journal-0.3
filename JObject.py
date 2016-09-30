# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:45:07 2016

@author: Kozmik
"""


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
        if tag not in self.tags:
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
        
    def getCopy(self):
        new = JEntry(self.date, self.body, self.tags, self.parent, self.child)
        return new
        
    def equals(self, entry):
        if len(self.getTags()) != len(entry.getTags()):
            return False
        for tag in self.tags:
            if tag not in entry.getTags():
                return False
        if self.date != entry.getDate():
            return False
        if self.body != entry.getBody():
            return False
        if self.parent != entry.getParent():
            return False
        if self.child != entry.getChild():
            return False
        return True


class JObject():
    def __init__(self):
        self.storage = dict()
        self.population = 0
        
    def getAllDates(self):
        return sorted(self.storage.keys())
        
    def getAllTags(self):
        tagslist = []
        for date in self.storage:
            for tag in self.storage[date].getTags():
                if tag not in tagslist:
                    tagslist.append(tag)
        return tagslist
        
    def add(self, entry):
        self.storage[entry.getDate()] = entry
        self.population += 1
        
    def delete(self, entry):
        del self.storage[entry.getDate()]
        self.population -= 1
        
    def getEntry(self, date):
        return self.storage[date]
        
    def getNumberOfEntries(self):
        return self.population
        
    def getCopy(self):
        new = JObject()
        for date in self.getAllDates():
            new.add(self.getEntry(date).getCopy())
        return new   
        
    def isEmpty(self):
        if self.storage:
            return False
        else:
            return True
            
    def equals(self, journal):
        if self.population != journal.getNumberOfEntries():
            return False
        for date in self.getAllDates():
            if date not in journal.getAllDates():
                return False
            else:
                if not self.getEntry(date).equals(journal.getEntry(date)):
                    return False
        return True
