import pygame

from Util import resolution as res, variables as var
from enum import Enum
from Map.full_board_generator import FullBoardGenerator
from Map.empty_board_generator import EmptyBoardGenerator
from Map.random_board_generator import RandomBoardGenerator
from Util.models import Position
from Util.loader import Loader
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml'])


class GameMap(Enum):
    FULL = 1
    EMPTY = 2
    RANDOM = 3

    def get_map_generator(self, loader, calculate_position):
        if self == GameMap.FULL:
            return FullBoardGenerator(loader, calculate_position)
        elif self == GameMap.EMPTY:
            return EmptyBoardGenerator(loader, calculate_position)
        elif self == GameMap.RANDOM:
            return RandomBoardGenerator(loader, calculate_position)


class GameObjects:
    def __init__(self, screen):
        self._screen = screen
        self._loader = Loader()
        self._map_generator = var.map_type.get_map_generator(self._loader, self.calculate_position)
        self._walls, self._floors, self._boxes, self._players = self._map_generator.get_map()
        self._bombs = {}
        self._explosions = {}
        self._modifiers = {}
        self._clock = pygame.time.Clock()

    @property
    def loader(self):
        return self._loader

    def add_bomb(self, bomb, position):
        self._bombs[position] = bomb

    def add_explosion(self, explosion, position):
        self._explosions[position] = explosion

    def add_modifier(self, modifier, position):
        self._modifiers[position] = modifier

    @staticmethod
    def calculate_position(coords):
        real_size = settings.image_size * settings.block_scale
        return Position(x=(coords.x + 1 / 2) * real_size + res.START_X, y=(coords.y + 1 / 2) * real_size + res.START_Y)

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
