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
random_node = "wikipediak4by6wf"

taken_down = {}
infected_neighbors = {}
for node in darkweb:
    if node == random_node:
        taken_down[node] = True  
        infected_neighbors = 0
    else:
        taken_down[node] = False
        infected_neighbors = 0
        
nx.set_node_attributes(darkweb, taken_down, "taken_down")
nx.set_node_attributes(darkweb, infected_neighbors, "infected_neighbors")

def break_nodes(graph):
    x = 0
    for node in graph:
        if graph.nodes[node]["taken_down"] == True and graph.nodes[node]["infected_neighbors"] != len(graph[node]):
            graph.nodes[list(darkweb[node].keys())[graph.nodes[node]["infected_neighbors"]]]["taken_down"] = True
            graph.nodes[node]["infected_neighbors"] += 1
            return
            
for _ in range(0, 100):
    break_nodes(darkweb)
    
i = 0
for node in darkweb:
    if darkweb.nodes[node]["taken_down"] == True:
        print(node)
        i += 1
        print(i)