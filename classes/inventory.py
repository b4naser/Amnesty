import pygame

from classes.item import Coin, Weapon

# Collide itd są beznadziejne, można ogólnie sprawdzaćc zy myszka jest na przedmiocie i zależnie regulować akcje, bo itemek może kontrolować w jakim sprite groupie się znajduje

# TODO: It should inherit from pygame.sprite.Group
class Inventory(object):

    def __init__(self):
        self.max_amount = 20
        self._inventory = pygame.sprite.Group()
        self._equipped = pygame.sprite.Group()

        self.gold = 0

    def update(self):
        # Calculate positions for items in inventory
        row = 0
        column = 0
        for item in self._inventory:
            item.rect.x = 12 + column*32 + column*16
            item.rect.y = 400 + row*32

            column += 1

            if column > 3:
                column = 0
                row += 1

        # Assign positions for equipped items
        for item in self._equipped:
            if isinstance(item, Weapon):
                item.rect.x = 44
                item.rect.y = 284

    def draw(self, surface):
        self._inventory.draw(surface)
        self._equipped.draw(surface)

    def equip(self, item):
        self._equipped.add(item)
        self._inventory.remove(item)

    def unequip(self, item):
        self._inventory.add(item)
        self._equipped.remove(item)

    def add(self, item):
        if len(self._inventory) > self.max_amount-1:
            return False
        else:
            self._inventory.add(item)
            return True

    def collide_inventory(self, point):
        for item in self._inventory:
            # TODO: Item rect is relative to position in inventory surface, not whole screen
            absolute_rect = item.rect.copy()
            absolute_rect.x += 800

            if absolute_rect.collidepoint(point):
                return item

    def collide_equipped(self, point):
        for item in self._equipped:
            # TODO: Item rect is relative to position in inventory surface, not whole screen
            absolute_rect = item.rect.copy()
            absolute_rect.x += 800

            if absolute_rect.collidepoint(point):
                return item

    def get_equipped_weapon(self):
        for item in self._equipped:
            if isinstance(item, Weapon):
                return item

        return False