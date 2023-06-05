#!/usr/bin/python3
import sys
#from econosphere import *
from market import *
import matplotlib as mpl
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
                        5 : "Medium-of-Exchange", 6 : "Labor",  7 : "Food",  8 : "Housing"  ,
                        9 : "Genes", 10: "Land"})

    human = cNode(name="Worker", owner=wrld, uvI_O={"Food" : -1 , "Labor" : 1})
    farm = cNode(name="Farm", owner=wrld, uvI_O={"Labor" : -1, "Food" : 1})
    print(str(vars(institution)))
    print(str(vars(human)))
    #miZList1 = subGov[2] << miZList
    #commercialNode = miZList[0] << miZList[1:]
    #foofoo =map(lambda obj: iNode.iZygote(obj), foo)
    #iZList = list() 
    #for i in nList + zList:
    #print(str(i))
    #for i in nList + zList:
    #print(str(vars(i)))

    Node.nodes = {}
    Node.indx = 0
    
"""



    money = UseValue("medium-of-exchange")
    power = UseValue("power")
    fear = UseValue("fear")
    print(money)
"""
