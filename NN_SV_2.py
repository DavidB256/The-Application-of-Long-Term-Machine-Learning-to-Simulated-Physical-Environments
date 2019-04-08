import physics_engine as pe
import neural_network as nn
from environments import Environment
import numpy as np
from time import time
import math

start_time = time() # just a timer


# config
order = 6
e = Environment(solids=[pe.Circle(pos=[-100, .001])],
                g_type='uniform',
                g_strength=[0, -9.81])
destinations = [[0, 0], [100, 0], [200, 0], [100, 0], [200, 0]]
gravities = [-9.81, -9.81, -9.81, -20, -20]
n = nn.NeuralNetwork(inputs=np.array([[0, 0, 0]]),
                     l1_size=8)

# run neural network
for i in range(10 ** order):
    # print percent progress
    if i % ((10 ** order) / 100) == 0:
        print(i / (10 ** (order - 2)))

    # switch variables every 5 iterations
    if i % 20 == 0:
        destination = destinations[int(i / 20) % 5]
        e.g_strength[1] = gravities[int(i / 20) % 5]

    n.inputs[0] = [e.g_strength[1] / 10, (destination[0] + 100) / 100, (destination[1] + 0) / 100]

    # turn the inputs into outputs using existing weights
    n.feedforward()

    # setup for running physics engine
    e.solids[0].velocity = [n.l2[0][0] * 100, n.l2[0][1] * 100]
    e.solids[0].pos = [-100, .001]

    # run physics engine and use it in the cost function to determine error for later use in backpropagation
    end_pos = pe.run_physics_engine(tick_length=.2, environ=e, time_limit=10**3)

    # modify data for optimal use by backpropagation algorithm
    difference = [end_pos[0] - destination[0], end_pos[1] - destination[1]]
    share_proportion = .5 - (nn.nonlin(np.random.normal()) / 2)
    complement = 1 - share_proportion
    shared_difference = [(difference[0] * complement) + (difference[1] * share_proportion),
                         (difference[1] * complement) + (difference[0] * share_proportion)]
    l2_error = np.array([-nn.tanh(shared_difference[0] / 100), -nn.tanh(shared_difference[1] / 100)])

    n.backpropagation(l2_error)

print('syn0')
print(n.syn0)
print('syn1')
print(n.syn1)
print('l2')
print(n.l2)

n.inputs = np.array([[-9.81 / 10, 200 / 100, 0 / 100]])

print('a')
n.inputs[0][1] = 4
n.feedforward(print_output=True)
print('b')
n.inputs[0][1] = 1
n.feedforward(print_output=True)
print('c')
n.inputs[0][1] = 2
n.inputs[0][0] = -2
n.feedforward(print_output=True)

print()
print('time elapsed:', time() - start_time) # just a timer

