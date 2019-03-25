from math import sqrt

# returns distance between two points, finds the magnitude of a vector when the other parameter is [0, 0]
def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

class Gaps2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def input0(self):
        return [self.x, self.y]
    def input3(self):
        return [self.x ** 2, 0]
    def input4(self):
        return [0, self.y ** 2]

class Gaps3:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def input0(self):
        return [self.x, self.y]
    def input1(self):
        return [1 / self.x, 0]
    def input2(self):
        return [0, 1 / self.y]
    def input3(self):
        return [self.x ** 2, 0]
    def input4(self):
        return [0, self.y ** 2]
