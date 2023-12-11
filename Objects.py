from math import ceil
import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, surface, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(surface, (75, 50))
        self.rect = self.image.get_rect(center=(x, -50))
        self.mask = pygame.mask.from_surface(self.image)

        self.add(group)

    def update(self, *args):
        if self.rect.y < args[0]:

            self.rect.y += args[1]
        else:
            self.kill()
            self.remove()


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        print(1)
        self.image = pygame.transform.scale(pygame.image.load("images/bear3.png").convert_alpha(), (width // 10, width // 7))
        self.rect = self.image.get_rect(centerx=width // 2, bottom=height - self.image.get_height() * 2)
        self.rect_begin = self.image.get_rect(centerx=width // 2, bottom=height - self.image.get_height() * 2)

        self.mask = pygame.mask.from_surface(self.image)


class Background:
    def __init__(self, WIDTH, HEIGHT):
        self.image = pygame.transform.scale(pygame.image.load("images/bg1.png").convert(), (WIDTH, HEIGHT))
        self.tiles = ceil(HEIGHT / self.image.get_height()) + 1  # tiles make endless background scrolling ,
        self.list_bg = [self.image for x in range(self.tiles)]
        self.scroll = 0  # variable which scroll our background


class Button:
    def __init__(self, y, width, height, name):
        self.image = pygame.transform.scale(pygame.image.load(f"images/buttons/{name}"), (width // 6, height //15))

        self.rect = self.image.get_rect(center=(0, y))
        print(y)
        self.rect.x = width//2 - self.image.get_width()//2

    def draws(self):
        # draw button

        from main import screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # get mouse position on the screen

        pos = pygame.mouse.get_pos()

        action = False
        # check if mouse is over the button and click it
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        return action
