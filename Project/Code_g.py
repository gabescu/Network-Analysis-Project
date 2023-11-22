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

#Function that makes a subgraph starting from a specified number of nodes, that covers at most a specified percentage of the original graph
def make_subgraph(G, n_nodes=1, p=20, debug=False):

    nodes = list(G.nodes)
    N = len(nodes)
    subgraph_nodes = []
    if debug:
        print(f"Making subgraph starting from {n_nodes} nodes, taking {p}% of the total nodes from their neighbourhood")

    for node in range(n_nodes):

        if debug:
            print(f"---Iteration  = {node}")
        n_count = 0
        start_node = random.choice(nodes)
        if debug:
            print(f"Starting at node: {start_node}")
        subgraph_nodes.append(start_node)
        curr_node = start_node
        curr_neighbors = list(G.neighbors(curr_node))
        if debug:
            print(f"Neighbours of starting node: {curr_neighbors}")
        idx = 0

        while n_count < (p/100 * N):

            if idx == len(subgraph_nodes) and curr_neighbors in subgraph_nodes:
                if debug:
                    print(f"There are no more edges to follow, stopping")
                break

            if len(curr_neighbors) == 0:
                if debug:
                    print(f"Current node is dangling")
                if idx + 1 >= len(subgraph_nodes):
                    if debug:
                        print(f"There are no more edges to follow, stopping")
                    break

                idx += 1
                if debug:
                    print(f"Taking node at idx {idx}")
                curr_node = subgraph_nodes[idx]
                curr_neighbors = list(G.neighbors(curr_node))
                if debug:
                    print(f"Curr node = {curr_node}, neighbors: ")
                    print(curr_neighbors)
                continue

            for neighbor in curr_neighbors:
                
                if neighbor not in subgraph_nodes:
                    subgraph_nodes.append(neighbor)
                    n_count += 1

                if n_count >= (p/100 * N):
                    break
            
            if debug:
                print(f"Added current neighbors, new subgraph nodes list is")
                print(subgraph_nodes)
            
            if idx >= len(subgraph_nodes):
                if debug:
                    print(f"There are no more edges to follow, stopping")
                break

            curr_node = subgraph_nodes[idx]
            idx += 1
            if debug:
                print(f"Taking node at idx {idx}")
            curr_neighbors = list(G.neighbors(curr_node))
            if idx == len(subgraph_nodes) and curr_neighbors in subgraph_nodes:
                if debug:
                    print(f"There are no more edges to follow, stopping")
                break
            if debug:
                print(f"Curr node = {curr_node}, neighbors: ")
                print(curr_neighbors)

    G_subgraph = G.subgraph(subgraph_nodes)
    if debug:
        print(f"Final node list:")
        print(subgraph_nodes)
        print(f"Made a subgraph with {len(G_subgraph)} nodes")
    return G_subgraph

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
