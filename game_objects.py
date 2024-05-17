import pygame

from global_variables import N, BOX_CHANCE, PLAYERS
from map_generator import initialize_board


class GameObjects:
    def __init__(self, screen):
        self._screen = screen
        self._walls, self._floors, self._boxes, self._players = initialize_board(N, BOX_CHANCE, PLAYERS)
        self._bombs = {}
        self._explosions = {}
        self._modifiers = {}
        self._clock = pygame.time.Clock()

    def add_bomb(self, bomb, x, y):
        self._bombs[(x, y)] = bomb

    def add_explosion(self, explosion, x, y):
        self._explosions[(x, y)] = explosion

    def add_modifier(self, modifier, x, y):
        self._modifiers[(x, y)] = modifier

    @property
    def screen(self):
        return self._screen

    @property
    def walls(self):
        return self._walls

    @property
    def floors(self):
        return self._floors

    @property
    def boxes(self):
        return self._boxes

    @property
    def players(self):
        return self._players

    @property
    def bombs(self):
        return self._bombs

    @property
    def explosions(self):
        return self._explosions

    @property
    def modifiers(self):
        return self._modifiers

    @property
    def clock(self):
        return self._clock

    def walls_objects(self):
        return list(self._walls.values())

    def boxes_objects(self):
        return list(self._boxes.values())

    def bomb_objects(self):
        return list(self._bombs.values())
