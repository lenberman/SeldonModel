#!/usr/bin/python3
import sys
from econosphere import *
#import pdb; pdb.set_trace()
import pdbrc

if __name__ == '__main__':
    wrld = World(2)
    zList = wrld >> ("Alice", "Bob", "Carol", "Dylan")  # returns list of zygotes
    miZList = list(map(lambda obj: iNode.iZygote(obj), zList))
    miZList1 = subGov[2] << miZList
    commercialNode = miZList[0] << miZList[1:]
    #foofoo =map(lambda obj: iNode.iZygote(obj), foo)
    iZList = list()
    for z in zList:
        iz = iNode.iZygote(z)
        iZList.append(iz)
        print(str(vars(iz)))


    for i in nList + zList:
        print(str(i))
    for i in nList + zList:
        print(str(vars(i)))

"""
    nList = wrld << (("USA", 6), ("China", 6)) # returns list of nations
    usa = nList[1]
    subGov = usa >> ("NY","CA","TX")
    institution = Institution(nList, "WorldBank")
    print(str(vars(institution)))



    nations = {}
    nations[0] = wrld.getNation(6,"USA")
    nations[1] = wrld.getNation(6, "China")
    institution = Insitution(nations, "Fed")
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
