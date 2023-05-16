#!/usr/bin/python3
from econosphere import *

# commodities may be owned, may be physical
#        factories have locations, processes do not
class commodity(value):
    money = None
    def __init__(self, useV,
                 cv,  # # c/v: organic composition of commodity. capital/labor at locA.
                 rt,  # # realization time
                 cs,  # # sensitivity to change in capital dCdM
                 locA=(now),
                 owner=None,
                 capital=None):
        value.__init__(self, useV, owner)
        self.capital = capital  # # (cf, cm, cphys, celec, cbio)
        self.locA = locA
        self.cv = cv  # # sensitivity to change in labor input dCdL
        self.rt = rt  # #
        self.dCdM = 0  # sensitivity to change in capital

    def getOwner(self):
        self.owner

        # # vector of values relative to other commodities.
    def exchange(self, other=money):
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

