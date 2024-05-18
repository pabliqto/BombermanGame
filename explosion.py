import pygame

from utilities import load_png
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml', 'images_paths.toml'])


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, coords):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(settings.explosion_1, settings.block_scale)
        self.rect.center = position.x, position.y
        self.time = pygame.time.get_ticks()
        self.countdown = 400
        self.state = False
        self._coords = coords

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time >= self.countdown:
            self.kill()
        if (current_time - self.time) >= self.countdown / 2:
            self.image, _ = load_png(settings.explosion3, settings.block_scale)
        else:
            self.image, _ = load_png(settings.explosion3, settings.block_scale)

    @property
    def coords(self):
        return self._coords
