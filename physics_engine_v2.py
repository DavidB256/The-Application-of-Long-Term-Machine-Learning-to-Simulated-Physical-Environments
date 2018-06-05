from time import time

# all measurements are in base metric units, all angles are in radians
# shapes: rect=0, circle=1

class Rect:
    def __init__(self, pos, velocity, theta=0, omega=0, height=10, width=10, mass=1, static=False):
        self.theta = theta
        self.omega = omega
        self.height = height
        self.width = width
        self.mass = mass
        self.static = static

        # sets initial position and rotation because lists can't be kept as default values in the __init__ parameters
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos
        if velocity is None:
            self.velocity = [0, 0]
        else:
            self.velocity = velocity

class

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

