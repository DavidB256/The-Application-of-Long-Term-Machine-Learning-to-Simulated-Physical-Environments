from math import sqrt

# all measurements are in base metric units
# do not name any variables with uppercase letters!  it will break the graphics engine!

# collision type codes: nc = not colliding, c = circle, l = left side, r = right side, t = top side, b = bottom side, v = vertex
# 1, 2, 3, and 4 = the corners of a rectangle, with 1 in the top right and counting counterclockwise from there
# type codes are put in order, so if solid1 is a circle intersecting with solid2's right side, the collision type would be 'cr'

# returns distance between two points, finds the magnitude of a vector when the other parameter is [0, 0]
def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# returns dot product of two vectors
def dp(v1, v2):
    return (v1[0] * v2[0]) + (v1[1] * v2[1])

# calculate post-relfection velocity of an object hitting a static surface given two points on the vector perpendicular to the static object's
# surface and the dynamic object's velocity vector, uses equation: v' = v - 2(v ⋅ n)n
def reflect(p1, p2, velocity):
    x_diff = p1[0] - p2[0]
    y_diff = p1[1] - p2[1]
    magnitude = distance([x_diff, y_diff], [0, 0])
    norm_perp_v = [x_diff / magnitude, y_diff / magnitude]

    vel_perp_dp = dp(velocity, norm_perp_v)
    addend_x = norm_perp_v[0] * vel_perp_dp * -2
    addend_y = norm_perp_v[1] * vel_perp_dp * -2

    return [addend_x, addend_y]

# fix velocities of colliding objects when one is static, so energy/momentum are not transferred
def resolve_static_collision(solid_d, solid_s, intersection_type):
    if intersection_type == 'cc':
        addend = reflect(solid_d.pos, solid_s.pos, solid_d.velocity)
        solid_d.velocity[0] += addend[0]
        solid_d.velocity[1] += addend[1]

    elif intersection_type in ['cl', 'cr', 'lc', 'rc', 'lr', 'rl']:
        solid_d.velocity[0] *= -1

    elif intersection_type in ['ct', 'cb', 'tc', 'bc', 'tb', 'bt']:
        solid_d.velocity[1] *= -1

    elif intersection_type == 'c1':
        addend = reflect(solid_d.pos, [solid_s.bounds.r, solid_s.bounds.t], solid_d.velocity)
        solid_d.velocity[0] += addend[0]
        solid_d.velocity[1] += addend[1]

    elif intersection_type == 'c2':
        addend = reflect(solid_d.pos, [solid_s.bounds.l, solid_s.bounds.t], solid_d.velocity)
        solid_d.velocity[0] += addend[0]
        solid_d.velocity[1] += addend[1]

    elif intersection_type == 'c3':
        addend = reflect(solid_d.pos, [solid_s.bounds.l, solid_s.bounds.b], solid_d.velocity)
        solid_d.velocity[0] += addend[0]
        solid_d.velocity[1] += addend[1]

    elif intersection_type == 'c4':
        addend = reflect(solid_d.pos, [solid_s.bounds.r, solid_s.bounds.b], solid_d.velocity)
        solid_d.velocity[0] += addend[0]
        solid_d.velocity[1] += addend[1]

    elif intersection_type == '1c':
        addend = reflect([solid_d.bounds.r, solid_d.bounds.t], solid_s.pos, solid_d.velocity)
        solid_d.velocity[0] += addend[0]
        solid_d.velocity[1] += addend[1]

    elif intersection_type == '2c':
        addend = reflect([solid_d.bounds.l, solid_d.bounds.t], solid_s.pos, solid_d.velocity)
        solid_d.velocity[0] += addend[0]
        solid_d.velocity[1] += addend[1]

    elif intersection_type == '3c':
        addend = reflect([solid_d.bounds.l, solid_d.bounds.b], solid_s.pos, solid_d.velocity)
        solid_d.velocity[0] += addend[0]
        solid_d.velocity[1] += addend[1]

    elif intersection_type == '4c':
        addend = reflect([solid_d.bounds.r, solid_d.bounds.b], solid_s.pos, solid_d.velocity)
        solid_d.velocity[0] += addend[0]
        solid_d.velocity[1] += addend[1]

