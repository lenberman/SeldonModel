#!/usr/bin/python3
import random
import statistics
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import pdb; 
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

