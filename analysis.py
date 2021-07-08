"""
Henry Manley - hjm67@cornell.edu

Analyzes simulated imperfect treatment data.
"""

from simulation import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot(data, varlist, size = False):
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
    assert type(varlist) == list
    for var in varlist:
        assert var in data.columns

    fig = plt.figure()
    if len(varlist) == 3:
        ax = fig.add_subplot(111, projection = '3d')
        if size is False:
            ax.scatter(data[str(varlist[0])], data[str(varlist[1])], data[str(varlist[2])])
        else:
            ax.scatter(data[str(varlist[0])], data[str(varlist[1])], data[str(varlist[2])], s = data[str(size)])
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



if __name__ == "__main__":
    d = simulate(S = 2, N = 100, C = 10, K = 10)
    d = distribution(d)
    print(d)
    plot(d, ['N', 'K', 'Bias'])

# wrap this in a function, recolor by interval, size by density, and investigate bias definition
