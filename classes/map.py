import pygame
import pytmx
import random

from classes.cam import Cam
from classes.tile import Tile
from classes.item import Item, Coin, Weapon
from classes.player import Player
from classes.music import Music


class Map(object):
    def __init__(self, map_file):
        self.music = Music()

        self.map_file = pytmx.load_pygame(map_file)

        # IDEA: is needed. Player here or in main class?
        self.player = Player()

        self.background_tiles = pygame.sprite.Group()
        self.collision_tiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.items.add(Item(3, 32, 32))
        self.items.add(Item(1, 300, 320))
        self.items.add(Item(0, 64, 64))
        self.items.add(Item(0, 400, 400))

        # Load tiles
        for x, y, image in self.map_file.layers[0].tiles():
            self.background_tiles.add(Tile(x*self.map_file.tilewidth, y*self.map_file.tileheight, image))

        for x, y, image in self.map_file.layers[1].tiles():
            self.collision_tiles.add(Tile(x*self.map_file.tilewidth, y*self.map_file.tileheight, image))

    def update(self):
        # Handle collision with items
        for item in self.items:
            if item.rect.colliderect(self.player.rect):
                if isinstance(item, Coin):
                    Music.coin_pick()

                    self.player.inventory.gold += item.value
                    self.items.remove(item)
                else:
                    if self.player.inventory.add(item):
                        Music.item_pick()
                        self.items.remove(item)



        # Handle collision with tiles before
        # TODO: Check if it really works, cuz I don't believe
        if self.player.vector["x"]:
            player_rect = self.player.rect.copy()
            player_rect.x += self.player.vector["x"]

            collision_flag = False

            for tile in self.collision_tiles:
                if player_rect.colliderect(tile.rect):
                    if self.player.vector["x"] > 0:
                        player_rect.right = tile.rect.left
                    else:
                        player_rect.left = tile.rect.right

                    collision_flag = True

            if collision_flag:
                Cam.x -= player_rect.x - self.player.rect.x
                self.player.x += player_rect.x - self.player.rect.x
            else:
                Cam.x -= self.player.vector["x"]
                self.player.x += self.player.vector["x"]

            self.player.vector["x"] = 0

        if self.player.vector["y"]:
            player_rect = self.player.rect.copy()
            player_rect.y += self.player.vector["y"]

            collision_flag = False

            for tile in self.collision_tiles:
                if player_rect.colliderect(tile.rect):
                    if self.player.vector["y"] > 0:
                        player_rect.bottom = tile.rect.top
                    else:
                        player_rect.top = tile.rect.bottom

                    collision_flag = True

            if collision_flag:
                Cam.y -= player_rect.y - self.player.rect.y
                self.player.y += player_rect.y - self.player.rect.y
            else:
                Cam.y -= self.player.vector["y"]
                self.player.y += self.player.vector["y"]

            self.player.vector["y"] = 0

        self.player.update()
        self.player.inventory.update()
        self.background_tiles.update()
        self.collision_tiles.update()
        self.items.update()
