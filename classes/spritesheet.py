import pygame

#IDEA: There is possibility to make a better/more useful class than this

class SpriteSheet(object):

    def __init__(self, file_name):
        self.spritesheet = pygame.image.load(file_name).convert_alpha()

    def get_sprite(self, x, y, width, height):
        image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))

        return image
