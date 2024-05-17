import random

from utilities import calculate_position
from box import Box
from global_variables import BOX_CHANCE
from box_board_generator import BoxBoardGenerator


class RandomBoardGenerator(BoxBoardGenerator):
    def __init__(self):
        super().__init__()
        self._box_chance = BOX_CHANCE

    def _generate_box(self, i, j):
        if (2 < i < self._n - 3 or 2 < j < self._n - 3) and random.random() <= self._box_chance:
            self._boxes_dir[(i, j)] = Box(*calculate_position(i, j), i, j)
