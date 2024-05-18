import pygame

from utilities import load_png
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml', 'images_paths.toml'])


class Floor(pygame.sprite.Sprite):
    def __init__(self, position, coords):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(settings.floor, settings.block_scale)
        self.rect.center = position.x, position.y
        self._coords = coords

    @property
    def coords(self):
        return self._coords
