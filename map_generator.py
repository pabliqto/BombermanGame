import random
import pygame

from floor import Floor
from box import Box
from wall import Wall
from player import Player
from utilities import calculate_position


def initialize_board(n, chance, players_count):
    walls_dir = {}
    floors_arr = []
    boxes_dir = {}
    players_dir = {}

    for i in range(n):
        for j in range(n):
            position = calculate_position(i, j)
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                walls_dir[(i, j)] = Wall(*position, i, j)
            elif i % 2 == 0 and j % 2 == 0:
                walls_dir[(i, j)] = Wall(*position, i, j)
            else:
                floors_arr.append(Floor(*position, i, j))
                if (2 < i < n - 3 or 2 < j < n - 3) and random.random() <= chance:
                    boxes_dir[(i, j)] = Box(*position, i, j)

    player_keys = [(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE),
                   (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
                   (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_RSHIFT),
                   (pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6, pygame.K_KP0)]

    start_positions = [(1, 1), (n - 2, n - 2), (n - 2, 1), (1, n - 2)]

    for i in range(players_count):
        player = Player(*calculate_position(*start_positions[i]), player_keys[i])
        players_dir[player.player_id] = player

    return walls_dir, floors_arr, boxes_dir, players_dir
