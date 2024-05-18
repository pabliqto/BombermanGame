import pygame

from global_variables import BOMB_SCALE, BOMB_COUNTDOWN, N, BOMB_STRENGTH
from utilities import load_png, calculate_position
from models import Position


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

        s_x = max(1, self.xcoord - self.strength)
        f_x = min(N, self.xcoord + self.strength + 1)
        s_y = max(1, self.ycoord - self.strength)
        f_y = min(N, self.ycoord + self.strength + 1)

        for i in range(self.xcoord, f_x):
            coords = Position(x=i, y=self.ycoord)
            if i != self.xcoord and self.controller.is_wall(coords):
                break
            self.controller.handle_explosion(coords, self.player_id)

        for i in range(self.xcoord, s_x-1, -1):
            coords = Position(x=i, y=self.ycoord)
            if i != self.xcoord and self.controller.is_wall(coords):
                break
            self.controller.handle_explosion(coords, self.player_id)

        for j in range(self.ycoord, f_y):
            coords = Position(x=self.xcoord, y=j)
            if j != self.ycoord and self.controller.is_wall(coords):
                break
            self.controller.handle_explosion(coords, self.player_id)

        for j in range(self.ycoord, s_y-1, -1):
            coords = Position(x=self.xcoord, y=j)
            if j != self.ycoord and self.controller.is_wall(coords):
                break
            self.controller.handle_explosion(coords, self.player_id)

        self.controller.delete_bomb(self.coords)
        self.controller.new_explosion(self.coords)
        self.controller.give_bomb(self.player_id)
        self.kill()
