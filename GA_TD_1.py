import gene_functions
import physics_engine as pe
from time import time
from environments import Environment
import numpy as np
from genetic_algorithm import *

def get_fitness(dna, yerp=False):
    # create unique object of gene function class for each iteration
    g = gene_functions.Gatd1()

    # make sure to reset pos before starting again!!!!!!!!!!
    e.solids[0].pos = [-100, -100]

    # set velocity based on input functions and weights from DNA
    for i in range(2):
        e.solids[0].velocity[i] = g.input0()[i] * dna[0] + \
                                  g.input1()[i] * dna[1]

    end_pos = pe.run_physics_engine(tick_length, e, time_limit)

    return 1 / pe.distance([0, 0], end_pos)

start_time = time()  # just a timer

gen_count = 500 # for how many generations training will last
mutate_chance = .5 # the odds of an organism being mutated on any given generation
full_mutate_chance = .3 # odds of an organism being replaced by a randomized organism instead of just being tweaked according to the normal distribution
standard_deviations = [.1 for i in range(2)] # how much each gene is mutated by, follows normal distribution so
gene_ranges = [(-3, 3) for i in range(2)]
pop_size = 10 # number of organisms in the population

time_limit = 10 ** 10 # how long each fitness test will run for before just giving up
tick_length = .2 # how often the physics engine will update, smaller values create more precise simulations but take longer

e = Environment(solids=[pe.Circle(pos=[-100, -100]),
                        pe.Rect(static=True, pos=[-155, 0], height=300),
                        pe.Rect(static=True, pos=[155, 0], height=300),
                        pe.Rect(static=True, pos=[0, -155], width=300),
                        pe.Rect(static=True, pos=[0, 155], width=300)],
                g_type='downward',
                g_strength=.2)


# initialize population with random genes
initial_population = []
for i in range(pop_size):
    dna = []
    for gene_range in gene_ranges:
        dna.append(np.random.uniform(gene_range[0], gene_range[1]))
    initial_population.append(Organism(dna))

p = Population(initial_population)


# iterates through all generations
for generation in range(gen_count):
    # print percent progress
    if (generation * 100) / gen_count % 1 == 0:
        print((generation * 100) / gen_count)

    # calculate fitness of each organism
    for org in p.organisms:
        org.fitness = get_fitness(org.dna)

    # do natural selection and reproduction
    p.natural_selection()
    p.reproduce('unweighted breeding')

    # mutate the population after reproduction
    for org in p.organisms:
        org.mutate(mutate_chance, full_mutate_chance, standard_deviations, gene_ranges)

# print results at end
for org in p.organisms:
    org.fitness = get_fitness(org.dna, True)
    print(org.fitness, org.dna)

print('time elapsed:', time() - start_time)


# this termination function needs to be copied into physics_engine.py above the run_physics_engine() function
# it is kept here to save it, because the copy of it in physics_engine.py has to be changed for each distinct algorithm used

# def termination(environ, tick_length):
#     if distance([0, 0], environ.solids[0].velocity) <= .01:
#         return True
#     return False
