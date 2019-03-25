from genetic_algorithm import *
import random as r
import physics_engine as pe
from environments import Environment
from time import time
import gene_functions

# return a starting position along the surface of the planet for the rocket based on a given x and top, a boolean that is True if the rocket goes on top, else bottom
def get_start_pos(x, top):
    x_prime = (x * (10 + 1.001)) / 10

    y_prime = (((10.5 ** 2 - x ** 2) ** .5) * (10 + 1.001)) / 10

    if not top:
        y_prime *= -1

    return [x_prime, y_prime]

# returns fitness of an organism based on its genotype
def get_fitness(start_x, dna):
    start_pos = get_start_pos(start_x, top)
    e.solids[1].pos = [start_pos[0], start_pos[1]]

    # reset position
    g = gene_functions.Gaps3(e.solids[1].pos[0], e.solids[1].pos[1])

    # set velocity based on input functions and weights from DNA
    for i in range(2):
        e.solids[1].velocity[i] = g.input0()[i] * dna[0] + \
                                  g.input1()[i] * dna[1] + \
                                  g.input2()[i] * dna[2] + \
                                  g.input3()[i] * dna[3] + \
                                  g.input4()[i] * dna[4]

    initial_velocity = e.solids[1].velocity

    # run the physics engine until either the termination condition is reached (termination function has to be put into the physics_engine.py
    runtime = pe.run_physics_engine(tick_length, e, time_limit)

    # if the simulation exceeds the time limit before the termination condition is reached, or way too quickly, the organism's fitness will be virtually 0
    if runtime >= time_limit or runtime <= tick_length * 10:
        return .00001 # can't be 0 bc that could cause division by 0 later on

    # fitness function, tries to minimize velocity while maximizing time spent before crashing back down to planet, uses normalized quantities
    velocity_magnitude = pe.distance(initial_velocity, [0, 0])

    norm_runtime = (runtime - tick_length * 10) / (time_limit - tick_length * 10)
    norm_velocity = velocity_magnitude / 4.5

    return (norm_runtime - norm_velocity) ** 2

start_time = time() # just a timer
top = True # boolean for whether rocket is moving right along top of planet or left along bottom of planet with each generation, switches halfway through
start_x = -10 # initial x-coordinate of rocket, will be incremented with each generation so that organisms adapted to all positions/launch angles

gen_count = 1000 # for how many generations training will last
mutate_chance = .75 # the odds of an organism being mutated on any given generation
full_mutate_chance = .4 # odds of an organism being replaced by a randomized organism instead of just being tweaked according to the normal distribution
standard_deviations = [.1 for i in range(5)] # how much each gene is mutated by, follows normal distribution so
gene_ranges = [(-3, 3) for i in range(5)]
pop_size = 100 # number of organisms in the population

time_limit = 40 # how long each fitness test will run for before just giving up
tick_length = .2 # how often the physics engine will update, smaller values create more precise simulations but take longer

e = Environment(solids=[pe.Circle(static=True),
                        pe.Circle(radius=1)],
                g_type='nonuniform',
                g_strength=10)


# initialize population with random genes
initial_population = []
for i in range(pop_size):
    dna = []
    for gene_range in gene_ranges:
        dna.append(r.randrange(gene_range[0], gene_range[1]))
    initial_population.append(Organism(dna))

p = Population(initial_population)


# iterates through all generations
for generation in range(gen_count):
    # print percent progress
    if (generation * 100) / gen_count % 1 == 0:
        print((generation * 100) / gen_count)

    # have the rocket move a little bit around the surface of the planet with each generation, first it goes right along the top of the planet (top=True),
    # then it goes left along the bottom of the planet (top=False).  It loops 10 times
    if top:
        start_x += (10 * 2 * 2) / gen_count
        if start_x >= 10:
            top = False
    else:
        start_x -= (10 * 2 * 2) / gen_count
        if start_x <= -10:
            top = True

    # calculate fitness of each organism
    for org in p.organisms:
        org.fitness = get_fitness(start_x, org.dna)

    # do natural selection and reproduction
    p.natural_selection()
    p.reproduce('unweighted breeding')

    # mutate the population after reproduction
    for org in p.organisms:
        org.mutate(mutate_chance, full_mutate_chance, standard_deviations, gene_ranges)

# print results at end
for org in p.organisms:
    org.fitness = get_fitness(start_x, org.dna)
    print(org.fitness, org.dna)

print('time elapsed:', time() - start_time)


# this termination function needs to be copied into physics_engine.py above the run_physics_engine() function
# it is kept here to save it, because the copy of it in physics_engine.py has to be changed for each distinct algorithm used

# def termination(environ, tick_length):
#     next_pos = [environ.solids[1].pos[0] + (environ.solids[1].velocity[0] * tick_length), environ.solids[1].pos[1] + (environ.solids[1].velocity[1] * tick_length)]
#
#     if distance([0, 0], next_pos) <= 11:
#         return True
#     return False
