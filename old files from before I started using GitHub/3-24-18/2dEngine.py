from math import sin, cos, radians
from time import time

# all measurements are in base metric units
# shapes: rect=0, ellipse=1

class Solid:
    def __init__(self, pos_derivs, rot_derivs, height, width, mass, static):
        self.height = height
        self.width = width
        self.mass = mass
        self.static = static

        # sets initial position and rotation
        if pos_derivs is None:
            self.pos_derivs = [[0, 0], [0, 0], [0, -9.81], [0, 0]]
        else:
            self.pos_derivs = pos_derivs
        if rot_derivs is None:
            self.rot_derivs = [[0, 0], [0, 0], [0, 0], [0, 0]]
        else:
            self.rot_derivs = rot_derivs

    def update(self, t):
        # update pos derivs from s to a and round out floating point errors
        for i in range(2):
            self.pos_derivs[0][i] += (self.pos_derivs[1][i] * t) + (.5 * self.pos_derivs[2][i] * t * t) + ((1/3) * self.pos_derivs[3][i] * t * t * t)
        for i in range(2):
            self.pos_derivs[1][i] += (self.pos_derivs[2][i] * t) + (.5 * self.pos_derivs[3][i] * t * t)
        for i in range(2):
            self.pos_derivs[2][i] += self.pos_derivs[3][i] * t
        for i in range(4):
            for j in range(2):
                self.pos_derivs[i][j] = round(self.pos_derivs[i][j], 15)

        # K LET'S ADD THE SAME THING BUT FOR ROTATION LATER

class Rect(Solid):
    def __init__(self, pos_derivs=None, rot_derivs=None, height=1, width=1, mass=1, static=False):
        Solid.__init__(self, pos_derivs, rot_derivs, height, width, mass, static)

        # initializes solid in output.txt
        f.write('init' + '?' +
                'shape' + '0' + '?' +
                'pos_derivs' + str(self.pos_derivs) + '?' +
                'rot_derivs' + str(self.rot_derivs) + '?' +
                'height' + str(self.height) + '?' +
                'width' + str(self.width) + '\n')

start_time = time()

t = .1
f = open('output.txt', 'w')

solids = []
solids.append(Rect())
solids.append(Rect(pos_derivs=[[5, 0], [0, 5], [0, -9.81], [0, 0]]))

for i in range(int(1 / t)):
    for j in range(len(solids)):
        # creates txt output
        f.write(str(j) +
                'tick' + str(i) + '?' +
                'pos_derivs' + str(solids[j].pos_derivs) + '\n')

        solids[j].update(t)


print('time elapsed:', time() - start_time)
