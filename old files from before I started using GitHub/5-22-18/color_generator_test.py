import pygame as pg
from random import randrange

def rand_color():
    return randrange(10, 246), randrange(10, 246), randrange(10, 246)

disp_width = 400
disp_height = 400
tile_count = 100
tiles_per = 1 / tile_count
counter = 0
colors = [[0, 0, 0],
          [1, 0, 0], [0, 1, 0], [0, 0, 1],
          [0, 0, .5], [.5, 0, .5], [0, .5, 0], [.5, .5, 0], [.5, .5, 0], [.5, .5, 0], [.5, .5, 0], ]


pg.init()
pg.display.set_caption('graphics_engine')
game_display = pg.display.set_mode((disp_width, disp_height))

while True:
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    for i in range(tile_count ** 2):
        color = colors[counter]

        x = disp_width * tiles_per * (counter % tile_count)
        y = disp_height * tiles_per * int(counter / tile_count)
        pg.draw.rect(game_display, color, (x, y, x + disp_width * tiles_per, y + disp_height * tiles_per))

        counter += 1
