import pygame

from Objects.game_objects import GameObjects, GameMap
from Util import resolution as res, variables as var
from Controllers.game_logic import GameLogic
from pygame._sdl2 import Window
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml'])


def main():
    # Initialize pygame
    pygame.init()

    # Maximize window
    screen = pygame.display.set_mode((res.WINDOW_WIDTH, res.WINDOW_HEIGHT), pygame.RESIZABLE)
    Window.from_display_module().maximize()

    # Set window size
    res.WINDOW_HEIGHT = pygame.display.Info().current_h
    res.WINDOW_WIDTH = pygame.display.Info().current_w
    real_size = settings.image_size * settings.block_scale
    res.OLD_START_X = res.START_X = (res.WINDOW_WIDTH - settings.n * real_size) // 2
    res.OLD_START_Y = res.START_Y = (res.WINDOW_HEIGHT - settings.n * real_size) // 2

    # Set window icon, title and game clock
    icon = pygame.image.load("images/animations/yellow/yellow-idle-front.png")
    pygame.display.set_caption("Bomberman")
    pygame.display.set_icon(icon)

    game = True
    while game:
        game_objects = GameObjects(screen)
        game_logic = GameLogic(game_objects)
        game = game_logic.run()

    pygame.quit()


if __name__ == "__main__":
    var.map_type = GameMap.FULL
    main()
