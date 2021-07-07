# Simulating Biased Treatment Estimates: How Networks Complicate Things

## Motivations
This repository is motivated by growing questions in field of econometrics, particularly
surrounding how underlying networks contribute to biased treatment estimates. Consider [Miguel and Kremer 2004](https://onlinelibrary.wiley.com/doi/epdf/10.1111/j.1468-0262.2004.00481.x), which is concerned with isolating the causal effects of deworming
programs in Kenyan schools. Such an experimental design is concerned with mitagating
splillovers (maintaing [SUTVA](https://blogs.iq.harvard.edu/violations_of_s#:~:text=Methods%20for%20causal%20inference%2C%20in,treatments%20of%20others%20around%20him.)), but such a possibility is nearly impossible in the
real world. As a brute-force solution to the notion of "connected" networks of pupils
of students across treatment and control schools, a distance-based penalty is introduced
to the OLS framework.

Since, many studies, particularly in the space of microfinance and developmental economics [(Banerjee, Chandrasekhar, Duflo, and Jackson)](https://economics.mit.edu/files/9070), [(Chandrasekhar and Lewis 2019)](http://stanford.edu/~arungc/CL.pdf), [(Hardy et. al)](https://arxiv.org/pdf/1904.00136.pdf) have been aimed at addressing this network dilemma in a more methodological fashion.

What has yet to be developed, though, is a more general econometric framework that tackles
this question. It seems that there is great promise in exploiting tools from probability
and graph theory, especially in developing Monte Carlo simulations, to model the adverse effects
of imperfect random-sampling and the subsequent violation of SUTVA. Similarly, there is room
to explore and apply [graph traversal algorithms](https://www.cs.cornell.edu/courses/cs2110/2019sp/L18-GraphTraversal/L18-GraphTraversal.pdf) to the challenge of recovering an unknown
network to bolster a conservative estimate of the effect of a graph's connectedness on
the treatment coefficient.

This repository is a codebase for exploration and simulation in this general area.

## Installation
To use the code, clone the repository to a local directory. From the command line and in that
directory, type: `pip install -r requirements.txt`. This will install repository-specific dependencies.

From there, typing `python simulation.py` will run the main simulation functions, and yield both
images and raw data to analyze. Further analysis is done in `analysis.py`.
