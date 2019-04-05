import numpy as np
from time import time
from environments import Environment
import physics_engine as pe
import math

# THIS CODE IS LARGELY COPIED DIRECTLY FROM https://iamtrask.github.io/2015/07/12/basic-python-network/ BECAUSE ALL NEURAL NETWORKS WORK THE SAME(ish)
# Trask, A. (2015). A Neural Network in 11 lines of Python (Part 1). iamtrask.github.io
# PLEASE DO NOT ARREST ME FOR PLAGIARISM

start_time = time() # just a timer

# sigmoid and sigmoid derivative functions
def nonlin(x, deriv=False):
    if deriv:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))

# hyperbolic tangent function, similar to sigmoid but has a range of (-1, 1) as opposed to (0, 1)
def tanh(x):
    return (math.e ** (2 * x) - 1) / (math.e ** (2 * x) + 1)

class NeuralNetwork:
    def __init__(self, inputs, destination, l1_size):
        self.inputs = inputs
        self.destination = destination

        # randomly initialize our weights with mean 0, make number of nodes in hidden layer equal to l1_size
        self.syn0 = 2 * np.random.random((inputs[0].size, l1_size)) - 1
        self.syn1 = 2 * np.random.random((l1_size, 2)) - 1

    def feedforward(self):
        # Feed forward through layers 0, 1, and 2
        self.l0 = self.inputs
        self.l1 = nonlin(np.dot(self.l0, self.syn0))
        self.l2 = nonlin(np.dot(self.l1, self.syn1))

    def backpropagation(self, l2_error):
        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        l2_delta = l2_error * nonlin(self.l2, deriv=True)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        l1_error = l2_delta.dot(self.syn1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        l1_delta = l1_error * nonlin(self.l1, deriv=True)

        self.syn1 += self.l1.T.dot(l2_delta)
        self.syn0 += self.l0.T.dot(l1_delta)


e = Environment(solids=[pe.Circle(pos=[-100, .001])],
                g_type='uniform',
                g_strength=[0, -9.81])
destination = np.array([100, 0])
n = NeuralNetwork(np.array([[e.g_strength[1], destination[0] - e.solids[0].pos[0], destination[1] - e.solids[0].pos[1]]]),
                  destination,
                  8)

# run neural network
for i in range(10 ** 4):
    n.feedforward()

    e.solids[0].velocity = [n.l2[0][0] * 100, n.l1[0][1] * 100]
    # print('l2', n.l2)
    print('vel', e.solids[0].velocity)

    end_pos = pe.run_physics_engine(tick_length=.2, environ=e, time_limit=10**3)
    print('end_pos', end_pos)
    difference = [end_pos[0] - destination[0], end_pos[1] - destination[1]]

    share_proportion = .5 - (nonlin(np.random.normal()) / 2)
    complement = 1 - share_proportion

    shared_difference = [(difference[0] * complement) + (difference[1] * share_proportion),
                         (difference[1] * complement) + (difference[0] * share_proportion)]
    print('sd', shared_difference)
    l2_error = np.array([tanh(shared_difference[0] / 100), tanh(shared_difference[1] / 100)])

    print('l2 error', l2_error)
    n.backpropagation(l2_error)

print(n.l2)

print('time elapsed:', time() - start_time) # just a timer
