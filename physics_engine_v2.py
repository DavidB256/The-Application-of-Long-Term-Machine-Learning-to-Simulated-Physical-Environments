from time import time

# all measurements are in base metric units, all angles are in radians
# shapes: rect=0, circle=1

class Rect:
    def __init__(self, pos, velocity, tilt=0, angular_v=0, height=10, width=10, mass=1, static=False):
        self.tilt = tilt # angle of object, in rads
        self.angular_v = angular_v # angular velocity, in rads/sec
        self.height = height
        self.width = width
        self.mass = mass
        self.static = static # if true, the object will never move nor rotate

        # sets initial position because lists can't be kept as default values in function parameters
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos
        if velocity is None:
            self.velocity = [0, 0]
        else:
            self.velocity = velocity

    def update(self, t):
        # udpate position and tilt based on linear and rotational velocities
        for i in range(2):
            self.pos[i] += self.velocity * t
        self.tilt += self.angular_v * t

        # determine boundaries of rectangle
        
