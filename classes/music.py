import pygame
import random


class Music(object):
    def __init__(self):
        pygame.mixer.music.load("media/sounds/No More Magic.mp3")
        pygame.mixer.music.play(-1)

    @staticmethod
    def item_pick():
        pygame.mixer.Sound(
            file="media/sounds/RPG Sound Pack/inventory/cloth" + str(random.randint(1, 2)) + ".wav").play()

    @staticmethod
    def coin_pick():
        pygame.mixer.Sound(
            file="media/sounds/RPG Sound Pack/inventory/coin" + str(random.randint(1, 3)) + ".wav").play()

    @staticmethod
    def player_attack():
        pygame.mixer.Sound(
            file="media/sounds/RPG Sound Pack/battle/swing" + str(random.randint(1, 3)) + ".wav").play()