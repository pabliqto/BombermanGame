import pygame

from modifiers import ModifierType
import resolution as res
from models import Position
from dynaconf import Dynaconf
import variables as var

settings = Dynaconf(settings_files=['settings.toml'])


class Player(pygame.sprite.Sprite):

    def __init__(self, p_id, position, k, loader):
        pygame.sprite.Sprite.__init__(self)
        self.name = var.player_names[p_id-1]
        self.speed = settings.player_speed
        self.direction = "S"
        self.animation = 1
        self.cooldown = settings.cooldown
        self.player_id = p_id
        self.bomb = None
        self.bomb_count = settings.start_bomb
        self.bomb_strength = settings.bomb_strength
        self.keys = k
        self.loader = loader
        self.color = var.players_colors[var.players_colors_values[self.player_id - 1]]
        self.image, self.rect = loader.load_png(f"animations/{self.color}/{self.color}-idle-front.png",
                                                settings.player_scale)
        self.rect.center = position.x, position.y
        self.score = 0
        self.extra_speed = 0
        self.extra_fire = 0
        self.coords = self.get_coords()

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
                self.image, self.rect = self.loader.load_png(pic, settings.player_scale)
            self.cooldown = settings.cooldown
        else:
            self.cooldown -= 1

    def orientation(self, direction):
        scale = settings.player_scale
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
            self.image, self.rect = self.loader.load_png(name, scale)
            self.direction = direction
        else:
            self.animation_move(direction)
        self.rect.topleft = (x, y)

    def move(self, rect):
        self.rect = rect
        self.coords = self.get_coords()

    def change_bomb_status(self, bomb=None):
        self.bomb = bomb

    def change_extra_fire(self, value):
        self.extra_fire += value

    def give_bomb(self):
        self.bomb_count += 1

    def get_coords(self):
        x, y = self.rect.center
        real_size = settings.block_scale * settings.image_size
        i = (x - res.START_X) // real_size
        j = (y - res.START_Y) // real_size
        return Position(x=i, y=j)

    def can_place_bomb(self):
        return not self.bomb and self.bomb_count > 0

    def collect_modifier(self, modifier):
        if modifier.type == ModifierType.SPEED:
            self.extra_speed += modifier.value
        elif modifier.type == ModifierType.BOMB:
            self.bomb_count += modifier.value
        elif modifier.type == ModifierType.FIRE:
            self.extra_fire += modifier.value
        modifier.kill()
