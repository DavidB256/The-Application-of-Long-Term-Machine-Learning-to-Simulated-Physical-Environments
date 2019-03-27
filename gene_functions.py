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
    # def input1(self):
    #     return [self.x ** 2, 0]
    # def input4(self):
    #     return [0, self.y ** 2]

# gene functions for GA_TD_1
class Gatd1:
    def __init__(self):
        pass

    def input0(self):
        return [10, 0]
    def input1(self):
        return [0, 10]
