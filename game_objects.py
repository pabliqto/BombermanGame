import pygame

from enum import Enum
from full_board_generator import FullBoardGenerator
from empty_board_generator import EmptyBoardGenerator
from random_board_generator import RandomBoardGenerator


class GameMap(Enum):
    FULL = 1
    EMPTY = 2
    RANDOM = 3

    def get_map_generator(self):
        if self == GameMap.FULL:
            return FullBoardGenerator()
        elif self == GameMap.EMPTY:
            return EmptyBoardGenerator()
        elif self == GameMap.RANDOM:
            return RandomBoardGenerator()


class GameObjects:
    def __init__(self, screen, map_type: GameMap):
        self._screen = screen
        self._map_generator = map_type.get_map_generator()
        self._walls, self._floors, self._boxes, self._players = self._map_generator.get_map()
        self._bombs = {}
        self._explosions = {}
        self._modifiers = {}
        self._clock = pygame.time.Clock()

    def add_bomb(self, bomb, position):
        self._bombs[position] = bomb

    def add_explosion(self, explosion, position):
        self._explosions[position] = explosion

    def add_modifier(self, modifier, position):
        self._modifiers[position] = modifier

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
