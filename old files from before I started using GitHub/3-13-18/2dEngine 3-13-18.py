from math import sin, cos, radians
from time import time

# all measurements are in base metric units

class Solid:
    def __init__(self, pos_derivs, rot_derivs, height, width, mass, static):
        self.height = height
        self.width = width
        self.mass = mass
        self.static = static

        if rot_derivs is None:
            self.rot_derivs = [[0, 0], [0, 0], [0, 0], [0, 0]]
        else:
            self.rot_derivs = rot_derivs
        if pos_derivs is None:
            self.pos_derivs = [[0, 0], [0, 0], [0, -9.81], [0, 0]]
        else:
            self.pos_derivs = pos_derivs

    def update(self, t):
        # update pos derivs from a to x, using eqs derived via calc
        for i in range(2):
            self.pos_derivs[2][i] += self.pos_derivs[3][i] * t
        for i in range(2):
            self.pos_derivs[1][i] += (self.pos_derivs[2][i] * t) + (.5 * self.pos_derivs[3][i] * t * t)
        for i in range(2):
            self.pos_derivs[0][i] += (self.pos_derivs[1][i] * t) + (.5 * self.pos_derivs[2][i] * t * t) + ((1/3) * self.pos_derivs[3][i] * t * t * t)

        # update pos derivs from x to a, same as above code but in reverse, less accurate for some reason
        # for i in range(2):
        #     self.pos_derivs[0][i] += (self.pos_derivs[1][i] * t) + (.5 * self.pos_derivs[2][i] * t * t) + ((1/3) * self.pos_derivs[3][i] * t * t * t)
        # for i in range(2):
        #     self.pos_derivs[1][i] += (self.pos_derivs[2][i] * t) + (.5 * self.pos_derivs[3][i] * t * t)
        # for i in range(2):
        #     self.pos_derivs[2][i] += self.pos_derivs[3][i] * t

        #K LET'S ADD THE SAME THING BUT FOR ROT

class Rect(Solid):
    def __init__(self, pos_derivs=None, rot_derivs=None, height=1, width=1, mass=1, static=False):
        Solid.__init__(self, pos_derivs, rot_derivs, height, width, mass, static)

start_time = time()

t = .01
solids = [Rect()]

for i in range(100):
    for solid in solids:
        solid.update(t)
        print(solid.pos_derivs)

print('time elapsed:', time() - start_time)
