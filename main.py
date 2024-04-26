import pygame

from global_variables import (WINDOW_WIDTH, WINDOW_HEIGHT, N, PLAYERS, CHANCE)
from textrender import render
from board import Board


def draw_scoreboard(screen, players):
    font = pygame.font.Font(None, 30)
    x = WINDOW_WIDTH - 200
    y = 150
    for player in players:
        score_text = f"Player {player.player_id}: {player.score}"
        score_surface = font.render(score_text, True, (255, 255, 255))  # White color
        screen.blit(score_surface, (x, y))
        y += 40


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

        for player in game_board.get_players_sprites():

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
                game_board.place_bomb(player.get_player_id())
            if pressed:
                game_board.move_player(player.get_player_id(), pressed)
            # print(game_board.get_modifiers_sprites())
            # hit_list = pygame.sprite.spritecollide(player, game_board.get_modifiers_sprites(), False)
            # for hit in hit_list:
            #     player.collect_modifier(hit)

        screen.fill((47, 47, 46))
        game_board.update()
        game_board.draw(screen)

        draw_scoreboard(screen, game_board.get_players())

        if game_board.end_game():
            running = False
            winner = game_board.get_winner()

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

