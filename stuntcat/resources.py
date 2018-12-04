""" For loading resources.
"""
import os
import time
import pygame
_sfx_cache = {}
_gfx_cache = {}

def data_path():
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
    path = os.path.join(data_path(), 'sounds', amusic)
    return path

def gfx(image, convert=False, convert_alpha=False):
    global _gfx_cache
    gfx_key = (image, convert, convert_alpha)
    if gfx_key in _gfx_cache:
        return _gfx_cache[gfx_key]

    path = os.path.join(data_path(), 'images', image)
    asurf = pygame.image.load(path)
    _gfx_cache[gfx_key] = asurf
    return asurf

def sfx(snd, play=False, stop=False):
    global _sfx_cache
    snd_key = snd
    if snd_key in _sfx_cache:
        asound = _sfx_cache[snd_key]
    else:
        path = os.path.join(data_path(), 'sounds', snd)
        asound = pygame.mixer.Sound(path)
        _sfx_cache[snd_key] = asound

    # print(snd_key, play, stop, time.time())
    if play:
        asound.play()
    if stop:
        asound.stop()
    return asound
