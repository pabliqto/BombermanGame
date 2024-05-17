from utilities import calculate_position
from box import Box
from box_board_generator import BoxBoardGenerator


class FullBoardGenerator(BoxBoardGenerator):
    def __init__(self):
        super().__init__()

    def _generate_box(self, i, j):
        if 2 < i < self._n - 3 or 2 < j < self._n - 3:
            self._boxes_dir[(i, j)] = Box(*calculate_position(i, j), i, j)
