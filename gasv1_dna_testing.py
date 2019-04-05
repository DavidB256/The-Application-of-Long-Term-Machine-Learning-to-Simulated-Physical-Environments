import gene_functions
from environments import Environment
import physics_engine as pe

dna = [-0.4782179829546539, 0.07012079426483595, 2.7799442290567735, 0.4543957971535216]

destination = [100, 100]
g = gene_functions.Gasv1(-9.81, destination)
velocity = [0, 0]

for i in range(2):
    velocity[i] = g.input0()[i] * dna[0] + \
                  g.input1()[i] * dna[1] + \
                  g.input2()[i] * dna[2] + \
                  g.input3()[i] * dna[3]

print('velocity', velocity)

e = Environment(solids=[pe.Circle(pos=[-100, .001], velocity=velocity)],
                g_type='uniform',
                g_strength=[0, -9.81])

end_pos = pe.run_physics_engine(.2, e, 10 ** 2)
print('end_pos', end_pos)

print('dist', pe.distance(end_pos, destination))
