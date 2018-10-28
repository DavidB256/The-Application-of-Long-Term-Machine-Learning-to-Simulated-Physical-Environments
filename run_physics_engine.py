import physics_engine as pe
from time import time

start_time = time()

length = 20 # duration for which the simulation will run, in seconds
tick_length = .1 # length of one tick, in seconds

# create objects from the classes in physics_engine.py
solids = [pe.Circle(pos=[-50, 0], velocity=[5, 0], radius=10),
          pe.Circle(pos=[50, 0], velocity=[-5, 0], radius=10),
          pe.Circle(pos=[0, -50], velocity=[0, 5], radius=10),
          pe.Circle(pos=[0, 50], velocity=[0, -5], radius=10)]

f = open('output.txt', 'w')

# iterate through time
for tick in range(int(length / tick_length)):
    # write info of and update each solid
    for solid in solids:
        solid.write(f, tick)
        solid.update(tick_length)

    # detect and resolve intersections
    for i, solid1 in enumerate(solids[:-1]):
        for solid2 in solids[i + 1:]:
            pe.resolve_collision(solid1, solid2, solid1.colliding(solid2))

print('time elapsed:', time() - start_time)
