import pygame

from global_variables import (WINDOW_WIDTH, WINDOW_HEIGHT, N, PLAYERS, CHANCE)
from board import Board
from utilities import draw_scoreboard, endgame_text

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

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
            running = False
            winner = game_board.get_winner()

            endgame_text(screen, winner)

            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                            pygame.quit()
                            quit()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

