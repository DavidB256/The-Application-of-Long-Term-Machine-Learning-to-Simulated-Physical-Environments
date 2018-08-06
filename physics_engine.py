from math import sin, cos, radians, sqrt

# all measurements are in base metric units, all angles are in radians

# compare two border lines and return true if they intersect
def intersect(border1, border2):
    # eliminates duplicate comparisons, like line to vertical and vertical to line, in order to reduce the number of if statements needed
    # from 9 to 6
    if (border1.__class__.__name__ == 'Vertical' != border2.__class__.__name__) or \
       (border1.__class__.__name__ == 'Line' and border2.__class__.__name__ == 'Arc'):
        temp = border1
        border1 = border2
        border2 = temp

    # if border1 is a arc, then border2 can be an arc, line, or vertical
    if border1.__class__.__name__ == 'Arc':
        # for comparison to another circle, checks if the distance between then centers is less than the sum of the cirlces' radii
        if border2.__class__.__name__ == 'Arc':
            return sqrt((border1.center[0] - border2.center[0]) ** 2 +
                   (border1.center[1] - border2.center[1]) ** 2) <= border1.radius + border2.radius

        # for comparison to a line, finds if the line passes through the circle or if one of its endpoints lies within the circle
        elif border2.__class__.__name__ == 'Line':
            # this convoluted formula finds the x coordinate of the point of intersection of a line and the shortest path (a perpendicular
            # line) to a certain point (the center of the circle)
            x = (border1.center[0] - border2.y_intercept * border2.slope + border1.center[1] * border2.slope) / (border2.slope ** 2 + 1)
            y = border2.slope * x + border2.y_intercept

            return (border2.domain[0] <= x <= border2.domain[1] and
                   sqrt((x - border1.center[0]) ** 2 + (y - border1.center[1]) ** 2) <= border1.radius) or \
                   sqrt((border2.domain[0] - border1.center[0]) ** 2 +
                   (border2.slope * border2.domain[0] + border2.y_intercept - border1.center[1]) ** 2) <= border1.radius or \
                   sqrt((border2.domain[1] - border1.center[0]) ** 2 +
                   (border2.slope * border2.domain[1] + border2.y_intercept - border1.center[1]) ** 2) <= border1.radius

        # for comparison to a vertical line, find if the line passes through the circle or ends within the circle
        elif border2.__class__.__name__ == 'Vertical':
            return (border2.y_range[0] <= border1.center[1] <= border2.y_range[1] and
                   abs(border1.center[0] - border2.x_coord) <= border1.radius) or \
                   sqrt((border2.x_coord - border1.center[0]) ** 2 + (border2.y_range[0] - border1.center[1]) ** 2) <= border1.radius or \
                   sqrt((border2.x_coord - border1.center[0]) ** 2 + (border2.y_range[1] - border1.center[1]) ** 2) <= border1.radius

    # if border1 is a line, then border2 can be either a line or a vertical
    elif border1.__class__.__name__ == 'Line':
        # for comparison to another line, checks if their point of intersection lies within their domains
        if border2.__class__.__name__ == 'Line':
            # if the lines are parallel, the difference of their slopes would be 0, which would result in division by 0
            try:
                x = (border2.y_intercept - border1.y_intercept) / (border1.slope - border2.slope)
            except ZeroDivisionError:
                return False
            return border1.domain[0] <= x <= border1.domain[1] and border2.domain[0] <= x <= border2.domain[1]

        # for comparison to a vertical line, checks if their intersection lies on the domain of the line and the range of the vertical
        elif border2.__class__.__name__ == 'Vertical':
            return border1.domain[0] <= border2.x_coord <= border1.domain[1] and \
                   border2.y_range[0] <= border1.slope * border2.x_coord + border1.y_intercept <= border2.y_range[1]

    # if border1 is a vertical, then so is border2
    # for comparison to another vertical, checks if they have the same x-coordinate and their ranges overlap
    elif border1.__class__.__name__ == 'Vertical':
        return border1.x_coord == border2.x_coord and (border2.y_range[0] <= border1.y_range[0] <= border2.y_range[1] or
                                                       border2.y_range[0] <= border1.y_range[1] <= border2.y_range[1] or
                                                       border1.y_range[0] <= border2.y_range[0] <= border1.y_range[1])


# for the border of a circle, called an arc because i can't call two things circles
class Arc:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius


# for a border of a rectangle that can be expressed using y = mx + b format
class Line:
    def __init__(self, slope=None, y_intercept=None, domain=None):
        self.slope = slope
        self.y_intercept = y_intercept
        self.domain = domain


# for a vertical border of a rectangle whose tilt is a multiple of 90 degrees
class Vertical:
    def __init__(self, x_coord=None, y_range=None,):
        self.x_coord = x_coord
        self.y_range = y_range


