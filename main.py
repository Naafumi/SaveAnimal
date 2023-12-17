import random

import pygame
from Objects import Player, Background, Button, Fire
from Scripts import createEnemy, collideRectEnemy, collideRectFire

pygame.init()

game_active = False
score_board = False
playerNotHit = True
start_game = True

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
# values of score, player speed, speed of create enemies
begin_game_speed = 3
game_speed = 3
speed_create_begin = 3000
speed_create = 3000
score = 0

player = Player(WIDTH, HEIGHT)
player_group = pygame.sprite.Group()
player_group.add(player)

# create enemies and group for function which generate them in game
enemies_images = {
    'oil': [f"{index}.png" for index in [1, 2, 3, 4]],
    'cars': [f"{index}.png" for index in [1, 2, 3, 4]]}
enemies_surfaces = []

fire = Fire(WIDTH, HEIGHT)
fire_group = pygame.sprite.Group()
fire_group.add(fire)

if __name__ == "__main__":
    for path in enemies_images:
        if path == 'oil':
            for index in enemies_images[path]:
                enemies_surfaces.append(
                    pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                           (WIDTH // 9, HEIGHT // 13)))

    for path in enemies_images:
        if path == 'cars':
            for index in enemies_images[path]:
                if index == '3.png' or index == '4.png':
                    enemies_surfaces.append(
                        pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                               (WIDTH // 10, HEIGHT // 5)))
                else:
                    enemies_surfaces.append(
                        pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                               (WIDTH // 4, HEIGHT // 9)))

enemies_gr = pygame.sprite.Group()

# EVENTS
CREATE_ENEMY = pygame.USEREVENT
pygame.time.set_timer(CREATE_ENEMY, speed_create)

CHANGE_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_SPEED, 4000)

ANIMATE_PLAYER = pygame.USEREVENT + 2
pygame.time.set_timer(ANIMATE_PLAYER, game_speed * 100)

ANIMATE_FIRE = pygame.USEREVENT + 3
pygame.time.set_timer(ANIMATE_FIRE, 250)

bg = Background(WIDTH, HEIGHT)

but_restart = Button((HEIGHT // 2 - HEIGHT // 10), WIDTH, HEIGHT, "restart.png", 5)
but_quit = Button((but_restart.rect.height + HEIGHT // 2), WIDTH, HEIGHT, "exit.png", 5)
but_play = Button(HEIGHT // 2, WIDTH, HEIGHT, "play.png", 4)


# here code take actual score and then convert int to pygame text
def display_score():
    global score
    score += game_speed // 3

    text_score = font_score.render(f"score: {score}", False, WHITE)
    return text_score


def reset_game():
    # clear enemies
    enemies_gr.empty()

    # reset score
    global score
    score = 0

    # unblock player movement
    global playerNotHit
    playerNotHit = True

    # change speed and position to initial
    global game_speed
    game_speed = begin_game_speed
    global player
    player.rect.x, player.rect.y = player.rect_begin
    global speed_create
    speed_create = speed_create_begin

    # activate game and close scoreboard
    global game_active
    game_active = True
    global score_board
    score_board = False
    global start_game
    start_game = False


if __name__ == "__main__":
    while True:
        # code read pressed keys from keyboard

        keys = pygame.key.get_pressed()

        # check quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if start_game:
                screen.fill((10, 200, 90))
                start_text = font_score.render("Welcome to the real World!", False, WHITE)
                screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 8))
                if but_play.draws(WIDTH, HEIGHT):
                    reset_game()
                pygame.display.update()

            if score_board:
                # if our game is paused code activate end background
                screen.fill((90, 130, 255))
                global actual_score
                screen.blit(actual_score, (WIDTH // 2 - actual_score.get_width() // 2, HEIGHT // 15))
                # draw buttons and check whether are pressed
                if but_restart.draws(WIDTH, HEIGHT):
                    reset_game()
                if but_quit.draws(WIDTH, HEIGHT):
                    pygame.quit()
                    exit()
                pygame.display.update()

            if game_active:

                # here we check all our events and if we have some event we do it

                if event.type == CREATE_ENEMY:
                    createEnemy(enemies_gr, enemies_images, enemies_surfaces, WIDTH)

                if event.type == CHANGE_SPEED:
                    game_speed += 1

                    speed_create = 1500 // (game_speed // begin_game_speed)
                    pygame.time.set_timer(CREATE_ENEMY, speed_create)
                if event.type == ANIMATE_PLAYER:
                    player.animatePlayer()

                if event.type == ANIMATE_FIRE:
                    fire.animateFire(HEIGHT)

        if game_active:
            actual_score = display_score()
            if collideRectEnemy(player, enemies_gr):
                playerNotHit = False
                player.update(HEIGHT, game_speed)

            game_active, score_board = collideRectFire(player, fire_group)

            # if game is over code draw background for fast loading score board and passes the rest of game code
            if not game_active:
                screen.fill((90, 130, 255))

                screen.blit(actual_score, (WIDTH // 2 - actual_score.get_width() // 2, HEIGHT // 15))

                if but_restart.draws(WIDTH, HEIGHT):
                    reset_game()
                if but_quit.draws(WIDTH, HEIGHT):
                    pygame.quit()
                    exit()
                pygame.display.update()
                continue

            # checks player movement
            if pygame.KEYDOWN and playerNotHit:
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

            # here we display our background and change his coordinate and after we display this background again. This imitates background scrolling
            for i in range(0, bg.tiles):
                screen.blit(bg.list_bg[i], (0,
                                            -i * HEIGHT + bg.scroll)) if -i * HEIGHT + bg.scroll < HEIGHT else None
                # there program use list of images(background) and scroll them

            bg.scroll += game_speed
            if bg.scroll > HEIGHT:
                bg.scroll = 0

            enemies_gr.draw(screen)  # here code displays our enemies
            enemies_gr.update(HEIGHT, game_speed)  # here program moves them

            screen.blit(actual_score, (WIDTH // 35, 0))

            player_group.draw(screen)

            fire_group.draw(screen)

            pygame.display.update()
            # how often we restart our cycle / we restart our code 60 times at 1 sec

        clock.tick(FPS)
