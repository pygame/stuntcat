import pygame as pg


def main(args):
    try:
        gamemain(args)
    except KeyboardInterrupt:
        print('Keyboard Interrupt...')
        print('Exiting')

def gamemain(args):
    pg.init()
    clock = pg.time.Clock()
    going = True
    screen = pg.display.set_mode((320, 200))
    screen.fill((255, 0, 0))
    while going:
        for e in pg.event.get():
            if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key in [pg.K_ESCAPE, pg.K_q]:
                going = False

        pg.display.flip()
        clock.tick(30)
