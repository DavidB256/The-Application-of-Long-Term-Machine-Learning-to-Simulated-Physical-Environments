import gene_functions
import physics_engine as pe
from time import time
from environments import Environment
from genetic_algorithm import *
import random as r

def get_fitness(dna, destination, barrier_x):
    # create unique object of gene function class for each iteration
    g = gene_functions.Gatd2(destination, barrier_x)

    # make sure to reset pos before starting again!!!!!!!!!!
    e.solids[0].pos = [-100, -100]

    # set velocity based on input functions and weights from DNA
    for i in range(2):
        e.solids[0].velocity[i] = g.input0()[i] * dna[0] + \
                                  g.input1()[i] * dna[1] + \
                                  g.input2()[i] * dna[2] + \
                                  g.input3()[i] * dna[3] + \
                                  g.input4()[i] * dna[4] + \
                                  g.input5()[i] * dna[5]

        if abs(e.solids[0].velocity[i]) >= 100:
            return 10 ** -10

    end_pos = pe.run_physics_engine(tick_length, e, time_limit)

    return 1 / (pe.distance(destination, end_pos) ** 2)

start_time = time()  # just a timer
destination = [0, 0]
barrier_x = 0

gen_count = 2000 # for how many generations training will last
mutate_chance = .55 # the odds of an organism being mutated on any given generation
full_mutate_chance = .3 # odds of an organism being replaced by a randomized organism instead of just being tweaked according to the normal distribution
standard_deviations = [.01 for i in range(6)] # how much each gene is mutated by, follows normal distribution so
gene_ranges = [(-.1, .1) for i in range(6)]
pop_size = 10 # number of organisms in the population

time_limit = 10 ** 10 # how long each fitness test will run for before just giving up
tick_length = .2 # how often the physics engine will update, smaller values create more precise simulations but take longer

e = Environment(solids=[pe.Circle(pos=[-100, -100]),
                        pe.Rect(static=True, width=100),
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

    # generate random positions of barrier and destination every n generations
    if generation % 1000 == 0:
        destination = [r.randrange(-130, 131), r.randrange(25, 131)]
        barrier_x = r.randrange(-150, 151)
        e.solids[1].pos = [barrier_x, 0]

    # calculate fitness of each organism
    for org in p.organisms:
        org.fitness = get_fitness(org.dna, destination, barrier_x)

    # do natural selection and reproduction
    p.natural_selection()
    p.reproduce('unweighted breeding')

    # mutate the population after reproduction
    for org in p.organisms:
        org.mutate(mutate_chance, full_mutate_chance, standard_deviations, gene_ranges)

# print results at end
for org in p.organisms:
    org.fitness = get_fitness(org.dna, destination, barrier_x)
    print(org.fitness, org.dna)

print('time elapsed:', time() - start_time)


# this termination function needs to be copied into physics_engine.py above the run_physics_engine() function
# it is kept here to save it, because the copy of it in physics_engine.py has to be changed for each distinct algorithm used

# def termination(environ, tick_length):
#     if distance([0, 0], environ.solids[0].velocity) == 0:
#         return True
#     return False
