# -*- coding: utf-8 -*-

import numpy as np
from multiprocessing import Pool, Lock
import csv
import sys


class Network:
    def __init__(self, num_nodes, interactions_per_node, interaction_partners, memory_cost, initial_memory_poisson, payoff_matrix):
        self.num_nodes = num_nodes  # number of Nodes in the Network
        # interactions each Node will have on average in one generation
        self.interactions_per_node = interactions_per_node
        # total number of partners a Node can interact with, taken as symmetrically to their left and right in an ordered network
        self.interaction_partners = interaction_partners
        # metabolic cost of each memory slot, paid once over the lifetime
        self.memory_cost = float(memory_cost)
        # [hawk-hawk winner, hawk-hawk loser, hawk-dove hawk, hawk-dove dove; dove-dove dove]
        self.payoff_matrix = payoff_matrix
        self.nodes = []  # list of Node objects of the network
        self.history = []  # after every refresh, save the  and std dev of fitness and memory
        # generate uniform sample of sizes
        sizes = np.random.random_sample(self.num_nodes)
        # initial memory is a poisson distribution
        memory = np.random.poisson(
            float(initial_memory_poisson), size=self.num_nodes)
        aggression = np.full(self.num_nodes, 0.5)
        # create iniital Nodes
        for i in range(self.num_nodes):
            self.nodes.append(Node(sizes[i], memory[i], aggression[i]))

    def interact(self):
        # choose pairs of Nodes to play Hawk-Dove game
        if self.interaction_partners == self.num_nodes:
            # each node has the same probability of having an interaction, with all nodes equally likely to interact with all other nodes
            indices = np.random.choice(self.num_nodes, size=(
                int(self.interactions_per_node*self.num_nodes/2), 2))
            for i in range(int(self.interactions_per_node*self.num_nodes/2)):
                ind1 = indices[i][0]
                ind2 = indices[i][1]
                if ind1 != ind2:  # check for interaction with self
                    self.hawk_dove(self.nodes[ind1], self.nodes[ind2])
                else:  # assign new partner if assigned an interaction with self
                    ind2 = np.random.choice(
                        [index for index in np.arange(self.num_nodes) if index != ind1])
                    self.hawk_dove(self.nodes[ind1], self.nodes[ind2])
        else:
            # get relative indices of potential neighbors
            potential_partners = [i for i in range(int(-1*self.interaction_partners/2),
                                                   int(1 + self.interaction_partners/2)) if i != 0]
            # first pick a Node randomly
            focal_node = np.random.choice(self.num_nodes, size=int(
                self.interactions_per_node*self.num_nodes/2))
            # then randomly pick a partner from its potential partners
            neighbor_indices = np.random.choice(potential_partners,  size=int(
                self.interactions_per_node*self.num_nodes/2))
            for i in range(int(self.interactions_per_node*self.num_nodes/2)):
                focal_index = focal_node[i]
                partner_index = (
                    focal_node[i] + neighbor_indices[i]) % self.num_nodes
                self.hawk_dove(self.nodes[focal_index],
                               self.nodes[partner_index])

    def hawk_dove(self, node1, node2):
        # increment the total number of interactions a Node has had over its lifetime
        node1.num_interactions += 1
        node2.num_interactions += 1

        # these numbers are used to determine if an ignorant Node plays hawk or dove
        rand_nums = np.random.random_sample(2)

        # If a Node remembers beating a bigger Node than its current partner, it plays hawk;
        # If a Node remembers losing to a smaller Node than its current partner, it plays dove;
        # Otherwise, we label the Node as ignorant, its probability of playing hawk is its aggression
        # Victories are stored in memory as 1 and losses as 0, if there was not a hawk-hawk interaction,
        # the interaction still uses a memory slot, but it is recorded as None.

        if node2.size < node1.min_size:  # player 1 plays hawk
            if node1.size < node2.min_size:  # player 2 plays hawk
                if node1.size > node2.size:  # player 1 wins
                    node1.fitness += self.payoff_matrix[0]
                    node2.fitness += self.payoff_matrix[1]
                    node1.add_memory(node2.size, 1)
                    node2.add_memory(node1.size, 0)
                else:  # player 2 wins
                    node2.fitness += self.payoff_matrix[0]
                    node1.fitness += self.payoff_matrix[1]
                    node1.add_memory(node2.size, 0)
                    node2.add_memory(node1.size, 1)
            elif node1.size > node2.max_size:  # player 2 plays dove
                node1.fitness += self.payoff_matrix[2]
                node2.fitness += self.payoff_matrix[3]
                node1.add_memory(node2.size, None)
                node2.add_memory(node1.size, None)
            else:  # player 2 ignorant
                # player 2 plays ignorant hawk
                if node2.aggression > rand_nums[1]:
                    if node1.size > node2.size:  # player 1 wins
                        node1.fitness += self.payoff_matrix[0]
                        node2.fitness += self.payoff_matrix[1]
                        node1.add_memory(node2.size, 1)
                        node2.add_memory(node1.size, 0)
                    else:  # player 2 wins
                        node2.fitness += self.payoff_matrix[0]
                        node1.fitness += self.payoff_matrix[1]
                        node1.add_memory(node2.size, 0)
                        node2.add_memory(node1.size, 1)
                else:  # player 2 plays ignorant dove
                    node1.fitness += self.payoff_matrix[2]
                    node2.fitness += self.payoff_matrix[3]
                    node1.add_memory(node2.size, None)
                    node2.add_memory(node1.size, None)
        elif node2.size > node1.max_size:  # player 1 plays dove
            if node1.size < node2.min_size:  # player 2 plays hawk
                node2.fitness += self.payoff_matrix[2]
                node1.fitness += self.payoff_matrix[3]
            elif node1.size > node2.max_size:  # player 2 plays dove
                node1.fitness += self.payoff_matrix[4]
                node2.fitness += self.payoff_matrix[4]
            else:  # player 2 ignorant
                # player 2 plays ignorant hawk
                if node2.aggression > rand_nums[1]:
                    node2.fitness += self.payoff_matrix[2]
                    node1.fitness += self.payoff_matrix[3]
                else:  # player 2 plays ignorant dove
                    node1.fitness += self.payoff_matrix[4]
                    node2.fitness += self.payoff_matrix[4]
            node1.add_memory(node2.size, None)
            node2.add_memory(node1.size, None)

        else:  # player 1 ignorant
            if node1.aggression > rand_nums[0]:  # player 1 plays ignorant hawk
                if node1.size < node2.min_size:  # player 2 plays hawk
                    if node1.size > node2.size:  # player 1 wins
                        node1.fitness += self.payoff_matrix[0]
                        node2.fitness += self.payoff_matrix[1]
                        node1.add_memory(node2.size, 1)
                        node2.add_memory(node1.size, 0)
                    else:  # player 2 wins
                        node2.fitness += self.payoff_matrix[0]
                        node1.fitness += self.payoff_matrix[1]
                        node1.add_memory(node2.size, 0)
                        node2.add_memory(node1.size, 1)
                elif node1.size > node2.max_size:  # player 2 plays dove
                    node1.fitness += self.payoff_matrix[2]
                    node2.fitness += self.payoff_matrix[3]
                    node1.add_memory(node2.size, None)
                    node2.add_memory(node1.size, None)
                else:  # player 2 ignorant
                    # player 2 plays ignorant hawk
                    if node2.aggression > rand_nums[1]:
                        if node1.size > node2.size:  # player 1 wins
                            node1.fitness += self.payoff_matrix[0]
                            node2.fitness += self.payoff_matrix[1]
                            node1.add_memory(node2.size, 1)
                            node2.add_memory(node1.size, 0)
                        else:  # player 2 wins
                            node2.fitness += self.payoff_matrix[0]
                            node1.fitness += self.payoff_matrix[1]
                            node1.add_memory(node2.size, 0)
                            node2.add_memory(node1.size, 1)
                    else:  # player 2 plays ignorant dove
                        node1.fitness += self.payoff_matrix[2]
                        node2.fitness += self.payoff_matrix[3]
                        node1.add_memory(node2.size, None)
                        node2.add_memory(node1.size, None)
            else:  # player 1 plays ignorant dove
                if node1.size < node2.min_size:  # player 2 plays hawk
                    node2.fitness += self.payoff_matrix[2]
                    node1.fitness += self.payoff_matrix[3]
                elif node1.size > node2.max_size:  # player 2 plays dove
                    node1.fitness += self.payoff_matrix[4]
                    node2.fitness += self.payoff_matrix[4]
                else:  # player 2 ignorant
                    # player 2 plays ignorant hawk
                    if node2.aggression > rand_nums[1]:
                        node2.fitness += self.payoff_matrix[2]
                        node1.fitness += self.payoff_matrix[3]
                    else:  # player 2 plays ignorant dove
                        node1.fitness += self.payoff_matrix[4]
                        node2.fitness += self.payoff_matrix[4]
                node1.add_memory(node2.size, None)
                node2.add_memory(node1.size, None)

    def refresh_network(self):
        # create new Nodes to fully replace the existing network
        for node in self.nodes:
            # Nodes pay a cost per memory slot at the end of their life
            node.fitness -= len(node.size_memory)*self.memory_cost
            # Fitness cannot be negative
            if node.fitness < 0:
                node.fitness = 0

        # get fitness of Nodes
        fitness = np.array([node.fitness for node in self.nodes])
        # fitness values are now normalized
        normalized_fitness = fitness/np.sum(fitness)
        # random weighted choice based on fitness
        reproducing_node_index = np.random.choice(
            self.num_nodes, self.num_nodes, p=normalized_fitness)
        reproducing_node_memory = np.array(
            [len(self.nodes[index].size_memory) for index in reproducing_node_index])  # memory of new nodes
        reproducing_node_aggression = np.full(
            self.num_nodes, 0.5)  # aggression of new nodes

        # record means to see results
        self.history.append([np.mean(fitness), np.std(fitness), np.mean(
            reproducing_node_memory), np.std(reproducing_node_memory)])

        # add mutations
        mutations = np.random.binomial(1, 0.1, self.num_nodes)
        sign = np.random.choice([-1, 1], size=self.num_nodes)
        memory_mutations = mutations*sign
        reproducing_node_memory += memory_mutations  # mutate memory
        # generate uniform sample of sizes
        sizes = np.random.random_sample(self.num_nodes)

        del self.nodes[:]  # clear current nodes
        for i in range(self.num_nodes):  # create new nodes
            self.nodes.append(
                Node(sizes[i], reproducing_node_memory[i], reproducing_node_aggression[i]))


