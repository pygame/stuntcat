""" For loading resources.
"""
import os

import pygame


_SFX_CACHE = {}
_GFX_CACHE = {}


def data_path():
    """
    Get the path for the data directory.

    :return: The path.
    """
    if os.path.exists('data'):
        path = 'data'
    else:
        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
        )
    return path


def music(amusic=None, load=True, play=True, stop=False):
    """ For loading and playing music.

    ::Example::

    music('bla.ogg', load=True, play=True)
    music(stop=True)
    """
    # perhaps the mixer is not included or initialised.
    if pygame.mixer and pygame.mixer.get_init():
        if load and not stop:
            pygame.mixer.music.load(music_path(amusic))
        if play and stop is None or stop is False:
            pygame.mixer.music.play()
        elif stop:
            pygame.mixer.music.stop()


def music_path(amusic):
    """
    Get the path for the music directory.

    :param amusic: the music directory name.

    :return: The path.
    """
    return os.path.join(data_path(), 'sounds', amusic)


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

    path = os.path.join(data_path(), 'images', image)
    asurf = pygame.image.load(path)
    if convert:
        asurf.convert()
    elif convert_alpha:
        asurf.convert_alpha()
    _GFX_CACHE[gfx_key] = asurf
    return asurf


def sfx(snd, play=False, stop=False):
    """
    Load and return a sound effect from the sound directory.
    :param snd:
    :param play:
    :param stop:
    :return: The sound.
    """
    snd_key = snd
    if snd_key in _SFX_CACHE:
        asound = _SFX_CACHE[snd_key]
    else:
        path = os.path.join(data_path(), 'sounds', snd)
        asound = pygame.mixer.Sound(path)
        _SFX_CACHE[snd_key] = asound

    # print(snd_key, play, stop, time.time())
    if play:
        asound.play()
    if stop:
        asound.stop()
    return asound
