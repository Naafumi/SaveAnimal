import pygame

class Back(pygame.sprite.Sprite):

    def __init__(self,  filename, bg_size, spd):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.transform.scale((pygame.image.load(filename).convert_alpha()), bg_size)
        self.rect = self.surface.get_rect(bottomleft=(0, 0))
        self.speed = spd

    def update(self, *args):
        if self.rect.y < args[0]:
            self.rect.y += self.speed
        else:
            self.kill()
            self.remove()