class Solid:
    def __init__(self, pos, velocity, tilt, angular_v, mass, material, static, f_coeff):
        self.tilt = tilt # angle of object, in degrees
        self.angular_v = angular_v # angular velocity, in degrees/sec
        self.mass = mass
        self.material = material # NEED DESCRIPTION ONCE I ACTUALLY KNOW WHAT IM GONNA DO WITH THIS
        self.static = static # if True, then the object cannot be moved
        self.f_coeff = f_coeff # IDK HOW THIS IS GONNA WORK, MIGHT BE IMPLEMENTED INTO MATERIALS

        # sets initial position because lists can't be kept as default values in function parameters
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos
        if velocity is None:
            self.velocity = [0, 0]
        else:
            self.velocity = velocity

    # udpate position and tilt based on linear and rotational velocities
    def update_pos(self, t):
        for i in range(2):
            self.pos[i] += self.velocity[i] * t
        self.tilt += self.angular_v * t


# for creating a rectangular solid
class Rect(Solid):
    def __init__(self, pos=None, velocity=None, tilt=0., angular_v=0., mass=1., material=0, static=False, f_coeff=0., height=10., width=10.):
        Solid.__init__(self, pos, velocity, tilt, angular_v, mass, material, static, f_coeff)

        self.height = height
        self.width = width

        # contains 4 border objects for each of the 4 border lines of the rectangle, determined in the update method
        self.borders = [None for i in range(4)]

        # the length of the diagonal of the rectangle, used as a filter to prevent collision testing with two far-apart rectangles
        self.diagonal = sqrt(height ** 2 + width ** 2)

    def get_rect_borders(self):
        # a rectangle is the same if it is rotated by 180 degrees either way any number of times
        theta = self.tilt % 180

        # find the four corners of the rectangle
        x = self.pos[0]
        y = self.pos[1]
        adj_width = cos(radians(theta)) * self.width / 2
        opp_width = sin(radians(theta)) * self.width / 2
        adj_height = cos(radians(theta)) * self.height / 2
        opp_height = sin(radians(theta)) * self.height / 2

        tl = (x - adj_width - opp_height, # top left corner when tilt equals 0
              y + opp_width - adj_height)
        tr = (x + adj_width - opp_height, # tops right corner when tilt equals 0
              y - opp_width - adj_height)
        bl = (x - adj_width + opp_height, # bottom left corner when tilt equals 0
              y + opp_width + adj_height)
        br = (x + adj_width + opp_height, # bottom right corner when tilt equals 0
              y - opp_width + adj_height)

        # these three if statements define the lines that make up the rectangle, given the four corners
        # if tilt is 0 or 90 degrees, then we need to worry about vertical lines, so they are special cases
        # tilt cannot be a multiple of 90 that is not 0 or 90 because earlier in this function, we make sure that 0 <= tilt < 180
        if theta == 0:
            self.borders = [Line(slope=0, y_intercept=tl[1], domain=(tl[0], tr[0])),
                            Vertical(x_coord=tl[0], y_range=(bl[1], tl[1])),
                            Line(slope=0, y_intercept=bl[1], domain=(tl[0], tr[0])),
                            Vertical(x_coord=tr[0], y_range=(br[1], tr[1]))]

        # the main difference between when tilt is 0 versus when tilt is 90 degrees is that the two lines that are vertical and
        # the two lines that are normal swap
        elif theta == 90:
            self.borders = [Vertical(x_coord=tl[0], y_range=(tl[1], tr[1])),
                            Line(slope=0, y_intercept=tr[1], domain=(tl[0], bl[0])),
                            Vertical(x_coord=bl[0], y_range=(bl[1], br[1])),
                            Line(slope=0, y_intercept=tr[1], domain=(tr[0], br[0]))]

        # with any rotation that will not give us vertical lines, we can calculate the slope of lines 0 and 2, which are parallel, and then
        # use the perpendicular line formula (m_p = -1 / m) to find the slope of lines 1 and 3
        # the y_intercepts are calculated by rearranging y = mx + b into b = y - mx
        else:
            m1 = (tl[1] - tr[1]) / (tl[0] - tr[0])
            m2 = -1 / m1

            self.borders = [Line(slope=m1, y_intercept=tl[1] - m1 * tl[0]),
                            Line(slope=m2, y_intercept=tl[1] - m2 * tl[0], domain=(tl[0], bl[0])),
                            Line(slope=m1, y_intercept=br[1] - m1 * br[0]),
                            Line(slope=m2, y_intercept=br[1] - m2 * br[0], domain=(tr[0], br[0]))]

            # because the domain must be declared with the least value first, lines 0 and 2, which are initially the top and bottom
            # lines of the rectangle, must have the order of their domain reversed when the tilt is greater than 90 degrees
            if theta < 90:
                self.borders[0].domain = (tl[0], tr[0])
                self.borders[2].domain = (bl[0], br[0])
            else:
                self.borders[0].domain = (tr[0], tl[0])
                self.borders[2].domain = (br[0], bl[0])


# for creating a circular solid
class Circle(Solid):
    def __init__(self, pos=None, velocity=None, tilt=0., angular_v=0., mass=1., material=0, static=False, f_coeff=0., radius=5.):
        Solid.__init__(self, pos, velocity, tilt, angular_v, mass, material, static, f_coeff)

        self.radius = radius

        self.borders = None # contains Arc object to describe the circle's border

    def get_circle_borders(self):
        borders = Arc(self.pos, self.radius)

