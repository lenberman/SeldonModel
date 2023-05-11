#!/usr/bin/python3
import sys
from econosphere import *


if __name__ == '__main__':
    wrld = World(2)
    reg = wrld.getRegion(12)
    print(str(wrld))
    print(str(reg))
    z0 = bNode.zygote("Alice")
    z1 = bNode.zygote("Bob")
    z2 = bNode.zygote("Carol")
    z3 = bNode.zygote("David")
    print(z0 is bNode.zygote("Alice"))
    ev = Event()
    print(ev)
    money = UseValue("medium-of-exchange")
    print(money)
