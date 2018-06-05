from math import sin, cos, radians

# all measurements are in base metric units

class Solid:
    def __init__(self, x, y, theta, height, width, mass, velocity, gravity, static):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.mass = mass
        self.static = static

        if velocity is None:
            self.velocity = [0, 0]
        else:
            self.velocity = velocity

        if gravity is None:
            self.forces = {'g': [0, -9.81 * self.mass]}
        else:
            self.forces = [gravity]

    # adds a force to forces using either a list containing its x and y components or its magnitude and angle
    def add_force(self, force=None, magnitude=None, theta=None):
        if force is None:
            self.forces.append([cos(radians(theta)) * magnitude, sin(radians(theta)) * magnitude])
        else:
            self.forces.append(force)

    def update(self, t):
        # velocity =
        pass

class Rect(Solid):
    def __init__(self, x=0, y=0, theta=0, height=1, width=1, mass=1, velocity=None, gravity=None, static=False):
        Solid.__init__(self, x, y, theta, height, width, mass, velocity, gravity, static)

r1 =Rect(mass=2)
print(r1.forces)
