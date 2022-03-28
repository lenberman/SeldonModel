#!/usr/bin/python3
from econosphere import *


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
        self.capital = capital
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
        if owner is None:
            owner = self.owner
        edg(amt, self)  # return out edge


class bNode(gNode, iNode):  # Biological nodes & selves
    def __init__(self, name, info, loc):
        gNode.__init__(self, loc)
        iNode.__init__(self, name, info)

    def compete(self, other):
        pass


class person(bNode, corp):  # Economic nodes &  selves
    class labor(edg):
        def __init__(self, concrete, period):
            edg.__init_(self, concrete)
            self.period = period

            # #skills represents both genome and human skills
    def __init__(self, name, loc, skills=None, capital=None):
        bNode.__init__(self, name,skills, loc)
        corp.__init__(self, name, skills, capital)
        self.skills = skills

    def getLabor(self, start=0, duration=1):
        person.labor(self.skills, self, None, (now+start, now+start+duration))


class Market(iNode, gNode):
    def __init__(self):
        self.xchange = {}

    def addUseV(self, useV, price=None):  # price $|useValue
        1


out1 = person("Len", (0, 0, 0, 1), "skills")
