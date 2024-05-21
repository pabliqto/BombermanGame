import pygame
from Util import resolution as res, variables as var
from math import ceil
from dynaconf import Dynaconf

images = Dynaconf(settings_files=['images_paths.toml'])


class Drawer:
    def __init__(self, screen, loader):
        self._circle_cache = {}
        self._screen = screen
        self._loader = loader

    @property
    def screen(self):
        return self._screen

    @property
    def loader(self):
        return self._loader

    # code from https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame
    def _circlepoints(self, r):
        r = int(round(r))
        if r in self._circle_cache:
            return self._circle_cache[r]
        x, y, e = r, 0, 1 - r
        self._circle_cache[r] = points = []
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

    def render(self, text, font, gfcolor=pygame.Color('white'), ocolor=(0, 0, 0), opx=5):
        textsurface = font.render(text, True, gfcolor).convert_alpha()
        w = textsurface.get_width() + 2 * opx
        h = font.get_height()

        osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

        for dx, dy in self._circlepoints(opx):
            surf.blit(osurf, (dx + opx, dy + opx))

        surf.blit(textsurface, (opx, opx))
        return surf

    # end of stackoverflow code

    def endgame_text(self, winner):
        game_over_font = pygame.font.Font(None, 100)
        player_won = pygame.font.Font(None, 80)
        font_exit = pygame.font.Font(None, 40)
        game_over_text = self.render("GAME OVER", game_over_font, opx=7)
        if winner is None:
            player_won_text = self.render("DRAW", player_won, opx=6)
        else:
            player_won_text = self.render(f"{var.player_names[winner - 1]} WON", player_won, opx=6)
        exit_text = self.render("Press Space to restart or ESC to exit ", font_exit, opx=5)
        game_over_text_rect = game_over_text.get_rect(center=(res.WINDOW_WIDTH // 2, res.WINDOW_HEIGHT // 2 - 100))
        player_won_text_rect = player_won_text.get_rect(center=(res.WINDOW_WIDTH // 2, res.WINDOW_HEIGHT // 2 - 30))
        exit_text_rect = exit_text.get_rect(center=(res.WINDOW_WIDTH // 2, res.WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(game_over_text, game_over_text_rect)
        self.screen.blit(player_won_text, player_won_text_rect)
        self.screen.blit(exit_text, exit_text_rect)

    def draw_player_info(self, player, player_id):
        positions = [(0, 0), (res.WINDOW_WIDTH, res.WINDOW_HEIGHT), (res.WINDOW_WIDTH, 0), (0, res.WINDOW_HEIGHT)]
        colors = ["yellow", "blue", "red", "green"]
        pos = ["topleft", "bottomright", "topright", "bottomleft"]

        # If player is dead, show dead head
        if player is None:
            head_image, head_rect = self.loader.load_png(f"heads/{var.players_colors[var.players_colors_values[player_id-1]]}-head-dead.png", 2.5)
        else:
            head_image, head_rect = self.loader.load_png(f"heads/{player.color}-head.png", 2.5)

        setattr(head_rect, pos[player_id - 1], positions[player_id - 1])

        # If player is dead, don't show bomb count, speed and radius
        if player:
            # Load images
            bomb_image, bomb_rect = self.loader.load_png(images.bomb_image_1, 3)
            radius_image, radius_rect = self.loader.load_png(images.fire, 3)
            speed_image, speed_rect = self.loader.load_png(images.speed, 3)

            # Load text
            font = pygame.font.Font(None, 36)
            text_surface = font.render(f"{player.name}", True, (255, 255, 255))
            bomb_count_text_surface = font.render(f"{player.bomb_count}", True, (255, 255, 255))
            speed_text_surface = font.render(f"{ceil(player.extra_speed / 100)}", True, (255, 255, 255))
            radius_text_surface = font.render(f"{player.extra_fire}", True, (255, 255, 255))

            # Get text rectangles
            text_rect = text_surface.get_rect()
            bomb_count_text_rect = bomb_count_text_surface.get_rect()
            speed_text_rect = speed_text_surface.get_rect()
            radius_text_rect = radius_text_surface.get_rect()

            # Set the position of the images and text
            vertical_offset = head_rect.height if player_id % 2 == 1 else -head_rect.height
            setattr(bomb_rect, pos[player_id - 1],
                    (positions[player_id - 1][0], positions[player_id - 1][1] + vertical_offset))
            vertical_offset_radius = bomb_rect.height + 10 if player_id % 2 == 1 else -bomb_rect.height - 10
            vertical_offset_speed = radius_rect.height + 10 if player_id % 2 == 1 else -radius_rect.height - 10
            radius_rect.center = bomb_rect.centerx, bomb_rect.centery + vertical_offset_radius
            speed_rect.center = radius_rect.centerx, radius_rect.centery + vertical_offset_speed

            direction = 1 if player_id in (1, 4) else -1
            text_rect.center = (head_rect.centerx + direction * (head_rect.width + 10), head_rect.centery)
            bomb_count_text_rect.center = (bomb_rect.centerx + direction * bomb_rect.width, bomb_rect.centery)
            speed_text_rect.center = (speed_rect.centerx + direction * speed_rect.width, speed_rect.centery)
            radius_text_rect.center = (radius_rect.centerx + direction * radius_rect.width, radius_rect.centery)

            self.screen.blit(bomb_image, bomb_rect)
            self.screen.blit(radius_image, radius_rect)
            self.screen.blit(speed_image, speed_rect)
            self.screen.blit(text_surface, text_rect)
            self.screen.blit(bomb_count_text_surface, bomb_count_text_rect)
            self.screen.blit(speed_text_surface, speed_text_rect)
            self.screen.blit(radius_text_surface, radius_text_rect)
        self.screen.blit(head_image, head_rect)

    def draw_scoreboard(self, scoreboard):
        font = pygame.font.Font(None, 30)
        x = res.WINDOW_WIDTH - 130
        y = res.WINDOW_HEIGHT // 2 - 80
        for player_id, score in scoreboard.score.items():
            score_text = f"{var.player_names[player_id-1]}: {score}"
            score_surface = font.render(score_text, True, (255, 255, 255))  # White color
            self.screen.blit(score_surface, (x, y))
            y += 40

    def count(self, i):
        game_over_font = pygame.font.Font(None, 200)
        game_over_text = self.render(str(i), game_over_font, opx=7)
        game_over_text_rect = game_over_text.get_rect(center=(res.WINDOW_WIDTH // 2, res.WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_text_rect)
        pygame.display.update()
