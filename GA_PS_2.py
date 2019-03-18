from genetic_algorithm import *
from random import randrange
import physics_engine as pe
from environments import Environment
from time import time

start_time = time()

gen_count = 1200 # for how many generations training will last
mutate_chance = .8 # the odds of an organism being mutated on any given generation
full_mutate_chance = .05 # odds of an organism being replaced by a randomized organism instead of just being tweaked according to the normal distribution
standard_deviations = [.15 for i in range(5)] # how much each gene is mutated by, follows normal distribution so
gene_ranges = [(-5, 5) for i in range(5)]
pop_size = 40 # number of organisms in the population

time_limit = 100 # how long each fitness test will run for before just giving up
tick_length = .2 # how often the physics engine will update, smaller values create more precise simulations but take longer

start_pos = [0, 11.001]
e = Environment(solids=[pe.Circle(static=True),
                        pe.Circle(radius=1, pos=start_pos)],
                g_type='nonuniform',
                g_strength=10)

# input functions whose return values will be adjusted by weights in DNA
def input0():
    return start_pos
def input1():
    return [0, pe.distance(start_pos, [0, 0])]
def input2():
    return [pe.distance(start_pos, [0, 0]), 0]
def input3():
    return [start_pos[0] ** 2, 0]
def input4():
    return [0, start_pos[1] ** 2]

# initialize population with random genes
initial_population = []
for i in range(pop_size):
    dna = []
    for gene_range in gene_ranges:
        dna.append(randrange(gene_range[0], gene_range[1]))
    initial_population.append(Organism(dna))

p = Population(initial_population)

# returns fitness of an organism based on its genotype
def get_fitness(organism):
    # reset position
    e.solids[1].pos = [start_pos[0], start_pos[1]]

    # set velocity based on input functions and weights from DNA
    for i in range(2):
        e.solids[1].velocity[i] = input0()[i] * organism.dna[0] + \
                                  input1()[i] * organism.dna[1] + \
                                  input2()[i] * organism.dna[2] + \
                                  input3()[i] * organism.dna[3] + \
                                  input4()[i] * organism.dna[4]

    # run the physics engine until either the termination condition is reached (termination function has to be put into the physics_engine.py
    runtime = pe.run_physics_engine(tick_length, e, time_limit)

    # if the simulation exceeds the time limit before the termination condition is reached, or way too quickly, the organism's fitness will be virtually 0
    if runtime >= time_limit or runtime <= tick_length * 10:
        return .001

    # fitness function, tries to minimize velocity while maximizing time spent before crashing back down to planet, uses normalized quantities
    velocity_magnitude = pe.distance([0] + organism.dna, [0, 0])

    norm_runtime = runtime / time_limit
    norm_velocity = velocity_magnitude / 5

    return (norm_runtime - norm_velocity) ** 2

# iterates through all generations
for generation in range(gen_count):
    # print percent progress
    if (generation * 100) / gen_count % 1 == 0:
        print((generation * 100) / gen_count)

    # calculate fitness of each organism
    for organism in p.organisms:
        organism.fitness = get_fitness(organism)

    # do natural selection and mutation
    p.natural_selection()
    p.reproduce('unweighted breeding')
    for organism in p.organisms:
        organism.mutate(mutate_chance, full_mutate_chance, standard_deviations, gene_ranges)


for organism in p.organisms:
    print(organism.dna, organism.fitness)

print('time elapsed:', time() - start_time)

# termination function needs to be copied into physics_engine.py above the run_physics_engine() function
# it is kept here to save it, because the copy of it in physics_engine.py has to be changed for each distinct algorithm used

# def termination(environ, tick_length):
#     next_pos = [environ.solids[1].pos[0] + (environ.solids[1].velocity[0] * tick_length), environ.solids[1].pos[1] + (environ.solids[1].velocity[1] * tick_length)]
#
#     if distance([0, 0], next_pos) <= 11:
#         return True
#     return False

