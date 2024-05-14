import pygame

from global_variables import BOMB_SCALE, BOMB_COUNTDOWN, N, BOMB_STRENGTH
from utilities import load_png, calculate_position


class Bomb(pygame.sprite.Sprite):
    def __init__(self, xcoord, ycoord, controller, strength=BOMB_STRENGTH, player_id=5, number=-1):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("animations/bomb/bomb_1.png", BOMB_SCALE)
        self.rect.center = (calculate_position(xcoord, ycoord))
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.player_id = player_id
        self.number = number
        self.placement_time = pygame.time.get_ticks()
        self.strength = strength
        self.state = False
        self.controller = controller

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.placement_time >= BOMB_COUNTDOWN:
            self.explode()
        if (current_time - self.placement_time) % 400 < 200:
            self.image, _ = load_png("animations/bomb/bomb_3.png", BOMB_SCALE)
        else:
            self.image, _ = load_png("animations/bomb/bomb_2.png", BOMB_SCALE)

    def explode(self):
        if self.state:
            return
        self.state = True

        s_x = max(1, self.xcoord - self.strength)
        f_x = min(N, self.xcoord + self.strength + 1)
        s_y = max(1, self.ycoord - self.strength)
        f_y = min(N, self.ycoord + self.strength + 1)

        for i in range(self.xcoord, f_x):
            if i != self.xcoord and self.controller.is_wall(i, self.ycoord):
                break
            self.controller.handle_explosion(i, self.ycoord, self.player_id)

        for i in range(self.xcoord, s_x-1, -1):
            if i != self.xcoord and self.controller.is_wall(i, self.ycoord):
                break
            self.controller.handle_explosion(i, self.ycoord, self.player_id)

        for j in range(self.ycoord, f_y):
            if j != self.ycoord and self.controller.is_wall(self.xcoord, j):
                break
            self.controller.handle_explosion(self.xcoord, j, self.player_id)

        for j in range(self.ycoord, s_y-1, -1):
            if j != self.ycoord and self.controller.is_wall(self.xcoord, j):
                break
            self.controller.handle_explosion(self.xcoord, j, self.player_id)

        self.controller.delete_bomb(self.xcoord, self.ycoord)
        self.controller.new_explosion(self.xcoord, self.ycoord)
        self.controller.give_bomb(self.player_id)
        self.kill()

