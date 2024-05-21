import random

from Objects.box import Box
from Map.box_board_generator import BoxBoardGenerator
from Util import variables as var


class RandomBoardGenerator(BoxBoardGenerator):
    def __init__(self, loader, calculate_position):
        super().__init__(loader, calculate_position)
        self._box_chance = var.box_chance

    def _generate_box(self, coords):
        if (2 < coords.x < self._n - 3 or 2 < coords.y < self._n - 3) and random.random() <= self._box_chance:
            self._boxes_dir[coords] = Box(self.calculate_position(coords), coords, self.loader)
