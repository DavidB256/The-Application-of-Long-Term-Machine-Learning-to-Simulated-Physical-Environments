from math import sqrt

# all measurements are in base metric units
# do not name any variables with uppercase letters!  it will break the graphics engine!

# returns distance between two points
def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

class Solid:
    def __init__(self, pos, velocity, mass, f_coeff):
        self.mass = mass
        self.f_coeff = f_coeff # coefficient of friction, the coefficients of two objects will be added when they move along each other

        # sets initial position and velocity because lists can't be kept as default values in function parameters
        if pos is None:
            self.pos = [0., 0.]
        else:
            self.pos = pos
        if velocity is None:
            self.velocity = [0., 0.]
        else:
            self.velocity = velocity


# for creating a rectangular solid
class Rect(Solid):
    def __init__(self, pos=None, velocity=None, mass=1., f_coeff=0., width=10., height=10., static=False):
        Solid.__init__(self, pos, velocity, mass, f_coeff)

        self.width = width
        self.height = height
        self.static = static # boolean that is False if the rectangle can be moved

        self.diagonal = sqrt(height ** 2 + width ** 2) # acts as a filter to prevent collision testing of two far-apart solids
        self.bounds = Boundaries(self.pos, width, height) # object containing the domain and range of the rectangle
        # idk what the source of the error in the above line is, I'm just leaving it as is

    # udpate position and bounds based velocity
    def update(self, t):
        #find distance moved in both directions
        x = self.velocity[0] * t
        y = self.velocity[1] * t

        # update position
        self.pos[0] += x
        self.pos[1] += y

        # update bounds
        self.bounds.x_min += x
        self.bounds.x_max += x
        self.bounds.y_min += y
        self.bounds.y_max += y

    # returns True if the rectangle is intersecting with the other shape
    def intersecting(self, other):
        if other.__class__.__name__ == 'Rect':
            if (self.bounds.x_max < other.bounds.x_min) or (self.bounds.x_min > other.bounds.x_max):
                return False
            if (self.bounds.y_max < other.bounds.y_min) or (self.bounds.y_min > other.bounds.y_max):
                return False
            return True

        elif other.__class__.__name__ == 'Circle':
            # if the solids are farther apart than the sum of their diagonals, there is no way that they could be touching, return False
            if distance(self.pos, other.pos) > self.diagonal + other.radius:
                return False

            # return true if one of the corners of the rectangle lies within the circle or the circle is touching one of the lines of the rect
            # it is best to explicitly ask about corners because the only way that a circle can touch a rectangle without its center being
            # either within the rectangle's domain or range is by including one of the corners
            if distance(other.pos, [self.bounds.x_min, self.bounds.y_min]) <= other.radius or \
               distance(other.pos, [self.bounds.x_min, self.bounds.y_max]) <= other.radius or \
               distance(other.pos, [self.bounds.x_max, self.bounds.y_min]) <= other.radius or \
               distance(other.pos, [self.bounds.x_max, self.bounds.y_max]) <= other.radius or \
               (self.bounds.x_min < other.pos[0] < self.bounds.x_max and abs(self.pos[1] - other.pos[1]) <= self.height + other.radius) or \
               (self.bounds.y_min < other.pos[1] < self.bounds.y_max and abs(self.pos[0] - other.pos[0]) <= self.width + other.radius):
                return True
            return False

    def write(self, f):


# for creating a circular solid
class Circle(Solid):
    def __init__(self, pos=None, velocity=None, mass=1., f_coeff=0., radius=5., static=False):
        Solid.__init__(self, pos, velocity, mass, f_coeff)

        self.radius = radius
        self.static = static # boolean that is False if the circle can be moved

    # udpate position based velocity
    def update(self, t):
        for i in range(2):
            self.pos[i] += self.velocity[i] * t

    def intersecting(self, other):
        if other.__class__.__name__ == 'Rect':
            # if the solids are farther apart than the sum of their diagonals, there is no way that they could be touching, return False
            if distance(self.pos, other.pos) > other.diagonal + self.radius:
                return False

            # return true if one of the corners of the rectangle lies within the circle or the circle is touching one of the lines of the rect
            # it is best to explicitly ask about corners because the only way that a circle can touch a rectangle without its center being
            # either within the rectangle's domain or range is by including one of the corners
            if distance(self.pos, [other.bounds.x_min, other.bounds.y_min]) <= self.radius or \
               distance(self.pos, [other.bounds.x_min, other.bounds.y_max]) <= self.radius or \
               distance(self.pos, [other.bounds.x_max, other.bounds.y_min]) <= self.radius or \
               distance(self.pos, [other.bounds.x_max, other.bounds.y_max]) <= self.radius or \
               (other.bounds.x_min < self.pos[0] < other.bounds.x_max and abs(self.pos[1] - other.pos[1]) <= other.height + self.radius) or \
               (other.bounds.y_min < self.pos[1] < other.bounds.y_max and abs(self.pos[0] - other.pos[0]) <= other.width + self.radius):
                return True
            return False

        elif other.__class__.__name__ == 'Circle':
            if distance(self.pos, other.pos) <= self.radius + other.radius:
                return True
            return False

# class to store boundaries of rectangle
class Boundaries:
    def __init__(self, pos, width, height):
        self.x_min = pos[0] - (width / 2)
        self.x_max = pos[0] + (width / 2)
        self.y_min = pos[1] - (height / 2)
        self.y_max = pos[1] + (height / 2)
