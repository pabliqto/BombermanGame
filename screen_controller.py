from utilities import calculate_position, calculate_player_position


class ScreenController:
    def __init__(self, screen, walls, floors, boxes, bombs, explosions, modifiers, players, game):
        self.screen = screen
        self.walls = walls
        self.floors = floors
        self.boxes = boxes
        self.bombs = bombs
        self.explosions = explosions
        self.modifiers = modifiers
        self.players = players
        self.game = game

    def get_screen(self):
        return self.screen

    def fill(self):
        self.screen.fill((47, 47, 46))

    def resize(self):
        for wall in self.walls.values():
            wall.rect.center = calculate_position(wall.xcoord, wall.ycoord)

        for floor in self.floors:
            floor.rect.center = calculate_position(floor.xcoord, floor.ycoord)

        for box in self.boxes.values():
            box.rect.center = calculate_position(box.xcoord, box.ycoord)

        for bomb in self.bombs.values():
            bomb.rect.center = calculate_position(bomb.xcoord, bomb.ycoord)

        for explosion in self.explosions.values():
            explosion.rect.center = calculate_position(explosion.xcoord, explosion.ycoord)

        for modifier in self.modifiers.values():
            modifier.rect.center = calculate_position(modifier.xcoord, modifier.ycoord)

        for player in self.players.values():
            player.rect.center = calculate_player_position(*player.rect.center)
