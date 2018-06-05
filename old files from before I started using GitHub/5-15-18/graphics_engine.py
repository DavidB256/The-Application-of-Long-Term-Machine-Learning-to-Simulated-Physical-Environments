import pygame as pg
from time import time, sleep

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# setup for display
disp_width = 500
disp_height = 500
pg.init()
pg.display.set_caption('graphics_engine')
game_display = pg.display.set_mode((disp_width, disp_height))
game_display.fill((255, 255, 255))
running = True

f = open('output.txt', 'r')

solids = []

while running:
    pg.display.update()

    # exit condition
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    # get next line, check if it is the end of the file
    line = f.readline()
    if line == '':
        break

    # find question marks in the line
    qm_locs = []
    for i, j in enumerate(line):
        if j == '?':
            qm_locs.append(i)

    # initalize new shapes and make changes to characteristics of new ones
    if line[:4] == 'init':
        solids.append({})
        index = -1
    else:
        index = ''
        for j in line:
            if j not in digits:
                break
            index += j
        index = int(index)
    for i in range(len(qm_locs) - 1):
        term = line[qm_locs[i] + 1:qm_locs[i + 1]]
        for j in range(1, len(term)): # the starting number for j should be the minimum length for any instance variable of a solid
            if term[j] in digits + ['[']:
                split = j
                break
        # if the value is a number, convert it from string to int, if it is a list, leave it as is
        try:
            solids[index][term[:split]] = int(term[split:])
        except ValueError:
            solids[index][term[:split]] = term[split:]

    for solid in solids:
        # get x and y coordinates from sold[pos_derivs], which is a string made from a list
        for i in range(3, len(solid['pos_derivs'])):
            if solid['pos_derivs'][i] == ',':
                x = float(solid['pos_derivs'][2:i])
                comma = i
                break
        for i in range(comma + 3, len(solid['pos_derivs'])):
            if solid['pos_derivs'][i] == ']':
                y = float(solid['pos_derivs'][comma + 2:i])
                break

        if solid['shape'] == 0:
            pg.draw.rect(game_display, (0, 0, 0), (x, y, x + solid['width'], y + solid['height']))

    sleep(.1)

pg.quit()

    # for pen_theta in [i * pi / 4 for i in range(9)]:
    #     pen_x = int(cos(pen_theta) * 50 + disp_width / 2)
    #     pen_y = int(sin(pen_theta) * 50 + disp_height / 2)
    #     pg.draw.circle(game_display, color['black'], (pen_x, pen_y), (pen_radius))
