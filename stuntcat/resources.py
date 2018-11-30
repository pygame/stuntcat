""" For loading resources.
"""
import os
import pygame

def gfx(image):
    path = os.path.join('data', 'images', image)
    return pygame.image.load(path)
