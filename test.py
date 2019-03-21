import physics_engine as pe
import environments

start_pos = [0, 11.001]
x = start_pos[0]
y = start_pos[1]


def input0():
    return [x, y]
def input3():
    return [x ** 2, 0]
def input4():
    return [0, y ** 2]

vvvv = [0, 0]
dna = [4.825566117052131, 1.747478546895659, -0.4155162122089578]

for i in range(2):
    vvvv[i] = input0()[i] * dna[0] + \
              input3()[i] * dna[1] + \
              input4()[i] * dna[2]

print('vvvv', vvvv)

e = environments.Environment(solids=[pe.Circle(static=True),
                        pe.Circle(radius=1, pos=start_pos, velocity=vvvv)],
                g_type='nonuniform',
                g_strength=10)


# run the physics engine until either the termination condition is reached (termination function has to be put into the physics_engine.py
runtime = pe.run_physics_engine(.2, e, 100)
print(runtime)

# if the simulation exceeds the time limit before the termination condition is reached, or way too quickly, the organism's fitness will be virtually 0
if runtime >= 100 or runtime <= .2 * 10:
    print('fitness:', 0)
else:
    # fitness function, tries to minimize velocity while maximizing time spent before crashing back down to planet, uses normalized quantities
    velocity_magnitude = pe.distance(vvvv, [0, 0])

    norm_runtime = (runtime - .2 * 10) / (100 - .2 * 10)
    norm_velocity = velocity_magnitude / 5

    print((norm_runtime - norm_velocity) ** 2)
