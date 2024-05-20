import random

from explosion import Explosion
from bomb import Bomb
from modifiers import Modifier
import variables as var
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml'])


class BombController:
    def __init__(self, objects, map_drawer, scoreboard):
        self.objects = objects
        self.map_drawer = map_drawer
        self.scoreboard = scoreboard

    def delete_bomb(self, coords):
        del self.objects.bombs[coords]

    def give_bomb(self, player_id):
        if self.objects.players.get(player_id):
            self.objects.players.get(player_id).give_bomb()

    def new_explosion(self, coords):
        new_explosion = Explosion(self.objects.calculate_position(coords), coords, self.objects.loader)
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
            if var.modifiers and 1 - settings.modifier_chance <= random_number:
                new_modifier = Modifier(self.objects.calculate_position(coords), coords, self.objects.loader)
                self.objects.modifiers[coords] = new_modifier
                self.map_drawer.add_modifier(new_modifier)

            if var.extra_bomb and random_number <= var.extra_bomb_chance:
                new_bomb = Bomb(self.objects.calculate_position(coords), coords, self, self.objects.loader)
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
