from utilities import calculate_position, calculate_player_position


class screen_controller:
    def __init__(self, objects):
        self.objects = objects

    def fill(self):
        self.objects.screen.fill((47, 47, 46))

    def resize(self):
        for wall in self.objects.walls.values():
            wall.rect.center = calculate_position(wall.xcoord, wall.ycoord)

        for floor in self.objects.floors:
            floor.rect.center = calculate_position(floor.xcoord, floor.ycoord)

        for box in self.objects.boxes.values():
            box.rect.center = calculate_position(box.xcoord, box.ycoord)

        for bomb in self.objects.bombs.values():
            bomb.rect.center = calculate_position(bomb.xcoord, bomb.ycoord)

        for explosion in self.objects.explosions.values():
            explosion.rect.center = calculate_position(explosion.xcoord, explosion.ycoord)

        for modifier in self.objects.modifiers.values():
            modifier.rect.center = calculate_position(modifier.xcoord, modifier.ycoord)

        for player in self.objects.players.values():
            player.rect.center = calculate_player_position(*player.rect.center)
