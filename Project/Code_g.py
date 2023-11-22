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

#Lists for the plot
yList = []
xList = []

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

#Function that returns the node with most weights
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

def eigenvector_centrality(graph):
    eigenvector = nx.eigenvector_centrality(graph, max_iter=7000)
    max_e = max(eigenvector.items(), key=operator.itemgetter(1))[0]
    return max_e

def attack_nodes_closeness():
    max_centrality_node = max_closeness_centrality(darkweb)
    darkweb.remove_node(max_centrality_node)

#Function that removes the max degree node
def attack_nodes(mode, darkweb2):
    if mode == 0:
        node_to_remove = max_betweenness_centrality(darkweb2)
    elif mode == 1:
        node_to_remove = degree_attack(darkweb2)
    elif mode == 2:
        node_to_remove = max_pagerank(darkweb2)
    elif mode == 3:
        node_to_remove = max_closeness_centrality(darkweb2)
    elif mode == 4:
        node_to_remove = eigenvector_centrality(darkweb2)
    elif mode == 5:
        node_to_remove = weighted_node(darkweb2)
    darkweb2.remove_node(node_to_remove)


#Loop functions by steps times
# print("Please select number of steps:")
# steps = int(input())
for _ in range(6):
    xList2 = []
    yList2 = []
    darkweb2 = darkweb.copy()
    i = 0
    start_time = time.time()
    mid_time = start_time
    while i < 800 and mid_time-start_time < 180:
        attack_nodes(_, darkweb2)
        mid_time = time.time()
        i += 1
        darkweb_undirected = darkweb2.to_undirected()
        largest_cc = round(len(max(nx.connected_components(darkweb_undirected), key=len)) / len(darkweb2.nodes) * 100, 3)
        yList2.append(largest_cc)
        xList2.append(round(mid_time-start_time))
    print(f"The largest connected component has {str(largest_cc)}% of the nodes in it")
    print(_)
    print("It took " + str(i) + " steps.")
    # yList.append(yList2)
    print("And " + str(round(mid_time-start_time)) + " seconds.")
    # xList.append(xList2)
    plt.plot(xList2, yList2, label = "id %s"%_)
    

plt.xlim([0,200])
plt.xlabel("Time")
plt.ylabel("Percentage")
plt.title("Differences Between Attack Strategies")
plt.show()
end_time = time.time()
#Print number of connected components in the graph
print(nx.number_connected_components(darkweb_undirected), f"Total time of execution is {round(end_time - start_time, 3)} seconds")
