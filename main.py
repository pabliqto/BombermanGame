import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("icon.png", 1.3)
        self.rect.topleft = (x, y)
        self.speed = 1
    def update(self):
        pass

    def move(self, direction):
        #write the code to move the player but check if the next position is a wall or a floor
        #if it is a wall do not move
        match direction:
            case "W":
                self.rect.y -= self.speed
            case "A":
                self.rect.x -= self.speed
            case "S":
                self.rect.y += self.speed
            case "D":
                self.rect.x += self.speed

        for wall in allWalls:
            if self.rect.colliderect(wall.rect):
                if direction == "W":
                    self.rect.y += self.speed
                elif direction == "A":
                    self.rect.x += self.speed
                elif direction == "S":
                    self.rect.y -= self.speed
                elif direction == "D":
                    self.rect.x -= self.speed
                break

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
    w = (window_width - n*size)//2
    h = (window_height - n*size)//2

    walls = []
    floors = []
    for i in range(n):
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                walls.append(Wall(w + i*size, h + j*size))
            elif i % 2 == 0 and j % 2 == 0:
                walls.append(Wall(w + i*size, h + j*size))
            else:
                floors.append(Floor(w + i*size, h + j*size))
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
    player = Player(walls[0].rect.x + walls[0].image.get_width(), walls[0].rect.y+walls[0].image.get_height())

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
        if keys[pygame.K_w]:
            player.move("W")
        elif keys[pygame.K_a]:
            player.move("A")
        elif keys[pygame.K_s]:
            player.move("S")
        elif keys[pygame.K_d]:
            player.move("D")

        screen.fill((47, 47, 46))
        allWalls.draw(screen)
        allFloors.draw(screen)
        allPlayers.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
