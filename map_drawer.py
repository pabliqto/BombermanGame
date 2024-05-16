import pygame

from global_variables import PLAYERS


class MapDrawer:
    def __init__(self, objects):
        self.wall_sprites = pygame.sprite.RenderPlain(list(objects.walls.values()))
        self.floor_sprites = pygame.sprite.RenderPlain(list(objects.floors.values()))
        self.box_sprites = pygame.sprite.RenderPlain(list(objects.boxes.values()))
        self.bomb_sprites = pygame.sprite.RenderPlain(list(objects.bombs.values()))
        self.explosion_sprites = pygame.sprite.RenderPlain(list(objects.explosions.values()))
        self.modifier_sprites = pygame.sprite.RenderPlain(list(objects.modifiers.values()))
        self.player_sprites = pygame.sprite.RenderPlain(list(objects.players.values()))
        self.scoreboard = {i: 0 for i in range(1, PLAYERS + 1)}

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
