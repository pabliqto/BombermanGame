import pygame
import random
from map_generator import initialize_board
from bomb import Bomb
from global_variables import START_X, START_Y, REAL_SIZE
from explosion import Explosion
from modifiers import Modifier


class Board:
    def __init__(self, n, chance, players_count):
        self.walls, self.floors, self.boxes, self.players = initialize_board(n, chance, players_count)
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

    def update(self):
        self.bomb_sprites.update()
        self.explosion_sprites.update()
        self.modifier_sprites.update()
        self.player_sprites.update()

    def draw(self, screen):
        self.wall_sprites.draw(screen)
        self.floor_sprites.draw(screen)
        self.box_sprites.draw(screen)
        self.bomb_sprites.draw(screen)
        self.modifier_sprites.draw(screen)
        self.player_sprites.draw(screen)
        self.explosion_sprites.draw(screen)

    def get_players_sprites(self):
        return self.player_sprites

    def get_modifiers_sprites(self):
        return self.modifier_sprites

    def get_players(self):
        return list(self.players.values())

    def get_players_ids(self):
        return list(self.players.keys())

    def get_player(self, player_id):
        return self.players.get(player_id)

    def end_game(self):
        return len(self.get_players()) == 1

    def get_winner(self):
        return list(self.players.keys())[0]

    def is_wall(self, x, y):
        return self.walls.get((x, y)) is not None

    def delete_bomb(self, x, y):
        del self.bombs[(x, y)]

    def give_bomb(self, player_id):
        if player_id in self.players:
            self.players[player_id].give_bomb()

    def new_explosion(self, x, y):
        new_explosion = Explosion((x + 1 / 2) * REAL_SIZE + START_X, (y + 1 / 2) * REAL_SIZE + START_Y)
        self.explosions[(x, y)] = new_explosion
        self.explosion_sprites.add(new_explosion)

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

    def check_position(self, player, new_pos):
        if new_pos.collidelist(list(self.walls.values())) == -1 and new_pos.collidelist(list(self.boxes.values())) == -1:
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

    def no_boxes(self, x, y):
        return self.boxes.get((x, y)) is None

    def no_bombs(self, x, y):
        return self.bombs.get((x, y)) is None

    def place_bomb(self, player_id):
        player = self.players[player_id]
        if not player.bomb and player.bomb_count > 0:
            i, j = player.get_coords()
            if self.no_boxes(i, j) and self.no_bombs(i, j):
                new_bomb = Bomb(i, j, player_id, player.current_bomb, player.bomb_strength, self)
                self.bombs[(i, j)] = new_bomb
                self.bomb_sprites.add(new_bomb)
                player.change_bomb_status()
                player.bomb_count -= 1

    def handle_explosion(self, x, y, player_id):
        if self.boxes.get((x, y)) is not None:
            self.boxes.get((x, y)).kill()
            if player_id in self.players:
                self.players[player_id].score += 10

            del self.boxes[(x, y)]

            if random.random() <= 0.5:
                new_modifier = Modifier((x + 1 / 2) * REAL_SIZE + START_X, (y + 1 / 2) * REAL_SIZE + START_Y, x, y, random.choice(["speed", "bomb", "fire"]))
                self.modifiers[(x, y)] = new_modifier
                self.modifier_sprites.add(new_modifier)

        elif not self.no_bombs(x, y):
            self.bombs[(x, y)].explode()
        for i in list(self.players.keys()):
            if self.players[i] is not None:
                if self.players[i].get_coords() == (x, y):
                    self.players[player_id].score += 50
                    self.players[i].kill()
                    del self.players[i]

        self.new_explosion(x, y)
