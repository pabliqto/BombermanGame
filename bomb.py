import pygame

from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml', 'images_paths.toml'])


class Bomb(pygame.sprite.Sprite):
    def __init__(self, position, coords, controller, loader, strength=settings.bomb_strength, player_id=5):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loader.load_png(settings.bomb_image_1, settings.bomb_scale)
        self.rect.center = position.x, position.y
        self._coords = coords
        self.player_id = player_id
        self.placement_time = pygame.time.get_ticks()
        self.strength = strength
        self.fire = False
        self.controller = controller
        self.loader = loader

    @property
    def xcoord(self):
        return self._coords.x

    @property
    def ycoord(self):
        return self._coords.y

    @property
    def coords(self):
        return self._coords

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.placement_time >= settings.bomb_cooldown:
            self.explode()
        if (current_time - self.placement_time) % 400 < 200:
            self.image, _ = self.loader.load_png(settings.bomb_image_3, settings.bomb_scale)
        else:
            self.image, _ = self.loader.load_png(settings.bomb_image_2, settings.bomb_scale)

    def explode(self):
        if self.fire:
            return
        self.fire = True

        vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for i in range(4):
            for j in range(self.strength + 1):
                coords = self.coords + tuple(j * z for z in vectors[i])
                if self.controller.objects.walls.get(coords):
                    break
                self.controller.handle_explosion(coords, self.player_id)

        self.controller.delete_bomb(self.coords)
        self.controller.new_explosion(self.coords)
        self.controller.give_bomb(self.player_id)
        self.kill()
