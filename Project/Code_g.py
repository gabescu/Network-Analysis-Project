import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import operator


#Reading
inp = open("darkweb-edges.csv")
edges = []
for row in inp:
    row = row.split(",")
    edge = [row[0], row[1], int(row[2])]
    edges.append(edge)
inp.close()

#Creating the Directed Graphs
darkweb = nx.DiGraph()
darkweb.add_weighted_edges_from(edges)
nr_nodes = len(darkweb.nodes)

#Function that returnes the node with maximum betweenness centrality
def max_betweenness_centrality(graph):
    betweenness = nx.betweenness_centrality(graph)
    max_b = max(betweenness.items(), key=operator.itemgetter(1))[0]
    return max_b

#Function that returnes the node with maximum degree
def degree_attack(graph):
    max_degree = max(dict(darkweb.out_degree()).values())
    max_degree_node = list(dict(darkweb.out_degree()).keys())[max_degree]
    return max_degree_node

#Function that returns the node with maximum pagerank value
def max_pagerank(graph):
    pagerank = nx.pagerank(graph, max_iter = 1000, weight = "weight")
    max_p = max(pagerank.items(), key=operator.itemgetter(1))[0]
    return max_p

#Function that removes the node
def attack_nodes():
    node_to_remove = max_betweenness_centrality(darkweb)
    darkweb.remove_node(node_to_remove)

#Loop functions by steps times
print("Please select number of steps:")
steps = int(input())
darkweb_undirected = darkweb.to_undirected()
i = 0
while i < steps:
    attack_nodes()
    darkweb_undirected = darkweb.to_undirected()
    i += 1

#Print number of connected components in the graph
print(nx.number_connected_components(darkweb_undirected))
    