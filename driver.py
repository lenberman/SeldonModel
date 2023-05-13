#!/usr/bin/python3
import sys
from econosphere import *


if __name__ == '__main__':
    wrld = World(2)
    reg = wrld.getRegion(12)
    print(str(wrld))
    print(str(reg))
    subR = reg.getSubregion(3)
    print(str(subR))
    alice = bNode.zygote("Alice")
    bob = bNode.zygote("Bob")
    carol = bNode.zygote("Carol")
    david = bNode.zygote("David")
    print(alice is bNode.zygote("Alice"))
    
    ev = Event()
    print(ev)
    money = UseValue("medium-of-exchange")
    print(money)
