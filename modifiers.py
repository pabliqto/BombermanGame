import pygame
from global_variables import REAL_SIZE, BLOCK_SCALE
from utilities import load_png
from enum import Enum
import random


class ModifierType(Enum):
    SPEED = 1
    BOMB = 2
    FIRE = 3


class Modifier(pygame.sprite.Sprite):
    def __init__(self, x, y, xcoord, ycoord):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(list(ModifierType))
        if self.type == ModifierType.SPEED:
            self.image, self.rect = load_png("modifiers\\speed.png", BLOCK_SCALE)
            self.value = 240
        elif self.type == ModifierType.BOMB:
            self.image, self.rect = load_png("modifiers\\bomb.png", BLOCK_SCALE)
            self.value = 1
        elif self.type == ModifierType.FIRE:
            self.image, self.rect = load_png("modifiers\\fire.png", BLOCK_SCALE)
            self.value = 1
        self.rect.center = (x, y)
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.image = pygame.transform.scale(self.image, (REAL_SIZE, REAL_SIZE))


