import pygame

from classes.cam import Cam


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x + Cam.x
        self.rect.y = self.y + Cam.y
