import random

import pygame
from Objects import Player, Background, Button
from Scripts import createEnemy, collideRect

pygame.init()

game_active = True
score_board = False

# size of our screen
WIDTH = 700
HEIGHT = 800

SCREEN_SIZE = (WIDTH, HEIGHT)

# constant variables
COLOR = (0, 140, 120)
WHITE = (255, 255, 255)
BLUE = (0, 50, 255)

# fonts

font_score = pygame.font.Font('fonts/pixel.ttf', WIDTH // 20)

screen = pygame.display.set_mode(SCREEN_SIZE)  # provide size of screen
pygame.display.set_caption("Save Animal")  # Game's name
pygame.display.set_icon(
    pygame.transform.rotate(pygame.image.load("images/bear.png").convert(), 180))  # our logo of game

clock = pygame.time.Clock()
FPS = 60
# speed of game
begin_game_speed = 3
game_speed = 3
speed_create = 3000

score = 0

# create enemies and group for function which generate them in game
enemies_images = ['1.png', '2.png', '3.png']

enemies_surfaces = [pygame.image.load('images/enemies/' + path).convert_alpha() for path in enemies_images]

enemies_gr = pygame.sprite.Group()

# EVENTS
CREATE_ENEMY = pygame.USEREVENT
pygame.time.set_timer(CREATE_ENEMY, speed_create)

CHANGE_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_SPEED, 4000)

bg = Background(WIDTH, HEIGHT)

but_restart = Button((HEIGHT // 2 - HEIGHT//10), WIDTH, HEIGHT, "restart.png")
but_quit = Button((but_restart.rect.height + HEIGHT // 2), WIDTH, HEIGHT, "exit.png")


player = Player(WIDTH, HEIGHT)

player_group = pygame.sprite.Group()
player_group.add(player)


def display_score():
    global score
    score += game_speed // 3

    text_score = font_score.render(f"score: {score}", False, WHITE)
    return text_score


def reset_game():
    #clear enemies
    enemies_gr.empty()

    #reset score
    global score
    score = 0

    #change speed and position to initial
    global game_speed
    game_speed = begin_game_speed
    global player
    player.rect.x = player.rect_begin

    #activate game and close scoreboard
    global game_active
    game_active = True
    global score_board
    score_board = False


if __name__ == "__main__":
    while True:
        # code read pressed keys from keyboard

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if score_board:

                screen.fill((90, 130, 255))
                global actual_score
                screen.blit(actual_score, (WIDTH // 2 - actual_score.get_width() // 2, HEIGHT // 15))

                if but_restart.draws():
                    reset_game()
                if but_quit.draws():
                    pygame.quit()
                    exit()



                pygame.display.update()

            if game_active:

                # here we check all our events and if we have some event we do it

                if event.type == CREATE_ENEMY:
                    createEnemy(enemies_gr, enemies_images, enemies_surfaces, WIDTH)
                    print(speed_create)
                if event.type == CHANGE_SPEED:
                    game_speed += 1

                    speed_create = 1500//(game_speed//begin_game_speed)
                    pygame.time.set_timer(CREATE_ENEMY, speed_create)

        if game_active:

            game_active, score_board = collideRect(player, enemies_gr)
            if not game_active:
                continue
            

            # checks keys of movement
            if pygame.KEYDOWN:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    if player.rect.x > 0:
                        player.rect.x -= game_speed
                    else:
                        player.rect.x = 0
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    if player.rect.x < WIDTH - player.rect.width:
                        player.rect.x += game_speed
                    else:
                        player.rect.x = WIDTH - player.rect.width

            # here we display our background and change his coordinate and after we display this backgtround again. This imitates background scrolling
            for i in range(0, bg.tiles):
                screen.blit(bg.list_bg[i], (0,
                                            -i * HEIGHT + bg.scroll)) if -i * HEIGHT + bg.scroll < HEIGHT else None  # there program use list of images(background) and scroll them

            bg.scroll += game_speed
            if bg.scroll > HEIGHT:
                bg.scroll = 0

            enemies_gr.draw(screen)  # here code displays our enemies
            enemies_gr.update(HEIGHT, game_speed)  # here program moves them

            actual_score = display_score()
            screen.blit(actual_score, (WIDTH // 35, 0))

            player_group.draw(screen)

            pygame.display.update()
            # how often we restart our cycle / we restart our code 60 times at 1 sec

        clock.tick(FPS)
