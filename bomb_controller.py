import random

from explosion import Explosion
from global_variables import MODIFIER_CHANCE, EXTRA_BOMB_CHANCE
from bomb import Bomb
from modifiers import Modifier
from utilities import calculate_position


class BombController:
    def __init__(self, objects, map_drawer):
        self.objects = objects
        self.map_drawer = map_drawer

    def update(self):
        for bomb in list(self.objects.bombs.values()):
            bomb.update()
            if bomb.exploded:
                del self.objects.bombs[(bomb.x, bomb.y)]

    def delete_bomb(self, x, y):
        del self.objects.bombs[(x, y)]

    def is_wall(self, x, y):
        return self.objects.walls.get((x, y)) is not None

    def give_bomb(self, player_id):
        if self.objects.players.get(player_id):
            self.objects.players.get(player_id).give_bomb()

    def new_explosion(self, x, y):
        new_explosion = Explosion(*calculate_position(x, y), x, y)
        self.objects.explosions[(x, y)] = new_explosion
        self.map_drawer.add_explosion(new_explosion)

    def handle_explosion(self, x, y, player_id):
        self.resolve_box_explosion(x, y, player_id)
        self.resolve_bomb_explosion(x, y)
        self.manage_player_deaths(x, y, player_id)
        self.new_explosion(x, y)

    def resolve_box_explosion(self, x, y, player_id):
        if self.objects.boxes.get((x, y)):
            self.objects.boxes.get((x, y)).kill()
            if player_id in self.objects.players:
                self.map_drawer.scoreboard[player_id] += 10

            del self.objects.boxes[(x, y)]

            random_number = random.random()

            # modifiers and extra bombs
            if EXTRA_BOMB_CHANCE <= random_number <= MODIFIER_CHANCE:
                new_modifier = Modifier(*calculate_position(x, y), x, y)
                self.objects.modifiers[(x, y)] = new_modifier
                self.map_drawer.add_modifier(new_modifier)
            elif random_number < EXTRA_BOMB_CHANCE:
                new_bomb = Bomb(x, y, self)
                self.objects.bombs[(x, y)] = new_bomb
                self.map_drawer.bomb_sprites.add(new_bomb)

    def resolve_bomb_explosion(self, x, y):
        if self.objects.bombs.get((x, y)):
            self.objects.bombs[(x, y)].explode()

    def manage_player_deaths(self, x, y, player_id):
        for i in list(self.objects.players.keys()):
            if self.objects.players[i] is not None:
                if self.objects.players[i].get_coords() == (x, y):
                    if i != player_id and player_id in self.objects.players:
                        self.map_drawer.scoreboard[player_id] += 50
                    self.objects.players[i].kill()
                    del self.objects.players[i]