# fix velocities of colliding objects, aka "the other function"
def resolve_collision(solid1, solid2, intersection_type):
    # dealing with statics
    if solid1.static:
        # if both solids are static, do nothing
        if solid2.static:
            return
        # if solid1 is static while solid2 is dynamic, refer to the other function, swapping the order of the intersection_type
        resolve_static_collision(solid2, solid1, intersection_type[1] + intersection_type[0])
    # if solid2 is static while solid1 is dynamic, refer to the other function
    elif solid2.static:
        resolve_static_collision(solid1, solid2, intersection_type)

    # for if two circles are colliding
    if intersection_type == 'cc':
        x_diff = solid1.pos[0] - solid2.pos[0]
        y_diff = solid1.pos[1] - solid2.pos[1]
        dist = distance([x_diff, y_diff], [0, 0])
        dist_v = [x_diff, y_diff]

        norm_dist_v = [dist_v[0] / dist, dist_v[1] / dist]
        tan_v = [-norm_dist_v[1], norm_dist_v[0]]

        norm_vel_1 = dp(norm_dist_v, solid1.velocity)
        tan_vel_1 = dp(tan_v, solid1.velocity)
        norm_vel_2 = dp(norm_dist_v, solid2.velocity)
        tan_vel_2 = dp(tan_v, solid2.velocity)

# parent class for Rect and Circle
class Solid:
    def __init__(self, pos, velocity, mass, bounce, static):
        self.mass = mass
        self.bounce = bounce # percentage of kinetic energy retained upon a collision with this object, so 1 indicates most elastic
        self.static = static # boolean that is False if the solid can be moved

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
    def __init__(self, pos=None, velocity=None, mass=10., bounce=1., static=False, width=20., height=20.):
        Solid.__init__(self, pos, velocity, mass, bounce, static)

        self.width = width
        self.height = height

        self.diagonal_radius = sqrt(height ** 2 + width ** 2) / 2 # acts as a filter to prevent collision testing of two far-apart solids
        # idk what the source of the error in this line is, I'm just leaving it as is
        self.bounds = Boundaries(self.pos, width, height) # object containing the domain and range of the rectangle

    # udpate position and bounds based on velocity
    def update(self, t):
        #find distance moved in both directions
        d_x = self.velocity[0] * t
        d_y = self.velocity[1] * t

        # update position
        self.pos[0] += d_x
        self.pos[1] += d_y

        # update bounds
        self.bounds.l += d_x
        self.bounds.r += d_x
        self.bounds.t += d_y
        self.bounds.b += d_y

    # returns string based on whether circle is touching other shape, and if so, where
    def collision_type(self, other):
        if other.__class__.__name__ == 'Rect':
            # check for lr and rl
            if max(self.bounds.b, other.bounds.b) <= min(self.bounds.t, other.bounds.t):
                if (other.bounds.l <= self.bounds.l <= other.bounds.r) and (self.bounds.l <= other.bounds.r <= self.bounds.r):
                    return 'lr'
                elif (other.bounds.l <= self.bounds.r <= other.bounds.r) and (self.bounds.l <= other.bounds.l <= self.bounds.r):
                    return 'rl'

            # check for tb and bt
            if max(self.bounds.l, other.bounds.l) <= min(self.bounds.r, other.bounds.r):
                if (other.bounds.b <= self.bounds.b <= other.bounds.t) and (self.bounds.b <= other.bounds.t <= self.bounds.t):
                    return 'bt'
                elif (other.bounds.b <= self.bounds.t <= other.bounds.t) and (self.bounds.b <= other.bounds.b <= self.bounds.t):
                    return 'tb'

        elif other.__class__.__name__ == 'Circle':
            # if the solids are farther apart than the sum of their diagonals, there is no way that they could be touching, return False
            if distance(other.pos, self.pos) > self.diagonal_radius + other.radius:
                return 'nc'

            # check corners of rectangle
            if distance([self.bounds.r, self.bounds.t], other.pos) <= other.radius:
                return '1c'
            elif distance([self.bounds.l, self.bounds.t], other.pos) <= other.radius:
                return '2c'
            elif distance([self.bounds.l, self.bounds.b], other.pos) <= other.radius:
                return '3c'
            elif distance([self.bounds.r, self.bounds.b], other.pos) <= other.radius:
                return '4c'

            # check if circle intersects top or bottom
            if self.bounds.l <= other.pos[0] <= self.bounds.r:
                if other.pos[1] - other.radius <= self.bounds.t <= other.pos[1] + other.radius:
                    return 'tc'
                elif other.pos[1] - other.radius <= self.bounds.b <= other.pos[1] + other.radius:
                    return 'bc'
            # check if circle intersects left or right
            elif self.bounds.b <= other.pos[1] <= self.bounds.t:
                if other.pos[0] - other.radius <= self.bounds.r <= other.pos[0] + other.radius:
                    return 'rc'
                elif other.pos[0] - other.radius <= self.bounds.l <= other.pos[0] + other.radius:
                    return 'lc'

        return 'nc'

    # writes instance variables of object into output file
    def write(self, f, tick):
        f.write(str(tick) + '?' +
                'shape' + 'Rect?' +
                'pos' + str(self.pos) + '?' +
                'velocity' + str(self.velocity) + '?' +
                'bounce' + str(self.bounce) + '?' +
                'width' + str(self.width) + '?' +
                'height' + str(self.height) + '?\n')

