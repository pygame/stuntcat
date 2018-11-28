def test_first():
    import pygame as pg
    surf = pg.Surface((1, 1))
    surf.fill((244, 0, 0))
    assert surf.get_at((0, 0)) == (244, 0, 0)


def test_game():
    from stuntcat.game import Game
    Game()
