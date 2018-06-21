# IDEA: The idea is needed how deal with items
import pygame
import json

from classes.cam import Cam
from classes.spritesheet import SpriteSheet
#from classes.tooltip import Tooltip

ITEMS_IMAGES_DIR = "media/items/"

class Item(object):
    def __new__(cls, *args, **kwargs):
        with open("items.json") as json_data:
            items_data = json.load(json_data)

            for item in items_data["items"]:
                if item["id"] == args[0]:
                    if item["type"] == "coin":
                        return Coin(
                            args[1],
                            args[2],
                            SpriteSheet(ITEMS_IMAGES_DIR + item["image"]["file"]).get_sprite(item["image"]["x"],
                                                                                             item["image"]["y"],
                                                                                             32,
                                                                                             32),
                            item
                        )
                    elif item["type"] == "weapon":
                        return Weapon(
                            args[1],
                            args[2],
                            SpriteSheet(ITEMS_IMAGES_DIR + item["image"]["file"]).get_sprite(item["image"]["x"],
                                                                                             item["image"]["y"],
                                                                                             32,
                                                                                             32),
                            item
                        )


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image, item_info):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        self.desc = item_info["name"]
        self.value = item_info["value"]

        # For oscillation
        # FIXME: Should depend on time, not frame
        self.frame = 1
        self.osc = 0
        self.osc = 0
        self.dir = 1

    def update(self):
        if self.osc > 3:
            self.dir = -1
        elif self.osc < -3:
            self.dir = 1

        if self.frame % 4 == 0:
            self.osc += self.dir
            self.frame = 1

        self.frame += 1

        self.rect.x = self.x + Cam.x
        self.rect.y = self.y + Cam.y + self.osc


class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, image, item_info):
        pygame.sprite.Sprite.__init__(self)

        self.image_o = image
        self.image = self.image_o

        self.rect = self.image_o.get_rect()

        self.x = x
        self.y = y

        self.name = item_info["name"]
        self.desc = item_info["desc"]
        self.value = item_info["value"]

        # For oscillation
        # FIXME: Should depend on time, not frame
        self.frame = 1
        self.osc = 0
        self.dir = 1

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            event = pygame.event.Event(pygame.USEREVENT, msg=self.name)
            pygame.event.post(event)

        if self.osc > 3:
            self.dir = -1
        elif self.osc < -3:
            self.dir = 1

        if self.frame % 4 == 0:
            self.osc += self.dir
            self.frame = 1

        self.frame += 1

        self.rect.x = self.x + Cam.x
        self.rect.y = self.y + Cam.y + self.osc


class Ring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.value = None
        self.type = "ring"

        self.image = SpriteSheet("media/items/items.png").get_sprite(320, 320, 32, 32)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        # For oscillation
        # FIXME: Should depend on time, not frame
        self.frame = 1
        self.osc = 0
        self.dir = 1

    def update(self):
        if self.osc > 3:
            self.dir = -1
        elif self.osc < -3:
            self.dir = 1

        if self.frame % 4 == 0:
            self.osc += self.dir
            self.frame = 1

        self.frame += 1

        self.rect.x = self.x + Cam.x
        self.rect.y = self.y + Cam.y + self.osc
