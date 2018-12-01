""" For loading resources.
"""
import os
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

def gfx(image, convert=False, convert_alpha=False):
    global _gfx_cache
    gfx_key = (image, convert, convert_alpha)
    if gfx_key in _gfx_cache:
        return _gfx_cache[gfx_key]

    path = os.path.join(data_path(), 'images', image)
    asurf = pygame.image.load(path)
    _gfx_cache[gfx_key] = asurf
    return asurf

def sfx(snd):
    global _sfx_cache
    if snd in _sfx_cache:
        return _sfx_cache[snd]

    path = os.path.join(data_path(), 'sounds', snd)
    asound = pygame.mixer.Sound(path)
    _sfx_cache[snd] = asound
    return asound
