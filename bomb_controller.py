import random

from explosion import Explosion
from global_variables import MODIFIER_CHANCE, EXTRA_BOMB_CHANCE
from bomb import Bomb
from modifiers import Modifier
from utilities import calculate_position


class BombController:
    def __init__(self, bombs, explosions, players, modifier, boxes, walls, game):
        self.bombs = bombs
        self.explosions = explosions
        self.players = players
        self.modifiers = modifier
        self.boxes = boxes
        self.walls = walls
        self.game = game

    def update(self):
        for bomb in list(self.bombs.values()):
            bomb.update()
            if bomb.exploded:
                del self.bombs[(bomb.x, bomb.y)]

    def delete_bomb(self, x, y):
        del self.bombs[(x, y)]

    def is_wall(self, x, y):
        return self.walls.get((x, y)) is not None

    def give_bomb(self, player_id):
        if self.game.get_player_controller().get_player(player_id):
            self.game.get_player_controller().get_player(player_id).give_bomb()

    def new_explosion(self, x, y):
        new_explosion = Explosion(*calculate_position(x, y), x, y)
        self.explosions[(x, y)] = new_explosion
        self.game.get_map_drawer().explosion_sprites.add(new_explosion)

    def handle_explosion(self, x, y, player_id):
        if self.game.get_player_controller().boxes.get((x, y)):
            self.boxes.get((x, y)).kill()
            if player_id in self.players:
                self.game.get_map_drawer().scoreboard[player_id] += 10

            del self.boxes[(x, y)]

            random_number = random.random()

            # modifiers and extra bombs
            if EXTRA_BOMB_CHANCE <= random_number <= MODIFIER_CHANCE:
                new_modifier = Modifier(*calculate_position(x, y), x, y)
                self.modifiers[(x, y)] = new_modifier
                self.game.get_map_drawer().modifier_sprites.add(new_modifier)
            elif random_number < EXTRA_BOMB_CHANCE:
                new_bomb = Bomb(x, y, self)
                self.bombs[(x, y)] = new_bomb
                self.game.get_map_drawer().bomb_sprites.add(new_bomb)

        elif self.game.get_player_controller().bombs.get((x, y)):
            self.bombs[(x, y)].explode()

        for i in list(self.players.keys()):
            if self.players[i] is not None:
                if self.players[i].get_coords() == (x, y):
                    if i != player_id and player_id in self.players:
                        self.game.get_map_drawer().scoreboard[player_id] += 50
                    self.players[i].kill()
                    del self.players[i]

        self.new_explosion(x, y)
