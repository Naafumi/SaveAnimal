from Objects import Enemy
import random
import pygame


def createEnemy(group, enemies_images, enemies_surfaces, width):
    random_index = random.randint(0, len(enemies_images) - 1)
    random_x = random.randint(20, width - 20)
    return Enemy(random_x, enemies_surfaces[random_index], group)


def collideRect(player, enemies_gr):
    from main import game_active, score_board
    if pygame.sprite.spritecollide(player, enemies_gr, False, pygame.sprite.collide_mask):
        return False, True
    else:
        return True, False


