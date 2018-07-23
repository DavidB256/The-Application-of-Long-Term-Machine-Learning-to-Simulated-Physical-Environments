import pygame as pg

pg.init()

screen = pg.display.set_mode((400, 400))
screen.fill((255, 255, 255))

theta = 45

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    surface = pg.Surface((200, 100))
    surface.fill((50, 50, 50))
    surface.set_colorkey((255, 255, 255))

    rotated_surface = pg.transform.rotate(surface, theta - 170)
    rotated_rect = rotated_surface.get_rect()
    rotated_rect.center = (100, 100)
    screen.blit(rotated_surface, rotated_rect)

    pg.draw.rect(screen, (255, 0, 0), (100, 100, 2, 2))

    pg.display.update()
