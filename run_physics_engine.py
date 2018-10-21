import physics_engine as pe
from time import time

start_time = time()

length = 10 # duration for which the simulation will run, in seconds
tick_length = .1 # length of one tick, in seconds

# create objects from the classes in physics_engine.py and put them into lists
rects = []
circles = [pe.Circle(pos=[250, 250])]

f = open('output.txt', 'w')

# write output from physics engine into output.txt, use question marks as separators between instance variables
for tick in range(int(length / tick_length)):
    for rect in rects:
        f.write(str(tick) + '?' +
                'shape' + 'Rect?' +
                'pos' + str(rect.pos) + '?' +
                'velocity' + str(rect.velocity) + '?' +
                'mass' + str(rect.mass) + '?' +
                'f_coeff' + str(rect.f_coeff) + '?' +
                'width' + str(rect.width) + '?' +
                'height' + str(rect.height) + '?' +
                'static' + str(rect.static) + '?\n')

        rect.update(tick_length)

    for circle in circles:
        f.write(str(tick) + '?' +
                'shape' + 'Circle?' +
                'pos' + str(circle.pos) + '?' +
                'velocity' + str(circle.velocity) + '?' +
                'mass' + str(circle.mass) + '?' +
                'f_coeff' + str(circle.f_coeff) + '?' +
                'radius' + str(circle.radius) + '?' +
                'static' + str(circle.static) + '?\n')

        circle.update(tick_length)

print('time elapsed', time() - start_time)
