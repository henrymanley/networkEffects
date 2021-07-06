"""
Henry Manley - hjm67@cornell.edu
"""
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random

def randomGraph(n, s, c):
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



def sample(G, n):
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



if __name__ == "__main__":
    g = randomGraph(10, 2, 3)
    g1 = sample(g, 5)
    drawGraph(g1)
