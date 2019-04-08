import numpy as np
import math


# THIS CODE IS LARGELY COPIED DIRECTLY FROM https://iamtrask.github.io/2015/07/12/basic-python-network/ BECAUSE ALL NEURAL NETWORKS WORK THE SAME(ish)
# Trask, A. (2015). A Neural Network in 11 lines of Python (Part 1). iamtrask.github.io
# PLEASE DO NOT ARREST ME FOR PLAGIARISM


# hyperbolic tangent function, similar to sigmoid but has a range of (-1, 1) as opposed to (0, 1), used for squahsing but with negs
def tanh(x):
    return (math.e ** (2 * x) - 1) / (math.e ** (2 * x) + 1)

# sigmoid and sigmoid derivative functions
def nonlin(x, deriv=False):
    if deriv:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


class NeuralNetwork:
    def __init__(self, inputs, l1_size):
        self.inputs = inputs

        # randomly initialize our weights with mean 0, make number of nodes in hidden layer equal to l1_size
        self.syn0 = 2 * np.random.random((inputs[0].size, l1_size)) - 1
        self.syn1 = 2 * np.random.random((l1_size, 2)) - 1

    def feedforward(self, print_output=False):
        # Feed forward through layers 0, 1, and 2
        self.l0 = self.inputs
        self.l1 = nonlin(np.dot(self.l0, self.syn0))
        self.l2 = nonlin(np.dot(self.l1, self.syn1))

        if print_output:
            print('l2', self.l2)

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
