import pygame

from global_variables import PLAYERS


class map_drawer:
    def __init__(self, walls, floors, boxes, players, modifiers, bombs, explosions, game):
        self.wall_sprites = pygame.sprite.RenderPlain(list(walls.values()))
        self.floor_sprites = pygame.sprite.RenderPlain(floors)
        self.box_sprites = pygame.sprite.RenderPlain(list(boxes.values()))
        self.bomb_sprites = pygame.sprite.RenderPlain(list(bombs.values()))
        self.explosion_sprites = pygame.sprite.RenderPlain(list(explosions.values()))
        self.modifier_sprites = pygame.sprite.RenderPlain(list(modifiers.values()))
        self.player_sprites = pygame.sprite.RenderPlain(list(players.values()))
        self.scoreboard = {i: 0 for i in range(1, PLAYERS + 1)}
        self.game = game

    def add_bomb(self, bomb):
        self.bomb_sprites.add(bomb)

    def add_modifier(self, modifier):
        self.modifier_sprites.add(modifier)

    def add_explosion(self, explosion):
        self.explosion_sprites.add(explosion)

    def draw(self, screen):
        self.wall_sprites.draw(screen)
        self.floor_sprites.draw(screen)
        self.box_sprites.draw(screen)
        self.bomb_sprites.draw(screen)
        self.modifier_sprites.draw(screen)
        self.player_sprites.draw(screen)
        self.explosion_sprites.draw(screen)

    def update(self):
        self.bomb_sprites.update()
        self.explosion_sprites.update()
        self.modifier_sprites.update()
        self.player_sprites.update()
