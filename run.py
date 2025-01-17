from class_network import Network
from plots import plot1, plot2, plot_boxes, plot_means, plot_transit
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import multiprocessing as mp
import cProfile
import csv


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
    with open('memo_test.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        next(csv_reader)
        with open('mean_memories.csv', 'w') as new_file:
            csv_writer_m = csv.writer(new_file)

            with open('mean_fitness.csv', 'w') as new_file2:
                csv_writer_f = csv.writer(new_file2)

                for line in csv_reader:

                    # Simulation parameters
                    num_nodes = int(line[0])
                    interactions_per_node = int(line[1])
                    hawk_dove_payoff = line[5:11]
                    hawk_dove_payoff = [float(i) for i in hawk_dove_payoff]
                    memory_cost = float(line[2])
                    initial_memory_poisson = int(line[3])
                    initial_aggression = float(line[4])
                    network_methode = line[-4:]
                    network_methode[2] = int(network_methode[2])
                    network_methode[3] = float(network_methode[3])
                    # network_methode = ['M3', 'Small-world', 4, 0.1]
                    # network_methode = ['M2','Uniform',6 , 0.1]

                    # Create the initial Network
                    my_network = Network(num_nodes, interactions_per_node, hawk_dove_payoff,
                                         memory_cost, initial_memory_poisson, initial_aggression, network_methode)
                    # list of lists (L2) L2 is the list of memory of each individual (in order) at the end. Memory lists L2 for each generation
                    # Memo_uncertainty = []
                    # Fitness = []  # same as Memory but with fitness data
                    # Aggression = []
                    # Memo_size = []
                    # Sizes = []
                    for i in range(5000):  # simulate this many generations
                        my_network.interact()
                        my_network.refresh_network()
                        # Memo_uncertainty.append(mean_per_indiv(
                        #     my_network.memo_uncertainty_history))
                        # Fitness.append(lasts(my_network.fitness_history))
                        # Aggression.append(list(my_network.aggression))
                        # Memo_size.append(list(my_network.memory))
                        # boxes are printed only for a few generations
                        # if (i == 0 or i == 100 or i == 1000 or i == 3500 or i == 4000 or i == 4800 or i == 4900 or i == 4999):
                        #     # plot_boxes(my_network, i, x)
                        #     Sizes.append(my_network.sizes)

                    csv_writer_m.writerow([i[1]for i in my_network.history])
                    csv_writer_f.writerow([i[0]for i in my_network.history])
                    # plot_means(my_network, x)
                    # print('Memory_size '+str(x)+'=', Memo_size)
                    # print('Agression ='+str(x), Aggression)
                    # print('Fitness '+str(x)+'=', Fitness)
                    # print('Memory_uncertainty ='+str(x), Memo_uncertainty)


# set the number of processes to be used
# np = mp.cpu_count()   # ... as detected by multiprocessing
NP = int(sys.argv[1])   # ... as passed in via the command line
# memo_cost = int(sys.argv[2])

with mp.Pool(NP) as p:
    p.map(my_f, range(NP))

# my_f(1)
