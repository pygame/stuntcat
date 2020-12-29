""" For loading resources.
"""
import os

import pygame


_SFX_CACHE = {}
_GFX_CACHE = {}


def distance(pos_a, pos_b):
    """
    2D distance calculation function.

    :param pos_a: Position as a two item tuple-like.
    :param pos_b: Position as a two item tuple-like.
    """
    return ((pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2) ** 0.5


def data_path():
    """
    Get the path for the data directory.

    :return: The path.
    """
    if os.path.exists("data"):
        path = "data"
    else:
        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data",
        )
    return path


def music(amusic=None, load=True, play=True, stop=False, loop=1):
    """For loading and playing music.

    ::Example::

    music('bla.ogg', load=True, play=True)
    music(stop=True)
    """
    # perhaps the mixer is not included or initialised.
    if pygame.mixer and pygame.mixer.get_init():
        if load and not stop:
            pygame.mixer.music.load(music_path(amusic))
        if play and stop is None or stop is False:
            pygame.mixer.music.play(loop)
        elif stop:
            pygame.mixer.music.stop()


def music_path(amusic):
    """
    Get the path for the music directory.

    :param amusic: the music directory name.

    :return: The path.
    """
    return os.path.join(data_path(), "sounds", amusic)


def gfx(image, convert=False, convert_alpha=False):
    """
    Load and return an image surface from the image data directory.

    :param image: image file name.
    :param convert:
    :param convert_alpha:
    :return: Image surface.
    """
    gfx_key = (image, convert, convert_alpha)
    if gfx_key in _GFX_CACHE:
        return _GFX_CACHE[gfx_key]

    path = os.path.join(data_path(), "images", image)
    asurf = pygame.image.load(path)
    if convert:
        asurf = asurf.convert()
    if convert_alpha:
        asurf = asurf.convert_alpha()
    _GFX_CACHE[gfx_key] = asurf
    return asurf


# pylint:disable=too-many-arguments
def sfx(snd, play=False, stop=False, fadeout=None, fadein=0, loops=0):
    """
    Load and return a sound effect from the sound directory.
    :param snd:
    :param play:
    :param stop:
    :param fadeout:
    :param fadein:
    :param loops:
    :return: The sound.
    """
    snd_key = snd
    if snd_key in _SFX_CACHE:
        asound = _SFX_CACHE[snd_key]
    else:
        path = os.path.join(data_path(), "sounds", snd)
        asound = pygame.mixer.Sound(path)
        _SFX_CACHE[snd_key] = asound

    # print(snd_key, play, stop, time.time())
    if play:
        asound.play(loops=loops, fade_ms=fadein)
    if stop:
        asound.stop()
    if fadeout:
        asound.fadeout(fadeout)
    return asound
