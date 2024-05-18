import random

from explosion import Explosion
from global_variables import MODIFIER_CHANCE, EXTRA_BOMB_CHANCE
from bomb import Bomb
from modifiers import Modifier
from utilities import calculate_position
from models import Position


class BombController:
    def __init__(self, objects, map_drawer, scoreboard):
        self.objects = objects
        self.map_drawer = map_drawer
        self.scoreboard = scoreboard

    def delete_bomb(self, coords):
        del self.objects.bombs[coords]

    def is_wall(self, position):
        return self.objects.walls.get(position) is not None

    def give_bomb(self, player_id):
        if self.objects.players.get(player_id):
            self.objects.players.get(player_id).give_bomb()

    def new_explosion(self, coords):
        new_explosion = Explosion(calculate_position(coords), coords)
        self.objects.explosions[coords] = new_explosion
        self.map_drawer.add_explosion(new_explosion)

    def handle_explosion(self, coords, player_id):
        self.resolve_bomb_explosion(coords)
        self.resolve_box_explosion(coords, player_id)
        self.manage_player_deaths(coords, player_id)
        self.new_explosion(coords)

    def resolve_box_explosion(self, coords, player_id):
        if self.objects.boxes.get(coords):
            self.objects.boxes.get(coords).kill()
            if player_id in self.objects.players:
                self.scoreboard.box_destroyed(player_id)
            del self.objects.boxes[coords]

            random_number = random.random()

            # modifiers and extra bombs
            if EXTRA_BOMB_CHANCE <= random_number <= MODIFIER_CHANCE:
                new_modifier = Modifier(calculate_position(coords), coords)
                self.objects.modifiers[coords] = new_modifier
                self.map_drawer.add_modifier(new_modifier)
            elif random_number < EXTRA_BOMB_CHANCE:
                new_bomb = Bomb(calculate_position(coords), coords, self)
                self.objects.bombs[coords] = new_bomb
                self.map_drawer.bomb_sprites.add(new_bomb)

    def resolve_bomb_explosion(self, coords):
        if self.objects.bombs.get(coords):
            self.objects.bombs[coords].explode()

    def manage_player_deaths(self, coords, player_id):
        for p_id in list(self.objects.players.keys()):
            if self.objects.players[p_id].get_coords() == coords:
                if player_id not in (p_id, 5):
                    self.scoreboard.kill_player(player_id)
                self.objects.players[p_id].kill()
                del self.objects.players[p_id]
