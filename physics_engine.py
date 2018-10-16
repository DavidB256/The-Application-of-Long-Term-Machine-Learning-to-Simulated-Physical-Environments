from math import sqrt

# all measurements are in base metric units

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
    def __init__(self, pos=None, velocity=None, mass=1., f_coeff=0., width=10., height=10.):
        Solid.__init__(self, pos, velocity, mass, f_coeff)

        self.width = width
        self.height = height

        self.diagonal = sqrt(height ** 2 + width ** 2) # acts as a filter to prevent collision testing of two far-apart rectangles
        self.bounds = Boundaries(pos, width, height) # object containing the domain and range of the rectangle
        # idk what the source of the error in the above line is, I'm just leaving it as is

    # udpate position and bounds based velocity
    def update(self, t):
        #find distance moved in both directions
        x = self.velocity[0] * t
        y = self.velocity[1] * t

        # update position
        self.pos[0] += x
        self.pos[y] += y

        # update bounds
        self.bounds.x_min += x
        self.bounds.x_max += x
        self.boundsbounds.y_min += y
        self.bounds.y_max += y

    # returns True if the rectangle is intersecting with the other shape
    def intersecting(self, other):
        if other.__class__.__name__ == 'Rect':
            # this is just inefficientan
            # # if the rectangles are farther apart than the sum of their diagonals, there is no way that they could be touching, return False
            # if sqrt((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2) > self.diagonal + other.diagonal:
            #     return False

            x_intersecting = not((self.bounds.x_max < other.bounds.x_min) or (self.bounds.x_min > other.bounds.x_max))
            if (self.bounds.x_max < other.bounds.x_min) or (self.bounds.x_min > other.bounds.x_max):
                return False
            if (self.bounds.y_max < other.bounds.y_min) or (self.bounds.y_min > other.bounds.y_max):
                return False
            return True

        elif other.__class__.__name__ == 'Circle':
            # if the solids are farther apart than the sum of their diagonals, there is no way that they could be touching, return False
            if sqrt((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2) > self.diagonal + other.radius:
                return False



# for creating a circular solid
class Circle(Solid):
    def __init__(self, pos=None, velocity=None, mass=1., f_coeff=0., static=False, radius=5.):
        Solid.__init__(self, pos, velocity, mass, f_coeff)

        self.static = static # boolean that is False if the circle can be moved
        self.radius = radius

        self.borders = None # contains Arc object to describe the circle's border

    # udpate position based velocity
    def update(self, t):
        for i in range(2):
            self.pos[i] += self.velocity[i] * t

class Boundaries:
    def __init__(self, pos, width, height):
        self.x_min = pos[0] - (width / 2)
        self.x_max = pos[0] + (width / 2)
        self.y_min = pos[1] - (height / 2)
        self.y_max = pos[1] + (height / 2)
