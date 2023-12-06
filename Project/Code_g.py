import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import operator
import time


# Reading
inp = open("darkweb-edges.csv")
edges = []
for row in inp:
    row = row.split(",")
    edge = [row[0], row[1], int(row[2])]
    edges.append(edge)
inp.close()

# Creating the Directed Graphs
darkweb = nx.DiGraph()
darkweb.add_weighted_edges_from(edges)
nr_nodes = len(darkweb.nodes)

# Lists for the plot
yList = []
xList = []

# Function that returns the node with maximum betweenness centrality
def max_betweenness_centrality(graph):
    max_node = None
    betweenness = nx.betweenness_centrality(graph)
    max_node = max(betweenness.items(), key=operator.itemgetter(1))[0]
    if max_node:
        return max_node
    return None

# Function that returns the node with maximum degree
def degree_attack(graph):
    max_node = None
    max_degree = max(dict(graph.out_degree()).values())
    max_node = list(dict(graph.out_degree()).keys())[max_degree]
    if max_node:
        return max_node
    return None

# Function that returns the node with maximum pagerank value
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
    
def attack_nodes_subgraph(mode, darkweb2, subgraph):
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

def attack_nodes(mode, darkweb2):
    if mode == 0:
        largest_cc = max(nx.connected_components(darkweb2.to_undirected()), key=len)
        subgraph = darkweb2.subgraph(largest_cc)
        node_to_remove = max_betweenness_centrality(subgraph)
    elif mode == 1:
        node_to_remove = degree_attack(darkweb2)
    elif mode == 2:
        node_to_remove = max_pagerank(darkweb2)
    elif mode == 3:
        largest_cc = max(nx.connected_components(darkweb2.to_undirected()), key=len)
        subgraph = darkweb2.subgraph(largest_cc)
        node_to_remove = max_closeness_centrality(subgraph)
    elif mode == 4:
        node_to_remove = eigenvector_centrality(darkweb2)
    elif mode == 5:
        node_to_remove = weighted_node(darkweb2)
    if node_to_remove:
        darkweb2.remove_node(node_to_remove)
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

#Function to test splitting the node attacking only nodes in the subgraph
def test_subgraph(n, iter, darkweb2):

    #n = number of nodes to delete on each attack
    #iter = number of iterations to test for
    #OUTPUT FORMAT: list of tuples, where each tuple contains the percentage of the graph described by the largest connected component and the
    #number of connected components after the attack on that iteration
    delete_nodes = n
    data = []
    for i in range(iter):
        darkweb = darkweb2.copy() #reset graph on each iteration
        try:
            subgraph = make_subgraph(darkweb, 5, 10, False)
            #print(f"Subgraph has {len(subgraph)} nodes")
            for _ in range(delete_nodes):
                node_to_remove = weighted_node(subgraph)
                if node_to_remove == -1: #-1 is returned if a node with max weight can't be found, case in which we stop
                    break
                darkweb.remove_node(node_to_remove)

            darkweb_undirected = darkweb.to_undirected()
            largest_cc = round(len(max(nx.connected_components(darkweb_undirected), key=len)) / len(darkweb.nodes) * 100, 3)
            cc = len(max(nx.connected_components(darkweb_undirected), key=len))
            data.append((largest_cc, cc))
            #print(f"ITER {i}: {delete_nodes} iterations of weighted node attack | Split in {cc} components | largest componenent : {largest_cc}% of the network")
        except:
            print(f"Error at iteration {i}")
    return data

# Loop functions by steps times
# print("Please select number of steps:")
# steps = int(input())

def print_method(number):
    if number == 0:
        return "Betweenness Centrality"
    elif number == 1:
        return "Max Degree"
    elif number == 2:
        return "Pagerank"
    elif number == 3:
        return "Closeness Centrality"
    elif number == 4:
        return "Eigenvector Centrality"
    elif number == 5:
        return "Weighted Node"

for _ in range(6):
    xList2 = []
    yList2 = []
    darkweb2 = darkweb.copy()
    DarkSubgraph = weighted_subgraph(darkweb2.to_undirected()).copy()
    i = 0
    start_time = time.time()
    mid_time = start_time
    ok = 1
    while i < 800 and mid_time-start_time < 300 and ok:
        ok = attack_nodes(_, darkweb2)
        mid_time = time.time()
        i += 1
        darkweb_undirected = darkweb2.to_undirected()
        largest_cc = round(len(max(nx.connected_components(darkweb_undirected), key=len)) / len(darkweb2.nodes) * 100, 3)
        yList2.append(largest_cc)
        xList2.append(i)
    print(f"The largest connected component has {str(largest_cc)}% of the nodes in it")
    print(print_method(_))
    print("It took " + str(i) + " steps.")
    # yList.append(yList2)
    print("And " + str(round(mid_time-start_time)) + " seconds.")
    # xList.append(xList2)
    plt.plot(xList2, yList2, label = print_method(_))


    

plt.xlim([0,800])
plt.xlabel("Steps")
plt.ylabel("Percentage")
plt.title("Differences Between Attack Strategies")
plt.legend(loc = 'best')
plt.show()
end_time = time.time()
# Print number of connected components in the graph
print(nx.number_connected_components(darkweb_undirected), f"Total time of execution is {round(end_time - start_time, 3)} seconds")
