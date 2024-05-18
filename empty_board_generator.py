from map_interface import IMapGenerator
from utilities import calculate_position
from wall import Wall
from floor import Floor
from models import Position


class EmptyBoardGenerator(IMapGenerator):
    def __init__(self):
        super().__init__()

    def _generate_map(self):
        for i in range(self._n):
            for j in range(self._n):
                coords = Position(x=i, y=j)
                position = calculate_position(coords)
                if self._should_be_wall(coords):
                    self._walls_dir[coords] = Wall(position, coords)
                else:
                    self._floors_dir[coords] = Floor(position, coords)
