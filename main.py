from simulation import *

controller = NetworkRegression()

d = controller.simulate(S = 2, N = 100, C = 10, K = 10, sampler = controller.ideal_sampler, iterations = 10)
d = controller.aggregate(d)
analysis = Analysis(S = 2, N = 100, C = 10, K = 10, sampler = "controller", iterations = 10)
d = analysis.distribution(d, 10)

# plot(d, ['Prob', 'N'])
analysis.plot(d, ['Prob', 'N', 'K'])
#
d10 = d[d['N'] == 10]
analysis.plot(d10, ['Prob', 'K', 'C'])

d20 = d[d['N'] == 20]
analysis.plot(d20, ['Prob', 'K', 'C'])

d100 = d[d['N'] == 100]
analysis.plot(d100, ['Prob', 'K', 'C'])
