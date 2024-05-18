import pygame
import random

from enum import Enum
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml', 'images_paths.toml'])


class ModifierType(Enum):
    SPEED = 1
    BOMB = 2
    FIRE = 3


class Modifier(pygame.sprite.Sprite):
    def __init__(self, position, coords, loader):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(list(ModifierType))
        if self.type == ModifierType.SPEED:
            self.image, self.rect = loader.load_png(settings.speed, settings.block_scale)
            self.value = 500
        elif self.type == ModifierType.BOMB:
            self.image, self.rect = loader.load_png(settings.bomb, settings.block_scale)
            self.value = 1
        elif self.type == ModifierType.FIRE:
            self.image, self.rect = loader.load_png(settings.fire, settings.block_scale)
            self.value = 1
        self.rect.center = position.x, position.y
        self._coords = coords

    @property
    def coords(self):
        return self._coords
