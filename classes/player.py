from classes.cam import Cam
from classes.spritesheet import SpriteSheet
from classes.inventory import Inventory
from classes.music import Music

# TODO: Maybe Player should inherit from pygame.Surface or pygame.sprite.Sprite?
class Player(object):
    def __init__(self):
        self.inventory = Inventory()

        self.image = SpriteSheet("media/char.png").get_sprite(0, 0, 32, 48)
        self.rect = self.image.get_rect()

        # Used to delay moving player till the collision will be checked
        # TODO: Change vector to class
        self.vector = {"x": 0, "y": 0}

        self.x = 200
        self.y = 200

        # FIXME: Connected with fixme from platform.py
        # If you consider it's stupid know that when you player he is on different position
        # till he will be updated and collide with newly created items
        self.rect.x = self.y
        self.rect.y = self.x

        # Actual sprite position
        self.sprite_col = 0
        self.sprite_row = 0

        # Used to draw sprite at certain frames
        self.frame = 0

        # Save attacking state:
        self.attacking = False
        self.attacking_time = 0

    def update(self):
        self.image = SpriteSheet("media/char.png").get_sprite(self.sprite_col*32, self.sprite_row*48, 32, 48)
        self.rect.x = self.x + Cam.x
        self.rect.y = self.y + Cam.y

        if self.attacking:
            self.attacking_time += 1;

        if self.attacking_time > 5:
            self.attacking = False
            self.attacking_time = 0

    def move_left(self):
        if not self.sprite_row == 1:
            self.frame = 0

        if self.frame % 5 == 0:
            self.sprite_col += 1
            self.sprite_row = 1
            if self.sprite_col > 3:
                self.sprite_col = 0

            self.frame = 1

        self.frame += 1

        self.vector["x"] -= 6

    def move_right(self):
        if not self.sprite_row == 2:
            self.frame = 0

        if self.frame % 4 == 0:
            self.sprite_col += 1
            self.sprite_row = 2
            if self.sprite_col > 3:
                self.sprite_col = 0

            self.frame = 1

        self.frame += 1

        self.vector["x"] += 6

    def move_top(self):
        if not self.sprite_row == 3:
            self.frame = 0

        if self.frame % 4 == 0:
            self.sprite_col += 1
            self.sprite_row = 3
            if self.sprite_col > 3:
                self.sprite_col = 0

            self.frame = 1

        self.frame += 1

        self.vector["y"] -= 6

    def move_down(self):
        if not self.sprite_row == 0:
            self.frame = 0

        if self.frame % 4 == 0:
            self.sprite_col += 1
            self.sprite_row = 0
            if self.sprite_col > 3:
                self.sprite_col = 0

            self.frame = 1

        self.frame += 1

        self.vector["y"] += 6

    def attack(self):
        if self.inventory.get_equipped_weapon():
            self.attacking = True
            Music.player_attack()