from random import random, randrange
import numpy as np


# class that has all genes and fitness as instance variables
class Organism:
    def __init__(self, dna):
        self.dna = dna # list of allele values

        self.fitness = 0 # determined after running algorithm, higher = better genotype

    # chooses to mutate an organism based on mutate_chance, then adds to each gene a randomly chosen value from a normal distribution whose standard deviation
    # equals the corresponding value in the list of one standard deviation for each gene, standard_deviations
    # if a rarer full mutation occurs, a genotype is replaced with a new, completely random one
    def mutate(self, mutate_chance, full_mutate_chance, standard_deviations, gene_ranges):
        rand = random()

        if rand < full_mutate_chance:
            for i, gene_range in enumerate(gene_ranges):
                self.dna[i] = randrange(gene_range[0], gene_range[1])

        elif rand < mutate_chance:
            for i in range(len(self.dna)):
                self.dna[i] += np.random.normal() * standard_deviations[i]


# contains list of genotypes as instance variable organisms and methods relating to the population
class Population:
    def __init__(self, organisms):
        self.organisms = organisms

        self.size = len(organisms)
        self.half = int(self.size / 2)

    # perform gradient natural selection in which half of the population is killed off, with odds of surviving proprtional to fitness
    def natural_selection(self):
        # clear list of organisms
        next_generation = []

        # add up fitness scores of all organisms, sort organisms by their fitnesses in a list of lists containing fitness and the index of the organism
        total_fitness = 0
        fitnesses = []
        for i, organism in enumerate(self.organisms):
            total_fitness += organism.fitness
            fitnesses.append([organism.fitness, i])
        fitnesses.sort()

        # random values between 0 and 1 are generated to designate survivors
        survivors = [random() for i in range(self.half)]
        survivors.sort()

        # if a value in the survivors list falls within the range [sum of fitnesses of all previous organisms, sum of all previous organisms and current organism),
        # it gets added to the new organisms list
        fitness_sum = 0
        survivor_index = 0
        for fitness in fitnesses:
            fitness_sum += fitness[0] / total_fitness

            while survivors[survivor_index] < fitness_sum:
                next_generation.append(self.organisms[fitness[1]])

                survivor_index += 1
                if survivor_index >= len(survivors):
                    self.organisms = next_generation
                    return

    # performs chromosomal crossing over with two DNA lists of parent orgnanisms to produce the DNA of a child
    def crossing_over(self, dna1, dna2):
        new_dna = []

        for i in range(len(dna1)):
            if random() < .5:
                new_dna.append(dna1[i])
            else:
                new_dna.append(dna2[i])

        return new_dna

    # fills in remaining 50% of population after natural selection according to desired method (cloning or breeding)
    def reproduce(self, method):
        # refill population by breeding 50 sets of parents, chosen randomly but with their odds of being chosen proportional to their fitness
        if method == 'weighted breeding':
            for i in range(self.half):
                pass

        # refill population by breeding 50 sets of parents, chosen randomly
        elif method == 'unweighted breeding':
            for i in range(self.half):
                parent1 = self.organisms[randrange(self.half)]
                parent2 = self.organisms[randrange(self.half)]

                self.organisms.append(Organism(self.crossing_over(parent1.dna, parent2.dna)))


