import physics_engine as pe

# gene functions for GA_PS_2, uses starting position of rocket
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

# gene functions for GA_PS_3, uses starting position of rocket
class Gaps3:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def input0(self):
        return [self.x, self.y]

    # the other two gene functions are commented out
    # def input1(self):
    #     return [self.x ** 2, 0]
    # def input4(self):
    #     return [0, self.y ** 2]

# gene functions for GA_TD_1
class Gatd1:
    def __init__(self, b):
        self.b = b
        pass

    def input0(self):
        return self.b[0]
    def input1(self):
        return self.b[1]

# gene functions for GA_TD_2, uses randomly generated destination
# location and x-coordinate of barrier, starting position of ball
class Gatd2:
    def __init__(self, destination, barrier_x):
        self.destination = destination
        self.barrier_x = barrier_x

    def input0(self):
        return [self.destination[0] + 100, 0]
    def input1(self):
        return [0, self.destination[1] + 100]
    def input2(self):
        return [self.barrier_x, 0]
    def input3(self):
        return [self.barrier_x ** 2, 0]
    def input4(self):
        return [100, 0]
    def input5(self):
        return [0, 100]

class Gasv1:
    def __init__(self, gravity, destination):
        self.gravity = gravity
        self.destination = destination

    def input0(self):
        return [0, self.gravity]
    def input1(self):
        return [0, self.gravity ** 2]
    def input2(self):
        return [0, self.destination[1]]
    def input3(self):
        return [self.destination[0] + 100, 0]
