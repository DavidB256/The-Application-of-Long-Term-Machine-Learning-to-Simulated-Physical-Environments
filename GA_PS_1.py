from genetic_algorithm import *
from random import randrange
import physics_engine as pe
from environments import Environment
from time import time

start_time = time()

e = Environment(solids=[pe.Circle(static=True),
                        pe.Circle(radius=1, pos=[0, 11.01])],
                             g_type='nonuniform',
                             g_strength=10)

gen_count = 100
mutate_chance = .8
standard_deviations = [.05, .05]
pop_size = 10
time_limit = 100

p = Population([Organism([randrange(-10, 11), randrange(-10, 11)]) for i in range(pop_size)])

def termination():
    if e.solids[0].collision_type(e.solids[1]) == 'cc':
        print(1)
        return True
    return False

def get_fitness(organism):
    e.solids[1].pos[0] = 0
    e.solids[1].pos[1] = 11.1
    e.solids[1].velocity[0] = organism.dna[0]
    e.solids[1].velocity[1] = organism.dna[1]

    time = pe.run_physics_engine(tick_length=.01,
                                 environ=e,
                                 termination_func=termination(),
                                 time_limit=time_limit)

    velocity_magnitude = pe.distance(organism.dna, [0, 0])
    return 1 / (time - velocity_magnitude) ** 2


for generation in range(gen_count):
    if (generation * 100) / gen_count % 1 == 0:
        print((generation * 100) / gen_count)

    for organism in p.organisms:
        organism.fitness = get_fitness(organism)

    p.natural_selection()
    p.reproduce('unweighted breeding')
    for organism in p.organisms:
        organism.mutate(.8, [.01, .01])


total_fitness = 1
for organism in p.organisms:
    print(organism.dna, pe.distance(organism.dna, [0, 0]), organism.fitness)
    total_fitness *= organism.fitness

print('time elapsed:', time() - start_time)
