import physics_engine as pe

length = 2 # duration for which the simulation will run, in seconds
tick = .1 # length of one tick, in seconds

solids = {'rects': [pe.Rect(velocity=(1, 0))],
          'circles': []}

f = open('output.txt', 'w')

for i in range(int(length / tick)):
    for rect in solids['rects']:
        f.write(str(i) + '?' +
                'rect?' +
                str(rect.pos) + '?' +
                str(rect.tilt) + '?' +
                str(rect.material) + '?' + # different materials will correspond to different colors
                str(rect.height) + '?' +
                str(rect.width) + '\n')

        rect.update_pos(tick)
        rect.get_rect_borders()

    for circle in solids['circles']:
        f.write(str(i) + '?' +
                'circle?' +
                str(circle.pos) + '?' +
                str(circle.tilt) + '?' + # down the line, I may want to implement a way to show the tilt of a circle in the graphics engine
                str(circle.material) + '?' +
                str(circle.radius) + '\n')

        circle.update_pos(tick)
        circle.get_circle_borders()
