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
    max_node = None
    betweenness = nx.betweenness_centrality(graph)
    max_node = max(betweenness.items(), key=operator.itemgetter(1))[0]
    if max_node:
        return max_node
    return None

#Function that returns the node with maximum degree
def degree_attack(graph):
    max_node = None
    max_degree = max(dict(graph.out_degree()).values())
    max_node = list(dict(graph.out_degree()).keys())[max_degree]
    if max_node:
        return max_node
    return None

#Function that returns the node with maximum pagerank value
def max_pagerank(graph):
    max_node = None
    pagerank = nx.pagerank(graph, max_iter = 7000, weight = "weight")
    max_node = max(pagerank.items(), key=operator.itemgetter(1))[0]
    if max_node:
        return max_node
    return None

def max_closeness_centrality(graph):
    max_node = None
    closeness = nx.closeness_centrality(graph)
    max_node = max(closeness.items(), key=operator.itemgetter(1))[0]
    if max_node:
        return max_node
    return None

def eigenvector_centrality(graph):
    max_node = None
    eigenvector = nx.eigenvector_centrality(graph, max_iter=7000)
    max_node = max(eigenvector.items(), key=operator.itemgetter(1))[0]
    if max_node:
        return max_node
    return None

def nodes_closeness(graph):
    max_node = None
    max_node = max_closeness_centrality(graph)
    if max_node:
        return max_node
    return None

def weighted_node(graph):
    max_sum = 0
    max_node = None
    for node in graph.nodes:
        weight_sum = 0
        for neighbor in graph.neighbors(node):
            weight_sum += graph[node][neighbor]["weight"]
        if weight_sum >= max_sum:
            max_sum = weight_sum
            max_node = node
    if max_node:
        return max_node
    return None
    
def attack_nodes(mode, darkweb2, subgraph):
    if mode == 0:
        node_to_remove = max_betweenness_centrality(subgraph)
    elif mode == 1:
        node_to_remove = degree_attack(subgraph)
    elif mode == 2:
        node_to_remove = max_pagerank(subgraph)
    elif mode == 3:
        node_to_remove = max_closeness_centrality(subgraph)
    elif mode == 4:
        node_to_remove = eigenvector_centrality(subgraph)
    elif mode == 5:
        node_to_remove = weighted_node(subgraph)
    if node_to_remove:
        darkweb2.remove_node(node_to_remove)
        subgraph.remove_node(node_to_remove)
        return 1
    return 0


def weighted_neighbor(graph, node, node_list):
    neighbor = None
    max_weight = 0
    for nb in graph.neighbors(node):
        if nb not in node_list:
            if graph[node][nb]["weight"] > max_weight:
                max_weight = graph[node][nb]["weight"]
                neighbor = nb
    if neighbor:
        return neighbor
    else:
        nodes = list(graph.neighbors(node))
        random_nb = random.choice(nodes)
        return random_nb

def weighted_subgraph(graph):
    nodes = list(graph.nodes)
    random_node = random.choice(nodes)
    subgraph_nodes = [random_node]
    while len(subgraph_nodes)/len(nodes) < 0.10:
        random_node = weighted_neighbor(graph, random_node, subgraph_nodes)
        if random_node not in subgraph_nodes:
            subgraph_nodes.append(random_node)
    subgraph = graph.subgraph(subgraph_nodes)
    return subgraph

#Function that makes a subgraph starting from a specified number of nodes, that covers at most a specified percentage of the original graph
def make_subgraph(G, n_nodes=5, p=10, debug=False, seed=4):
    #Note: params for >10% of graph covered: n_nodes=5, p=10, seed=4
    random.seed(seed)
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
# print("Please select number of steps:")
# steps = int(input())

for _ in range(10):
    xList2 = []
    yList2 = []
    darkweb2 = darkweb.copy()
    DarkSubgraph = weighted_subgraph(darkweb2.to_undirected()).copy()
    i = 0
    start_time = time.time()
    mid_time = start_time
    ok = 1
    while i < 300 and mid_time-start_time < 300 and ok:
        ok = attack_nodes(5, darkweb2, DarkSubgraph)
        mid_time = time.time()
        i += 1
        darkweb_undirected = darkweb2.to_undirected()
        largest_cc = round(len(max(nx.connected_components(darkweb_undirected), key=len)) / len(darkweb2.nodes) * 100, 3)
        yList2.append(largest_cc)
        xList2.append(i)
    print(f"The largest connected component has {str(largest_cc)}% of the nodes in it")
    print(_)
    print("It took " + str(i) + " steps.")
    # yList.append(yList2)
    print("And " + str(round(mid_time-start_time)) + " seconds.")
    # xList.append(xList2)
    plt.plot(xList2, yList2, label = f"Seed {_}")
    

plt.xlim([0,300])
plt.xlabel("Steps")
plt.ylabel("Percentage")
plt.title("Differences Between Attack Strategies")
plt.legend(loc = 'best')
plt.show()
end_time = time.time()
#Print number of connected components in the graph
print(nx.number_connected_components(darkweb_undirected), f"Total time of execution is {round(end_time - start_time, 3)} seconds")
