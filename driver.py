#!/usr/bin/python3
import sys
from econosphere import *
##import pdb; pdb.set_trace()


if __name__ == '__main__':
    wrld = World(2)
    nList = wrld << (("USA", 6), ("China", 6))
    zList = wrld >> ("Alice", "Bob")
    iZList = list()
    for z in zList:
        iz = iNode.iZygote(z)
        iZList.append(iz)
        print(str(vars(iz)))


    for i in nList + pList:
        print(str(i))
    for i in nList + pList:
        print(str(vars(i)))

"""
    nations = {}
    nations[0] = wrld.getNation(6,"USA")
    nations[1] = wrld.getNation(6, "China")
    institution = Government.getInsitution(nations, "Fed")
    subgov = nations[0].getSubGov(3)
    print(str(wrld))
    alice = bNode.zygote("Alice")
    bob = bNode.zygote("Bob")
    carol = bNode.zygote("Carol")
    david = bNode.zygote("David")
    print(alice is bNode.zygote("Alice"))
    print(str(subgov))
    ev = Event()
    print(ev)
    money = UseValue("medium-of-exchange")
    power = UseValue("power")
    fear = UseValue("fear")
    print(money)
"""
