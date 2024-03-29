from math import ceil
import pygame
from random import randint

pygame.init()


class Enemy:
    class staticEnemy(pygame.sprite.Sprite):
        def __init__(self, x, surface, group):
            pygame.sprite.Sprite.__init__(self)

            self.image = surface
            self.height = self.image.get_height()
            self.rect = self.image.get_rect(center=(x, -self.height))
            self.mask = pygame.mask.from_surface(self.image)

            self.add(group)

        def update(self, *args):

            if self.rect.y < args[0]:

                self.rect.y += args[1]
            else:
                self.kill()
                self.remove()

    class staticKillerEnemy(pygame.sprite.Sprite):
        def __init__(self, x, surface, group):
            pygame.sprite.Sprite.__init__(self)

            self.image = surface
            self.height = self.image.get_height()
            self.rect = self.image.get_rect(center=(x, -self.height))
            self.mask = pygame.mask.from_surface(self.image)

            self.add(group)

        def update(self, *args):

            if self.rect.y < args[0]:

                self.rect.y += args[1]
            else:
                self.kill()
                self.remove()

    class animaticEnemy(pygame.sprite.Sprite):
        def __init__(self, x, surfaces, group):
            pygame.sprite.Sprite.__init__(self)
            self.images_pack = surfaces
            self.pack_len = len(self.images_pack) - 1
            self.i = 0

            self.image = surfaces[0]
            self.height = self.image.get_height()
            self.rect = self.image.get_rect(center=(x, -self.height))
            self.mask = pygame.mask.from_surface(self.image)

            self.add(group)

        def animateEnemy(self):
            self.image = self.images_pack[self.i]
            if self.i == self.pack_len:
                self.i = 0
            else:
                self.i += 1

        def update(self, height, game_speed, x=0):
            if x == 0:
                if self.rect.y < height:
                    self.rect.y += game_speed
                else:
                    self.kill()
                    self.remove()

            if x == 1:
                self.image = self.images_pack[self.i]
                if self.i == self.pack_len:
                    self.i = 0
                else:
                    self.i += 1
                x = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.i = int(0)
        self.width = width
        self.height = height
        self.images_pack = [
            pygame.transform.scale(pygame.image.load(f"images/player/bear/{i}.png").convert_alpha(),
                                   (width // 10, width // 7)) for i in range(3)]
        self.pack_len = len(self.images_pack) - 1
        self.image = self.images_pack[0]
        self.rect = self.image.get_rect(centerx=width // 2, bottom=height - self.image.get_height() * 4)
        self.rect_begin = (width // 2 - (self.rect.width // 2), height - self.image.get_height() * 4)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if self.rect.y < args[0]:
            self.rect.y += args[1]

    def animatePlayer(self, playerNotHit):
        if playerNotHit:
            self.images_pack = [
                pygame.transform.scale(pygame.image.load(f"images/player/bear/{i}.png").convert_alpha(), (self.width // 10, self.width // 7)) for i in range(3)]
        if not playerNotHit:
            self.images_pack = [
                    pygame.transform.scale(pygame.image.load(f"images/player/stars/{i}.png").convert_alpha(), (self.width // 10, self.width // 7)) for i in range(4)]
        self.image = self.images_pack[self.i]
        if self.i == self.pack_len:
            self.i = 0
        else:
            self.i += 1


class Background:
    def __init__(self, WIDTH, HEIGHT):
        self.image = pygame.transform.scale(pygame.image.load("images/scoreboard/background.png").convert(), (WIDTH, HEIGHT))
        self.tiles = ceil(HEIGHT/self.image.get_height())+1 #tiles make endless background scrolling ,
        self.list_bg = [self.image for x in range(self.tiles)]
        self.scroll = 0 #variable which scroll our background





class Fire(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.random_index = None
        self.image_pack = [pygame.transform.scale(pygame.image.load(f"images/fire/{i}.png"), (width, height // 8)) for
                           i in range(6)]
        self.image = pygame.transform.scale(pygame.image.load(f"images/fire/{0}.png"), (width, height // 8))

        self.rect = self.image.get_rect(bottomleft=(0, height))
        self.rect.width = width
        self.rect.height = height // 8
        self.mask = pygame.mask.from_surface(self.image)

    def animateFire(self, height):
        self.random_index = randint(0, 5)
        self.image = self.image_pack[self.random_index]
        self.rect = self.image.get_rect(bottomleft=(0, height))


class StaticObjects:
    width = 700
    height = 800

    WHITE = (255, 255, 255)
    pixel_small = pygame.font.Font('fonts/pixel.ttf', width // 45)
    pixel_medium = pygame.font.Font('fonts/pixel.ttf', width // 20)
    pixel_big = pygame.font.Font('fonts/pixel.ttf', width // 15)
    metal_big = pygame.font.Font('fonts/Faceless.ttf', width // 8)


class RestartBoard(StaticObjects):
    text_died = StaticObjects.metal_big.render("YOU DIED", False, (255, 0, 0))
    text_press = StaticObjects.pixel_small.render("press space to restart", False, (200, 200, 200))
    image_bear_fired = pygame.transform.scale(pygame.image.load("images/scoreboard/fire/0.png"),
                                              (StaticObjects.width // 2, StaticObjects.height // 2))
    image_bear_trapped = pygame.transform.scale(pygame.image.load("images/scoreboard/trap/0.png"),
                                              (StaticObjects.width, StaticObjects.height))

class StartMenu(StaticObjects):
    start_text = [StaticObjects.pixel_big.render("Welcome", False, StaticObjects.WHITE),
                  StaticObjects.pixel_big.render("to the real World!", False, StaticObjects.WHITE)]


class Button:
    def __init__(self, y, width, height, name, size):
        self.image = pygame.transform.scale(pygame.image.load(f"images/buttons/{name}"),
                                            (width // size, height // size // 2.5))

        self.rect = self.image.get_rect(center=(0, y))

        self.rect.x = width // 2 - self.image.get_width() // 2

    def draws(self, *args, res=False):
        # draw button

        from main import screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # get mouse position on the screen

        pos = pygame.mouse.get_pos()

        action = False
        # check if mouse is over the button and click it
        if self.rect.collidepoint(pos):
            self.rect.width = args[0] // 4
            self.rect.height = args[1] // 10
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        # if player press space we also will restart game
        if res:
            if pygame.KEYDOWN and args[2][pygame.K_SPACE]:
                action = True

        return action
