import random

from math import ceil
import pygame
from Objects import Enemy


pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)

#size of our screen
WIDTH = 700
HEIGHT = 500
SCREEN_SIZE = (WIDTH, HEIGHT)

#constant variables
COLOR = (0, 140, 120)
WHITE = (255, 255, 255)
BLUE = (0, 50, 255)

screen = pygame.display.set_mode(SCREEN_SIZE) #provide size of screen
pygame.display.set_caption("Save Animal") #Game's name
pygame.display.set_icon(pygame.image.load("F:\Фотошоп\photoshop\фото для фш\cEdDG.png"))#our logo of game

clock = pygame.time.Clock()
FPS = 60
spd=3 # speed of game

#create enemies and group for function which generate them in game
enemies_images = ['1.png', '2.png']

enemies_surfaces = [pygame.image.load('images/enemies/' + path).convert_alpha() for path in enemies_images]
enemies_gr = pygame.sprite.Group()

class Background():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("images/bg1.png").convert(), (WIDTH, HEIGHT))
        self.tiles = ceil(HEIGHT/self.image.get_height())+1 #tiles make endless background scrolling ,
        self.list_bg = [self.image for x in range(self.tiles)]
        self.scroll = 0 #variable which scroll our background
bg = Background()


class Player():
    def __init__(self):
        # self.image = pygame.surface.Surface((75, 75))

        self.image = pygame.transform.scale(pygame.image.load("images/bear3.png").convert_alpha(), (50, 75))

        self.rect = self.image.get_rect(centerx=WIDTH//2, bottom=HEIGHT-self.image.get_height()*2)
player = Player()



def createEnemy(group):
    random_indx = random.randint(0, len(enemies_images) - 1)
    random_x = random.randint(20, WIDTH-20)
    return Enemy(random_x, enemies_surfaces[random_indx], spd, group)


def colideRect():
    for enemy in enemies_gr:

        if enemy.rect.colliderect(player.rect):

            enemy.kill()



while True:

    #here we check all our events and if we have some event we do it
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            createEnemy(enemies_gr)

    colideRect()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if player.rect.x > 0:
            player.rect.x -= spd

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if player.rect.x < WIDTH-player.rect.width:
            player.rect.x += spd


    #here we display our background and change his coordinate and after we display this backgtround again. This imitates background scrolling
    for i in range(0, bg.tiles):
        screen.blit(bg.list_bg[i], (0, -i*HEIGHT+bg.scroll)) if -i*HEIGHT+bg.scroll < HEIGHT else None  #there program use list of images(background) and scroll them

    bg.scroll += spd
    if bg.scroll > HEIGHT:
        bg.scroll = 0










    enemies_gr.draw(screen) #here code displays our enemies
    enemies_gr.update(HEIGHT, spd) #here program moves them
    screen.blit(player.image, player.rect)

    pygame.display.update()
    clock.tick(FPS) #how often we restart our cycle / we restart our code 60 times at 1 sec





