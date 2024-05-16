from utilities import calculate_position, calculate_player_position


class screen_controller:
    def __init__(self, objects):
        self.objects = objects

    def fill(self):
        self.objects.screen.fill((47, 47, 46))

    def resize(self):
        entities = {**self.objects.walls, **self.objects.boxes,
                    **self.objects.bombs, **self.objects.explosions, **self.objects.modifiers}

        for entity in entities.values():
            entity.rect.center = calculate_position(entity.xcoord, entity.ycoord)
        for player in self.objects.players.values():
            player.rect.center = calculate_player_position(*player.rect.center)
        for floor in self.objects.floors:
            floor.rect.center = calculate_position(floor.xcoord, floor.ycoord)
