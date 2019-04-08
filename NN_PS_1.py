import physics_engine as pe
import neural_network as nn
from environments import Environment
import numpy as np
from time import time
import math

start_time = time() # just a timer

# hyperbolic tangent function, similar to sigmoid but has a range of (-1, 1) as opposed to (0, 1), used for squahsing but with negs
def tanh(x):
    return (math.e ** (2 * x) - 1) / (math.e ** (2 * x) + 1)


# config
order = 3
e = Environment(solids=[pe.Circle(pos=[-100, 0], mass=100, static=True),
                        pe.Circle(pos=[0, 0], velocity=[4, 0], mass=1, radius=1),
                        pe.Circle(pos=[50, 0], velocity=[0, 2.582], mass=20)],
                 g_type='nonuniform',
                 g_strength=10)
n = nn.NeuralNetwork(inputs=np.array([[e.g_strength / 10, e.solids[0].pos[0] / 10, e.solids[0].pos[1] / 10]]),
                     l1_size=8)

# run neural network
for i in range(10 ** order):
    # print percent progress
    if i % ((10 ** order) / 100) == 0:
        print(i / (10 ** (order - 2)))

    # # switch variables every 5 iterations
    # if i % 20 == 0:
    #     destination = destinations[int(i / 20) % 5]
    #     e.g_strength[1] = gravities[int(i / 20) % 5]

    # turn the inputs into outputs using existing weights
    n.feedforward()

    # setup for running physics engine
    initial_velocity = [n.l2[0][0] * 10, n.l1[0][1] * 10]
    e.solids[1].velocity = initial_velocity
    e.solids[1].pos = [0, 11.001]

    # run physics engine and use it in the cost function to determine error for later use in backpropagation
    final_velocity = pe.run_physics_engine(tick_length=.2, environ=e, time_limit=50)

    # modify data for optimal use by backpropagation algorithm
    difference = [initial_velocity[0] - final_velocity[0], initial_velocity[1] - final_velocity[1]]
    share_proportion = .5 - (nn.nonlin(np.random.normal()) / 2)
    complement = 1 - share_proportion
    shared_difference = [(difference[0] * complement) + (difference[1] * share_proportion),
                         (difference[1] * complement) + (difference[0] * share_proportion)]

    l2_error = np.array([-tanh(shared_difference[0] / 100), -tanh(shared_difference[1] / 100)])

    n.backpropagation(l2_error)

print('syn0')
print(n.syn0)
print('syn1')
print(n.syn1)
print('l2')
print(n.l2)

n = nn.NeuralNetwork(inputs=np.array([[-9.81 / 10, 200 / 100, 0 / 100]]),
                     l1_size=8)

print('a')

print()
print('time elapsed:', time() - start_time) # just a timer
