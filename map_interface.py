import pygame

from abc import ABC, abstractmethod
from player import Player
from utilities import calculate_position
from global_variables import N, PLAYERS


class IMapGenerator(ABC):
    def __init__(self):
        self._n = N
        self._players_count = PLAYERS
        self._walls_dir = {}
        self._floors_dir = {}
        self._boxes_dir = {}
        self._player_keys = [(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE),
                             (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
                             (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_RSHIFT),
                             (pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6, pygame.K_KP0)]
        self._start_positions = [(1, 1), (self._n - 2, self._n - 2), (self._n - 2, 1), (1, self._n - 2)]
        self._players_dir = self.create_players()

    @abstractmethod
    def _generate_map(self):
        pass

    def create_players(self):
        players_dir = {}
        for i in range(self._players_count):
            player = Player(*calculate_position(*self._start_positions[i]), self._player_keys[i])
            players_dir[player.player_id] = player
        return players_dir

    @staticmethod
    def _should_be_wall(i, j, n):
        if i == 0 or i == n - 1 or j == 0 or j == n - 1:
            return True
        if i % 2 == 0 and j % 2 == 0:
            return True
        return False

    def get_map(self):
        self._generate_map()
        return self._walls_dir, self._floors_dir, self._boxes_dir, self._players_dir
