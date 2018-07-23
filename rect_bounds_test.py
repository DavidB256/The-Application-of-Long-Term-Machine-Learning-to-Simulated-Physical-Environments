import pygame as pg
from math import pi, sin, cos

pg.init()

screen = pg.display.set_mode((400, 400))
screen.fill((255, 255, 255))

screen_center = (200, 200)

# instance variables
w = 200
h = 100
x = -100
y = 0
theta = 300

# find endpoints
theta %= 180
theta_rads = theta / 57.2958

tl = (x - (w/2) * cos(theta_rads) - (h/2) * sin(theta_rads),
           y + (w/2) * sin(theta_rads) - (h/2) * cos(theta_rads))
tr = (x + (w/2) * cos(theta_rads) - (h/2) * sin(theta_rads),
           y - (w/2) * sin(theta_rads) - (h/2) * cos(theta_rads))
bl = (x - (w/2) * cos(theta_rads) + (h/2) * sin(theta_rads),
           y + (w/2) * sin(theta_rads) + (h/2) * cos(theta_rads))
br = (x + (w/2) * cos(theta_rads) + (h/2) * sin(theta_rads),
           y - (w/2) * sin(theta_rads) + (h/2) * cos(theta_rads))

# here we go again
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    surface = pg.Surface((w, h))
    surface.fill((50, 50, 50))
    surface.set_colorkey((255, 255, 255))

    rotated_surface = pg.transform.rotate(surface, theta)
    rotated_rect = rotated_surface.get_rect()
    rotated_rect.center = (x + screen_center[0], y + screen_center[1])
    screen.blit(rotated_surface, rotated_rect)

    pg.draw.rect(screen, (255, 0, 0), (tl[0] + screen_center[0] - 2, tl[1] + screen_center[1] - 2, 4, 4))
    pg.draw.rect(screen, (0, 255, 0), (tr[0] + screen_center[0] - 2, tr[1] + screen_center[1] - 2, 4, 4))
    pg.draw.rect(screen, (0, 0, 255), (bl[0] + screen_center[0] - 2, bl[1] + screen_center[1] - 2, 4, 4))
    pg.draw.rect(screen, (255, 0, 255), (br[0] + screen_center[0] - 2, br[1] + screen_center[1] - 2, 4, 4))

    pg.display.update()
