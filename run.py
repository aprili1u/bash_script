from class_network import Network
from plots import plot1, plot2, plot_boxes, plot_means, plot_transit
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import multiprocessing as mp
import cProfile
import csv
from filelock import Timeout, FileLock

# global lock
lock = mp.Lock()


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
        # lock = FileLock("mean_memories.csv.lock")
        with open('mean_memories3.csv', 'a') as new_file:
            csv_writer_m = csv.writer(new_file)

            with open('last_generation_distribution.csv', 'a') as new_file2:
                csv_writer_d = csv.writer(new_file2)

                for line in csv_reader:
                    # if line[0] == str(x):

                    # Simulation parameters
                    num_nodes = int(line[1])
                    interactions_per_node = int(line[2])
                    hawk_dove_payoff = line[6:12]
                    hawk_dove_payoff = [float(i)
                                        for i in hawk_dove_payoff]
                    memory_cost = float(line[3])
                    initial_memory_poisson = int(line[4])
                    initial_aggression = float(line[5])
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

                    for i in range(100):  # simulate this many generations
                        my_network.interact()
                        previous_memories = my_network.refresh_network()
                        # Memo_uncertainty.append(mean_per_indiv(
                        #     my_network.memo_uncertainty_history))
                        # Fitness.append(lasts(my_network.fitness_history))
                        # Aggression.append(list(my_network.aggression))
                        # Memo_size.append(list(my_network.memory))
                        # boxes are printed only for a few generations
                        # if (i == 0 or i == 100 or i == 1000 or i == 3500 or i == 4000 or i == 4800 or i == 4900 or i == 4999):
                        #     # plot_boxes(my_network, i, x)
                        #     Sizes.append(my_network.sizes)
                    SD = np.std(
                        np.array(my_network.history[-100:]), axis=0)  # SD on a moving window of size 100
                    Mean = np.mean(
                        np.array(my_network.history[-100:]), axis=0)  # mean on a moving window of size 100
                    threshold = SD[1] / Mean[1]

                    while (threshold > 0.1 and len(my_network.history) < 100000):
                        my_network.interact()
                        previous_memories = my_network.refresh_network()
                        SD = np.std(
                            np.array(my_network.history[-100:]), axis=0)  # SD on a moving window of size 100
                        Mean = np.mean(
                            np.array(my_network.history[-100:]), axis=0)  # mean on a moving window of size 100
                        threshold = SD[1] / Mean[1]

                    lock.acquire()
                    csv_writer_m.writerow([line[0]] + ['Mean'] + [i[1]
                                                                  for i in my_network.history])
                    csv_writer_d.writerow(
                        [line[0]] + ['generation : ' + str(len(my_network.history))] + list(previous_memories))
                    csv_writer_m.writerow(
                        [line[0]] + ['SD'] + my_network.SD_history)
                    lock.release()
                    # print([i[1]
                    #        for i in my_network.history])
                    # print(list(my_network.memory))
                    # print(list(my_network.SD_history))


def my_f2(x):
    # print("here")
    # with open('new_names.csv', 'r') as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #     for line in csv_reader:
    return(x**2)


# set the number of processes to be used
# # np = mp.cpu_count()   # ... as detected by multiprocessing
# NP = int(sys.argv[1])   # ... as passed in via the command line
NP = 2

with mp.Pool(NP, initargs=lock,) as p:
    output = p.starmap_async(my_f2, range(10))
    # p.map(my_f, range(NP))
    print(output.get())
