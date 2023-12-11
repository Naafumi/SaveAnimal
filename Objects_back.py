import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, surface, spd, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(surface, (75, 50))
        self.rect = self.image.get_rect(center=(x, -50))
        self.speed = spd

        self.add(group)


    def update(self, *args):
        if self.rect.y < args[0]:
            self.rect.move_ip(0, args[1])
        else:
            self.kill()
            self.remove()