class Node:
    def __init__(self, size, memory_length, aggression):
        self.size = size
        self.num_interactions = 0
        self.fitness = 0.0
        self.min_size = 0.0  # size of the largest size you have beaten
        self.max_size = 1.0  # size of smallest size you have lost to you

        # check that memory is positive
        if memory_length < 0:
            memory_length = 0
        self.size_memory = [None]*int(memory_length)
        self.outcome_memory = [None]*int(memory_length)

        # check that aggression is between 0 and 1
        if aggression > 1.0:
            self.aggression = 1.0
        elif aggression < 0.0:
            self.aggression = 0.0
        else:
            self.aggression = aggression

    def add_memory(self, new_size, outcome):
        if len(self.size_memory) == 0:
            return

        # Update the Node's perception of the biggest partner it has beaten and smallest partner it has lost to if the new memory
        # changes these values (min, max).
        if self.num_interactions > len(self.size_memory):  # memory is full
            self.outcome_memory.append(outcome)  # gain memory
            self.size_memory.append(new_size)
            if outcome == 1:  # won fight
                if new_size > self.min_size:  # check if new memory changes min
                    self.min_size = new_size  # set new min
                    self.size_memory.pop(0)  # lose memory
                    self.outcome_memory.pop(0)
                # check if losing min memory
                elif self.size_memory[0] == self.min_size:
                    self.size_memory.pop(0)  # lose memory
                    self.outcome_memory.pop(0)
                    # set new min
                    self.min_size = max([self.size_memory[i] for i in range(
                        len(self.outcome_memory)) if self.outcome_memory[i] == 1])
                else:  # lose memory
                    self.size_memory.pop(0)
                    self.outcome_memory.pop(0)
            elif outcome == 0:  # lost fight
                if new_size < self.max_size:
                    self.max_size = new_size  # set new max
                    self.size_memory.pop(0)  # lose memory
                    self.outcome_memory.pop(0)
                # check if losing max memory
                elif self.size_memory[0] == self.max_size:
                    self.size_memory.pop(0)  # lose memory
                    self.outcome_memory.pop(0)
                    # set new max
                    self.max_size = min([self.size_memory[i] for i in range(
                        len(self.outcome_memory)) if self.outcome_memory[i] == 0])
                else:  # lose memory
                    self.size_memory.pop(0)
                    self.outcome_memory.pop(0)
            else:  # no fight, lose memory
                self.size_memory.pop(0)
                self.outcome_memory.pop(0)
                if [self.size_memory[i] for i in range(len(self.outcome_memory)) if self.outcome_memory[i] == 0] != []:
                    self.max_size = min([self.size_memory[i] for i in range(
                        len(self.outcome_memory)) if self.outcome_memory[i] == 0])
                else:
                    self.max_size = 1.0
                if [self.size_memory[i] for i in range(len(self.outcome_memory)) if self.outcome_memory[i] == 1] != []:
                    self.min_size = max([self.size_memory[i] for i in range(
                        len(self.outcome_memory)) if self.outcome_memory[i] == 1])
                else:
                    self.min_size = 0.0

        else:  # memory is not full
            if outcome == 1:  # won fight
                if new_size > self.min_size:  # check if new min
                    self.min_size = new_size
            elif outcome == 0:  # lost fight
                if new_size < self.max_size:  # check if new max
                    self.max_size = new_size
            # gain memory
            self.size_memory[self.num_interactions-1] = new_size
            self.outcome_memory[self.num_interactions-1] = outcome