# for creating a circular solid
class Circle(Solid):
    def __init__(self, pos=None, velocity=None, mass=10., bounce=1., static=False, radius=10.):
        Solid.__init__(self, pos, velocity, mass, bounce, static)

        self.radius = radius

    # udpate position based velocity
    def update(self, t):
        for i in range(2):
            self.pos[i] += self.velocity[i] * t

    # returns string based on whether circle is touching other shape, and if so, where
    def collision_type(self, other):
        if other.__class__.__name__ == 'Rect':
            # if the solids are farther apart than the sum of their diagonals, there is no way that they could be touching, return False
            if distance(self.pos, other.pos) > other.diagonal_radius + self.radius:
                return 'nc'

            # check corners of rectangle
            if distance([other.bounds.r, other.bounds.t], self.pos) <= self.radius:
                return 'c1'
            elif distance([other.bounds.l, other.bounds.t], self.pos) <= self.radius:
                return 'c2'
            elif distance([other.bounds.l, other.bounds.b], self.pos) <= self.radius:
                return 'c3'
            elif distance([other.bounds.r, other.bounds.b], self.pos) <= self.radius:
                return 'c4'

            # check if circle intersects top or bottom
            if other.bounds.l <= self.pos[0] <= other.bounds.r:
                if self.pos[1] - self.radius <= other.bounds.t <= self.pos[1] + self.radius:
                    return 'ct'
                elif self.pos[1] - self.radius <= other.bounds.b <= self.pos[1] + self.radius:
                    return 'cb'
            # check if circle intersects left or right
            elif other.bounds.b <= self.pos[1] <= other.bounds.t:
                if self.pos[0] - self.radius <= other.bounds.r <= self.pos[0] + self.radius:
                    return 'cr'
                elif self.pos[0] - self.radius <= other.bounds.l <= self.pos[0] + self.radius:
                    return 'cl'

            return 'nc'

        elif other.__class__.__name__ == 'Circle':
            if distance(self.pos, other.pos) <= self.radius + other.radius:
                return 'cc'
            return 'nc'

    # writes instance variables of object into output file
    def write(self, f, tick):
        f.write(str(tick) + '?' +
                'shape' + 'Circle?' +
                'pos' + str(self.pos) + '?' +
                'velocity' + str(self.velocity) + '?' +
                'bounce' + str(self.bounce) + '?' +
                'radius' + str(self.radius) + '?\n')

# class to store boundaries of rectangles
class Boundaries:
    def __init__(self, pos, width, height):
        self.l = pos[0] - (width / 2)
        self.r = pos[0] + (width / 2)
        self.b = pos[1] - (height / 2)
        self.t = pos[1] + (height / 2)
