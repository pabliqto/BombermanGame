import pygame

from global_variables import PLAYER_SPEED, COOLDOWN, PLAYER_SCALE, REAL_SIZE, START_X, START_Y
from loadpng import load_png


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
        self.bomb_strength = 2
        self.keys = k
        if self.player_id == 2:
            self.color = "blue"
        elif self.player_id == 3:
            self.color = "red"
        elif self.player_id == 4:
            self.color = "green"
        else:
            self.color = ""
        if self.color:
            self.image, self.rect = load_png("animations/" + self.color + "/" + self.color + "-idle-front" + ".png", PLAYER_SCALE)
        else:
            self.image, self.rect = load_png("animations/yellow/" + self.color + "idle-front.png", PLAYER_SCALE)
        self.rect.center = (x, y)
        self.score = 0
        self.extra_speed = 0
        self.extra_fire = 0

    def update(self):
        pass

    def animation_move(self, direction):
        scale = PLAYER_SCALE
        if direction == "WD" or direction == "SD":
            direction = "D"
        if direction == "WA" or direction == "SA":
            direction = "A"

        if self.cooldown == 0:
            if self.color:
                pic = "animations/" + self.color + "/" + "walk-"
            else:
                pic = "animations/yellow/walk-"
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
                if self.color:
                    pic += str(curr_animation) + '-' + self.color + '.png'
                else:
                    pic += str(curr_animation) + '.png'
                self.image, self.rect = load_png(pic, scale)
            self.cooldown = COOLDOWN
        else:
            self.cooldown -= 1

    def orientation(self, direction):
        scale = PLAYER_SCALE
        x, y = self.rect.topleft
        if direction != self.direction:
            if self.color:
                name = "animations/" + self.color + "/" + self.color + '-idle-'
            else:
                name = "animations/yellow/idle-"

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

    def change_extra_speed(self, value):
        self.extra_speed += value

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
        i = (x - START_X) // REAL_SIZE
        j = (y - START_Y) // REAL_SIZE
        return i, j

    def collect_modifier(self, modifier):
        if modifier.type == "speed":
            self.extra_speed = modifier.value
        elif modifier.type == "bomb":
            self.bomb_count += modifier.value
        elif modifier.type == "fire":
            self.extra_fire += modifier.value
        modifier.kill()
