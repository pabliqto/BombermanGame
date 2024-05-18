from map_interface import IMapGenerator
from wall import Wall
from floor import Floor
from models import Position


class EmptyBoardGenerator(IMapGenerator):
    def __init__(self, loader, calculate_position):
        super().__init__(loader, calculate_position)

    def _generate_map(self):
        for i in range(self._n):
            for j in range(self._n):
                coords = Position(x=i, y=j)
                position = self.calculate_position(coords)
                if self._should_be_wall(coords):
                    self._walls_dir[coords] = Wall(position, coords, self.loader)
                else:
                    self._floors_dir[coords] = Floor(position, coords, self.loader)
