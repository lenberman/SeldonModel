#!/usr/bin/python3
from commodity import *


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


out1 = person("Len", location(), "skills")
