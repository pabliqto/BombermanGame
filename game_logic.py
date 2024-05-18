import pygame

from utilities import draw_scoreboard, endgame_text, draw_player_info
from screen_controller import ScreenController
from player_controller import PlayerController
from bomb_controller import BombController
from map_drawer import MapDrawer
from scoreboard import Scoreboard
import resolution as res
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml'])


class GameLogic:
    def __init__(self, game_objects):
        self.objects = game_objects
        self.scoreboard = Scoreboard()
        self.map_drawer = MapDrawer(self.objects)
        self.bomb_controller = BombController(self.objects, self.map_drawer, self.scoreboard)
        self.player_controller = PlayerController(self.objects, self.bomb_controller, self.map_drawer, self.scoreboard)
        self.screen_controller = ScreenController(self.objects)
        self.winner = None

    def check_endgame(self):
        return len(self.objects.players) <= 1

    def run(self, running=True):
        while running:
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and self.check_endgame():
                        running = False

                # Resize window
                if event.type == pygame.VIDEORESIZE:
                    res.OLD_START_X = res.START_X
                    res.OLD_START_Y = res.START_Y
                    res.WINDOW_WIDTH = event.w
                    res.WINDOW_HEIGHT = event.h
                    real_size = settings.image_size * settings.block_scale
                    res.START_X = (res.WINDOW_WIDTH - settings.n * real_size) // 2
                    res.START_Y = (res.WINDOW_HEIGHT - settings.n * real_size) // 2
                    self.screen_controller.resize()

            keys = pygame.key.get_pressed()

            self.screen_controller.fill()
            self.map_drawer.update()
            self.map_drawer.draw(self.objects.screen)

            draw_scoreboard(self.objects.screen, self.scoreboard)

            for player_id in range(1, settings.players + 1):
                player = self.objects.players.get(player_id)
                draw_player_info(self.objects.screen, player, player_id)

            # Game logic
            if not self.check_endgame():
                for player in self.map_drawer.player_sprites:
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
                        self.player_controller.place_bomb(player.player_id)
                    if pressed:
                        self.player_controller.move_player(player.player_id, pressed)

                    hit_list = pygame.sprite.spritecollide(player, self.map_drawer.modifier_sprites, False)
                    for hit in hit_list:
                        player.collect_modifier(hit)
            else:
                if self.winner is None:
                    self.winner = self.player_controller.get_winner()
                endgame_text(self.objects.screen, self.winner, res.WINDOW_WIDTH, res.WINDOW_HEIGHT)

            pygame.display.flip()
            self.objects.clock.tick(60)
