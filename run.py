from class_network import Network
from plots import plot1, plot2, plot_boxes, plot_means, plot_transit
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import multiprocessing as mp

index = 0


def lasts(L):
    """L is a list of lists lasts return a list of last items of each list in L"""
    Lasts = []
    for ind in L:  # browse L
        Lasts.append(ind[-1])
    return Lasts


def mean_per_indiv(L):
    """L is a list of lists mean_per_indiv return a list of the average avalue of each list in L"""
    M = []
    for ind in L:  # browse L
        M.append(np.mean(ind))
    return M


def combine_dictionnaries(ini_dictionary1, ini_dictionary2):
    # combining dictionaries
    # using dict comprehension and set
    final_dictionary = {x: ini_dictionary1.get(x, 0) + ini_dictionary2.get(x, 0)
                        for x in set(ini_dictionary1).union(ini_dictionary2)}

    return(final_dictionary)


def my_f(x):
    """Function to be run in parallel.
    """
    # print('index :', index)
    print('x :', x)
    # index += 1
    # Simulation parameters
    num_nodes = 50
    interactions_per_node = 500
    hawk_dove_payoff = [0.5, -1.5, 1, 0, 0.5, 0.5]
    memory_cost = 0.01
    initial_memory_poisson = 1
    initial_aggression = 0.5
    # network_methode = ['M1']
    network_methode = ['M3', 'Small-world', 4, 0.1]
    #network_methode = ['M2','Uniform',6 , 0.1]

    # Create the initial Network
    my_network = Network(num_nodes, interactions_per_node, hawk_dove_payoff,
                         memory_cost, initial_memory_poisson, initial_aggression, network_methode)
    # list of lists (L2) L2 is the list of memory of each individual (in order) at the end. Memory lists L2 for each generation
    Memo_uncertainty = []
    Fitness = []  # same as Memory but with fitness data
    Aggression = []
    Memo_size = []
    Sizes = []
    for i in range(4000):  # simulate this many generations
        my_network.interact()
        Memo_uncertainty.append(mean_per_indiv(
            my_network.memo_uncertainty_history))
        Fitness.append(lasts(my_network.fitness_history))
        Aggression.append(list(my_network.aggression))
        Memo_size.append(list(my_network.memory))
        # boxes are printed only for a few generations
        if (i == 0 or i == 100 or i == 1000 or i == 2500 or i == 3000 or i == 3800 or i == 3900 or i == 3999):
            plot_boxes(my_network, i, x)
            Sizes.append(my_network.sizes)

        my_network.refresh_network()

    plot_means(my_network, x)

    print('Memory_size =', Memo_size)
    print('Agression =', Aggression)
    print('Fitness =', Fitness)
    print('Memory_uncertainty =', Memo_uncertainty)


# set the number of processes to be used
# np = mp.cpu_count()   # ... as detected by multiprocessing
NP = int(sys.argv[1])   # ... as passed in via the command line

with mp.Pool(NP) as p:
    p.map(my_f, range(NP))
