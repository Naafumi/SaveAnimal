from Objects import Enemy
from random import randint
import pygame


def createEnemy(group, enemies_surfaces, fire_surfaces, width):
    fireNot = randint(0, 1)

    random_index = randint(0, len(enemies_surfaces) - 1 )
    random_x = randint(20, width - 20)

    return Enemy(random_x, enemies_surfaces[random_index], group, fire_surfaces, fireNot)


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
