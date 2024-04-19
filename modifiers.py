import pygame
from global_variables import (COOLDOWN, PLAYER_SCALE, PLAYER_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, N,
                              START_X, START_Y, REAL_SIZE, BOMB_SCALE, BOMB_COUNTDOWN, PLAYERS)
from loadpng import load_png

from global_variables import BLOCK_SCALE
class Modifier(pygame.sprite.Sprite):
    def __init__(self, x, y, xcoord, ycoord, modifier_type):
        pygame.sprite.Sprite.__init__(self)
        if modifier_type == "speed":
            self.image, self.rect = load_png("modifiers\\speed.png", BLOCK_SCALE)
            self.value = 240
        elif modifier_type == "bomb":
            self.image, self.rect = load_png("modifiers\\bomb.png", BLOCK_SCALE)
            self.value = 1
        else:
            self.image, self.rect = load_png("modifiers\\fire.png", BLOCK_SCALE)
            self.value = 1
        self.rect.center = (x, y)
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.image = pygame.transform.scale(self.image, (REAL_SIZE, REAL_SIZE))
        self.type = modifier_type


