#!/usr/bin/python3
import random
import statistics
import math
import sys
#import ipdb
#ipdb.set_trace()

locs = {}


class node:
    indx = 0

    def _init__(self, name=None):
        # increment then stor
        node.indx += 1
        self.nId = node.indx


#  directed  edges with (multi-dimsensional) capacity
class edg:
    def __init__(self, capacity, src=None, tgt=None, delay=None):
        self.edge = [src, tgt]
        self.capacity = capacity
        self.delay = delay


class location:

    def __init__(self, t, i=None, j=None, k=None):
        val = (t, i, j, k)
        try:
            val = locs[val]
        except KeyError:
            locs[val] = val
            val


class gNode(node):  # Geometrical nodes.  Override
    gVerse = {}

    def __init__(self,
                 loc1,  # simple connected region.  Perhaps a point
                 loc2=None):  # perhaps  a  lifetime
        self.loc1 = loc1
        self.loc2 = loc2


class iNode(node):  # iNodes are controlled by sNodes (state nodes)class iNode:
    INFO_TYPES = ["nPerson", "cPerson", "lGov", "sGov", "nGov",
                  "health", "military",
                  "commodity", "BUS", "CAR", "CARRIAGE", "PLATFORM",
                  "BUSSTOP",  "ELEVATOR", "STAIRWAY", "STREET", "COMPOSITE"]

    def __init__(self, info, encoding=None):
        self.info = info
        self.encoding = encoding


class corp(iNode):
    def __init__(self, loc, capital=None):
        self.capital = capital


class value(iNode):
    gifts = location(0)

    def __init__(self, useV):
        iNode.__init__(self, useV)

    def useValue(self):
        self.info

    def price(self, valorand=None):
        pass


# commodities may be owned,
#        factories have locations, processes do not
class commodity(value):
    def __init__(self, useV, locA=None, owner=None):
        value.__init__(self, useV, owner)
        self.owner = owner

    def getOwner(self):
        self.owner

        # next get out-edges from commodity node
    def produce(self,
                loc,  labor,  # must have location and labor
                parts=None,
                owner=None,
                amt=1):
        edg(amt, self)  # return out edge 


class labor(value):
    def __init__(self, concrete, period):
        value.__init_(self, concrete)
        self.period = period

        def createCommodity(self):   # by envisioning use
            pow(self.concrete, concrete)


class bNode(gNode, iNode):  # Biological nodes & selves
    def __init__(self, info, loc):
        gNode.__init__(self, loc)
        iNode.__init__(self, info)

    def compete(self, other):
        pass


class person(bNode, corp):  # Economic nodes &  selves
    def __init__(self, name, skills, loc, capital=None):
        bNode.__init__(self, skills, loc)
        corp.__init__(self, capital)

    def labor(self, period=None):
        [gNode(self) , 1]


class Market(iNode, gNode):
    def __init__(self):
        self.xchange = {}

    def addUseV(self, useV, price=None):  # price $|useValue
        1
