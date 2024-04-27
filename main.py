import pygame
import sys
import ctypes
from global_variables import N, REAL_SIZE, CHANCE, PLAYERS
import resolution as res
from board import Board
from utilities import draw_scoreboard, endgame_text

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    if sys.platform == "win32":
        HWND = pygame.display.get_wm_info()["window"]
        SW_MAXIMIZE = 3
        ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)
    res.WINDOW_HEIGHT = pygame.display.Info().current_h
    res.WINDOW_WIDTH = pygame.display.Info().current_w
    res.OLD_START_X = res.START_X = (res.WINDOW_WIDTH - N * REAL_SIZE) // 2
    res.OLD_START_Y = res.START_Y = (res.WINDOW_HEIGHT - N * REAL_SIZE) // 2
    icon = pygame.image.load("images/animations/yellow/idle-front.png")
    pygame.display.set_caption("Bomberman")
    clock = pygame.time.Clock()
    pygame.display.set_icon(icon)

    game_board = Board(N, CHANCE, PLAYERS)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                res.OLD_START_X = res.START_X
                res.OLD_START_Y = res.START_Y
                res.WINDOW_WIDTH = event.w
                res.WINDOW_HEIGHT = event.h
                res.START_X = (res.WINDOW_WIDTH - N * REAL_SIZE) // 2
                res.START_Y = (res.WINDOW_HEIGHT - N * REAL_SIZE) // 2
                game_board.resize()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        if not game_board.endgame():
            for player in game_board.player_sprites:

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
                    game_board.place_bomb(player.player_id)
                if pressed:
                    game_board.move_player(player.player_id, pressed)
                hit_list = pygame.sprite.spritecollide(player, game_board.modifier_sprites, False)
                for hit in hit_list:
                    player.collect_modifier(hit)

        screen.fill((47, 47, 46))
        game_board.update()
        game_board.draw(screen)

        draw_scoreboard(screen, game_board.get_players())

        if game_board.endgame():
            winner = game_board.get_winner()
            endgame_text(screen, winner, res.WINDOW_WIDTH, res.WINDOW_HEIGHT)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

