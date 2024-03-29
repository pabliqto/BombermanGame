import pygame
import os
import random

from global_variables import (COOLDOWN, PLAYER_SCALE, PLAYER_SPEED, BLOCK_SCALE, WINDOW_WIDTH, WINDOW_HEIGHT, N,
                              START_X, START_Y, REAL_SIZE, BOMB_SCALE)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_id=0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("idle-front.png", PLAYER_SCALE)
        self.rect.center = (x, y)
        self.speed = PLAYER_SPEED
        self.direction = "S"
        self.animation = 1
        self.cooldown = COOLDOWN
        self.player_id = player_id
        self.bomb = False
        self.bomb_count = 10
        self.current_bomb = 0

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

        if new_pos.collidelist(walls) == -1 and new_pos.collidelist(list(boxes.values())) == -1:
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

        if new_pos.collidelist(walls) == -1 and new_pos.collidelist(list(boxes.values())) == -1:
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
                new_bomb = Bomb((i+1/2) * REAL_SIZE + START_X, (j+1/2) * REAL_SIZE + START_Y, i, j, self.player_id, self.current_bomb)
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

#jak gracz kladzie bombe to do czasu zejscia z niej ma jakas flage, jak zejdzie to sie przelacza i nie moze chodzic po bombie/ trzeba rozpatrzec aby nie mogl przejsc z jednej na druga
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, xcoord, ycoord, player_id, number):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("bomb_1.png", BOMB_SCALE)
        self.rect.center = (x, y)
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.player_id = player_id
        self.number = number

    def explode(self):
        pass


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


def initialize_board(chance=0.1):
    walls_arr = []
    floors_arr = []
    boxes_dir = {}

    for i in range(N):
        for j in range(N):
            if i == 0 or i == N - 1 or j == 0 or j == N - 1:
                walls_arr.append(Wall(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j))
            elif i % 2 == 0 and j % 2 == 0:
                walls_arr.append(Wall(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j))
            else:
                floors_arr.append(Floor(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j))
                if (2 < i < N - 3 or 2 < j < N - 3) and random.random() <= chance:
                    boxes_dir[(i, j)] = Box(START_X + i * REAL_SIZE, START_Y + j * REAL_SIZE, i, j)

    return walls_arr, floors_arr, boxes_dir


if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption("Bomberman")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    bombs = {}
    walls, floors, boxes = initialize_board()
    allWalls = pygame.sprite.RenderPlain(walls)
    allFloors = pygame.sprite.RenderPlain(floors)
    allBoxes = pygame.sprite.RenderPlain(list(boxes.values()))
    allBombs = pygame.sprite.RenderPlain(list(bombs.values()))
    player = Player(START_X+(3*REAL_SIZE)/2, START_Y+(3*REAL_SIZE)/2)

    allPlayers = pygame.sprite.RenderPlain([player])
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        keys = pygame.key.get_pressed()
        direction = ''
        if keys[pygame.K_w]:
            direction += 'W'
        if keys[pygame.K_s]:
            direction += 'S'
        if keys[pygame.K_a]:
            direction += 'A'
        if keys[pygame.K_d]:
            direction += 'D'
        if direction:
            player.move(direction)

        if keys[pygame.K_SPACE]:
            player.place_bomb()

        screen.fill((47, 47, 46))

        font = pygame.font.Font(None, 36)
        text = font.render(f'Bomb status: {player.bomb}, Bomb Count: {player.bomb_count}', True, (255, 255, 255))
        screen.blit(text, (10, 10))
        allWalls.draw(screen)
        allFloors.draw(screen)
        allBoxes.draw(screen)
        allBombs.draw(screen)
        allPlayers.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
