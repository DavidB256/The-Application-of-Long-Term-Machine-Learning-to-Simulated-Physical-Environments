from genetic_algorithm import *
from random import randrange
import physics_engine as pe
from environments import Environment
from time import time
import gene_functions


# returns fitness of an organism based on its genotype
def get_fitness(dna):
    # reset position
    e.solids[1].pos = [x, y]

    g = gene_functions.Gaps2(x, y)

    # set velocity based on input functions and weights from DNA
    for i in range(2):
        e.solids[1].velocity[i] = g.input0()[i] * dna[0] + \
                                  g.input3()[i] * dna[1] + \
                                  g.input4()[i] * dna[2]

    initial_velocity = e.solids[1].velocity

    # run the physics engine until either the termination condition is reached (termination function has to be put into the physics_engine.py
    runtime = pe.run_physics_engine(tick_length, e, time_limit)

    # if the simulation exceeds the time limit before the termination condition is reached, or way too quickly, the organism's fitness will be virtually 0
    if runtime >= time_limit or runtime <= tick_length * 10:
        return .00001 # can't be 0 bc that would cause division by 0 later on

    # fitness function, tries to minimize velocity while maximizing time spent before crashing back down to planet, uses normalized quantities
    velocity_magnitude = pe.distance(initial_velocity, [0, 0])

    norm_runtime = (runtime - tick_length * 10) / (time_limit - tick_length * 10)
    norm_velocity = velocity_magnitude / 5

    return (norm_runtime - norm_velocity) ** 2

start_time = time() # just a timer

gen_count = 300 # for how many generations training will last
mutate_chance = .5 # the odds of an organism being mutated on any given generation
full_mutate_chance = .2 # odds of an organism being replaced by a randomized organism instead of just being tweaked according to the normal distribution
standard_deviations = [.1 for i in range(3)] # how much each gene is mutated by, follows normal distribution so
gene_ranges = [(-5, 5) for i in range(3)]
pop_size = 100 # number of organisms in the population

time_limit = 100 # how long each fitness test will run for before just giving up
tick_length = .2 # how often the physics engine will update, smaller values create more precise simulations but take longer

start_pos = [0, 11.001]
x = start_pos[0]
y = start_pos[1]
e = Environment(solids=[pe.Circle(static=True),
                        pe.Circle(radius=1, pos=start_pos)],
                g_type='nonuniform',
                g_strength=10)


# initialize population with random genes
initial_population = []
for i in range(pop_size):
    dna = []
    for gene_range in gene_ranges:
        dna.append(randrange(gene_range[0], gene_range[1]))
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

    # do natural selection and mutation
    p.natural_selection()
    p.reproduce('unweighted breeding')

    for org in p.organisms:
        org.mutate(mutate_chance, full_mutate_chance, standard_deviations, gene_ranges)


for org in p.organisms:
    org.fitness = get_fitness(org.dna)
    print(org.fitness, org.dna)

print('time elapsed:', time() - start_time)

# termination function needs to be copied into physics_engine.py above the run_physics_engine() function
# it is kept here to save it, because the copy of it in physics_engine.py has to be changed for each distinct algorithm used

# def termination(environ, tick_length):
#     next_pos = [environ.solids[1].pos[0] + (environ.solids[1].velocity[0] * tick_length), environ.solids[1].pos[1] + (environ.solids[1].velocity[1] * tick_length)]
#
#     if distance([0, 0], next_pos) <= 11:
#         return True
#     return False

