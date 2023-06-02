#!/usr/bin/python3
from econosphere import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

G=nx.MultiDiGraph()

nodeTypeColor = { "iNode" : .20 , "bNode" : .40, "Government" : .6, "Institution": .8 }

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
                  
nodeColor = []
for node in G.nodes():
    if node.__class__ is World:
        nodeColor.append(.84)
    elif node.__class__ is Government:
        nodeColor.append(.66)
    elif node.__class__ is Institution:
        nodeColor.append(.50)
    elif node.__class__ is iNode:
        nodeColor.append(.33)
    elif node.__class__ is bNode:
        nodeColor.append(.16)

edgeColor = []
edgeClsDict =nx.get_edge_attributes(G,"cls")
for edge in G.edges():
    cls = edgeClsDict[(edge[0],edge[1],0)]
    if cls is Inclusion:
        edgeColor.append(.84)
    elif cls is Meiotic:
        edgeColor.append(.66)
    elif cls is Mitotic:
        edgeColor.append(.50)
    elif cls is Agreement:
        edgeColor.append(.33)


#values = [val_map.get(node, 0.25) for node in G.nodes()]

# Specify the edges you want here
red_edges = [('A', 'C'), ('E', 'C')]
edge_colours = ['black' if not edge in red_edges else 'red'
                for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]


# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
                       node_color = nodeColor, node_size = 500)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edge_color=edgeColor, arrows=True)
plt.show()

pos = nx.spring_layout(G, seed=63)  # Seed layout for reproducibility
colors = range()
options = {
    "node_color": "#A0CBE2",
    "edge_color": colors,
    "width": 4,
    "edge_cmap": plt.cm.Blues,
    "with_labels": False,
}
nx.draw(G, pos, **options)
plt.show()
"""
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(1, 5)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)

# explicitly set positions
pos = {1: (0, 0), 2: (-1, 0.3), 3: (2, 0.17), 4: (4, 0.255), 5: (5, 0.03)}
"""
options = {
    "font_size": 36,
    "node_size": 3000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 5,
    "width": 5,
}

nx.draw_networkx(G, pos, **options)

# Set margins for the axes so that nodes aren't clipped
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()

G = nx.complete_graph(5)
#write_gml(G, "./path.to.file")
nx.draw(G)


G = nx.DiGraph()
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
