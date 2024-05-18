import pygame

from global_variables import BOMB_SCALE, BOMB_COUNTDOWN, N, BOMB_STRENGTH
from utilities import load_png
from models import Position
from enum import Enum


class ExplodeDirection(Enum):
    VERTICAL = 1
    HORIZONTAL = 2

    def coord(self, bomb):
        if self == ExplodeDirection.VERTICAL:
            return bomb.xcoord
        return bomb.ycoord


class Bomb(pygame.sprite.Sprite):
    def __init__(self, position, coords, controller, strength=BOMB_STRENGTH, player_id=5):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("animations/bomb/bomb_1.png", BOMB_SCALE)
        self.rect.center = position.x, position.y
        self._coords = coords
        self.player_id = player_id
        self.placement_time = pygame.time.get_ticks()
        self.strength = strength
        self.fire = False
        self.controller = controller

    @property
    def xcoord(self):
        return self._coords.x

    @property
    def ycoord(self):
        return self._coords.y

    @property
    def coords(self):
        return self._coords

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.placement_time >= BOMB_COUNTDOWN:
            self.explode()
        if (current_time - self.placement_time) % 400 < 200:
            self.image, _ = load_png("animations/bomb/bomb_3.png", BOMB_SCALE)
        else:
            self.image, _ = load_png("animations/bomb/bomb_2.png", BOMB_SCALE)

    def explode(self):
        if self.fire:
            return
        self.fire = True

        vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for i in range(4):
            for j in range(self.strength + 1):
                coords = self.coords + tuple(j * z for z in vectors[i])
                if self.controller.is_wall(coords):
                    break
                self.controller.handle_explosion(coords, self.player_id)

        self.controller.delete_bomb(self.coords)
        self.controller.new_explosion(self.coords)
        self.controller.give_bomb(self.player_id)
        self.kill()
