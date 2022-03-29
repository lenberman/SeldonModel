#!/usr/bin/python3
import random
import statistics
import math
import sys


now = 0


class location:  # space time chunk starting now
    locs = {}

    def __init__(self, t=now, i=None, j=None, k=None):
        val = (t, i, j, k)
        try:
            val = location.locs[val]
        except KeyError:
            location.locs[val] = val
            val


class node:   # # node in Seldon decomposition
    indx = 0

    def _init__(self):  # # any node may have lifetime
        # increment then stor
        node.indx += 1
        self.nId = node.indx


#  directed  edges with (multi-dimsensional) capacity and adjustable delay.
class edg(node):
    def __init__(self, capacity, src=None, tgt=None, lifetime=(now, now+1)):
        node.__init__(self)
        self.edge = [src, tgt]
        self.lifetime = lifetime
        self.capacity = capacity  # (useValue,capacity,unit cost)


class gNode(node):  # Geometrical nodes.  Override
    gVerse = {}

    def __init__(self,
                 loc1,  # simple connected region.  Perhaps a slice
                 loc2=None):  # perhaps  a  lifetime
        self.loc1 = loc1
        self.loc2 = loc2


class iNode(node):  # iNodes are controlled by sNodes (state nodes)class iNode:
    INFO_TYPES = ["nPerson",
                  "cPerson",
                  "lGov",
                  "state",  # # model constraints
                  "nation",  # # biologically derived identity. force
                  "health",
                  "military",
                  "technology",
                  "commodity",
                  "fCapital",
                  "mCapital",
                  "eCapital",
                  "bCapitcal"]

    # govt = getState(self, name, spaceTime=(location(now)))

    def __init__(self, name, info, technology=None):
        node.__init__(self)
        self.name = name
        self.info = info
        self.technology = technology

    def setOwner(self, owner):
        self.owner = owner


class technology(iNode):   # # scale factors for interaction modes 
    def __init__(self, name, info):
        iNode.__init__(self, name, info)
        self.factor = {}   # # scale factors for interaction modes 


class corp(iNode):
    def __init__(self, name, info, loc, capital=None):
        iNode.__init__(self, name, info, capital)
        self.capital = capital


class value(iNode):
    gifts = location(0)

    def __init__(self, name, useV, owner=None):
            iNode.__init__(self, name, (useV, owner))

    def useValue(self):
        self.info

    def price(self, valorand=None):
        pass

