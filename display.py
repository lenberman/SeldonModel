#!/usr/bin/python3
from market import *
import os
import subprocess
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx


G=nx.MultiDiGraph()

wrld = World(g=G)
zList = wrld >> ("Alice", "Bob", "Carol", "Dylan")  # returns list of zygotes
miZList = list(map(lambda obj: iNode.iZygote(obj,wrld), zList))
nList = wrld << ("USA", "China", "Russia", "Ukraine") # returns list of nations
usa = nList[0]
subGov = usa >> ("NY","CA","TX")
subGov[0] << miZList    # make iZygotes citizen of NY
wrld.geometrize()
institution = Institution(govList=nList,nm="WorldBank")
nyInstitution = Institution(govList=subGov, nm="PATH")

UseValue.resetUV(uvList= {  0 : "Fear",  1 : "Power",
                            2 : "Friendship",  3 : "Loyalty",  4 : "Love",
                            5 : "$$$", 6 : "Labor",  7 : "Food",  8 : "Housing"  ,
                            9 : "Genes", 10: "Land"})
### We illustrate a couple of derived UseValues.
laborer = UseValue(name="Laborer", uVector=[("Food" , -1) , ("Housing",-1), ("Labor", 1)])
farm = UseValue(name="Farm", uVector=[("Labor", -1), ("Food", 1),("Land", 1),("$$$", -.1)])
### The model (World) uses
### (1) the laborer UseValue to initialize the possessions of each iZygote and
### (2) the farm UseValue to illustrate an enterprise which transforms labor and $$$s 
worker = cNode(name="Worker", owner=wrld, uv=laborer, factory=True, saleable=False)
farmer = cNode(name="Farm", owner=wrld, uv=farm, factory=True, saleable=True)
moneySupply = cNode(name="u$a", owner=usa, uv=UseValue.UV("$$$"),
                    factory=False, saleable=False)
usa_mkt = Market(money=moneySupply, govList=[usa])

workerNeeded = Offer(who=miZList[0], itemList=UseValue.UV("Labor"), transWhere="*",
                     transWhen="7", offer=False, price=2, until="@14*13")
usa_mkt.submit(offer=workerNeeded)

# create display
nodeColor = []
for node in G.nodes():
    cls = Node.nodes[node].__class__
    G.nodes[node] ["color"] =  Node.nodeColors[cls]
    G.nodes[node] ["style"] =  Node.nodeStyle[cls]
    G.nodes[node] ["penwidth"] =  3.0
    nodeColor.append(Node.nodeColors[cls])

edgeColor = []
for edge in G.edges():
    edgeData = G.get_edge_data(edge[0],edge[1])
    for data in edgeData.items():# key is first element of data
        edgeColor.append(Edge.edgeColors[data[0]])
        G.edges[edge[0],edge[1], data[0]]["color"] = Edge.edgeColors[data[0]]
        G.edges[edge[0],edge[1], data[0]]["style"] = Edge.edgeStyles[data[0]]
        G.edges[edge[0],edge[1], data[0]]["penwidth"] = 3.0

# Need to create a layout when doing separate calls to draw nodes and edges
pos=nx.planar_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), linewidths=2.0, node_shape='o',
                       node_color = nodeColor,  node_size=3000)
nx.draw_networkx_labels(G, pos, font_size=24)
nx.draw_networkx_edges(G, pos, edge_color=edgeColor, width=3, style="dotted",
                       arrows=True, arrowsize=30, node_size=3000)
nx.nx_agraph.write_dot(G,"multi.dot")
#dot -T png multi.dot > multi.png  or #cat multi.dot | dot -T png > multi.dot.png
os.system("cat multi.dot | dot -T png > multi.dot.png")
subprocess.run(["firefox", "multi.dot.png"])
plt.show()


