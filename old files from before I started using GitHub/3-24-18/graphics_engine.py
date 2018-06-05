import pygame as pg
from time import time
import re

# setup for display
color = {'white': (255, 255, 255), 'black': (0, 0, 0),
         'red': (255, 0, 0), 'green': (0, 255, 0),
         'blue': (0, 0, 255)}
disp_width = 500
disp_height = 500
pg.init()
pg.display.set_caption('graphics_engine')
game_display = pg.display.set_mode((disp_width, disp_height))
game_display.fill(color['white'])
game_running = True # will i need this?  probably not

f = open('output.txt', 'r')

solids = []

while game_running:
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_running = False

    line = f.readline()
    if line == '':
        break

    qm_locs = []
    qms = re.compile('\?').finditer(line)
    for qm in qms:
        qm_locs.append(qm.span()[0])

    if line[:4] == 'init':
        solids.append({})



    # for pen_theta in [i * pi / 4 for i in range(9)]:
    #     pen_x = int(cos(pen_theta) * 50 + disp_width / 2)
    #     pen_y = int(sin(pen_theta) * 50 + disp_height / 2)
    #     pg.draw.circle(game_display, color['black'], (pen_x, pen_y), (pen_radius))


pg.quit()
