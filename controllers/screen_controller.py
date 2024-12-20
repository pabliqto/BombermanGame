

class ScreenController:
    def __init__(self, objects):
        self.objects = objects

    def fill(self):
        self.objects.screen.fill((47, 47, 46))

    def resize(self):
        entities = [self.objects.walls, self.objects.boxes,
                    self.objects.bombs, self.objects.explosions, self.objects.modifiers,
                    self.objects.players, self.objects.floors]

        for d in entities:
            for entity in d.values():
                position = self.objects.calculate_position(entity.coords)
                entity.rect.center = position.x, position.y
