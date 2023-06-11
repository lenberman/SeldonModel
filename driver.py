#!/usr/bin/python3
import sys
#from econosphere import *
from market import *
#import pdb; pdb.set_trace()
import pdb
#pdb.set_trace()

if __name__ == '__main__':
    G=nx.MultiDiGraph()
    wrld = World(g=G)
    zList = wrld >> ("Alice", "Bob", "Carol", "Dylan")  # returns list of zygotes
    miZList = list(map(lambda obj: iNode.iZygote(obj,wrld), zList)) # iZygotes
    nList = wrld << ("USA", "China", "Russia", "Ukraine") # returns list of nations
    usa = nList[0]
    subGov = usa >> ("NY","CA","TX")
    subGov[0] << miZList    # make iZygotes citizen of NY
    wrld.geometrize()
    institution = Institution(govList=nList, nm="WorldBank")
    nyInstitution = Institution(govList=subGov, nm="PATH")
    UseValue.resetUV(uvList= {  0 : "Fear",  1 : "Power",
                        2 : "Friendship",  3 : "Loyalty",  4 : "Love",
                        5 : "$$$", 6 : "Labor",  7 : "Food",  8 : "Housing"  ,
                        9 : "Genes", 10: "Land"})

    tStrip = Offer(who=subGov[0], itemList=UseValue.UV("$$$"), transWhere="*", offer=True, price="1", until="@10*10")
    tBills = []
    for i in range(1,10):
        tBill = Offer(who=subGov[0], itemList=UseValue.UV("$$$"), transWhere="*", offer=True, price="1", until="@"+str(i)+"0")
        tBills.append(tBill)

    pdb.set_trace()
    Node.nodes = {}
    Node.indx = 0
    
"""



    money = UseValue("medium-of-exchange")
    power = UseValue("power")
    fear = UseValue("fear")
    print(money)
"""
