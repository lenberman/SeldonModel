#!/usr/bin/python3
""" Provides Base classes for graph and geometry """
import random
import statistics
import math
import sys
import pdb
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

NOW = 0
#import pdb; pdb.set_trace()

class Event:  # space time chunk starting NOW
    """" time and space """
    events = {}

    @classmethod
    def getChunk(cls, t=NOW, i=None, j=None, k=None):
        try:
            return Event.events[(t, (i,j,k) )]
        except KeyError:
            return  Event(t, i, j, k)

    def __init__(self, t=NOW, i=None, j=None, k=None):
        self.time = t
        self.space = (i,j,k)
        assert Event.events.get((self.time,self.space)) is None
        Event.events[(self.time,self.space)] = (self.time,self.space)

    def __str__(self):
        return "(@" + str(self.time) + "T, loc:" + str(self.space) + ")"


class UseValue:
    """ Examples include: fear power friendship love medium-of-exchange """
    uvId = 0
    uvList = {}
    @classmethod
    def  UV(cls, name, list=None):    #list(name) relates this UV to previous
        obj = cls.uvList.get(name)
        if  obj is None:   # create UseValue
            obj = UseValue(name, list)
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
class Edge:
    """ 4 different semantic types of edges """
    edgeTypes = {}

    @classmethod
    def connect(cls, src, tgt):
        return cls(src, tgt)

    def __str__(self):
        return str(vars(self.edge[0])) + "\n\t>>\n" + str(vars(self.edge[1])) + \
            "@(" + str(self.start) + ", " + str(self.end) + ")\n"

    # create edge from (src->tgt || tgt->src)
    def __init__(self, src=None , tgt=None, forward=True, end=None, start = NOW):
        self.forward = forward
        if forward == True:  # check Node.isTop
            self.edge = [src, tgt]
        else:
            self.edge = [tgt, src]
        self.start = start
        self.end = end

        def reverse(self):
            self.edge = (self.edge[1], self.edge[0])


##Node
class Node:   # # Node in Seldon decomposition
    """ Base class for all nodes """
    indx = 0
    nodes = {}

    # create out-edges from self to tgt
    def __rshift__(self, tgt):
        for target in tgt:
            nodeTgt = target[0](target[1])
        return edge

    def __init__(self, name=None, event=None):  # # any Node may have lifetime
        # increment then stor
        Node.indx += 1
        self.name = name
        self.nId = Node.indx
        if self.name is None:
            self.name = "Node_" + str(self.nId)
        self.edges = []
        self.birth = event
        self.location = None
        self.info= None
        self.power = None
        self.fear = None
        assert Node.nodes.get(name) is None
        Node.nodes[self.name] = self

    def setName(self, nm):
        del Node.nodes[self.name]
        self.name = nm
        Node.nodes[self.name] = self

        
    """ retrieves """
    @classmethod
    def getNode(cls, name):
        nd = Node.nodes.get(name)
        if not nd is None:
            assert isinstance(nd, cls)
            return nd
        return None


    def addEdge(self, tgt=None, edgClass=None, fwd=True, strt=None, nd=None):
        tmp = edgClass(self, target=tgt, forward=fwd, end=nd, start=strt)
        assert not self is tgt
        self.edges.append(tmp)
        if not tgt is None:
            tgt.edges.append(tmp)
        return tmp

    # returns list (possibly empty) of edges of given class.
    def getEdges(self, edgClass):
        rv = []
        for edge in self.edges:
            if edge.__class__ is edgClass:
                rv.append(edge)
        return rv

    def ancestors(self, edgClass, stopNodeClass, forward=True):
        val = [self]
        for e in self.edges:
            if e.__class__ is edgClass:
                if e.edge[0] is self:
                    parent = e.edge[1]
                else:
                    parent = e.edge[0]
                if parent.__class__ is stopNodeClass:
                    val.append(parent)
                    return val
                else:
                    val += parent.ancestors(edgClass, stopNodeClass)
                break
        return val


    def __str__(self):
        rv = str(vars(self)) + str(self.birth)
        return rv

    def where(self, when=NOW):...

    def step(self, until=NOW+1):
        ...


Node.nodes = {}
Node.indx = 0

if __name__ == '__main__':
    nd = Node("test", None)
    nd1 = Node("test1", None)
    edge = nd >> nd1
    pprint(str(edge))
    pprint(str(nd))
