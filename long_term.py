import physics_engine as pe
import neural_network as nn
from environments import Environment
import numpy as np
from time import time
import random as r

start_time = time() # just a timer

def get_l2_error(difference):
    share_proportion = .5 - (nn.nonlin(np.random.normal()) / 2)
    complement = 1 - share_proportion
    shared_difference = [(difference[0] * complement) + (difference[1] * share_proportion),
                         (difference[1] * complement) + (difference[0] * share_proportion)]

    return np.array([-nn.tanh(shared_difference[0] / 100), -nn.tanh(shared_difference[1] / 100)])


# for mutating DNA so that half of its gens at random are reset
def mutate_half(dna, gene_range):
    for i in range(len(dna)):
        if r.random < .5:
            dna[i] = np.random.uniform(gene_range[0], gene_range[1])

    return dna

# for changing variables in NN runs by small amounts
def tweak(x):
    delta = x * (np.random.normal(scale=.02) + .05)

    if r.random() < .5:
        return x - delta
    return x + delta


# all 6 possible orders in which the algorithm will be introduced to the environments
orders = [['PS', 'TD', 'SV'],
          ['PS', 'SV', 'TD'],
          ['TD', 'PS', 'SV'],
          ['TD', 'SV', 'PS'],
          ['SV', 'TD', 'PS'],
          ['SV', 'PS', 'TD']]
# possible start locations for PS_1's rocket (solids[1])
ps1_starts = [[-11.001, .1], [.1, -11.001], [11.001, .1], [.1, 11.001], [7.8, 7.8], [-7.8, 7.8], [-7.8, -7.8], [7.8, -7.8]]

# 6 environments for the LT ML algorithm to use, only initialized with instance variables that will be kept constant
PS_1 = Environment(solids=[pe.Circle(static=True),
                           pe.Circle(radius=1, pos=[0, 11.01])],
                   g_type='nonuniform',
                   g_strength=100)
PS_2 = Environment(solids=[pe.Circle(static=True, pos=[-100, 0], mass=100),
                           pe.Circle(radius=1, pos=[-88.99, 0], mass=1),
                           pe.Circle(radius=3, pos=[1, 0], velocity=[0, 3.162])],
                   g_type='nonuniform',
                   g_strength=10)
TD_1 = Environment(solids=[pe.Circle(pos=[1, 1]),
                           pe.Rect(static=True, pos=[-155, 0], height=300),
                           pe.Rect(static=True, pos=[155, 0], height=300),
                           pe.Rect(static=True, pos=[0, -155], width=300),
                           pe.Rect(static=True, pos=[0, 155], width=300)],
                  g_type='downward',
                  g_strength=.2)
TD_2 = Environment(solids=[pe.Circle(pos=[-100, -100]),
                           pe.Rect(static=True, width=150, pos=[10, 0]),
                           pe.Rect(static=True, pos=[-155, 0], height=300),
                           pe.Rect(static=True, pos=[155, 0], height=300),
                           pe.Rect(static=True, pos=[0, -155], width=300),
                           pe.Rect(static=True, pos=[0, 155], width=300)],
                  g_type='downward',
                  g_strength=.2)
SV_1 = Environment(solids=[pe.Circle()],
                   g_type='uniform',
                   g_strength=[0, -9.81])
SV_2 = Environment(solids=[pe.Circle(),
                           pe.Rect(static=True, pos=[100, -450], height=1000),
                           pe.Rect(static=True, pos=[100, 600], height=1000)],
                   g_type='uniform',
                   g_strength=[0, -9.81])

# each NN run will have 10^magnitude iterations
magnitude = 2

