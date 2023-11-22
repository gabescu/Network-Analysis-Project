import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import operator
import time


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

#Function that returns the node with maximum betweenness centrality
def max_betweenness_centrality(graph):
    betweenness = nx.betweenness_centrality(graph)
    max_b = max(betweenness.items(), key=operator.itemgetter(1))[0]
    return max_b

#Function that returns the node with maximum degree
def degree_attack(graph):
    max_degree = max(dict(graph.out_degree()).values())
    max_degree_node = list(dict(graph.out_degree()).keys())[max_degree]
    return max_degree_node

#Function that returns the node with maximum pagerank value
def max_pagerank(graph):
    pagerank = nx.pagerank(graph, max_iter = 7000, weight = "weight")
    max_p = max(pagerank.items(), key=operator.itemgetter(1))[0]
    return max_p

def max_closeness_centrality(graph):
    closeness = nx.closeness_centrality(graph)
    max_c = max(closeness.items(), key=operator.itemgetter(1))[0]
    return max_c

def eigenvector_centrality(graph):
    eigenvector = nx.eigenvector_centrality(graph)
    max_e = max(eigenvector.items(), key=operator.itemgetter(1))[0]
    return max_e

def nodes_closeness(graph):
    max_centrality_node = max_closeness_centrality(graph)
    return max_centrality_node

def weighted_node(graph):
    max_sum = 0
    for node in graph.nodes:
        weight_sum = 0
        for neighbor in graph.neighbors(node):
            weight_sum += graph[node][neighbor]["weight"]
        if weight_sum >= max_sum:
            max_sum = weight_sum
            max_node = node
    return max_node
    

#Function that removes the max degree node
def attack_nodes(graph):
    node_to_remove = weighted_node(graph)
    darkweb.remove_node(node_to_remove)

#Loop functions by steps times
print("Please select number of steps:")
steps = int(input())
darkweb_undirected = darkweb.to_undirected()
i = 0
start_time = time.time()
while i < steps:
    attack_nodes(darkweb)
    darkweb_undirected = darkweb.to_undirected()
    largest_cc = round(len(max(nx.connected_components(darkweb_undirected), key=len)) / len(darkweb.nodes) * 100, 3)  
    print(f"The largest connected component has {str(largest_cc)}% of the nodes in it")
    i += 1

end_time = time.time()
#Print number of connected components in the graph
print(nx.number_connected_components(darkweb_undirected), f"Total time of execution is {round(end_time - start_time, 3)} seconds")
