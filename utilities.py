import pygame
import os
from math import ceil
from global_variables import REAL_SIZE
import resolution as res

# code from https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame

_circle_cache = {}

# Draw the outline of the game over text
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render(text, font, gfcolor=pygame.Color('white'), ocolor=(0,0,0), opx=5):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

# end of stackoverflow code


def draw_scoreboard(screen, scoreboard):
    font = pygame.font.Font(None, 30)
    x = res.WINDOW_WIDTH - 130
    y = res.WINDOW_HEIGHT // 2 - 80
    for player_id, score in scoreboard.score.items():
        score_text = f"Player {player_id}: {score}"
        score_surface = font.render(score_text, True, (255, 255, 255))  # White color
        screen.blit(score_surface, (x, y))
        y += 40


def endgame_text(screen, winner, window_width, window_height):
    game_over_font = pygame.font.Font(None, 100)
    player_won = pygame.font.Font(None, 80)
    font_exit = pygame.font.Font(None, 40)
    game_over_text = render("GAME OVER", game_over_font, opx=7)
    if winner is None:
        player_won_text = render("DRAW", player_won, opx=6)
    else:
        player_won_text = render(f"PLAYER {winner} WON", player_won, opx=6)
    exit_text = render("Press ESC or Space to exit", font_exit, opx=5)
    game_over_text_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 100))
    player_won_text_rect = player_won_text.get_rect(center=(window_width // 2, window_height // 2 - 30))
    exit_text_rect = exit_text.get_rect(center=(window_width // 2, window_height // 2 + 20))
    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(player_won_text, player_won_text_rect)
    screen.blit(exit_text, exit_text_rect)


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


# Calculate the positions of the objects in the game
def calculate_position(x, y):
    return (x + 1 / 2) * REAL_SIZE + res.START_X, (y + 1 / 2) * REAL_SIZE + res.START_Y


# Calculate the position of the player
def calculate_player_position(x, y):
    new_x = x - res.OLD_START_X
    new_y = y - res.OLD_START_Y
    return res.START_X + new_x, res.START_Y + new_y


def draw_player_info(screen, player, player_id):
    positions = [(0, 0), (res.WINDOW_WIDTH, res.WINDOW_HEIGHT), (res.WINDOW_WIDTH, 0), (0, res.WINDOW_HEIGHT)]
    colors = ["yellow", "blue", "red", "green"]
    pos = ["topleft", "bottomright", "topright", "bottomleft"]

    # If player is dead, show dead head
    if player is None:
        head_image, head_rect = load_png(f"heads/{colors[player_id-1]}-head-dead.png", 2.5)
    else:
        head_image, head_rect = load_png(f"heads/{player.color}-head.png", 2.5)

    setattr(head_rect, pos[player_id-1], positions[player_id-1])

    # If player is dead, don't show bomb count, speed and radius
    if player:
        # Load images
        bomb_image, bomb_rect = load_png(f"animations/bomb/bomb_1.png", 3)
        radius_image, radius_rect = load_png(f"modifiers/fire.png", 3)
        speed_image, speed_rect = load_png(f"modifiers/speed.png", 3)

        # Load text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Player {player.player_id}", True, (255, 255, 255))
        bomb_count_text_surface = font.render(f"{player.bomb_count}", True, (255, 255, 255))
        speed_text_surface = font.render(f"{ceil(player.extra_speed/100)}", True, (255, 255, 255))
        radius_text_surface = font.render(f"{player.extra_fire}", True, (255, 255, 255))

        # Get text rectangles
        text_rect = text_surface.get_rect()
        bomb_count_text_rect = bomb_count_text_surface.get_rect()
        speed_text_rect = speed_text_surface.get_rect()
        radius_text_rect = radius_text_surface.get_rect()

        # Set the position of the images and text
        vertical_offset = head_rect.height if player_id % 2 == 1 else -head_rect.height
        setattr(bomb_rect, pos[player_id - 1], (positions[player_id - 1][0], positions[player_id - 1][1] + vertical_offset))
        vertical_offset_radius = bomb_rect.height + 10 if player_id % 2 == 1 else -bomb_rect.height - 10
        vertical_offset_speed = radius_rect.height + 10 if player_id % 2 == 1 else -radius_rect.height - 10
        radius_rect.center = bomb_rect.centerx, bomb_rect.centery + vertical_offset_radius
        speed_rect.center = radius_rect.centerx, radius_rect.centery + vertical_offset_speed

        direction = 1 if player_id in (1, 4) else -1
        text_rect.center = (head_rect.centerx + direction * (head_rect.width + 10), head_rect.centery)
        bomb_count_text_rect.center = (bomb_rect.centerx + direction * bomb_rect.width, bomb_rect.centery)
        speed_text_rect.center = (speed_rect.centerx + direction * speed_rect.width, speed_rect.centery)
        radius_text_rect.center = (radius_rect.centerx + direction * radius_rect.width, radius_rect.centery)

        screen.blit(bomb_image, bomb_rect)
        screen.blit(radius_image, radius_rect)
        screen.blit(speed_image, speed_rect)
        screen.blit(text_surface, text_rect)
        screen.blit(bomb_count_text_surface, bomb_count_text_rect)
        screen.blit(speed_text_surface, speed_text_rect)
        screen.blit(radius_text_surface, radius_text_rect)
    screen.blit(head_image, head_rect)
