# Simulating Biased Treatment Estimates: How Networks Complicate Things
#### Henry Manley - The Federal Reserve Bank of Dallas, Cornell University

## Motivations
This repository is motivated by growing questions in the field of econometrics, particularly
surrounding how underlying networks contribute to biased treatment estimates. Consider [Miguel and Kremer 2004](https://onlinelibrary.wiley.com/doi/epdf/10.1111/j.1468-0262.2004.00481.x), which is concerned with isolating the causal effects of deworming
programs in Kenyan schools. Such an experimental design is concerned with mitagating
splillovers (maintaing [SUTVA](https://blogs.iq.harvard.edu/violations_of_s#:~:text=Methods%20for%20causal%20inference%2C%20in,treatments%20of%20others%20around%20him.)), but such a possibility is nearly impossible in the
real world. As a brute-force solution to the notion of "connected" networks of pupils
of students across treatment and control schools, a distance-based penalty is introduced
to the OLS framework.

Since, many studies, particularly in the space of microfinance and developmental economics [(Banerjee, Chandrasekhar, Duflo, and Jackson)](https://economics.mit.edu/files/9070), [(Chandrasekhar and Lewis 2019)](http://stanford.edu/~arungc/CL.pdf), [(Hardy et. al)](https://arxiv.org/pdf/1904.00136.pdf) have been aimed at addressing this network dilemma in a more methodological fashion.

What has yet to be developed, though, is a more general econometric framework that tackles
this question. The currently best available robustness check [(Burke, Bergquist, Miguel 2019)](https://academic.oup.com/qje/article-abstract/134/2/785/5266398) on SUTVA comes in the form
of randomizing treatment, and then ex-post bootstrapping the assignment variable to test
for changes in group means based on the inclusion of certain subjects.

It seems that there is great promise in exploiting tools from probability
and graph theory, especially in developing Monte Carlo simulations, to model the adverse effects
of imperfect random-sampling and the subsequent violation of SUTVA. Similarly, there is room
to explore and apply [graph traversal algorithms](https://www.cs.cornell.edu/courses/cs2110/2019sp/L18-GraphTraversal/L18-GraphTraversal.pdf) to the challenge of recovering an unknown
network to bolster a conservative estimate of the effect of a graph's connectedness on
the treatment coefficient.

This repository is a codebase for exploration and simulation in this general area.

## Theory
The most general form of this problem can be delineated with some notation from graph
theory. Consider the graph G that is the set of all vertices *V*, and edges *E* from such
vertices (*G = {V, E}*). In an experimental setting, we assume that there are disjoint
graphs for treated and untreated subjects such that there are two independent graphs.
This assumption is in line with SUTVA, but is often impossible to provide robust
evidence. The terms vertices and nodes are used interchangeably. For each disjoint
graph, nodes *i* and *j* are either connected by *e ??? E*, or unconnected. For the purposes
of the proposed methodology, such connections are unweighted (there is no relative measure
of connectedness) and undirected.

The principle investigation is whether any number of *c* edges connecting nodes in each
of the once disjoint treatment and control graphs can be recovered by sampling *k*
nodes and obtaining the set of edges from such nodes. In a practical setting, this procedure
would be implemented by asking some number of subjects in each group a relational question that
would yield a list of subjects that, for example, they interact with. In the worst case,
a complete graph (for both treatment and control groups) would require that for each
subject, a list of *n-1* subjects would need to be presented to them to recover the entire
underlying network. The ultimate goal is to capture the frequency of edges drawn between
the assumed disjoint graphs to adjust this effect in the OLS estimation of treatment.

Since we are not concerned with the entirety of the underlying network but instead
only the edges that connect them (if any at all), we are willing to accept some confidence
interval on a random subset of this *n-1* dilemma. Of particular interest is if there is a method to minimize
not only the number of subjects that are questioned, but also the length of the list (of other subjects)
that they are presented to each subject. There are a few avenues to explore in the framing
of this question- for example, perhaps targeting more central nodes (nodes in each graph that have
highest degrees) would help to learn the most about the underlying graphs in the least costly manor,
but also unlikely to yield information about edges connecting the once, or the assumed, disjoint
graphs. This rests upon the assumption that subjects in both groups are meant to be mutually exclusive
and unaffected by any spillovers (which too are meant to be non-existent).

The goal of recovering such data has the possibility of being computationally costly (*O(n(n-1))*), but does
also clue in help from probability theory and graph traversal to impute.


## Simulation Parameters
For the purposes of simulating imperfect treatment caused by network SUTVA violations,
the following variables are parameterized as such and are used throughout the body
of all simulation code:

`G`: the graph object such that G = {V, E} <br />
`N`: the number of observations/people in each group (treatment and control) <br />
`S`: the number of groups <br />
`C`: the number of edges shared between treatment and control groups <br />
`K`: the number of samples drawn from each group to reverse-engineer a sub-graph G' <br />
`Sampler`: the sampling function used to recover data about G <br />
`I`: the number of bootstraps performed for combination of N, S, C, K, and Sampler <br />

## Installation
To use the code, clone the repository to a local directory. From the command line and in that
directory, type: `pip install -r requirements.txt`. This will install repository-specific dependencies.

From there, typing `python main.py` will run the main the simulation function on
default parameters, and yield both images and pandas dataframes to analyze.

To use or modify such simulations, instantiate an object of type `NetworkRegression`.
To analyze results of your custom paramterization of this object, instatiate an
object of type `Analysis`, a class that extends `NetworkRegression`.

```python
from simulation import *

controller = NetworkRegression()
d = controller.simulate(S = 2, N = 100, C = 10, K = 10, sampler = controller.ideal_sampler, iterations = 10)
d = controller.aggregate(d)

analysis = Analysis(S = 2, N = 100, C = 10, K = 10, sampler = "controller", iterations = 10)
d = analysis.distribution(d, 10)
d20 = d[d['N'] == 20]
analysis.plot(d20, ['Prob', 'K', 'C'])
```

## Sampling Functions
Simulations can be conceptualized in two ways. The first and the simpler of the two, is
assuming that you have asked the "perfect question" that allows a given subject to
reveal all of the subjects that they "interact with". Note how this approach is different
from the second approach, which not only randomly selects subjects to question (as does
the first approach) but also samples a list of subjects (from each group) and asks if they
"interact with" each person on that list. In the context of simulation, this "question" is
answered for each randomly selected subject in attempt to reveal cross-graph edges or connections.
This simulation is realized by passing the `simulate()` function the `ideal_sampler`
sampler.

The second approach can be viewed as a negation of the first, where subjects are not asked
for a comprehensive list of all people they know, but instead are presented with a list
of subjects to identify connections. Note, the second approach is more similar to how
this methodology could be intuitively implemented. Not to mention, asking a subject to list
all of the people they know is not a reasonable exercise. Nevertheless, the first
approach is helpful in generating quick estimations of the parameters needed to recover
any shared edges. In short, the first approach is representative of the ideal world in which
all sampled participants yield all of the desired information with the fewest number of "questions".
This simulation, in its most naive and computationally basic form, is realized by passing
the `simulate()` function the `base_real_sampler` sampler. The ultimate goal is
to design an algorithmic approach, by making incremental improvements to the sampling method
to recover the most about an unknown network in a computationally efficient way.
