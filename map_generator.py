import random
import pygame

from floor import Floor
from box import Box
from wall import Wall
from player import Player
from utilities import calculate_position


def initialize_board(n, box_chance, players_count):
    walls_dir = {}
    floors_dir = {}
    boxes_dir = {}
    players_dir = {}

    # Create walls, floors, boxes
    for i in range(n):
        for j in range(n):
            position = calculate_position(i, j)
            if should_be_wall(i, j, n):
                walls_dir[(i, j)] = Wall(*position, i, j)
            else:
                floors_dir[(i, j)] = Floor(*position, i, j)
                generate_box(i, j, n, box_chance, boxes_dir)

    # Player keys
    player_keys = [(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE),
                   (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
                   (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_RSHIFT),
                   (pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6, pygame.K_KP0)]

    # Player start positions
    start_positions = [(1, 1), (n - 2, n - 2), (n - 2, 1), (1, n - 2)]

    # Create players
    for i in range(players_count):
        player = Player(*calculate_position(*start_positions[i]), player_keys[i])
        players_dir[player.player_id] = player

    return walls_dir, floors_dir, boxes_dir, players_dir


def should_be_wall(i, j, n):
    if i == 0 or i == n - 1 or j == 0 or j == n - 1:
        return True
    if i % 2 == 0 and j % 2 == 0:
        return True
    return False


def generate_box(i, j, n, box_chance, boxes_dir):
    if (2 < i < n - 3 or 2 < j < n - 3) and random.random() <= box_chance:
        boxes_dir[(i, j)] = Box(*calculate_position(i, j), i, j)