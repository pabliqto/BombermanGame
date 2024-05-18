from utilities import calculate_position
from box import Box
from box_board_generator import BoxBoardGenerator


class FullBoardGenerator(BoxBoardGenerator):
    def __init__(self):
        super().__init__()

    def _generate_box(self, coords):
        if 2 < coords.x < self._n - 3 or 2 < coords.y < self._n - 3:
            self._boxes_dir[coords] = Box(calculate_position(coords), coords)
