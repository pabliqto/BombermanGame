import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("idle-front.png", 1.3)
        self.rect.topleft = (x, y)
        # self.image = pygame.transform.rotate(self.image, 180)
        self.speed = 3
        self.direction = "N"
        self.animation = 1
    def update(self):
        pass
    def animation_move(self,direction):
        if direction == "D":
            if self.animation == 1:
                self.image, self.rect = load_png("walk-right2.png", 1.3)
                self.animation = 2
            elif self.animation == 2:
                self.image, self.rect = load_png("walk-right3.png", 1.3)
                self.animation = 3
            elif self.animation == 3:
                self.image, self.rect = load_png("walk-right4.png", 1.3)
                self.animation = 4
            elif self.animation == 4:
                self.image, self.rect = load_png("walk-right1.png", 1.3)
                self.animation = 1
        elif direction == "A":
            if self.animation == 1:
                self.image, self.rect = load_png("walk-left2.png", 1.3)
                self.animation = 2
            elif self.animation == 2:
                self.image, self.rect = load_png("walk-left3.png", 1.3)
                self.animation = 3
            elif self.animation == 3:
                self.image, self.rect = load_png("walk-left4.png", 1.3)
                self.animation = 4
            elif self.animation == 4:
                self.image, self.rect = load_png("walk-left1.png", 1.3)
                self.animation = 1
        elif direction == "W":
            if self.animation == 1:
                self.image, self.rect = load_png("walk-back2.png", 1.3)
                self.animation = 2
            elif self.animation == 2:
                self.image, self.rect = load_png("walk-back3.png", 1.3)
                self.animation = 3
            elif self.animation == 3:
                self.image, self.rect = load_png("walk-back4.png", 1.3)
                self.animation = 4
            elif self.animation == 4:
                self.image, self.rect = load_png("walk-back1.png", 1.3)
                self.animation = 1
        elif direction == "S":
            if self.animation == 1:
                self.image, self.rect = load_png("walk-front2.png", 1.3)
                self.animation = 2
            elif self.animation == 2:
                self.image, self.rect = load_png("walk-front3.png", 1.3)
                self.animation = 3
            elif self.animation == 3:
                self.image, self.rect = load_png("walk-front4.png", 1.3)
                self.animation = 4
            elif self.animation == 4:
                self.image, self.rect = load_png("walk-front1.png", 1.3)
                self.animation = 1
    def orientation(self, direction):
        x, y = self.rect.topleft
        if direction != self.direction:
            if direction == "W":
                self.image, self.rect = load_png("idle-back.png", 1.3)
            elif direction == "A":
                self.image, self.rect = load_png("idle-left.png", 1.3)
            elif direction == "S":
                self.image, self.rect = load_png("idle-front.png", 1.3)
            elif direction == "D":
                self.image, self.rect = load_png("idle-right.png", 1.3)
            elif direction == "SA" or direction == "WA":
                self.image, self.rect = load_png("idle-left.png", 1.3)
            elif direction == "SD" or direction == "WD":
                self.image, self.rect = load_png("idle-right.png", 1.3)
            if  direction not in {"WA", "AS", "SD", "WD"}:
                self.direction = direction
                self.animation_move(direction)
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

        if "W" in direction:
            new_pos.y -= self.speed

        if "S" in direction:
            new_pos.y += self.speed

        f = 1
        for wall in allWalls:
            if new_pos.colliderect(wall.rect):
                print("wall", wall.rect)
                f = 0
        if f:
            self.rect = new_pos
        else:
            new_pos = self.rect.copy()

        if "A" in direction:
            new_pos.x -= self.speed


        if "D" in direction:
            new_pos.x += self.speed

        f = 1
        for wall in allWalls:
            if new_pos.colliderect(wall.rect):
                f = 0
        if f:
            self.rect = new_pos
        else:
            new_pos = self.rect.copy()

        # self.rect = new_pos
        self.orientation(direction)


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
        # if len(xd) > 0:
        player.move(xd)

        screen.fill((47, 47, 46))
        allWalls.draw(screen)
        allFloors.draw(screen)
        allPlayers.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
