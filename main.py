
import pygame


from Objects import Player, Background, Button, Fire,  RestartBoard, StartMenu, Text
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



score_board_image = pygame.transform.scale(pygame.image.load("images/scoreboard/bearfired.png"),
                                           (WIDTH // 2, HEIGHT // 2))


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
    # 'oil': [f"{index}.png" for index in [1, 2, 3, 4]],
    # 'cars': [f"{index}.png" for index in [1, 2, 3, 4]],
    # 'trash': [f"{index}.png" for index in [1, 2, 3, 4]],
    # 'log': [f"{index}.png" for index in [1, 2, 3, 4]],
    'fire': [f"{index}.png" for index in [1, 2, 3, 4]],
    'trap': [f"{index}.png" for index in [1]]}

static_enemies_surfaces = []
animatic_enemies_surfaces = []
fire_surfaces = []

fire: Fire = Fire(WIDTH, HEIGHT)
fire_group = pygame.sprite.Group()
fire_group.add(fire)

if __name__ == "__main__":

#create surfaces from our images
    for path in enemies_images:
        if path == 'oil':
            for index in enemies_images[path]:
                static_enemies_surfaces.append(
                    pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                           (WIDTH // 9, HEIGHT // 13)))


        if path == 'cars':
            for index in enemies_images[path]:
                if index == '3.png' or index == '4.png':
                    static_enemies_surfaces.append(
                        pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                               (WIDTH // 10, HEIGHT // 5)))
                else:
                    static_enemies_surfaces.append(
                        pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                               (WIDTH // 4, HEIGHT // 9)))
        if path == 'fire':
            for index in enemies_images[path]:
                animatic_enemies_surfaces.append(
                    pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                           (WIDTH // 16, HEIGHT // 14)))
        if path == 'trash':
            for index in enemies_images[path]:
                if index == '1.png':
                    static_enemies_surfaces.append(pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(), (WIDTH // 8, HEIGHT // 12)))
                if index == '2.png':
                    static_enemies_surfaces.append(pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(), (WIDTH // 7, HEIGHT // 12)))
                if index == '3.png':
                    static_enemies_surfaces.append(pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(), (WIDTH // 6, HEIGHT // 7)))
                if index == '4.png':
                    static_enemies_surfaces.append(pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(), (WIDTH // 8, HEIGHT // 10)))

        if path == 'log':
            for index in enemies_images[path]:
                if index == '1.png' or index == '4.png':
                    static_enemies_surfaces.append(
                        pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                               (WIDTH // 6, HEIGHT // 8)))
                if index == '2.png' or index == '3.png' :
                    static_enemies_surfaces.append(
                        pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                               (WIDTH // 7, HEIGHT // 14)))

        if path == 'trap':
            for index in enemies_images[path]:
                if index == '1.png':
                    static_enemies_surfaces.append(pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(), (WIDTH // 8, HEIGHT // 12)))
                if index == '2.png':
                    static_enemies_surfaces.append(pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(), (WIDTH // 7, HEIGHT // 12)))
                if index == '3.png':
                    static_enemies_surfaces.append(pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(), (WIDTH // 6, HEIGHT // 7)))
                if index == '4.png':
                    static_enemies_surfaces.append(pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(), (WIDTH // 8, HEIGHT // 10)))



static_enemies_group = pygame.sprite.Group()
animatic_enemies_group = pygame.sprite.Group()

# EVENTS
CREATE_ENEMY = pygame.USEREVENT
pygame.time.set_timer(CREATE_ENEMY, speed_create)

CHANGE_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_SPEED, 4000)

ANIMATE_PLAYER = pygame.USEREVENT + 2
pygame.time.set_timer(ANIMATE_PLAYER, game_speed * 100)

ANIMATE_FIRE = pygame.USEREVENT + 3
pygame.time.set_timer(ANIMATE_FIRE, 150)

ANIMATE_ENEMIES = pygame.USEREVENT + 4
pygame.time.set_timer(ANIMATE_ENEMIES, 250)


bg = Background(WIDTH, HEIGHT)

but_restart = Button((HEIGHT // 2.5 - HEIGHT // 8), WIDTH, HEIGHT, "restart.png", 5)
but_quit = Button((HEIGHT // 2.5), WIDTH, HEIGHT, "exit.png", 5)
but_play = Button(HEIGHT // 2, WIDTH, HEIGHT, "play.png", 4)


# here code take actual score and then convert int to pygame text
def display_score():
    global score
    score += game_speed // 3

    text_score = Text.pixel_medium.render(f"score: {score}", False, WHITE)
    return text_score


def reset_game():
    # clear enemies
    static_enemies_group.empty()
    animatic_enemies_group.empty()

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

            #START MENU
            if start_game:
                start_img = pygame.transform.scale(pygame.image.load("images/start menu/2.png"), (WIDTH,  HEIGHT))
                screen.blit(start_img, (0, 0))


                screen.blit(StartMenu.start_text[0], (WIDTH // 2 - StartMenu.start_text[0].get_width() // 2, HEIGHT // 8))
                screen.blit(StartMenu.start_text[1], (WIDTH // 2 - StartMenu.start_text[1].get_width() // 2, HEIGHT // 8 + StartMenu.start_text[1].get_height()))
                screen.blit(RestartBoard.text_press, (WIDTH // 2 - RestartBoard.text_press.get_width() // 2, HEIGHT // 2 - HEIGHT // 10))
                if but_play.draws(WIDTH, HEIGHT, keys, res=True):
                    reset_game()

                pygame.display.update()
            #SCOREBOARD
            if score_board:
                # if our game is paused code activate end background
                screen.fill((100, 31, 21))

                global actual_score

                screen.blit(RestartBoard.text_died, (WIDTH // 2 - RestartBoard.text_died.get_width() // 2, HEIGHT // 15))
                screen.blit(actual_score, (WIDTH // 2 - actual_score.get_width() // 2, HEIGHT // 12))
                screen.blit(score_board_image, (WIDTH//2-score_board_image.get_width()//2, HEIGHT//2))
                screen.blit(RestartBoard.text_press, (WIDTH // 2 - RestartBoard.text_press.get_width() // 2, HEIGHT-HEIGHT//30))

                # draw buttons and check whether are pressed
                if but_restart.draws(WIDTH, HEIGHT, keys, res=True):
                    reset_game()
                if but_quit.draws(WIDTH, HEIGHT):
                    pygame.quit()
                    exit()
                pygame.display.update()

            #GAME IS BEING PLAYED
            if game_active:

                # here we check all our events and if we have some event we do it

                if event.type == CREATE_ENEMY:
                    createEnemy(static_enemies_group, static_enemies_surfaces, animatic_enemies_group, animatic_enemies_surfaces, WIDTH)

                if event.type == CHANGE_SPEED:
                    game_speed += 1

                    speed_create = 1500 // (game_speed // begin_game_speed)
                    pygame.time.set_timer(CREATE_ENEMY, speed_create)
                if event.type == ANIMATE_PLAYER and playerNotHit:
                    player.animatePlayer()

                if event.type == ANIMATE_FIRE:
                    fire.animateFire(HEIGHT)

                if event.type == ANIMATE_ENEMIES:
                    animatic_enemies_group.update(HEIGHT, game_speed, x=1)  # here program moves them






        if game_active:
            actual_score = display_score()
            if collideRectEnemy(player, static_enemies_group):
                playerNotHit = False
                player.update(HEIGHT, game_speed)

            game_active, score_board = collideRectFire(player, fire_group)

            if collideRectEnemy(player, animatic_enemies_group):
                game_active, score_board = collideRectFire(player, animatic_enemies_group)




            # if game is over code draw background for fast loading score board and passes the rest of game code
            if not game_active:
                screen.fill((100, 31, 21))



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

            static_enemies_group.draw(screen)  # here code displays our enemies
            static_enemies_group.update(HEIGHT, game_speed)  # here program moves them

            animatic_enemies_group.draw(screen)  # here code displays our enemies
            animatic_enemies_group.update(HEIGHT, game_speed)  # here program moves them

            screen.blit(actual_score, (WIDTH // 35, 0))

            player_group.draw(screen)

            fire_group.draw(screen)

            pygame.display.update()
            # how often we restart our cycle / we restart our code 60 times at 1 sec

        clock.tick(FPS)
