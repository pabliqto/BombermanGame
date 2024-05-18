import pygame

from global_variables import BLOCK_SCALE
from utilities import load_png


class Floor(pygame.sprite.Sprite):
    def __init__(self, position, coords):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("floor.png", BLOCK_SCALE)
        self.rect.center = position.x, position.y
        self._coords = coords

    @property
    def coords(self):
        return self._coords