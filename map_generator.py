import random
import pygame

from global_variables import START_X, REAL_SIZE, START_Y
from floor import Floor
from box import Box
from wall import Wall
from player import Player

def initialize_board(n, chance, players_count):
    walls_dir = {}
    floors_arr = []
    boxes_dir = {}
    players_dir = {}

    for i in range(n):
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                walls_dir[(i, j)] = Wall(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)
            elif i % 2 == 0 and j % 2 == 0:
                walls_dir[(i, j)] = Wall(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)
            else:
                floors_arr.append(Floor(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j))
                if (2 < i < n - 3 or 2 < j < n - 3) and random.random() <= chance:
                    boxes_dir[(i, j)] = Box(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)

    player1 = Player(START_X + (3 * REAL_SIZE) / 2, START_Y + (3 * REAL_SIZE) / 2,
                     [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE])

    players_dir[player1.player_id] = player1

    if players_count > 1:
        player2 = Player(START_X + (n - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         START_Y + (n - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL])
        players_dir[player2.player_id] = player2

    if players_count > 2:
        player3 = Player(START_X + (n - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         START_Y + (3 * REAL_SIZE) / 2,
                         [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_RSHIFT])
        players_dir[player3.player_id] = player3

    if players_count > 3:
        player4 = Player(START_X + (3 * REAL_SIZE) / 2,
                         START_Y + (n - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         [pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6, pygame.K_KP0])
        players_dir[player4.player_id] = player4


    return walls_dir, floors_arr, boxes_dir, players_dir
