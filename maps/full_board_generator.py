from objects.box import Box
from maps.box_board_generator import BoxBoardGenerator


class FullBoardGenerator(BoxBoardGenerator):
    def __init__(self, loader, calculate_position):
        super().__init__(loader, calculate_position)

    def _generate_box(self, coords):
        if 2 < coords.x < self._n - 3 or 2 < coords.y < self._n - 3:
            self._boxes_dir[coords] = Box(self.calculate_position(coords), coords, self.loader)
