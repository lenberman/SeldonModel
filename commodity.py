#!/usr/bin/python3
from econosphere import *


class capital:
    def __init__(self, cap):  # # capital or Transformation of capital as 2 vectors of length 5
        self.capital = cap  # # (cf, cm, cphys, celec, cbio)
        # # fixed/units  money phys elec bio 


# commodities may be owned,
#        factories have locations, processes do not
class commodity(value):
    def __init__(self, useV,
                 cv,  # # c/v: organic composition of commodity. capital/labor at locA.
                 rt,  # # realization time
                 locA=(now),
                 owner=None,
                 capital=None):
        value.__init__(self, useV, owner)
        self.owner = owner
        self.capital = capital  # # (cf, cm, cphys, celec, cbio)
        self.locA = locA
        self.cv = cv
        self.rt = rt

    def getOwner(self):
        self.owner

    def exchange(self, other):
        o1 = self.owner
        self.owner = other.owner
        other.owner = o1

        # next realize produces out-edges from commodity node, sources of commodities 
    def instantiate(self,
                    loc,  labor,  # must have location and labor
                    parts=None,
                    amt=1):
        edg(amt, self, None, (now, now+self.rt))  # return out edge

        # next  produce & connect out-edge(s) from commodity node
    def transport(self,
                  loc,
                  owner=None,  # #default don't change owner
                  amt=None):  # #default : ALL
        if owner is not None:
            self.owner = owner
        edg(amt, self)  # return out edge


class Market(iNode, gNode):
    def __init__(self):
        self.xchange = {}

    def addUseV(self, useV, price=None):  # price $|useValue
        1


