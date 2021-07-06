"""
Henry Manley - hjm67@cornell.edu

Simulates imperfect treatment effects created by node connectedness. Given an
undirected graph G = {V,E}, what can we learn about the underlying network from
sampling?
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random

def randomGraph(n: int, s: int, c: int):
    """
    Returns s complete graphs connected by c edges. This simulation models
    imperfect treatment across samples (particularly when s = 2).

    @param n is the number of nodes in each sample
    @param s is the number of samples
    @param c in the number of randomly connected nodes between each sample in s
    """

    graphs = []
    for i in range(s):
        g = nx.complete_graph(n)
        graphs.append(g)

    G = graphs[0]
    for j in range(1, len(graphs)):
        fromNodes = list(G.nodes)
        maxNode = max(fromNodes)
        g = nx.relabel_nodes(graphs[j], lambda x: x + maxNode + 1)

        toNodes = list(g.nodes)
        fromList = random.sample(fromNodes, c)
        toList = random.sample(toNodes, c)

        G = nx.compose(G, g)

        for i in range(len(toList)):
            G.add_edge(fromNodes[i], toNodes[i])

    return G


def sample(G, n: int):
    """
    Return the reverse-engineered graph G1. G1 is created by sampling n nodes
    from graph G, which is the collection of complete graphs each connected by some
    constant number of edges.

    @param G is the graph object to sample and reverse engineer
    @param n is the number of nodes to sample from G
    """
    allNodes = list(G.nodes)
    sampleNodes = random.sample(allNodes, n)

    G1 = nx.Graph()
    G1.add_nodes_from(sampleNodes)
    for node in sampleNodes:
        sampleEdges = list(G.edges(node))
        G1.add_edges_from(sampleEdges)
    return G1


def drawGraph(G):
    """
    Draws graph object G to window.

    @param G is the graph object to be drawn
    """
    nx.draw(G, node_size = 30,  with_labels=True)
    plt.show()


def simulate(S: int, N: int, C: int, K: int, iterations = 10):
    """
    Simulate the probability of having properly estimated a regression
    treatment estimate given a graph G. Returns a pandas df of

    @param N is range of nodes in G to generate
    @param S is range of samples to generate
    @param C is range of connections to generate
    @param K is the number of nodes to sample from G
    @param iterations is the number of bootstraps to perform for each permutation
    of each N, S, C, and K.
    """
    assert N%10 == 0
    print(N)
    data = pd.DataFrame(columns = ["N", "S", "C", "K", "Bias"])
    for s in range(2, S + 1):
        for c in range(1, C + 1):
            for n in range(10, N + 10, 10):
                G = randomGraph(n, s, c)
                for k in range(1, K + 1):
                    for i in range(1, iterations + 1):
                        paramGraph = sample(G, k)
                        bias = not nx.is_connected(paramGraph)
                        row = {"N": n, "S": s, "C": c, "K": k, "Bias": bias}
                        data = data.append(row, ignore_index = True)
    return data


if __name__ == "__main__":
    # drawGraph(g1)
    d = simulate(S = 2, N = 100, C = 5, K = 10)
    print(d)
    print(d.head(20))

    df = d.groupby(['N', 'S', 'C', 'K'])['Bias'].sum().reset_index()
    print(df.head(20))
