#!/usr/bin/python3
import sys
from econosphere import *
#import pdb; pdb.set_trace()
import pdbrc

if __name__ == '__main__':
    wrld = World(2)
    zList = wrld >> ("Alice", "Bob", "Carol", "Dylan")  # returns list of zygotes
    miZList = list(map(lambda obj: iNode.iZygote(obj), zList))
    nList = wrld << ("USA", "China") # returns list of nations
    usa = nList[1]
    subGov = usa >> ("NY","CA","TX")
    institution = Institution(nList, "WorldBank")
    print(str(vars(institution)))
    #miZList1 = subGov[2] << miZList
    #commercialNode = miZList[0] << miZList[1:]
    #foofoo =map(lambda obj: iNode.iZygote(obj), foo)
    iZList = list()
    for i in nList + zList:
        print(str(i))
    for i in nList + zList:
        print(str(vars(i)))

"""



    money = UseValue("medium-of-exchange")
    power = UseValue("power")
    fear = UseValue("fear")
    print(money)
"""
