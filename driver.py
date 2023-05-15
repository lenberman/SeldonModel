#!/usr/bin/python3
import sys
from econosphere import *
import pdb; pdb.set_trace()


if __name__ == '__main__':
    wrld = World(2)
    nations = {}
    nations[0] = wrld.getNation(6)
    nations[1] = wrld.getNation(6)
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
