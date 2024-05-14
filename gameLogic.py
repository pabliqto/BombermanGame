from mapDrawer import mapDrawer
from playerController import playerController
from bombController import bombController
import resolution as res
from global_variables import N, REAL_SIZE, PLAYERS
from screenController import screenController
from utilities import draw_scoreboard, endgame_text, draw_player_info
import pygame


class gameLogic:
    def __init__(self, screen, walls, floors, boxes, bombs, explosions, modifiers, players):
        self.playerController = playerController(
            players, walls, floors, boxes, bombs, explosions, modifiers, self)
        self.bombController = bombController(
            bombs, explosions, players, modifiers, boxes, walls,self)
        self.mapDrawer = mapDrawer(
            walls, floors, boxes, players, modifiers, bombs, explosions, self)
        self.screenController = screenController(
            screen, walls, floors, boxes, bombs, explosions, modifiers, players, self)
        self.clock = pygame.time.Clock()

    def get_screen_controller(self):
        return self.screenController

    def get_player_controller(self):
        return self.playerController

    def get_bomb_controller(self):
        return self.bombController

    def get_map_drawer(self):
        return self.mapDrawer

    def endgame(self):
        return len(self.playerController.get_players()) == 1

    def run(self, running=True):
        while running:
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and self.endgame():
                        running = False

                # Resize window
                if event.type == pygame.VIDEORESIZE:
                    res.OLD_START_X = res.START_X
                    res.OLD_START_Y = res.START_Y
                    res.WINDOW_WIDTH = event.w
                    res.WINDOW_HEIGHT = event.h
                    res.START_X = (res.WINDOW_WIDTH - N * REAL_SIZE) // 2
                    res.START_Y = (res.WINDOW_HEIGHT - N * REAL_SIZE) // 2
                    self.screenController.resize()

            keys = pygame.key.get_pressed()

            # Game logic
            if not self.endgame():
                for player in self.mapDrawer.player_sprites:

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
                        self.playerController.place_bomb(player.player_id)
                    if pressed:
                        self.playerController.move_player(player.player_id, pressed)

                    hit_list = pygame.sprite.spritecollide(player, self.mapDrawer.modifier_sprites, False)
                    for hit in hit_list:
                        player.collect_modifier(hit)

            self.screenController.fill()
            self.mapDrawer.update()
            self.mapDrawer.draw(self.screenController.get_screen())

            draw_scoreboard(self.screenController.get_screen(), self.mapDrawer.scoreboard)

            for player_id in range(1, PLAYERS + 1):
                player = self.playerController.get_player(player_id)
                draw_player_info(self.screenController.get_screen(), player, player_id)

            # Endgame
            if self.endgame():
                winner = self.playerController.get_winner()
                endgame_text(self.screenController.get_screen(), winner, res.WINDOW_WIDTH, res.WINDOW_HEIGHT)

            pygame.display.flip()
            self.clock.tick(60)
