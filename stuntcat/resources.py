""" For loading resources.
"""
import os
import pygame

def gfx(image):
    if os.path.exists(os.path.join('data', 'images')):
        path = os.path.join('data', 'images', image)
    else:
        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            'images',
            image
        )

    return pygame.image.load(path)
