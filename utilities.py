import pygame
import os
from global_variables import WINDOW_WIDTH, WINDOW_HEIGHT

# code from https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame

_circle_cache = {}


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


def draw_scoreboard(screen, players):
    font = pygame.font.Font(None, 30)
    x = WINDOW_WIDTH - 200
    y = 350
    for player in players:
        score_text = f"Player {player.player_id}: {player.score}"
        score_surface = font.render(score_text, True, (255, 255, 255))  # White color
        screen.blit(score_surface, (x, y))
        y += 40


def endgame_text(screen, winner):
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
