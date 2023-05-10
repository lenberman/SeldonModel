#!/usr/bin/python3
import random
import statistics
import math
import sys
import numpy as np
from pprint import pprint

now = 0
class World:
    def __init__(self, extent, dimension=3, faces=6):
        self.dimension = dimension
        self.faces = faces
        self.extent = extent
        self.shape = [ faces ]
        self.regions = ()
        size = faces
        for i  in range(dimension-1):
            self.shape.append(extent)
            size *= extent
            #        self.surface = np.empty(self.shape, dtype=dict.__class__)
        self.surface = list()
        for i in range(size):
            rem = i//faces
            coord = list()
            coord. append(i%faces)
            for j in range(dimension-1):
                coord.append(rem%extent)
                rem //= extent
            self.surface.append(coord)


    def __str__(self):
        rv = "Dimension(" + str(self.dimension) + ")" + "Extent(" + str(self.extent) + ")\n"
        rv += str(self.shape) 
        return rv
        
    def getRegion(self, size):
        return Region(self, size)

    def addNode(self, nd, loc=None):
        if self.dimension == 3:
            region = self.surface[loc[1],loc[2],loc[3]]
        elif self.dimension == 2:
            region = self.surface[loc[1],loc[2]]
        elif self.dimension == 1:
            region = self.surface[loc[1]]

class Region:
    def __init__(self, world, size=1):
        self.world = world
        self.size = size
        self.locales = {}
        for i in(range(size)):
            val = tuple(world.surface.pop())
            self.locales[val] = {}
        # del world.surface[0:size]

    def __str__(self):
        var = "World:" + str(self.world) + ", size= "
        var += str(self.size) + " locales: "  str(self.locales)
        return var
        

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
    def getRootNode(self, event):...
        

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
    reg = wrld.getRegion(12)
    print(str(wrld))
    print(str(reg))
    ev = Event()
    print(ev)
    money = UseValue("medium-of-exchange")
    print(money)
    
    