def simulate(ID, trial, generations, num_nodes, interactions_per_node, interaction_partners, memory_cost, initial_memory_poisson, p0, p1, p2, p3, p4):
    print('ID'+str(ID))
    print('trial'+str(trial))
    print('generations'+str(generations))
    print('num_nodes'+str(num_nodes))
    print('interactions_per_node'+str(interactions_per_node))
    print('interaction_partners' + str(interaction_partners))
    print(memory_cost)
    print(initial_memory_poisson)
    print(p0, p1, p2, p3, p4)
    hawk_dove_payoff = [float(p0), float(p1), float(p2),
                        float(p3), float(p4)]

    # initialize Network
    my_network = Network(int(num_nodes), int(interactions_per_node),
                         int(interaction_partners), float(
        memory_cost), float(initial_memory_poisson),
        hawk_dove_payoff)

    # simulate generations of interactions
    for g in range(int(generations)):
        my_network.interact()
        my_network.refresh_network()

    # save final data from simulations
    mean_fitness = np.asarray(my_network.history)[:, 0].tolist()
    std_fitness = np.asarray(my_network.history)[:, 1].tolist()
    mean_memory = np.asarray(my_network.history)[:, 2].tolist()
    std_memory = np.asarray(my_network.history)[:, 3].tolist()
    final_memory_distribution = [len(node.size_memory)
                                 for node in my_network.nodes]
    final_fitness_distribution = [node.fitness for node in my_network.nodes]

    # write data to file
    with lock:
        with open('results.csv', 'a', newline='') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow([ID, trial, "Mean_Fitness"] + mean_fitness)
            csv_writer.writerow([ID, trial, "Std_Fitness"] + std_fitness)
            csv_writer.writerow([ID, trial, "Mean_Memory"] + mean_memory)
            csv_writer.writerow([ID, trial, "Std_Memory"] + std_memory)
            csv_writer.writerow(
                [ID, trial, "Final_Memory_Distribution"] + final_memory_distribution)
            csv_writer.writerow(
                [ID, trial, "Final_Fitness_Distribution"] + final_fitness_distribution)

    return ID


lock = Lock()

if __name__ == '__main__':
    params = []
    with open('para.csv', 'r') as read:
        csv_reader = csv.reader(read)
        header = next(csv_reader)
        print(header)
        for line in csv_reader:
            params.append(tuple(line))
    NP = int(sys.argv[1])

    pool = Pool(processes=NP, initargs=lock)
    r = pool.starmap_async(simulate, params)
    print(r.get())
