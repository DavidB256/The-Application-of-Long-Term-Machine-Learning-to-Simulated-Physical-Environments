import pygame as pg
from time import sleep

# housekeeping
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
white = (255, 255, 255)
black = (0, 0, 0)
tick_len = .05
x = 0
y = 0
counter = 0
f = open('output.txt', 'r')
solids = []

# setup for display
disp_width = 500
disp_height = 500
pg.init()
pg.display.set_caption('graphics_engine')
game_display = pg.display.set_mode((disp_width, disp_height))
game_display.fill(white)


while True:
    # update the frame, begin new frame with a blank screen
    pg.display.update()
    game_display.fill(white)

    # exit when X in top right corner of engine window is pressed
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

    # initalize new shapes and get index of shape being created/edited in solids list
    # index refers to the index of the string at which there is the split between the name and the value
    if line[:4] == 'init':
        solids.append({})
        index = -1
    else:
        counter += 1

        index = ''
        for i in line:
            if i not in digits:
                break
            index += i
        index = int(index)

    # split variable from value for each expressions sandwiched between qms, update respective dictionary in solids list
    for i in range(len(qm_locs) - 1):
        term = line[qm_locs[i] + 1:qm_locs[i + 1]]
        for j in range(1, len(term)): # the starting number for j should be the minimum length for any instance variable of a solid
            if term[j] in digits + ['[']:
                split = j
                break
        # add the variable/update the value
        # if the value is a number, convert it from string to int, if it is a list, leave it as is and suffer the consequences
        try:
            solids[index][term[:split]] = int(term[split:])
        except ValueError:
            solids[index][term[:split]] = term[split:]

    # iterate through each existing solid to display them
    for solid in solids:
        # get x and y coordinates from sold[pos_derivs], which is a string made from a list, biting me in the ass
        for i in range(3, len(solid['pos_derivs'])):
            if solid['pos_derivs'][i] == ',':
                x = float(solid['pos_derivs'][2:i])
                comma_index = i
                break
        for i in range(comma_index + 3, len(solid['pos_derivs'])):
            if solid['pos_derivs'][i] == ']':
                y = float(solid['pos_derivs'][comma_index + 2:i])
                break

        # draw shape based on its variables recorded in its respective dict in solids list
        w = solid['width']
        h = solid['height']
        if solid['shape'] == 0:
            pg.draw.rect(game_display, (0, 0, 0), (x - int(w / 2), y - int(h / 2), w, h))
        elif solid['shape'] == 1:
            pg.draw.ellipse(game_display, (0, 0, 0), (x - int(w / 2), y - int(h / 2), w, h))

    game_display.blit(pg.font.SysFont('Arial', 12).render(str(round(counter * tick_len, 2)) + 's', 0, black), (0, 0))

    # pause between each frame
    sleep(.01)
    # input()

pg.quit() # shutdown for when main while loop is exited after whole output.txt is read
