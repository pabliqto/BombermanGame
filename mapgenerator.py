import random

from global_variables import N, START_X, REAL_SIZE, START_Y
from floor import Floor
from box import Box
from wall import Wall


def initialize_board(chance=0.7):
    walls_dir = {}
    floors_arr = []
    boxes_dir = {}

    for i in range(N):
        for j in range(N):
            if i == 0 or i == N - 1 or j == 0 or j == N - 1:
                walls_dir[(i, j)] = Wall(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)
            elif i % 2 == 0 and j % 2 == 0:
                walls_dir[(i, j)] = Wall(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)
            else:
                floors_arr.append(Floor(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j))
                if (2 < i < N - 3 or 2 < j < N - 3) and random.random() <= chance:
                    boxes_dir[(i, j)] = Box(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)

    return walls_dir, floors_arr, boxes_dir
