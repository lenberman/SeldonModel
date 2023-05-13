#!/usr/bin/python3
import random
import statistics
import math
import sys
import numpy as np
from pprint import pprint

now = 0
class World:
    # create world with given dimension and #faces each 
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
        self.surface = {}
        for i in range(size):
            rem = i//faces
            coord = list()
            coord. append(i%faces)
            for j in range(dimension-1):
                coord.append(rem%extent)
                rem //= extent
            self.surface[tuple(coord)] = {}


    def __str__(self):
        rv = "Dimension(" + str(self.dimension)  + "), Extent(" + str(self.extent) + ")\n"
        rv += str(self.shape) +"\n" + str(self.surface)
        return rv
        
    def getRegion(self, size):
        return Region(self.surface, self, size)

class Region:
    def __init__(self, regions, parent, size=1):
        self.parent = parent
        self.size = size
        self.locales = {}
        assert(size<=len(regions))
        for i in(range(size)):
            a = regions.popitem()
            self.locales[a[0]] = a[1]

    def getSubregion(self, size=1):
        subR = Region(self.locales, self, size)
        assert(subR.parent == self)
        for i in(range(size)):
            val = self.locales.popitem()
            subR.locales[val[0]] = val[1]
        self.size -= size
        return subR
        

    def __str__(self):
        var = "\nRegion of size(" + str(self.size) + ") in world:[" + str(self.parent) + "], size= "
        var += " locales: "  + str(self.locales)
        return var
        
    # add node to a locale in self
    def addNode(self, nd, locale=None):
        ...

class Event:  # space time chunk starting now
    events = {}
    def __init__(self, t=now, i=None, j=None, k=None):
        val = (t, i, j, k)
        try:
            val = Event.events[val]
        except KeyError:
            Event.events[val] = val
        self.val = val

class UseValue:  #fear power friendship love medium-of-exchange
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
    # create edge from (src->tgt || tgt->src)
    def __init__(self, src=None , tgt=None, forward=True, end=None, start = now):
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
    nodes = {}

    def __init__(self, name, information, event=Event()):  # # any Node may have lifetime
        # increment then stor
        Node.indx += 1
        self.nId = Node.indx
        self.edges = {}
        self.birth = event
        self.info= information

        

    def addEdge(self, tgt=None, forward=True, start=None, end=None):
        tmp = edg(self, tgt, forward, end, start)


    def where(self, when=now):...
        
    def step(self, until=now+1):
        ...

class bNode(Node):
    @classmethod
    def zygote(cls, name, info=None):
        try:
            return Node.nodes[name]
        except KeyError:
            Node.nodes[name] =  bNode(name, info)
            z = Node.nodes[name]
            z.zygote = True
        return z
        
    def __init__(self, name=None, info=None, event=Event()):
        super().__init__(self, info,event)
        self.zygote = False


    def addEdge(self, tgt, info, event=Event()):...
        
    

class iNode(Node):
    sorts = [ "Zygotic", "Commercial", "Governmental", "Institutional" ]

    @classmethod
    def  iZygote(cls, nd):
        assert(nd.zygote == True)
        ...

    def __init__(self, gov, event=Event(), info=None, mny=None):
        super().__init__(self, info, event)
        self.possessions = ()   #owned cNodes
        self.gov = gov

class govNode(iNode):...

class insNode(iNode):...

class cNode(Node):
    def __init__(self, possessor, factory=True, cInfo=None):
        super().__init__(self, cInfo)
        self.owner = possessor
        self.info = cInfo
    ...

    
    
