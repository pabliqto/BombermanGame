import pygame

from global_variables import BLOCK_SCALE
from utilities import load_png


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, xcoord, ycoord):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("floor.png", BLOCK_SCALE)
        self.rect.center = (x, y)
        self.xcoord = xcoord
        self.ycoord = ycoord
