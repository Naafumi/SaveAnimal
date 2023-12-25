from random import randint
import pygame
from Objects import Enemy


def createEnemy(static_group, static_surfaces, animate_group, animate_surfaces, static_kill_group, width):
    stat_or_anim = randint(0, 4)
    if stat_or_anim == 0 or stat_or_anim == 1 or stat_or_anim == 2:
        kill = randint(0, 2)
        if kill == 0:
            random_index = randint(0, len(static_surfaces['kill']) - 1)
            random_x = randint(20, width - 20)
            name = 'kill'
            return Enemy.staticKillerEnemy(random_x, static_surfaces[name][random_index], static_kill_group)
        if kill == 1 or kill == 2:
            random_index = randint(0, len(static_surfaces['freeze']) - 1)

            random_x = randint(20, width - 20)
            name = 'freeze'
            return Enemy.staticEnemy(random_x, static_surfaces[name][random_index], static_group)

    if stat_or_anim == 3 or stat_or_anim == 4:
        random_x = randint(20, width - 20)

        return Enemy.animaticEnemy(random_x, animate_surfaces, animate_group)





def collideRectEnemy(player, enemies_gr):
    if pygame.sprite.spritecollide(player, enemies_gr, False, pygame.sprite.collide_mask):

        return True
    else:
        return False

sound_burned = pygame.mixer.Sound(f'sounds/burned.wav')
def collideRectFire(player, fire_gr):
    if pygame.sprite.spritecollide(player, fire_gr, False, pygame.sprite.collide_mask):
        sound_burned.play()
        return False, True
    else:
        return True, False
