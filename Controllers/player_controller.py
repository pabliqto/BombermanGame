from Objects.bomb import Bomb


class PlayerController:
    def __init__(self, objects, bomb_controller, map_drawer, scoreboard):
        self.objects = objects
        self.bomb_controller = bomb_controller
        self.map_drawer = map_drawer
        self.scoreboard = scoreboard

    def get_winner(self):
        count = len(self.objects.players.values())
        if count == 1:
            return list(self.objects.players.keys())[0]
        elif count == 0:
            return self.scoreboard.get_top_scorer()

    @staticmethod
    def simplify_direction(direction):
        if len(direction) == 4 or direction == 'AD' or direction == 'WS':
            return

        if len(direction) == 3:
            if "W" in direction and "S" in direction:
                direction = direction.replace("W", "")
                direction = direction.replace("S", "")
            elif "A" in direction and "D" in direction:
                direction = direction.replace("A", "")
                direction = direction.replace("D", "")
        return direction

    def update_position(self, player, direction, extra_speed):
        new_pos = player.rect.copy()
        if "A" in direction:
            new_pos.x -= player.speed + extra_speed

        if "D" in direction:
            new_pos.x += player.speed + extra_speed

        self.check_position(player, new_pos)

        new_pos = player.rect.copy()
        if "W" in direction:
            new_pos.y -= player.speed + extra_speed

        if "S" in direction:
            new_pos.y += player.speed + extra_speed
        return new_pos

    # check if player can move in the given direction
    def move_player(self, player_id, direction):
        player = self.objects.players[player_id]
        if player is None:
            return

        direction = self.simplify_direction(direction)
        if not direction:
            return

        player.orientation(direction)
        extra_speed = 2 if player.extra_speed > 0 else 0
        new_pos = self.update_position(player, direction, extra_speed)

        self.check_position(player, new_pos)

    def place_bomb(self, player_id):
        player = self.objects.players.get(player_id)
        if player.can_place_bomb():
            coords = player.get_coords()
            if self.is_position_valid_for_bomb(coords):
                self.deploy_bomb(player, coords)

    def is_position_valid_for_bomb(self, coords):
        return not self.objects.boxes.get(coords) and not self.objects.bombs.get(coords)

    def deploy_bomb(self, player, coords):
        player_id = player.player_id
        strength = player.bomb_strength
        if player.extra_fire > 0:
            player.change_extra_fire(-1)
            strength += 2
        position = self.objects.calculate_position(coords)
        new_bomb = Bomb(position, coords, self.bomb_controller, self.objects.loader, strength, player_id)
        self.objects.bombs[coords] = new_bomb
        self.map_drawer.add_bomb(new_bomb)
        player.change_bomb_status(new_bomb)
        player.bomb_count -= 1

    # handle player movement around a newly placed bomb and wall and box collision
    def check_position(self, player, new_pos):
        if self.is_position_clear(player, new_pos):
            player.move(new_pos)

    # checking if player is colliding with a wall, a box or a bomb
    def is_position_clear(self, player, position):
        return (position.collidelist(self.objects.walls_objects()) == -1
                and position.collidelist(self.objects.boxes_objects()) == -1
                and self.bomb_move(player, position))

    # handle movement around a bomb
    def bomb_move(self, player, position):
        bombs = self.objects.bomb_objects()

        # no bombs - can move freely
        if len(bombs) == 0:
            return True

        bindex = position.collidelist(bombs)

        # change player status if he is off the bomb
        if bindex == -1 and player.bomb:
            player.change_bomb_status()

        return bindex == -1 or bombs[bindex] is player.bomb
