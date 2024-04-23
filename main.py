import random

import pygame

import modifiers
from explosion import Explosion
from global_variables import (COOLDOWN, PLAYER_SCALE, PLAYER_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, N,
                              START_X, START_Y, REAL_SIZE, BOMB_SCALE, BOMB_COUNTDOWN, PLAYERS)
from loadpng import load_png
from mapgenerator import initialize_board
from textrender import render
from modifiers import Modifier


class Player(pygame.sprite.Sprite):
    id_counter = 1

    def __init__(self, x, y, k):
        pygame.sprite.Sprite.__init__(self)
        self.speed = PLAYER_SPEED
        self.direction = "S"
        self.animation = 1
        self.cooldown = COOLDOWN
        self.player_id = Player.id_counter
        Player.id_counter += 1
        self.bomb = False
        self.bomb_count = 1
        self.current_bomb = 0
        self.bomb_strength = 2
        self.keys = k
        if self.player_id == 2:
            self.color = "blue"
        elif self.player_id == 3:
            self.color = "red"
        elif self.player_id == 4:
            self.color = "green"
        else:
            self.color = ""
        if self.color:
            self.image, self.rect = load_png("animations/" + self.color + "/" + self.color + "-idle-front" + ".png", PLAYER_SCALE)
        else:
            self.image, self.rect = load_png("animations/yellow/" + self.color + "idle-front.png", PLAYER_SCALE)
        self.rect.center = (x, y)
        self.score = 0
        self.extra_speed = 0
        self.extra_fire = 0

    def update(self):
        pass

    def animation_move(self, direction):
        scale = PLAYER_SCALE
        if direction == "WD" or direction == "SD":
            direction = "D"
        if direction == "WA" or direction == "SA":
            direction = "A"

        if self.cooldown == 0:
            if self.color:
                pic = "animations/" + self.color + "/" + "walk-"
            else:
                pic = "animations/yellow/walk-"
            curr_animation = self.animation

            if curr_animation == 4:
                curr_animation = 1
            else:
                curr_animation += 1

            if direction == "D":
                pic += 'right'
            elif direction == "A":
                pic += 'left'
            elif direction == "W":
                pic += 'back'
            elif direction == "S":
                pic += 'front'

            if direction != "WS" and direction != "AD":
                self.animation = curr_animation
                if self.color:
                    pic += str(curr_animation) + '-' + self.color + '.png'
                else:
                    pic += str(curr_animation) + '.png'
                self.image, self.rect = load_png(pic, scale)
            self.cooldown = COOLDOWN
        else:
            self.cooldown -= 1

    def orientation(self, direction):
        scale = PLAYER_SCALE
        x, y = self.rect.topleft
        if direction != self.direction:
            if self.color:
                name = "animations/" + self.color + "/" + self.color + '-idle-'
            else:
                name = "animations/yellow/idle-"

            if direction == "W":
                name += "back"
            elif direction == "A":
                name += "left"
            elif direction == "S":
                name += "front"
            elif direction == "D":
                name += "right"
            elif direction == "SA" or direction == "WA":
                name += "left"
            elif direction == "SD" or direction == "WD":
                name += "right"
            name += '.png'
            self.image, self.rect = load_png(name, scale)
            self.direction = direction
        else:
            self.animation_move(direction)
        self.rect.topleft = (x, y)

    def move(self, direction):
        if len(direction) == 4 or direction == 'AD' or direction == 'WS':
            return

        if len(direction) == 3:
            if "W" in direction and "S" in direction:
                direction = direction.replace("W", "")
                direction = direction.replace("S", "")
            elif "A" in direction and "D" in direction:
                direction = direction.replace("A", "")
                direction = direction.replace("D", "")

        new_pos = self.rect.copy()
        self.orientation(direction)

        extra = 0
        if self.extra_speed > 0:
            self.extra_speed -= 1
            extra = 2

        if "A" in direction:
            new_pos.x -= self.speed + extra

        if "D" in direction:
            new_pos.x += self.speed + extra

        if new_pos.collidelist(list(walls.values())) == -1 and new_pos.collidelist(list(boxes.values())) == -1:
            blist = list(bombs.values())
            bindex = new_pos.collidelist(blist)
            if not self.bomb and bindex == -1:
                self.rect = new_pos
            elif self.bomb and bindex != -1:
                if blist[bindex].player_id == self.player_id and blist[bindex].number == self.current_bomb:
                    self.rect = new_pos
            elif self.bomb and bindex == -1:
                self.rect = new_pos
                self.bomb = False
                self.current_bomb += 1

        new_pos = self.rect.copy()

        if "W" in direction:
            new_pos.y -= self.speed + extra

        if "S" in direction:
            new_pos.y += self.speed + extra

        if new_pos.collidelist(list(walls.values())) == -1 and new_pos.collidelist(list(boxes.values())) == -1:
            blist = list(bombs.values())
            bindex = new_pos.collidelist(blist)
            if not self.bomb and bindex == -1:
                self.rect = new_pos
            elif self.bomb and bindex != -1:
                if blist[bindex].player_id == self.player_id and blist[bindex].number == self.current_bomb:
                    self.rect = new_pos
            elif self.bomb and bindex == -1:
                self.rect = new_pos
                self.bomb = False
                self.current_bomb += 1

    def place_bomb(self):
        if not self.bomb and self.bomb_count > 0:
            i, j = self.get_coords()
            if boxes.get((i, j)) is None and bombs.get((i, j)) is None:
                new_bomb = Bomb((i + 1 / 2) * REAL_SIZE + START_X, (j + 1 / 2) * REAL_SIZE + START_Y, i, j,
                                self.player_id, self.current_bomb, self.bomb_strength)
                bombs[(i, j)] = new_bomb
                allBombs.add(new_bomb)
                self.bomb = True
                self.bomb_count -= 1

    def get_coords(self):
        x, y = self.rect.center
        i = (x - START_X) // REAL_SIZE
        j = (y - START_Y) // REAL_SIZE
        return i, j

    def collect_modifier(self, modifier):
        if modifier.type == "speed":
            self.extra_speed = modifier.value
        elif modifier.type == "bomb":
            self.bomb_count += modifier.value
        elif modifier.type == "fire":
            self.extra_fire += modifier.value
        modifier.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, xcoord, ycoord, player_id, number, strength):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("animations/bomb/bomb_1.png", BOMB_SCALE)
        self.rect.center = (x, y)
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.player_id = player_id
        self.number = number
        self.placement_time = pygame.time.get_ticks()
        self.countdown = BOMB_COUNTDOWN
        self.strength = strength
        self.state = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.placement_time >= self.countdown:
            self.explode()
        if (current_time - self.placement_time) % 400 < 200:
            self.image, _ = load_png("animations/bomb/bomb_3.png", BOMB_SCALE)
        else:
            self.image, _ = load_png("animations/bomb/bomb_2.png", BOMB_SCALE)

    def explode(self):
        if self.state:
            return
        self.state = True

        bonus = 0
        if self.player_id in players and players[self.player_id].extra_fire > 0:
            players[self.player_id].extra_fire -= 1
            bonus = 2

        s_x = max(1, self.xcoord - self.strength - bonus)
        f_x = min(N, self.xcoord + self.strength + 1 + bonus)
        s_y = max(1, self.ycoord - self.strength - bonus)
        f_y = min(N, self.ycoord + self.strength + 1 + bonus)

        for i in range(self.xcoord, f_x):
            if i != self.xcoord and walls.get((i, self.ycoord)) is not None:
                break
            self.handle_explosion(i, self.ycoord)

        for i in range(self.xcoord, s_x-1, -1):
            if i != self.xcoord and walls.get((i, self.ycoord)) is not None:
                break
            self.handle_explosion(i, self.ycoord)

        for j in range(self.ycoord, f_y):
            if j != self.ycoord and walls.get((self.xcoord, j)) is not None:
                break
            self.handle_explosion(self.xcoord, j)

        for j in range(self.ycoord, s_y-1, -1):
            if j != self.ycoord and walls.get((self.xcoord, j)) is not None:
                break
            self.handle_explosion(self.xcoord, j)

        del bombs[(self.xcoord, self.ycoord)]
        new_explosion = Explosion(*self.rect.center)
        explosions[self.rect.center] = new_explosion
        allExplosions.add(new_explosion)
        if self.player_id in players: players[self.player_id].bomb_count += 1
        self.kill()

    def handle_explosion(self, x, y):
        if boxes.get((x, y)) is not None:
            boxes.get((x, y)).kill()
            if self.player_id in players:
                players[self.player_id].score += 10

            del boxes[(x, y)]

            if random.random() <= 0.5:
                new_modifier = Modifier((x + 1 / 2) * REAL_SIZE + START_X, (y + 1 / 2) * REAL_SIZE + START_Y, x, y, random.choice(["speed", "bomb", "fire"]))
                modifiers[(x, y)] = new_modifier
                allModifiers.add(new_modifier)

        elif bombs.get((x, y)) is not None:
            bombs[(x, y)].explode()
        for i in list(players.keys()):
            if players[i] is not None:
                if players[i].get_coords() == (x, y):
                    players[self.player_id].score += 50
                    players[i].kill()
                    del players[i]

        new_explosion = Explosion((x + 1 / 2) * REAL_SIZE + START_X, (y + 1 / 2) * REAL_SIZE + START_Y)
        explosions[(x, y)] = new_explosion
        allExplosions.add(new_explosion)

