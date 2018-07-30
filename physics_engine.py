from time import time
from math import sin, cos, radians, sqrt

# all measurements are in base metric units, all angles are in radians

# compare two border lines and return true if they intersect
def intersect(border1, border2):
    if (border1.__class__.__name__ == 'Vertical' != border2.__class__.__name__) or \
       (border1.__class__.__name__ == 'Line' and border2.__class__.__name__ == 'Arc'):
        temp = border1
        border1 = border2
        border2 = temp

    if border1.shape == 'line':
        # finds if the intersection of the lines lies within their domains
        if border2.shape == 'line':
            try:
                x = (border2.y_intercept - border1.y_intercept) / (border1.slope - border2.slope)
            # if the lines are parallel, the difference of their slopes would be 0, divide by 0 = :(
            except ZeroDivisionError:
                return False
            return border1.domain[0] <= x <= border1.domain[1] and border2.domain[0] <= x <= border2.domain[1]

        # finds if the intersection of the lines lies within the domain of the sloped line and the range of the vertical line
        elif border2.shape == 'vertical':
            return border1.domain[0] <= border2.x_coord <= border1.domain[1] and \
                   border2.y_range[0] <= border1.slope * border2.x_coord + border1.y_intercept <= border2.y_range[1]

        # finds if the line passes through the circle or if one of its endpoints lies within the circle
        elif border2.shape == 'circle':
            # this convoluted formula finds the x coordinate of the point of intersection of a line and the shortest path (a perpendicular
            # line) to a certain point (the center of the circle)
            x = (border2.center[0] - border1.y_intercept * border1.slope + border2.center[1] * border1.slope) / (
            border1.slope ** 2 + 1)
            y = border1.slope * x + border1.y_intercept

            return (border1.domain[0] <= x <= border1.domain[1] and
                    sqrt((x - border2.center[0]) ** 2 + (y - border2.center[1]) ** 2) <= border2.radius) or \
                   sqrt((border1.domain[0] - border2.center[0]) ** 2 + (
                   border1.slope * border1.domain[0] + border1.y_intercept - border2.center[1]) ** 2) \
                   <= border2.radius or \
                   sqrt((border1.domain[1] - border2.center[0]) ** 2 + (
                   border1.slope * border1.domain[1] + border1.y_intercept - border2.center[1]) ** 2) \
                   <= border2.radius

    # test vertical with the three shapes
    elif border1.shape == 'vertical':
        # finds if the intersection of the lines lies within the domain of the sloped line and the range of the vertical line
        if border2.shape == 'line':
            return border2.domain[0] <= border1.x_coord <= border2.domain[1] and \
                   border1.y_range[0] <= border2.slope * border1.x_coord + border2.y_intercept <= border1.y_range[1]

        # finds if the verticals have the same x coordinate and have overlapping ranges
        elif border2.shape == 'vertical':
            return border1.x_coord == border2.x_coord and (border2.y_range[0] <= border1.y_range[0] <= border2.y_range[1] or
                                                      border2.y_range[0] <= border1.y_range[1] <= border2.y_range[1] or
                                                      border1.y_range[0] <= border2.y_range[0] <= border1.y_range[1])

        # finds if the vertical passes through the circle or if one of its endpoints lies within the circle
        elif border2.shape == 'circle':
            return (border1.y_range[0] <= border2.center[1] <= border1.y_range[1] and border2.center[
                0] - border1.x_coord <= border2.radius) or \
                   sqrt((border1.x_coord - border2.center[0]) ** 2 + (
                   border1.y_range[0] - border2.center[1]) ** 2) <= border2.radius or \
                   sqrt((border1.x_coord - border2.center[0]) ** 2 + (
                   border1.y_range[1] - border2.center[1]) ** 2) <= border2.radius

    # test circle with the three shapes
    elif border1.shape == 'circle':
        # finds if the line passes through the circle or if one of its endpoints lies within the circle
        if border2.shape == 'line':
            # this convoluted formula finds the x coordinate of the point of intersection of a line and the shortest path (a perpendicular
            # line) to a certain point (the center of the circle)
            x = (border1.center[0] - border2.y_intercept * border2.slope + border1.center[1] * border2.slope) / (
            border2.slope ** 2 + 1)
            y = border2.slope * x + border2.y_intercept

            return (border2.domain[0] <= x <= border2.domain[1] and
                    sqrt((x - border1.center[0]) ** 2 + (y - border1.center[1]) ** 2) <= border1.radius) or \
                   sqrt((border2.domain[0] - border1.center[0]) ** 2 +
                        (border2.slope * border2.domain[0] + border2.y_intercept - border1.center[1]) ** 2) <= border1.radius or \
                   sqrt((border2.domain[1] - border1.center[0]) ** 2 +
                        (border2.slope * border2.domain[1] + border2.y_intercept - border1.center[1]) ** 2) <= border1.radius

        # finds if the vertical passes through the circle or if one of its endpoints lies within the circle
        elif border2.shape == 'vertical':
            return (border2.y_range[0] <= border1.center[1] <= border2.y_range[1] and border1.center[
                0] - border2.x_coord <= border1.radius) or \
                   sqrt((border2.x_coord - border1.center[0]) ** 2 + (
                   border2.y_range[0] - border1.center[1]) ** 2) <= border1.radius or \
                   sqrt((border2.x_coord - border1.center[0]) ** 2 + (
                   border2.y_range[1] - border1.center[1]) ** 2) <= border1.radius

        # finds if the distance between the circles' centers is less than or equal to the sum of their radii
        elif border2.shape == 'circle':
            return sqrt((border1.center[0] - border2.center[0]) ** 2 + (
            border1.center[1] - border2.center[1]) ** 2) <= border1.radius + border2.radius

