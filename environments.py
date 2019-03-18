import physics_engine as pe
from random import randrange

# this file is for storing and saving environments so that run_physics_engine.py isn't overrun with many lines of commented-out code

# has an instance variable for everything that can be unique to an environment
class Environment:
    def __init__(self, solids, g_type=None, g_strength=None):
        self.solids = solids
        self.g_type = g_type
        self.g_strength = g_strength

# GA_PS_1(find escape velocity)
e9 = Environment(solids=[pe.Circle(static=True),
                         pe.Circle(radius=1, pos=[0, 11.001], velocity=[1.8803971814935971, 74.22871855340509])],
                 g_type='nonuniform',
                 g_strength=10)

# GA_PS_1(find escape velocity)
e8 = Environment(solids=[pe.Circle(static=True),
                         pe.Circle(radius=1, pos=[0, 11.001], velocity=[0, 3.7890526644854963])],
                 g_type='nonuniform',
                 g_strength=10)

# test side-view golf without friction, just bounce
e7 = Environment(solids=[pe.Circle(pos=[-100, 100], velocity=[10, 5]),
                         pe.Rect(pos=[0, -15], height=20, width=600, static=True, bounce=.7)],
                 g_type='uniform',
                 g_strength=[0, -15])

# gravity assist test
e6 = Environment(solids=[pe.Circle(pos=[-100, 0], static=True, mass=100),
                         pe.Circle(pos=[0, 0], velocity=[3, 0], mass=1, radius=1),
                         pe.Circle(pos=[50, 0], velocity=[0, 1.5], mass=20)],
                 g_type='nonuniform',
                 g_strength=10)

# worst moon ever
e5 = Environment(solids=[pe.Circle(static=True, mass=1000),
                         pe.Circle(pos=[50, 0], velocity=[0, 15], mass=100),
                         pe.Circle(pos=[65, 0], velocity=[1, 0], radius=1, mass=1)],
                 g_type='nonuniform',
                 g_strength=10)

# rectangle bouncing in a box with standard gravity
e4 = Environment(solids=[pe.Rect(pos=[0, 0], velocity=[15, 20]),
                         pe.Rect(pos=[-55, 0], height=100, width=10, static=True, bounce=.9),
                         pe.Rect(pos=[55, 0], height=100, width=10, static=True, bounce=.9),
                         pe.Rect(pos=[0, 55], height=10, width=100, static=True, bounce=.9),
                         pe.Rect(pos=[0, -55], height=10, width=100, static=True, bounce=.9)],
                 g_type='uniform',
                 g_strength=[0, -20])

# small circles bouncing around in a box
e3 = Environment(solids=[pe.Circle(pos=[randrange(-45, 45), randrange(-45, 45)], velocity=[randrange(-25, 25), randrange(-25, 25)], radius=3) for i in range(10)] + \
                         [pe.Rect(pos=[-55, 0], height=100, width=10, static=True),
                          pe.Rect(pos=[55, 0], height=100, width=10, static=True),
                          pe.Rect(pos=[0, 55], height=10, width=100, static=True),
                          pe.Rect(pos=[0, -55], height=10, width=100, static=True)])

# for testing basic collisions with a static circle
e2 = Environment(solids=[pe.Circle(pos=[40, 14], velocity=[-5, 0]),
                         pe.Circle(static=True),
                         pe.Rect(pos=[-40, 17], velocity=[5, 0])])

# ball rolling on a flat surface
e1 = Environment(solids=[pe.Rect(pos=[0, -20], width=300, static=True, bounce=.99),
                         pe.Circle(velocity=[5, 0])],
                 g_type='uniform',
                 g_strength=[0, -40])
