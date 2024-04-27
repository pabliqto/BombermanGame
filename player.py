import pygame

from global_variables import PLAYER_SPEED, COOLDOWN, PLAYER_SCALE, REAL_SIZE, BOMB_STRENGTH
from utilities import load_png
from modifiers import ModifierType
import resolution as res


class Player(pygame.sprite.Sprite):
    id_counter = 1

    def __init__(self, x, y, k):
        pygame.sprite.Sprite.__init__(self)
        self.speed = PLAYER_SPEED
        self.direction = "S"
        self.animation = 1
        self.cooldown = COOLDOWN
        self.player_id = Player.id_counter
        Player.id_counter += 1
        self.bomb = False
        self.bomb_count = 1
        self.current_bomb = 0
        self.bomb_strength = BOMB_STRENGTH
        self.keys = k
        self.color = ["yellow", "blue", "red", "green"][self.player_id - 1]
        self.image, self.rect = load_png(f"animations/{self.color}/{self.color}-idle-front.png", PLAYER_SCALE)
        self.rect.center = (x, y)
        self.score = 0
        self.extra_speed = 0
        self.extra_fire = 0

    def update(self):
        if self.extra_speed > 0:
            self.extra_speed -= 1

    def animation_move(self, direction):
        if direction == "WD" or direction == "SD":
            direction = "D"
        if direction == "WA" or direction == "SA":
            direction = "A"

        if self.cooldown == 0:
            pic = "animations/" + self.color + "/" + "walk-"
            curr_animation = self.animation

            if curr_animation == 4:
                curr_animation = 1
            else:
                curr_animation += 1

            if direction == "D":
                pic += 'right'
            elif direction == "A":
                pic += 'left'
            elif direction == "W":
                pic += 'back'
            elif direction == "S":
                pic += 'front'

            if direction != "WS" and direction != "AD":
                self.animation = curr_animation
                pic += str(curr_animation) + '-' + self.color + '.png'
                self.image, self.rect = load_png(pic, PLAYER_SCALE)
            self.cooldown = COOLDOWN
        else:
            self.cooldown -= 1

    def orientation(self, direction):
        scale = PLAYER_SCALE
        x, y = self.rect.topleft
        if direction != self.direction:
            name = "animations/" + self.color + "/" + self.color + '-idle-'

            if direction == "W":
                name += "back"
            elif direction == "A":
                name += "left"
            elif direction == "S":
                name += "front"
            elif direction == "D":
                name += "right"
            elif direction == "SA" or direction == "WA":
                name += "left"
            elif direction == "SD" or direction == "WD":
                name += "right"
            name += '.png'
            self.image, self.rect = load_png(name, scale)
            self.direction = direction
        else:
            self.animation_move(direction)
        self.rect.topleft = (x, y)

    def move(self, rect):
        self.rect = rect

    def current_bomb_add(self):
        self.current_bomb += 1

    def change_bomb_status(self):
        self.bomb = not self.bomb

    def change_extra_fire(self, value):
        self.extra_fire += value

    def give_bomb(self):
        self.bomb_count += 1

    def get_coords(self):
        x, y = self.rect.center
        i = (x - res.START_X) // REAL_SIZE
        j = (y - res.START_Y) // REAL_SIZE
        return i, j

    def collect_modifier(self, modifier):
        if modifier.type == ModifierType.SPEED:
            self.extra_speed += modifier.value
        elif modifier.type == ModifierType.BOMB:
            self.bomb_count += modifier.value
        elif modifier.type == ModifierType.FIRE:
            self.extra_fire += modifier.value
        modifier.kill()
