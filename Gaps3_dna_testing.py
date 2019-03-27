import physics_engine as pe
import environments
import gene_functions

start_pos = [[-11.001, .1], [.1, -11.001], [11.001, .1], [.1, 11.001], [7.8, 7.8], [-7.8, 7.8], [-7.8, -7.8], [7.8, -7.8]]

for i in start_pos:
    print('pos', i)

    x = i[0]
    y = i[1]

    g = gene_functions.Gaps3(x, y)

    velocity = [0, 0]
    dna = [0.29087740586878064]

    for j in range(2):
        velocity[j] = g.input0()[j] * dna[0]
                      # g.input1()[j] * dna[1] + \
                      # g.input4()[j] * dna[2]
    print(velocity)

            # print('velocity', velocity)

    e = environments.Environment(solids=[pe.Circle(static=True),
                            pe.Circle(radius=1, pos=i, velocity=velocity)],
                    g_type='nonuniform',
                    g_strength=10)


    # run the physics engine until either the termination condition is reached (termination function has to be put into the physics_engine.py
    runtime = pe.run_physics_engine(.2, e, 100)
    # print('runtime', runtime)

    # if the simulation exceeds the time limit before the termination condition is reached, or way too quickly, the organism's fitness will be virtually 0
    if runtime >= 100 or runtime <= .2 * 10:
        print('fitness', 0)
    else:
        # fitness function, tries to minimize velocity while maximizing time spent before crashing back down to planet, uses normalized quantities
        velocity_magnitude = pe.distance(velocity, [0, 0])

        norm_runtime = (runtime - .2 * 10) / (100 - .2 * 10)
        norm_velocity = velocity_magnitude / 5

        print('fitness', (norm_runtime - norm_velocity) ** 2)

    print()
