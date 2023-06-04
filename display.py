#!/usr/bin/python3
from econosphere import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot

G=nx.MultiDiGraph()

wrld = World(g=G)
zList = wrld >> ("Alice", "Bob", "Carol", "Dylan")  # returns list of zygotes
miZList = list(map(lambda obj: iNode.iZygote(obj,wrld), zList))
nList = wrld << ("USA", "China", "Russia", "Ukraine") # returns list of nations
usa = nList[0]
subGov = usa >> ("NY","CA","TX")
subGov[0] << miZList    # make iZygotes citizen of NY
wrld.geometrize()
institution = Institution(nList, "WorldBank")
nyInstitution = Institution(subGov, "PATH")

#for node in G.nodes():

nodeColorValues = {}
nodeColor = []
for node in G.nodes():
    cls = Node.nodes[node].__class__
    G.nodes[node] ["color"] =  Node.nodeColors[cls]
    G.nodes[node] ["penwidth"] =  3.0
    #nodeColorValues[Node.nodes[node]] = { "color" :  Node.nodeColors[cls] }
    nodeColor.append(Node.nodeColors[cls])

edgeColor = []
edgeColorValues = {}
edgeClsDict =nx.get_edge_attributes(G,"cls")
for edge in G.edges():
    edgeData = G.get_edge_data(edge[0],edge[1])
    for data in edgeData.items():# key is first element of data
        edgeColor.append(Edge.edgeColors[data[0]])
        G.edges[edge[0],edge[1], data[0]]["color"] = Edge.edgeColors[data[0]]
        G.edges[edge[0],edge[1], data[0]]["penwidth"] = 3.0
        #edgeColorValues[(edge[0],edge[1], data[0])] = { "color" : Edge.edgeColors[data[0]] }

#G.set_edge_attributes(edgeColorValues)
#G.set_node_attributes(nodeColorValues)

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
pos=nx.planar_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), linewidths=2.0, node_shape='o',
                       node_color = nodeColor, edge_colors="azure",  node_size=3000)
nx.draw_networkx_labels(G, pos, font_size=24)
nx.draw_networkx_edges(G, pos, edge_color=edgeColor, width=3, style="_", arrows=True, arrowsize=30, node_size=3000)
write_dot(G,"multi.dot")
#neato -T png multi.dot > multi.png
#A = nx.nx_agraph.to_agraph(G)
plt.show()

exit(0)
options = {
    "font_size": 36,
    "node_size": 3000,
    "node_color": "orange",
    "edgecolors": "blue",
    "linewidths": 5,
    "width": 5,
}

nx.draw_networkx(G, pos, **options)

# Set margins for the axes so that nodes aren't clipped
ax = plt.gca()
ax.margins(0.80)
plt.axis("on")
plt.show()

#G = nx.complete_graph(5)
#write_gml(G, "./path.to.file")
nx.draw(G)


#G = nx.DiGraph()
G.add_node(1)
G.add_nodes_from([2, 3],color="red")
#G.add_edge(1, 2)
#G.add_nodes_from(range(100, 110))
#H = nx.path_graph(10)
#G.add_nodes_from(H)  color="red" ?
G.add_edges_from([(1, 2, {"color": "blue"}), (1, 3)])


seed = 13648  # Seed random number generators for reproducibility
G = nx.random_k_out_graph(10, 3, 0.5, seed=seed)
pos = nx.spring_layout(G, seed=seed)

node_sizes = [3 + 10 * i for i in range(len(G))]
M = G.number_of_edges()
edge_colors = range(2, M + 2)
edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
cmap = plt.cm.plasma

nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="indigo")
edges = nx.draw_networkx_edges(
    G,
    pos,
    node_size=node_sizes,
    arrowstyle="->",
    arrowsize=10,
    edge_color=edge_colors,
    edge_cmap=cmap,
    width=2,
)
# set alpha value for each edge
for i in range(M):
    edges[i].set_alpha(edge_alphas[i])

pc = mpl.collections.PatchCollection(edges, cmap=cmap)
pc.set_array(edge_colors)

ax = plt.gca()
ax.set_axis_off()
plt.colorbar(pc, ax=ax)
plt.show()
