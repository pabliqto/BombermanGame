import pygame
import os
import random
import sys
from global_variables import (COOLDOWN, PLAYER_SCALE, PLAYER_SPEED, BLOCK_SCALE, WINDOW_WIDTH, WINDOW_HEIGHT, N,
                              START_X, START_Y, REAL_SIZE, BOMB_SCALE, BOMB_COUNTDOWN)

PLAYERS = 3


class Player(pygame.sprite.Sprite):
    id_counter = 0

    def __init__(self, x, y, k, player_id=0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("idle-front.png", PLAYER_SCALE)
        self.rect.center = (x, y)
        self.speed = PLAYER_SPEED
        self.direction = "S"
        self.animation = 1
        self.cooldown = COOLDOWN
        self.player_id = Player.id_counter
        Player.id_counter += 1
        self.bomb = False
        self.bomb_count = 10
        self.current_bomb = 0
        self.bomb_strength = 2
        self.keys = k

    def update(self):
        pass

    def animation_move(self, direction):
        scale = PLAYER_SCALE
        if direction == "WD" or direction == "SD":
            direction = "D"
        if direction == "WA" or direction == "SA":
            direction = "A"

        if self.cooldown == 0:
            pic = 'walk-'
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
                pic += str(curr_animation) + '.png'
                self.image, self.rect = load_png(pic, scale)
            self.cooldown = COOLDOWN
        else:
            self.cooldown -= 1

    def orientation(self, direction):
        scale = PLAYER_SCALE
        x, y = self.rect.topleft
        if direction != self.direction:
            if direction == "W":
                self.image, self.rect = load_png("idle-back.png", scale)
            elif direction == "A":
                self.image, self.rect = load_png("idle-left.png", scale)
            elif direction == "S":
                self.image, self.rect = load_png("idle-front.png", scale)
            elif direction == "D":
                self.image, self.rect = load_png("idle-right.png", scale)
            elif direction == "SA" or direction == "WA":
                self.image, self.rect = load_png("idle-left.png", scale)
            elif direction == "SD" or direction == "WD":
                self.image, self.rect = load_png("idle-right.png", scale)
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

        if "A" in direction:
            new_pos.x -= self.speed

        if "D" in direction:
            new_pos.x += self.speed

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
            new_pos.y -= self.speed

        if "S" in direction:
            new_pos.y += self.speed

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


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, xcoord, ycoord):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("floor.png", BLOCK_SCALE)
        self.rect.topleft = (x, y)
        self.xcoord = xcoord
        self.ycoord = ycoord


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, xcoord, ycoord):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("fl.png", BLOCK_SCALE)
        self.rect.topleft = (x, y)
        self.xcoord = xcoord
        self.ycoord = ycoord


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, xcoord, ycoord, player_id, number, strength):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("bomb_1.png", BOMB_SCALE)
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
            self.image, _ = load_png("bomb_3.png", BOMB_SCALE)
        else:
            self.image, _ = load_png("bomb_2.png", BOMB_SCALE)

    # def explode(self):
    #     if self.state:
    #         return
    #     self.state = True
    #     s_x = max(1, self.xcoord - self.strength)
    #     f_x = min(N, self.xcoord + self.strength + 1)
    #     s_y = max(1, self.ycoord - self.strength)
    #     f_y = min(N, self.ycoord + self.strength + 1)
    #     for i in range(s_x, f_x):
    #         if i == self.xcoord:
    #             for j in range(s_y, f_y):
    #                 if j == self.ycoord:
    #                     continue
    #                 if walls.get((i, j)) is not None:
    #                     break
    #                 if boxes.get((i, j)) is not None:
    #                     boxes.get((i, j)).kill()
    #                     del boxes[(i, j)]
    #                 if bombs.get((i, j)) is not None:
    #                     bombs[(i, j)].explode()
    #         else:
    #             if walls.get((i, self.ycoord)) is not None:
    #                 break
    #             if boxes.get((i, self.ycoord)) is not None:
    #                 boxes.get((i, self.ycoord)).kill()
    #                 del boxes[(i, self.ycoord)]
    #             if bombs.get((i, self.ycoord)) is not None:
    #                 bombs[(i, self.ycoord)].explode()
    #     del bombs[(self.xcoord, self.ycoord)]
    #     new_explosion = explosion(*self.rect.center)
    #     explosions[self.rect.center] = new_explosion
    #     allExplosions.add(new_explosion)
    #     self.kill()
    def explode(self):
        if self.state:
            return
        self.state = True
        s_x = max(1, self.xcoord - self.strength)
        f_x = min(N, self.xcoord + self.strength + 1)
        s_y = max(1, self.ycoord - self.strength)
        f_y = min(N, self.ycoord + self.strength + 1)
        for i in range(s_x, f_x):
            if i == self.xcoord:
                for j in range(s_y, f_y):
                    if j == self.ycoord:
                        continue
                    if walls.get((i, j)) is not None:
                        break
                    if boxes.get((i, j)) is not None:
                        boxes.get((i, j)).kill()
                        del boxes[(i, j)]
                    if bombs.get((i, j)) is not None:
                        bombs[(i, j)].explode()
                    new_explosion = explosion((i + 1 / 2) * REAL_SIZE + START_X, (j + 1 / 2) * REAL_SIZE + START_Y)
                    explosions[(i, j)] = new_explosion
                    allExplosions.add(new_explosion)
            else:
                if walls.get((i, self.ycoord)) is not None:
                    break
                if boxes.get((i, self.ycoord)) is not None:
                    boxes.get((i, self.ycoord)).kill()
                    del boxes[(i, self.ycoord)]
                if bombs.get((i, self.ycoord)) is not None:
                    bombs[(i, self.ycoord)].explode()
                new_explosion = explosion((i + 1 / 2) * REAL_SIZE + START_X, (self.ycoord + 1 / 2) * REAL_SIZE + START_Y)
                explosions[(i, self.ycoord)] = new_explosion
                allExplosions.add(new_explosion)
        del bombs[(self.xcoord, self.ycoord)]
        new_explosion = explosion(*self.rect.center)
        explosions[self.rect.center] = new_explosion
        allExplosions.add(new_explosion)
        self.kill()

class explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("explosion1.png", BLOCK_SCALE)
        self.rect.center = (x, y)
        self.time = pygame.time.get_ticks()
        self.countdown = 400  # ?
        self.state = False  # ?

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time >= self.countdown:
            self.kill()
        if (current_time - self.time) >= self.countdown /2:
            self.image, _ = load_png("explosion3.png", BLOCK_SCALE)
        else:
            self.image, _ = load_png("explosion2.png", BLOCK_SCALE)


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, xcoord, ycoord):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("box3.png", BLOCK_SCALE)
        self.rect.topleft = (x, y)
        self.xcoord = xcoord
        self.ycoord = ycoord


def load_png(name, scale: float = 1):
    fullname = os.path.join("images", name)
    image = pygame.image.load(fullname)
    size = image.get_size()
    size = (int(size[0] * scale), int(size[1] * scale))
    image = pygame.transform.scale(image, size)
    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image, image.get_rect()


def initialize_board(chance=0.9):
    walls_dir = {}
    floors_arr = []
    boxes_dir = {}

    for i in range(N):
        for j in range(N):
            if i == 0 or i == N - 1 or j == 0 or j == N - 1:
                walls_dir[(i, j)] = Wall(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)
            elif i % 2 == 0 and j % 2 == 0:
                walls_dir[(i, j)] = Wall(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)
            else:
                floors_arr.append(Floor(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j))
                if (2 < i < N - 3 or 2 < j < N - 3) and random.random() <= chance:
                    boxes_dir[(i, j)] = Box(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)

    return walls_dir, floors_arr, boxes_dir


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    icon = pygame.image.load("images/icon.png")
    clock = pygame.time.Clock()
    pygame.display.set_icon(icon)

    bombs = {}
    explosions = {}
    walls, floors, boxes = initialize_board()
    allWalls = pygame.sprite.RenderPlain(list(walls.values()))
    allFloors = pygame.sprite.RenderPlain(floors)
    allBoxes = pygame.sprite.RenderPlain(list(boxes.values()))
    allBombs = pygame.sprite.RenderPlain(list(bombs.values()))
    allExplosions = pygame.sprite.RenderPlain(list(explosions.values()))

    player1 = Player(START_X + (3 * REAL_SIZE) / 2, START_Y + (3 * REAL_SIZE) / 2,
                     [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE])
    list_of_players = [player1]
    if PLAYERS > 1:
        player2 = Player(START_X + (N - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         START_Y + (N - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL])
        list_of_players.append(player2)

    if PLAYERS > 2:
        player3 = Player(START_X + (N - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         START_Y + (3 * REAL_SIZE) / 2,
                         [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_RSHIFT])
        list_of_players.append(player3)

    if PLAYERS > 3:
        player4 = Player(START_X + (3 * REAL_SIZE) / 2,
                         START_Y + (N - 3) * REAL_SIZE + (3 * REAL_SIZE) / 2,
                         [pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6, pygame.K_KP0])
        list_of_players.append(player4)

    allPlayers = pygame.sprite.RenderPlain(list_of_players)
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

        screen.fill((47, 47, 46))
        allBombs.update()
        font = pygame.font.Font(None, 36)
        text = font.render(f'Bomb status: {player1.bomb}, Bomb Count: {player1.bomb_count}', True, (255, 255, 255))
        screen.blit(text, (10, 10))
        allWalls.draw(screen)
        allFloors.draw(screen)
        allBoxes.draw(screen)
        allBombs.draw(screen)
        allPlayers.draw(screen)
        allExplosions.draw(screen)
        allExplosions.update()
        # print(allExplosions)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
