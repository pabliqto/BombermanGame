import os
import pygame


class Loader:
    def __init__(self):
        pass

    @staticmethod
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