class Line:
    # shape can be 'line', 'vertical', or 'circle'
    # the 2nd, 3rd, and 4th lines of the following __init__ declaration contain the instance variables exclusively for
    # 'line', 'vertical', and 'circle', respectively
    # shape is the instance variable that is required for all three types, because it specifies the type
    def __init__(self, slope=None, y_intercept=None, domain=None):
        self.slope = slope
        self.y_intercept = y_intercept
        self.domain =domain

class Vertical:
    def __init__(self, x_coord=None, y_range=None,):
        self.x_coord = x_coord
        self.y_range = y_range

class Arc:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

class Rect:
    def __init__(self, pos, velocity, tilt=0., angular_v=0., height=10., width=10., mass=1., material=0, static=False, f_coeff=0.):
        self.tilt = tilt # angle of object, in degrees
        self.angular_v = angular_v # angular velocity, in degrees/sec
        self.height = height
        self.width = width
        self.mass = mass
        self.material = material # significance tbd: should it be a fixed set or more easily mutable?  does it matter?
        self.static = static # if true, the object will never move nor rotate
        self.f_coeff = f_coeff # should they be combined multiplicatively or additively

        # sets initial position because lists can't be kept as default values in function parameters
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos
        if velocity is None:
            self.velocity = [0, 0]
        else:
            self.velocity = velocity

        # will contain 4 Line objects for each of the 4 border lines of the rectangle, set in the update method
        self.borders = [None for i in range(4)]

        # the length of the diagnol of the rectangle, used as a filter to prevent collision testing with two far-apart rectangles
        self.diagonal = sqrt(height ** 2 + width ** 2)

    def update(self, t):
        # udpate position and tilt based on linear and rotational velocities
        for i in range(2):
            self.pos[i] += self.velocity * t
        self.tilt += self.angular_v * t

        # a rectangle is the same if it is rotated by 180 degrees either way any number of times
        self.tilt %= 180

        # find the four corners of the rectangle
        x = self.pos[0]
        y = self.pos[1]
        adj_width = cos(radians(self.tilt)) * self.width / 2
        opp_width = sin(radians(self.tilt)) * self.width / 2
        adj_height = cos(radians(self.tilt)) * self.height / 2
        opp_height = sin(radians(self.tilt)) * self.height / 2

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
        if self.tilt == 0:
            self.borders = [Line(shape='line', slope=0, y_intercept=tl[1], domain=(tl[0], tr[0])),
                            Line(shape='vertical', x_coord=tl[0], y_range=(bl[1], tl[1])),
                            Line(shape='line', slope=0, y_intercept=bl[1], domain=(tl[0], tr[0])),
                            Line(shape='vertical', x_coord=tr[0], y_range=(br[1], tr[1]))]

        # the main difference between when tilt is 0 versus when tilt is 90 degrees is that the two lines that are vertical and
        # the two lines that are normal swap
        elif self.tilt == 90:
            self.borders = [Line(shape='vertical', x_coord=tl[0], y_range=(tl[1], tr[1])),
                            Line(shape='line', slope=0, y_intercept=tr[1], domain=(tl[0], bl[0])),
                            Line(shape='vertical', x_coord=bl[0], y_range=(bl[1], br[1])),
                            Line(shape='line', slope=0, y_intercept=tr[1], domain=(tr[0], br[0]))]

        # with any rotation that will not give us vertical lines, we can calculate the slope of lines 0 and 2, which are parallel, and then
        # use the perpendicular line formula (m_p = -1 / m) to find the slope of lines 1 and 3
        # the y_intercepts are calculated by rearranging y = mx + b into b = y - mx
        else:
            m1 = (tl[1] - tr[1]) / (tl[0] - tr[0])
            m2 = -1 / m1

            self.borders = [Line(shape='line', slope=m1, y_intercept=tl[1] - m1 * tl[0]),
                            Line(shape='line', slope=m2, y_intercept=tl[1] - m2 * tl[0], domain=(tl[0], bl[0])),
                            Line(shape='line', slope=m1, y_intercept=br[1] - m1 * br[0]),
                            Line(shape='line', slope=m2, y_intercept=br[1] - m2 * br[0], domain=(tr[0], br[0]))]

            # because the domain must be declared with the least value first, lines 0 and 2, which are initially the top and bottom
            # lines of the rectangle, must have the order of their domain reversed when the tilt is greater than 90 degrees
            if self.tilt < 90:
                self.borders[0].domain = (tl[0], tr[0])
                self.borders[2].domain = (bl[0], br[0])
            else:
                self.borders[0].domain = (tr[0], tl[0])
                self.borders[2].domain = (br[0], bl[0])
