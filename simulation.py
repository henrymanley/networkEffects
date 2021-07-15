"""
Henry Manley - hjm67@cornell.edu

Ideal World Simulation

Simulates imperfect treatment effects created by node connectedness. Given an
undirected graph G = {V,E}, what can we learn about the underlying network from
sampling?
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random
import itertools


class NetworkRegression():

    def drawGraph(self, G):
        """
        Draws graph object G to window.

        @param G is the graph object to be drawn
        """
        nx.draw(G, node_size = 30,  with_labels=True)
        plt.show()


    def randomGraph(self, n: int, s: int, c: int):
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


    def ideal_sampler(self, G, n: int, s: int):
        """
        Returns an indicator of subgraph non-disjointedness.

        This implementation assumes that for every sample of V, you perfectly retrieve all
        degree and edge information and there is no "cost" incurred by this retrieval.
        Thus, a set of v in V are randomly sampled for each s in S. Then, all edge
        information are retrieved for each v to map out a subgraph G'. This implementation
        assumes that each group is non-disjoint.

        @param G is the graph object to sample and reverse engineer
        @param n is the number of nodes to sample from G
        @param s is the number of groups
        """
        assert s == 2
        allNodes = list(G.nodes)
        G1 = nx.Graph()

        for i in range(s):
            index = int(len(allNodes)/s)
            if i == 0:
                sampleNodes = random.sample(allNodes[index:], n)
            else:
                sampleNodes = random.sample(allNodes[:index], n)
            G1.add_nodes_from(sampleNodes)
            for node in sampleNodes:
                sampleEdges = list(G.edges(node))
                G1.add_edges_from(sampleEdges)

        return int(nx.is_connected(G1))


    def base_real_sampler(self, G, n: int, s: int):
        """
        Returns the number of edges recovered from sampling.

        This implementation randomly samples n nodes from each group s in S.
        Each combination of nodes between these two groups and tested for edges
        between them. If there is an edge that connects them, that is indicative
        of bias that is in fact captured by this base simulation. Else, it is possible
        that whilst each sample was representative of their populations, there are simply
        few edges connecting them to begin with.

        @param G is the graph object to sample and reverse engineer
        @param n is the number of nodes to sample from G
        @param s is the number of groups
        """
        assert s == 2
        allNodes = list(G.nodes)
        index = int(len(allNodes)/s)
        G1 = nx.Graph()

        treatedNodes = random.sample(allNodes[index:], n)
        controlNodes = random.sample(allNodes[:index], n)

        combinations = list(itertools.product(treatedNodes, controlNodes))
        edges = 0
        for pair in combinations:
            connected = pair[0] in G.neighbors(pair[1])
            if connected:
                edges += 1
        return edges


    def mod1_real_sampler(self, G, n: int, s: int):
        """
        Returns the number of edges recovered from sampling.

        This implementation is the first functional improvement on the base_real_sampler.
        In particular, this method first samples nodes withing groups to draw out
        rough estimates of underlying graphs for each group s in S. This process
        is done probabilistically, whereas once nodes are sampled (without replacement)
        and are "questioned" to obtain edge information, nodes that appear to be more
        central will have neighbors that will be excluded from this sampling.

        Then, each combination of nodes between these two subgroups and tested for edges
        between them. If there is an edge that connects them, that is indicative
        of bias that is in fact captured by this base simulation. Else, it is possible
        that whilst each sample was representative of their populations, there are simply
        few edges connecting them to begin with.

        @param G is the graph object to sample and reverse engineer
        @param n is the number of nodes to sample from G
        @param s is the number of groups
        """
        pass


    def simulate(self, S: int, N: int, C: int, K: int, sampler, iterations = 10):
        """
        Simulate the probability of having properly estimated a regression
        treatment estimate given a graph G. Returns a pandas df with simulation
        iterations as line items.

        @param N is range of nodes in G to generate
        @param S is range of samples to generate
        @param C is range of connections to generate
        @param K is the number of nodes to sample from G
        @param sample is a sampling function that MUST return an integer indicator
        of recovered edges.
        @param iterations is the number of bootstraps to perform for each permutation
        of each N, S, C, and K.
        """
        assert N%10 == 0
        data = pd.DataFrame(columns = ["N", "S", "C", "K", "Bias"])
        for s in range(2, S + 1):
            for c in range(1, C + 1):
                for n in range(10, N + 10, 10):
                    print(n)
                    G = self.randomGraph(n, s, c)
                    for k in range(1, K + 1):
                        for i in range(1, iterations + 1):
                            bias = sampler(G, k, s)
                            assert type(bias) == int
                            row = {"N": n, "S": s, "C": c, "K": k, "Bias": bias}
                            data = data.append(row, ignore_index = True)
        return data


    def aggregate(self, data):
        """
        From simulation pandas dataframe, where each row represents a single bootstrap,
        compute parameter-level aggregates. Note, bias is an instance of one or more
        edges in the underlying network being drawn from treatment and control nodes.

        @param data is the aforementioned pandas dataframe- the product of simulate()
        """
        data = data.groupby(['N', 'S', 'C', 'K'])['Bias'].sum().reset_index()
        data['Bias'] = data['Bias'].astype(int)
        return data


class Analysis(NetworkRegression):

    def getSimParams(self):
        """
        Gets all simulation attributes for object of type Analysis.
        """
        return [self.N, self.S, self.C, self.K, self.I, self.Func]


    def plot(self, data, varlist: list, size = False):
        """
        Given aggregated simulation statistics pandas dataframe, plot paramterized variables
        in 2 or 3-dimensional space.

        @param data is the aforementioned pandas dataframe

        @param varlist is the list of variables to plot. If the the list is of length 2,
        the first variable specified is y, and the second x. If the list is of length 3,
        the variable order is as follows: x, y, z. The variables in this list MUST be
        exact column names in the dataframe data.

        @param size is an optional argument which can be specified to determine the variable
        used to size data points in either 2d or 3d settings.
        """
        for var in varlist:
            assert var in data.columns

        fig = plt.figure()
        if len(varlist) == 3:
            ax = fig.add_subplot(111, projection = '3d')
            data['strX'] = data[str(varlist[0])].astype(str)

            if size is False:
                ax.scatter(data[str(varlist[0])], data[str(varlist[1])], data[str(varlist[2])])
            else:
                ax.scatter(data[str(varlist[0])], data[str(varlist[1])], data[str(varlist[2])], data[str(varlist[0])])

            ax.set_xlabel(varlist[0])
            ax.set_ylabel(varlist[1])
            ax.set_zlabel(varlist[2])

        if len(varlist) == 2:
            if size is False:
                plt.scatter(data[str(varlist[0])], data[str(varlist[1])])
            else:
                plt.scatter(data[str(varlist[0])], data[str(varlist[1])], s = data[str(size)])
            plt.xlabel(varlist[0])
            plt.ylabel(varlist[1])

        plt.show()


    def distribution(self, data, iterations: int):
        """
        Given aggregated simulation statistics pandas dataframe, approximate probability
        distribution.

        @param data is the aforementioned pandas dataframe
        @param iterations is the number of iterations each parameter combination was
        performed

        NOTES:
        As it stands now, Bias is the frequency of recovering a singular edge (regardless of
        the number of edges). The best way to visualize this would be to plot (Bias/K) against
        N. Do this for each C. --> will need new way to handle "recovering" at least 2, 3, ...
        """
        data['Prob'] = data['Bias']/self.getSimParams()[4]
        return data


    def __init__(self, N: int, S: int, C: int, K: int, sampler: str, iterations: int):
        """
        Initialize object of type Analysis. This subclass of NetworkRegression
        is used to analyze simulated results, yielded by the init()'s parameters.

        @param N is range of nodes in G generated
        @param S is range of samples generated
        @param C is range of connections generated
        @param K is the number of nodes sampled from G
        @param sampler is a test description of the sampling function used
        @param iterations is the number of iterations performed
        """
        super().__init__()
        self.N = N
        self.S = S
        self.C = C
        self.K = K
        self.I = iterations
        self.Func = sampler
