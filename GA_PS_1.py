from genetic_algorithm import *
from random import randrange
import physics_engine as pe
from environments import Environment
from time import time

start_time = time()

e = Environment(solids=[pe.Circle(static=True),
                        pe.Circle(radius=1, pos=[0, 11.001])],
                g_type='nonuniform',
                g_strength=10)

gen_count = 1000
mutate_chance = .8
standard_deviations = [.15]
pop_size = 20
time_limit = 100
tick_length = .2

p = Population([Organism([randrange(0, 6)]) for i in range(pop_size)])


def get_fitness(organism):
    e.solids[1].pos = [0, 11.001]
    e.solids[1].velocity = [0] + organism.dna

    runtime = pe.run_physics_engine(tick_length=tick_length,
                                    environ=e,
                                    time_limit=time_limit)

    if runtime >= time_limit or runtime <= tick_length * 10:
        return .001

    velocity_magnitude = pe.distance([0] + organism.dna, [0, 0])

    norm_runtime = runtime / time_limit
    norm_velocity = velocity_magnitude / 5

    return (norm_runtime - norm_velocity) ** 2


for generation in range(gen_count):
    # print percent progress
    if (generation * 100) / gen_count % 1 == 0:
        print((generation * 100) / gen_count)


    for organism in p.organisms:
        organism.fitness = get_fitness(organism)

    p.natural_selection()
    p.reproduce('unweighted breeding')
    for organism in p.organisms:
        organism.mutate(mutate_chance, standard_deviations)


for organism in p.organisms:
    print(organism.dna, pe.distance([0] + organism.dna, [0, 0]), organism.fitness)

print('time elapsed:', time() - start_time)
