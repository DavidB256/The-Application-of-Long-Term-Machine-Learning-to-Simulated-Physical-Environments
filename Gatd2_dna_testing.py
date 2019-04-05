import physics_engine as pe
from environments import Environment
import gene_functions
import random as r
import sys

total_distance = 1

for hyurgh in range(100):
    # print progress percentages
    if hyurgh % 10 == 0:
        print(hyurgh / 10)

    # generate random positions of barrier and destination
    destination = [r.randrange(-130, 131), r.randrange(25, 131)]
    barrier_x = r.randrange(-150, 151)

    # create unique object of gene function class for each iteration
    g = gene_functions.Gatd2(destination, barrier_x)

    stahp = False # if all you want is to translate a genotype into a velocity, make this true so that it doesn't worry about calculating fitness

    velocity = [0, 0]
    dna = [0.11870940760025564, 0.14619025558776677, -0.021505073248616467, 0.007780392065780623, 0.06793396673059486, 0.030996022553317557]

    # set velocity based on input functions and weights from DNA
    for i in range(2):
        velocity[i] = g.input0()[i] * dna[0] + \
                      g.input1()[i] * dna[1] + \
                      g.input2()[i] * dna[2] + \
                      g.input3()[i] * dna[3] + \
                      g.input4()[i] * dna[4] + \
                      g.input5()[i] * dna[5]
    # print('destination', destination)
    # print('barrier_x', barrier_x)
    # print('velocity', velocity)

    if stahp:
        sys.exit()

    e = Environment(solids=[pe.Circle(pos=[-100, -100], velocity=velocity),
                        pe.Rect(static=True, width=100, pos=[barrier_x, 0]),
                        pe.Rect(static=True, pos=[-155, 0], height=300),
                        pe.Rect(static=True, pos=[155, 0], height=300),
                        pe.Rect(static=True, pos=[0, -155], width=300),
                        pe.Rect(static=True, pos=[0, 155], width=300)],
                g_type='downward',
                g_strength=.2)


    # run the physics engine until the termination condition is reached (termination function has to be put into the physics_engine.py and return statement corrected)
    # time_limit is set to be virtually infinite because we are not worried about this environment running indefinitely, the ball will always eventually slow down to stop
    end_pos = pe.run_physics_engine(.1, e, 10 ** 10)

    total_distance += pe.distance(destination, end_pos)
    # print('end_pos', end_pos)
    # print('distance', pe.distance(destination, end_pos))
    # print()

print(total_distance)
print('total_distance', total_distance **  .001)
