import pygame


from game_objects import GameObjects, GameMap
from global_variables import N, REAL_SIZE
import resolution as res
from game_logic import GameLogic
from pygame._sdl2 import Window


if __name__ == "__main__":
    # Initialize pygame
    pygame.init()

    # Maximize window
    screen = pygame.display.set_mode((res.WINDOW_WIDTH, res.WINDOW_HEIGHT), pygame.RESIZABLE)
    Window.from_display_module().maximize()

    # Set window size
    res.WINDOW_HEIGHT = pygame.display.Info().current_h
    res.WINDOW_WIDTH = pygame.display.Info().current_w
    res.OLD_START_X = res.START_X = (res.WINDOW_WIDTH - N * REAL_SIZE) // 2
    res.OLD_START_Y = res.START_Y = (res.WINDOW_HEIGHT - N * REAL_SIZE) // 2

    # Set window icon, title and game clock
    icon = pygame.image.load("images/animations/yellow/yellow-idle-front.png")
    pygame.display.set_caption("Bomberman")
    pygame.display.set_icon(icon)

    map_type = GameMap.RANDOM

    game_objects = GameObjects(screen, map_type)
    gameLogic = GameLogic(game_objects)
    gameLogic.run()

    pygame.quit()
