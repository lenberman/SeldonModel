#!/usr/bin/python3
import random
import statistics
import math
import sys
import numpy as np
from pprint import pprint

now = 0
class Region:
    ## regions is a dict with indexed by index-tuples.
    def __init__(self, regions, size=1):
        self.size = size
        self.locales = {}
        assert(size<=len(regions))
        for i in(range(size)):
            a = regions.popitem()
            self.locales[a[0]] = a[1]

    def getSubregion(self, size=1):
        subR = Region(self.locales, size)
        for i in(range(size)):
            val = self.locales.popitem()
            subR.locales[val[0]] = val[1]
        self.size -= size
        return subR
        

    def __str__(self):
        var = "\nRegion of size(" + str(self.size) + ")   locales: "  + str(self.locales)
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
class Inclusion(edg):
    def __init__(self, *src, target=None, forward=False, end=None, start = now):
        super().__init__(src, target, forward, end, start)

class Meiotic(edg):
    def __init__(self, *src, target=None, forward=True, end=None, start = now):
        super().__init__(src, target, forward, end, start)

class Mitotic(edg):
    def __init__(self, *src, target=None, forward=True, end=None, start = now):
        super().__init__(src, target, forward, end, start)

class Agreement(edg):
    def __init__(self, src, target, forward=True, end=None, start = now):
        super().__init__(src, target, forward, end, start)

    def addPromise(self,uv):...

class Node:   # # Node in Seldon decomposition
    indx = 0
    nodes = {}

    def __init__(self, name, information, event=Event()):  # # any Node may have lifetime
        # increment then stor
        Node.indx += 1
        self.name = name
        self.nId = Node.indx
        self.edges = list()
        self.birth = event
        self.info= information
        Node.nodes[name] = self

    def addEdge(self, tgt=None, edgClass=None, fwd=True, strt=None, nd=None):
        tmp = edgClass(self, target=tgt, forward=fwd, end=nd, start=strt)
        self.edges.append(tmp)
        return tmp
            
            

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


    def addEdge(self, target, info, event=Event()):...
        
    

class iNode(Node):
    sorts = [ "Zygotic", "Commercial", "Governmental", "Institutional" ]

    @classmethod
    def  iZygote(cls, nd):
        assert(nd.zygote == True)
        assert(False)


        
    def __init__(self, gov, poss=None, event=Event(), info=None, mny=None,name=None):
        super().__init__(self, info, event)
        if poss is None:
            self.possessions = {} #owned cNodes
        else:
            self.possessions = poss
        


# linked to geometry
class Government(iNode):
    indx = 0
    def  __init__(self, region, laws=None, name=None): 
        if name is None:
            name = "gov" + str(Government.indx)
            Government.indx += 1
        super().__init__(self, laws, name)
        self.region = region
        self.nation = False

    @classmethod
    def getInsitution(participants, name, rules=None):
        external = participants[0].nation
        for gov in participants:
            assert(external is gov.nation)
        inst = Institution(participants, name)
        return inst
            

    # internal governmental subdivision
    def getSubGov(self, size):
        reg = Region(self.region.locales, size)
        reg = Government(reg)
        edge = reg.addEdge(self, Mitotic, False)
        return reg

## World holds regions and Nations.  Links  geometry to nodes.
class World(Government):
    disputeRS = None
    
    # create world with given dimension and #faces each 
    def __init__(self, extent, dimension=3, faces=6):
        self.dimension = dimension
        self.faces = faces
        self.extent = extent
        self.shape = [ faces ]
        self.states = list()
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

    def getNation(self, size):
        reg = self.getRegion( size)
        gov = Government(reg)
        gov.nation = True
        self.states.append(gov)
        edge = gov.addEdge(self, Inclusion, False)
        return gov

    def __str__(self):
        rv = "Dimension(" + str(self.dimension)  + "), Extent(" + str(self.extent) + ")\n"
        rv += str(self.shape) +"\n" + str(self.surface)
        return rv
        
    def getRegion(self, size):
        assert(size <= len(self.surface))
        return Region(self.surface, size)


class Institution(iNode):
    def __init__(self, govList, name):
        ...

class Commerce(Node):
    def __init__(self, possessor:iNode, factory=True, cInfo=None):
        super().__init__(self, cInfo)
        self.owner = possessor
        self.info = cInfo
    ...

    
    
