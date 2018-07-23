import pygame as pg

pg.init()

screen_h = 400
screen_w = 400
screen_center = (screen_h / 2, screen_w /2)

screen = pg.display.set_mode((400, 400))
screen.fill((255, 255, 255))

def test(center, w, h, theta, point, index):
    screen.fill((255, 255, 255))

    surface = pg.Surface((dim[2], dim[3]))
    surface.fill((50, 50, 50))
    surface.set_colorkey((255, 255, 255))

    rotated_surface = pg.transform.rotate(surface, theta)
    rotated_rect = rotated_surface.get_rect()
    rotated_rect.center = (100, 100)
    screen.blit(rotated_surface, rotated_rect)

# test 1, control
test(dim=(-100, -100, 100, 100), theta=0, point=(0, 0), index=0)
