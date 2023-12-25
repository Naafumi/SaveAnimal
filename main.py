
import pygame

from random import randint
from Objects import Player, Background, Button, Fire,  RestartBoard, StartMenu, StaticObjects
from Scripts import createEnemy, collideRectEnemy, collideRectFire


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

game_active = False
score_board = False
playerNotHit = True
start_game = True
checkCollide = True


# size of our screen

WIDTH = 700
HEIGHT = 800



# constant variables
COLOR = (0, 140, 120)
WHITE = (255, 255, 255)
BLUE = (0, 50, 255)

back = 'fire'



screen = pygame.display.set_mode((WIDTH, HEIGHT))  # provide size of screen
pygame.display.set_caption("Save Him@")  # Game's name
pygame.display.set_icon(pygame.image.load("images/bear.png").convert())  # our logo of game

clock = pygame.time.Clock()
FPS = 60
# values of score, player speed, speed of create enemies
begin_game_speed = 3
game_speed = 3
speed_create_begin = 3000
speed_create = 3000
score = 0

#load sounds
sound_hits = [pygame.mixer.Sound(f'sounds/hits/{i}.wav') for i in range(6)]
sound_trap = [pygame.mixer.Sound(f'sounds/trap/{i}.wav') for i in range(5)]
sound_bears = [pygame.mixer.Sound(f'sounds/bear/{i}.wav') for i in range(3)]
pygame.mixer.music.load('sounds/soundtrackfinal.wav')





player = Player(WIDTH, HEIGHT)
player_group = pygame.sprite.Group()
player_group.add(player)

bg = Background(WIDTH, HEIGHT)


static_enemies_surfaces = {
    'freeze': [],
    'kill': []
}
animatic_enemies_surfaces = []

static_enemies_group = pygame.sprite.Group()
static_enemies_group_k = pygame.sprite.Group()
animatic_enemies_group = pygame.sprite.Group()



fire_surfaces = []
fire: Fire = Fire(WIDTH, HEIGHT)
fire_group = pygame.sprite.Group()
fire_group.add(fire)


# create enemies and group for function which generate them in game
enemies_images = {
    'oil': [f"{index}.png" for index in range(4)],
    'cars': [f"{index}.png" for index in range(4)],
    'trash': [f"{index}.png" for index in range(4)],
    'log': [f"{index}.png" for index in range(4)],
    'fire': [f"{index}.png" for index in range(4)],
    'trap': [f"{index}.png" for index in range(4)],
    'tire': [f"{index}.png" for index in range(2)]
}