def draw_scoreboard(screen, players):
    font = pygame.font.Font(None, 30)
    x = WINDOW_WIDTH - 200
    y = 150
    for player in players:
        score_text = f"Player {player.player_id}: {player.score}"
        score_surface = font.render(score_text, True, (255, 255, 255))  # White color
        screen.blit(score_surface, (x, y))
        y += 40


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    icon = pygame.image.load("images/animations/yellow/idle-front.png")
    pygame.display.set_caption("Bomberman")
    clock = pygame.time.Clock()
    pygame.display.set_icon(icon)

    bombs = {}
    explosions = {}
    modifiers = {}
    walls, floors, boxes = initialize_board()
    allWalls = pygame.sprite.RenderPlain(list(walls.values()))
    allFloors = pygame.sprite.RenderPlain(floors)
    allBoxes = pygame.sprite.RenderPlain(list(boxes.values()))
    allBombs = pygame.sprite.RenderPlain(list(bombs.values()))
    allExplosions = pygame.sprite.RenderPlain(list(explosions.values()))
    allModifiers = pygame.sprite.RenderPlain(list(modifiers.values()))

    player1 = Player(START_X + (3 * REAL_SIZE) / 2, START_Y + (3 * REAL_SIZE) / 2,
                     [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE])
    players = {1: player1}
    if PLAYERS > 1:
        player2 = Player(START_X + (N - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         START_Y + (N - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL])
        players[2] = player2

    if PLAYERS > 2:
        player3 = Player(START_X + (N - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         START_Y + (3 * REAL_SIZE) / 2,
                         [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_RSHIFT])
        players[3] = player3

    if PLAYERS > 3:
        player4 = Player(START_X + (3 * REAL_SIZE) / 2,
                         START_Y + (N - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         [pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6, pygame.K_KP0])
        players[4] = player4

    allPlayers = pygame.sprite.RenderPlain(list(players.values()))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        for player in allPlayers:
            pressed = ''
            a, b, c, d, e = player.keys
            if keys[a]:
                pressed += 'W'
            if keys[b]:
                pressed += 'S'
            if keys[c]:
                pressed += 'A'
            if keys[d]:
                pressed += 'D'
            if keys[e]:
                player.place_bomb()
            if pressed:
                player.move(pressed)
            hit_list = pygame.sprite.spritecollide(player, allModifiers, False)
            for hit in hit_list:
                player.collect_modifier(hit)

        screen.fill((47, 47, 46))
        allBombs.update()
        allWalls.draw(screen)
        allFloors.draw(screen)
        allBoxes.draw(screen)
        allBombs.draw(screen)
        allPlayers.draw(screen)
        allExplosions.draw(screen)
        allExplosions.update()
        allModifiers.draw(screen)

        draw_scoreboard(screen, list(players.values()))

        if len(players) == 1:
            running = False
            winner = list(players.keys())[0]

            game_over_font = pygame.font.Font(None, 100)
            player_won = pygame.font.Font(None, 80)
            font_exit = pygame.font.Font(None, 40)
            game_over_text = render("GAME OVER", game_over_font, opx=7)
            player_won_text = render(f"PLAYER {winner} WON", player_won, opx=6)
            exit_text = render("Press ESC or Space to exit", font_exit, opx=5)
            game_over_text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            player_won_text_rect = player_won_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            exit_text_rect = exit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(player_won_text, player_won_text_rect)
            screen.blit(exit_text, exit_text_rect)

            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                            pygame.quit()
                            quit()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

