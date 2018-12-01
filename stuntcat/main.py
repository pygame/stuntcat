import pygame as pg


def main(args):
    try:
        gamemain(args)
    except KeyboardInterrupt:
        print('Keyboard Interrupt...')
        print('Exiting')

def gamemain(args):

    from .game import Game
    Game().mainloop()
