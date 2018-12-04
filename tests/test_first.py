import pytest

@pytest.fixture(scope='session')
def pg():
    """ This initialises pygame and quits it once per session.

    Also returns pygame so it can be used as a fixture.
    """
    import pygame
    # setup.
    pygame.init()
    yield pygame
    # teardown
    pygame.quit()


def test_first(pg):
    surf = pg.Surface((1, 1), pg.SRCALPHA, 32)
    surf.fill((244, 0, 0))
    assert surf.get_at((0, 0)) == (244, 0, 0)


def test_game(pg):
    from stuntcat.game import Game
    Game()