# loop through 6 possible order of environment paths
for order in orders:
    print(order)

    # loop through each path within that order
    for path in order:
        print(path)

        if path == 'PS':
            # start things off
            e = PS_1
            time_limit = 50

            n = nn.NeuralNetwork(np.array([[e.solids[1].pos[0], e.solids[1].pos[1], e.g_strength, time_limit]]), 8)

            # run neural network
            for i in range(10 ** magnitude):
                # tweak a variable every 25 iterations
                if i % 25 == 0:
                    if (i / 25) % 3 == 0:
                        e.solids[1].pos = r.choice(ps1_starts)
                        n.inputs[0][0] = e.solids[1].pos[0]
                        n.inputs[0][1] = e.solids[1].pos[1]
                    elif (i / 25) % 3 == 1:
                        temp = tweak(e.g_strength)
                        if temp > 0:
                            e.g_strength = temp
                            n.inputs[0][2] = temp
                    else:
                        temp = tweak(time_limit)
                        if temp > 0:
                            time_limit = temp
                            n.inputs[0][3] = temp

                # turn the inputs into outputs using existing weights
                n.feedforward()

                # setup for running physics engine
                initial_velocity = [n.l2[0][0] * 10, n.l2[0][1] * 10]
                e.solids[1].velocity = initial_velocity
                e.solids[1].pos = [n.inputs[0][0], n.inputs[0][1]]

                # run physics engine and use it in the cost function to determine error for later use in backpropagation
                runtime = pe.run_physics_engine(tick_length=.2, environ=e, time_limit=time_limit, e_type='PS_1')

                # modify data for optimal use by backpropagation algorithm
                difference = [runtime, runtime]

                if i == (10 ** magnitude) - 1:
                    print('PS_1', difference)

                n.backpropagation(get_l2_error(difference))


            # start things off again
            e = PS_2
            time_limit = 50

            n.inputs = np.array([[e.solids[2].pos[0], e.solids[2].pos[1], e.g_strength, 3.162]])

            # run neural network
            for i in range(10 ** magnitude):
                # tweak a variable every 25 iterations
                if i % 25 == 0:
                    if (i / 25) % 2 == 0:
                        e.solids[2].pos[0] = tweak(e.solids[2].pos[0])
                        n.inputs[0][0] = e.solids[2].pos[0]
                    elif (i / 25) % 2 == 1:
                        temp = tweak(e.g_strength)
                        if temp > 0:
                            e.g_strength = temp
                            n.inputs[0][2] = temp

                    n.inputs[0][3] = (100 * e.g_strength / e.solids[2].pos[0])

                # turn the inputs into outputs using existing weights
                n.feedforward()

                # setup for running physics engine
                initial_velocity = [n.l2[0][0] * 10, n.l2[0][1] * 10]
                e.solids[1].velocity = initial_velocity
                e.solids[1].pos = [-88.99, 0]

                # run physics engine and use it in the cost function to determine error for later use in backpropagation
                vel = pe.run_physics_engine(tick_length=.2, environ=e, time_limit=time_limit, e_type='PS_2')

                # modify data for optimal use by backpropagation algorithm
                difference = [initial_velocity[0] - vel[0], initial_velocity[1] - vel[1]]

                if i == (10 ** magnitude) - 1:
                    print('PS_2', difference)

                n.backpropagation(get_l2_error(difference))


        elif path == 'TD':
            # start things off
            e = TD_1
            time_limit = 10 ** 3
            destination = [100, 100]

            n.inputs = np.array([[e.solids[0].pos[0], e.solids[0].pos[1], destination[0], destination[1]]])

            # run neural network
            for i in range(10 ** magnitude):
                # tweak a variable every 25 iterations
                if i % 25 == 0:
                    if (i / 25) % 4 == 0:
                        temp = tweak(e.solids[0].pos[0])
                        if abs(temp) <= 130:
                            e.solids[0].pos[0] = temp
                            n.inputs[0][0] = temp
                    elif (i / 25) % 4 == 1:
                        temp = tweak(e.solids[0].pos[1])
                        if abs(temp) <= 130:
                            e.solids[0].pos[1] = temp
                            n.inputs[0][1] = temp
                    elif (i / 25) % 4 == 2:
                        temp = tweak(destination[0])
                        if abs(temp) <= 130:
                            destination[0] = temp
                            n.inputs[0][2] = temp
                    else:
                        temp = tweak(destination[1])
                        if abs(temp) <= 130:
                            destination[1] = temp
                            n.inputs[0][3] = temp

                # turn the inputs into outputs using existing weights
                n.feedforward()

                # setup for running physics engine
                initial_velocity = [n.l2[0][0] * 10, n.l2[0][1] * 10]
                e.solids[0].velocity = initial_velocity
                e.solids[0].pos = [n.inputs[0][0], n.inputs[0][1]]

                # run physics engine and use it in the cost function to determine error for later use in backpropagation
                end_pos = pe.run_physics_engine(tick_length=.2, environ=e, time_limit=time_limit, e_type='TD_1')

                # modify data for optimal use by backpropagation algorithm
                difference = [destination[0] - end_pos[0], destination[1] - end_pos[1]]

                if i == (10 ** magnitude) - 1:
                    print('TD_1', difference)

                n.backpropagation(get_l2_error(difference))

            # start things off again
            e = TD_2
            time_limit = 10 ** 3
            destination = [100, 100]

            n.inputs = np.array([[destination[0], destination[1], e.solids[1].pos[0], 2]])

            # run neural network
            for i in range(10 ** magnitude):
                # tweak a variable every 25 iterations
                if i % 25 == 0:
                    if (i / 25) % 3 == 0:
                        temp = tweak(destination[0])
                        if abs(temp) <= 130:
                            destination[0] = temp
                            n.inputs[0][0] = temp
                    elif (i / 25) % 3 == 1:
                        temp = tweak(destination[1])
                        if 20 <= temp <= 130:
                            destination[1] = temp
                            n.inputs[0][1] = temp
                    elif (i / 25) % 3 == 2:
                        temp = tweak(e.solids[1].pos[0])
                        if abs(temp) <= 150:
                            e.solids[1].pos[0] = temp
                            n.inputs[0][2] = temp

                    # ternary value
                    if e.solids[1].pos[0] <= -75:
                        n.inputs[0][3] = 0
                    elif e.solids[1].pos[0] >= 75:
                        n.inputs[0][3] = 1
                    else:
                        n.inputs[0][3] = 2

                # turn the inputs into outputs using existing weights
                n.feedforward()

                # setup for running physics engine
                initial_velocity = [n.l2[0][0] * 10, n.l2[0][1] * 10]
                e.solids[0].velocity = initial_velocity
                e.solids[0].pos = [-100, -100]

                # run physics engine and use it in the cost function to determine error for later use in backpropagation
                end_pos = pe.run_physics_engine(tick_length=.2, environ=e, time_limit=time_limit, e_type='TD_2')

                # modify data for optimal use by backpropagation algorithm
                difference = [destination[0] - end_pos[0], destination[1] - end_pos[1]]

                if i == (10 ** magnitude) - 1:
                    print('TD_2', difference)

                n.backpropagation(get_l2_error(difference))

                n.backpropagation(get_l2_error(difference))
        elif path == 'SV':
            # start things off
            e = SV_1
            time_limit = 10 ** 2
            destination = [100, 10]

            n.inputs = np.array([[destination[0], destination[1], e.g_strength[1], 0]])

            # run neural network
            for i in range(10 ** magnitude):
                # tweak a variable every 25 iterations
                if i % 25 == 0:
                    if (i / 25) % 3 == 0:
                        destination[0] = tweak(destination[0])
                        n.inputs[0][0] = destination[0]
                    elif (i / 25) % 3 == 1:
                        destination[1] = tweak(destination[1])
                        n.inputs[0][1] = destination[1]
                    else:
                        temp = tweak(e.g_strength[1])
                        if temp > 0:
                            e.g_strength[1] = temp
                            n.inputs[0][3] = temp

                # turn the inputs into outputs using existing weights
                n.feedforward()

                # setup for running physics engine
                initial_velocity = [n.l2[0][0] * 10, n.l2[0][1] * 10]
                e.solids[0].velocity = initial_velocity
                e.solids[0].pos = [0, 0]

                # run physics engine and use it in the cost function to determine error for later use in backpropagation
                end_pos = pe.run_physics_engine(tick_length=.2, environ=e, time_limit=time_limit, e_type='SV_1', destination=destination)

                # modify data for optimal use by backpropagation algorithm
                difference = [destination[0] - end_pos[0], destination[1] - end_pos[1]]

                if i == (10 ** magnitude) - 1:
                    print('TD_1', difference)

                n.backpropagation(get_l2_error(difference))

            # start things off again
            e = SV_2
            time_limit = 10 ** 2

            n.inputs = np.array([[50, 10, 100, e.g_strength[1]]])

            # run neural network
            for i in range(10 ** magnitude):
                # tweak a variable every 25 iterations
                if i % 25 == 0:
                    if (i / 25) % 2 == 0:
                        temp = tweak(e.g_strength[1])
                        if temp > 0:
                            e.g_strength[1] = temp
                            n.inputs[0][3] = temp
                    else:
                        temp = tweak(e.solids[1].pos[0])
                        e.solids[1].pos[0] = temp
                        e.solids[2].pos[0] = temp
                        n.inputs[0][2] = temp

                # turn the inputs into outputs using existing weights
                n.feedforward()

                # setup for running physics engine
                initial_velocity = [n.l2[0][0] * 10, n.l2[0][1] * 10]
                e.solids[0].velocity = initial_velocity
                e.solids[0].pos = [0, 0]

                # run physics engine and use it in the cost function to determine error for later use in backpropagation
                end_pos = pe.run_physics_engine(tick_length=.2, environ=e, time_limit=time_limit, e_type='SV_2')

                # modify data for optimal use by backpropagation algorithm
                difference = [-e.solids[0].pos[0], -e.solids[0].pos[0]]

                if i == (10 ** magnitude) - 1:
                    print('SV_2', difference)

                n.backpropagation(get_l2_error(difference))


print('time elapsed:', time() - start_time) # just a timer
