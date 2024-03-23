import pygame
import os
COOLDOWN = 8
PlAYER_SCALE = 1.3

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("idle-front.png", PlAYER_SCALE)
        self.rect.topleft = (x, y)
        self.speed = 2
        self.direction = "S"
        self.animation = 1
        self.cooldown = COOLDOWN

    def update(self):
        pass

    def animation_move(self, direction):
        scale = PlAYER_SCALE
        if self.cooldown == 0:
            pic = 'walk-'
            curr_animation = self.animation

            if curr_animation == 4:
                curr_animation = 1
            else:
                curr_animation += 1

            if direction == "D" or direction == "WD" or direction == "SD":
                pic += 'right'
            elif direction == "A" or direction == "WA" or direction == "SA":
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
        scale = PlAYER_SCALE
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
            if direction not in {"WA", "AS", "SD", "WD"}:
                self.direction = direction
                self.animation_move(direction)
            self.cooldown = COOLDOWN
        else:
            self.animation_move(direction)

        self.rect.topleft = (x, y)

    def move(self, direction):
        new_pos = self.rect.copy()

        if len(direction) == 3:
            if "W" in direction and "S" in direction:
                direction = direction.replace("W", "")
                direction = direction.replace("S", "")
            elif "A" in direction and "D" in direction:
                direction = direction.replace("A", "")
                direction = direction.replace("D", "")
        self.orientation(direction)

        if "A" in direction:
            new_pos.x -= self.speed

        if "D" in direction:
            new_pos.x += self.speed

        f = 1
        for wall in allWalls:
            if new_pos.colliderect(wall.rect):
                print("?")
                f = 0
                break
        if f:
            self.rect = new_pos
        else:
            new_pos = self.rect.copy()


        if "W" in direction:
            new_pos.y -= self.speed

        if "S" in direction:
            new_pos.y += self.speed

        f = 1
        for wall in allWalls:
            if new_pos.colliderect(wall.rect):
                print("wall", wall.rect.bottom, wall.rect.top, wall.rect.left, wall.rect.right)
                print("player", self.rect.bottom, self.rect.top, self.rect.left, self.rect.right)
                f = 0
                break
        if f:
            self.rect = new_pos



class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("floor.png", 3)
        self.rect.topleft = (x, y)


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("fl.png", 3)
        self.rect.topleft = (x, y)


class Box(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


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


def initialize_board(n, window_width, window_height, size=48):
    if n % 2 == 0:
        n += 1
    w = (window_width - n * size) // 2
    h = (window_height - n * size) // 2

    walls = []
    floors = []
    for i in range(n):
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                if i > 2:  ## DO WYWALENIA
                    walls.append(Wall(w + i * size, h + j * size))
            elif i % 2 == 0 and j % 2 == 0:

                walls.append(Wall(w + i * size, h + j * size))
            else:
                floors.append(Floor(w + i * size, h + j * size))
    return walls, floors


if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption("Bomberman")

    screen = pygame.display.set_mode((1400, 1000))
    icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    n = 15
    window_width = screen.get_width()
    window_height = screen.get_height()

    walls, floors = initialize_board(n, window_width, window_height)
    allWalls = pygame.sprite.RenderPlain(walls)
    allFloors = pygame.sprite.RenderPlain(floors)
    player = Player(walls[0].rect.x + walls[0].image.get_width(), walls[0].rect.y + walls[0].image.get_height())

    allPlayers = pygame.sprite.RenderPlain(player)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        keys = pygame.key.get_pressed()
        xd = ''
        if keys[pygame.K_w]:
            xd += 'W'
        if keys[pygame.K_a]:
            xd += 'A'
        if keys[pygame.K_s]:
            xd += 'S'
        if keys[pygame.K_d]:
            xd += 'D'
        if len(xd) > 0:
            player.move(xd)

        screen.fill((47, 47, 46))
        allWalls.draw(screen)
        allFloors.draw(screen)
        allPlayers.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
