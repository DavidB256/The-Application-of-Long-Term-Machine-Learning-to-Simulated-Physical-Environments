import pygame as pg
from time import sleep
from string import digits, ascii_uppercase
from random import randrange

# housekeeping
white = (255, 255, 255)
black = (0, 0, 0)
f = open('output.txt', 'r')
tick = 0

# setup for display
disp_width = 500
disp_height = 500
pg.init()
pg.display.set_caption('physics_engine')
game_display = pg.display.set_mode((disp_width, disp_height))
game_display.fill(white)


while True:
    # update the frame after drawing each object
    pg.display.update()

    # exit when X in top right corner of window is pressed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    # get next line, quit if it is the end of the file
    line = f.readline()
    if line == '':
        break

    # find locations of question marks in the line
    qm_locs = []
    for i, char in enumerate(line):
        if char == '?':
            qm_locs.append(i)

    # clear screen if new tick, erasing shapes from previous tick
    if line[:qm_locs[0]] != tick:
        game_display.fill(white)
        tick = line[:qm_locs[0]]

    # put all instance variables of the onject described in the line into variables dictionary
    variables = {}
    for i, qm_loc in enumerate(qm_locs[1:]):
        for j, char in enumerate(line[qm_locs[i] + 1:qm_loc]):
            # find the index of the variables's value's first character, which can be either a digit for numbers,
            # an uppercase letter for booleans, or an open bracket for lists
            if char in digits + ascii_uppercase + '[':
                split_index = j + qm_locs[i] + 1
                break
        # split the section of the line between the current and previous question marks into key and value using split_index
        variables[line[qm_locs[i] + 1:split_index]] = line[split_index:qm_loc]

    # get instance variables from variables dict into the needed fomat
    x = 0
    y = 0
    for i, char in enumerate(variables['pos']):
        if char == ',':
            x = int(float(variables['pos'][1:i]))
            y = int(float(variables['pos'][i + 1:-1]))

    # draw the shape
    if variables['shape'] == 'Rect':
        w = float(variables['width'])
        h = float(variables['height'])
        pg.draw.rect(game_display, black, (x - int(w / 2) + int(disp_width / 2), -y - int(h / 2) + int(disp_height / 2), w, h))
    elif variables['shape'] == 'Circle':
        r = int(float(variables['radius']))
        pg.draw.circle(game_display, black, (x + int(disp_width / 2), -y + int(disp_height / 2)), r)

    # print tick number on screen
    game_display.blit(pg.font.SysFont('Arial', 12).render(str(tick), 0, black), (0, 0))

    # pause between each frame
    sleep(.01)

# shutdown for when main while loop is exited after all of output.txt is read
pg.quit()
