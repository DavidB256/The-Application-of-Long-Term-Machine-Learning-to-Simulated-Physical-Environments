class Line:
    def __init__(self, shape, slope=None, intercept=None, a=None, radius=None, vertical_shift=None, horizontal_shift=None, concave_up=None):
        if shape == 'sloped_line':
            self.slope = slope
            self.intercept = intercept
        elif shape == 'vertical':
            self.a = a
        elif shape == 'arc':
            self.radius = radius
            self.vertical_shift = vertical_shift
            self.horizontal_shift = horizontal_shift
            self.concave_up = concave_up

TESTINGTESTING 123