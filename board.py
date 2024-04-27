import pygame
import random
from map_generator import initialize_board
from bomb import Bomb
from explosion import Explosion
from modifiers import Modifier
from utilities import calculate_position, calculate_player_position


class Board:
    def __init__(self, n, box_chance, players_count, extra_bomb_chance, modifier_chance):
        self.walls, self.floors, self.boxes, self.players = initialize_board(n, box_chance, players_count)
        self.bombs = {}
        self.explosions = {}
        self.modifiers = {}
        self.wall_sprites = pygame.sprite.RenderPlain(list(self.walls.values()))
        self.floor_sprites = pygame.sprite.RenderPlain(self.floors)
        self.box_sprites = pygame.sprite.RenderPlain(list(self.boxes.values()))
        self.bomb_sprites = pygame.sprite.RenderPlain(list(self.bombs.values()))
        self.explosion_sprites = pygame.sprite.RenderPlain(list(self.explosions.values()))
        self.modifier_sprites = pygame.sprite.RenderPlain(list(self.modifiers.values()))
        self.player_sprites = pygame.sprite.RenderPlain(list(self.players.values()))
        self.extra_bomb_chance = extra_bomb_chance
        self.modifier_chance = modifier_chance
        self.scoreboard = {i: 0 for i in range(1, players_count+1)}

    def update(self):
        self.bomb_sprites.update()
        self.explosion_sprites.update()
        self.modifier_sprites.update()

    def draw(self, screen):
        self.wall_sprites.draw(screen)
        self.floor_sprites.draw(screen)
        self.box_sprites.draw(screen)
        self.bomb_sprites.draw(screen)
        self.modifier_sprites.draw(screen)
        self.player_sprites.draw(screen)
        self.explosion_sprites.draw(screen)

    def get_players(self):
        return list(self.players.values())

    def players_ids(self):
        return list(self.players.keys())

    def get_player(self, player_id):
        return self.players.get(player_id)

    def endgame(self):
        return len(self.get_players()) == 1

    def get_winner(self):
        return list(self.players.keys())[0]

    def is_wall(self, x, y):
        return self.walls.get((x, y)) is not None

    def is_box(self, x, y):
        return self.boxes.get((x, y)) is not None

    def delete_bomb(self, x, y):
        del self.bombs[(x, y)]

    def give_bomb(self, player_id):
        if player_id in self.players:
            self.players[player_id].give_bomb()

    def new_explosion(self, x, y):
        new_explosion = Explosion(*calculate_position(x, y), x, y)
        self.explosions[(x, y)] = new_explosion
        self.explosion_sprites.add(new_explosion)

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
            player.change_extra_speed(-1)
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

    def no_bombs(self, x, y):
        return self.bombs.get((x, y)) is None

    def place_bomb(self, player_id):
        player = self.players[player_id]
        if not player.bomb and player.bomb_count > 0:
            i, j = player.get_coords()
            if not self.is_box(i, j) and self.no_bombs(i, j):
                new_bomb = Bomb(i, j, self, player.bomb_strength, player_id, player.current_bomb)
                self.bombs[(i, j)] = new_bomb
                self.bomb_sprites.add(new_bomb)
                player.change_bomb_status()
                player.bomb_count -= 1

    def handle_explosion(self, x, y, player_id):
        if self.is_box(x, y):
            self.boxes.get((x, y)).kill()
            self.scoreboard[player_id] += 10

            del self.boxes[(x, y)]

            random_number = random.random()

            # modifiers and extra bombs
            if self.extra_bomb_chance <= random_number <= self.modifier_chance:
                new_modifier = Modifier(*calculate_position(x, y), x, y)
                self.modifiers[(x, y)] = new_modifier
                self.modifier_sprites.add(new_modifier)
            elif random_number < self.extra_bomb_chance:
                new_bomb = Bomb(x, y, self)
                self.bombs[(x, y)] = new_bomb
                self.bomb_sprites.add(new_bomb)

        elif not self.no_bombs(x, y):
            self.bombs[(x, y)].explode()

        for i in list(self.players.keys()):
            if self.players[i] is not None:
                if self.players[i].get_coords() == (x, y):
                    if i != player_id:
                        self.scoreboard[player_id] += 50
                    self.players[i].kill()
                    del self.players[i]

        self.new_explosion(x, y)

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
