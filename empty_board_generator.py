from map_interface import IMapGenerator
from utilities import calculate_position
from wall import Wall
from floor import Floor


class EmptyBoardGenerator(IMapGenerator):
    def __init__(self):
        super().__init__()

    def _generate_map(self):
        for i in range(self._n):
            for j in range(self._n):
                position = calculate_position(i, j)
                if self._should_be_wall(i, j, self._n):
                    self._walls_dir[(i, j)] = Wall(*position, i, j)
                else:
                    self._floors_dir[(i, j)] = Floor(*position, i, j)
