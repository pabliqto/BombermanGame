import pygame

from abc import ABC, abstractmethod
from objects.player import Player
from utilities.models import Position
from dynaconf import Dynaconf
from utilities import variables as var

settings = Dynaconf(settings_files=['settings.toml'])


class IMapGenerator(ABC):
    def __init__(self, loader, calculate_position):
        self._loader = loader
        self.calculate_position = calculate_position
        self._n = settings.n
        self._players_count = var.player_number
        self._walls_dir = {}
        self._floors_dir = {}
        self._boxes_dir = {}
        self._player_keys = [(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE),
                             (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
                             (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_RSHIFT),
                             (pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6, pygame.K_KP0)]
        self._start_coords = [Position(x=1, y=1),
                              Position(x=self._n - 2, y=self._n - 2),
                              Position(x=self._n - 2, y=1),
                              Position(x=1, y=self._n - 2)]
        self._players_dir = self.create_players()

    @property
    def loader(self):
        return self._loader

    @abstractmethod
    def _generate_map(self):
        pass

    def create_players(self):
        players_dir = {}
        for i in range(self._players_count):
            player = Player(i+1, self.calculate_position(self._start_coords[i]), self._player_keys[i], self._loader)
            players_dir[player.player_id] = player
        return players_dir

    def _should_be_wall(self, coords):
        if coords.x == 0 or coords.x == self._n - 1 or coords.y == 0 or coords.y == self._n - 1:
            return True
        if coords.x % 2 == 0 and coords.y % 2 == 0:
            return True
        return False

    def get_map(self):
        self._generate_map()
        return self._walls_dir, self._floors_dir, self._boxes_dir, self._players_dir
