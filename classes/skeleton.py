import pygame
from classes.spritesheet import SpriteSheet

class Skeleton(pygame.sprite.Sprite):

    def __init__(self, x, y, window_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = SpriteSheet("media/skeleton.png").get_sprite(16, 0, 16, 16)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y

        self.window_size = window_size

        self.direction = 1

    def update(self, player_pos):
        self.x += 1

        self.rect.x = self.x-player_pos[0]+(self.window_size[0]/2)
        self.rect.y = self.y-player_pos[1]+(self.window_size[1]/2)
