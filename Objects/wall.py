import pygame

from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml', 'images_paths.toml'])


class Wall(pygame.sprite.Sprite):
    def __init__(self, position, coords, loader):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loader.load_png(settings.wall, settings.block_scale)
        self.rect.center = position.x, position.y
        self._coords = coords

    @property
    def coords(self):
        return self._coords
