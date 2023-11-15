import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

inp = open("darkweb-edges.csv")
edges = []
for row in inp:
    row = row.split(",")
    edge = [row[0], row[1], int(row[2])]
    edges.append(edge)
inp.close()

darkweb = nx.DiGraph()
darkweb.add_weighted_edges_from(edges)
nr_nodes = len(darkweb.nodes)

def attack_nodes(graph):
    max_degree = max(dict(darkweb.out_degree()).values())
    max_degree_node = list(dict(darkweb.out_degree()).keys())[max_degree]
    darkweb.remove_node(max_degree_node)

darkweb_undirected = darkweb.to_undirected()


i = 0
while i < 1830:
    darkweb_undirected = darkweb.to_undirected()
    attack_nodes(darkweb.degree())
    i += 1
    
darkweb_undirected = darkweb.to_undirected()
print(i, nx.number_connected_components(darkweb_undirected))
    