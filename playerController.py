from bomb import Bomb


class playerController:
    def __init__(self, players, walls, floors, boxes, bombs, explosions, modifiers, game):
        self.players = players
        self.walls = walls
        self.floors = floors
        self.boxes = boxes
        self.bombs = bombs
        self.explosions = explosions
        self.modifiers = modifiers
        self.game = game

    def update(self):
        for player in self.players.values():
            player.update()

    def get_players(self):
        return list(self.players.values())

    def get_player(self, player_id):
        return self.players.get(player_id)

    def players_ids(self):
        return list(self.players.keys())

    def get_winner(self):
        return list(self.players.keys())[0]

    def give_bomb(self, player_id):
        if player_id in self.players:
            self.players[player_id].give_bomb()

    # check if player can move in the given direction
    def move_player(self, player_id, direction):
        player = self.players[player_id]
        if len(direction) == 4 or direction == 'AD' or direction == 'WS':
            return

        if len(direction) == 3:
            if "W" in direction and "S" in direction:
                direction = direction.replace("W", "")
                direction = direction.replace("S", "")
            elif "A" in direction and "D" in direction:
                direction = direction.replace("A", "")
                direction = direction.replace("D", "")

        new_pos = player.rect.copy()
        player.orientation(direction)

        extra = 0
        if player.extra_speed > 0:
            extra = 2

        if "A" in direction:
            new_pos.x -= player.speed + extra

        if "D" in direction:
            new_pos.x += player.speed + extra

        self.check_position(player, new_pos)

        new_pos = player.rect.copy()

        if "W" in direction:
            new_pos.y -= player.speed + extra

        if "S" in direction:
            new_pos.y += player.speed + extra

        self.check_position(player, new_pos)

    def is_box(self, x, y):
        return self.boxes.get((x, y)) is not None

    def no_bombs(self, x, y):
        return self.bombs.get((x, y)) is None

    def place_bomb(self, player_id):
        player = self.players[player_id]
        if not player.bomb and player.bomb_count > 0:
            i, j = player.get_coords()
            if not self.is_box(i, j) and self.no_bombs(i, j):
                strength = player.bomb_strength
                if player.extra_fire > 0:
                    player.change_extra_fire(-1)
                    strength += 2
                new_bomb = Bomb(i, j, self.game.get_bomb_controller(), strength, player_id, player.current_bomb)
                self.bombs[(i, j)] = new_bomb
                self.game.get_map_drawer().add_bomb(new_bomb)
                player.change_bomb_status()
                player.bomb_count -= 1

    # handle player movement around a newly placed bomb and wall and box collision
    def check_position(self, player, new_pos):
        if new_pos.collidelist(list(self.walls.values())) == -1 and new_pos.collidelist(
                list(self.boxes.values())) == -1:
            blist = list(self.bombs.values())
            bindex = new_pos.collidelist(blist)
            if not player.bomb and bindex == -1:
                player.move(new_pos)
            elif player.bomb and bindex != -1:
                if blist[bindex].player_id == player.player_id and blist[bindex].number == player.current_bomb:
                    player.move(new_pos)
            elif player.bomb and bindex == -1:
                player.move(new_pos)
                player.change_bomb_status()
                player.current_bomb_add()
