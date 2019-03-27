import physics_engine as pe
from environments import Environment
import gene_functions

g = gene_functions.Gatd1()

velocity = [0, 0]
dna = [-2.4215988204335663, -1.0889519542788124]

for j in range(2):
    velocity[j] = g.input0()[j] * dna[0] + \
                  g.input1()[j] * dna[1]


e = Environment(solids=[pe.Circle(pos=[-100, -100], velocity=velocity),
                        pe.Rect(static=True, pos=[-155, 0], height=300),
                        pe.Rect(static=True, pos=[155, 0], height=300),
                        pe.Rect(static=True, pos=[0, -155], width=300),
                        pe.Rect(static=True, pos=[0, 155], width=300)],
                g_type='downward',
                g_strength=.2)

print(e.solids[0].velocity)

# run the physics engine until the termination condition is reached (termination function has to be put into the physics_engine.py and return statement corrected)
# time_limit is set to be virtually infinite because we are not worried about this environment running indefinitely, the ball will always eventually slow down to stop
end_pos = pe.run_physics_engine(.2, e, 10 ** 10)

print('fitness', 1 / pe.distance([0, 0], end_pos))
