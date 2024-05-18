import random

from utilities import calculate_position
from box import Box
from global_variables import BOX_CHANCE
from box_board_generator import BoxBoardGenerator


class RandomBoardGenerator(BoxBoardGenerator):
    def __init__(self):
        super().__init__()
        self._box_chance = BOX_CHANCE

    def _generate_box(self, coords):
        if (2 < coords.x < self._n - 3 or 2 < coords.y < self._n - 3) and random.random() <= self._box_chance:
            self._boxes_dir[coords] = Box(calculate_position(coords), coords)
