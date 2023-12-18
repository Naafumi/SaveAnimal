from Objects import Enemy
from random import randint
import pygame


def createEnemy(static_group, static_surfaces, animate_group, animate_surfaces, width):
    stat_or_anim = randint(0, 1)
    if stat_or_anim == 0:
        random_index = randint(0, len(static_surfaces) - 1)
        random_x = randint(20, width - 20)

        return Enemy.staticEnemy(random_x, static_surfaces[random_index], static_group)
    if stat_or_anim == 1:

        random_x = randint(20, width - 20)

        return Enemy.animaticEnemy(random_x, animate_surfaces, animate_group)



def collideRectEnemy(player, enemies_gr):
    if pygame.sprite.spritecollide(player, enemies_gr, False, pygame.sprite.collide_mask):
        return True
    else:
        return False


def collideRectFire(player, fire_gr):
    if pygame.sprite.spritecollide(player, fire_gr, False, pygame.sprite.collide_mask):
        return False, True
    else:
        return True, False
