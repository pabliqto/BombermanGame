import pygame

from global_variables import BLOCK_SCALE
from loadpng import load_png


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("animations/explosion/explosion1.png", BLOCK_SCALE)
        self.rect.center = (x, y)
        self.time = pygame.time.get_ticks()
        self.countdown = 400  # ?
        self.state = False  # ?

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time >= self.countdown:
            self.kill()
        if (current_time - self.time) >= self.countdown / 2:
            self.image, _ = load_png("animations/explosion/explosion3.png", BLOCK_SCALE)
        else:
            self.image, _ = load_png("animations/explosion/explosion2.png", BLOCK_SCALE)
