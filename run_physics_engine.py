from time import time
from environments import *
from graphics_engine import *

start_time = time()

length = 30 # duration for which the simulation will run, in seconds
tick_length = .1 # length of one tick, in seconds

# choose saved environment
e = e4

f = open('output.txt', 'w') # choose doc to write into

# iterate through time
for tick in range(int(length / tick_length)):
    for solid in e.solids:
        # update velocities of non-static solids based on uniform gravity
        if e.g_type == 'uniform':
            if not solid.static:
                for i in range(2):
                    solid.velocity[i] += e.g_strength[i] * tick_length

        # update velocities of non-static solids based on nonuniform gravity
        elif e.g_type == 'nonuniform':
            if not solid.static:
                for other in e.solids:
                    # don't let it apply gravity upon itself
                    if solid.pos == other.pos:
                        continue

                    # normalize velocity vector
                    x_diff = other.pos[0] - solid.pos[0]
                    y_diff = other.pos[1] - solid.pos[1]
                    dist = pe.distance(solid.pos, other.pos)
                    norm_dist_v = [x_diff / dist, y_diff / dist]
                    # formula for acceleration derived from Newton's formula for universal gravitation
                    g = (e.g_strength * other.mass) / ((solid.pos[0] - other.pos[0]) ** 2 + (solid.pos[1] - other.pos[1]) ** 2)

                    # use normalized vector, acceleration, and tick length to adjust velocity in either direction
                    for i in range(2):
                        solid.velocity[i] += norm_dist_v[i] * g * tick_length

        # write info of and update each solid
        solid.write(f, tick)
        solid.update(tick_length)

    # detect and resolve intersections
    for i, solid1 in enumerate(e.solids[:-1]):
        for solid2 in e.solids[i + 1:]:
            ct = solid1.collision_type(solid2)
            # nc means "not colliding"
            if ct != 'nc':
                # resolve the collision
                pe.resolve_collision(solid1, solid2, ct)

                #account for loss of kinetic energy due to collision: v^2' = v^2 * bounce --> v' = v * sqrt(bounce)
                for j in range(2):
                    solid1.velocity[j] *= solid2.bounce ** .5
                    solid2.velocity[j] *= solid1.bounce ** .5

                # have a solid bounce back away from its collider to prevent one object just sinking into another
                solid1.update(tick_length)
                solid2.update(tick_length)

print('time elapsed:', time() - start_time)
# run graphics of simulation immediately after processing it
display_graphics(save_loc=r'C:\Users\David\Desktop\physics sims\frames\\', sleep_time=0)
