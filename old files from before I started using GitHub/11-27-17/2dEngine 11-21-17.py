from math import sin, cos, radians

# all measurements are in base metric units

class Solid:
    def __init__(self, position_derivs, theta, height, width, mass, static):
        self.theta = theta
        self.height = height
        self.width = width
        self.mass = mass
        self.static = static

        if position_derivs is None:
            self.position_derivs = [[0, 0], [0, 0], [0, -9.81], [0, 0]]
        else:
            self.position_derivs = [[0, 0], [0, 0], [0, 0], [0, 0]]



class Rect(Solid):
    def __init__(self, position_derivs=None, theta=0, height=1, width=1, mass=1, static=False):
        Solid.__init__(self, position_derivs, theta, height, width, mass, static)

solids = []
solids.append(Rect())

print(solids[0].mass)