if __name__ == "__main__":
    #create surfaces from our images
    for path in enemies_images:
        if path == 'oil':
            for index in enemies_images[path]:
                static_enemies_surfaces['freeze'].append(
                    pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                               (WIDTH // 9, HEIGHT // 13)))


        if path == 'cars':
            for index in enemies_images[path]:
                size = [(WIDTH // 4, HEIGHT // 9), (WIDTH // 4, HEIGHT // 9), (WIDTH // 10, HEIGHT // 5), (WIDTH // 10, HEIGHT // 5) ]
                for i in range(4):
                    if index == f'{i}.png':
                        static_enemies_surfaces['freeze'].append(
                            pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                                       size[i]))
        if path == 'fire':
            for index in enemies_images[path]:
                animatic_enemies_surfaces.append(
                    pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                           (WIDTH // 16, HEIGHT // 14)))
        if path == 'trash':
            for index in enemies_images[path]:
                size = [(WIDTH // 8, HEIGHT // 12), (WIDTH // 7, HEIGHT // 12), (WIDTH // 6, HEIGHT // 7), (WIDTH // 8, HEIGHT // 10)]
                for i in range(4):
                    if index == f'{i}.png':
                        static_enemies_surfaces['freeze'].append(
                            pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                                   size[i]))

        if path == 'log':
            for index in enemies_images[path]:
                size = [(WIDTH // 6, HEIGHT // 8), (WIDTH // 7, HEIGHT // 14), (WIDTH // 7, HEIGHT // 14), (WIDTH // 6, HEIGHT // 8)]
                for i in range(4):
                    if index == f'{i}.png':
                        static_enemies_surfaces['freeze'].append(
                            pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                                   size[i]))

        if path == 'trap':

            for index in enemies_images[path]:
                size = [(WIDTH // 8, HEIGHT // 12), (WIDTH // 7, HEIGHT // 12), (WIDTH // 9, HEIGHT // 12), (WIDTH // 8, HEIGHT // 10)]
                for i in range(4):
                    if index == f'{i}.png':
                        static_enemies_surfaces['kill'].append(
                            pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                                   size[i]))


        if path == 'tire':
            for index in enemies_images[path]:
                size = [(WIDTH // 10, HEIGHT // 18), (WIDTH // 12, HEIGHT // 18)]
                for i in range(2):

                    if index == f'{i}.png':

                        static_enemies_surfaces['freeze'].append(
                            pygame.transform.scale(pygame.image.load(f'images/enemies/{path}/{index}').convert_alpha(),
                                                   size[i]))


# EVENTS
CREATE_ENEMY = pygame.USEREVENT
pygame.time.set_timer(CREATE_ENEMY, speed_create)

CHANGE_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_SPEED, 4000)

ANIMATE_PLAYER = pygame.USEREVENT + 2
pygame.time.set_timer(ANIMATE_PLAYER, (200 // (game_speed // begin_game_speed)) if playerNotHit else 50)

ANIMATE_FIRE = pygame.USEREVENT + 3
pygame.time.set_timer(ANIMATE_FIRE, 150)

ANIMATE_ENEMIES = pygame.USEREVENT + 4
pygame.time.set_timer(ANIMATE_ENEMIES, 250)

SOUND_BEAR = pygame.USEREVENT + 5
pygame.time.set_timer(SOUND_BEAR, 10000)



but_restart = Button((HEIGHT // 2.5 - HEIGHT // 8), WIDTH, HEIGHT, "restart.png", 5)
but_quit = Button((HEIGHT // 2.5), WIDTH, HEIGHT, "exit.png", 5)
but_play = Button(HEIGHT // 2, WIDTH, HEIGHT, "play.png", 4)


# here code take actual score and then convert int to pygame text
def display_score():
    global score
    score += game_speed // 3

    text_score = StaticObjects.pixel_medium.render(f"score: {score}", False, WHITE)
    return text_score


def reset_game():
    # clear enemies
    static_enemies_group.empty()
    static_enemies_group_k.empty()
    animatic_enemies_group.empty()

    # reset score
    global score
    score = 0

    # unblock player movement
    global playerNotHit
    playerNotHit = True

    global checkCollide
    checkCollide = True

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

    pygame.mixer.music.play(-1, 0, 5000)




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
                start_img = pygame.transform.scale(pygame.image.load("images/scoreboard/start.png"), (WIDTH,  HEIGHT))
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
                if back == 'fire':
                    screen.blit(RestartBoard.image_bear_fired, (WIDTH//2-RestartBoard.image_bear_fired.get_width()//2, HEIGHT//2))
                if back == 'trap':
                    screen.blit(RestartBoard.image_bear_trapped, (0, 0))
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
                    createEnemy(static_enemies_group, static_enemies_surfaces, animatic_enemies_group, animatic_enemies_surfaces, static_enemies_group_k, WIDTH)

                if event.type == CHANGE_SPEED:
                    game_speed += 1

                    speed_create = 1500 // (game_speed // begin_game_speed)
                    pygame.time.set_timer(CREATE_ENEMY, speed_create)
                if event.type == ANIMATE_PLAYER:
                    player.animatePlayer(playerNotHit)
                    pygame.time.set_timer(ANIMATE_PLAYER, (200 // (game_speed // begin_game_speed)) if playerNotHit else 50)
                if event.type == ANIMATE_FIRE:
                    fire.animateFire(HEIGHT)

                if event.type == ANIMATE_ENEMIES:
                    animatic_enemies_group.update(HEIGHT, game_speed, x=1)  # here program moves them

                if event.type == SOUND_BEAR:
                    rand_sx = randint(0, 2)
                    rand_t = randint(10000, 17000)
                    sound_bears[rand_sx].play()
                    pygame.time.set_timer(SOUND_BEAR, rand_t)




        if game_active:
            actual_score = display_score()


            if collideRectEnemy(player, static_enemies_group) and checkCollide:

                playerNotHit = False
                checkCollide = False
                rand_x = randint(0, 5)
                sound_hits[rand_x].play()

            if not playerNotHit:
                player.update(HEIGHT, game_speed)

                game_active, score_board = collideRectFire(player, fire_group)


            if collideRectEnemy(player, static_enemies_group_k):
                game_active, score_board = collideRectFire(player, static_enemies_group_k)
                rand_x = randint(0, 4)
                sound_trap[rand_x].play()
                back = 'trap'
            if collideRectEnemy(player, animatic_enemies_group):
                game_active, score_board = collideRectFire(player, animatic_enemies_group)

                back = 'fire'



            # if game is over code draw background for fast loading score board and passes the rest of game code
            if not game_active:
                screen.fill((100, 31, 21))

                pygame.mixer.music.stop()


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
            for i in range(0, bg.tiles):
                screen.blit(bg.list_bg[i], (0,
                                            -i * HEIGHT + bg.scroll)) if -i * HEIGHT + bg.scroll < HEIGHT else None  # there program use list of images(background) and scroll them

            bg.scroll += game_speed
            if bg.scroll > HEIGHT:
                bg.scroll = 0

            static_enemies_group.draw(screen)  # here code displays our enemies
            static_enemies_group.update(HEIGHT, game_speed)  # here program moves them

            static_enemies_group_k.draw(screen)  # here code displays our enemies
            static_enemies_group_k.update(HEIGHT, game_speed)  # here program moves them

            animatic_enemies_group.draw(screen)  # here code displays our enemies
            animatic_enemies_group.update(HEIGHT, game_speed)  # here program moves them

            screen.blit(actual_score, (WIDTH // 35, 0))

            player_group.draw(screen)

            fire_group.draw(screen)



            pygame.display.update()
            # how often we restart our cycle / we restart our code 60 times at 1 sec

        clock.tick(FPS)
