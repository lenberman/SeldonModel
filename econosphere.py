#!/usr/bin/python3
import random
import statistics
import math
import sys
import numpy as np
from pprint import pprint

now = 0
dimension = 3
faces = 6

class World:
    def __init__(self, extent):
        self.extent = extent
        self.shape = [ faces ]
        for i  in range(dimension-1):
            self.shape.append(extent)
        print(self.shape)
        self.surface = np.empty(self.shape, dtype=dict.__class__)
        

    def __str__(self):
        rv = "Dimension(" + str(dimension) + ")" + "Extent(" + str(self.extent) + ")\n"
        rv += str(np.shape(self.surface))
        return rv
        
    def addNode(self, nd, loc=None):
        if dimension == 3:
            region = self.surface[loc[1],loc[2],loc[3]]
        elif dimension == 2:
            region = self.surface[loc[1],loc[2]]
        elif dimension == 1:
            region = self.surface[loc[1]]

class Event:  # space time chunk starting now
    events = {}
    def __init__(self, t=now, i=None, j=None, k=None):
        val = (t, i, j, k)
        try:
            val = Event.events[val]
        except KeyError:
            Event.events[val] = val
        self.val = val

class UseValue:
    uvId = 0
    uvList = dict()
    @classmethod
    def  UV(cls, name, list=None):    #list(name) relates this UV to previous
        obj = cls.uvList.get(name)
        if ( obj is None):   # create UseValue
            obj = UseValue(nm, list)
        obj

    def __init__(self, nm, ins=None):
        UseValue.uvId += 1
        if ins is not None:
            for i in ins:
                nm += "|" + str(i.uvId)
            nm += "|"
        self.name = nm
        self.uvId = UseValue.uvId
        UseValue.uvList[ nm ] = self
        UseValue.uvList[ self.uvId ] = self
        self

    def __str__(self):
        return self.name + "(" + str(self.uvId) + ")"
        
#  directed  edges with (multi-dimsensional) capacity and adjustable delay.
class edg:
    edgeDict = {}
    def __init__(self, src, tgt=None, forward=True, end=None, start = now):
        self.forward = forward
        if forward == True:
            self.edge = [src, tgt]
        else:
            self.edge = [tgt, src]
        self.start = start
        self.end = end
                 
        #  self.capacity = capacity  # (UseValue,capacity,unit cost)  in agreement class
class inclusion(edg):
    def __init__(self, src, tgt=None, forward=False, end=None, start = now):
        super().__init__(self, src, tgt, forward, end, start)

class meiotic(edg):
    def __init__(self, src, tgt=None, forward=True, end=None, start = now):
        super().__init__(self, src, tgt, forward, end, start)

class mitotic(edg):
    def __init__(self, src, tgt=None, forward=True, end=None, start = now):
        super().__init__(self, src, tgt, forward, end, start)

class agreement(edg):
    def __init__(self, src, tgt, forward=True, end=None, start = now):
        super().__init__(self, src, tgt, forward, end, start)

    def addPromise(self,uv):...

class Node:   # # Node in Seldon decomposition
    indx = 0
    @classmethod   #get node
    def getNode(cls, edges):
        newNode = True
        for e in edges:
            if not ( e.__class__ is Meiotic):
                newNode = False
                break
        if newNode == True:
            ...

    def __init__(self, information, event=Event()):  # # any Node may have lifetime
        # increment then stor
        Node.indx += 1
        self.nId = Node.indx
        self.birth = event
        self.info= information

    def where(self, when=now):...
        
    def step(self, until=now+1):
        ...

class bNode(Node):
    def __init__(self, info=None,event=Event()):
        super().__init__(self, info,event)
    ...

class iNode(Node):
    sorts = [ "Zygotic", "Commercial", "Governmental", "Institutional" ]
    
    def __init__(self, gov, event=Event(), info=None, mny=None):
        super().__init__(self, info, event)
        self.gov = gov
        ...
    def getCNode(self, uv , factory=False):
        ...

class cNode(Node):
    def __init__(self, possessor, cInfo=None):
        super().__init__(self, cInfo)
        self.owner = possessor
    ...

if __name__ == '__main__':
    wrld = World(2)
    print(str(wrld))
    ev = Event()
    print(ev)
    money = UseValue("medium-of-exchange")
    print(money)
    
    
